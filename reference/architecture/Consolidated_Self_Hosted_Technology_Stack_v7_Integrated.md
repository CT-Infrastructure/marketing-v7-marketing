> Imported V7 reference; links to the original atlas or historical Sources/ paths refer to the separately retained source package, not this repository. Do not execute historical commands.

# Consolidated Self-Hosted Technology Stack

**Version 7 — Consolidated Full Implementation, revision 1**  
**Updated:** October 25, 2026  
**Current reference:** This consolidated V7 edition supersedes `train-router-rebuild-docs-2026-10-24.zip` as the architecture/rebuild/workflow planning reference and extends the earlier V7 online-marketing document. It preserves the original ZIP as historical evidence and carries forward all V4/V5/V6/V7 safeguards.

## Consolidation decision

The software baseline remains V7, not a silent V8. All 72 content patterns and 36 marketing patterns are integrated with infrastructure, access, data, deployment, voice, email, shared controls, legacy continuity and recovery in one registry: **190 workflows, 215 Mermaid diagrams with PNG/SVG renders, and typed cross-workflow relationships**.

**Read first:** [Unified implementation](Unified_Implementation_Guide.md), [diagram guide](Diagram_Guide.md), [all workflow procedures](../All_Workflows_v7_Integrated.md), [legacy reconciliation](../Migration/README.md), [rebuild runbook](../Migration/Unified_Rebuild_Runbook.md), [software/function index](../Implementation/Component_Function_Matrix.md), and [integration contracts](../Implementation/Integration_Contracts.md).

**Consolidation additions:** Mermaid-based documentation rendering is a bounded build utility, not an always-on platform. Existing applications' actual runtime dependencies (including PHP, queue workers, Temporal, media/metadata utilities, native databases and encryption keys) are explicitly accounted for. No conditional platform is installed or activated by this decision. Lighthouse remains the one selected V7 *marketing* CLI addition; the documentation renderer is a separate consolidation tool.

**Legacy reconciliation:** Preserve all 156 disposition and 104 recovery rows, with original evidence and explicit V7 treatment. Keep held/stopped/retired intent; do not resurrect old model-serving deployments merely because V7 selects a new local AI function. Non-core workloads are isolated/conditional/owner-decided, not silently deleted or made mandatory marketing dependencies.

**Status:** Reference design and documentation artifacts implemented; live infrastructure, application integrations, custom dispatch/controller code, site-specific configuration, provider authorization and production tests are not established by this package. Documentation validation is distinct from runtime acceptance.

**Interpretation clarifications:** Native application databases/queues remain supported; PostgreSQL is not a universal replacement. ResourceSpace needs its actual image/media/metadata utilities. Activepieces needs its release-specific workers/queue and recoverable encryption key. Mautic's custom guard must cover every recipient/send path at the actual transport boundary. Mermaid topology is not proof of service connectivity. All exact versions and runtime/edition compatibility remain deployment gates.

---

## Retained V7 baseline — full text

The baseline below is retained in full for decision continuity. This consolidation's precedence/status clarifications govern interpretation. The unmodified source is preserved under `Sources/V7/`.

### Original V7 standardization text

**Version 7 — Standardized Baseline: Online Marketing Integration**  
**Updated:** October 25, 2026  
**Supersedes:** Version 6 as the reference for future stack evaluations.  
**Retains:** All Version 4 voice-agent, Version 5 email deliverability/warming, and Version 6 content-production selections, safeguards, lifecycle rules, and acceptance tests unless explicitly clarified here.

## Executive decision

**Primary objective:** Preserve the existing infrastructure and minimize additional independently operated services, dependencies, maintenance, and resource consumption without sacrificing required functionality, security, compatibility, reliability, recoverability, or business compliance.

**Version 7 integrates 36 common online marketing workflows**, including SEO, content, social publishing, lead capture, email nurture, sales handoff, ecommerce (conditional), paid advertising (external network), retention, agency operations, reputation, experiments, referrals, SMS, and marketing analytics.

**One additional selected open-source command-line tool:**

- **Lighthouse CLI** — Technical website quality auditing for performance, accessibility, technical SEO, and best practices. Apache-2.0. Runs in a bounded existing job environment; **not** a new persistent application. It requires a tested Node.js and Chrome/Chromium runtime. Its audits supplement rather than replace SerpBear, Matomo, Vale, or Playwright.

**No new mandatory independent marketing application platform.** The selected additions across V6 and V7 are FFmpeg, Pandoc, Vale, and Lighthouse as invoked utilities. Postiz's pre-existing required Temporal infrastructure, existing Mautic database, and other baseline runtime dependencies remain real services and must be accounted for separately.

**New Version 7 conditional candidates (not installed by this decision):** WooCommerce (ecommerce); GrowthBook open-source core (website A/B experiments); changedetection.io (specialized public-page change monitoring); Chatwoot (shared conversational inbox); Jitsi Meet (webinar/meeting delivery); pretix (ticketed event registrations); Site Reviews (WordPress structured reviews); CookieConsent by orestbida (conditional frontend cookie/consent management). Their alternatives and limitations appear in Section 2.

**External platforms only when the corresponding business channel is activated:** Advertising accounts/networks (Google Ads, Meta etc.), social networks and approved APIs, public business listings and their APIs, SMS service/carrier, payment processors, third-party review platforms and eligible event providers. The V4 SIP trunk, V5 managed SMTP relay, public DNS, and business mailbox dependencies remain unchanged.

**Status:** These are architectural selections. Installation, integrations, security review, API authorization, licensing, benchmarks, and acceptance tests remain open until proven in deployed environments.

## 1. Core Technology Stack

| Category | Selected technologies / established role |
|---|---|
| Router & Firewall | OpenWrt, firewall4, nftables |
| DHCP & DNS | dnsmasq, odhcpd |
| Router Administration | LuCI, uHTTPd, Dropbear |
| Private Networking / VPN | Tailscale + Headscale |
| Operating Systems | Debian Stable |
| Virtualization | Proxmox VE (QEMU/KVM) |
| Containers | Podman + Quadlet |
| System & Network Management | systemd, systemd-networkd, OpenSSH, chrony |
| Reverse Proxy & HTTPS | Caddy |
| Identity & SSO | Keycloak |
| Password Management | Vaultwarden, KeePassXC (offline recovery) |
| Secrets Management | SOPS + age |
| Infrastructure Automation | Ansible |
| Relational Databases | PostgreSQL; MariaDB where MySQL compatibility is required |
| Vector Database Extension | pgvector |
| Caching & Key-Value Storage | Valkey; substitute for software-mandated Redis only after compatibility testing |
| Object Storage | SeaweedFS |
| Cross-Application Workflow Automation | Activepieces |
| Local AI Inference | llama.cpp |
| AI Model Routing | Local OmniRoute build |
| AI Image Generation | ComfyUI |
| AI Experimentation & Evaluation | MLflow |
| Telemetry Collection | OpenTelemetry Collector Contrib |
| Metrics & Monitoring | Prometheus, node_exporter, blackbox_exporter |
| Dashboards & Alerting | Grafana |
| Log Management | Loki |
| Backup & Recovery | restic, pgBackRest, mariadb-backup, Proxmox native backups |
| Hardware Monitoring | smartmontools, Network UPS Tools (NUT) |
| Vulnerability & Patch Management | Trivy, unattended-upgrades |
| Version Control & Collaboration | Git, Forgejo |
| Testing & Validation | Playwright |
| Research & Metasearch | SearXNG |
| SEO Rank Monitoring | SerpBear |
| Project & Editorial Management | OpenProject |
| Website & Blog Publishing | WordPress |
| Marketing Contact Management & Campaigns | Mautic |
| Digital Asset Management | ResourceSpace |
| Social Media Publishing | Postiz |
| Website Analytics & Goals | Matomo |
| Diagramming & Collaboration | Excalidraw |
| Telephone Session Control — V4 | Asterisk (PJSIP, ARI) |
| Public Telephone Network Connectivity — V4 | External SIP trunk service |
| Real-Time Voice Agent — V4 | Pipecat |
| Telephony-to-AI Audio Bridge — V4 | Asterisk `chan_websocket` + community `pipecat-asterisk`, pinned and validated |
| Speech-to-Text — V4 | Whisper via Pipecat local Faster-Whisper backend |
| Text-to-Speech — V4 | Kokoro ONNX via Pipecat |
| Voice Activity Detection — V4 | Silero VAD + Pipecat |
| Outbound Voice Call Controller — V4 | Custom Python controller + Asterisk ARI + PostgreSQL |
| Telephone Consent & Suppression — V4 | PostgreSQL call-specific ledger; synchronized to Mautic where appropriate |
| Outbound Call Scheduling — V4 | Activepieces triggers; PostgreSQL durable state; controller enforces dialing/retries |
| Voice-Agent Retrieval & Tools — V4 | llama.cpp + OmniRoute; PostgreSQL + pgvector; approved APIs |
| Call Artifacts — V4 | Asterisk/Pipecat; PostgreSQL; SeaweedFS under retention/recording policy |
| Voice Observability — V4 | OpenTelemetry, Prometheus, Grafana, Loki, MLflow |
| Public Email DNS & Sender Identity — V5 | External authoritative DNS provider; SPF, DKIM, DMARC, MX, return-path records; Ansible/API when supported |
| Production Outbound Marketing Mail — V5 | External managed SMTP relay (default) integrated with Mautic |
| Inbound Email & Replies — V5 | Existing business mailbox/IMAP/API provider, external when needed |
| Sender DNS/Auth Checks — V5 | checkdmarc |
| DMARC and SMTP TLS Reporting — V5 | parsedmarc + PostgreSQL |
| Email Contact & Consent Authority — V5 | Mautic |
| Email Campaign Creation & Scheduling — V5 | Mautic + existing content production stack |
| Email Queue / Dispatch — V5 | Supported Mautic native queue/Doctrine transport, bounded consumers, systemd |
| Email Warm-up Policy & Volumes — V5 | Activepieces decisions + PostgreSQL policy/reservations + custom dispatch guard |
| Provider Delivery/Bounce Feedback — V5 | Provider/Mautic callback + Activepieces + PostgreSQL + Mautic |
| Email Unsubscribe & Suppression — V5 | Mautic + provider suppression + pre-dispatch eligibility checks |
| Email Sender Reputation — V5 | External provider feedback/Postmaster; parsedmarc; Activepieces; PostgreSQL |
| Email Dashboards & Alerts — V5 | Prometheus, Grafana, OpenTelemetry, Loki, PostgreSQL |
| Email Testing — V5 | Mailpit (staging only), Playwright, controlled real-mailbox tests |
| Email Incident Response — V5 | Activepieces, OpenProject, PostgreSQL, Mautic, Grafana |
| Email Deployment Management — V5 | Ansible, Forgejo, SOPS + age, Podman + Quadlet, systemd |
| Postiz Internal Workflows — V6 | Temporal for Postiz v2.12.0+; supported isolated persistence/visibility on PostgreSQL where validated |
| Content Research & Discovery — V6 | SearXNG, SerpBear, Matomo, approved WordPress and Mautic data |
| Content Planning & Strategy — V6 | OpenProject, llama.cpp, Activepieces, PostgreSQL |
| Audience & Campaign Intelligence — V6 | Mautic, Matomo, SerpBear, PostgreSQL, llama.cpp |
| Content Briefs, RAG & Source Retrieval — V6 | llama.cpp, OmniRoute, SearXNG, PostgreSQL + pgvector, OpenProject |
| AI Writing, Summaries, Classification & Localization — V6 | llama.cpp + OmniRoute, licensed checkpoints as needed |
| AI Visuals & Graphics — V6 | ComfyUI, Excalidraw, deterministic charts where accuracy matters |
| Offline Transcription & Narration — V6 | Batch Faster-Whisper and Kokoro ONNX wrappers separate from live calls |
| Audio & Video Processing — V6 | FFmpeg and ffprobe |
| Document & eBook Conversion — V6 | Pandoc |
| Editorial Style / Brand-Language Rules — V6 | Vale + versioned Forgejo rules |
| Content Workflow Orchestration — V6 | Activepieces + bounded Python jobs + systemd + PostgreSQL state |
| Content Lifecycle & Publishing Ledger — V6 | PostgreSQL, linked to OpenProject approvals and destinations |
| Content Asset Library & Working Artifacts — V6 | ResourceSpace approved assets; SeaweedFS suitable intermediate/bulk storage |
| Source, Prompts & Templates — V6 | Git + Forgejo |
| Website Publishing — V6 | WordPress + Activepieces |
| Social Publishing — V6 | Postiz + Activepieces; Postiz itself uses Temporal |
| Email Content Publishing — V6 | Mautic governed by V5 sender controls |
| Content Repurposing — V6 | llama.cpp, OmniRoute, ComfyUI, FFmpeg, Pandoc, Activepieces |
| Content AI Evaluation — V6 | MLflow and reviewed evaluation datasets |
| Content QA — V6 | Vale, Playwright, FFmpeg/ffprobe, custom validators |
| Content Performance & Operations — V6 | Matomo, SerpBear, Mautic, Postiz metrics, PostgreSQL, Grafana, MLflow |
| Technical Website Quality Auditing — V7 — NEW | **Lighthouse CLI**: scheduled/on-demand performance, accessibility, basic SEO and best-practice audits |
| Marketing Strategy & Funnel Coordination — V7 | OpenProject + Activepieces + PostgreSQL |
| Acquisition / Lead Capture — V7 | WordPress, Mautic forms, Matomo, Activepieces |
| Marketing Contacts, Lifecycle & Lead Scoring — V7 | Mautic; approved sales handoffs to OpenProject |
| Marketing Email Journeys — V7 | Mautic + V5 managed SMTP relay/dispatch/consent controls |
| Marketing Social Distribution — V7 | Postiz, ResourceSpace, Activepieces |
| SEO Discovery, Rank & Audit — V7 | SearXNG + SerpBear + Lighthouse + Playwright |
| Campaign IDs, UTMs & Analytics — V7 | Matomo (website authority) + PostgreSQL marketing operational records |
| Cross-Channel Reporting — V7 | PostgreSQL-normalized source snapshots + Grafana; Metabase conditional for advanced BI |
| Marketing Experiments — V7 | Mautic native email A/B; controlled WordPress variants + Matomo goals; GrowthBook conditional |
| Lead Magnets & Marketing Downloads — V7 | Pandoc; Typst when needed; ResourceSpace; WordPress; Mautic forms |
| Referral & Simple Loyalty State — V7 | WordPress/Mautic + Activepieces + PostgreSQL auditable ledgers, only for limited programs |
| Agency Client Operations — V7 | OpenProject, Mautic, ResourceSpace with verified account/project isolation |
| Marketing Orchestration & API Integrations — V7 | Activepieces; native destination APIs and bounded Python adapters when needed |
| Marketing Monitoring & Recovery — V7 | OpenTelemetry + Prometheus + Grafana + Loki; existing backups and incident management |

