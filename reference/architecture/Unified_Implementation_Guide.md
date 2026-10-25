> Imported V7 reference; links to the original atlas or historical Sources/ paths refer to the separately retained source package, not this repository. Do not execute historical commands.

# Unified Implementation Guide
## V7 · consolidation revision 1 · 25 October 2026

**Authority:** V7 is the software and workflow decision baseline. This consolidated edition is the current planning/rebuild reference and supersedes `train-router-rebuild-docs-2026-10-24.zip` as an operating design. The old ZIP remains immutable historical evidence. Nothing in this package attests that software has been installed, a migration has happened, a provider has approved access, or production acceptance has passed.

### Start with the interconnected views

[System overview](../PNG/A00.png) · [Deployment boundaries](../PNG/A01.png) · [Authority and execution contract](../PNG/A02.png) · [Complete 190-workflow graph](../SVG/A03.svg) · [Cutover/recovery](../PNG/A04.png) · [Precedence](../PNG/A05.png).

Open `Atlas.html` from the package root for the offline searchable atlas. Every workflow has a detailed Markdown procedure, editable Mermaid, PNG and SVG. `Workflow_Catalog_v7_Integrated.json` is the machine-readable workflow registry; `Workflow_Connections.csv` distinguishes **handoffs**, **controls** and **runtime prerequisites**. A business handoff is not necessarily a synchronous API call, and the operational dependency graph is not a single execution DAG.

## 1. Scope, precedence and preservation

The complete reference contains 36 infrastructure/recovery workflows (I), 12 shared integration/control workflows (X), 12 voice workflows (V), 14 email workflows (E), 72 content workflows (C), 36 marketing workflows (M), and eight legacy-continuity workflows (L). The 72 content names/procedures and 36 marketing identities are retained from the source catalogs. New IDs for infrastructure, shared controls, voice, email and legacy lanes are consolidation design decompositions, not claims that those exact IDs existed in the source.

Precedence is: approved site-specific security and owner decisions → this integrated V7 clarification → retained V7 selections and safeguards → earlier V4/V5/V6 content where not superseded → historical evidence. A proposed target cannot erase an inconvenient observation. “Selected” never means “live”; an observed running container never means “approved to rebuild”; a disabled workload is not a missing service to auto-start.

The archive's 156 service-disposition records and 104 recovery records are preserved with all original columns in the migration crosswalks. Every row has a target treatment, workflow references, and an unresolved activation/owner status. Historical DNS/routes receive a separate review register. Old scripts and commands are source evidence, not a new executable deployment runbook.

## 2. Reference deployment and trust zones

Use an OpenWrt edge/router and a supported Proxmox VE host platform for virtualization. Use Debian application guests and Podman/Quadlet/systemd where supported. The legacy Train Ubuntu/Docker/Podman/libvirt deployment is a migration source; it is not silently relabeled as the V7 target. Do not install an arbitrary Debian release beneath Proxmox or replace a working router in place without a tested rollback path.

| Zone | Intended placement | Access and persistence rule |
|---|---|---|
| Edge and network | OpenWrt, firewall4/nftables, dnsmasq/odhcpd, LuCI/uHTTPd/Dropbear | Authorized management path only; known-good router export and physical recovery |
| Management | Proxmox, SSH, Forgejo/Ansible administration, recovery tools | Private LAN/VPN; break-glass outside SSO/DNS dependency loops |
| Application | Caddy, WordPress, Mautic, Matomo, Postiz, Activepieces, OpenProject, ResourceSpace | Only explicitly intended public ingress; per-app identities and hostnames |
| Data | PostgreSQL, MariaDB, Valkey, SeaweedFS | No public exposure; per-app credentials, databases/schemas and backup contracts |
| AI and bounded jobs | llama.cpp/OmniRoute, ComfyUI, FFmpeg/Pandoc/Vale/Lighthouse, batch speech | Untrusted inputs isolated; CPU/GPU/time/disk budgets; no automatic provider fallback |
| Real-time voice | Asterisk preferably in a dedicated Debian VM; controller/Pipecat nearby | Explicit carrier SIP/RTP/NAT rules; ARI and media controls private |
| Observability | OTel Collector, Prometheus/exporters, Loki, Grafana, MLflow | Redacted labels; durable alert evidence; external notification path where approved |
| Recovery | Offline keys, off-host backup target, isolated restore network | Independent failure domain where available; never overwrite the last known-good generation |
| Legacy | Isolated guests/services for approved non-core capabilities | No marketing credentials inherited; retain held/stopped/retired decisions |

