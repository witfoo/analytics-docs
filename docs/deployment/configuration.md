# Configuration

WitFoo Analytics is configured through environment variables in `docker/.env`.

## Core Variables

| Variable | Default | Description |
| --- | --- | --- |
| `CASSANDRA_HOST` | `cassandra` | Cassandra hostname |
| `NATS_URL` | `nats://nats:4222` | NATS connection URL |
| `JWT_SECRET` | (required) | Secret key for JWT signing |
| `ORG_ID` | `witfoo` | Organization identifier |

## Service Ports

| Variable | Default | Service |
| --- | --- | --- |
| `REVERSE_PROXY_PORT` | `8080` | Web UI and API access |
| `API_PORT` | `8090` | API gateway |
| `IE_PORT` | `8082` | Incident Engine |
| `UI_PORT` | `5173` | SvelteKit dev server |

## Security Variables

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | HS256 signing key for JWT tokens |
| `AUTH_CONFIG_ENCRYPTION_KEY` | AES-256-GCM key for credential encryption (base64) |
| `ANALYTICS_SECRET` | HMAC-SHA256 shared secret for Conductor auth |

## Feature Flags

| Variable | Default | Description |
| --- | --- | --- |
| `WF_LICENSE` | (empty) | Intel API license key for framework sync |
| `VITE_UI_MODULES` | `all` | UI module visibility: `all`, `search_only`, `search_observer` |
| `GRAFANA_REMOTE_WRITE_URL` | (empty) | Enable Prometheus remote write to Grafana |

## Cassandra Tuning

| Variable | Default | Description |
| --- | --- | --- |
| `CASSANDRA_HEAP` | `1G` | JVM heap size |
| `CASSANDRA_NEWSIZE` | `200M` | JVM new generation size |
| `DATA_NODE_HOSTS` | (empty) | External Cassandra hosts for processing nodes |

## Example .env

```bash
JWT_SECRET=your-secret-key-here
ORG_ID=my-org
CASSANDRA_HOST=cassandra
NATS_URL=nats://nats:4222
AUTH_CONFIG_ENCRYPTION_KEY=base64-encoded-32-byte-key
```
