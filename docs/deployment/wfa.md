# WFA Deployment

The WitFoo Appliance (WFA) CLI provides automated deployment and management of WitFoo Analytics.

## Installation

```bash
wfa analytics install --role <role>
```

### Available Roles

| Role | Description |
| --- | --- |
| `aio` | All-in-One: all analytics services |
| `aio-conductor` | AIO + Conductor signal pipeline |
| `data-node` | Dedicated Cassandra database node |
| `processing-node` | Dedicated processing (external Cassandra) |

## Configuration

```bash
wfa analytics configure
```

The interactive wizard configures:

- **Retention** — Data retention periods
- **UI Modules** — Which modules to enable (all, search-only, search+observer)
- **CyberGrid** — Intelligence feed settings
- **Clustering** — Multi-node Cassandra configuration

## Management Commands

| Command | Description |
| --- | --- |
| `wfa analytics start` | Start all services |
| `wfa analytics stop` | Stop all services |
| `wfa analytics status` | Show service status |
| `wfa analytics upgrade` | Upgrade to new version |

## Current Version

The latest WFA release is **v2.1.17**. Highlights:

- **Container self-healing** — a running container whose environment has drifted from the current node specification (for example, a newly required encryption key added by an upgrade) is recreated automatically within the ~60-second reconcile loop; a configured-but-absent container is likewise recreated, and image pulls fall back to a present local image during a brief registry outage.
- **Startup-race hardening** — service initialization uses a level-triggered readiness model, eliminating a class of startup deadlocks.
- **Certificate stability** — the generated local CA is preserved across upgrades (no trust break), and the reverse proxy is supplied with the local CA bundle for Conductor WebSocket/API TLS.
- **Supply chain** — Go 1.26.3 and refreshed dependencies (22 CVEs closed).

## Authentication Configuration

WFA deployments support SAML single sign-on configuration through the built-in wizard, available in both conductor-ui and console-ui settings pages. The wizard provides provider presets for Azure AD, Okta, OneLogin, and PingIdentity with automatic SP key pair generation.

For detailed SAML setup instructions, see [Authentication Settings](../admin-guide/settings/authentication.md).

## Hardware Validation

The `install` command validates hardware against the role's minimum requirements before proceeding:

| Role | Min CPU | Min RAM | Min Disk |
| --- | --- | --- | --- |
| AIO | 4 cores | 8 GB | 50 GB |
| AIO + Conductor | 8 cores | 16 GB | 100 GB |
| Data Node | 4 cores | 8 GB | 200 GB |
| Processing Node | 4 cores | 8 GB | 50 GB |