These are isolation responsibilities, not a requirement for nine physical servers. Consolidate guests where appropriate while retaining least privilege, storage ownership and separate scheduling. A single host/UPS/ISP is still a single failure domain. “Enterprise-tier” here means disciplined ownership, change, security, evidence and recovery—not an unsupported claim of high availability.

All example addresses/domains are unset in `site.example.json`; historical IPs in source records must be revalidated, not copied into a live target. Define actual LAN/management/application/data/guest zones, VLAN support, IPv4 and IPv6 rules, DNS ownership, DHCP reservations, certificate names and approved exposure. Keep local dnsmasq separate from the external authoritative public DNS provider. Inventory hosted Tailscale and local Headscale as separate control planes; no federation or equivalent ACL policy is assumed.

## 3. Runtime dependency inventory

Caddy is an ingress/TLS component, not an application worker, PHP interpreter, queue or universal SSO gateway. Keycloak only protects applications and protocols for which an integration has been implemented and tested. Native authentication and a documented break-glass path remain where needed.

| Application/domain | Persistent/runtime requirements | Required proof before enablement |
|---|---|---|
| Activepieces | App and workers, PostgreSQL, supported Redis-compatible queue, application encryption keys | Webhook signatures, credential recovery, queue replay semantics and exact-version Valkey compatibility |
| WordPress | Supported PHP/web runtime, MariaDB/MySQL, plugins and uploads | REST scopes, staging, ownership, plugin compatibility, content restore |
| Mautic | Supported PHP/application workers, MariaDB/native queue, mail transport and dispatch integration | Per-recipient final guard covers immediate/manual/queued/restarted sending paths |
| Matomo | Supported PHP runtime, MariaDB/MySQL, archive jobs | Consent behavior, goal event integrity, archiving and restore; not a PostgreSQL application conversion |
| Postiz | App/workers, required native Temporal, SQL stores/visibility, compatible cache and channel tokens | Exact release topology, token scopes, scheduling, unknown-result reconciliation and coherent restore |
| OpenProject | Supported release-specific application services and database | API mapping, exact revision approvals, permissions and restore |
| ResourceSpace | PHP and compatible MySQL/MariaDB; original assets; image/media/metadata tools | ImageMagick, FFmpeg, Ghostscript, ExifTool, Inkscape and other required utilities pinned and exercised |
| Keycloak / Vaultwarden / Forgejo | Product-supported persistence, keys, attachments/repos and native configuration | Recovered identities, encrypted state and access paths; no assumed universal database substitution |
| AI / media | Pinned models, prompts, node graphs, libraries and bounded workers | Source/model rights, tool permissions, resource budgets, offline/batch versus voice latency |
| Voice | Asterisk, approved carrier, controller, Pipecat/bridge, STT/TTS/VAD and database | Release-matched media transport, two-way audio, transfer, interruptions and fail-closed dialing |
| SeaweedFS | Chosen master/volume/filer/S3 topology and associated metadata | Native app compatibility; no assumption that every app can use arbitrary S3 storage |
| Observability | Collector/exporters, metrics/log stores, dashboard/rules/config | Freshness, retention, alert dedupe, credential expiry, delivery and recovery |

Do not trim a vendor release's required worker/cache/queue simply because the high-level stack lists one application name. Conversely, do not install every conditional technology to complete a diagram. Preserve PostgreSQL as workflow/analytics authority and MariaDB where native applications require it. pgvector stores/searches embeddings; it does not itself create embeddings. ResourceSpace owns approved assets; SeaweedFS can hold appropriate working artifacts but cannot replace asset rights/approval metadata.

## 4. Ownership and end-to-end business execution

OpenProject owns briefs, assigned human work, editorial decisions, launch authorization and budget approvals. Mautic owns marketing contact identity, email preferences, segments, scoring and campaign history. The telephone controller's PostgreSQL ledger owns call-specific authorization/suppression. SMS and tracking permissions are separate contexts. WordPress, Postiz and Mautic own their native publications/journeys; their supported APIs—not direct writes into private tables—are the normal integration boundary.

The common path is verified event → authenticated intake (X01) → deduplicated durable receipt (X02) → source-owner reads → approved brief (X03) → bounded generation/transform (X05) → QA and rights checks → final channel eligibility (X04) → native action → reconcile (X06) → source-aware measurement (X10) → human-reviewed improvement. Unknown outcomes enter HOLD/reconciliation, not an automatic retry storm. X07 provides audited repair/replay, X08 withdrawal/deletion, X09 incidents, X11 release control, and X12 diagram/build governance.