### Core clarifications carried forward

- Selected components are not deemed installed or production validated.
- Debian hosts; Proxmox VE virtualization; Podman/Quadlet/systemd for production application deployment, preferably rootless where supported.
- Mautic uses its supported application database (typically MariaDB); PostgreSQL is separate operational/analytics storage and should not be forced into Mautic's internal database role.
- Marketing contact identity, consent, segmentation, unsubscribe and campaign history belong to Mautic; do not create a second marketing CRM.
- WordPress owns websites/pages, Postiz owns scheduled social posts, Mautic owns email journeys, OpenProject owns approvals, ResourceSpace owns approved creative assets, Matomo owns website analytics, SerpBear owns rank history, and PostgreSQL owns separate workflow/job/audit ledgers.
- Activepieces is primary cross-application orchestration; native app scheduling remains native. Postiz's required Temporal is a real internal dependency **not** a reason to add Temporal as a second marketing orchestrator.
- Managed SMTP and replies remain external by default; Postal/mailbox servers remain conditional alternatives only.
- Grafana is the default operational and modest business-metric view; Metabase remains conditional for dedicated business intelligence (not automatically installed).
- Lighthouse is not equivalent to a full site crawler, backlink intelligence tool, search ranking provider or replacement for accessibility testing by humans.

## 2. Conditional Technologies

Install only when a documented requirement cannot reliably be satisfied by the existing stack. An optional feature is **not** part of the mandatory V7 deployment.

### 2.1 Previously established conditional technologies — Versions 1–6 retained

| Technology | When justified | Default / reason not to add |
|---|---|---|
| RabbitMQ | Advanced brokering/throughput not met by native queues and PostgreSQL state | Use existing application queues and bounded workers |
| General-purpose Temporal usage | Independent long-running, durable workflows requiring it | Activepieces remains business orchestrator; Postiz's internal Temporal is already required |
| OpenBao | Dynamic secrets / centralized machine API | SOPS + age and Keycloak where sufficient |
| ClickHouse | High-volume event analytics beyond relational reporting | PostgreSQL first |
| Metabase | Business-facing self-service BI beyond Grafana | Grafana for operations and simpler metrics |
| Healthchecks | Independent cron/job heartbeat monitoring | Existing Prometheus/blackbox_exporter |
| ntfy | Dedicated user push notifications | Existing Grafana/alerting workflow |
| Samba | SMB network file sharing | Existing object/asset storage for marketing workloads |
| mcp-searxng | MCP search interface needed | Call existing SearXNG API directly otherwise |
| softflowd + netflow2ng + ntopng | Network traffic analytics requirements | Baseline monitoring otherwise |
| rsyslog / Vector | Log pipelines that OTel/Loki do not satisfy | Existing selected pipeline |
| LiveKit Server + SIP + Agents | WebRTC rooms/browser calling justify voice architecture change | Asterisk/Pipecat selected; architectural alternative, not add-on |
| FreeSWITCH | Specialized telephony/media switching | Asterisk selected |
| Speaches | Independently scaled/shared STT/TTS APIs | Embedded Pipecat audio services |
| Piper | Voice/language/performance gap in Kokoro | Reuse Kokoro first; check licenses |
| SIPp | SIP/load protocol testing | Testing only, not a persistent service |
| Easy!Appointments | Self-service sales booking needed | Mautic lead intake + OpenProject human follow-up |
| Alternative speech recognition | Proven live latency/quality gap | Current Faster-Whisper integration |
| Postal | Managed SMTP inadequate, self-hosting justified | Managed SMTP default |
| mailcow or Mailu | Self-hosting business IMAP/reply mailboxes necessary | Existing external mailbox default; select one only |
| DNSControl | DNS configuration-as-code beyond Ansible/provider API | Ansible and Forgejo first |
| python-email-validator | Additional import/validation quality | Embed as library, not server |
| Dedicated email IP / alternate SMTP relay | Reputation/throughput or provider constraints | Existing managed transport first |
| Custom email transport adapter | Missing Mautic/provider callback behavior | Small bounded adapter only |
| Typst CLI | Professionally typeset PDF output required | Pandoc alone for conversions; Typst for layout |
| Kdenlive | Human nonlinear video editing required | FFmpeg automation first |
| ComfyUI video models/nodes | Approved video motion generation required | Existing imagery, audio, FFmpeg first |
| Embedding/reranking/specialized model checkpoints | Measured RAG, language, visual or output quality gaps | Existing llama.cpp + OmniRoute + compatible models first |
| Additional rendering libraries | Required format, layout, accessibility, codec cannot be met | FFmpeg/Pandoc/Vale/Lighthouse/Playwright first |
| Dedicated render capacity | Batch media demand exceeds limits without harming real-time voice | Resource limits and schedules first |
| Publishing API adapter | Destination cannot be safely reached by Activepieces/native APIs | Small adapter, not platform |

### 2.2 New conditional online marketing technologies — Version 7

| Technology / repository | Purpose | Existing-stack-first alternative | Deployment type | Trigger for adoption |
|---|---|---|---|---|
| **WooCommerce** — https://github.com/woocommerce/woocommerce | Shopping cart, checkout, products, orders, purchase webhooks | WordPress + existing permitted external commerce API, if already present | WordPress plugin, GPL-2.0 | Own-site ecommerce is activated |
| **GrowthBook (OSS core)** — https://github.com/growthbook/growthbook | Assignment, statistics and management for controlled web experiments | Mautic native email A/B; limited custom WordPress + Matomo experiment | Independent open-core application | More complex/frequent webpage experimentation is needed; verify edition and terms |
| **changedetection.io** — https://github.com/dgtlmoon/changedetection.io | Targeted public competitor/page change detection | SearXNG + Playwright periodic comparison + PostgreSQL/Activepieces | Additional service | Custom monitoring becomes too labor-intensive or unreliable |
| **Chatwoot** — https://github.com/chatwoot/chatwoot | Shared customer/conversation inbox across supported channels | Mautic + OpenProject human tasks + existing business mailbox | Additional open-core service | High-volume omnichannel interactions and team routing needed |
| **Jitsi Meet** — https://github.com/jitsi/jitsi-meet | Meetings and webinars | Existing legally/contractually suitable meeting provider | Additional RTC services | First-party hosted webinars or group video calls required |
| **pretix** — https://github.com/pretix/pretix | Ticket inventory, registration, payment and attendee operations | WordPress + Mautic registration for simple free events | Additional application | Paid/capacity-controlled events; review license/additional terms |
| **Site Reviews** — https://github.com/pryley/site-reviews | First-party reviews, moderation, structured display | WordPress comments / approved simple intake | WordPress plugin | Public testimonial/product-service review site required |
| **CookieConsent** — https://github.com/orestbida/cookieconsent | Browser-side tracking permission UI and script gating | Existing WordPress compliant consent handling and Matomo controls where sufficient | JavaScript library, MIT | Applicable privacy rules/trackers require granular consent controls |
| **Google Ads API client library** — https://github.com/googleads/google-ads-python | Optional typed API client for ads reporting/control | Activepieces HTTP/API integration | Python library, Apache-2.0 | API integration requires more than maintained HTTP adapter |

