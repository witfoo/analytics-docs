# Environment Variables

Complete reference for WitFoo Analytics environment variables.

## Required

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | HS256 signing key for the session JWT. Must be identical across the reverse proxy, API, Incident Engine, and dispatcher. **Fail-closed**: the API and Incident Engine refuse to start on an empty or known-default value. |

!!! warning "Encryption and secret keys are fail-closed"
    On WFA appliances, `JWT_SECRET` and `AUTH_CONFIG_ENCRYPTION_KEY` are generated automatically and injected into every container. For standalone or Docker Compose deployments, generate them with `scripts/dev/generate-secrets.sh` (or `openssl rand`). The API and Incident Engine **will not start** with a missing or default secret rather than fall back to an insecure default. If a container crash-loops on a missing key right after a WFA upgrade, WFA 2.1.13+ self-heals it within ~60 seconds; on older WFA, run `systemctl restart wfad`.

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
| `AUTH_CONFIG_ENCRYPTION_KEY` | (empty) | XChaCha20-Poly1305 master key (base64-encoded) that encrypts auth secrets — LDAP bind passwords, SAML private keys, TLS keys — and AI-provider API keys at rest. The single consolidated key as of v0.9.7. **Fail-closed**: the API and Incident Engine refuse to start when AI configurations exist but this key is absent. WFA auto-generates it deterministically. |
| `AI_ENCRYPTION_KEY` | (empty) | **Legacy / decommissioning.** Pre-v0.9.7 AES-GCM key, retained only for one-time re-encryption of older ciphertext under `AUTH_CONFIG_ENCRYPTION_KEY`. New deployments do not need it. |
| `REDACTION_MASTER_KEY` | (empty) | HKDF master key for the optional Conductor redaction pipeline (deterministic PII tokenization plus an encrypted at-rest alias store). Required only when redaction is enabled; must be stable across the appliance fleet. |
| `SSL_CERT_FILE` | `/certs/ca-bundle.crt` | Local CA bundle the reverse proxy trusts for Conductor WebSocket/API TLS. Injected by WFA on Conductor-bearing nodes. |
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
