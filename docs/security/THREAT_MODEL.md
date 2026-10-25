# Threat model and enforcement points

| Threat | Enforcement / proof required | Owner |
|---|---|---|
| Malicious issue, source page or prompt injection | Immutable task packet, no issue-driven argv/tools, scope checking and independent approvals; prompt-only promises are insufficient | F03/F12 |
| Agent edits control policy or forges success | No controller DB/mount, trusted manifest hash, protected paths, broker-side GitHub verification and separate review | F11/F13/F14 |
| Build dependency/model/custom node compromise | Approved source, exact digest/lock, SBOM, Trivy, node allowlist, isolated test execution | F09/CP tasks |
| Container escape or lateral network movement | Disposable engineering VM + rootless container defense in depth; no production routes/socket/credentials; seccomp/LSM and egress probes | F06/F12 |
| Secret/PII exfiltration | Synthetic fixtures, minimized task context, scope-bound identities, no broad credential mounts, secret scanning/redaction and retention | F10/F16 |
| Lease expiry races or duplicate dispatch | Atomic claims, fences, retained orphan locks, kill/reap proof, provider idempotency and uncertain-result reconciliation | F11/X02/X06 |
| Shared-file race or destructive Git action | Disjoint owned paths, prefix-aware locks, snapshot isolation, trusted integration worktrees, protected main | F13 |
| Cross-client data exposure | App/API/asset/DB/metrics partition tests; no assumption that segments equal tenants | I13/M16/M19/IT06 |
| Forged/replayed webhook, SSRF or XML/file parser attack | Raw-body signature verification, timestamp/replay window, schema/body limits, deny-by-default egress, hardened parsers/jobs | X01/X05/E14 |
| Unapproved send/call/publication/spend | Final channel-specific guard, atomic quota, exact human approval, network/credential restriction, source reconciliation | X03/X04/E11/E12/V02/G04–G08 |
| Lost source data or unsafe rollback | Private source custody, immutable generations, coherent DB/files backup, held restore, single writer and later suppression replay | I23/I24/I25/I26 |
| Swarm exhausts CPU/GPU/budget or voice latency | Resource/monetary reservation before launch, finite timeout/retry, actual usage reconciliation, priority reservation | F08/F17/I28 |

Residual risks include kernel/runtime defects, compromised approved upstreams, social engineering of human approvers, unavailable provider APIs, false-positive/negative scanners and one-host power/ISP failure. Document accepted residual risks with owner and expiry; do not claim enterprise high availability from a single host.

All security exceptions must identify affected component, exact setting, reason, restricted scope, compensating controls, reviewer, expiry and test evidence. Blanket `--privileged`, host sockets, broad host mounts or unconfined security profiles are not acceptable default exceptions.
