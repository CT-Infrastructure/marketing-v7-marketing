# Credentials, GitHub and CI trust

## Identity separation
Bootstrap administrator may create the private repository/project and configure policy; retire or remove elevated scopes after setup. Metadata coordinator needs only approved issue/project read/write, not repository administration or deployment. Workers receive source snapshots and no GitHub write token by default. Independent reviewers read candidates; trusted integrator writes topic branches/PRs and requests merge under repository protections. Production operator uses a separate approval path and credentials outside the agent environment.

Projects access is distinct from repository issue access; test exact token/App/account capability. Prefer narrowly scoped GitHub App installation tokens for appropriate organization automation; personal Projects and permissions may need a different reviewed identity. Do not silently fall back to a broad personal token. Do not ask the user to paste secrets into chat or issue bodies. The package tools invoke `gh` using existing trusted authentication; they never print token values.

## GitHub Actions
Default workflow permission is `contents: read`; job-scoped additional permissions require justification. Pin actions to verified full commit SHA and review transitive dependencies. Optional workflow dependency lockfiles are a preview/platform feature and are not assumed. `persist-credentials: false`; no direct interpolation of issue titles/bodies into shell. No `pull_request_target` checkout/execution of untrusted head code. No deployment from an untrusted `workflow_run` artifact without provenance verification. No secrets or write tokens in ordinary PR builds.

Prefer clean hosted runners or clean disposable engineering VMs. Persistent self-hosted runners can be compromised even for private-repository PRs. A production runner is not an acceptable place to run arbitrary agent code. Production routes and credentials remain absent from untrusted runners; required environment reviews do not themselves isolate a runner.

## Protected branches, environments and plan limits
Validate the account plan and private repository capabilities. A private repository may not support required reviewers/environments/rulesets on the chosen plan. A UI checkbox, fallback label or issue comment does not replace unavailable enforcement. Block autonomous merge/deployment until an equivalent externally enforced human-controlled path is approved; never make a repository public just to obtain a feature.

CODEOWNERS is generated only after actual accounts/teams and write access are verified. Protect `.github/`, `tools/`, `orchestration/`, `schemas/`, `config/`, lockfiles and production configuration. Only enforce required checks after the workflows really exist and run; do not create an impossible bootstrap. No bypass for a generic coding bot. At least one human code-owner review for security/control-plane changes; two-person authorization for production-critical changes where available. Native environment reviewer lists generally require one listed reviewer, not an automatic two-person quorum; implement the desired quorum explicitly.

## Release and data
Build/scan/test the same immutable artifact digest promoted to production. Signed attestations are useful only with verified issuer, subject and workflow identity. Separate identity minting from untrusted builds; OIDC requires scoped claims/audience and short TTL. No signed result is trusted just because a model pasted it. Git and evidence stores contain only sanitized manifests; encrypted secrets still require careful repo access and offline key custody. Secret exposure triggers rotation, not merely deletion of the visible string.