**Do not make these additions automatically.** A conditional app must have its own integration owner, supported version/dependencies, least-privilege identities, backup/recovery plan, threat model, observable health and explicit approval.

### 2.3 External marketing dependencies (not open-source software)

| Function | External system | Rules |
|---|---|---|
| Paid advertising / retargeting | Google Ads, Meta, other approved networks and their APIs | Authorized account, spending limits, audience eligibility, API permissions, manual budget approval |
| Social distribution / engagement APIs | Facebook, Instagram, LinkedIn, TikTok, YouTube, X, etc. | Supported Postiz/API capabilities, tokens, platform constraints; no guarantee all metrics/DMs exposed |
| SMS marketing | SMS-capable carrier/provider and jurisdictional registration | Independent opt-in, STOP handling, suppression; SIP calling service does not imply SMS availability |
| Third-party reviews | Google and other official review platforms | Official integration rules and anti-incentive/review-gating policies |
| Business listing publication | Google Business Profile and other listing APIs | Authorized access, quotas, ownership; no OSS substitute for external listing platform |
| Ecommerce payment settlement | Payment processor / bank provider | Required if charging customers; payments, refunds, chargebacks reconciled |
| Public research / rank data | Search engines and configured position-data services | Terms/rate limits/cost; SearXNG and SerpBear do not guarantee free source data |
| Email transport / replies / DNS | V5 managed SMTP, mailboxes and authoritative public DNS | Already selected baseline external dependencies |
| Telephone connectivity | V4 SIP trunk provider | Already selected baseline external dependency |

### Conditional and license principles

- All selected and conditional software should be reviewed for actual business use, AGPL/GPL obligations, network-use provisions, bundled/proprietary extensions, and model/media rights.
- Open-source source availability does not imply that every bundled enterprise feature is open-source. GrowthBook and Chatwoot may be open-core.
- A frontend cookie banner alone does not guarantee legal compliance; map every tracker to consent decisions, audit behavior and applicable jurisdictional obligations.
- Matomo's core has goals/ecommerce reporting and default attribution; **advanced multi-channel attribution is a commercial Matomo On-Premise plugin**. Prefer transparent, documented SQL models on existing PostgreSQL when multi-touch attribution is required without buying a premium module.
- Referral/commission/loyalty automation can be implemented using existing PostgreSQL and Activepieces only when the ledger, anti-fraud, payout reconciliation and accounting complexity are modest. For larger affiliate programs, evaluate a purpose-built platform separately.

## 3. Online Marketing Workflows — Version 7

**36 common workflow patterns**, not 36 additional applications. Existing software is the default in every step. `Conditional` and `External` identify actual gaps, not automatically selected additions.

### A. Services and B2B marketing

| ID | Workflow | End-to-end sequence (responsible software) | New dependency |
|---|---|---|---|
| M01 | Lead capture and contact management | WordPress landing page → Mautic form → permission and deduplication in Mautic → Activepieces routing → OpenProject task | None |
| M02 | Nurture and score leads | Mautic eligible segment → approved email sequence → V5 dispatch guard and managed SMTP → engagement feedback → Mautic score → sales handoff | No new software; V5 SMTP external |
| M03 | Sales follow-up | Mautic qualified stage → Activepieces eligibility check → OpenProject assignment → Mautic outcome; optionally V4 calling controller only with separate telephone authorization | Easy!Appointments conditional; no default addition |
| M04 | SEO content marketing | SearXNG + SerpBear + Matomo → OpenProject brief → llama.cpp/OmniRoute → ComfyUI/ResourceSpace → Vale + Playwright + Lighthouse → OpenProject approval → WordPress | Lighthouse selected CLI (V7) |
| M05 | Marketing analytics and attribution | Matomo goals + Mautic outcomes + Postiz/SerpBear available data → Activepieces → PostgreSQL normalized snapshots → Grafana | No new software; optional Metabase; multi-touch SQL custom |

### B. Ecommerce and conversion marketing

| ID | Workflow | End-to-end sequence (responsible software) | New dependency |
|---|---|---|---|
| M06 | Welcome email series | Mautic consented signup → segment → welcome series → V5 authorized SMTP → engagement/lead score | None; V5 SMTP |
| M07 | Abandoned cart/checkout | Supported commerce event → Activepieces hold/recheck purchase and consent → Mautic recovery message → stop immediately upon purchase/opt-out | **Conditional WooCommerce** or other actual checkout system |
| M08 | Post-purchase cross-sell/upsell | Validated order → Mautic lifecycle segment → approved relevant recommendations → V5 dispatch → revenue measurement | Conditional ecommerce/order data |
| M09 | Dormant-customer win-back | Mautic inactivity and eligible contact state → approved Mautic reactivation → suppression/purchase check → outcome | None for email engagement; order feed for true customer retention |
| M10 | Paid search/social and retargeting | OpenProject campaign approval → llama.cpp/ComfyUI creative → authorized ad networks → WordPress + Matomo conversions → Activepieces reporting and human-controlled budgets | **External ads accounts/APIs/ad spend**, no new OSS platform |

### C. Content, creators, and social media

| ID | Workflow | End-to-end sequence (responsible software) | New dependency |
|---|---|---|---|
| M11 | Content discovery and calendar | SearXNG → llama.cpp topic analysis → OpenProject calendar/brief → ComfyUI/ResourceSpace assets → approval → publication | None |
| M12 | Video/audio repurposing | Authorized existing footage → Faster-Whisper transcription → llama.cpp clips/scripts → FFmpeg resize/caption/encode → ResourceSpace → approval → Postiz | None; Kdenlive conditional |
| M13 | Newsletter subscriber onboarding | Mautic form/permission → segmentation → welcome emails → newsletter → V5 delivery → engagement update | None; V5 SMTP |
| M14 | Comment/DM engagement follow-up | Postiz-supported or official API event → Activepieces classify via llama.cpp → OpenProject human review where needed → approved response/lead link to Mautic | Chatwoot conditional; channel APIs external |
| M15 | Social-to-site conversion reporting | Postiz supported metrics + Matomo campaign goals + Mautic qualification → PostgreSQL normalized data → Grafana | None; missing social API metrics remain unknown |

### D. Marketing agency operations

| ID | Workflow | End-to-end sequence (responsible software) | New dependency |
|---|---|---|---|
| M16 | Client onboarding | WordPress/Mautic intake → Activepieces → OpenProject client project → ResourceSpace asset acquisition → controlled approvals | None; enforce client isolation |
| M17 | Multi-channel publishing | OpenProject brief → llama.cpp/ComfyUI assets → Vale/QA → exact revision approval → WordPress + Postiz + Mautic → reconciliation | None; Postiz's required Temporal remains |
| M18 | Client-facing campaign dashboards | Matomo + SerpBear + Mautic + Postiz permitted metrics → PostgreSQL → Grafana | Metabase conditional for self-service BI |
| M19 | Lead generation and routing | WordPress form → Mautic contact and consent → Activepieces dedupe/qualification → responsible person/client → OpenProject work item | None; separate client data carefully |
| M20 | Automated client reports | Activepieces scheduled sources → PostgreSQL → Grafana data / controlled templates → Pandoc → OpenProject approval → authorized distribution | None; Typst conditional for PDFs |

### E. Cross-industry marketing workflows

| ID | Workflow | End-to-end sequence (responsible software) | New dependency |
|---|---|---|---|
| M21 | Keyword tracking and alerts | SerpBear → Activepieces comparisons → OpenProject optimization task → WordPress edit proposal | None |
| M22 | Competitor change tracking | SearXNG discoveries → Playwright permitted snapshots → PostgreSQL differences → llama.cpp digest → OpenProject decision | changedetection.io conditional |
| M23 | Email/site A/B tests | Mautic native email variants, or WordPress controlled variant allocation → Matomo goals → analysis → OpenProject promotion approval | GrowthBook conditional for mature website experiments |
| M24 | Landing page optimization | Matomo goals and funnel indicators → Lighthouse/Playwright audit → OpenProject hypothesis → WordPress revised variant → measured comparison | None for lightweight experiments |
| M25 | Consent-aware audience segmentation | Mautic permission and lifecycle signals → dynamic segment/score → Mautic campaigns → eligibility re-check | None |
| M26 | Referral marketing | WordPress referral link/form → Activepieces → PostgreSQL attribution/eligibility ledger → Mautic notification/reward | None for simple program; processor conditional |
| M27 | Affiliate management | Partner intake/approval → tracking links → purchase verification → PostgreSQL commission accrual → human reconciliation/payout approval | Specialized affiliate platform conditional at scale; payment provider external |
| M28 | Influencer discovery and outreach | SearXNG public research → llama.cpp summary → OpenProject shortlist/approval → authorized personalized outreach → referral/UTM measurement | Platform/API access external; no default software |
| M29 | First-party review requests | Eligible customer event → Mautic neutral request → WordPress review destination → moderation → reporting | Site Reviews plugin conditional; third-party sites external |
| M30 | Reputation and brand monitoring | Permitted SearXNG/API research → Activepieces/Playwright monitoring → llama.cpp classification → OpenProject resolution | changedetection.io or Chatwoot conditional |
| M31 | Webinar registration and follow-up | WordPress + Mautic form → reminders via V5 → approved event delivery → attendance event → Mautic nurturing | Existing meeting platform external or Jitsi conditional; pretix for ticketing |
| M32 | Permission-based SMS marketing | Mautic independent SMS permission → Activepieces dispatch checks → external SMS-capable transport → STOP/bounce feedback → immediate Mautic suppression | External SMS carrier/provider, no OSS platform required by default |
| M33 | Local SEO and listings | SearXNG + SerpBear + Lighthouse → WordPress local pages → authorized external listing update → Matomo and rank tracking | External business profile/listing APIs |
| M34 | Loyalty and reward programs | Valid purchase event → PostgreSQL atomic points ledger → Activepieces → eligible reward → Mautic notification → redemption audit | Order system and processor conditional; no default rewards SaaS |
| M35 | Marketing budget optimization | Ad network spend + Matomo conversions + verified sales → PostgreSQL KPI snapshots → Grafana → OpenProject budget approval → authorized API change | External ad account and spend required |
| M36 | Marketing synchronization | Supported WordPress/Mautic/Postiz/SerpBear/Matomo events → Activepieces normalization/identity mapping → PostgreSQL operational records → updates only to authoritative owners | None |

### 3.1 Workflow execution reference

`Event or schedule → source verification → consent/authorization → collect data → deduplicate → AI or rule processing → QA → human approval when required → native destination action → reconcile external result → record durable state → monitor → evaluate KPI → create improvement task.`

Different families skip irrelevant stages but may **never bypass** final send/dial/publish controls.

### 3.2 Shared funnel and channel ownership

