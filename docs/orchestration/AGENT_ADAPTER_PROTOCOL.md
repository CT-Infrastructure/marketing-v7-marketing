# Provider-neutral agent adapter contract

F12 qualifies one real adapter before unattended launch. Choose an available native agent orchestration tool or an approved CLI inside a digest-pinned container. Do not install a second business workflow platform to implement this engineering control plane. The package deliberately does not invent an agent-provider command or include a credential.

## Inputs
The trusted launcher writes `/task/task.json`, supplied read-only, with task metadata, immutable base revision, input hash, lease token, fence and owned paths. The full reviewed repository snapshot is at `/workspace`; only the task's allowed scopes are writable. `/out` is a bounded results directory. The adapter must read AGENTS.md, the complete issue body and its source references, then the role prompt selected from the trusted task kind:

| Task kind | Role prompt |
|---|---|
| implementation | `prompts/03_IMPLEMENTER.md` |
| test-authoring | `prompts/04_TEST_AUTHOR.md` |
| verification / integration | `prompts/06_VERIFIER.md` |
| component / preservation / provider | `prompts/10_COMPONENT_BUILDER.md` |
| foundation | Corresponding foundation brief, under coordinator supervision |
| selection | `prompts/11_CONDITIONAL_DECISION.md`; disabled until explicitly selected |
| human-gate / epic | Not eligible worker jobs |

Never pass issue prose as executable shell. The image, program and argument list come from trusted policy. Never allow a worker to start unmanaged nested workers or change its model/budget/network privileges without coordinator admission. A provider's own native multi-agent feature must account for every child in the same budgets and leases.

## Outputs
Write `/out/result.json` conforming to `schemas/agent-result.schema.json`. A result may request `ready_for_review`, `blocked` or `failed`; it cannot claim ACCEPTED. Preserve packet task/token/fence/input/base bindings. List every actual changed regular file under owned paths and each artifact hash. Include actual test commands, exit codes, evidence level and unavailable checks. Never include secrets or raw private inventory in the result.

The host computes the actual source diff and verifies artifact hashes. Symlinks, special files, path traversal, undeclared changes, stale input or results outside scope are rejected. Agent Git metadata and hooks are never trusted. Returning a successful process exit without a valid result does not complete work.

## Qualification tests
Prove clean start/exit and cancellation, timeout with a possible remote job still running, denied management/VPN/cloud-metadata/IPv6 destinations, per-task writable scopes, bounded disk/log/output, no engine socket or production credential access, and token revocation. Enforce RPM/TPM and monetary ceilings outside the untrusted process through provider-account policy or a trusted broker. Detect unknown usage and charge the conservative reservation until reconciled. Keep reserve capacity for operating systems, backups, databases and real-time voice. Provider unavailability must not trigger an unapproved fallback model or channel.

The supplied `run_agents.py` is a CPU-only single-host reference launcher. GPU scheduling, provider-native remote jobs, distributed coordination and verified Git integration are separate qualifications. A capability statement, successful import, model-generated test report or Boolean in a local example policy is not qualification evidence.
