# Changelog

Version history for WitFoo products.

## v1.1.0 (2026-07-14)

Feature release on the 1.0.0 GA line — *from signal to evidence and decisive action*. Sharper investigations, the new **Certify** compliance-certification capability, scheduled report delivery, broader data onboarding, and a hardened, verified multi-tenant foundation. A recommended, drop-in upgrade for all 1.0.x deployments. **[Watch the 1.1.0 tour.](https://vimeo.com/1209183185)**

### Investigation

- **One-click CVE explanations** — click any CVE in a report or on a host for a plain-language explanation (severity, description, weakness type), served offline from a committed CVE library with no internet calls
- **Exploitability-aware threat scoring** — a live vulnerability on a host connected to an outside asset now raises incident suspicion and flags attacker and victim, with a new "Weak Edge" view (CVE × technique × attacker × victim) alongside Attack Chain
- **Verdict-first entity detail** — the node/entity panel leads with a clear verdict ("Suspicious · 39% · Medium") then why-flagged / where-who / related / activity, values humanized, raw JSON and schema behind an Advanced disclosure
- **In-panel relationship pivoting** — search all of an entity's relationships from its panel with a "Top relationships" shortlist (internal users first)
- **The true target of an attack is always visible** — the internal host under attack is no longer missing from a work unit's evidence and graph; attacker→victim is correctly linked

### Asset & Identity

- **Accurate internal-user classification** — a user counts as internal/managed only when sourced from a real identity system (Entra ID, AD, Okta, Ping…); log noise and failed logins no longer inflate the count
- **Open-port visibility on assets** — assets carry the observed network services (open ports), searchable and filterable from asset search
- **Full-scope range filtering** — min/max filters for an asset's port, vulnerability, and product counts now narrow the entire dataset, not just the rows on screen

### Compliance & Certify

- **Certify — audit certification packages (SOC 2 / ISO 27001 / CMMC)** — build an audit submission inside WitFoo with guided questions, malware-scanned attachments, and live-data auto-population, exported as one integrity-hashed package (report + attachments + manifest) streamed on demand (Pro/Max tiers)
- **One Auditor, many frameworks** — adds PCI DSS v4.0 and Essential Eight mappings beyond CIS Controls
- **ISO 27001 updated to the 2022 standard** — built-in ISO 27001 moves to the current :2022 Annex A (93 controls)
- **Honest compliance-readiness score** — partial control coverage now counts as partial, so the readiness percentage reflects reality

### Reporting & Data

- **Scheduled report delivery** — schedule reports and dashboards as offline PDFs delivered on a cadence to notification channels (email attaches the PDF; Slack and webhook get a link and summary)
- **Retention-ceiling visibility** — the health dashboard charts the oldest record's age against the enforced retention limit, per data type

### Integrations

- **LevelBlue / USM Anywhere ingest** — pull LevelBlue (AlienVault) USM Anywhere alarms and events via one API credential per tenant, with no endpoint or agent changes
- **VMware NSX-T log coverage** — recognizes and classifies NSX-T log sources that had been flooding the unknowns bucket
- **Accurate Integration Health** — a raw log-server listener is no longer shown as an API-pull integration; only genuine integrations appear
- **Self-monitoring of ingestion quality** — automated monitoring flags data-classification anomalies and opens a tracked issue on its own
- **vCenter Broker telemetry parser** — added, queued for human sign-off before activation

### Reliability & Demo

- **Dependable operations dashboard** — the Conductor dashboard no longer hangs on endless spinners; it shows data fast, fills charts from the last known-good view, marks stale data, and offers Retry on failure
- **Realistic, story-driven demo** — a coherent scenario around a believable regional-healthcare organization facing technique-mapped attacks replaces random demo noise

### Trust & Quality

- **Tamper-proof cross-cluster threat intel** — shared threat-intel messages between clusters are cryptographically sealed end to end (body, not just labels), rolled out to keep mixed-version clusters working during upgrades
- **Verified access-control enforcement** — automated safeguards confirm every part of the platform enforces the correct permissions; remaining gaps were closed
- **New permissions reach upgraded customers** — new permissions (Certify, graph, automation) converge to already-deployed environments on upgrade, with no admin hand-editing of roles
- **Quality & multi-tenant isolation hardening** — a structured program closed test-suite blind spots (notably one-tenant-cannot-see-another isolation) plus coverage, mobile, accessibility, and resilience checks
- **Delivery-pipeline hardening** — recurring release-process risks turned into automated guardrails (git-enforced pre-commit hooks, static guards, contract tests), with the release test suite rescoped to run reliably in CI while exhaustive validation continues on live lab and beta appliances

## v1.0.0 (2026-06-30)

General-availability (GA) release. Builds on the 0.9.8 baseline with two new executive reports, a major step up in AI provider control and cost governance, a real collaboration layer, responsive mobile/tablet support, and a dedicated pre-1.0 full code review. Ships alongside **WitFoo Management Console 1.9.0**, **Conductor 1.8.0**, and **WFA 2.4.2**. **Upgrade recommended.**

### Reporting & Compliance

- **Vulnerability Management report** — hosts ranked by severity-weighted exposure, with host↔CVE drill-down, all server-paginated for large estates
- **Threat Model report** — your security controls mapped against the MITRE ATT&CK matrix from real audit findings, with per-cell drill-down and an optional AI narrative
- **Reporter improvements** — correct dark-theme charts, interactive drill-down and paging on the threat and vulnerability views, and a reorganized Reporter navigation

### AI & Automation

- **AI Provider Enhancement** — per-provider model catalogs with best-practice defaults and an economy tier; pre-save live model interrogation (your key is validated, never logged); and a `best`/`economy` AI profile that auto-routes each purpose to an appropriate model, preserving operator pins
- **Improved AI tooling** — the assistant can use read-only platform tools to ground answers in your live data
- **MCP Authentication** — optional per-organization bearer/API-key auth for the Model Context Protocol integration (default off; keys hashed at rest, shown once)
- **AI summary caching** — on-demand summaries (including Auditor findings) cached per organization to cut cost and latency

### Collaboration & Profile

- **User Profile** — self-hosted avatar upload, self-service password and locale, presence and author cards, and one-click "message a user"
- **Chat Upgrade** — file attachments, emoji reactions, and a more robust realtime connection
- **CyberGrid community** — share Work Units and Work Collections to the community directory, a within- and cross-cluster User Directory, and a durable, self-healing directory-submission pipeline that reports its true status

### Detection & Pipeline

- **Azure Email Security** — Microsoft Defender for Office 365 phishing email and phishing-click signals now produce Work Units
- **VMware NSX-T parsing** — NSX-T operational and degraded-service events classified and actionable instead of landing in unknown
- **Conductor visibility** — per-agent up/down/health for Beats agents, expanded Integration Health detail, the Conductor link hidden on non-Conductor nodes, and corrected Cisco Umbrella configuration fields
- **Search & collections** — Work Unit search on client IP across source and destination addresses; Work Collections on hostnames, URLs, file names, and file hashes; plus facet, Client-IP-search, and pagination fixes

### Platform & Operations

- **Mobile & tablet support** — responsive Analytics, Conductor, and Console UIs with drawer navigation and touch-friendly controls below desktop widths
- **Sign-in** — the login page defaults to SAML single sign-on when enabled (local login always reachable); Azure/SAML SSO reliability fixes
- **Health dashboard** — a Data Retention card showing the actually-enforced retention, a corrected host Total Memory gauge, and a per-node Cassandra health view
- **Improved automated monitoring** — telemetry redacted at the source under a configurable policy (`off`/`standard`/`strict`); opt-in, PII-free cluster-problem reporting
- **Console node management** — Analytics nodes managed from the Console with an accurate last-seen-based online/offline indicator

### Infrastructure & Hardening

- **Pre-1.0 full code review** — external-dependency and vulnerability verification, Cassandra optimization (including a 5.0.8 upgrade with a per-node health monitor), an adversarial re-review of the entire 0.9.8→1.0.0 change set, deeper test and docker-log coverage, documentation accuracy, and an expanded certification curriculum
- Continued supply-chain and CI security-gate hardening (secret scanning, static analysis, dependency and image scanning, log-injection and SSRF call-site gates)

## v0.9.8 (2026-06-23)

Operational-resilience, AI-cost, and pipeline-coverage release with broad security hardening. Ships alongside **WitFoo Management Console 1.8.0**, **Conductor 1.7.0**, and **WFA 2.3.0**. **Upgrade recommended.**

### Security & Hardening

- Resolved a class of log-injection and outbound-request (anti-rebinding / SSRF) hardening findings across the platform and the management console; outbound connections now validate the destination host before any credentials are attached
- Tightened per-route access controls across the incident and configuration APIs, with a build-time guard that fails the pipeline on any newly ungated route
- Stronger TLS/certificate validation on appliance-to-Conductor health checks
- Refreshed dependency tree and supply-chain updates, plus new recurring-vulnerability prevention gates (secret scanning, app/image SAST, signed images and SBOMs) added to the build pipeline
- Azure / SAML single sign-on reliability — assertion-replay handling bounded to the provider acceptance window and request-binding fixes, so a valid login is no longer falsely rejected as a replay

### Operational Resilience

- **Compliance Readiness no longer strands at 0% after a redeploy** — a snapshot guard preserves the last healthy compliance figure and a startup probe waits for data readiness before regenerating, so a restart can never serve a collapsed 0% snapshot
- **AI cost optimization** — Anthropic prompt caching, a cheaper model tier for report and on-demand summaries, and demo-mode containment dramatically cut AI spend
- **Production Dashboards** — Custom Dashboard widgets now show real production data or an explicit empty state, never placeholder sample data in a live tenant (sample data renders only in the editor preview or under demo mode)
- **Monorepo consolidation** — one codebase with change-detected image builds for faster, more reliable releases and independent per-product versioning (no customer-visible behavior change)
- WFA broker-startup deadlock resilience — a node can no longer get permanently wedged during service initialization; the startup gate is now bounded, observable, and self-creating of its broker objects

### Conductor & Pipeline

- **Beats agent up/down/health tracking** — a new **Agents** page in Conductor, up/down/stale transition alerting, and agent status forwarded to the Console node view
- **Pipeline self-heal** — a parser present in the build but not yet enabled can no longer ship "dark"; absent first-party parsers auto-enable while respecting explicit operator disables (`PARSER_RECONCILE`)
- **Fleet-wide Parser Audit** — RFC 5424-compliant severity enforced at a single chokepoint, a five-way detection-metadata cross-reference quality gate, 50 product-mapping corrections, and broader Microsoft Graph / Defender coverage
- **New Microsoft parsers and parsing fixes** — Microsoft Defender Vulnerability Management, Azure security / Graph sign-ins, directory audits, and Defender incidents now parse instead of landing in unknown
- **New log auto-parsers** — apt daily, Microsoft Identity Protection, and ModemManager
- Resolved a Conductor-pipeline noise issue (idle Beats keep-alive connections) and a pipeline-wedge condition

### Features & UX

- **Reliable, consistent faceted search** — one unified filter sidebar across Signals, Nodes, Edges, Work Units, and Work Collections, with facet counts that match the result rows
- **Assign a Work Unit (or individual response tasks) to an AI Agent** — full AI autonomy with live investigation progress: the AI sets the unit to Investigating, works the playbook step-by-step, and closes the ticket (human attestation is preserved — the AI never silently attests a task)
- **Reporter ROI corrected** — ROI is now Total Protection Value ÷ Annual Security Spend (including insurance coverage), so zero-incident ROI is non-zero
- **AI Chat fixes** — work-unit context now reaches the assistant, the chat pop-out works, and direct messages resolve member names and authenticate correctly
- **Human-friendly names everywhere** — node Products and Frameworks show real names, the work-unit activity feed shows status labels and user names, and the "Configuration Auditor" is renamed **Auditor**
- **Signal Search from a node's detail view** — pivot on a stable node id to find all of a node's signals, regardless of changing IPs
- **Auditor UX fixes** — the filter list is reactive, the findings pager works, and the loading spinner renders inline in the correct place
- **Configuration Auditor connector fixes** — Microsoft 365, Google Cloud, and OCI connectors now add and test successfully
- Enhanced work-unit activity notes and per-task notes / evidence
- **Licensing improvements** — licensing.witfoo.com reliability, Dev Mode hidden in non-development deployments, and CyberGrid licensing management
- **User Profile build-out** — the account profile page is populated and integrated with chat

### Console

- **Configuration Generator + `wfa fetch`** — pre-build a customer node configuration and publish a one-time URL; the customer runs `wfa fetch <url>` for zero-touch provisioning (config encrypted at rest, single-use token, 72h TTL)
- **Deeper remote management of Analytics/Data nodes** — start / stop / restart / upgrade / pull-images from the Console, with Cassandra data-node safety guards (destructive actions on a data-bearing node require explicit confirmation)
- The Console now surfaces Beats agent status forwarded from connected appliances

### Upgrade Notes

- No database migration; no breaking API changes
- New optional operator settings: `PARSER_RECONCILE` (parser self-reconcile policy) and `BROKER_HEALTH_GATE_WARN_SECONDS` (broker-health startup-gate warning threshold). `WF_DEMO_MODE` now also gates AI spend on demo deployments

### Resolved issues

Issues #160, #207, #208, #209, #211, #212, #213, #214, #215, #216, #217, #218, #219, #220, #221, #222, #223, #224, #225, #226, #228, #229, #230, #231, #232, #238, #239, #244, #245, #246, #247, #249, #260, #265, #266, #267, #269, #283 (plus the #203 / #205 / #206 auto-parser additions).

## Console 1.8.0 (2026-06-23)

- **Configuration Generator + `wfa fetch`** — pre-built one-time node configuration for zero-touch provisioning (#244)
- **Remote node management** — lifecycle and upgrade actions on connected Analytics/Data nodes with data-node safety guards (#160)
- Beats agent status forwarded from appliances now shown on the node view (#269)

## Conductor 1.7.0 (2026-06-23)

- **Beats agent tracking** — Agents page, up/down/stale alerting, and Console forward (#269)
- **Pipeline self-heal** — parsers can no longer ship dark; absent first-party parsers auto-enable (#245/#246)
- **Parser Audit** — RFC 5424 severity, a metadata cross-reference quality gate, 50 mapping corrections, and broader Microsoft Graph / Defender coverage (#266)
- New Microsoft parsers and parsing fixes (Defender Vulnerability Management, Azure sign-ins, directory audits, Defender incidents) and new auto-parsers (apt daily, Microsoft Identity Protection, ModemManager) (#203/#205/#206/#208/#245/#246/#247)
- Idle Beats keep-alive connection noise fixed (#247)

## WFA 2.3.0 (2026-06-23)

- Service-init deadlock resilience — a node can't get permanently wedged at startup; the broker-health gate self-creates its broker objects, fails open on best-effort objects, and is bounded + observable (`BROKER_HEALTH_GATE_WARN_SECONDS`) (#283)
- Bounded broker connect across broker-dependent services, so a broker outage self-heals instead of stranding a service dark (#267)
- Console node-status forward now carries a bounded Beats agent summary (#269)
- common v1.5.39; apt/rpm publishing restored

## Conductor 1.5.0 (2026-02-22)

- **Notification System** — Email, Slack, and webhook alerting with rule-based event routing, cooldown, and delivery history
- **LDAP Security Hardening** — Injection fix (CWE-90), TLS 1.2+ enforcement, connection timeouts
- **Per-Exporter Predicate Filtering** — Shared predicate engine with UI forms on all exporter settings
- **18 New Integrations** — Tenable, Cortex XDR, Proofpoint, Netskope, Okta, LimaCharlie, Mimecast, Deep Instinct, Druva, Cisco Umbrella/Meraki/Duo/AMP, and more
- **6 Auto-Generated Parsers** — GreyNoise, Kafka, WitFoo Console, WitFoo Intel, Nginx, Filebeat
- **Performance Benchmarks** — Benchmarks across all pipeline services (Splunk HEC, STIX, JetStream, flow functions)
- **UI Improvements** — Settings icons, Beacon Yellow arrows, favicon, improved defaults

## Console 1.5.0 (2026-02-22)

- **Disconnected Network Support** — Self-hosted IBM Plex fonts for air-gapped deployments
- **CI Quality Gates** — Race detection, security scanning, release branch handling

## v0.9.7 (2026-05-29)

Security-hardening and operational-resilience release. Consolidates the hardening work delivered across the 0.9.4–0.9.7 line into a single recommended upgrade.

### Security & Hardening

- Tenant isolation — active organization is derived from the verified session, never from client-supplied request parameters; SAML/LDAP user lookups are scoped per-organization
- Conductor management UI reachable only through the authenticated reverse proxy; internal trust headers gated behind an IP allowlist (`WF_TRUSTED_PROXIES`)
- Mandatory secret-key enforcement — `JWT_SECRET` and `AUTH_CONFIG_ENCRYPTION_KEY` fail closed instead of falling back to insecure defaults; stored credentials and AI-provider keys encrypted at rest under a consolidated XChaCha20-Poly1305 key
- WebSocket authorization enforced before upgrade; origin checking tightened across real-time endpoints
- Attachment and user-rendered content hardened against script-injection (XSS)
- Input encoding and bounded query limits; log sanitization and on-disk path containment

### Operational Resilience & Self-Healing

- Startup-race sweep — service initialization moved to a level-triggered readiness model, eliminating a class of startup deadlocks
- Container environment-drift self-heal — a running container missing a newly required environment variable after a WFA upgrade is recreated automatically within ~60 seconds
- Missing-container self-heal — a configured-but-absent container is recreated automatically; image pulls fall back to a present local image during a brief registry outage

### Conductor & Pipeline

- New opt-in redaction pipeline tokenizes PII before export to downstream SIEMs (requires `REDACTION_MASTER_KEY`)
- Conductor WebSocket/API TLS and header-auth fix for AIO+Conductor deployments
- Tenable.io REST asset-inventory parser

### Infrastructure

- Go 1.26.3 and refreshed dependency tree — 22 CVEs closed
- WFA bumped to v2.1.17
- New build-discipline guardrails and three operator runbooks (build discipline, submodule pin management, environment-variable drift recovery)
- Encryption/secret-key configuration reference added

### Upgrade Notes

- `JWT_SECRET` and `AUTH_CONFIG_ENCRYPTION_KEY` are required on the API and Incident Engine (WFA generates them automatically; standalone/Compose deployments use `scripts/dev/generate-secrets.sh`)
- No database migration; no breaking API changes

## WFA 2.1.17 (2026-05-29)

- Container environment-drift self-heal and missing-container self-heal
- Startup-race hardening across agent and pipeline services
- Generated CA preserved across upgrades; `SSL_CERT_FILE` supplied to the reverse proxy for Conductor WebSocket TLS
- Go 1.26.3, common v1.5.20, dependency CVE remediations

## v0.9.3 (2026-03-12)

### Features

- SAML onboarding wizard with provider presets (Azure AD, Okta, OneLogin, PingIdentity)
- SAML wizard ported to conductor-ui and console-ui
- Microsoft Sentinel integration connector
- SAML auth fallback with redirect loop detection
- Te Reo Maori (mi) locale -- 7th supported language
- AI language awareness for summaries and chat
- Classification rules management page
- Features settings page
- SP key pair auto-generation for SAML
- SAML configuration test endpoint

### Bug Fixes

- 25 pre-release bug fixes (PR189) across AI, signals, playbooks, CyberGrid, and conductor
- Work unit layout consolidated from 10 to 5 tabs
- Production deployment hardening (HSTS, trusted proxies, security headers)

### Infrastructure

- Cassandra seeder consolidation (DDL/DML separation)
- WFA v2.0.36 with dependency updates
- 89 i18n keys across 7 locales for SAML wizard

## dev (Initial Release)

- Initial documentation site created
- Getting Started guide with architecture diagrams
- User Guide for all 6 modules (Signals, Graph, Observer, Reporter, CyberGrid, Health)
- Admin Guide with RBAC permissions reference
- API Reference for 150+ endpoints
- AI & MCP documentation
- Deployment guide for Docker, WFA, and Conductor
- Reference section with permissions, roles, and environment variables