`Research (SearXNG/SerpBear/Matomo) → strategy (OpenProject) → content (llama.cpp/ComfyUI) → QA/approval (Vale/Playwright/Lighthouse/OpenProject) → distribution (WordPress/Postiz/Mautic) → site engagement (Matomo) → lead/contact (Mautic) → nurturing (Mautic + V5 SMTP) → sale/qualified handoff (Mautic + OpenProject / conditional checkout) → retention (Mautic) → reporting (PostgreSQL + Grafana) → next approved optimization.`

- WordPress controls web publication, including drafts, pending posts and live versions.
- Postiz controls social scheduling and delivery; Temporal is a Postiz-specific internal dependency for modern releases.
- Mautic controls marketing contact permissions, segments, scoring, campaign journeys, and the native email queue.
- OpenProject controls human editorial, sales follow-up, budget and campaign approvals.
- Activepieces coordinates cross-platform events, not independent unauthorized sends, edits or calls.
- ResourceSpace holds rights-checked approved media; SeaweedFS holds suitable working outputs.
- Matomo measures website sessions/goals and basic campaign referrers, **not** all offline purchases or every social platform's impressions by itself.
- Grafana remains the baseline for operations and reporting panels; conditional Metabase is preferred only if business BI requirements warrant it.

### 3.3 Marketing data model (logical records on existing PostgreSQL)

| Logical record | Purpose | Authority / duplication rule |
|---|---|---|
| `marketing_campaign` | Canonical campaign ID, owner, channels, objectives, attribution naming | Operational coordination; do not duplicate Mautic campaign internals |
| `marketing_campaign_channel` | Destinations, UTM conventions, tokens/links, approvals | References only; credentials in secrets store |
| `marketing_touch_event` | Where legally permitted, event ID/source/type/timestamp/freshness | Record only necessary lawful data; Matomo remains site analytics authority |
| `marketing_conversion` | Lead/goal/order/booking conversion references and values | Link to Mautic / Matomo / commerce source; reconcile duplicate reports |
| `marketing_workflow_run` | Event idempotency, state, policy/approval refs, retries | Activepieces execution plus durable PostgreSQL record |
| `marketing_contact_link` | Pseudonymous IDs and source mapping | Mautic is authoritative for contact identity and preferences |
| `marketing_channel_consent_audit` | Consent checks, authoritative-system reference and channel classification | Keep email/telephone/SMS/tracking independently governed |
| `marketing_source_snapshot` | SerpBear, Postiz, ad costs, Mautic, Matomo measures and freshness | Preserve provider provenance; missing != zero |
| `marketing_experiment` | Hypotheses, variants, assignment approach, results, approvals | Mautic native email tests or controlled website tests |
| `marketing_affiliate_ledger` | Simple referral/affiliate accrual, refunds and approvals | Only when program enabled; auditable reversals and reconciliations |
| `marketing_loyalty_ledger` | Atomic points earned/redeemed and reversal events | Only when ecommerce/loyalty enabled |
| `marketing_budget_approval` | Before/after proposed ad spend, authorization, audit | Actual network changes verified by provider response |
| `marketing_publish_reference` | Content revision, approved channel asset, destination post ID | Link to existing V6 publication ledger; do not create a competing owner |
| `marketing_audit_event` | Significant decisions, overrides and data corrections | Protected audit policy and separate retention |

Use existing PostgreSQL infrastructure, isolated databases/schemas/accounts. Keep personally identifiable contact information in Mautic where practical. Do not copy entire email/send/contact databases into a marketing data warehouse without demonstrated need and legal basis.

### 3.4 Tracking and attribution conventions

- Assign stable, immutable internal IDs for campaigns, approved creative revisions and destination publications.
- Use consistently encoded `utm_source`, `utm_medium`, `utm_campaign`, and, when meaningful, `utm_content` / `utm_term`; document a case-insensitive normalization strategy.
- Never put names, emails, phone numbers, or secrets in campaign URLs or other tracking tokens.
- Deduplicate consented events by authoritative provider ID, source and conversion/order identity; preserve timestamps and reporting windows.
- Distinguish **reach**, **impressions**, **clicks**, **site sessions**, **leads**, **qualified leads**, **orders**, **revenue**, **cost**, and **attributed value**; do not substitute one for another.
- Set up Matomo goals for actual form submissions, bookings and sales, with appropriate ecommerce tracking if deployed. Validate goals with Playwright and real test events.
- Core Matomo provides normal referrer/goal reporting. Premium multi-touch attribution is not assumed; custom PostgreSQL calculations must explicitly state window, matching assumptions and limitations.
- Track SEO keyword rank through SerpBear and technical audits through Lighthouse separately.
- Unavailable or delayed network/advertising metrics must be labeled unavailable/freshness-limited, not zero or fabricated.


## 4. Architecture & Decision Standards

### 4.1 Infrastructure and operations — preserved from Versions 1–6

- **OS and hosting:** Debian Stable application hosts. Proxmox VE manages QEMU/KVM VMs, using its supported Debian-based host platform and virtualization/networking guidance.
- **Deployment:** Podman + Quadlet + systemd, with rootless applications where practical. Do not assume vendor Docker Compose defaults transfer without alterations.
- **Security:** Caddy terminates HTTPS; Keycloak authenticates supported apps; SOPS + age protects configuration secrets; Vaultwarden stores human-held credentials; use least-privilege per-site/per-channel API accounts.
- **Data:** PostgreSQL first for operational ledgers and workflow records. Keep native app databases/versions supported: MariaDB for Mautic when required. Use pgvector for embeddings, not as an embedding engine. Valkey is a Redis replacement only after compatibility proof.
- **Backups:** pgBackRest for PostgreSQL, mariadb-backup for MariaDB, restic for protected files and remote copies, Proxmox-native backups for VMs; test full multi-service restores.
- **Monitoring:** OpenTelemetry Collector Contrib, Prometheus/exporters, Grafana, Loki and alert delivery. Watch queue lag, outgoing events, workflow failures, publication inconsistencies and API authorization expiry.
- **Versioning & configuration:** Ansible + Forgejo/Git, pinned images/libraries/custom adapters, reviewed changes, reproducible upgrades, tested rollback.
- **Operations:** UPS/disk monitoring, resource quotas, cron/systemd job health, secure internal networking, documented manual incident recovery.
- **Secrets:** No tokens or service passwords in prompt context, campaign links, logs, warehouse snapshots or published artifacts.
- **Persistence and compatibility:** Postiz v2.12.0+ depends on Temporal, a SQL database and Redis-compatible cache. Evaluate separately isolated PostgreSQL persistence and Temporal visibility; do not assume PostgreSQL visibility or Valkey substitution is validated for the chosen images. Temporally required containers and workers remain counted as independently operated runtime services.
- **Observability ownership:** Grafana is infrastructure/ops authoritative. Matomo remains website analytics authoritative. MLflow records AI experiments and quality results. Source platform data must be marked with freshness and provenance.
- **GPU contention:** Throttle ComfyUI/media jobs to protect Pipecat real-time speech latency and business-critical processing.
- **Storage roles:** ResourceSpace is approved, rights-tracked asset library. SeaweedFS may hold temporary/bulk render files. Assets and database metadata require coordinated backup/restore.

### 4.2 Retained Version 4 voice-agent architecture

- Asterisk (PJSIP and ARI) manages telephone sessions, SIP/RTP and transfers; a dedicated Debian VM is preferred for SIP/RTP/NAT reliability.
- Pipecat is the real-time AI conversation framework, with compatible community Asterisk WebSocket bridge, local Faster-Whisper STT, Kokoro ONNX TTS and Silero VAD.
- Custom Python controller coordinates authorized outbound dialing via Asterisk ARI, schedules, retries, states, provider reconciliation and human handoff.
- Activepieces provides business triggers, not time-sensitive audio control.
- PostgreSQL contains telephone-specific consent/suppression/Do-Not-Call state. Mautic may display synchronized status, but email opt-in **never grants telephone permission**.
- Verify intended recipient location/timezone, applicable calling hours, disclosure rules, AI-generated speech and recording authorization before dialing; silence or CRM membership is not consent.
- Store authorized call recordings/artifacts in SeaweedFS and structured records in PostgreSQL with protected role-based access and retention.
- Incomplete dial outcomes must be reconciled before retrying; fail safely when controller, carrier, audio or permission data unavailable.
- llama.cpp/OmniRoute supplies LLM inference; approved PostgreSQL/pgvector retrieval supplies knowledge; restricted app tools only.
- SIPp, LiveKit, FreeSWITCH, Speaches, Piper and other voice alternatives remain conditional, not V7 marketing additions.
- Benchmark STT, first-audio latency, interruptions, concurrent calls, carrier interop and GPU isolation; track in Prometheus/Grafana/Loki/MLflow.

### 4.3 Retained Version 5 email architecture and warm-up

**Contact authority:** Mautic owns marketing contact records, channel-specific eligibility, segments, consent evidence, unsubscribe and email suppression. Valid data import never implies permission to market.

**External infrastructure:** Use managed SMTP relay, existing business reply mailbox, external authoritative DNS and applicable provider feedback. Configure SPF, DKIM, DMARC, return-path, MX, TLS and reputation reporting. Local dnsmasq is **not** the public authoritative DNS provider.

**Authentication/reporting:** `checkdmarc` runs scheduled/deployment-time checks; `parsedmarc` parses report feeds into appropriately isolated PostgreSQL records. Google Postmaster Tools and provider feedback are external data sources whose absence must be treated as unknown.

**Send execution:** Mautic retains native queue/campaign scheduling. A custom small, auditable, systemd-controlled dispatch guard gates outbound sending using PostgreSQL durable quotas/reservations/policy state, provider limits and Mautic recipient eligibility. Activepieces schedules decisions and ingests events but cannot bypass final authorization. No extra sending app, independent warm-up platform or artificial engagement exchange.

**Warm-up state machine:** `DRAFT → PRECHECK → CANARY → RAMPING → PRODUCTION`; incident paths `HOLD → INVESTIGATION → RECOVERY` with explicit human approval. Gradual ramp depends on real recipient engagement, complaints, transport health and actual business need, **not** fixed day counts or fake replies/opens.

**Delivery feedback:** Callback signatures verified; deduplicate provider IDs; reconcile uncertain SMTP acceptances before retrying; handle hard/soft bounces, complaints, deferrals and unsubscribes. Ensure manual, immediate and restarted workers cannot bypass controls. Honor one-click and visible unsubscribes where required.

**Required logical records** (existing PostgreSQL): `email_sender_identity`, `email_warmup_policy`, `email_send_ledger`, `email_delivery_event`, `email_reputation_daily`, `email_warmup_audit`, `email_suppression_audit`. Mautic remains authoritative for contact data.

**Email test/staging:** Mailpit isolated and incapable of unintended production recipient forwarding; Playwright verifies unsubscribe/preference flows. Real mailbox integration testing confirms SMTP alignment and callback behavior. Mailpit is not production SMTP.

