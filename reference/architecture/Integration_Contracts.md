# Integration and execution contracts

These are normative implementation requirements for the reference design, not installed schemas or turnkey application exports. Use supported native APIs; do not write directly to application-private database tables to bypass ownership.

## Event envelope

```json
{
  "schema_version": "1",
  "event_id": "authoritative-provider-or-local-id",
  "source_system": "approved-source",
  "event_type": "verified-business-event",
  "occurred_at": "RFC3339-UTC",
  "received_at": "RFC3339-UTC",
  "client_id": "internal-partition",
  "campaign_id": "internal-campaign-id",
  "workflow_id": "M01",
  "correlation_id": "end-to-end-reference",
  "subject_ref": "native-authority-reference-not-raw-contact-data",
  "revision_hash": "exact-approved-content-and-assets-hash",
  "policy_version": "approved-policy-reference",
  "approval_ref": "OpenProject-decision-and-revision",
  "payload_ref": "authorized-minimal-payload-location"
}
```

Reject unauthenticated, expired/replayed or malformed callbacks before effects. Verify signatures over the provider's required raw bytes; apply bounded clock tolerance and provider-specific replay semantics. Persist a receipt once; duplicate arrivals return the original disposition, not a new action. Do not infer provider IDs or timestamps when absent—assign an explicit local receipt and document the deduplication limitation.

## Authorities and actions

| Boundary | Reads | Allowed writes | Blocking conditions |
|---|---|---|---|
| Mautic | Native contact, consent, suppression, journey | Supported contact/segment/campaign API under policy | Missing current eligibility; ambiguous identity; independently prohibited channel |
| WordPress | Revision, post status, assets | Approved staging/publish/update/withdraw API | Revision/hash/account mismatch; unapproved media; unknown prior publication |
| Postiz | Account scopes, schedule, native post ID | Approved native scheduling/action | Temporal/native worker unavailable; unknown result; revoked social token |
| OpenProject | Exact decision, approver and work item | Tasks, review requests, audit links | Missing authority or stale approval; LLM cannot approve itself |
| ResourceSpace | Original/approved asset, rights, expiry | Authorized asset/version metadata | Missing right, expired permission or content/asset mismatch |
| Asterisk/controller | Call policy and current live sessions | Controller-originated ARI operations only | Phone permission/window/cost/concurrency unknown; prior call outcome uncertain |
| SMTP | Current sender policy, eligibility and reservations | Sole guarded Mautic transport integration | Unreadable policy, exhausted quota, suppression or ambiguous prior acceptance |
| Ad/SMS/commerce APIs | Source-authoritative account/order/delivery state | Separately authorized bounded mutations | Channel permission, owner, budget or true order authority absent |
| PostgreSQL ledgers | Cross-app operational references | Inbox/outbox, action receipts, audits, snapshots | Native app ownership must not be duplicated or overridden |

## State and atomicity

A common operational state model is RECEIVED → VALIDATED → READY → AUTHORIZED → RESERVED → SUBMITTING → ACCEPTED/CONFIRMED → RECONCILED → COMPLETE. Separate branches are REJECTED, HOLD, UNKNOWN, RETRY_DUE, DEAD_LETTER, CANCELLED and WITHDRAWN. Native product states remain native; this model records the integration attempt, not a competing campaign or CRM state machine.

The unique action scope is `(client_id, source_system, source_event_id, action_scope, approved_revision)`. Use unique constraints and short transactions for inbox receipt and outbox intent; a lease identifies the current worker/expiry. Never hold a database transaction open across an unbounded external API call. A stale lease or restarted worker must first inspect prior attempt/receipt before resubmission. Conditional compare-and-swap/state version prevents two workers claiming the same action.

Exactly-once external effects cannot generally be guaranteed by a local transaction. Use provider idempotency keys where supported; otherwise persist intent before action and reconcile response/native IDs. A timeout after potential acceptance is UNKNOWN, not proof of failure. Persist reservation and uncertainty; query native state or require operator review before another attempt. A direct application action without a provider idempotency key must pass a tested destination-specific reconciliation strategy.

Email quotas and call concurrency use atomic reservations with policy/version scope and explicit expiry/reconciliation semantics. Expiry is not permission to resend a potentially accepted message. A definitive rejection may safely release the appropriate reservation; acceptance and UNKNOWN must follow the provider/policy-specific ledger treatment. Daily time windows use the recipient/sender policy timezone and UTC instants; daylight-saving transitions and clock skew are acceptance cases.

## Approval and consent tokens

An approval record names the authorized human/role, client, campaign, destination account, revision hash, asset hashes, limits, schedule window, policy version and expiry. A material revision, destination or asset change invalidates it. Read final approval and independent channel eligibility immediately before the effect; recheck after delays or lease recovery. Opt-out, withdrawal or safety hold takes precedence over pending authorizations.

## Required custom engineering inventory

| Integration | Required implementation | Deployed by this package? |
|---|---|---|
| Event intake | Source-specific signature, schema, replay validation | No |
| Identity linkage | Pseudonymous mapping to native authority; no second CRM | No |
| Transactional inbox/outbox | Database migrations, uniqueness, leases, receipt retention | No |
| Approval binding | OpenProject decision mapping to immutable revision/destination | No |
| Mautic final dispatch guard | Exact release transport hook/adapter covering every send path | No |
| Email quota/reservation controller | Concurrent-worker atomic limits and uncertainty ledger | No |
| Phone controller | State, permission, schedule, ARI origination, reconciliation | No |
| Pipecat media/tool bridge | Pinned media protocol and scoped tool-call enforcement | No |
| Content/browser/media jobs | Resource-limited job wrappers, validated inputs/outputs | No |
| Native publication adapters | Staging, destination IDs, unknown-result reconciliation | No |
| Parsedmarc ingestion | Pinned optional PostgreSQL backend or validated small adapter | No |
| Metric normalizers | Source/freshness/unit/currency/model-aware snapshots | No |
| Retention and deletion | Authority-driven tombstones, export cleanup, restore re-deletion | No |
| Legacy telemetry/scheduler migration | Producer discovery, dedupe implementation, single-owner handover | No |
| Diagram documentation build | Catalog → Mermaid → SVG/PNG → atlas → validation | Yes, local documentation tooling |

No custom adapter becomes an unowned permanent platform. Assign an owner, source repository, tested release, dependency lock, resource budget, monitoring, upgrade/rollback plan and recovery contract. Native scheduling remains within Mautic/Postiz/etc.; Activepieces coordinates cross-application transitions.

## Observability and failures

Use correlation_id, workflow_id, client partition, revision, native object IDs, state and redacted error class. Do not use phone/email/contact names as Prometheus labels. Record provider latency, queue age, lease expiration, retries, UNKNOWN age, stale consent, duplicate suppression, missed schedules and dead-letter age. Do not emit raw credentials or unrestricted prompt inputs into logs.

Classify failure as invalid, unauthorized, unavailable-before-effect, ambiguous-after-effect, rejected-permanent or recoverable-transient. Retries have attempt/time budgets, jitter, expiry and fresh authorization checks. Exceptions route to an owned OpenProject work item with minimally necessary evidence. Repair produces a new audited transition rather than editing history. Circuit breakers scope to the failed channel/client/sender where possible; do not stop unrelated transactional services without policy.

## Restore and replay invariant

Restore in isolation and HOLD. Validate data generations and decryptability; rehydrate current suppression, revocation and deletion state; query native/provider effects newer than the backup; repair receipt links; obtain human approval; release a small canary; only then resume native schedules. External email/calls/publications/payment effects cannot be undone by rolling back a VM snapshot.
