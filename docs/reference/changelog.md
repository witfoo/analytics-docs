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
