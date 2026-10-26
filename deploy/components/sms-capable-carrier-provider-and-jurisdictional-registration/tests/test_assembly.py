"""Disposable synthetic blob/transport tests; never invokes a Git binary."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import assemble_inputs as a
C=Path(a.__file__).parent
ROOT=C.parents[2]
class Blobs:
    def __init__(self, values): self.values=values
    def read(self, commit, path): return self.values[(commit,path)]
class Assembly(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=C)
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.target=self.base/'inputs'
        self.data=b'synthetic-public-blob\n'
        self.item=dict(repository=a.REPOSITORY,commit='a'*40,source_path='contracts/public.py',destination='inputs/F05/contracts/public.py',sha256=hashlib.sha256(self.data).hexdigest(),bytes=len(self.data))
        self.lock=dict(version=1,sources=[self.item])
        self.transport=Blobs({('a'*40,'contracts/public.py'):('100644',self.data)})
    def denied(self, lock=None, transport=None, target=None):
        with self.assertRaises((ValueError,KeyError,OSError)):
            a.assemble(self.lock if lock is None else lock,self.transport if transport is None else transport,self.target if target is None else target)
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.base.glob('.cp141-inputs-*')),[])
    def test_publish_exact_bytes(self):
        a.assemble(self.lock,self.transport,self.target)
        self.assertEqual((self.target/'F05/contracts/public.py').read_bytes(),self.data)
        self.assertEqual(list(self.base.glob('.cp141-inputs-*')),[])
    def test_missing_commit_file_digest_size_and_modes(self):
        for field,value in [('commit','b'*40),('source_path','missing.py'),('sha256','0'*64),('bytes',0)]:
            lock=copy.deepcopy(self.lock);lock['sources'][0][field]=value
            with self.subTest(field=field): self.denied(lock)
        for mode in ('120000','160000','040000'):
            with self.subTest(mode=mode): self.denied(transport=Blobs({('a'*40,'contracts/public.py'):(mode,self.data)}))
    def test_closed_lock_and_unsafe_paths(self):
        for field,value in [('extra',True),('bytes',True),('commit','main'),('sha256',True),('repository','private/repo')]:
            lock=copy.deepcopy(self.lock);lock['sources'][0][field]=value
            with self.subTest(field=field): self.denied(lock)
        for field in ('source_path','destination'):
            for value in ('../escape','/absolute','C:/private','inputs/../x','inputs//x','inputs/F05/CON','inputs/F05/x.','inputs/F05/x\\y','inputs/F05/a\nb'):
                lock=copy.deepcopy(self.lock);lock['sources'][0][field]=value
                with self.subTest(field=field,value=value): self.denied(lock)
        for lock in ({},dict(self.lock,extra=True),dict(self.lock,version=True),dict(self.lock,sources=[])):
            self.denied(lock)
        with self.assertRaises(ValueError): json.loads('{"version":1,"version":1}',object_pairs_hook=a.no_duplicate_keys)
    def test_atomicity_second_blob_failure_and_collision(self):
        lock=copy.deepcopy(self.lock)
        bad=dict(self.item,source_path='missing.py',destination='inputs/F16/missing.py')
        lock['sources'].append(bad)
        self.denied(lock)
        self.target.mkdir()
        (self.target/'sentinel').write_bytes(b'preserve')
        with self.assertRaises(ValueError):a.assemble(self.lock,self.transport,self.target)
        self.assertEqual((self.target/'sentinel').read_bytes(),b'preserve')
    def test_publish_failure_rolls_back(self):
        with patch.object(Path,'rename',side_effect=OSError('synthetic failure')):
            self.denied()
    def test_duplicate_casefold_prefix_collisions(self):
        for dest in (self.item['destination'],self.item['destination'].upper(),'inputs/F05/contracts','inputs/F05/contracts/public.py/child'):
            lock=copy.deepcopy(self.lock);lock['sources'].append(dict(self.item,destination=dest))
            self.denied(lock)
    def test_unsafe_destination_parent(self):
        self.denied(target=self.base/'absent'/'inputs')
        self.denied(target='relative-inputs')
        self.denied(target=self.base/'child'/'..'/'inputs')
        with patch.object(Path,'is_junction',return_value=True): self.denied()
        with patch.object(Path,'is_symlink',return_value=True): self.denied()
    def test_git_transport_command_contract_no_execution(self):
        # Fake stdout at the process boundary: validates argv, exact commit, mode and name.
        g=object.__new__(a.GitBlobs);g.repository=self.base
        outputs=[b'commit\n',b'100644 blob '+b'b'*40+b'\tcontracts/public.py\0',self.data]
        with patch.object(a.subprocess,'run',side_effect=[subprocess.CompletedProcess([],0,x,b'') for x in outputs]) as run:
            self.assertEqual(g.read('a'*40,'contracts/public.py'),('100644',self.data))
            self.assertEqual(run.call_count,3)
            for call in run.call_args_list:
                self.assertNotIn('shell',call.kwargs)
                self.assertEqual(call.kwargs['env']['GIT_NO_LAZY_FETCH'],'1')
                self.assertIn('protocol.allow=never',call.args[0])
        for row in (b'120000 blob '+b'b'*40+b'\tcontracts/public.py\0',b'160000 commit '+b'b'*40+b'\tcontracts/public.py\0',b'',b'100644 blob '+b'b'*40+b'\twrong.py\0'):
            with patch.object(g,'run',side_effect=[b'commit\n',row]):
                with self.assertRaises(ValueError):g.read('a'*40,'contracts/public.py')
    def test_supplied_accepted_exports_public_clean(self):
        # This is supplied-export integration, NOT a claim of canonical Git execution.
        lock=json.loads(a.LOCK.read_text(encoding='utf-8-sig'))
        blobs={}
        for item in lock['sources']:
            data=(C/ item['destination']).read_bytes()
            self.assertEqual(len(data),item['bytes'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),item['sha256'])
            blobs[(item['commit'],item['source_path'])]=('100644',data)
        clean=self.base/'public-clean'; component=clean/'deploy/components'/C.name
        component.mkdir(parents=True)
        for name in ('mock.py','policy.py','component.json','assemble_inputs.py','public-inputs.lock.json'):
            shutil.copyfile(C/name,component/name)
        (component/'tests').mkdir()
        shutil.copyfile(C/'tests/test_mock.py',component/'tests/test_mock.py')
        a.assemble(lock,Blobs(blobs),component/'inputs')
        argv=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-m','unittest','discover','-s',str(component/'tests'),'-v']
        result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('Ran 20 tests',result.stderr)
if __name__=='__main__':unittest.main()
