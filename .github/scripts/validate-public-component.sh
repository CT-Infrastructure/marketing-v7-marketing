#!/usr/bin/env bash
# CP141 public assembly; hosted stdlib coverage is partial F04 coverage.
set -euo pipefail
[[ "$#" = 1 && "$1" = cp141 ]] || { echo 'usage: validate-public-component.sh cp141' >&2; exit 2; }
export PYTHONDONTWRITEBYTECODE=1
unset PYTHONPATH PYTHONHOME
python3 -B -c 'import sys; sys.exit(0 if (3,12) <= sys.version_info[:2] < (4,0) else "Python >=3.12 and <4.0 required")'
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
component="$root/deploy/components/sms-capable-carrier-provider-and-jurisdictional-registration"
cd -- "$root"
# Discard inherited Git config, object paths, helpers, transport and tracing overrides.
for variable in "${!GIT_@}"; do unset "$variable"; done
unset SSH_ASKPASS SSH_AUTH_SOCK
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/false
export GIT_NO_REPLACE_OBJECTS=1 GIT_NO_LAZY_FETCH=1
export GIT_ALLOW_PROTOCOL=https
# Empty init templates and hooks; no credentials or configurable URL rewriting.
public_git() {
  command git -c credential.helper= -c core.hooksPath=/dev/null \
    -c protocol.allow=never -c protocol.https.allow=always "$@"
}
# Fail before fetching if the reviewed lock's repository or commit set drifts.
python3 -B - "$component" <<'PY'
import importlib.util, json, pathlib, sys
component = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('cp141_assembler', component / 'assemble_inputs.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
lock = json.loads(module.LOCK.read_text(encoding='utf-8-sig'), object_pairs_hook=module.no_duplicate_keys)
sources = module.validate_lock(lock)
expected = {'c06f435797142b77aa233fce9067e938942a0f5b',
            '30f56e90e1fc103eaf0491838b53ba07f9ab732c',
            'e0185b6bc6ef46a22ccf2196ccdbad2a2c9d4b52'}
if {item['commit'] for item in sources} != expected:
    sys.exit('reviewed CP141 commit set changed')
PY
# Do not create inputs: canonical assembly requires an absent destination.
test ! -e "$component/inputs" && test ! -L "$component/inputs"
scratch=$(mktemp -d "${RUNNER_TEMP:-/tmp}/public-component.XXXXXXXX")
control="$scratch/control.git"
public_git init --bare --template= "$control"
# Exactly three public fetches; no branches, submodules, provider APIs or retries.
for pin in c06f435797142b77aa233fce9067e938942a0f5b 30f56e90e1fc103eaf0491838b53ba07f9ab732c e0185b6bc6ef46a22ccf2196ccdbad2a2c9d4b52; do
  public_git -C "$control" fetch --no-tags --no-recurse-submodules --depth=1 \
    https://github.com/CT-Infrastructure/marketing-v7-control.git "$pin"
  test "$(public_git -C "$control" rev-parse --verify 'FETCH_HEAD^{commit}')" = "$pin"
  test "$(public_git -C "$control" rev-parse --verify "$pin^{commit}")" = "$pin"
done
# No further network: canonical assembler checks regular mode, bytes and SHA256
# of every locked blob and atomically publishes the component-local inputs.
export GIT_ALLOW_PROTOCOL=
python3 -B "$component/assemble_inputs.py" --control-repository "$control" --destination "$component/inputs"
# Run both modes even if one suite fails. No pip and no test substitutions.
status=0
for mode in normal optimized; do
  flags=(-B)
  if [[ "$mode" = optimized ]]; then flags+=(-O); fi
  if python3 "${flags[@]}" - "$component/tests" "$mode" <<'PY'
import json, sys, unittest
suite = unittest.defaultTestLoader.discover(sys.argv[1], pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
summary = dict(mode=sys.argv[2], expected_tests=33, tests_run=result.testsRun,
               skipped=len(result.skipped), failures=len(result.failures),
               errors=len(result.errors), unexpected_successes=len(result.unexpectedSuccesses),
               expected_failures=len(result.expectedFailures), coverage='partial F04; full host evidence separate')
print(json.dumps(summary, sort_keys=True), flush=True)
if result.testsRun != 33:
    print('CP141 test inventory changed: expected 33; investigate', file=sys.stderr)
sys.exit(0 if result.wasSuccessful() and result.testsRun == 33 else 1)
PY
  then :; else status=1; fi
done
exit "$status"
