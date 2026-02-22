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

## dev (Initial Release)

- Initial documentation site created
- Getting Started guide with architecture diagrams
- User Guide for all 6 modules (Signals, Graph, Observer, Reporter, CyberGrid, Health)
- Admin Guide with RBAC permissions reference
- API Reference for 150+ endpoints
- AI & MCP documentation
- Deployment guide for Docker, WFA, and Conductor
- Reference section with permissions, roles, and environment variables
