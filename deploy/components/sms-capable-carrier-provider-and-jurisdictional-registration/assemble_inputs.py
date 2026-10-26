"""Pinned local public Git blobs only; no fetch or repository code execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
REPOSITORY = 'CT-Infrastructure/marketing-v7-control'
LOCK = Path(__file__).with_name('public-inputs.lock.json')
def fail():
    raise ValueError('INVALID_PUBLIC_INPUT_ASSEMBLY')
def safe_path(value):
    if type(value) is not str or not value or '\\' in value or ':' in value:
        fail()
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in ('', '.', '..') for x in value.split('/')):
        fail()
    for part in p.parts:
        if (not re.fullmatch(r'[A-Za-z0-9_.-]+', part) or part.endswith('.')
            or part.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*('COM'+str(i) for i in range(1,10)),*('LPT'+str(i) for i in range(1,10))}):
            fail()
    return p
def validate_lock(lock):
    if type(lock) is not dict or set(lock) != {'version','sources'} or type(lock['version']) is not int or lock['version'] != 1:
        fail()
    if type(lock['sources']) is not list or not lock['sources']:
        fail()
    seen = set()
    for item in lock['sources']:
        if type(item) is not dict or set(item) != {'repository','commit','source_path','destination','sha256','bytes'}:
            fail()
        if item['repository'] != REPOSITORY:
            fail()
        for field, size in (('commit',40),('sha256',64)):
            if type(item[field]) is not str or not re.fullmatch('[a-f0-9]{'+str(size)+'}',item[field]):
                fail()
        if type(item['bytes']) is not int or not 0 <= item['bytes'] <= 16*1024*1024:
            fail()
        safe_path(item['source_path'])
        dest = safe_path(item['destination'])
        if len(dest.parts) < 3 or dest.parts[0] != 'inputs' or dest.parts[1] not in ('F04','F05','F16'):
            fail()
        portable = str(dest).casefold()
        if any(portable == old or portable.startswith(old+'/') or old.startswith(portable+'/') for old in seen):
            fail()
        seen.add(portable)
    return lock['sources']
class GitBlobs:
    def __init__(self, repository):
        self.repository = Path(repository).resolve(strict=True)
        if not self.repository.is_dir(): fail()
    def run(self, *args):
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,GIT_TERMINAL_PROMPT='0', GIT_NO_REPLACE_OBJECTS='1',GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
        return subprocess.run(['git','--no-pager','-c','core.hooksPath='+os.devnull,'-c','protocol.allow=never','-c','credential.helper=', '-C',str(self.repository),*args],env=env,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
    def read(self, commit, path):
        if self.run('cat-file','-t',commit).strip() != b'commit': fail()
        rows = self.run('ls-tree','-z',commit,'--',path).split(b'\0')
        if len(rows) != 2 or rows[-1] != b'': fail()
        meta, name = rows[0].split(b'\t',1)
        mode, kind, oid = meta.split()
        if name != path.encode() or mode not in (b'100644',b'100755') or kind != b'blob': fail()
        return mode.decode(), self.run('cat-file','blob',oid.decode('ascii'))
def assemble(lock, transport, destination):
    sources = validate_lock(lock)
    raw_target = Path(destination)
    if not raw_target.is_absolute() or '..' in raw_target.parts:
        fail()
    target = Path(os.path.abspath(destination))
    for parent in (target, *target.parents):
        if parent.is_symlink() or parent.is_junction(): fail()
    if target.exists() or not target.parent.is_dir(): fail()
    stage = Path(tempfile.mkdtemp(prefix='.cp141-inputs-',dir=target.parent))
    try:
        for item in sources:
            mode, data = transport.read(item['commit'],item['source_path'])
            if mode not in ('100644','100755') or type(data) is not bytes: fail()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']: fail()
            output = stage.joinpath(*PurePosixPath(item['destination']).parts[1:])
            output.parent.mkdir(parents=True,exist_ok=True)
            with output.open('xb') as f: f.write(data)
        # Parent must be exclusively held by caller; destination must remain absent.
        if target.exists() or target.is_symlink(): fail()
        stage.rename(target)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    return target
def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result: fail()
        result[key] = value
    return result
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--control-repository',required=True)
    parser.add_argument('--destination',required=True,help='New inputs directory in an exclusive caller-owned parent')
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text(encoding='utf-8-sig'),object_pairs_hook=no_duplicate_keys)
    assemble(lock,GitBlobs(args.control_repository),args.destination)
if __name__ == '__main__': main()
