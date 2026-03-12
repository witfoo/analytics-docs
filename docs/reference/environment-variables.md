# Environment Variables

Complete reference for WitFoo Analytics environment variables.

## Required

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | HS256 signing key for JWT tokens |

## Core

| Variable | Default | Description |
| --- | --- | --- |
| `ORG_ID` | `witfoo` | Organization identifier |
| `CASSANDRA_HOST` | `cassandra` | Cassandra hostname |
| `NATS_URL` | `nats://nats:4222` | NATS server URL |

## Service Ports

| Variable | Default | Service |
| --- | --- | --- |
| `REVERSE_PROXY_PORT` | `8080` | Reverse proxy |
| `API_PORT` | `8090` | API gateway |
| `IE_PORT` | `8082` | Incident Engine |
| `UI_PORT` | `5173` | SvelteKit |
| `AI_PORT` | `8003` | Artifact Ingestion |

## Security

| Variable | Default | Description |
| --- | --- | --- |
| `AUTH_CONFIG_ENCRYPTION_KEY` | (empty) | AES-256-GCM encryption key for encrypting LDAP/SAML credentials at rest (base64-encoded) |
| `ANALYTICS_SECRET` | (empty) | HMAC-SHA256 secret for Conductor auth |
| `WF_TRUSTED_PROXIES` | (empty) | Comma-separated list of trusted proxy IPs for forwarded header processing |
| `WF_JWT_SECRET` | (auto) | Shared JWT secret for Conductor SSO; auto-generated when not set |

## Feature Flags

| Variable | Default | Description |
| --- | --- | --- |
| `WF_LICENSE` | (empty) | Intel API license for framework sync |
| `VITE_UI_MODULES` | `all` | UI module visibility |
| `REVERSE_PROXY_MODE` | `false` | Enable proxy header trust for Conductor UI |
| `WF_DEMO_MODE` | `false` | Enable demo mode with sample data and guided onboarding |

## Monitoring

| Variable | Default | Description |
| --- | --- | --- |
| `GRAFANA_REMOTE_WRITE_URL` | (empty) | Prometheus remote write endpoint |
| `GRAFANA_INSTANCE_ID` | (empty) | Grafana Cloud instance ID |
| `GRAFANA_API_KEY` | (empty) | Grafana Cloud API key |

## Cassandra Tuning

| Variable | Default | Description |
| --- | --- | --- |
| `CASSANDRA_HEAP` | `1G` | JVM heap size |
| `CASSANDRA_NEWSIZE` | `200M` | JVM new generation size |
| `DATA_NODE_HOSTS` | (empty) | External Cassandra hosts (comma-separated) |

## Localization

| Variable | Default | Description |
| --- | --- | --- |
| `default_locale` | `en` | Default locale for AI background tasks such as playbook analysis (set via business settings) |
