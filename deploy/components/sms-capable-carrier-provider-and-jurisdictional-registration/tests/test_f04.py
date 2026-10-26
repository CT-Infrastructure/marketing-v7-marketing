"""Exact accepted conditionals and transition code; full validator is optional, not replaced."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import test_mock as t
m=t.m
F04=m.INPUTS/'F04'
SCHEMA=F04/'schemas/runtime/action-receipt.schema.json'
VALIDATOR=F04/'contracts/core/validate.py'
class F04(unittest.TestCase):
    def receipts(self,outcome):
        helper=t.Tests();helper.setUp()
        key=helper.unknown(outcome)
        before=helper.mock.snapshot()
        receipt=helper.mock.reconcile(key,b'synthetic-original',now=t.NOW,max_age=60)
        return helper,key,before,receipt
    def conditional(self,outcome):
        raw=SCHEMA.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'bba9b8f7575d75173709a54324485e2bf6b1034fe63437ab29e2e364876cd08b')
        schema=json.loads(raw)
        return next(c['then']['properties'] for c in schema['allOf'] if c['if']['properties'].get('reconciliation_outcome')=={'const':outcome})
    def check_conditional(self,receipt):
        # Targeted assertions over the exact accepted then-clause; not a schema validator.
        for field,rule in self.conditional(receipt['reconciliation_outcome']).items():
            value=receipt[field]
            if 'const' in rule:self.assertIs(value,rule['const']) if type(rule['const']) is bool else self.assertEqual(value,rule['const'])
            if rule.get('type')=='null':self.assertIsNone(value)
            if rule.get('type')=='string':
                self.assertIs(type(value),str);self.assertGreaterEqual(len(value),rule.get('minLength',0))
    def test_history_confirmed_runtime_and_restore_hold(self):
        for outcome in ('OCCURRED','NOT_OCCURRED'):
            h,k,before,r=self.receipts(outcome)
            self.check_conditional(r)
            self.assertEqual(r['outbound_state'],'CONFIRMED' if outcome=='OCCURRED' else 'HOLD')
            self.assertEqual(h.mock.outbound_state,'HOLD')
            after=h.mock.snapshot()
            self.assertEqual(after['outbound_state'],'HOLD')
            self.assertEqual(after['actions'][k]['history'][:-1],before['actions'][k]['history'])
            restored=m.Mock.restore(after,h.mock._verifier)
            self.assertEqual(restored.outbound_state,'HOLD')
            self.assertEqual(restored.intake(h.req,**h.args),r)
            self.assertEqual(restored.reconcile(k,b'synthetic-original',now=t.NOW,max_age=60),r)
            self.assertEqual(restored.snapshot(),after)
            revoked=copy.deepcopy(h.args)
            revoked['permission']=t.dc.replace(revoked['permission'],revoked=True)
            with self.assertRaises(ValueError): restored.intake(h.req,**revoked)
            self.assertEqual(restored.snapshot(),after)
            corrupt=copy.deepcopy(after)
            corrupt['actions'][k]['history'][-1]['outbound_state']='HOLD' if outcome=='OCCURRED' else 'CONFIRMED'
            with self.assertRaises(ValueError):m.Mock.restore(corrupt,h.mock._verifier)
            journal=m.f05.Journal()
            request=dict(schema_version='1.0',adapter='providers',action='transport.submit',account_ref='synthetic-account',action_key=k,expected_revision='synthetic-revision',payload_ref='synthetic-payload',outbound_state='HOLD')
            self.assertEqual(journal.reserve(request),'RESERVED_HELD')
            self.assertEqual(journal.reserve(request),'REUSE_RECEIPT')
    def test_mutated_hold_on_occurred_rejected(self):
        h,k,before,r=self.receipts('OCCURRED')
        r['outbound_state']='HOLD'
        with self.assertRaises(AssertionError):self.check_conditional(r)
    def test_exact_transition_function_partial_without_schema(self):
        raw=VALIDATOR.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'db6ad80cf8ebf7eb94c9c3a77ff07099efd76aebb6a53aa34696a870fb770454')
        tree=ast.parse(raw)
        selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('instant','check_transition')]
        from datetime import datetime
        ns={'datetime':datetime,'validate':lambda *args:None}
        exec(compile(ast.Module(body=selected,type_ignores=[]),str(VALIDATOR),'exec'),ns)
        for outcome in ('OCCURRED','NOT_OCCURRED'):
            h,k,before,r=self.receipts(outcome)
            history=h.mock.snapshot()['actions'][k]['history']
            for previous,current in zip(history,history[1:]):self.assertTrue(ns['check_transition'](previous,current))
            for field,value in [('attempt',2),('receipt_id',history[-2]['receipt_id']),('approval_ref','synthetic-other'),('status','SUBMITTED'),('recorded_at',t.OLD),('action_identity',{})]:
                bad=copy.deepcopy(r);bad[field]=value
                with self.subTest(outcome=outcome,field=field):
                    with self.assertRaises(ValueError):ns['check_transition'](history[-2],bad)
    def test_full_accepted_validator_if_available(self):
        try:
            import jsonschema
            import referencing
        except ImportError as exc:self.skipTest('NOT_RUN full F04 validator: '+str(exc))
        spec=importlib.util.spec_from_file_location('cp141_exact_f04',VALIDATOR)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for outcome in ('OCCURRED','NOT_OCCURRED'):
            h,k,before,r=self.receipts(outcome)
            history=h.mock.snapshot()['actions'][k]['history']
            for receipt in history:module.validate('action-receipt',receipt)
            for previous,current in zip(history,history[1:]):module.check_transition(previous,current)
            bad=copy.deepcopy(r);bad['outbound_state']='HOLD' if outcome=='OCCURRED' else 'CONFIRMED'
            with self.assertRaises(Exception):module.validate('action-receipt',bad)
if __name__=='__main__':unittest.main()