**Email operations:** Use Grafana/Prometheus and OpenProject incident tasks. On restored system, default to `HOLD` pending reconciliation and authorization. Transactional mail must remain protected from marketing sending pauses where lawfully distinct.

**Marketing extension in V7:** All marketing email workflows (welcome, nurture, win-back, abandoned checkout, webinar invitations and newsletters) **must reuse** this Version 5 final dispatch boundary. A new Activepieces automation may trigger approved Mautic journeys but cannot send directly to the relay as an unapproved bypass.

### 4.4 Retained Version 6 content-generation architecture

**Ownership:** OpenProject defines and approves briefs, work, revisions, and release decisions. Activepieces coordinates API transitions. PostgreSQL holds immutable lifecycle records and idempotency keys. Forgejo stores prompts, templates, brand rules and source. ResourceSpace stores approved rights-tracked assets. WordPress/Postiz/Mautic hold their native publications. Matomo and SerpBear provide measurement. MLflow handles model evaluation rather than workflow state.

**Research:** SearXNG and internal approved references, SerpBear tracking, Matomo site performance, Mautic audience signals, WordPress previous content, ResourceSpace media, approved PostgreSQL/pgvector search. Capture sources, dates, rights, author and evidence; search snippets and AI citations are not automatically verified.

**Text:** llama.cpp through compatible OmniRoute endpoints, structured prompt/output schemas, pinned checkpoints/prompts, material claim/source checks and risk-based human review. Use RAG only for approved and authorized knowledge.

**Visuals:** ComfyUI for AI visual generation; deterministic charts/Excalidraw for accurate diagrams and numerical comparisons. Capture approved models, LoRAs, node versions, prompts and rights. Review brand and accessibility.

**Media:** Batch Faster-Whisper and Kokoro ONNX are separate from live telephone sessions. FFmpeg/ffprobe for rendering, encoding, subtitles, thumbnails and validation. Kdenlive only where interactive editing is required. Bound CPU/GPU/disk and execution time.

**Documents:** Markdown templates, Pandoc conversion, conditional Typst CLI for PDF typesetting; validate fonts, pagination, headings, links, accessibility and reusable approved originals.

**Editorial QA:** Vale rule sets in Forgejo, structural validators, Playwright browser tests, FFmpeg media tests and factual/source/rights review. AI cannot approve its own externally released publication.

**Content states:** `IDEA`, `BRIEF_PENDING`, `BRIEF_APPROVED`, `RESEARCHED`, `DRAFTED`, `QA`, `IN_REVIEW`, `APPROVED`, `STAGED`, `PUBLISHED`, `MEASURED`, `REFRESH_DUE`, `REJECTED`, `HOLD`, `FAILED`, `WITHDRAWN`, `ARCHIVED`.

**Durable records:** `content_item`, `content_revision`, `content_brief`, `content_source`, `content_claim_review`, `content_asset`, `content_asset_rights`, `content_generation_job`, `content_render_job`, `content_approval`, `content_publish_target`, `content_publish_attempt`, `content_performance_snapshot`, `content_experiment`, `content_audit`.

**Approval boundary:** Approval references the exact revision, assets and destination; material change invalidates it. No unknown API result may be retried blindly. Publication IDs and state must be reconciled. Publishing fails closed when rights/QA/approval inaccessible or invalid.

**Measurement:** Matomo website goals, SerpBear keyword ranks, Mautic permitted email metrics, Postiz supported social metrics, PostgreSQL snapshots with freshness, Grafana, and MLflow evaluations. Recommendation creates a new reviewed revision, not unapproved live edits.

**72 existing content workflow categories** remain standard targets:

| Family | Workflows | Reused primary tools |
|---|---|---|
| A. Research & Strategy (1–8) | Trending topics, keyword clustering, competitor gaps, audience research, campaign concepts, topical mapping, fact packs, editorial calendar | SearXNG, SerpBear, Matomo, Mautic, llama.cpp, OpenProject |
| B. Website & SEO (9–16) | Pillar and cluster articles, how-to guides, FAQ, landing pages, comparisons, case studies, content refresh | llama.cpp, ComfyUI, WordPress, Vale, Playwright, **Lighthouse V7** |
| C. Social (17–24) | Posts, thought leadership, threads, carousels, infographics, polls, reply drafts, evergreen recycling | llama.cpp, ComfyUI, Excalidraw, ResourceSpace, Postiz |
| D. Email Content (25–32) | Newsletters, welcome, nurture, launches, events, variations, re-engagement, A/B | Mautic, llama.cpp, OpenProject, V5 dispatch |
| E. Images & Design (33–40) | Hero images, thumbnails, banners, lifestyle composites, illustrations, diagrams, visualization cards, variants/alt text | ComfyUI, Excalidraw, ResourceSpace |
| F. Audio & Podcasts (41–48) | Narration, scripts, editing, AI narration, audio ads/highlights, voice-agent scripts, show notes | Faster-Whisper, Kokoro, FFmpeg, llama.cpp |
| G. Video & Motion (49–56) | Shorts, slideshows, captions, walkthroughs, cutdowns, teasers, motion scenes, recaps | FFmpeg, ComfyUI, llama.cpp, Playwright, Postiz |
| H. Documents & Lead Magnets (57–64) | Whitepapers, eBooks, checklists, buying guides, PDF case studies, one-pagers, battlecards, webinar handouts | Pandoc, conditional Typst, ResourceSpace, WordPress, Mautic |
| I. Repurposing & Optimization (65–72) | Blog→social/email, podcast→blog, video→FAQ, localization, personas, accessibility, performance refreshes | Activepieces, llama.cpp, Pandoc, Faster-Whisper, Matomo, SerpBear |

### 4.5 New Version 7 marketing architecture

**Functional domains:**

1. **Discovery:** SearXNG provides candidate sources/topics; SerpBear monitors search positions; Matomo measures owned website demand; Lighthouse assesses selected live/staged page quality.
2. **Strategy & creative:** OpenProject manages campaigns and editorial tasks; llama.cpp/OmniRoute writes; ComfyUI/Excalidraw visualize; ResourceSpace holds approved assets; Vale/Playwright/Lighthouse test relevant deliverables.
3. **Distribution:** WordPress web, Postiz social, Mautic email. Third-party ad networks/listing providers remain external and require separate approvals.
4. **Lead capture and lifecycle:** WordPress + Mautic forms; Mautic consent, contact segments, scores and marketing journeys; OpenProject sales human tasks. No second CRM.
5. **Conversion:** Mautic lead qualification; WordPress/Matomo owned-site goals; ecommerce requires real commerce system; V4 Asterisk/Pipecat can be used only for separately authorized telephone campaigns.
6. **Retention:** Mautic win-back/onboarding/permission-based newsletters; custom referral/loyalty only when justified, with atomic PostgreSQL ledgers.
7. **Measurement:** Matomo site analytics; SerpBear rank tracking; Postiz social data as actually exposed; Mautic email data; provider ad metrics as actually available; PostgreSQL normalized snapshots and Grafana. MLflow model experiments separate.
8. **Orchestration:** Activepieces performs API glue, approvals routing, scheduled checks, credential-scoped activities, retries and reconciliation. Systemd/Python handle bounded local jobs. Temporal stays Postiz-internal.

**Security and compliance:**

- Separate email, SMS, AI telephone, cookie/tracking and ad audience synchronization consent contexts; enforce at the last possible action boundary.
- Maintain accurate sender identity, legally required disclosures, customer testimonials permissions, advertising truthfulness, valid offers, unsubscribe, STOP and suppression handling, and review-platform rules.
- Ad audience exports may be restricted by consent, platform requirements or privacy law. Do not upload customer lists merely because data exists in Mautic.
- Define human approval for campaign launch, budget changes, external outreach, reputation responses, use of customer testimonials, sensitive claims and production publication.
- Use scoped identities per site/client/channel and distinguish client partitioning in each SaaS-like application. Do not assume built-in Mautic/Postiz tenant isolation guarantees.
- No invented impressions, reviews, testimonials, purchase orders or engagement events. Never simulate reputation-improving clicks or email replies.
- Verify all public/external research as untrusted; AI model cannot treat third-party website instructions as permission to call internal APIs.
- No raw contact identifiers in URL parameters, generic logs or exported reports. Retain only business-required data; define applicable retention and rights-deletion handling.
- Preserve consistent consent rechecks after workflow delays; STOP/unsubscribe removes eligibility even for already queued messages.
- Do not auto-release budgets, send SMS, publish regulated claims or publicly respond to complaints solely based on LLM recommendations.

**Experiment safeguards:**

- Email variants may use supported Mautic native A/B functions under V5 sending limits.
- For website variants, establish stable random assignment and exposure tracking, predeclared metric, required sample size/analysis plan and rollback controls; a naive alternating-content page is not a statistically valid A/B test.
- Matomo core does not supply every premium experiment/attribution capability. Deploy GrowthBook OSS only when actual program sophistication justifies its extra platform and edition terms.
- Promotion of a winning variant remains a review/approval decision, not automatic self-publishing.


## 5. Standard Reference Workflows — Versions 5–7

### 5.1 Standard V5 email warm-up and sending workflow — retained

| Stage | Task | System owner / services | Output |
|---|---|---|---|
| 1. Plan | Sending purpose, audience, domain, approvals, limits, consent | OpenProject, Mautic | Approved plan |
| 2. Provision | Public DNS, SMTP relay, reply/report mailbox | Ansible, DNS/SMTP/mailbox providers | Identity infrastructure |
| 3. Authenticate | SPF, DKIM, DMARC, MX, TLS and delivered-message alignment | checkdmarc, controlled real-mailbox tests | Passing checks |
| 4. Reputation | Eligible provider feedback and Postmaster setup | External provider feedback | External metrics when available |
| 5. DMARC/TLS | Report collection and storage | parsedmarc, PostgreSQL | Authentication history |
| 6. Select audience | Genuine eligible recipients, suppression and engagement checks | Mautic | Authorized cohorts |
| 7. Create content | Use approved V6 research/writing/asset pipeline | SearXNG, llama.cpp, ResourceSpace | Draft email assets |
| 8. Review | Legal, editorial, links, segmentation | OpenProject | Exact approved revision |
| 9. Test | Mail headers, SMTP, links, unsubscribe, landing page | Mailpit staging, Playwright, real controlled delivery | Tested configuration |
| 10. Initialize | Stage, quotas, approvers, policy version | Activepieces, PostgreSQL | `PRECHECK` / `CANARY` |
| 11. Dispatch | Final consent/authorization, reservations, bounded sending | Mautic, systemd guard, SMTP provider | Send attempts |
| 12. Ingest feedback | Provider callbacks, failures, deferrals and complaints | Activepieces, PostgreSQL, Mautic | Deduplicated events |
| 13. Suppress | Unsubscribe, failed destinations, blocklists | Mautic, provider, dispatch guard | Eligible sends only |
| 14. Evaluate | Real provider metrics, complaints, DMARC and deferrals | parsedmarc, Prometheus, Grafana | Health evaluation |
| 15. Adjust | Ramp, maintain, reduce or hold | Activepieces, PostgreSQL, guard | Revised signed-off policy |
| 16. Recover | Investigate incidents before resume | OpenProject, Grafana, Mautic | Approved remediation |
| 17. Transition | Move into controlled production | Mautic, PostgreSQL, Activepieces | `PRODUCTION` |
| 18. Maintain | Ongoing consent, domain, reputation, reporting and backups | Existing V5 stack | Continuous readiness |

