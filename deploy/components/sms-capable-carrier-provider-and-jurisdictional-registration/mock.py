"""CP141 single-caller synthetic model. No transport implementation."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from dataclasses import replace

ROOT = Path(__file__).resolve().parents[3]
INPUTS = Path(__file__).resolve().parent / "inputs"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, INPUTS / Path(path).relative_to("inputs"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
f05 = load("cp141_f05", "inputs/F05/contracts/adapters/contract.py")
privacy = load("cp141_f16", "inputs/F16/contracts/privacy/eligibility.py")
from policy import EXPECTED

def require(ok):
    if not ok:
        raise ValueError("INVALID_SYNTHETIC_CONTRACT")
def closed(actual, expected):
    require(type(actual) is type(expected))
    if type(expected) is dict:
        require(set(actual) == set(expected))
        for k in expected:
            closed(actual[k], expected[k])
    elif type(expected) is list:
        require(len(actual) == len(expected))
        for a,b in zip(actual,expected):
            closed(a,b)
    else:
        require(actual == expected)
def validate_manifest(value):
    closed(value, EXPECTED)
    return "HOLD"
def ref(value):
    require(type(value) is str and re.fullmatch(r"synthetic-[a-z0-9-]{1,80}",value) is not None)
def clock(now, at, max_age):
    require(type(max_age) is int and max_age > 0)
    n, a = privacy.instant(now), privacy.instant(at)
    require(0 <= (n-a).total_seconds() <= max_age)
    return n,a
FIELDS = ("client_id","source_system","source_event_id","action_scope","approved_revision")
def key(identity):
    require(type(identity) is dict and set(identity)==set(FIELDS))
    for value in identity.values(): ref(value)
    data=json.dumps([identity[k] for k in FIELDS],ensure_ascii=False,separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(data).hexdigest()
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

class SyntheticVerifier:
    """Trusted fixture registry over ORIGINAL bytes, not vendor authentication."""
    def __init__(self, fixtures):
        require(type(fixtures) is dict)
        self._fixtures=copy.deepcopy(fixtures)
    def verify(self, raw):
        require(type(raw) is bytes and raw in self._fixtures)
        return copy.deepcopy(self._fixtures[raw])

class Mock:
    outbound_state="HOLD"
    def __init__(self, verifier):
        require(type(verifier) is SyntheticVerifier)
        self._verifier=verifier
        self._actions={}
        self._events={}
    def snapshot(self):
        return copy.deepcopy({"version":"1.0","outbound_state":"HOLD","actions":self._actions,"events":self._events})
    def intake(self, request, *, permission, lifecycle, reviews, rights=(), replay_receipt=None,
               approval, now, at, max_age, disposition="HELD"):
        clock(now,at,max_age)  # before duplicate lookup or mutation
        require(type(request) is dict and set(request)=={"identity","privacy","content_revision","assets","account_ref","provider_ref","purpose","jurisdiction","subject_ref"})
        ident=copy.deepcopy(request["identity"])
        action_key=key(ident)
        for field in ("content_revision","account_ref","provider_ref","purpose","jurisdiction","subject_ref"): ref(request[field])
        require(type(request["assets"]) is tuple)
        for item in request["assets"]: ref(item)
        pr=request["privacy"]
        require(type(pr) is privacy.Request and pr.channel=="sms")
        require(pr.client_ref==ident["client_id"] and pr.subject_ref==request["subject_ref"])
        require(pr.asset_refs==request["assets"] and ident["approved_revision"]==request["content_revision"])
        for field in ("account_ref","provider_ref","purpose","jurisdiction"):
            require(getattr(pr,field)==request[field])
        require(pr.max_age_seconds==max_age)
        decision=privacy.evaluate(replace(pr,now=now),permission,lifecycle,reviews,rights,replay_receipt=replay_receipt)
        require(decision.status=="ELIGIBLE_OFFLINE")
        require(type(approval) is dict and set(approval)=={"ref","owner","status","revision","client_ref","account_ref","subject_ref","provider_ref","purpose","jurisdiction","assets","observed_at","expires_at"})
        ref(approval["ref"]); ref(approval["owner"])
        require(approval["status"]=="APPROVED" and approval["revision"]==request["content_revision"])
        for field in ("account_ref","subject_ref","provider_ref","purpose","jurisdiction","assets"):
            require(approval[field]==request[field] and type(approval[field]) is type(request[field]))
        require(approval["client_ref"]==ident["client_id"])
        clock(now,approval["observed_at"],max_age)
        require(privacy.instant(now)<privacy.instant(approval["expires_at"]))
        adapter={"schema_version":"1.0","adapter":"providers","action":"transport.submit","account_ref":pr.account_ref,"action_key":action_key,"expected_revision":request["content_revision"],"payload_ref":"synthetic-payload","outbound_state":"HOLD"}
        f05.validate_request(adapter)
        require(disposition in ("HELD","TIMEOUT_AFTER_SUBMIT","REJECTED"))
        # Fingerprint all bound intent; privacy time is current evidence, not intent.
        intent={k:v for k,v in request.items() if k!="privacy"}
        intent["approval_ref"]=approval["ref"]
        fingerprint=digest(intent)
        if action_key in self._actions:
            require(self._actions[action_key]["fingerprint"]==fingerprint)
            return copy.deepcopy(self._actions[action_key]["history"][-1])
        history=[]
        entry={"intent":copy.deepcopy(intent),"fingerprint":fingerprint,"disposition":disposition,"history":history}
        def add(status):
            history.append(self._receipt(entry,action_key,status,at))
        add("HELD")
        if disposition!="HELD":
            add("SUBMITTED")
            add(f05.error_decision("TIMEOUT_AFTER_SUBMIT",submitted=True) if disposition=="TIMEOUT_AFTER_SUBMIT" else "REJECTED")
        self._actions[action_key]=entry
        return copy.deepcopy(history[-1])
    @staticmethod
    def _receipt(entry, action_key, status, at, outcome=None, evidence=None, obj=None):
        intent=entry["intent"]
        index=len(entry["history"])
        return {"schema_version":"1.0","receipt_id":"synthetic-"+hashlib.sha256((action_key+":"+str(index)).encode()).hexdigest(),
          "action_identity":copy.deepcopy(intent["identity"]),"action_key":action_key,
          "event_id":intent["identity"]["source_event_id"],"correlation_id":"synthetic-correlation",
          "approval_ref":intent["approval_ref"],"destination":intent["account_ref"],"attempt":1,
          "recorded_at":at,"status":status,"provider_object_ref":obj,"evidence_ref":"synthetic-evidence",
          "reconciliation_ref":evidence,"outbound_state":"CONFIRMED" if outcome=="OCCURRED" else "HOLD","reservation_retained":outcome!="NOT_OCCURRED",
          "reconciliation_outcome":outcome}
    def reconcile(self, action_key, raw, *, now, max_age):
        # Callback/reconciliation never adds actions and never authorizes sends.
        clock(now,now,max_age)
        proof=self._verifier.verify(raw)
        require(type(proof) is dict and set(proof)=={"action_key","account_ref","provider_ref","object_ref","event_ref","at","outcome","evidence_ref"})
        clock(now,proof["at"],max_age)
        for field in ("account_ref","provider_ref","object_ref","event_ref","evidence_ref"):
            if field=="object_ref" and proof[field] is None: continue
            ref(proof[field])
        require(proof["action_key"]==action_key and action_key in self._actions)
        entry=self._actions[action_key]
        require(proof["account_ref"]==entry["intent"]["account_ref"] and proof["provider_ref"]==entry["intent"]["provider_ref"])
        require(proof["outcome"] in ("OCCURRED","NOT_OCCURRED"))
        require((proof["object_ref"] is not None)==(proof["outcome"]=="OCCURRED"))
        require(privacy.instant(proof["at"])>=privacy.instant(entry["history"][-1]["recorded_at"]))
        if proof["event_ref"] in self._events:
            require(self._events[proof["event_ref"]]==proof)
            return copy.deepcopy(entry["history"][-1])
        require(entry["history"][-1]["status"]=="UNKNOWN")
        receipt=self._receipt(entry,action_key,"RECONCILED",proof["at"],proof["outcome"],proof["evidence_ref"],proof["object_ref"])
        entry["history"].append(receipt)
        self._events[proof["event_ref"]]=copy.deepcopy(proof)
        return copy.deepcopy(receipt)
    @classmethod
    def restore(cls, snapshot, verifier):
        require(type(snapshot) is dict and set(snapshot)=={"version","outbound_state","actions","events"})
        require(snapshot["version"]=="1.0" and snapshot["outbound_state"]=="HOLD")
        require(type(snapshot["actions"]) is dict and type(snapshot["events"]) is dict)
        require(len(snapshot["events"])==len(set(snapshot["events"])))
        for event,proof in snapshot["events"].items():
            ref(event)
            require(type(proof) is dict and set(proof)=={"action_key","account_ref","provider_ref","object_ref","event_ref","at","outcome","evidence_ref"})
            require(proof["event_ref"]==event and proof["action_key"] in snapshot["actions"])
            ref(proof["account_ref"]); ref(proof["provider_ref"]); ref(proof["evidence_ref"])
            if proof["object_ref"] is not None: ref(proof["object_ref"])
            privacy.instant(proof["at"])
        for action_key, entry in snapshot["actions"].items():
            require(type(entry) is dict and set(entry)=={"intent","fingerprint","disposition","history"})
            intent=entry["intent"]
            require(type(intent) is dict and set(intent)=={"identity","content_revision","assets","account_ref","provider_ref","purpose","jurisdiction","subject_ref","approval_ref"})
            for field in ("content_revision","account_ref","provider_ref","purpose","jurisdiction","subject_ref","approval_ref"): ref(intent[field])
            require(type(intent["assets"]) is tuple and len(set(intent["assets"]))==len(intent["assets"]))
            for asset in intent["assets"]: ref(asset)
            require(intent["content_revision"]==intent["identity"]["approved_revision"])
            require(key(entry["intent"]["identity"])==action_key and digest(entry["intent"])==entry["fingerprint"])
            require(entry["disposition"] in ("HELD","TIMEOUT_AFTER_SUBMIT","REJECTED"))
            h=entry["history"]
            require(type(h) is list and len(h)>0)
            statuses={"HELD":["HELD"],"TIMEOUT_AFTER_SUBMIT":["HELD","SUBMITTED","UNKNOWN"],"REJECTED":["HELD","SUBMITTED","REJECTED"]}[entry["disposition"]]
            require([x["status"] for x in h[:len(statuses)]]==statuses and len(h) in (len(statuses),len(statuses)+1))
            base={"intent":entry["intent"],"history":[]}
            for i,receipt in enumerate(h):
                privacy.instant(receipt["recorded_at"])
                if i: require(privacy.instant(receipt["recorded_at"])>=privacy.instant(h[i-1]["recorded_at"]))
                if i>=len(statuses):
                    require(entry["disposition"]=="TIMEOUT_AFTER_SUBMIT" and receipt["status"]=="RECONCILED")
                    require(receipt["reconciliation_outcome"] in ("OCCURRED","NOT_OCCURRED"))
                    require((receipt["provider_object_ref"] is not None)==(receipt["reconciliation_outcome"]=="OCCURRED"))
                    matches=[proof for proof in snapshot["events"].values() if proof["action_key"]==action_key]
                    require(len(matches)==1)
                    proof=matches[0]
                    require(proof["account_ref"]==intent["account_ref"] and proof["provider_ref"]==intent["provider_ref"])
                    require((proof["outcome"],proof["at"],proof["evidence_ref"],proof["object_ref"])==(receipt["reconciliation_outcome"],receipt["recorded_at"],receipt["reconciliation_ref"],receipt["provider_object_ref"]))
                    ref(receipt["reconciliation_ref"])
                    if receipt["provider_object_ref"] is not None: ref(receipt["provider_object_ref"])
                else:
                    require(receipt["reconciliation_outcome"] is None and receipt["reconciliation_ref"] is None and receipt["provider_object_ref"] is None)
                expected=cls._receipt(base,action_key,receipt["status"],receipt["recorded_at"],receipt["reconciliation_outcome"],receipt["reconciliation_ref"],receipt["provider_object_ref"])
                closed(receipt,expected)
                base["history"].append(receipt)
        require(len(snapshot["events"])==sum(1 for e in snapshot["actions"].values() if e["history"][-1]["status"]=="RECONCILED"))
        result=cls(verifier)
        result._actions=copy.deepcopy(snapshot["actions"])
        result._events=copy.deepcopy(snapshot["events"])
        return result
