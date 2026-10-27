"""Actual F04 schema/transition regressions; dependencies required, no silent skip."""
import copy
from pathlib import Path
import sys
import unittest
from jsonschema.exceptions import ValidationError
C=Path(__file__).resolve().parents[1];sys.path.insert(0,str(C))
from synthetic_journal import SyntheticJournal

NOW='2026-10-27T12:00:00Z'
LATER='2026-10-27T12:01:00Z'
IDENTITY=dict(client_id='synthetic-client',source_system='synthetic-ads',source_event_id='event-1',action_scope='synthetic-observe',approved_revision='revision-1')
from test_ads_policy import fixture
INTENT=fixture()[0]
INTENT['payload_ref']='synthetic-payload'

def scenario(outcome='OCCURRED'):
    proofs={}
    def verifier(raw):
        if raw not in proofs:raise ValueError('UNAUTHENTICATED_ORIGINAL_BYTES')
        return proofs[raw]
    j=SyntheticJournal(verifier);r=j.reserve(IDENTITY,INTENT,now=NOW);key=r['action_key'];j.record_prerecorded_unknown(key,now=NOW,approval_ref='synthetic-approval')
    proofs[b'original']=dict(action_key=key,account_ref=INTENT['account_ref'],provider_ref=INTENT['provider_ref'],campaign_ref=INTENT['campaign_ref'],revision=INTENT['revision'],outcome=outcome,provider_object_ref='synthetic-object' if outcome=='OCCURRED' else None,observed_at=NOW,event_ref='synthetic-proof',evidence_ref='synthetic-readback')
    return j,key,proofs,verifier

class JournalTests(unittest.TestCase):
    def test_duplicate_deepcopy_and_changed_intent(self):
        j=SyntheticJournal(lambda x:None);r=j.reserve(IDENTITY,INTENT,now=NOW);r['action_identity']['client_id']='mutated'
        again=j.reserve(IDENTITY,INTENT,now=NOW);self.assertEqual(IDENTITY,again['action_identity'])
        before=j.snapshot()
        with self.assertRaises(ValueError):j.reserve(IDENTITY,dict(INTENT,payload_ref='changed'),now=NOW)
        self.assertEqual(before,j.snapshot())
        for field,value in [('amount_minor',101),('currency','EUR'),('channels',('tracking',)),('asset_refs',('other-asset',))]:
            with self.subTest(field=field),self.assertRaises(ValueError):j.reserve(IDENTITY,dict(INTENT,**{field:value}),now=NOW)
        self.assertEqual(before,j.snapshot())
    def test_unknown_never_retries(self):
        j,key,_,_=scenario();before=j.snapshot();self.assertEqual('UNKNOWN',j.reserve(IDENTITY,INTENT,now=LATER)['status'])
        with self.assertRaises(ValueError):j.record_prerecorded_unknown(key,now=LATER,approval_ref='synthetic-approval')
        self.assertEqual(before,j.snapshot())
    def test_confirmed_history_distinct_runtime_and_restore_hold(self):
        j,key,_,v=scenario();before=j.snapshot();r=j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
        self.assertEqual(('RECONCILED','CONFIRMED',True),(r['status'],r['outbound_state'],r['reservation_retained']))
        self.assertEqual(before['actions'][key]['history'],j.snapshot()['actions'][key]['history'][:-1]);self.assertEqual('HOLD',j.outbound_state)
        import json
        restored=SyntheticJournal.restore(json.loads(json.dumps(j.snapshot())),v);self.assertEqual(j.snapshot(),restored.snapshot());self.assertEqual('HOLD',restored.outbound_state)
        self.assertEqual(r,restored.reconcile(key,b'original',now=LATER,max_age_seconds=120))
    def test_not_occurred_tombstone_not_retry(self):
        j,key,_,v=scenario('NOT_OCCURRED');r=j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
        self.assertEqual(('HOLD',False,None),(r['outbound_state'],r['reservation_retained'],r['provider_object_ref']))
        self.assertEqual(r,j.reserve(IDENTITY,INTENT,now=LATER));self.assertEqual(r,SyntheticJournal.restore(j.snapshot(),v).reserve(IDENTITY,INTENT,now=LATER))
    def test_wrong_bindings_stale_and_original_bytes_no_mutation(self):
        for field,value in [('account_ref','other'),('provider_ref','other'),('campaign_ref','other'),('revision','other'),('action_key','sha256:'+'0'*64),('observed_at','2026-10-26T12:00:00Z'),('observed_at','2026-10-28T12:00:00Z'),('provider_object_ref',None),('outcome','MAYBE')]:
            j,key,p,_=scenario();p[b'original'][field]=value;before=j.snapshot()
            with self.subTest(field=field),self.assertRaises(ValueError):j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
            self.assertEqual(before,j.snapshot())
        j,key,_,_=scenario();before=j.snapshot()
        with self.assertRaises(ValueError):j.reconcile(key,b'reencoded',now=LATER,max_age_seconds=120)
        self.assertEqual(before,j.snapshot())
    def test_replay_changed_proof_rejected(self):
        j,key,p,_=scenario();j.reconcile(key,b'original',now=LATER,max_age_seconds=120);before=j.snapshot();p[b'original']['provider_object_ref']='changed'
        with self.assertRaises(ValueError):j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
        self.assertEqual(before,j.snapshot())
    def test_restore_corruption_closed_shapes_and_chronology(self):
        j,key,_,v=scenario();j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
        mutations=[lambda s:s.update(outbound_state='CONFIRMED'),lambda s:s.update(secret='x'),lambda s:s['actions'][key].update(intent_fingerprint='0'*64),lambda s:s['actions'][key]['history'][1].update(action_key='sha256:'+'0'*64),lambda s:s['actions'][key]['history'][-1].update(recorded_at='2026-10-26T12:00:00Z'),lambda s:s['proofs'].clear(),lambda s:s['actions'][key]['history'][0].update(status='UNKNOWN')]
        for mutate in mutations:
            state=j.snapshot();mutate(state)
            with self.assertRaises((ValueError,KeyError,ValidationError)):SyntheticJournal.restore(state,v)
    def test_no_error_contains_supplied_secret(self):
        j=SyntheticJournal(lambda x:None)
        with self.assertRaises(ValueError) as caught:j.reserve(IDENTITY,dict(INTENT,payload_ref='secret with spaces'),now=NOW)
        self.assertNotIn('secret with spaces',str(caught.exception))


