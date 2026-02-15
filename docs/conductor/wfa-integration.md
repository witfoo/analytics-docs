# WFA Agent Architecture

WFA (WitFoo Agent) is the systemd daemon that orchestrates all Conductor containers on a WitFoo Appliance. It manages the complete container lifecycle from image management through runtime monitoring.

## Container Lifecycle

WFA follows a deterministic startup sequence:

1. **Pull Images** — Check the configured container registry for updated images, comparing SHA256 digests
2. **Create Containers** — Configure each container with environment variables, volume mounts, port mappings, and network settings
3. **Start in Dependency Order** — Launch containers respecting inter-service dependencies
4. **Monitor Health** — Continuously check container health and restart failed services

### Dependency Order

```
broker-edge
    ├── signal-server
    ├── signal-client
    ├── signal-parser
    │       └── artifact-filter
    │               └── artifact-exporter
    └── conductor-ui
```

Broker Edge must be healthy before any downstream service starts. The WFA container manager polls every 60 seconds for image updates.

## Auto-Update Mechanism

When `auto_update` is enabled in `node.json`:

- WFA configures Ubuntu's `unattended-upgrades` to include the WitFoo apt repository
- System packages (including WFA itself) are updated hourly via systemd timer overrides
- Container images are checked every 60 seconds against the registry
- Updated images are pulled and containers are recreated automatically

!!! note
    Container image updates are seamless — WFA compares SHA256 digests and only recreates containers when the image has changed. The startup dependency order is maintained during updates.

## Certificate Management

WFA manages TLS certificates with three source types:

| Source | Description |
|--------|-------------|
| **Embedded** | Default WitFoo certificates compiled into the WFA binary |
| **Customer** | Customer-provided certificates configured in `node.json` |
| **Generated** | Auto-generated certificates for development environments |

Certificate precedence: Customer certificates override embedded ones. The `ca-bundle.crt` is automatically generated combining all CA certificates.

All containers mount `/witfoo/certs` as `/certs` (read-only).

## Monitoring Integration

When `export_metrics` is enabled, WFA deploys a Grafana Agent container that:

- Scrapes Prometheus metrics from pipeline services
- Forwards metrics to Grafana Cloud
- Streams service logs and journal entries

When `local_metrics` is enabled, WFA additionally deploys:

- **Prometheus** (port 9090) — Local metrics collection with 24-hour retention
- **Grafana** (port 3000) — Local dashboards for pipeline visualization

## Docker System Maintenance

After all containers are confirmed running, WFA runs a Docker system prune in the background to reclaim disk space from stopped containers, unused networks, and old images.