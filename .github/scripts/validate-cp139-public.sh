#!/usr/bin/env bash
# Provision exact public data first; kernel-denied validation second. No installer.
set -euo pipefail
[[ "$#" = 0 ]] || { echo 'usage: validate-cp139-public.sh' >&2; exit 2; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
unset PYTHONPATH PYTHONHOME
exec python3 -I -S -B - "$root" <<'PY'
import base64,ctypes,email,errno,hashlib,json,os,platform,re,resource,selectors,shutil,signal,socket,stat,struct,subprocess,sys,sysconfig,tempfile,time,urllib.parse,urllib.request,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(sys.argv[1]).resolve(strict=True)
COMP=Path('deploy/components/google-ads-meta-other-approved-networks-and-their-apis')
START=time.monotonic();DEADLINE=START+360;LOG_BUDGET=4194304

def need(ok,message):
    if not ok:raise RuntimeError(message)
def tick():need(time.monotonic()<DEADLINE,'CP139_WHOLE_JOB_TIMEOUT')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def pairs(items):
    result={}
    for k,v in items:
        need(k not in result,'DUPLICATE_JSON_KEY');result[k]=v
    return result
# Target rejection occurs before acquisition or wheel/native imports.
need(sys.implementation.name=='cpython' and sys.version_info[:2]==(3,12),'UNSUPPORTED_CPYTHON_REQUIRES_3_12')
need(sys.platform=='linux' and platform.machine()=='x86_64' and sys.byteorder=='little' and struct.calcsize('P')==8,'UNSUPPORTED_LINUX_X86_64_ABI')
need(sysconfig.get_config_var('SOABI')=='cpython-312-x86_64-linux-gnu','UNSUPPORTED_CPYTHON_SOABI')
glibc=os.confstr('CS_GNU_LIBC_VERSION');need(glibc and glibc.startswith('glibc '),'UNSUPPORTED_LIBC')
need(tuple(map(int,glibc.split()[1].split('.')[:2]))>=(2,17),'UNSUPPORTED_GLIBC')
resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
resource.setrlimit(resource.RLIMIT_FSIZE,(16777216,16777216))
lockpath=ROOT/'.github/requirements/cp139-validation-py312-linux-x86_64.lock'
need(sha(lockpath)=='75ea66d9c233acecc3ec9334e361b2a81c17842dd704408630f6876322f1ca96','REVIEWED_WHEEL_LOCK_CHANGED')
lock=json.loads(lockpath.read_text(),object_pairs_hook=pairs)
need(set(lock)=={'schema','target','total_download_bytes','wheels'} and lock['schema']=='cp139-validation-wheels-1','INVALID_WHEEL_LOCK')
need(lock['target']=={'implementation':'cpython','python':'3.12','system':'Linux','machine':'x86_64','glibc_min':'2.17'},'LOCK_TARGET_MISMATCH')
need(type(lock['wheels']) is list and len(lock['wheels'])==6 and lock['total_download_bytes']==607388,'EXACT_SIX_WHEELS_REQUIRED')
operation=Path(tempfile.mkdtemp(prefix='cp139-public-validation-'))
need(ROOT not in operation.parents and operation not in ROOT.parents,'SCRATCH_MUST_BE_OUTSIDE_SOURCE')
work=operation/'work';work.mkdir();deps=work/'deps';deps.mkdir();downloads=work/'wheels';downloads.mkdir()
report={'status':'RUNNING','scope':'public provisioning then seccomp network-denied local tests; no filesystem isolation claim','runs':[],'native_credit':0,'wheel_installer_executed':False,'operation':str(operation)}
save(operation/'receipt.json',report)

def inventory(root):
    result={}
    for parent,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[n for n in dirs if n!='.git']
        for n in dirs+files:
            q=Path(parent)/n;need(not q.is_symlink(),'SOURCE_LINK_UNSUPPORTED')
        for n in files:
            q=Path(parent)/n;need(q.is_file(),'NONREGULAR_SOURCE');result[q.relative_to(root).as_posix()]=sha(q)
    return result
source_before=inventory(ROOT)

# Child output is bounded across provisioning and tests, with timeout and owned
# process-group cancellation. No retries, inherited credentials or Git overrides.
ENV={'PATH':'/usr/bin:/bin','HOME':str(work),'TMPDIR':str(work),'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1',
     'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_TERMINAL_PROMPT':'0','GIT_ASKPASS':'/bin/false',
     'GIT_NO_REPLACE_OBJECTS':'1','GIT_NO_LAZY_FETCH':'1','GIT_OPTIONAL_LOCKS':'0','GIT_ALLOW_PROTOCOL':'https'}

def owned_group_live(pid):
    """Observe only this still-pinned session/group; zombies are not running.

    Direct leader remains UNREAPED until all group signals finish. A live/zombie
    direct child pins its PID, so this PID cannot be recycled into another group.
    Descendants that deliberately escape via setsid are outside this observation;
    this helper never claims universal descendant reaping or filesystem isolation.
    """
    live=[];unknown=False
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():continue
        try:
            text=(entry/'stat').read_text();fields=text[text.rfind(')')+2:].split()
            if int(fields[2])==pid and int(fields[3])==pid and fields[0] not in ('Z','X'):
                live.append(int(entry.name))
        except FileNotFoundError:continue
        except (OSError,ValueError,IndexError):unknown=True
    return live,unknown

def cleanup_owned_group(proc):
    """Finite TERM/KILL then direct reap, never signal after PID pin release."""
    result={'session':proc.pid,'group':proc.pid,'signals':[],'direct_reaped':False,
            'orphan_reaping_guaranteed':False,'escaped_session_descendants':'NOT_QUALIFIED'}
    # Popen.poll()/wait() is forbidden before final group signals: either would
    # reap an exited leader and permit PID/PGID reuse. waitid(WNOWAIT) observes
    # exit state without releasing this ownership pin.
    try:
        os.waitid(os.P_PID,proc.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
        need(os.getpgid(proc.pid)==proc.pid and os.getsid(proc.pid)==proc.pid,'OWNED_SESSION_IDENTITY_LOST')
    except (ChildProcessError,ProcessLookupError):
        result['ownership']='LOST_NO_SIGNALS';return result
    result['ownership']='UNREAPED_DIRECT_CHILD_PINNED'
    def group_signal(sig):
        # Recheck the pinned direct-child identity immediately before every signal.
        os.waitid(os.P_PID,proc.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
        need(os.getpgid(proc.pid)==proc.pid and os.getsid(proc.pid)==proc.pid,'OWNED_SESSION_IDENTITY_LOST')
        try:os.killpg(proc.pid,sig);result['signals'].append(sig)
        except ProcessLookupError:result['signals'].append('GROUP_ABSENT')
    group_signal(signal.SIGTERM)
    grace=time.monotonic()+.25
    while time.monotonic()<grace:
        live,unknown=owned_group_live(proc.pid)
        if not live and not unknown:break
        time.sleep(.01)
    # KILL is intentionally issued even when the leader already exited, while its
    # unreaped PID still prevents recycled-group signalling. No poll guard.
    group_signal(signal.SIGKILL)
    settle=time.monotonic()+.25
    while time.monotonic()<settle:
        live,unknown=owned_group_live(proc.pid)
        if not live and not unknown:break
        time.sleep(.01)
    result['owned_group_live_after_kill'],result['proc_observation_incomplete']=owned_group_live(proc.pid)
    try:
        result['direct_exit_code']=proc.wait(timeout=1);result['direct_reaped']=True
    except subprocess.TimeoutExpired:result['direct_reap']='TIMEOUT_UNKNOWN_ROOT_RECONCILIATION_REQUIRED'
    # The pin is now released. Never send another group/PID signal from here.
    return result

def run(name,argv,cwd=None):
    global LOG_BUDGET
    tick();need(DEADLINE-time.monotonic()>3,'INSUFFICIENT_CLEANUP_TIME')
    proc=subprocess.Popen(argv,cwd=cwd,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
    sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ);data=bytearray()
    end=min(DEADLINE-2,time.monotonic()+90);failure=None;cleanup=None
    try:
        while sel.get_map():
            need(time.monotonic()<end,'CHILD_TIMEOUT_'+name)
            for key,_ in sel.select(min(.1,max(.001,end-time.monotonic()))):
                chunk=os.read(key.fd,8192)
                if not chunk:sel.unregister(key.fileobj);continue
                # Preserve the bounded prefix, including the chunk that overflowed.
                allowed=min(len(chunk),LOG_BUDGET);data.extend(chunk[:allowed]);LOG_BUDGET-=allowed
                need(allowed==len(chunk),'AGGREGATE_LOG_LIMIT')
        # EOF is not proof of leader exit or descendant quiescence. Observe without
        # reaping until natural leader exit, then clean its pinned group as well.
        while os.waitid(os.P_PID,proc.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is None:
            need(time.monotonic()<end,'CHILD_TIMEOUT_'+name);time.sleep(.01)
    except BaseException as error:failure=error
    finally:
        try:cleanup=cleanup_owned_group(proc)
        except BaseException as error:
            cleanup={'ownership':'CLEANUP_ERROR_UNKNOWN','error_class':type(error).__name__,'reason':str(error),'direct_reaped':False}
            if failure is None:failure=error
        sel.close();proc.stdout.close();(operation/(name+'.log')).write_bytes(data)
        print(data.decode(errors='replace'),flush=True)
        code=cleanup.get('direct_exit_code')
        item={'name':name,'argv':argv,'exit_code':code,'log_sha256':hashlib.sha256(data).hexdigest(),
              'cleanup':cleanup,'failure':None if failure is None else {'class':type(failure).__name__,'reason':str(failure)}}
        report['runs'].append(item);save(operation/'receipt.json',report)
    if failure is not None:raise failure
    need(cleanup.get('direct_reaped') is True and cleanup.get('owned_group_live_after_kill')==[] and cleanup.get('proc_observation_incomplete') is False,'OWNED_GROUP_CLEANUP_NOT_CONFIRMED')
    need(code==0,'CHILD_FAILED_'+name)
    return data.decode()

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise RuntimeError('WHEEL_REDIRECT_REJECTED')

try:
    names=set();total=0
    # Authenticated HTTPS is limited to these six lock URLs, no proxy/redirect,
    # resolver, credentials, index lookup, sdist, setup.py or installer execution.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    for entry in lock['wheels']:
        tick();need(type(entry) is dict and set(entry)=={'name','version','filename','url','size','sha256'},'WHEEL_ENTRY_SHAPE')
        filename=entry['filename'];u=urllib.parse.urlsplit(entry['url'])
        need(type(filename) is str and re.fullmatch(r'[A-Za-z0-9_.-]+\.whl',filename) and filename not in names,'INVALID_WHEEL_FILENAME')
        names.add(filename)
        need(u.scheme=='https' and u.netloc=='files.pythonhosted.org' and not u.query and not u.fragment and u.path.endswith('/'+filename),'UNAPPROVED_WHEEL_URL')
        need(type(entry['size']) is int and 0<entry['size']<=607388 and re.fullmatch('[a-f0-9]{64}',entry['sha256']),'INVALID_WHEEL_BOUND')
        with opener.open(urllib.request.Request(entry['url'],headers={'User-Agent':'CP139-exact-validation/1'}),timeout=15) as response:
            need(response.status==200 and response.geturl()==entry['url'],'WHEEL_HTTP_OR_REDIRECT')
            if response.headers.get('Content-Length') is not None:need(int(response.headers['Content-Length'])==entry['size'],'WHEEL_LENGTH_HEADER')
            chunks=[];received=0
            while received<=entry['size']:
                tick();chunk=response.read(min(16384,entry['size']+1-received))
                if not chunk:break
                chunks.append(chunk);received+=len(chunk)
            data=b''.join(chunks)
        need(len(data)==entry['size'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'WHEEL_HASH_OR_SIZE')
        (downloads/filename).write_bytes(data);total+=len(data)
    need(total==607388,'WHEEL_TOTAL_SIZE')
    # Validate EVERY archive/member across ALL wheels before writing any payload.
    planned=[];destinations=set();expanded=0
    for entry in lock['wheels']:
        with zipfile.ZipFile(downloads/entry['filename']) as archive:
            info=archive.infolist();need(0<len(info)<=400,'WHEEL_MEMBER_COUNT');archive_names=set()
            for member in info:
                name=member.filename;p=PurePosixPath(name);parts=name.rstrip('/').split('/')
                need(name and '\\' not in name and '\x00' not in name and not p.is_absolute() and all(x not in ('','.','..') and ':' not in x for x in parts),'UNSAFE_WHEEL_PATH')
                need(parts[0].lower() not in ('bin','scripts') and not any(x.endswith('.data') for x in parts) and not name.lower().endswith('.pth') and not any(x.lower() in ('sitecustomize.py','usercustomize.py') for x in parts),'WHEEL_STARTUP_OR_SCRIPT_REJECTED')
                portable=name.rstrip('/').casefold();need(portable not in archive_names,'WHEEL_DUPLICATE_ENTRY');archive_names.add(portable)
                need(str(p)==name.rstrip('/'),'WHEEL_NONCANONICAL_PATH')
                mode=(member.external_attr>>16)&0xffff
                need(stat.S_IFMT(mode) in (0,stat.S_IFREG,stat.S_IFDIR) and not member.flag_bits&1,'WHEEL_LINK_OR_ENCRYPTION')
                if member.is_dir():continue
                key=name.casefold();need(key not in destinations and not any(key.startswith(x+'/') or x.startswith(key+'/') for x in destinations),'WHEEL_DUPLICATE_OR_PREFIX_COLLISION')
                destinations.add(key);need(0<=member.file_size<=2097152,'WHEEL_MEMBER_SIZE');expanded+=member.file_size;need(expanded<=16777216,'WHEEL_EXPANSION_LIMIT')
                data=archive.read(member);need(len(data)==member.file_size,'WHEEL_MEMBER_TRUNCATED')
                if name.endswith('.so'):need(entry['name']=='rpds-py' and name.endswith('.cpython-312-x86_64-linux-gnu.so'),'UNSUPPORTED_NATIVE_WHEEL_MEMBER')
                planned.append((name,data))
            metadata=[x for x in info if x.filename.endswith('.dist-info/METADATA')];wheelmeta=[x for x in info if x.filename.endswith('.dist-info/WHEEL')]
            need(len(metadata)==len(wheelmeta)==1,'WHEEL_METADATA_COUNT')
            md=email.message_from_bytes(archive.read(metadata[0]));wm=email.message_from_bytes(archive.read(wheelmeta[0]))
            norm=lambda v:re.sub('[-_.]+','-',v).lower()
            need(norm(md['Name'])==norm(entry['name']) and md['Version']==entry['version'],'WHEEL_METADATA_BINDING')
            tags=wm.get_all('Tag') or []
            need(('py3-none-any' in tags) if entry['name']!='rpds-py' else any(t in ('cp312-cp312-manylinux_2_17_x86_64','cp312-cp312-manylinux2014_x86_64') for t in tags),'WHEEL_ABI_TAG')
    for name,data in planned:
        dest=deps.joinpath(*PurePosixPath(name).parts);dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as stream:stream.write(data)
    deps_before=inventory(deps)
    report['public_wheels']=[{'name':e['name'],'version':e['version'],'sha256':e['sha256'],'bytes':e['size']} for e in lock['wheels']]
    report['wheel_data_only_expanded_bytes']=expanded
    # Three exact public Git fetches; no tags/branches/submodules/helpers/hooks.
    store=work/'control.git'
    git=['git','--no-pager','-c','credential.helper=','-c','core.hooksPath=/dev/null','-c','protocol.allow=never','-c','protocol.https.allow=always','-c','http.followRedirects=false','-c','http.lowSpeedLimit=1','-c','http.lowSpeedTime=15','-c','pack.threads=1','-c','index.threads=1','-c','maintenance.auto=false','-c','gc.auto=0','-c','gc.autoDetach=false','-c','maintenance.autoDetach=false']
    run('git-init',git+['init','--bare','--template=',str(store)])
    pins=['c06f435797142b77aa233fce9067e938942a0f5b','30f56e90e1fc103eaf0491838b53ba07f9ab732c','e0185b6bc6ef46a22ccf2196ccdbad2a2c9d4b52']
    for pin in pins:
        run('fetch-'+pin[:8],git+['-C',str(store),'fetch','--no-tags','--no-recurse-submodules','--depth=1','https://github.com/CT-Infrastructure/marketing-v7-control.git',pin])
        need(sum(q.stat().st_size for q in store.rglob('*') if q.is_file())<=16777216,'PUBLIC_GIT_STORE_SIZE_LIMIT')
        need(run('verify-'+pin[:8],git+['-C',str(store),'rev-parse','--verify','FETCH_HEAD^{commit}']).strip()==pin,'PUBLIC_FETCH_PIN_MISMATCH')
    public=work/'public';public.mkdir()
    for rel in source_before:
        src=ROOT/rel;dst=public/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    need(not (public/COMP/'inputs').exists(),'PUBLIC_INPUT_DESTINATION_MUST_BE_ABSENT')
    # The supplementary accepted fixture is acquired as raw exact Git blob bytes
    # before the network guard; it is added only to a separate F04-suite copy.
    seedcmd=git+['-C',str(store),'cat-file','blob','bfda46f0c85e0898faa2dafeb118b9e3c096295b']
    seedlog=run('accepted-seed-blob',seedcmd).encode()
    need(len(seedlog)==575 and hashlib.sha256(seedlog).hexdigest()=='2bf607cd04b12024ed561e9f60af9b2ef2c04c9d6500899794be92873e43b6ba','ACCEPTED_SEED_BYTES')

    # Unprivileged Linux x86-64 classic-BPF seccomp. arch mismatch/x32 kills;
    # network, io_uring and namespace/ptrace escape syscalls return EPERM.
    # This guard is inherited by all subsequently spawned tests/Git children.
    need(len(list(Path('/proc/self/task').iterdir()))==1,'SECCOMP_REQUIRES_SINGLE_THREAD')
    for fd in Path('/proc/self/fd').iterdir():
        try:need(not stat.S_ISSOCK(os.fstat(int(fd.name)).st_mode),'INHERITED_SOCKET_UNSUPPORTED')
        except OSError:pass
    class Filter(ctypes.Structure):_fields_=[('code',ctypes.c_ushort),('jt',ctypes.c_ubyte),('jf',ctypes.c_ubyte),('k',ctypes.c_uint)]
    class Program(ctypes.Structure):_fields_=[('len',ctypes.c_ushort),('filter',ctypes.POINTER(Filter))]
    # BPF_LD/W/ABS arch,nr; JEQ/JGE; RET. AUDIT_ARCH_X86_64=0xc000003e.
    code=[(0x20,0,0,4),(0x15,1,0,0xc000003e),(0x06,0,0,0x80000000),(0x20,0,0,0),(0x35,0,1,0x40000000),(0x06,0,0,0x80000000)]
    forbidden=[41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,101,272,288,299,307,308,310,311,321,425,426,427,438]
    for number in forbidden:code.extend([(0x15,0,1,number),(0x06,0,0,0x00050000|errno.EPERM)])
    code.append((0x06,0,0,0x7fff0000));filters=(Filter*len(code))(*(Filter(*x) for x in code));program=Program(len(code),filters)
    libc=ctypes.CDLL(None,use_errno=True);libc.prctl.restype=ctypes.c_int
    need(libc.prctl(38,1,0,0,0)==0,'NO_NEW_PRIVS_UNAVAILABLE')
    need(libc.prctl(22,2,ctypes.byref(program),0,0)==0,'SECCOMP_FILTER_UNAVAILABLE')
    try:
        sock=socket.socket();sock.close();raise RuntimeError('NETWORK_GUARD_NOT_ENFORCED')
    except PermissionError as error:need(error.errno==errno.EPERM,'NETWORK_DENIAL_NOT_EPERM')
    # Conservative descriptor-acquisition denial: an invalid pidfd/fd must hit
    # the filter's EPERM, not merely EBADF from descriptor validation.
    libc.syscall.restype=ctypes.c_long;ctypes.set_errno(0)
    need(libc.syscall(438,-1,-1,0)==-1 and ctypes.get_errno()==errno.EPERM,'PIDFD_GETFD_GUARD_NOT_EPERM')
    ENV['GIT_ALLOW_PROTOCOL']='';resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
    report['network_guard']={'kind':'inherited unprivileged seccomp BPF','socket_probe':'EPERM','pidfd_getfd_invalid_descriptor_probe':'EPERM','arch':'x86_64 only','filesystem_isolated':False,'provisioning_network_already_complete':True}
    # Child bootstrap imports only verified data-only extracted packages after guard.
    bootstrap="import sys,socket,errno;from pathlib import Path;sys.path.insert(0,DEPS);\ntry:\n s=socket.socket();s.close();raise RuntimeError('NETWORK_GUARD_MISSING')\nexcept PermissionError as e:\n if e.errno!=errno.EPERM:raise RuntimeError('NETWORK_DENIAL_NOT_EPERM')\n".replace('DEPS',repr(str(deps)))
    py=[sys.executable,'-I','-S','-B']
    run('canonical-public20-assembly',py+['-c',bootstrap+"\nimport runpy;sys.argv=['assemble_inputs.py','--control-repository',STORE,'--destination',DEST];runpy.run_path(ASSEMBLER,run_name='__main__')".replace('STORE',repr(str(store))).replace('DEST',repr(str(public/COMP/'inputs'))).replace('ASSEMBLER',repr(str(public/COMP/'assemble_inputs.py')))],cwd=public)
    for entry in json.loads((public/COMP/'public-inputs.lock.json').read_text())['sources']:
        q=public/COMP/entry['destination'];need(q.stat().st_size==entry['bytes'] and sha(q)==entry['sha256'],'PUBLIC20_ASSEMBLED_BYTES')
    pristine_before=inventory(public)
    origin_code=bootstrap+"\nimport importlib.metadata as m;import jsonschema,referencing,rpds;print([(n,m.version(n)) for n in ['jsonschema','referencing','jsonschema-specifications','attrs','rpds-py','typing-extensions']]);print([jsonschema.__file__,referencing.__file__,rpds.__file__]);assert all(Path(x.__file__).is_relative_to(DEPS) for x in [jsonschema,referencing,rpds])".replace('DEPS',repr(str(deps)))
    run('package-origins',py+['-c',origin_code])
    tests=bootstrap+"\n"+r"""import unittest,json
sys.path.insert(0,COMPONENT)
from assemble_inputs import load_dependency
f04=load_dependency('f04');f16=load_dependency('f16');seen={'schema':0,'transition':0,'tracking':0,'audience_export':0}
v=f04.validate;t=f04.check_transition;e=f16.evaluate
def cv(*a,**k):seen['schema']+=1;return v(*a,**k)
def ct(*a,**k):seen['transition']+=1;return t(*a,**k)
def ce(req,*a,**k):
 if req.channel in seen:seen[req.channel]+=1
 return e(req,*a,**k)
f04.validate=cv;f04.check_transition=ct;f16.evaluate=ce
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(TESTDIR,pattern='test_*.py'))
print(json.dumps({'cp139':dict(tests=r.testsRun,skips=len(r.skipped),errors=len(r.errors),failures=len(r.failures),unexpected_successes=len(r.unexpectedSuccesses),calls=seen)}))
sys.exit(0 if r.wasSuccessful() and r.testsRun==25 and not r.skipped and not r.unexpectedSuccesses and all(seen.values()) else 1)
""".replace('COMPONENT',repr(str(public/COMP))).replace('TESTDIR',repr(str(public/COMP/'tests')))
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        output=run('component-'+mode,py+flags+['-c',tests],cwd=public)
        lines=[json.loads(x)['cp139'] for x in output.splitlines() if x.startswith('{"cp139":')];need(len(lines)==1 and lines[0]['tests']==25 and all(lines[0][k]==0 for k in ('skips','errors','failures','unexpected_successes')),'COMPONENT_STRUCTURED_COUNTS')
    need(inventory(public)==pristine_before,'COMPONENT_TEST_SOURCE_DRIFT')
    supplementary=work/'supplementary-f04';shutil.copytree(public,supplementary);seed=supplementary/COMP/'inputs/F04/schemas/event-envelope.example.json';need(not seed.exists(),'SEED_COLLISION');seed.write_bytes(seedlog)
    f04tests=bootstrap+"\nimport unittest,json;sys.path.insert(0,CORE);r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(CORE,pattern='test_contracts.py'));print(json.dumps({'f04':dict(tests=r.testsRun,skips=len(r.skipped),errors=len(r.errors),failures=len(r.failures),unexpected_successes=len(r.unexpectedSuccesses))}));sys.exit(0 if r.wasSuccessful() and r.testsRun==30 and not r.skipped and not r.unexpectedSuccesses else 1)".replace('CORE',repr(str(supplementary/COMP/'inputs/F04/contracts/core')))
    supplementary_before=inventory(supplementary)
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        output=run('accepted-f04-'+mode,py+flags+['-c',f04tests],cwd=supplementary)
        lines=[json.loads(x)['f04'] for x in output.splitlines() if x.startswith('{"f04":')];need(lines==[dict(tests=30,skips=0,errors=0,failures=0,unexpected_successes=0)],'F04_STRUCTURED_COUNTS')
    need(inventory(supplementary)==supplementary_before and inventory(deps)==deps_before,'SUPPLEMENTARY_OR_TOOLING_DRIFT')
    need(inventory(ROOT)==source_before,'CHECKOUT_SOURCE_DRIFT')
    report.update(status='PASS_PUBLIC_CLOSURE',component_tests={'normal':25,'optimized':25,'skips':0},F04_supplementary_tests={'normal':30,'optimized':30,'skips':0},source_unchanged=True,tooling_unchanged=True)
except BaseException as error:
    report.update(status='BLOCKED_OR_FAILED',error_class=type(error).__name__,reason=str(error));raise
finally:
    report['remaining_log_budget_bytes']=LOG_BUDGET;save(operation/'receipt.json',report)
    # Remove only this operation's owned work subtree. Receipts/raw logs remain.
    need(work.parent==operation and operation.name.startswith('cp139-public-validation-'),'CLEANUP_OWNERSHIP')
    if work.exists():shutil.rmtree(work)
    report['owned_work_removed']=not work.exists();save(operation/'receipt.json',report);print(json.dumps(report),flush=True)
PY
