"""Regression source: run only under a separately admitted root test token."""
import copy
from dataclasses import replace
import importlib.util
from pathlib import Path
import sys
import unittest

C=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(C))
import ads_policy as policy
from assemble_inputs import load_dependency

NOW='2026-10-27T12:00:00Z'
BEFORE='2026-10-27T11:59:00Z'
AFTER='2026-10-27T13:00:00Z'

def fixture(channels=('tracking','audience_export')):
    f=load_dependency('f16')
    intent=dict(client_ref='synthetic-client',subject_ref='synthetic-subject',account_ref='synthetic-account',campaign_ref='synthetic-campaign',revision='revision-1',provider_ref='synthetic-provider',jurisdiction='synthetic-jurisdiction',purpose='synthetic-purpose',asset_refs=('synthetic-asset',),amount_minor=100,currency='USD',channels=channels,expires_at=AFTER)
    consents={}
    for channel in channels:
        b={k:intent[k] for k in ('client_ref','subject_ref','account_ref','provider_ref','jurisdiction','purpose')};b['channel']=channel
        permission=f.Permission(**b,source_authority=f.AUTHORITIES[channel],granted=True,revoked=False,authority_available=True,valid_from=BEFORE,expires_at=AFTER,observed_at=BEFORE,evidence_ref='synthetic-permission')
        lifecycle=f.Lifecycle(intent['client_ref'],intent['subject_ref'],False,False,True,BEFORE,AFTER,3,3,None,False,None,'synthetic-lifecycle')
        rb={k:v for k,v in b.items() if k!='subject_ref'}
        reviews=tuple(f.Review(**rb,kind=k,status='APPROVED',revoked=False,reviewer_role=v,observed_at=BEFORE,expires_at=AFTER,evidence_ref='synthetic-'+k) for k,v in f.REVIEW_ROLES.items())
        right=f.AssetRight('synthetic-asset',intent['client_ref'],intent['purpose'],intent['account_ref'],False,BEFORE,AFTER,BEFORE,'synthetic-right')
        consents[channel]=dict(permission=permission,lifecycle=lifecycle,reviews=reviews,rights=(right,),replay_receipt=None)
    budget={k:intent[k] for k in ('client_ref','account_ref','campaign_ref','revision','provider_ref','amount_minor','currency')}
    budget.update(valid_from=BEFORE,expires_at=AFTER,observed_at=BEFORE,revoked=False,evidence_ref='synthetic-budget')
    return intent,consents,budget

def assess(i,c,b,now=NOW):return policy.assess_ad_intent(i,c,b,now=now,max_age_seconds=120)