V7 does not introduce alternative warm-up/sending engines and does not allow artificial engagement.

### 5.2 Standard V6 universal content production workflow — retained

| Stage | Task | Software |
|---|---|---|
| 1. Request | Define audience, objective, channel, owner, deadline | OpenProject |
| 2. Brief | Approve scope and risks | OpenProject, Activepieces |
| 3. Research | Verified source pack and SEO/analytics history | SearXNG, SerpBear, Matomo, Mautic |
| 4. Knowledge | Approved context, source IDs, retrieval rules | PostgreSQL + pgvector, Forgejo |
| 5. Draft | Local AI writing, metadata and structure | llama.cpp, OmniRoute |
| 6. Assets | Approved visual, image, audio and diagram components | ComfyUI, Excalidraw, Faster-Whisper, Kokoro, ResourceSpace |
| 7. Render | Convert into target formats | FFmpeg, Pandoc, conditional Typst |
| 8. QA | Style, structural, links, technical website/asset tests | Vale, Playwright, FFmpeg/ffprobe, **Lighthouse V7 for website targets** |
| 9. Assets & rights | Version/rights/provenance storage | ResourceSpace, SeaweedFS, PostgreSQL |
| 10. Editorial approval | Verify factual claims, brand, accessibility, rights | OpenProject |
| 11. Stage | Prepare destination content under approved identities | Activepieces, WordPress, Postiz, Mautic |
| 12. Publish | Final revision and permission recheck | WordPress, Postiz, Mautic |
| 13. Reconcile | Verify destination ID, delivery and unknown outcomes | Activepieces, PostgreSQL |
| 14. Measure | Goals, ranks, email and social activity | Matomo, SerpBear, Mautic, Postiz, PostgreSQL |
| 15. Improve | Evaluate controlled refresh or repurposing | Activepieces, MLflow, OpenProject |

### 5.3 New V7 universal online marketing campaign workflow

| Stage | Task | Responsible software/services | Output |
|---|---|---|---|
| 1. Objective | Specify channel, target segment, business goal, unit economics and constraints | OpenProject | Approved campaign specification |
| 2. Permission map | Define data collected and marketing eligibility by channel/jurisdiction | Mautic + approved policy rules | Channel-consent requirements |
| 3. Audience intelligence | Review permitted demand and previous performance | Matomo, Mautic, SearXNG, SerpBear | Research/segment pack |
| 4. Campaign identity | Assign stable campaign ID, UTM conventions, report owner | PostgreSQL, Forgejo config | Campaign metadata |
| 5. Creative brief | Draft and approve offer, benefits, evidence, CTA | OpenProject, local AI stack | Approved brief |
| 6. Production | Create text, images, documents and media | llama.cpp, OmniRoute, ComfyUI, Pandoc, FFmpeg | Draft channel assets |
| 7. QA | Vale, Playwright, Lighthouse, destination validation; brand/compliance review | Existing QA and OpenProject | Approval evidence |
| 8. Channel staging | Upload approved content as pending/scheduled to owning systems | WordPress, Postiz, Mautic, approved ad APIs | Staged destinations |
| 9. Release authorization | Confirm revision, target, credentials, consent and budget/volume policy | OpenProject approvals; PostgreSQL; V5/V4 dispatch as applicable | Signed-off action |
| 10. Execute | Native publishing, Mautic mailing, approved paid ad launch, or authorized call/SMS | Destination-owner system | External attempt IDs |
| 11. Reconcile | Check external outcome; deduplicate; distinguish unknown from failure | Activepieces, PostgreSQL | Confirmed status |
| 12. Collect performance | Sources, website goals, leads, costs, conversions, revenue, complaint/delivery metrics | Matomo, Mautic, Postiz, SerpBear, providers | Timestamped source snapshots |
| 13. Review results | Compare to named KPI with uncertainty and missing-data notes | PostgreSQL, Grafana, OpenProject | Analysis/decision |
| 14. Optimize | Create *new* work item and revised approved test | OpenProject, MLflow where AI relevant | Next authorized iteration |
| 15. Archive/withdraw | Handle end dates, suppression, cleanup, rights and revocation | Native channel owners + V6 lifecycle ledger | Audit and retention closure |

**Default policy:** no unreviewed public AI content, no auto-budgets without delegated authorization, no contact before verified eligibility, no social/API work beyond documented platform scope.

## 6. Compatibility, Deployment, Acceptance & Status

### 6.1 Compatibility and deployment rules

| Component | Mandatory verification |
|---|---|
| Lighthouse — NEW | Pin Lighthouse, supported Node.js, Chrome/Chromium and headless flags; run isolated/limited jobs; test audit repeatability and report parsing |
| WordPress and WooCommerce (if selected) | Verify WordPress/PHP/plugin compatibility, REST/webhooks, orders/refunds, staging, payment gateway and rollback; no extra CMS |
| Mautic | Pin version, supported MariaDB/queue semantics, email experiments, webhooks, stage/segment scoring, V5 suppression enforcement |
| Activepieces | Webhook authentication, rate limits, least-privilege connector credentials, run retries, timeouts, idempotent integration IDs |
| Postiz | Exact version, platform integration permissions, Temporal/orchestrator health, PostgreSQL/Valkey compatibility, publication reconciliation |
| Temporal (Postiz internal) | Worker health, namespace/persistence isolation, backed-up schemas, visibility configuration, DB pressure, upgrades/recovery |
| Matomo | Version, goal/event implementation, UTM attribution assumptions, consent handling, anonymization and data retention |
| SerpBear | Search data source, tracked term/rank freshness, auth, API access and limits |
| SearXNG | Approved engines, legal/terms constraints, metasearch availability and source provenance |
| OpenProject | Supported work-package APIs, exact revision-bound approval mapping, per-client permissions |
| ResourceSpace | Signed API, asset metadata/rights, file storage and retrieval after restore |
| llama.cpp/OmniRoute | Model capability, tool calls, JSON, streaming and inference performance tested per model |
| ComfyUI | Workflow schemas, custom nodes/checkpoints, security isolation and image rights |
| Vale/Playwright/FFmpeg/Pandoc | Pinned tool versions, template/test rule coverage, bounded run resources |
| Ad APIs | Identity, permissions, quotas, required attribution semantics, explicit spend limits and human change approval |
| SMS | Verified channel-specific consent, opt-outs, provider callback signatures, carrier registration, delivery status semantics |
| Conditional services | License, runtime dependencies, ports, SSO, data backup and service monitoring before installation |

### 6.2 Required V5 email acceptance tests — preserved

| Test | Required outcome |
|---|---|
| SPF/DKIM/DMARC and DNS | Valid real-message alignment |
| SMTP authentication | Valid authenticated TLS transport |
| Mautic targeting | Only eligible recipients selected |
| Consent/unsubscribe | Ineligible/opted-out contacts excluded |
| Unsubscribe during queue delay | Final dispatch prohibits send |
| Rate-cap enforcement | Authorized quotas cannot be exceeded |
| Concurrent workers | No duplicate sends/reservations or uncontrolled bursts |
| Immediate/manual bypass | Guard prevents unauthorized delivery |
| Permanent bounce | Correct suppression |
| Repeated provider webhook | Idempotent processing |
| Temporary SMTP rejection | Safe backoff; no retry storm |
| No Postmaster data | Mark unknown, not healthy |
| Activepieces/DB outage | New marketing authorization fails closed |
| Mautic restart | Guard remains effective |
| Mailpit test | Retry/headers/links behave in staging |
| Playwright unsubscribe | Actual UI/action succeeds |
| DNS misconfiguration | Production marketing traffic held |
| Restore after outage | Reconciled, held until approved |
| Incident recovery | Controlled ramp after approval |

### 6.3 Required V6 content acceptance tests — preserved

| Test | Required outcome |
|---|---|
| Brief and objective | Missing required values block generation |
| Research/evidence | Claims link to verified provenance |
| Untrusted sources | Prompt injection cannot alter tools/permissions |
| Structured AI output | Schema conforms or fails clearly |
| Approved knowledge retrieval | Access scope enforced |
| Factual review | Unsupported material claims held |
| Vale brand/style checks | Rule violations handled under policy |
| Disclaimers and rights | Invalid/missing items block release |
| ComfyUI models/nodes | Approved versions and job results recorded |
| ResourceSpace | Asset/rights metadata retrieval passes |
| FFmpeg | Audio/video/subtitles/output format validated; partial files invalid |
| Pandoc/Typst | Target formats/layout, hyperlinks and accessibility checked |
| Content approval | Bound to exact revision, assets and destination |
| Modified approved content | Approval invalidated if material |
| WordPress staging | Stays unpublished before approval |
| Postiz and Temporal | Correct account/schedule; dependency failure cannot silently lose work |
| Mautic email | V5 dispatch and consent controls upheld |
| Duplicate publishing request | No duplicate external publication |
| Unknown publishing result | External state reconciled before retry |
| Credential failure | Fail closed; no secret leak |
| Activepieces/DB outage | New publishing cannot bypass approval |
| Missing media | Publication held |
| Unauthorized social account | Release rejected |
| Invalid customer rights | External release blocked |
| Withdrawal | Internal and native destination state reconciled |
| No analytics | Mark unavailable |
| Changed model | Regression quality checks before promotion |
| Parallel rendering | Resource quotas and critical voice preserved |
| Restore | Approved originals, job state and decisions recoverable |

### 6.4 New Version 7 marketing acceptance tests

