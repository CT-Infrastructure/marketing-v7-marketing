"""Pure synthetic diagnostics. No consent decision authorizes spend or dispatch."""
import copy
import re
from assemble_inputs import load_dependency

INTENT_FIELDS={'client_ref','subject_ref','account_ref','campaign_ref','revision','provider_ref',
               'jurisdiction','purpose','asset_refs','amount_minor','currency','channels','expires_at'}
BUDGET_FIELDS={'client_ref','account_ref','campaign_ref','revision','provider_ref','amount_minor',
               'currency','valid_from','expires_at','observed_at','revoked','evidence_ref'}
MAX_MINOR=2**63-1

def require(value):
    if not value: raise ValueError('INVALID_SYNTHETIC_AD_INTENT')

def opaque(value):
    return type(value) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}',value) is not None

def validate_intent(intent,now):
    f16=load_dependency('f16')
    require(type(intent) is dict and set(intent)==INTENT_FIELDS)
    for k in ('client_ref','subject_ref','account_ref','campaign_ref','revision','provider_ref','jurisdiction','purpose'):
        require(opaque(intent[k]))
    require(type(intent['amount_minor']) is int and 0<intent['amount_minor']<=MAX_MINOR)
    require(type(intent['currency']) is str and re.fullmatch('[A-Z]{3}',intent['currency']) is not None)
    require(type(intent['asset_refs']) is tuple and len(set(intent['asset_refs']))==len(intent['asset_refs']) and all(opaque(x) for x in intent['asset_refs']))
    require(type(intent['channels']) is tuple and bool(intent['channels']) and len(set(intent['channels']))==len(intent['channels']) and all(x in ('tracking','audience_export') for x in intent['channels']))
    require(f16.instant(now)<f16.instant(intent['expires_at']))
    return copy.deepcopy(intent)

def budget_diagnostic(intent,budget,now,max_age_seconds):
    f16=load_dependency('f16')
    try:
        require(type(budget) is dict and set(budget)==BUDGET_FIELDS)
        require(type(max_age_seconds) is int and max_age_seconds>0)
        require(all(budget[k]==intent[k] for k in ('client_ref','account_ref','campaign_ref','revision','provider_ref','currency')))
        require(type(budget['amount_minor']) is int and intent['amount_minor']<=budget['amount_minor']<=MAX_MINOR)
        require(budget['revoked'] is False and opaque(budget['evidence_ref']))
        clock=f16.instant(now)
        require(f16.instant(budget['valid_from'])<=clock<f16.instant(budget['expires_at']))
        require(f16.fresh(budget['observed_at'],clock,max_age_seconds))
        return {'status':'BOUND_SYNTHETIC','reason':'LOCAL_BINDINGS_SATISFIED'}
    except (ValueError,TypeError,KeyError,OverflowError):
        return {'status':'DENY','reason':'BUDGET_BINDING_INVALID'}

def assess_ad_intent(intent,consents,budget,*,now,max_age_seconds):
    """consents maps required channels to actual F16 caller-authenticated records.

    Each value has permission/lifecycle/reviews/rights/replay_receipt keys. Types
    are the exact accepted F16 dataclasses; no payload trust boolean is accepted.
    Caller authenticates snapshots outside this offline function.
    """
    f16=load_dependency('f16')
    denied={'eligibility':'DENY','consent':{},'budget':{'status':'DENY','reason':'INTENT_INVALID'},'outbound_state':'HOLD','executable_authority':False}
    try:
        validate_intent(intent,now)
        require(type(max_age_seconds) is int and max_age_seconds>0)
        require(type(consents) is dict and set(consents)==set(intent['channels']))
        diagnostics={}
        for channel in intent['channels']:
            evidence=consents[channel]
            require(type(evidence) is dict and set(evidence)=={'permission','lifecycle','reviews','rights','replay_receipt'})
            req=f16.Request(client_ref=intent['client_ref'],subject_ref=intent['subject_ref'],channel=channel,
                purpose=intent['purpose'],account_ref=intent['account_ref'],jurisdiction=intent['jurisdiction'],
                provider_ref=intent['provider_ref'],now=now,max_age_seconds=max_age_seconds,asset_refs=intent['asset_refs'])
            d=f16.evaluate(req,evidence['permission'],evidence['lifecycle'],evidence['reviews'],evidence['rights'],replay_receipt=evidence['replay_receipt'])
            diagnostics[channel]={'status':d.status,'reason':d.reason}
        bd=budget_diagnostic(intent,budget,now,max_age_seconds)
        eligible=all(d['status']=='ELIGIBLE_OFFLINE' for d in diagnostics.values()) and bd['status']=='BOUND_SYNTHETIC'
        return {'eligibility':'ELIGIBLE_OFFLINE' if eligible else 'DENY','consent':diagnostics,'budget':bd,'outbound_state':'HOLD','executable_authority':False}
    except (ValueError,TypeError,KeyError,AttributeError,OverflowError):
        return copy.deepcopy(denied)


MANIFEST_SHA256 = '338f1ca2ee94f2cc313a9c93ef281473bac81f81b1f7c2ec009ff948204c3d7b'

def validate_component_manifest(value):
    """Closed reviewed offline configuration; no enablement/transport extensions."""
    import hashlib
    import json
    try:
        require(type(value) is dict)
        raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
        require(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA256)
    except (ValueError,TypeError,OverflowError):
        raise ValueError('INVALID_COMPONENT_MANIFEST') from None
    return True
