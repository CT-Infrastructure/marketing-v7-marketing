import copy
import dataclasses as dc
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import mock as m

NOW="2026-10-25T12:00:00Z"
OLD="2026-10-25T11:59:30Z"
END="2026-10-25T13:00:00Z"
def fixture():
    b=dict(client_ref="synthetic-client",subject_ref="synthetic-subject",channel="sms",purpose="synthetic-purpose",account_ref="synthetic-account",jurisdiction="synthetic-jurisdiction",provider_ref="synthetic-provider")
    pr=m.privacy.Request(**b,now=NOW,max_age_seconds=60)
    perm=m.privacy.Permission(**b,source_authority="Mautic.sms",granted=True,revoked=False,authority_available=True,valid_from=OLD,expires_at=END,observed_at=OLD,evidence_ref="synthetic-permission")
    life=m.privacy.Lifecycle(client_ref=b["client_ref"],subject_ref=b["subject_ref"],deleted=False,suppressed=False,authority_available=True,observed_at=OLD,retention_until=END,authority_generation=1,applied_generation=1,restore_epoch=None,replay_complete=False,replay_evidence_ref=None,evidence_ref="synthetic-life")
    rb={k:v for k,v in b.items() if k!="subject_ref"}
    reviews=tuple(m.privacy.Review(**rb,kind=k,status="APPROVED",revoked=False,reviewer_role=role,observed_at=OLD,expires_at=END,evidence_ref="synthetic-review") for k,role in m.privacy.REVIEW_ROLES.items())
    identity=dict(client_id=b["client_ref"],source_system="synthetic-mautic",source_event_id="synthetic-event",action_scope="synthetic-sms",approved_revision="synthetic-revision")
    req=dict(identity=identity,privacy=pr,content_revision="synthetic-revision",assets=(),**{k:v for k,v in b.items() if k not in ("client_ref","channel")})
    approval=dict(ref="synthetic-approval",owner="synthetic-owner",status="APPROVED",revision="synthetic-revision",assets=(),observed_at=OLD,expires_at=END,**{k:v for k,v in b.items() if k!="channel"})
    args=dict(permission=perm,lifecycle=life,reviews=reviews,approval=approval,now=NOW,at=NOW,max_age=60)
    return req,args
