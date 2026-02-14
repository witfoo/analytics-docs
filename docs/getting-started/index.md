# Getting Started

WitFoo Analytics is a security operations platform that transforms raw security data into actionable intelligence. It ingests artifacts from your infrastructure, correlates them into incidents, and provides comprehensive reporting, compliance tracking, and threat intelligence capabilities.

## Key Capabilities

- **Artifact Ingestion** — Receive security events from firewalls, IDS/IPS, endpoint agents, and SIEM tools
- **Incident Correlation** — Automatically group related artifacts into incidents using graph-based analysis
- **Compliance Readiness** — Track compliance against CIS CSC, NIST CSF, and other frameworks
- **Threat Intelligence** — Subscribe to and publish threat intelligence feeds via CyberGrid
- **Executive Reporting** — Generate reports on tool effectiveness, cost/savings, and security posture

## Quick Start

1. **[Install](installation.md)** — Deploy WitFoo Analytics using Docker Compose
2. **[First Login](first-login.md)** — Access the web UI and create your first user
3. **[Architecture](architecture.md)** — Understand the service architecture and data flow
4. **[Deployment Roles](deployment-roles.md)** — Choose the right deployment topology for your environment

## System Requirements

| Component | Minimum | Recommended |
| --- | --- | --- |
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Disk | 50 GB SSD | 200+ GB SSD |
| Docker | 24.0+ | Latest stable |
| Docker Compose | v2.20+ | Latest stable |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

!!! tip "All-in-One Deployment"
    For evaluation and small deployments, the AIO (All-in-One) role runs all services on a single machine. See [Deployment Roles](deployment-roles.md) for production topologies.