| Test | Required outcome |
|---|---|
| Marketing campaign schema | Campaign ID, channel, source, objective and owner created once |
| UTM propagation | WordPress, Postiz, Mautic links consistently tagged; no personal identifiers |
| Form submit | Mautic contact/consent, duplicate handling and Matomo goal correlated |
| Double-submit / webhook retry | No duplicate contacts, rewards, commissions or follow-up tasks |
| Cross-channel permission | Email, SMS, phone, ad audience and tracking decisions evaluated independently |
| Consent withdrawal in-flight | Queued prohibited messages/actions blocked at final dispatch |
| Website tracking | Tracking configured under consent rules; denied cookies/scripts not activated improperly |
| Lighthouse report | Headless audit works on staging and reports actionable, versioned findings |
| SEO separation | SerpBear rank and Lighthouse technical audit reported as distinct metrics |
| Social API disconnection | Account/permission failure visible; approved publications not duplicated |
| Postiz/Temporal outage | Social job held/reconciled with no unknown duplicate posts |
| Paid ads denied permissions | No unsupported attempted audience export/spend update |
| Ad budget change | Recorded human authorization, network confirmation, bounded limits |
| Ecommerce missing | Checkout recovery/loyalty disabled until valid order feed exists |
| Abandoned-cart purchase after trigger | Customer no longer receives the inappropriate recovery message |
| Refund/chargeback | Referral, commission and points reversed/audited as applicable |
| Attribution join | Event IDs deduplicated; model/period assumptions documented |
| Advertising data absent | Reporting shows unknown and freshness, not fabricated zeros |
| Experiment | Assignment/exposure, hypothesis, conversion and promotion approvals correct |
| First-party reviews | Legitimate testimonials verified and moderations auditable; no review gating |
| SMS STOP | Immediate suppression and no further marketing sends |
| Provider SMS unavailable | Safe retry or hold; no alternate unapproved sending path |
| Client separation | Users, tokens, dashboards and asset permissions isolated as required |
| Sales handoff | Lead assigned once; errors create visible work items |
| Real visitor metrics | Matomo goals tested with Playwright real conversion path |
| Marketing report | Shows channel unit, attribution source, refresh timestamp and confidence limitation |
| Recovery | Restore in held state and reconcile paid/published/sent external outcomes |
| Consent/retention deletion | Relevant records/caches/exports handled under documented privacy policy |

### 6.5 Implementation status and outstanding decisions

| Area | V7 decision | Remaining work |
|---|---|---|
| Core V6 infrastructure | Unchanged | Audit actually deployed versions and capacity |
| V4 voice stack | Preserved | Voice integrations, legal, audio latency and load validation |
| V5 email stack | Preserved | Real SMTP provider, DNS, Mautic queue, dispatch guard, callback and tests |
| V6 content stack | Preserved | Deploy FFmpeg/Pandoc/Vale, adapters, editorial approvals and QA |
| Lighthouse — NEW | **Selected CLI** | Install/pin Node runtime and Chromium, automated baseline staging tests |
| Marketing workflows | **36 architectural patterns standardized** | Implement triggers/APIs and business-specific policies |
| Marketing operational data | **Reuse PostgreSQL** | Isolated schema, event IDs, retention, migrations, backups |
| Marketing campaign/UTM convention | **Selected** | Version standardized naming and event definitions in Forgejo |
| Owned-site analytics | **Retain Matomo** | Goals, consent configuration, form/order events and KPI validation |
| CRM/lead workflow | **Retain Mautic** | Segments, scoring, lifecycle map, permissions and duplicate handling |
| Cross-app marketing automation | **Retain Activepieces** | Campaign templates, idempotent callbacks, exception queues |
| Content approval | **Retain OpenProject** | Human approvals for every material external revision/channel |
| Marketing reporting | **Grafana + PostgreSQL default** | Refresh and source dashboards; verify performance at scale |
| Native social scheduling | **Retain Postiz** | Actual Postiz + Temporal/DB/Valkey deployment compatibility |
| Website experiments | Basic permitted custom variant or Mautic email A/B | GrowthBook conditional only after defined requirement |
| Ecommerce | **Not automatically selected** | Choose WooCommerce if the business actually operates an online store |
| Client shared inbox | **Not automatically selected** | Deploy Chatwoot only at demonstrated message/team complexity |
| Webinar platform | **Not automatically selected** | External provider or Jitsi based on actual event use |
| Paid ad campaigns | **External provider conditional** | Approve accounts, SDK/API access, consent and spend governance |
| SMS | **External provider conditional** | Verify SMS support, jurisdictional registration, STOP and callback handling |
| Local business listings | **External provider conditional** | Verify listing owner authorization and provider API availability |
| Advanced BI | **Metabase remains conditional V6** | No duplicate dashboard platform absent unmet need |
| Referrals/affiliates | Small custom state only when program enabled | Financial controls and platform decision at larger scale |
| Security/compliance | Inherited + V7 consent/measurement rules | Business- and jurisdiction-specific review |
| Acceptance tests | V4/V5/V6 retained; V7 additions above | Execute in staging and document actual results |

### 6.6 Implementation priority sequence

| Priority | Action | Acceptance milestone |
|---|---|---|
| P0 | Inventory V6 deployments and Postiz/Temporal dependencies | Actual topology and service ownership documented |
| P0 | Confirm V5 Mautic email transport and suppression guard | Controlled fail-closed sending tested |
| P1 | Create campaign ID/UTM schema and PostgreSQL operational tables | Stable cross-channel references and permissions |
| P1 | Add Lighthouse CLI to bounded Debian job environment | Versioned technical audit report on staging WordPress |
| P1 | Connect WordPress/Mautic forms to Matomo conversion goals | Verified end-to-end lead and goal record |
| P1 | Complete SEO/content publication loop | SearXNG → OpenProject → QA → WordPress → Matomo/SerpBear |
| P1 | Complete social publication loop | OpenProject-approved master → Postiz → external confirmation |
| P1 | Build Mautic welcome, nurture and sales handoff | Permission-based campaign via V5; OpenProject tasks |
| P2 | Normalize Matomo/Mautic/Postiz/SerpBear source snapshots | Grafana marketing KPI panels with freshness |
| P2 | Launch approved newsletter, SEO refresh and content repurposing | Reusable cross-channel derivatives with version lineage |
| P2 | Implement controlled reports for clients/campaigns | No accidental exposure between client contexts |
| P3 | Test website experiments against actual demand | Statistically valid measurement and promotion controls |
| P3 | Activate business-specific ecommerce, ads, SMS, events or loyalty | Each activation separately approved and tested |
| P3 | Consider Metabase/GrowthBook/Chatwoot/etc. only after measured gaps | Added-service business case and recovery plan approved |


## 7. Consolidated Decision Standards for Future Stack Evaluations

All existing Version 6 principles continue to apply. The following consolidated rules are controlling for all subsequent versions:

### General standards — Versions 1–5 retained

1. Reuse selected services before considering anything new.
2. Preserve authoritative application ownership: Mautic contacts/campaigns, PostgreSQL designated operational state, Activepieces cross-app processes, Grafana operational dashboards.
3. Avoid competing CRM, website analytics, dashboard, social scheduler, CMS, DAM, email campaign or general-purpose automation systems without documented failure of the baseline.
4. Distinguish standalone servers from plugins, libraries, utilities, custom code, models, native application dependencies and external services; count real runtime services and persistence requirements even if bundled.
5. Prefer supported REST APIs, authenticated webhooks, SMTP/IMAP where permitted, supported DB interfaces and OpenTelemetry.
6. Require idempotent state, controlled retries, human approvals, monitoring, audit trail and rehearsed disaster recovery.
7. Treat email, telephone, SMS, tracking and ad-list consent/suppression as independent legal and policy decisions.
8. Preserve Keycloak/SSO where supported, Caddy HTTPS, secrets protection, network segmentation, backup and independent recovery access.
9. Prefer actively maintained, business-compatible open source; review license obligations for the deployed edition and modified/network services.
10. Validate actual pinned release compatibility on Podman/Quadlet, Valkey, native DB engines, models, codecs, SSO and object storage.
11. Add brokers, storage, BI or independent workers only for measured load or missing functionality.
12. Distinguish standardized architecture from production validation; all implementation gaps remain explicit.

### Content-generation standards — Version 6 retained

13. Reuse llama.cpp/OmniRoute/ComfyUI and existing model infrastructure before another AI platform.
14. OpenProject owns human editorial authority; AI cannot self-approve material public releases.
15. WordPress, Postiz and Mautic own their publication channels; Activepieces connects their supported APIs.
16. Share reusable research, drafts, QA, rights tracking, review, distribution and optimization mechanisms across 72 content categories.
17. Prefer bounded FFmpeg/Pandoc/Vale/Lighthouse utility jobs to additional persistent services.
18. Isolate GPU/media jobs to protect live Pipecat call responsiveness and operational capacity.
19. Track original source, provenance, usage rights, model configuration, prompts, assets and revision lineage.
20. Check permission and exact approved revision at final publishing boundary.
21. Reconcile unknown remote publish outcomes; retries must not duplicate externally visible content.
22. Respect application/code licenses, model weights, voices, fonts, codecs, media inputs and customer likeness rights separately.
23. Use testable factual quality, accessibility, destination compatibility, render limits and measurable business outcomes.
24. Preserve measurement authority: Matomo onsite, SerpBear rank, Mautic email, Postiz social, external platforms their own native metrics.
25. Reuse approved master content when deriving social/email/media variants; invalidate approval when material changes occur.
26. Never fabricate reviews, social interactions, clicks, emails or engagement to influence reputation or KPIs.
27. Account for Postiz/Temporal and other native application dependencies in actual deployment footprint.
28. Keep Typst, Kdenlive, advanced AI models and specialized platforms conditional until required.
29. Pin/version prompts, checkpoints, workflows, rendering recipes and MLflow evaluations.
30. Hold publishing when necessary evidence, rights, permission, QA, or destination state is unavailable.
31. Minimize separately administered services and new databases in favor of existing authenticated APIs and infrastructure.
32. Require an explicit change/selection record for functionality, OSS license, deployment effort, resource cost, security, monitoring, backup and long-term maintenance.

### Additional online marketing standards — New in Version 7

33. **Mautic remains the contact and marketing journey authority.** Do not install Twenty, EspoCRM, SuiteCRM, listmonk, Dittofeed or another CRM/mailer without demonstrated need for functions Mautic cannot perform.
34. **Matomo remains the web analytics authority.** Do not add Plausible, Umami or PostHog by default; multi-touch attribution must be explicitly modeled or separately licensed, never silently assumed included in Matomo core.
35. **Postiz remains the social distribution authority.** Do not add Buffer, Mixpost or another social scheduler absent demonstrated unsupported channels/features.
36. **SEO tasks have distinct owners:** SearXNG for source discovery; SerpBear for tracked positions; Lighthouse for page technical/performance/accessibility audit; Playwright for end-to-end rendered UX/behavior testing. None alone replaces all SEO functions.
37. **Preserve measurement integrity:** One campaign identity and UTM taxonomy, distinct metrics, source time/freshness and documented attribution limits.
38. **Enforce marketing permission per channel at execution time:** Ineligible contacts, unsubscribes, STOP, Do Not Call, audience-export restrictions or rejected tracking permissions must take precedence over scheduled campaigns.
39. **Paid advertising is always an external network dependency:** Client libraries are integrations, not open-source ad networks. Set spending limits, API scopes, human budget approval, and confirm conversions before optimization.
40. **Ecommerce is a conditional business capability:** Select WooCommerce within WordPress only if own-site checkout, carts, orders or lifecycle marketing truly require it. No abandoned-cart or sales/loyalty automation is valid without real purchase events.
41. **Experimentation requires valid methodology:** Keep Mautic native email tests. Use controlled WordPress variants/Matomo for low volume, adopt GrowthBook only when necessary and licensed. No automatic self-promotion of high-impact variants.
42. **Client/agency data needs verified isolation:** Mautic contact segments and OpenProject project labels are not automatically equivalent to hard tenant boundaries. Validate data access at API, asset, dashboard and publishing credential layers.
43. **Reputation and outreach must be truthful and permitted:** No fabricated testimonials, biased/gated review requests, unsolicited or prohibited automation, or hidden affiliate/influencer arrangements.
44. **Marketing add-ons must remain genuinely conditional:** WooCommerce, GrowthBook, changedetection.io, Chatwoot, Jitsi, pretix, Site Reviews and CookieConsent are candidate choices, not blanket baseline dependencies.
45. **Marketing reports require explainable numbers:** Retain query definitions, campaign IDs, currency, timezone, reporting period, source timestamps and errors; do not report missing feeds as zero.
46. **Leads crossing into telephone/SMS do not gain permission from Mautic's email status:** Version 4 and applicable messaging rules must be evaluated independently.
47. **Use human authorization for sensitive external changes:** Production budget changes, public reputation replies, withdrawals, major offer changes and direct high-risk outreach require proper approvals.
48. **Every extension must be reversible:** Document downgrade/rollback, content/schedule reconciliation, exportable data, backup and recovery for the changed workflow.

