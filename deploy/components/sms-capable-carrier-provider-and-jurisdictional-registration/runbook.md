# CP141 offline SMS contract
This is an external-contract-and-mock, with no service, installer, Containerfile,
scheduler, socket, SDK or native database writer. Mautic.sms owns SMS consent,
STOP/revocation and suppression; Activepieces remains orchestration owner.
F05 providers defines receipt.read / transport.submit / transport.cancel.
The mock only simulates receipt sequences; even ELIGIBLE_OFFLINE stays HOLD.

Use C:/Python314/python.exe -B [-O] -m unittest discover -s
deploy/components/sms-capable-carrier-provider-and-jurisdictional-registration/tests
-p test_*.py -v from the clean marketing checkout AFTER the public assembly in README.md.
The mock uses only component-local inputs; there is no private campaign-path
fallback. Full F04 validation has separate approved dependencies.
The caller supplies authenticated current F16 snapshots, current approval and
a reviewed max_age policy, with one coherent UTC simulation time. Synthetic
approval is not OpenProject authentication. No fixed permission clock exists.

Backup using snapshot(); restore validates receipt history and preserves keys,
reservations and callback replay IDs. New requests still require current F16
eligibility, including native generation and authenticated restore replay.
Return snapshots and receipts are deep copies. UNKNOWN never retries. Both
OCCURRED and NOT_OCCURRED append receipts; NOT_OCCURRED retains an action tombstone.
Rollback keeps the journal and HOLD; do not clear uncertainty or dedupe keys.

Provider selection, API/runtime/version/edition/digest/license, account scopes,
registration, sender identity, prices and signature/idempotency capability are
UNKNOWN, owned by Human provider/compliance owner. Real consent/STOP/replay,
review freshness and native authority availability belong to Privacy/Mautic owner.
Security/platform owner must qualify runtime workers, DB/cache, UID/GID,
storage/network enforcement, credentials references, SBOM/vulnerability evidence,
installation, authenticated backup and real recovery. No actual installation,
sandbox/staging/native operation or provider acceptance was executed.
No Quadlet rendering applies to this external classification.

F04 receipts retain its identity hashing, fields and transition semantics.
Full runtime schema validation requires the trusted pinned jsonschema/referencing
verifier; that execution is NOT_RUN in this stdlib-only worker. No substitute
schema authority is supplied. Independent verifier owns guard mutation in a
disposable copy, exact candidate validation and review; root owns CI, Copilot,
private transport binding and integration. Those are not claimed here.

Historical receipt correction (R2): RECONCILED/OCCURRED has outbound_state
CONFIRMED, a provider object and reservation_retained=true. This is past synthetic
occurrence, not runtime authorization. Session/snapshot/restore stay HOLD.
NOT_OCCURRED has HOLD, null object and reservation_retained=false; its tombstone
prevents retry. Original test_mock.py and the archived original 20-test evidence
remain unchanged; new tests add the exact corrected semantics.

Worker Git execution and canonical public-source validation are NOT_RUN; root
owns hermetic integration. Supplied accepted-export assembly and synthetic
transport tests are separate evidence, not proof of a public Git clone. The full
F04 validator is skipped with an explicit NOT_RUN reason when jsonschema/referencing
are absent. Targeted tests inspect exact hash-pinned accepted then-clauses and run
accepted check_transition code with schema validation stubbed; that transition
check is partial and never reported as full validation.
