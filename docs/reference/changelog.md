# Changelog

Version history for WitFoo products.

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

### Operational Resilience

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