class Tests(unittest.TestCase):
    def setUp(self):
        self.req,self.args=fixture()
        self.mock=m.Mock(m.SyntheticVerifier({}))
    def reject(self, req=None, args=None):
        before=self.mock.snapshot()
        with self.assertRaises(ValueError):
            self.mock.intake(req or self.req,**(args or self.args))
        self.assertEqual(before,self.mock.snapshot())
    def test_positive_held_dedupe_immutable(self):
        a=self.mock.intake(self.req,**self.args)
        self.assertEqual(a["status"],"HELD")
        self.assertEqual(a["outbound_state"],"HOLD")
        a["action_identity"]["client_id"]="synthetic-mutated"
        b=self.mock.intake(self.req,**self.args)
        self.assertEqual(b["action_identity"]["client_id"],"synthetic-client")
        self.req["identity"]["client_id"]="synthetic-mutated"
        self.assertEqual(self.mock.snapshot()["actions"][b["action_key"]]["history"][-1],b)
    def test_permission_matrix(self):
        changes=[("channel","email"),("channel","phone"),("source_authority","Mautic"),("revoked",True),("granted",False),("authority_available",False),("expires_at",NOW),("observed_at","2026-10-25T11:58:59Z")]
        changes += [(f,"synthetic-wrong") for f in ("client_ref","subject_ref","account_ref","purpose","provider_ref","jurisdiction")]
        for f,v in changes:
            with self.subTest(field=f,value=v):
                a=dict(self.args,permission=dc.replace(self.args["permission"],**{f:v}))
                self.reject(args=a)
        self.reject(args=dict(self.args,permission=None))
    def test_stop_suppression_retention_restore(self):
        for field,val in (("suppressed",True),("deleted",True),("authority_available",False),("retention_until",None),("retention_until",NOW),("applied_generation",0),("restore_epoch","synthetic-epoch")):
            with self.subTest(field=field):
                self.reject(args=dict(self.args,lifecycle=dc.replace(self.args["lifecycle"],**{field:val})))
    def test_review_matrix(self):
        for index in range(2):
            for field,val in [("revoked",True),("status","REVOKED"),("observed_at","2026-10-25T11:58:00Z"),("expires_at",NOW)]+[(f,"synthetic-wrong") for f in ("client_ref","account_ref","purpose","jurisdiction","provider_ref","reviewer_role")]:
                rev=list(self.args["reviews"])
                rev[index]=dc.replace(rev[index],**{field:val})
                with self.subTest(index=index,field=field):
                    self.reject(args=dict(self.args,reviews=tuple(rev)))
            self.reject(args=dict(self.args,reviews=(self.args["reviews"][index],)))
            self.reject(args=dict(self.args,reviews=self.args["reviews"]+(self.args["reviews"][index],)))
    def test_approval_bindings(self):
        for f in self.args["approval"]:
            a=copy.deepcopy(self.args)
            a["approval"][f]=True
            with self.subTest(field=f): self.reject(args=a)
    def test_time_before_mutation_fresh_and_duplicate(self):
        invalid=[None,True,False,0,1.2,float("nan"),float("inf"),"99999-01-01T00:00:00Z","2026-10-25T12:00:01Z","2026-10-25T11:58:59Z"]
        for duplicate in (False,True):
            if duplicate:self.mock.intake(self.req,**self.args)
            for value in invalid:
                self.reject(args=dict(self.args,at=value))
            for value in invalid[:8]:
                self.reject(args=dict(self.args,now=value))
            for value in (True,0,-1,float("inf"),"60"):
                self.reject(args=dict(self.args,max_age=value))
    def test_changed_intent(self):
        self.mock.intake(self.req,**self.args)
        a=copy.deepcopy(self.args);a["approval"]["ref"]="synthetic-other"
        self.reject(args=a)
    def unknown(self,outcome="OCCURRED",at=NOW):
        action_key=m.key(self.req["identity"])
        proof=dict(action_key=action_key,account_ref="synthetic-account",provider_ref="synthetic-provider",object_ref="synthetic-object" if outcome=="OCCURRED" else None,event_ref="synthetic-callback",at=at,outcome=outcome,evidence_ref="synthetic-readback")
        verifier=m.SyntheticVerifier({b"synthetic-original":proof})
        self.mock=m.Mock(verifier)
        a=self.mock.intake(self.req,**dict(self.args,disposition="TIMEOUT_AFTER_SUBMIT"))
        proof["account_ref"]="synthetic-mutated"
        self.assertEqual(a["status"],"UNKNOWN")
        return action_key
    def test_unknown_reconciliation_history_restore_tombstone(self):
        for outcome in ("OCCURRED","NOT_OCCURRED"):
            k=self.unknown(outcome)
            original=self.mock.snapshot()["actions"][k]["history"]
            a=self.mock.reconcile(k,b"synthetic-original",now=NOW,max_age=60)
            self.assertEqual(a["status"],"RECONCILED")
            self.assertEqual(a["reservation_retained"],outcome=="OCCURRED")
            self.assertEqual(self.mock.snapshot()["actions"][k]["history"][:-1],original)
            restored=m.Mock.restore(self.mock.snapshot(),self.mock._verifier)
            self.assertEqual(restored.outbound_state,"HOLD")
            self.assertEqual(restored.intake(self.req,**self.args),a)
            self.assertEqual(restored.reconcile(k,b"synthetic-original",now=NOW,max_age=60),a)
            a["action_identity"]["client_id"]="synthetic-mutation"
            self.assertEqual(restored.snapshot(),self.mock.snapshot())
    def test_callback_original_bytes_wrong_bindings_time(self):
        k=self.unknown()
        for body in (b"tamper",{},True):
            before=self.mock.snapshot()
            with self.assertRaises(ValueError):self.mock.reconcile(k,body,now=NOW,max_age=60)
            self.assertEqual(before,self.mock.snapshot())
        for f,v in (("account_ref","synthetic-wrong"),("provider_ref","synthetic-wrong"),("action_key","sha256:"+"0"*64),("at","2026-10-25T12:00:00.000001Z")):
            k=self.unknown()
            self.mock._verifier._fixtures[b"synthetic-original"][f]=v
            before=self.mock.snapshot()
            with self.assertRaises(ValueError):self.mock.reconcile(k,b"synthetic-original",now=NOW,max_age=60)
            self.assertEqual(before,self.mock.snapshot())
    def test_fractional_equal_rollover_chronology(self):
        self.assertEqual(m.clock("2026-10-26T00:00:00Z","2026-10-25T23:59:59.999999Z",60)[0].day,26)
        k=self.unknown(at="2026-10-25T11:59:59.999999Z")
        with self.assertRaises(ValueError):self.mock.reconcile(k,b"synthetic-original",now=NOW,max_age=60)
    def test_restore_corruption(self):
        k=self.unknown()
        snap=self.mock.snapshot()
        variants=[]
        for field,val in (("receipt_id","synthetic-fake"),("outbound_state","ACTIVE"),("attempt",True),("status","REJECTED"),("recorded_at","invalid"),("reservation_retained",False)):
            s=copy.deepcopy(snap);s["actions"][k]["history"][-1][field]=val;variants.append(s)
        s=copy.deepcopy(snap);s["actions"][k]["history"].pop(0);variants.append(s)
        for s in variants:
            with self.assertRaises(ValueError):m.Mock.restore(s,self.mock._verifier)
    def test_manifest_recursive_closed(self):
        expected=copy.deepcopy(m.EXPECTED)
        self.assertEqual(m.validate_manifest(expected),"HOLD")
        def mutations(obj,path=()):
            if isinstance(obj,dict):
                for k,v in obj.items():
                    yield path+(k,),True
                    yield from mutations(v,path+(k,))
        for path,val in mutations(expected):
            s=copy.deepcopy(expected);a=s
            for k in path[:-1]:a=a[k]
            a[path[-1]]=val
            with self.subTest(path=path):
                with self.assertRaises(ValueError):m.validate_manifest(s)
        s=copy.deepcopy(expected);s["enabled"]=True
        with self.assertRaises(ValueError):m.validate_manifest(s)
    def test_secret_shaped_input_not_echoed(self):
        for v in ("person@example.invalid","+15550000000","secret-token-value","https://invalid.test","../private"):
            q=copy.deepcopy(self.req);q["subject_ref"]=v
            try:self.mock.intake(q,**self.args)
            except ValueError as e:self.assertNotIn(v,str(e))
            else:self.fail("unsafe reference accepted")
    def test_freshness_and_expiry_boundaries(self):
        a=dict(self.args,now="2026-10-25T12:00:30Z")
        self.assertEqual(self.mock.intake(self.req,**a)["outbound_state"],"HOLD")
        self.reject(args=dict(a,now="2026-10-25T12:00:30.000001Z"))
        self.reject(args=dict(self.args,now=END,at=END))
    def test_restored_generation_and_receipt_bindings(self):
        life=dc.replace(self.args["lifecycle"],restore_epoch="synthetic-epoch",replay_complete=True,replay_evidence_ref="synthetic-replay")
        receipt=m.privacy.ReplayReceipt(client_ref="synthetic-client",subject_ref="synthetic-subject",restore_epoch="synthetic-epoch",generation=1,completed=True,authority_available=True,observed_at=OLD,evidence_ref="synthetic-replay")
        args=dict(self.args,lifecycle=life,replay_receipt=receipt)
        self.assertEqual(self.mock.intake(self.req,**args)["outbound_state"],"HOLD")
        for field,val in (("generation",0),("generation",True),("completed",False),("authority_available",False),("restore_epoch","synthetic-other"),("evidence_ref","synthetic-other"),("observed_at","2026-10-25T11:58:00Z")):
            self.reject(args=dict(args,replay_receipt=dc.replace(receipt,**{field:val})))
    def test_asset_rights_missing_mismatch_revoked(self):
        req=copy.deepcopy(self.req);req["assets"]=("synthetic-asset",)
        req["privacy"]=dc.replace(req["privacy"],asset_refs=req["assets"])
        args=copy.deepcopy(self.args);args["approval"]["assets"]=req["assets"]
        self.reject(req=req,args=args)
        right=m.privacy.AssetRight(asset_ref="synthetic-asset",client_ref="synthetic-client",purpose="synthetic-purpose",account_ref="synthetic-account",revoked=False,valid_from=OLD,expires_at=END,observed_at=OLD,evidence_ref="synthetic-right")
        self.assertEqual(self.mock.intake(req,**dict(args,rights=(right,)))["outbound_state"],"HOLD")
        for field,val in (("asset_ref","synthetic-other"),("client_ref","synthetic-other"),("revoked",True),("expires_at",NOW)):
            self.reject(req=req,args=dict(args,rights=(dc.replace(right,**{field:val}),)))
    def test_definitive_rejection_is_terminal(self):
        a=self.mock.intake(self.req,**dict(self.args,disposition="REJECTED"))
        self.assertEqual(a["status"],"REJECTED")
        self.assertEqual(self.mock.intake(self.req,**self.args),a)
        self.assertTrue(a["reservation_retained"])
    def test_restore_replay_corruption(self):
        k=self.unknown()
        self.mock.reconcile(k,b"synthetic-original",now=NOW,max_age=60)
        snap=self.mock.snapshot()
        for mode in ("missing","wrong","orphan","intent","extra"):
            s=copy.deepcopy(snap)
            if mode=="missing":s["events"]={}
            elif mode=="wrong":s["events"]["synthetic-callback"]["account_ref"]="synthetic-other"
            elif mode=="orphan":s["events"]["synthetic-callback"]["action_key"]="sha256:"+"0"*64
            elif mode=="intent":s["actions"][k]["intent"]["enabled"]=True
            else:s["enabled"]=True
            with self.assertRaises(ValueError):m.Mock.restore(s,self.mock._verifier)
    def test_callback_invalid_clock_no_mutation(self):
        k=self.unknown()
        for now in (None,True,0,float("nan"),float("inf"),"99999-01-01T00:00:00Z"):
            before=self.mock.snapshot()
            with self.assertRaises(ValueError):self.mock.reconcile(k,b"synthetic-original",now=now,max_age=60)
            self.assertEqual(before,self.mock.snapshot())
    def test_no_network_process_or_private_database(self):
        source=(Path(m.__file__)).read_text()
        for text in ("import socket","import subprocess","import urllib","import boto","sqlite3"):
            self.assertNotIn(text,source)
        self.assertEqual(m.f05.error_decision("NOT_FOUND",submitted=True),"UNKNOWN")
        self.assertEqual(self.mock.snapshot()["actions"],{})
if __name__=="__main__":unittest.main()