## 8. Version 7 Final Standardization Summary

| Area | Standardized decision |
|---|---|
| Core networking/OS/virtualization/containers | Retain Version 6 |
| Identity, proxies, secrets, provisioning and backups | Retain Version 6 |
| Relational/vector/cache/object storage | PostgreSQL/MariaDB, pgvector, Valkey, SeaweedFS as in Version 6 |
| General workflow automation | Activepieces |
| Native Postiz durable scheduling | Temporal as required by Postiz release; isolate and test |
| AI text/routing and visuals | llama.cpp + local OmniRoute, ComfyUI |
| Voice-agent architecture | Retain V4 Asterisk + Pipecat + authorized carrier/consent rules |
| Email delivery and warming | Retain V5 Mautic + managed relay + guard + monitoring |
| Content generation | Retain V6 FFmpeg, Pandoc, Vale and 72 content workflow categories |
| **Technical SEO / page audits** | **New selected Lighthouse CLI** |
| Keyword/source research | SearXNG, SerpBear |
| Strategy, project tasks, editorial/sales/budget approval | OpenProject |
| Lead capture, segmentation, lead scoring, nurturing and email campaigns | Mautic |
| Web/landing page publishing | WordPress |
| Social scheduling | Postiz |
| Approved marketing assets | ResourceSpace |
| Website conversions and campaign analytics | Matomo core; explicit goal configuration |
| Cross-system reporting and audit/ledger records | Existing PostgreSQL + Grafana; Metabase conditional |
| Campaign IDs and UTMs | Stable, versioned normalization conventions in Forgejo/PostgreSQL |
| SEO content and social repurposing | Existing V6 creation pipeline |
| Basic A/B testing | Mautic email A/B; carefully built WordPress/Matomo site variants |
| Ecommerce / abandoned cart / post-purchase | Conditional WooCommerce + order integrations |
| Specialized web experiments | Conditional GrowthBook OSS core |
| Public website change monitoring | Existing Playwright/Activepieces first; changedetection.io conditional |
| Omnichannel shared customer inbox | Chatwoot conditional |
| Events/webinars | Basic WordPress/Mautic signup; conditional Jitsi/pretix |
| First-party reviews | Existing WordPress support; conditional Site Reviews |
| Tracking consent frontend | Appropriate site setup; conditional CookieConsent library |
| Telephone/SMS marketing | V4 authorized calling; external permitted SMS network for SMS workflows |
| Paid ads, public listings, payments | External accounts/APIs when used, with enforced scopes, budgets and consent |
| Referral/affiliate/loyalty | Simple durable custom ledgers only where appropriate; additional platform conditional |
| Most-common online marketing workflow coverage | 36 patterns integrated into V6 baseline |
| Version 7 mandatory new software *platforms* | **Zero** |
| Version 7 selected new *CLI utilities* | **One: Lighthouse** (Node.js + Chrome/Chromium execution dependencies) |
| Version 7 new mandatory external marketing SaaS | **None beyond previous V4/V5 dependencies** |
| Implementation status | Selected architecture; deployed integration/testing is still required |

### Expected deployment footprint

- **Lighthouse:** Bounded CLI invocation on existing Debian/Podman job workers; requires supported Node.js and Chrome/Chromium binaries, pinned versions, predictable disk/memory and safe access to test URLs; **zero new persistent app servers**.
- **Marketing campaigns/workflows:** Additional application configuration, webhook/API connectors, PostgreSQL records, monitoring dashboards, staging test cases and optional Python adapters; **zero new general-purpose app engines**.
- **Conditional features:** WooCommerce/Site Reviews as WordPress extensions when chosen; GrowthBook/changedetection.io/Chatwoot/Jitsi/pretix as new services only if chosen; CookieConsent as frontend library. Each can add substantial dependency and operational work and must be justified separately.
- **Pre-existing dependency:** Postiz v2.12.0+ Temporal remains a required independent runtime; PostgreSQL/Valkey configuration needs release-specific proof, isolation and backup. It is not newly introduced in Version 7.
- **Existing external services:** V4 SIP trunk and V5 managed SMTP/public DNS/mailbox; new ads/SMS/payments/business-listings services only if campaigns require them.

### Primary objective — carried forward

> Preserve the full Version 6 self-hosted architecture and its Version 4/5 safeguards; minimize new independently operated services and maintenance while enabling the 36 common online marketing workflows with correct permissions, reliable reporting, native application ownership, explicit exceptions and measured return on added complexity.

### Critical implementation caution

This document is a **decision baseline**, not a representation that all selected software is installed, compatible, legally approved or production ready. Before any operation is enabled, verify versions, licensing of exact editions/plugins/models, credentials/API permissions, data ownership, backups, recovery, consent and all relevant acceptance tests. The software named here is not a substitute for channel-provider approvals or business-specific compliance review.

### Official project and reference documentation (selection verification)

- Lighthouse: https://github.com/GoogleChrome/lighthouse ; https://github.com/GoogleChrome/lighthouse/blob/main/readme.md
- Postiz configuration and Temporal: https://github.com/gitroomhq/postiz-docs/blob/main/self-host/configuration/reference.mdx
- Postiz runtime architecture: https://github.com/gitroomhq/postiz-docs/blob/main/self-host/architecture.mdx
- Mautic email A/B testing: https://docs.mautic.org/en/7.2/channels/emails.html
- Matomo goals: https://matomo.org/guide/reports/goals-and-conversions/
- Matomo commercial multi-channel attribution distinction: https://matomo.org/faq/reports/set-up-and-analyse-multi-channel-conversion-attribution-reports/
- WooCommerce: https://github.com/woocommerce/woocommerce
- GrowthBook open-source vs enterprise edition: https://github.com/growthbook/growthbook
- CookieConsent: https://github.com/orestbida/cookieconsent
- Changedetection: https://github.com/dgtlmoon/changedetection.io
- Chatwoot: https://github.com/chatwoot/chatwoot
- Jitsi: https://github.com/jitsi/jitsi-meet
- pretix: https://github.com/pretix/pretix
- Site Reviews: https://github.com/pryley/site-reviews

*Reference baseline prepared October 25, 2026. Revalidate licenses, runtime dependencies, and external API availability at deployment time.*

## Appendix A. Exact V6 content workflow catalog retained for handoff

| Content family | Retained workflow names |
|---|---|
| A. Research & Strategy | 1. Trending topic discovery; 2. SEO keyword clustering; 3. Competitor content-gap analysis; 4. Audience pain-point research; 5. Campaign concept generation; 6. Topical authority mapping; 7. Fact-check/source packs; 8. Editorial calendar generation |
| B. Website & SEO | 9. SEO pillar articles; 10. Topic-cluster articles; 11. How-to guides; 12. FAQ/knowledge articles; 13. Landing pages; 14. Comparison pages; 15. Customer case studies; 16. Existing-content refreshes |
| C. Social Media | 17. Short social posts; 18. Thought-leadership posts; 19. Threads; 20. Social carousels; 21. Infographics; 22. Poll campaigns; 23. Community reply drafts; 24. Evergreen post recycling |
| D. Email Content | 25. Newsletters; 26. Welcome sequences; 27. Lead nurture; 28. Product launches; 29. Event promotion; 30. Audience-specific variations; 31. Re-engagement; 32. A/B testing |
| E. Images & Visual Design | 33. Blog hero images; 34. Social graphics/thumbnails; 35. Advertising banners; 36. Product lifestyle composites; 37. Brand illustrations; 38. Process diagrams; 39. Data visualization cards; 40. Asset variants/accessibility |
| F. Audio & Podcasts | 41. Blog narration; 42. Podcast scripts; 43. Recorded podcast editing; 44. AI-narrated podcasts; 45. Audio ad creatives; 46. Short audio highlights; 47. Voice-agent knowledge scripts; 48. Transcripts/show notes |
| G. Video & Motion | 49. Vertical shorts; 50. Slideshow explainers; 51. Captioned videos; 52. Product walkthroughs; 53. Long-video cutdowns; 54. Teasers/thumbnails; 55. AI-generated motion scenes; 56. Webinar recaps |
| H. Documents & Lead Magnets | 57. Whitepapers; 58. eBooks; 59. Downloadable checklists; 60. Buyer's guides; 61. Case-study PDFs; 62. Product one-pagers; 63. Sales battlecards; 64. Webinar scripts/handouts |
| I. Repurposing & Optimization | 65. Blog-to-social; 66. Blog-to-newsletter; 67. Podcast-to-blog; 68. Video-to-FAQ/article; 69. Localization; 70. Persona-specific variants; 71. Accessibility assets; 72. Performance-driven refreshes |

## Appendix B. Standard decision record for future proposals

For each suggested software change or new marketing workflow, require a review record containing:

- **Task and unmet function:** Description, frequency, business requirement and proof that existing V7 components do not meet it.
- **Proposed package:** Repository, current maintainer activity, selected version/edition, commercial license and material dependencies.
- **Baseline substitutes:** Existing-stack first choice, supported plugins/libraries, small integration option and reason not sufficient.
- **Deployment classification:** Native feature, existing library/CLI, new plugin, custom bounded job, independent service, or external account/network.
- **State ownership:** Source-of-truth app, API objects, durable PostgreSQL records, migration plan and idempotency strategy.
- **Security and privacy:** SSO, API tokens, client/role isolation, marketing consent, retention, rights and provider terms.
- **Operations:** Resource footprint, GPU/CPU/RAM/disk, queues, monitoring, logs, alert owner, patch process and backups/restore test.
- **Acceptance and rollback:** Test evidence, version pins, failure behavior, release/rollback/withdrawal controls.
- **Decision:** Select, select as conditional, defer or reject, with approver, rationale, date and next review.

Use this **Version 7** document, including its inherited Version 4/5/6 policies, as the mandatory starting point for such decisions.