**Research to website:** M11/C01–C08 discover and plan; C09–C16 prepare website/SEO content; Vale, Playwright and Lighthouse validate the intended staged revision; OpenProject authorizes; M04/M17 publish via WordPress; Matomo goals and SerpBear ranks feed M05/M21/M24 and C72. A performance recommendation creates a new brief/revision rather than editing a live page without review.

**Content to social:** C17–C24 and media derivatives use approved ResourceSpace assets. Postiz owns scheduling and publication, with its native Temporal runtime. Activepieces records destination IDs and checks unknown outcomes before retrying. Social metrics and messaging capabilities depend on the actual platform/API permissions; unsupported data is unavailable, not zero.

**Lead to nurture and sales:** WordPress/Mautic forms enter M01/M19; Mautic records permission and deduplicates identities; M25 segments; M06/M02/M13 nurture under the V5 email guard. M03 assigns a human sales task. Phone or SMS is only activated after an independent channel authorization. An email opt-in is not permission to call.

**Paid/commerce/event channels:** M07/M08/M34 require a real order authority and reconciled refunds; M10/M35 require authorized external ad accounts and explicit budget permissions; M31 requires an approved event service; M32 requires separate SMS permission and STOP processing. Conditional extensions do not become mandatory solely because they are listed. Referenced or optional tools in a workflow do not require installation when its baseline path already meets the need.

**Reporting:** Matomo owns website goals, Mautic contact/email outcomes, SerpBear keyword ranks, Postiz/providers available social/ad results. PostgreSQL normalizes snapshots with source/time/coverage; Grafana presents them. Do not relabel clicks as leads, impressions as visits, or attributed revenue as verified incremental revenue. Matomo premium attribution/experiment capabilities are not assumed. MLflow evaluates model/prompt performance, not business workflow state.

## 5. Email control boundary

E01–E10 preserve the earlier email lifecycle; E11–E14 expose final dispatch, quota reservation, replies and authentication-report ingestion. Use the approved managed SMTP relay and existing reply/report mailbox by default. Mailpit is isolated staging only.

The guard must run at the actual per-recipient transport boundary, including manual, queued, immediate and restarted-worker paths. It re-reads authoritative eligibility and sender policy, reserves quota atomically, validates the exact approved revision, then submits through the sole authorized transport. A normal Activepieces precheck or systemd rate limit is not this guard. If the deployed Mautic integration cannot guarantee the boundary, marketing email remains disabled.

Record an action key before sending. Distinguish rejected-before-acceptance, accepted, delivered, deferred, permanent failure and acceptance-unknown. Accepted-by-SMTP is not delivered-to-inbox. An ambiguous timeout retains a reserved/unknown attempt and blocks blind duplicate sending; reconcile provider evidence. Signed callbacks update delivery state and suppression promptly. Restores begin HOLD and refresh suppression before replay. Transactional mail requires its separately classified policy, not a blanket marketing bypass.

Warm-up progresses PRECHECK → CANARY → RAMPING → PRODUCTION only from genuine eligible demand, transport/authentication and observed reputation evidence. HOLD/INVESTIGATION/RECOVERY paths require authorization. No fake opens, replies, reciprocal sending or calendar-only volume escalation. `parsedmarc` output/adapter behavior must match the exact pinned release; the currently documented PostgreSQL integration is optional and needs validation with the selected runtime.

## 6. Voice control boundary

V01–V12 retain Asterisk/PJSIP/ARI, a dedicated Python call controller, Pipecat, the pinned WebSocket bridge, Faster-Whisper, Kokoro ONNX and Silero VAD. Activepieces creates business requests; it does not control the real-time audio loop. Carrier connectivity and APIs are external dependencies.

The controller checks separately recorded telephone authorization, suppression, recipient jurisdiction/timezone, allowed calling window, approved campaign/script and concurrency/cost limits at origination. No LLM can override those checks. The conversation loop permits only whitelisted tools with scoped credentials, validated arguments and action-specific approval; untrusted retrieved text cannot grant permissions. Recording starts only under the applicable reviewed policy. Opt-out cancels future eligible work immediately and is reconciled to the contact view.

Unknown origination, transfer or disconnect outcomes are reconciled against Asterisk/carrier state before retry. Human handoff is an owned destination with timeout/fallback, not an unverified transfer API assumption. Store allowed artifacts under role/retention policy. Measure two-way audio, first response, interruption behavior, failure handling and concurrent load. Batch graphics/media jobs must not exhaust voice GPU/CPU capacity.

## 7. Security, privacy and operational boundaries