class PolicyTests(unittest.TestCase):
    def test_each_channel_and_both_positive_still_held(self):
        for channels in [('tracking',),('audience_export',),('tracking','audience_export')]:
            with self.subTest(channels=channels):
                r=assess(*fixture(channels));self.assertEqual('ELIGIBLE_OFFLINE',r['eligibility']);self.assertEqual('HOLD',r['outbound_state']);self.assertIs(r['executable_authority'],False)
                self.assertEqual(set(channels),set(r['consent']))
    def test_budget_and_consent_independent_diagnostics(self):
        i,c,b=fixture();b['revoked']=True;r=assess(i,c,b)
        self.assertEqual('DENY',r['eligibility']);self.assertTrue(all(v['status']=='ELIGIBLE_OFFLINE' for v in r['consent'].values()));self.assertEqual('DENY',r['budget']['status'])
        b['revoked']=False;c['tracking']['permission']=replace(c['tracking']['permission'],revoked=True);r=assess(i,c,b)
        self.assertEqual('BOUND_SYNTHETIC',r['budget']['status']);self.assertEqual('DENY',r['consent']['tracking']['status'])
    def test_permission_binding_matrix_and_unrelated_channel(self):
        for field in ['client_ref','subject_ref','account_ref','provider_ref','jurisdiction','purpose','source_authority','channel']:
            i,c,b=fixture();c['tracking']['permission']=replace(c['tracking']['permission'],**{field:'other'})
            with self.subTest(field=field):self.assertEqual('DENY',assess(i,c,b)['eligibility'])
        i,c,b=fixture();c['tracking']=c['audience_export'];self.assertEqual('DENY',assess(i,c,b)['eligibility'])
    def test_permission_time_revocation_exact_booleans(self):
        for changes in [{'revoked':True},{'granted':1},{'authority_available':False},{'expires_at':NOW},{'valid_from':AFTER},{'observed_at':'2026-10-27T10:00:00Z'},{'observed_at':AFTER}]:
            i,c,b=fixture();c['tracking']['permission']=replace(c['tracking']['permission'],**changes)
            with self.subTest(changes=changes):self.assertEqual('DENY',assess(i,c,b)['eligibility'])
    def test_reviews_rights_lifecycle_replay(self):
        for key,value in [('reviews',()),('reviews','bad'),('rights',()),('replay_receipt','invented')]:
            i,c,b=fixture();c['tracking'][key]=value;self.assertEqual('DENY',assess(i,c,b)['eligibility'])
        for changes in [{'suppressed':True},{'deleted':True},{'retention_until':None},{'applied_generation':2},{'restore_epoch':'restore-1'}]:
            i,c,b=fixture();c['tracking']['lifecycle']=replace(c['tracking']['lifecycle'],**changes);self.assertEqual('DENY',assess(i,c,b)['eligibility'])
        i,c,b=fixture();c['tracking']['rights']=(replace(c['tracking']['rights'][0],revoked=True),);self.assertEqual('DENY',assess(i,c,b)['eligibility'])
        i,c,b=fixture();c['tracking']['reviews']=(c['tracking']['reviews'][0],)*2;self.assertEqual('DENY',assess(i,c,b)['eligibility'])
    def test_budget_binding_and_exclusive_expiry(self):
        for key,value in [('client_ref','other'),('account_ref','other'),('campaign_ref','other'),('revision','other'),('provider_ref','other'),('currency','EUR'),('amount_minor',99),('amount_minor',True),('amount_minor',2**64),('expires_at',NOW),('valid_from',AFTER),('observed_at',AFTER),('revoked',1),('evidence_ref','')]:
            i,c,b=fixture();b[key]=value
            with self.subTest(key=key,value=value):self.assertEqual('DENY',assess(i,c,b)['eligibility'])
    def test_intent_closed_money_and_no_clock_shortcut(self):
        for key,value in [('amount_minor',True),('amount_minor',float('nan')),('amount_minor',float('inf')),('amount_minor',0),('amount_minor',2**64),('currency','usd'),('expires_at',NOW),('channels',('email',)),('channels',()),('asset_refs',('same','same'))]:
            i,c,b=fixture();i[key]=value;self.assertEqual('DENY',assess(i,c,b)['eligibility'])
        i,c,b=fixture();i['secret']='do-not-echo';self.assertNotIn('do-not-echo',str(assess(i,c,b)))
        self.assertEqual('DENY',assess(*fixture(),now=AFTER)['eligibility'])
    def test_inputs_immutable_and_results_independent(self):
        i,c,b=fixture();before=copy.deepcopy((i,c,b));r=assess(i,c,b);r['consent'].clear();self.assertEqual(before,(i,c,b));self.assertEqual('ELIGIBLE_OFFLINE',assess(i,c,b)['eligibility'])
    def test_invalid_max_age(self):
        for age in [True,0,-1,None,float('nan')]:
            self.assertEqual('DENY',policy.assess_ad_intent(*fixture(),now=NOW,max_age_seconds=age)['eligibility'])

    def test_manifest_closed_and_always_held(self):
        import json
        manifest=json.loads((C/'component.json').read_text())
        self.assertTrue(policy.validate_component_manifest(manifest))
        for key,value in [('production_enabled',True),('outbound_state','ALLOW'),('provider_transport',{'endpoint':'invented'}),('unexpected',True)]:
            changed=copy.deepcopy(manifest);changed[key]=value
            with self.assertRaises(ValueError):policy.validate_component_manifest(changed)