class JournalReviewRegressionTests(unittest.TestCase):
    def test_fresh_pre_submission_proof_rejected_without_mutation(self):
        # Old code accepts this exactly-fresh absence proof (120 seconds old),
        # even though it predates the recorded submission/UNKNOWN attempt.
        for outcome in ('NOT_OCCURRED','OCCURRED'):
            j,key,proofs,_=scenario(outcome)
            proofs[b'original']['observed_at']='2026-10-27T11:59:00Z'
            before=j.snapshot()
            with self.subTest(outcome=outcome),self.assertRaises(ValueError):
                j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
            self.assertEqual(before,j.snapshot())
            self.assertEqual('UNKNOWN',before['actions'][key]['history'][-1]['status'])
            self.assertIs(before['actions'][key]['history'][-1]['reservation_retained'],True)

    def test_attempt_boundary_and_exact_proof_replay_remain_positive(self):
        for outcome in ('OCCURRED','NOT_OCCURRED'):
            j,key,proofs,verifier=scenario(outcome)
            # Equality with original submission/UNKNOWN is valid, including the
            # exact freshness boundary; reconciliation is recorded later.
            proofs[b'original']['observed_at']=NOW
            receipt=j.reconcile(key,b'original',now='2026-10-27T12:02:00Z',max_age_seconds=120)
            before=j.snapshot()
            self.assertEqual(receipt,j.reconcile(key,b'original',now='2026-10-27T12:02:00Z',max_age_seconds=120))
            self.assertEqual(before,j.snapshot())
            restored=SyntheticJournal.restore(before,verifier)
            self.assertEqual(receipt,restored.reconcile(key,b'original',now='2026-10-27T12:02:00Z',max_age_seconds=120))
            self.assertEqual(before,restored.snapshot())
            self.assertEqual('HOLD',restored.outbound_state)

    def test_same_native_event_across_account_provider_client_namespaces(self):
        for partition in ('account_ref','provider_ref','client_ref'):
            j,first,proofs,verifier=scenario()
            second_intent=copy.deepcopy(INTENT);second_intent[partition]='synthetic-other-'+partition
            second_identity=dict(IDENTITY,source_event_id='event-2')
            second_identity['client_id']=second_intent['client_ref']
            second=j.reserve(second_identity,second_intent,now=NOW)['action_key']
            j.record_prerecorded_unknown(second,now=NOW,approval_ref='synthetic-approval-2')
            second_proof=copy.deepcopy(proofs[b'original']);second_proof['action_key']=second
            for field in ('account_ref','provider_ref','campaign_ref','revision'):second_proof[field]=second_intent[field]
            proofs[b'second-original']=second_proof
            first_receipt=j.reconcile(first,b'original',now=LATER,max_age_seconds=120)
            with self.subTest(partition=partition):
                second_receipt=j.reconcile(second,b'second-original',now=LATER,max_age_seconds=120)
                self.assertEqual('CONFIRMED',second_receipt['outbound_state'])
                self.assertEqual(first_receipt['reconciliation_ref'],second_receipt['reconciliation_ref'])
                self.assertNotEqual(first_receipt['action_key'],second_receipt['action_key'])
                self.assertEqual(2,len(j.snapshot()['proofs']))
                restored=SyntheticJournal.restore(j.snapshot(),verifier)
                self.assertEqual(j.snapshot(),restored.snapshot())
                self.assertEqual(second_receipt,restored.reconcile(second,b'second-original',now=LATER,max_age_seconds=120))

    def test_same_namespace_event_reuse_for_other_action_rejected(self):
        j,first,proofs,_=scenario()
        second_identity=dict(IDENTITY,source_event_id='event-2')
        second=j.reserve(second_identity,INTENT,now=NOW)['action_key']
        j.record_prerecorded_unknown(second,now=NOW,approval_ref='synthetic-approval-2')
        proofs[b'second-original']=dict(proofs[b'original'],action_key=second)
        j.reconcile(first,b'original',now=LATER,max_age_seconds=120)
        before=j.snapshot()
        with self.assertRaises(ValueError):j.reconcile(second,b'second-original',now=LATER,max_age_seconds=120)
        self.assertEqual(before,j.snapshot())
        proofs[b'original']['evidence_ref']='changed-proof-same-namespace'
        with self.assertRaises(ValueError):j.reconcile(first,b'original',now=LATER,max_age_seconds=120)
        self.assertEqual(before,j.snapshot())

    def test_v2_replay_index_proof_and_history_restore_coherence(self):
        import json
        from synthetic_journal import fingerprint
        j,key,_,verifier=scenario();j.reconcile(key,b'original',now=LATER,max_age_seconds=120)
        original=j.snapshot();self.assertEqual(2,original['version'])
        event=next(iter(original['proofs']))
        namespace=json.loads(event)
        self.assertEqual([INTENT['client_ref'],INTENT['provider_ref'],INTENT['account_ref'],'synthetic-proof'],namespace)
        for mutation in ('wrong-namespace','digest','proof-before-attempt','proof-after-receipt','receipt-outcome-mismatch','unknown-entry-field'):
            state=copy.deepcopy(original);entry=state['proofs'][event]
            if mutation=='wrong-namespace':state['proofs']['synthetic-proof']=state['proofs'].pop(event)
            elif mutation=='digest':entry['proof_digest']='0'*64
            elif mutation=='unknown-entry-field':entry['unreviewed']=True
            else:
                if mutation=='proof-before-attempt':entry['proof']['observed_at']='2026-10-27T11:59:00Z'
                elif mutation=='proof-after-receipt':entry['proof']['observed_at']='2026-10-27T12:02:00Z'
                else:entry['proof']['evidence_ref']='different-from-historical-receipt'
                entry['proof_digest']=fingerprint(entry['proof'])
            before=copy.deepcopy(state)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):SyntheticJournal.restore(state,verifier)
            self.assertEqual(before,state)
        restored=SyntheticJournal.restore(json.loads(json.dumps(original)),verifier)
        self.assertEqual(original,restored.snapshot())

    def test_explicit_legacy_unreconciled_migration_and_ambiguous_rejection(self):
        j,key,_,verifier=scenario();legacy=j.snapshot();legacy['version']=1
        # Empty-proof UNKNOWN history is losslessly migratable, still held.
        original=copy.deepcopy(legacy);restored=SyntheticJournal.restore(legacy,verifier)
        self.assertEqual(2,restored.snapshot()['version']);self.assertEqual(original,legacy)
        self.assertEqual(original['actions'],restored.snapshot()['actions']);self.assertEqual('HOLD',restored.outbound_state)
        j.reconcile(key,b'original',now=LATER,max_age_seconds=120);v2=j.snapshot();legacy=copy.deepcopy(v2);legacy['version']=1
        entry=next(iter(v2['proofs'].values()))
        legacy['proofs']={'synthetic-proof':{'action_key':key,'proof_digest':entry['proof_digest']}}
        before=copy.deepcopy(legacy)
        # V1 never stored authenticated observed_at, so accepting it would
        # silently bypass the new attempt chronology and namespace coherence.
        with self.assertRaises(ValueError):SyntheticJournal.restore(legacy,verifier)
        self.assertEqual(before,legacy)
