# Parallel-agent execution protocol

## 1. Three different graphs
The source runtime graph contains 1,847 handoffs/control/runtime relationships and can contain feedback loops. It describes business operation, not the order in which engineers must write code. `orchestration/task_graph.json` is the acyclic build prerequisite graph. Parent/sub-issue relationships describe reporting hierarchy, not execution dependency. Do not merge these graphs.

Each of the 190 workflows has BUILD, TEST and VERIFY packages. BUILD and TEST can begin independently after their interface/harness prerequisites; VERIFY waits for both and relevant component/control evidence. Components, infrastructure configuration, documentation, adapters and fixtures can advance in parallel. Integration slices test real boundaries after local qualifications. Human production gates are never schedulable coding tasks. Conditional candidate packages remain deferred until a reviewed selection changes the graph.

## 2. Admission and maximum useful concurrency
A task is runnable only when enabled, not manual, all hard prerequisites are ACCEPTED, capacity is available, no conflicting path/exclusive lock is held, required agent capabilities exist, and global/account/provider budgets permit a start. A task count is not hardware capacity. Before dispatch, the trusted source checkout must contain the accepted prerequisite revisions; a stale local HEAD cannot satisfy an accepted dependency. The integrator refreshes the trusted checkout after merges; the launcher verifies Git ancestry before issuing dependent work. Use measured CPU, memory, disk, GPU/VRAM and dedicated integration slots, with headroom for OS, backups and real-time voice. Provider RPM/TPM, account concurrency and monetary caps can be the tighter bound. Spend ceilings must be enforced by the provider account or trusted egress broker outside the untrusted worker, not merely by a CLI option the worker can alter.

The scheduler greedily fills available slots in priority/critical-path/age order; it is not a mathematical guarantee of globally optimal packing. Use all *admissible* parallel work, not arbitrary unlimited worker counts. Do not batch the whole program behind a phase barrier. When the frontier shrinks, split a genuinely divisible task or improve contracts rather than ignore dependencies. Parallelize review/test authors where trusted capacity exists. Serialize only shared paths, environment mutations, database migration application, main integration and protected production changes.

## 3. Ownership, claims and fencing
One trusted controller owns a local SQLite ledger (standard Python library, not a new production service). Claims use `BEGIN IMMEDIATE` and reserve task, path locks, explicit locks and capacity atomically. Each claim has an unpredictable token plus monotonically increasing fence, attempt number, deadline and immutable input/base hash. Agents cannot open or edit that ledger. Project fields/comments are projections only.

The trusted launcher heartbeats live processes; an agent cannot keep a dead job alive by posting a comment. A lease expiration enters ORPHANED and retains reservations and locks. The controller first kills/reaps the known container/process, rejects all later stale results, reconciles any external PR/job creation, then explicitly releases/requeues. Never automatically retry an uncertain provider submission or assume a TTL fences a running remote agent. Retry budget is finite; repeat failures create scoped repair work.

## 4. Isolated implementation
Each task receives a fresh exported source snapshot and task packet. No shared writable checkout, Git metadata, agent home, tokens, Docker/Podman socket or coordinator state is mounted. A container has its own UID/limits/tmp/output. Agent-created Git metadata is untrusted and discarded. The trusted integrator owns separate Git worktrees and copies only verified, allowed regular files from a candidate into them; it does not run agent hooks/config.

Containers are rootless, read-only except the task workspace/output and bounded tmpfs, capability-dropped with no-new-privileges and default seccomp/LSM. Network defaults to none. A model/API-dependent agent needs a specifically approved isolated network or provider-native sandbox. A rootless bridge by itself is **not** an egress firewall; prove management LAN, cloud metadata, VPN and IPv6 paths are blocked before enabling network. Inference tokens, when needed, are narrow and task-scoped; no production secrets. Agent binaries/argv/image come from trusted adapter configuration, never issue text.

## 5. Completion and merge
Agent result → host-side scope/manifest validation → independent reviewer → CI at exact candidate revision → trusted integrator PR/merge queue → verified merge receipt → ACCEPTED. Only then can build dependents start. Verification tasks similarly require an independent executor receipt at the declared evidence level. A worker exit code, agent-written JSON, closed issue, checklist or project status cannot establish acceptance.

A model reviewer alone does not substitute for required human security/production approval. High-risk work has a different verifier identity from implementation and test author. Review and verification use read-only candidate artifacts; reviewers cannot silently rewrite tests. Protected file changes require their named owner. Candidate commits are re-tested when rebased. The controller can use official GitHub merged-PR metadata plus required check/review/ruleset evidence, and records all limitations.

## 6. Safe stops and blocked work
Global STOP prevents new claims, cancels/revokes active work according to policy and quarantines uncertain results. Stop new work on cost exhaustion, compromised credentials, sandbox escape suspicion, unhealthy shared test infrastructure or integrity failure. Do not automatically clear the stop flag.

A blocked task records the exact missing fact/credential/interface and an unblock owner. Other ready work continues. Site and provider absence should not stop unrelated mock-based implementation. Conditional branches do not block the core release by accident; a human records non-applicability where appropriate. Deferred never means implemented.

## 7. Status and proof
Expose READY/RUNNING/REVIEW/BLOCKED/ORPHANED/ACCEPTED counts, queue age, actual worker processes, resource reservations, spend, conflicts, test freshness and bottleneck. Report launched agents only when an adapter returned a real job/process ID. The bundled demo is synthetic and does not launch AI agents. This package does not install or test a chosen commercial/native agent provider for you.

## 8. Scale boundary
The reference ledger supports one coordinator on one durable local filesystem. Multiple agents may run in parallel and multiple controller threads/processes can contend safely on that file, but it is not a distributed production scheduler. For multi-host agents, implement and qualify a trusted broker/remote adapter through F11/F12, reuse approved infrastructure where practical, and maintain fencing/kill/reconciliation semantics. Do not put the SQLite database on network storage and call that high availability.
