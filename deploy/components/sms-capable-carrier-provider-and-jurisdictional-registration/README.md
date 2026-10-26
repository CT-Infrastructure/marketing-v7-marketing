# CP141 reproducible public dependencies

These commands are for root/user execution in a separately authorized public
integration environment, from a clean marketing checkout with this candidate.
They are documentation only; the worker does not execute Git or network calls.

```powershell
git clone --no-checkout https://github.com/CT-Infrastructure/marketing-v7-control.git ../marketing-v7-control
git -C ../marketing-v7-control cat-file -e 'c06f435797142b77aa233fce9067e938942a0f5b^{commit}'
git -C ../marketing-v7-control cat-file -e '30f56e90e1fc103eaf0491838b53ba07f9ab732c^{commit}'
git -C ../marketing-v7-control cat-file -e 'e0185b6bc6ef46a22ccf2196ccdbad2a2c9d4b52^{commit}'
$component = Join-Path (Get-Location) 'deploy/components/sms-capable-carrier-provider-and-jurisdictional-registration'
$control = (Resolve-Path ../marketing-v7-control).Path
C:/Python314/python.exe -B "$component/assemble_inputs.py" --control-repository "$control" --destination "$component/inputs"
C:/Python314/python.exe -B -m unittest discover -s "$component/tests" -p 'test_*.py' -v
C:/Python314/python.exe -B -O -m unittest discover -s "$component/tests" -p 'test_*.py' -v
```

The clone must contain all three commits before assembly. Assembly runs with
read-only source and network disabled; no fetch, checkout, hooks, installations
or repository scripts are invoked. Root CI and independent acceptance remain
separate owner responsibilities. Missing commits fail closed.

public-inputs.lock.json pins all 20 approved regular inputs, with exact repository,
commit, source path, destination, SHA256 and bytes. F04 is pinned to
c06f435797142b77aa233fce9067e938942a0f5b, F05 to
30f56e90e1fc103eaf0491838b53ba07f9ab732c, and F16 to
e0185b6bc6ef46a22ccf2196ccdbad2a2c9d4b52. The reviewed lock is source, not a
mutable branch or a caller-supplied lock. Only Git regular blobs 100644/100755
are accepted. The mock loads F05/F16 from component-local inputs only, with no
private export fallback. Generated inputs are ignored by component .gitignore
and excluded from the candidate; no competing contracts are vendored.

--destination accepts an absolute, absent destination under an existing parent.
For alternative destinations, place the reviewed component alongside its inputs
before running the documented test command. The parent must be exclusively held
by the caller; no symlink/junction ancestors are allowed. Same-parent staging
and rename publish only a complete validated assembly. Failure removes staging;
existing assemblies/collisions are refused. Refresh in a new disposable checkout
or destination, preserving prior evidence. Concurrent hostile filesystem owners
are outside this single-caller offline tool's guarantees.

Dependency license: UNKNOWN. Root/legal owner must confirm the public repository
license at each pinned revision before redistribution; no license file was supplied
among accepted inputs. Public provenance does not establish license clearance,
provider selection, runtime qualification or actual Git validation by this worker.
Full F04 validation requires the separately approved jsonschema/referencing
verifier. No dependency installation is performed here. See runbook.md and
security.md for historical CONFIRMED receipts versus runtime HOLD.
