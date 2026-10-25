# Security policy

Report suspected vulnerabilities privately to the named repository security owner through the private channel configured during F02. Until that owner/channel is configured, do not open public issues with exploit details, credentials, personal data or production topology. No actual private reporting address is invented here.

Supported scope is the pinned, reviewed release in this repository; a version-selection document does not establish patch currency. Dependency, model and container updates require review, regression tests and rollback evidence. Scan source and built artifacts; scanners complement rather than replace review.

All environments begin with external actions disabled. Separate coding/metadata/review/integration/deployment identities and networks. Source archives containing historical operational evidence are never uploaded wholesale. Treat any exposed secret as compromised: stop, restrict access, rotate at the authority, review logs and publish only redacted incident evidence.

See `docs/security/THREAT_MODEL.md`, `CONTAINER_AND_HOST_BASELINE.md`, `CREDENTIALS_AND_CI.md` and `docs/orchestration/EXECUTION_PROTOCOL.md`. The security controls in this package require site and runner validation before autonomous operation.
