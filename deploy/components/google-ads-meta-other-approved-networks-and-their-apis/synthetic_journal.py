"""Append-only synthetic receipt history; never a provider client or durable store."""
import copy
import hashlib
import json
from ads_policy import opaque, require, validate_intent, INTENT_FIELDS
from assemble_inputs import load_dependency

RUNTIME_OUTBOUND_STATE='HOLD'
IDENTITY_FIELDS={'client_id','source_system','source_event_id','action_scope','approved_revision'}

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)

def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

PROOF_FIELDS={'action_key','account_ref','provider_ref','campaign_ref','revision','outcome',
              'provider_object_ref','observed_at','event_ref','evidence_ref'}

def replay_identity(intent,event_ref):
    """Opaque native IDs are unique only within client/provider/account scope."""
    return canonical([intent['client_ref'],intent['provider_ref'],intent['account_ref'],event_ref])

def validate_reconciliation_proof(action,key,proof):
    """Bind to original attempt history, never a later RECONCILED timestamp."""
    f16=load_dependency('f16')
    require(type(proof) is dict and set(proof)==PROOF_FIELDS)
    require(proof['action_key']==key)
    require(all(proof[k]==action['intent'][k] for k in ('account_ref','provider_ref','campaign_ref','revision')))
    require(proof['outcome'] in ('OCCURRED','NOT_OCCURRED') and opaque(proof['event_ref']) and opaque(proof['evidence_ref']))
    require((proof['outcome']=='OCCURRED' and opaque(proof['provider_object_ref'])) or (proof['outcome']=='NOT_OCCURRED' and proof['provider_object_ref'] is None))
    submission=[r for r in action['history'] if r['status']=='SUBMITTED']
    unknown=[r for r in action['history'] if r['status']=='UNKNOWN']
    require(len(submission)==len(unknown)==1)
    bound=max(f16.instant(submission[0]['recorded_at']),f16.instant(unknown[0]['recorded_at']))
    observed=f16.instant(proof['observed_at'])
    require(observed>=bound)
    return observed

