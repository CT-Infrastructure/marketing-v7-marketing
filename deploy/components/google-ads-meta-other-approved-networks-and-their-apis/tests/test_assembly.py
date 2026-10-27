"""Synthetic transport fixture; actual public Git integration belongs to root."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
C=Path(__file__).resolve().parents[1];sys.path.insert(0,str(C))
import assemble_inputs as assembly
LOCK=json.loads((C/'public-inputs.lock.json').read_text())

class FixtureTransport:
    def __init__(self,root):self.root=root;self.calls=[];self.failure=None
    def read(self,commit,path):
        self.calls.append((commit,path))
        if self.failure and len(self.calls)==self.failure:raise ValueError('SYNTHETIC_TRANSPORT_FAILURE')
        matches=[e for e in LOCK['sources'] if e['commit']==commit and e['source_path']==path]
        if len(matches)!=1:raise ValueError('MISSING_PUBLIC_BLOB')
        return '100644',(self.root/matches[0]['destination']).read_bytes()

class AssemblyTests(unittest.TestCase):
    def test_lock_has_exact_twenty_and_three_pins(self):
        self.assertEqual(20,len(assembly.validate_lock(LOCK)));self.assertEqual(3,len({x['commit'] for x in LOCK['sources']}))
    def test_lock_mutations_traversal_collision_commit_hash_size(self):
        for field,value in [('source_path','../escape'),('destination','inputs/F04/../escape'),('commit','0'*40),('sha256','0'*64),('bytes',True),('repository','other')]:
            lock=copy.deepcopy(LOCK);lock['sources'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):assembly.validate_lock(lock)
        lock=copy.deepcopy(LOCK);lock['sources'][1]['destination']=lock['sources'][0]['destination'].upper()
        with self.assertRaises(ValueError):assembly.validate_lock(lock)
    def test_exact_bytes_atomic_publish_and_existing_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'inputs';transport=FixtureTransport(C)
            assembly.assemble(LOCK,transport,target)
            self.assertEqual(20,len(transport.calls))
            for entry in LOCK['sources']:
                data=(target/Path(entry['destination']).relative_to('inputs')).read_bytes();self.assertEqual(entry['sha256'],hashlib.sha256(data).hexdigest())
            with self.assertRaises(ValueError):assembly.assemble(LOCK,transport,target)
    def test_failure_rolls_back_and_no_partial_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'inputs';transport=FixtureTransport(C);transport.failure=2
            with self.assertRaises(ValueError):assembly.assemble(LOCK,transport,target)
            self.assertFalse(target.exists());self.assertEqual([],list(Path(tmp).iterdir()))
    def test_wrong_blob_mode_hash_size_and_publish_failure(self):
        for mode,data in [('120000',b'link'),('100644',b'wrong'),('100755',b'wrong')]:
            with tempfile.TemporaryDirectory() as tmp:
                class Bad:
                    def read(self,*args):return mode,data
                with self.assertRaises(ValueError):assembly.assemble(LOCK,Bad(),Path(tmp)/'inputs')
                self.assertEqual([],list(Path(tmp).iterdir()))
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path,'rename',side_effect=OSError('synthetic publish failure')):
                with self.assertRaises(OSError):assembly.assemble(LOCK,FixtureTransport(C),Path(tmp)/'inputs')
            self.assertEqual([],list(Path(tmp).iterdir()))
    def test_loader_has_no_private_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            lockfile=Path(tmp)/'public-inputs.lock.json';lockfile.write_bytes((C/'public-inputs.lock.json').read_bytes())
            with patch.object(assembly,'LOCK',lockfile):
                with self.assertRaises(ValueError):assembly.load_dependency('f16')
    def test_duplicate_json_keys_denied(self):
        with self.assertRaises(ValueError):json.loads('{"version":1,"version":1}',object_pairs_hook=assembly.no_duplicate_keys)