Use per-app/per-client service credentials, explicit allowed destinations and least privilege. Store secrets in encrypted SOPS/age configuration or approved runtime secret injection; store human-held recovery credentials in Vaultwarden/KeePassXC as appropriate. Do not put private tokens in prompts, logs, diagrams, URLs or warehouse snapshots. Keycloak does not automatically isolate clients within applications. Test UI, API, dashboard, asset and credential boundaries independently; use separate app deployments where needed for real tenant isolation.

Every publication approval binds the exact content revision, asset hashes, destination and intended schedule. Material changes invalidate approval. Final eligibility fails closed when consent/approval/policy cannot be read. Backoff is bounded and jittered, with maximum attempts, expiry and a visible dead-letter owner. Restore/replay must re-read revocations, suppression and current external state before any send, call, publish, reward or budget mutation.

Collect only required lawful data. Define retention by class and client; deletion propagates through current systems, exports and applicable caches, while controlled backup expiry and restoration re-deletion prevent resurrection. Claims, customer evidence, media/model rights, calling/SMS rules and tracking behavior require business/jurisdiction-specific review. The package is not legal approval.

## 8. Reliability, backup and recovery

I19/I20/I21/I33 establish actual telemetry producers, host snapshots, health checks and one scheduler owner. Configuration fields named cooldown or dedupe are not proof of implementation. Alert actions need durable keys, suppression, severity, freshness and an accountable route. Monitor dependencies, queue depth/age, error rate, missed schedules, provider permission expiry, backup age and restore evidence—not just container uptime.

Use pgBackRest for PostgreSQL, mariadb-backup for MariaDB, restic for appropriate files/off-host copies, and Proxmox native VM backups. Include secrets needed to decrypt application state, Temporal persistence/visibility as required, original assets plus metadata, publication receipts and controller ledgers. A filesystem copy or VM snapshot alone may not be an application-consistent database backup. Verify checksums and independent restore; an off-host destination should not be the same physical failure domain when recoverability requires independence.

Set owner-approved RPO/RTO, retention and capacity targets before deployment; no measured values are invented here. I24 tests restoration in isolation and HOLD. I25 transfers one writer/controller/scheduler at a time; I26 reconciles target-side writes before rollback. I27 coordinates UPS shutdown and dependency-aware restart. Stopped/held legacy services remain stopped until separately authorized.

## 9. Implementation stages and go/no-go evidence

| Stage | Workflows | Exit evidence |
|---|---|---|
| Inventory and custody | I01–I04, I12, I35 | Owner scope, legacy row reconciliation, offline recovery, exact source/image/secret identities |
| Network and host | I05–I11, I14, I36 | Isolated router and guest validation, IPv4/IPv6/exposure tests, rollback and correct time |
| Data and operations | I15–I24, I27–I28, I33–I34 | Native database/asset restore, monitored dependencies, resource and backup budgets |
| Shared contract | X01–X11 | Authenticated ingress, durable keys, approvals, final guards, reconciliation and replay tests |
| Controlled content | C01–C72, M04/M11/M12/M17 | Exact-revision staging/publish proof, asset rights and native destination receipts |
| Email and permitted voice | E01–E14, V01–V12 | Staging/canary, provider and permission evidence, no manual bypass, uncertainty handling |
| Remaining marketing | M01–M36 | Owner-specific channel gates, real conversion feeds, client isolation and report quality |
| Legacy continuity | L01–L08, I29–I32 | Owner decision and checkpoint for each kept/held/retired/non-core item |
| Cutover and drills | I25–I26, X09/X11/X12 | One writer, reconciled external effects, rollback checkpoint, validated docs and recovery drill |

`Implementation/Acceptance_Matrix.csv` records required live tests as NOT_RUN or OPEN_SOURCE_BLOCKER. Documentation checks are reported separately under Validation. A diagram build passing cannot promote any production gate.

## 10. What is and is not implemented by this delivery

Implemented here: the consolidated design, complete source preservation/crosswalks, connected workflow registry, detailed run procedures, Mermaid source generation, rendered diagrams, offline atlas, build scripts and documentation validation.

Still site-specific engineering: inventory and hardware choices; image/version pins; application deployments; actual schemas/migrations; Activepieces/native application exports; API/transport adapters; the Mautic guard and voice controller implementation; credentials/provider permissions; human role assignment; backup targets; measured limits; legal/compliance review; and live acceptance evidence. These are explicit design contracts, not disguised production-ready code. See `Implementation/Integration_Contracts.md` and `site.example.json`.

No new mandatory always-on platform is selected by this consolidation. Mermaid rendering adds a documentation build dependency, and application-specific runtime dependencies are made visible rather than treated as new optional platforms. All prior V7 conditional choices remain conditional.