class SyntheticJournal:
    """The trusted verifier maps original bytes to authenticated fixture evidence.

    No bytes are parsed as self-authenticating proof. Histories model prerecorded
    outcomes only. CONFIRMED is historical receipt truth, never runtime authority.
    """
    def __init__(self,verifier):
        require(callable(verifier));self._verifier=verifier;self._actions={};self._proofs={}

    @property
    def outbound_state(self): return 'HOLD'

    def reserve(self,identity,intent,*,now):
        f04=load_dependency('f04');f16=load_dependency('f16')
        require(type(identity) is dict and set(identity)==IDENTITY_FIELDS)
        require(all(opaque(x) for x in identity.values()))
        require(type(intent) is dict and set(intent)==INTENT_FIELDS|{'payload_ref'})
        require(opaque(intent['payload_ref']))
        validate_intent({k:v for k,v in intent.items() if k!='payload_ref'},now)
        require(identity['approved_revision']==intent['revision'] and identity['client_id']==intent['client_ref'])
        f16.instant(now)
        key=f04.action_key(identity);digest=fingerprint(intent)
        if key in self._actions:
            require(self._actions[key]['intent_fingerprint']==digest)
            return copy.deepcopy(self._actions[key]['history'][-1])
        receipt={'schema_version':'1.0','receipt_id':'receipt-'+fingerprint([key,0])[:32],
            'action_identity':copy.deepcopy(identity),'action_key':key,'event_id':identity['source_event_id'],
            'correlation_id':'correlation-'+fingerprint(key)[:24],'approval_ref':None,
            'destination':intent['provider_ref'],'attempt':1,'recorded_at':now,'status':'HELD',
            'provider_object_ref':None,'evidence_ref':'synthetic-reservation','reconciliation_ref':None,
            'outbound_state':'HOLD','reservation_retained':True,'reconciliation_outcome':None}
        f04.validate('action-receipt',receipt)
        self._actions[key]={'intent':json.loads(canonical(intent)),'intent_fingerprint':digest,'history':[receipt]}
        return copy.deepcopy(receipt)

    def _next(self,key,status,now,**changes):
        f04=load_dependency('f04');old=self._actions[key]['history'][-1];new=copy.deepcopy(old)
        new.update(status=status,recorded_at=now,receipt_id='receipt-'+fingerprint([key,len(self._actions[key]['history'])])[:32],**changes)
        f04.check_transition(old,new)
        return new

    def record_prerecorded_unknown(self,key,*,now,approval_ref):
        """Describe a prerecorded ambiguous effect; performs no submit operation."""
        require(key in self._actions and opaque(approval_ref))
        history=self._actions[key]['history'];require(history[-1]['status']=='HELD')
        submitted=self._next(key,'SUBMITTED',now,approval_ref=approval_ref)
        # Validate the second transition before mutating either history entry.
        unknown=copy.deepcopy(submitted);unknown.update(status='UNKNOWN',receipt_id='receipt-'+fingerprint([key,len(history)+1])[:32])
        load_dependency('f04').check_transition(submitted,unknown)
        history.extend([submitted,unknown]);return copy.deepcopy(unknown)

    def reconcile(self,key,original_bytes,*,now,max_age_seconds):
        require(type(original_bytes) is bytes and key in self._actions)
        f16=load_dependency('f16');clock=f16.instant(now)
        require(type(max_age_seconds) is int and max_age_seconds>0)
        proof=copy.deepcopy(self._verifier(original_bytes))
        action=self._actions[key]
        validate_reconciliation_proof(action,key,proof)
        require(f16.fresh(proof['observed_at'],clock,max_age_seconds))
        pd=fingerprint(proof);event=replay_identity(action['intent'],proof['event_ref'])
        entry={'action_key':key,'proof_digest':pd,'proof':copy.deepcopy(proof)}
        if event in self._proofs:
            require(self._proofs[event]==entry)
            return copy.deepcopy(action['history'][-1])
        require(action['history'][-1]['status']=='UNKNOWN')
        receipt=self._next(key,'RECONCILED',now,provider_object_ref=proof['provider_object_ref'],
            evidence_ref=proof['evidence_ref'],reconciliation_ref=proof['event_ref'],reconciliation_outcome=proof['outcome'],
            outbound_state='CONFIRMED' if proof['outcome']=='OCCURRED' else 'HOLD',reservation_retained=proof['outcome']=='OCCURRED')
        action['history'].append(receipt);self._proofs[event]=entry
        return copy.deepcopy(receipt)

    def snapshot(self):
        return copy.deepcopy({'version':2,'outbound_state':'HOLD','actions':self._actions,'proofs':self._proofs})

    @classmethod
    def restore(cls,state,verifier):
        require(type(state) is dict and set(state)=={'version','outbound_state','actions','proofs'})
        require(type(state['version']) is int and state['version'] in (1,2) and state['outbound_state']=='HOLD')
        # V1 retained only a digest, so reconciled proof chronology cannot be
        # validated or reconstructed. Migrate only unreconciled V1 snapshots.
        # Reconciled V1 requires separate authenticated evidence recovery, not
        # silently accepting history or inventing missing proof fields.
        require(state['version']==2 or not state['proofs'])
        require(type(state['actions']) is dict and type(state['proofs']) is dict)
        candidate=copy.deepcopy(state);f04=load_dependency('f04');events={}
        for key,action in candidate['actions'].items():
            require(type(action) is dict and set(action)=={'intent','intent_fingerprint','history'})
            require(type(action['intent']) is dict and set(action['intent'])==INTENT_FIELDS|{'payload_ref'})
            require(opaque(action['intent']['payload_ref']))
            require(type(action['intent']['asset_refs']) is list and type(action['intent']['channels']) is list)
            restored_intent=copy.deepcopy(action['intent']);restored_intent.pop('payload_ref')
            restored_intent['asset_refs']=tuple(restored_intent['asset_refs']);restored_intent['channels']=tuple(restored_intent['channels'])
            require(fingerprint(action['intent'])==action['intent_fingerprint'])
            history=action['history'];require(type(history) is list and bool(history) and history[0]['status']=='HELD')
            validate_intent(restored_intent,history[0]['recorded_at'])
            require(history[0]['approval_ref'] is None and history[0]['provider_object_ref'] is None and history[0]['reconciliation_ref'] is None and history[0]['reservation_retained'] is True)
            ids=set()
            for i,receipt in enumerate(history):
                f04.validate('action-receipt',receipt);require(receipt['action_key']==key and receipt['destination']==action['intent']['provider_ref'] and receipt['action_identity']['approved_revision']==action['intent']['revision'] and receipt['action_identity']['client_id']==action['intent']['client_ref'])
                require(receipt['receipt_id']=='receipt-'+fingerprint([key,i])[:32])
                require(receipt['attempt']==1 and receipt['correlation_id']=='correlation-'+fingerprint(key)[:24])
                require(receipt['receipt_id'] not in ids);ids.add(receipt['receipt_id'])
                if i:f04.check_transition(history[i-1],receipt)
            last=history[-1]
            if last['status']=='RECONCILED':
                event=replay_identity(action['intent'],last['reconciliation_ref'])
                require(event not in events);events[event]=key
        require(set(events)==set(candidate['proofs']))
        for event,entry in candidate['proofs'].items():
            require(type(entry) is dict and set(entry)=={'action_key','proof_digest','proof'} and entry['action_key']==events[event])
            key=entry['action_key'];action=candidate['actions'][key];last=action['history'][-1]
            proof=entry['proof'];observed=validate_reconciliation_proof(action,key,proof)
            require(event==replay_identity(action['intent'],proof['event_ref']))
            require(entry['proof_digest']==fingerprint(proof))
            require(observed<=load_dependency('f16').instant(last['recorded_at']))
            require(all(proof[p]==last[r] for p,r in (('event_ref','reconciliation_ref'),
                    ('outcome','reconciliation_outcome'),('provider_object_ref','provider_object_ref'),
                    ('evidence_ref','evidence_ref'))))
        obj=cls(verifier);obj._actions=candidate['actions'];obj._proofs=candidate['proofs'];return obj
