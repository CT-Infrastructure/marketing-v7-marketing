# Contributing and agent handoff

Use one stable package key per branch/PR. A test-authoring task may run concurrently with its implementation task because their write paths differ. A verifier waits for both merged revisions and required component evidence. A merged PR is engineering progress, not a campaign approval.

Before proposing changes run `python tools/validate_package.py` and `python -m unittest discover -s tests/package -v`. These validate the package tooling, not all marketing services. Each implementation task must add its own executable unit/contract tests; independent test suites and native integration checks follow the backlog.

Work outside protected root files unless the task explicitly owns them. Shared lockfile/schema updates go through a contract maintainer and are merged before consumer rebases. No broad formatting or opportunistic upgrades in unrelated paths. Split oversized tasks into scoped child packages through reviewed manifest updates.

A PR must include package key, base/candidate commit, owned path diff, test commands/results, security analysis, dependency versions, rollback, evidence level and blockers. Test evidence becomes stale when the tested commit or relevant dependency changes. Code owners and an independent reviewer approve; the trusted integrator serializes updates to main or uses a supported merge queue. No auto-merge based only on an agent's prose.

Raw evidence with customer or infrastructure identifiers stays in the approved private evidence store. Git contains sanitized manifests and hashes. Preserve license obligations and upstream notices; no blanket license for third-party software is asserted.
