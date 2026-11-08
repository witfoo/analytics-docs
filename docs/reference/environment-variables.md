# Environment Variables

Reference for the WitFoo Analytics 1.2.0 environment variables that an operator sets.

On a WFA-managed appliance, WFA builds each container's environment, and you change behaviour through `node.json` (see [WFA node.json keys](#wfa-nodejson-keys) below). The variables on this page are set directly only on Docker Compose and standalone stacks, in the root `.env` file of the checkout (`docker/.env` is a link to it) or in the shell you run `docker compose` from.

## Required

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | The secret the session key is derived from. Must be identical across the reverse proxy, api, incident-engine and dispatcher. **Fail-closed**: the api, incident-engine and dispatcher refuse to start when it is empty. |
| `AUTH_CONFIG_ENCRYPTION_KEY` | The key that seals the secrets stored in the database: LDAP bind passwords, SAML private keys, TLS private keys, AI-provider API keys, notification-channel configurations, audit-connector credentials and Vrax connection credentials. 32 random bytes, base64 (`openssl rand -base64 32`). **Required from 1.2.0, with no default**: every `docker compose` command refuses to run until it is set, and the api and incident-engine refuse to start with a value that is not 32 bytes of base64, or with the value earlier compose files shipped as a default. Set it on the api and incident-engine. |
| `WF_JWT_SECRET` | Shared secret for Conductor single sign-on. The AIO plus Conductor compose file refuses to run until it is set (`openssl rand -hex 32`). |

| Variable | Default | Description |
| --- | --- | --- |
| `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` | (empty) | Comma-separated base64 32-byte keys that `AUTH_CONFIG_ENCRYPTION_KEY` replaced. Values sealed under them stay readable, and incident-engine rewrites them under the current key. Set it on the api **and** incident-engine, to the same value. |

!!! warning "Encryption and secret keys are fail-closed"
    On WFA appliances WFA supplies `JWT_SECRET` and `AUTH_CONFIG_ENCRYPTION_KEY` to every container that needs them. Do not edit them by hand.

    On Docker Compose and standalone stacks, the launch scripts generate a key and write it to `.env` when none is set. On more than one node, every node that runs the api or incident-engine against the same Cassandra cluster needs the same `AUTH_CONFIG_ENCRYPTION_KEY` and `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS`: copy both from the first node's `.env` before a second node's first start. A stack that was started from an earlier compose file and never set a key of its own needs a one-time step; see [Upgrading to 1.2.0](upgrade-1.2.0.md).

    The key is part of your data. Back it up whenever you back up the database, and store the two apart.

## Core

| Variable | Default | Description |
| --- | --- | --- |
| `ORG_ID` | `development` | Organization identifier used in metric labels |
| `CASSANDRA_HOSTS` | `cassandra:9042` | Cassandra contact points |
| `NATS_URL` | `nats://nats:4222` | NATS server URL |

## Published addresses (Docker Compose)

There are no per-service port variables. The compose files publish fixed ports, on one of two host addresses:

| Variable | Default | What it publishes |
| --- | --- | --- |
| `LISTEN_IP` | `0.0.0.0` in the compose files (the example `.env` sets `127.0.0.1`) | The services that must be reachable from outside: the reverse proxy (443, 8081), the artifact receiver (8090, and 8443 with TLS) and Cassandra (9042, 9160). Restrict Cassandra's ports at the host firewall. |
| `INTERNAL_LISTEN_IP` | `127.0.0.1` | The internal services: api (8080), incident-engine (8082), dispatcher (8003), UI (3000), NATS (4222, 8222), the Conductor broker edge (4223, 8223), Prometheus (9090) and Grafana (3001) |

Before 1.2.0, `LISTEN_IP` published every service. See [Docker Compose Reference](../deployment/docker-compose.md) for the full port list of each compose file.

## Edge, proxies and origins

| Variable | Service | Default | Description |
| --- | --- | --- | --- |
| `WF_TRUSTED_PROXIES` | reverse proxy | (empty) | Comma-separated addresses or CIDRs of the load balancers whose `X-Forwarded-For` the edge believes. With it unset, a TLS edge trusts no forwarder. An edge without TLS, or in LB mode, trusts the private ranges `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` and `127.0.0.1` for one more release, with a startup WARN. `X-Real-IP` is never read. Entries wider than /8 (IPv4) or /32 (IPv6), and entries that do not parse, are dropped with an ERROR. Behind a load balancer, set it to the load balancer's own address, not a private-network range, before you enable the MCP exposure listener. A list that includes `10.0.0.0/8`, `172.16.0.0/12` or `192.168.0.0/16`, or an entry that overlaps the proxy's own Docker network, is accepted with a WARN, but every client behind the load balancer then shares one failed-authentication count on `/mcp`. |
| `WF_ALLOWED_ORIGINS` | reverse proxy | (empty = same origin only) | Comma-separated origins allowed to open WebSocket connections through the proxy (`/ws/chat`, `/ws/graph`, `/ws/events` and the Conductor WebSocket routes). A refused origin gets `403` `{"error":"Origin not allowed"}`. |
| `WF_ALLOWED_ORIGINS` | dispatcher | (empty = same origin only) | Comma-separated origins allowed to call `POST /mcp`. A request that carries an `Origin` header must match, whatever credential it presents. A browser page that calls `/mcp` must be listed even when the appliance serves it. Clients that send no `Origin` need no entry. |
| `TLS_ENABLED` | reverse proxy | `true` in the compose files | Turns HTTPS on when exactly `true` |
| `LB_MODE` | reverse proxy | (unset) | SSL load balancer mode when exactly `true`: HTTP only on `LB_LISTEN_PORT` |
| `LB_LISTEN_PORT` | reverse proxy | `80` | Port to listen on in LB mode |

## Security

| Variable | Default | Description |
| --- | --- | --- |
| `AI_ENCRYPTION_KEY` | (empty) | **Legacy.** The key of an earlier AI-key format, kept only so older stored values stay readable while they are re-sealed under `AUTH_CONFIG_ENCRYPTION_KEY`. New deployments do not need it. |
| `REDACTION_MASTER_KEY` | (empty) | HKDF master key for the optional Conductor redaction pipeline. Required only when redaction is enabled; must be stable across the appliance fleet. |
| `SSL_CERT_FILE` | `/certs/ca-bundle.crt` | Local CA bundle the reverse proxy trusts for Conductor WebSocket and API TLS. Injected by WFA on Conductor-bearing nodes. |
| `ANALYTICS_SECRET` | (empty) | HMAC-SHA256 secret for Conductor authentication |
| `SECRET_KEY` | (unset) | Conductor UI and Console UI session key. Leave it unset, and each program keeps a key of its own in `.secret_key` beside its database (keep that file with the database). Or set 64 hexadecimal characters, for example the output of `openssl rand -hex 32`. From 1.2.0 both programs refuse to start with a value earlier releases or example files carried, or with a value that is not a usable key. |

`NOTIFICATION_ENCRYPTION_KEY` is removed in 1.2.0. Notification channels are sealed with `AUTH_CONFIG_ENCRYPTION_KEY`.

## Authentication

| Variable | Default | Description |
| --- | --- | --- |
| `AUTH_PUBLIC_REGISTRATION_ENABLED` | `false` | Turns on public self-registration (`POST /api/v1/auth/register`), limited to 10 requests an hour per client |
| `AUTH_PUBLIC_REGISTRATION_DOMAINS` | (empty) | Comma-separated `<email-domain>=<org_id>` pairs. An account is created only when the address's domain is mapped, in the mapped organization, and inactive until an administrator enables it. Matched exactly, no wildcards. **Fail-closed**: one malformed entry rejects the whole map, and registration creates no account. |

## MCP

On a WFA appliance (WFA 2.5.1 or later), WFA sets the first five from `node.json` fields you set: `mcp_http_enabled`, `mcp_public_url`, `mcp_oauth_ui_url`, `mcp_oauth_cimd`, and `mcp_exposure_enabled` for `MCP_EXPOSURE_PORT`. The `MCP_RELAY_*` variables come from fields that only `wfa mcp-relay` writes. `LICENSE_CHECK_INTERVAL` is not a `node.json` field. See [MCP Configuration](../ai/mcp/configuration.md).

| Variable | Service | Default | Description |
| --- | --- | --- | --- |
| `WF_MCP_HTTP_ENABLED` | dispatcher | `false` | Serves the Streamable HTTP MCP transport at `POST /mcp`. Unset, `/mcp` does not exist (`404`). |
| `MCP_PUBLIC_URL` | api, dispatcher | (unset) | The MCP URL as an app is given it: `https`, a host, the path `/mcp` exactly, in canonical form (lowercase host, no default port, no trailing slash). It is the token audience; the issuer is this URL without `/mcp`. Needed for app sign-in. |
| `MCP_OAUTH_UI_URL` | api, dispatcher | (unset) | The `https` address of the analytics UI, where a signed-in user approves an app. The authorization endpoint is this URL plus `/ui/oauth/authorize`. Needed for app sign-in. |
| `MCP_OAUTH_CIMD` | api, dispatcher | `on` | `on` or `off`. `off` means only pre-registered clients can sign in; set it where the appliance's only egress is a corporate proxy. |
| `MCP_EXPOSURE_PORT` | reverse proxy | (unset, off) | Port of the MCP exposure listener, which serves `/mcp` and the app sign-in endpoints and nothing else. WFA uses 8444. |
| `MCP_RELAY_ENABLED` | reverse proxy, api | (absent) | `true` while the AI-connector relay runs. Written by WFA only. |
| `MCP_RELAY_HANDLE` | reverse proxy, api | (absent) | The relay address handle. Written by WFA only. |
| `MCP_RELAY_CREDENTIAL` | reverse proxy | (absent) | The relay tunnel credential. Written by WFA only. |
| `MCP_RELAY_REACK_REQUIRED` | api | (absent) | `true` when the relay is stopped until its notice is acknowledged again. Written by WFA only. |
| `LICENSE_CHECK_INTERVAL` | incident-engine | `1h` | How often the appliance checks its licence. A licence change reaches MCP within this interval, plus up to 30 seconds, plus up to 60 seconds for an idle WebSocket. |

App sign-in is available only when both `MCP_PUBLIC_URL` and `MCP_OAUTH_UI_URL` are set and valid. An invalid value is logged as an error and read as unset. The relay variables are written only by `wfa mcp-relay`; see [AI-connector relay](../ai/mcp/relay.md).

## Artifact receiver capacity

These variables set the limits of artifact-ingestion. A WFA appliance has no setting for the `WF_CONN_` variables in 1.2.0.

| Variable | Default | Description |
| --- | --- | --- |
| `WF_INGEST_PROFILE` | (unset) | `small` (body 32 MiB, in-flight budget 128 MiB, 1,024 stream connections) or `default` (body 64 MiB, budget 256 MiB). Unset, the memory budget chooses. The receiver logs the profile it runs, and why, at start. |
| `WF_MEMORY_BUDGET_MB` | (unset) | The container's memory budget in MiB. A value below 768 selects the small profile when `WF_INGEST_PROFILE` is unset; an appliance with less than about 18.5 GiB of host memory runs the small profile. WFA sets it. |
| `WF_INGEST_MAX_MESSAGE_MIB` | `9.5` | Largest WebSocket message in MiB. 9.5 MiB is the largest artifact the message bus takes, so a higher value is ignored with a note in the log. |
| `WF_CONN_MAX` | `1024` | Most connections the plain listener holds at once (16 to 65536) |
| `WF_CONN_MAX_TLS` | `512` | The same for the TLS listener |
| `WF_CONN_MAX_PER_SOURCE` | `128` | Most connections one source address (an IPv6 address counts as its /64) holds on the plain and TLS listeners |
| `WF_CONN_TRUSTED` | loopback only | Comma-separated CIDRs and addresses exempt from the per-source share. List a NAT or load balancer address that many Conductors share. |

With a memory budget set, the receiver lowers its connection caps from it: 1,024 plain and 512 TLS once the budget reaches about 1.7 GiB. Where more than about 40 to 60 Conductors reach the receiver from one address, they share 128 connections. On a WFA appliance, give them more than one address or more than one receiver.

## Processing

| Variable | Service | Default | Description |
| --- | --- | --- | --- |
| `GRAPH_PROCESSOR_TTL_ARTIFACTS` | graph-processor, api, incident-engine, dispatcher | `2592000` (30 days) | The artifact-retention **fallback**. The policy is the organization's **Retention → Search** setting; this value applies when that is not set or cannot be read. It is also the fallback for how far back a search may reach. |
| `DISRUPTION_SKIP_SETTLED` | incident-engine | `true` | The disruption check leaves alone incidents whose leads cannot have changed since the last check. `false` checks every incident in full every time. Compose only; a WFA appliance runs the default. |
| `RESPONDER_QUEUE_BUDGET_MB` | responder-engine | `128` | Memory, in MiB, that requests waiting for a responder worker may hold together (1 to 4,096). A request that finds no room gets `503` with `Retry-After: 1`. |
| `CASSANDRA_BROADCAST_RPC_ADDRESS` | cassandra | (unset) | The address Cassandra advertises to clients. An IPv6-only analytics Cassandra container needs it: without it the container refuses to start. |

## Feature Flags

| Variable | Default | Description |
| --- | --- | --- |
| `WF_LICENSE` | (empty) | Appliance license key, for framework sync and CyberGrid directory submission |
| `VITE_UI_MODULES` | `all` | UI module visibility |
| `REVERSE_PROXY_MODE` | `false` | Enable proxy header trust for Conductor UI |
| `WF_DEMO_MODE` | `false` | Enable demo mode with sample data and guided onboarding. Also gates AI spend: AI analysis returns canned output and the auto-provisioned AI provider is created disabled, so a demo deployment incurs no AI provider usage |
| `PARSER_RECONCILE` | `enabled` | signal-parser self-reconcile policy. On startup the parser enables any first-party parser compiled into the binary but absent from the `PARSERS` KV, while leaving explicit operator disables untouched. `enabled` applies the reconcile, `report-only` only emits the `parser_registry_dark_count` / `parser_registry_reconciled_total` metrics, `off` disables it |
| `BROKER_HEALTH_GATE_WARN_SECONDS` | `120` | WFA broker-health startup-gate threshold. A persistent wait is logged at INFO and escalates to WARN once it exceeds this many seconds |

## Monitoring

| Variable | Default | Description |
| --- | --- | --- |
| `GRAFANA_REMOTE_WRITE_URL` | (empty) | Grafana Cloud Prometheus remote-write endpoint |
| `GRAFANA_REMOTE_WRITE_USER` | (empty) | Grafana Cloud Prometheus instance ID |
| `GRAFANA_REMOTE_WRITE_API_KEY` | (empty) | Grafana Cloud API token for metrics |

When these are empty, Prometheus skips remote write.

## Cassandra Tuning

| Variable | Default | Description |
| --- | --- | --- |
| `JVM_EXTRA_OPTS` | (unset) | JVM options the Cassandra image appends last. On a Compose stack, set the heap here, for example `-Xms4G -Xmx4G`. The image ignores `MAX_HEAP_SIZE`, so `CASSANDRA_HEAP` does not change the heap. WFA sets the heap through this variable. |
| `DATA_NODE_HOSTS` | `cassandra:9042` | Processing-node compose file: comma-separated external Cassandra contact points |

## Localization

| Variable | Default | Description |
| --- | --- | --- |
| `default_locale` | `en` | Default locale for AI background tasks such as playbook analysis (set via business settings) |

## WFA node.json keys

On a WFA-managed appliance, set these keys in `node.json`, then run `wfa restart`. They need WFA 2.5.1 or later; install WFA 2.5.3.

| Key | Default | Description |
| --- | --- | --- |
| `mcp_http_enabled` | `false` | Turns on the HTTP MCP transport (`WF_MCP_HTTP_ENABLED` on the dispatcher) |
| `mcp_exposure_enabled` | `false` | Opens the MCP exposure listener on host port 8444 (IPv4). Has an effect only together with `mcp_http_enabled` |
| `mcp_public_url` | (unset) | `MCP_PUBLIC_URL` for app sign-in |
| `mcp_oauth_ui_url` | (unset) | `MCP_OAUTH_UI_URL` for app sign-in |
| `mcp_oauth_cimd` | `on` | `MCP_OAUTH_CIMD` |
| `mcp_relay_enabled`, `mcp_relay_handle`, `mcp_relay_credential`, `mcp_relay_ack`, `mcp_relay_revoke_pending` | (absent) | The AI-connector relay's state. Written only by `wfa mcp-relay`; do not set them by hand |
| `trusted_proxies` | (unset) | The load balancers in front of the appliance, for example `["192.0.2.10"]`. WFA passes the list to the reverse proxy as `WF_TRUSTED_PROXIES` |
| `graph_worker_count` | (unset: 4 workers) | Graph-processor worker count, 1 to 64 |
| `graph_appliance_touch_seconds` | (unset: 60) | How long the graph processor serves one appliance's artifacts from one lookup of its node, 0 to 3600; `0` turns the cache off |

!!! warning "Re-running wfa configure or wfa fetch"
    Re-running `wfa configure` or `wfa fetch` (including `wfa configure --license-file`) keeps the `mcp_` keys, but writes `node.json` **without** `trusted_proxies`. Add `trusted_proxies` again after each re-run, then run `wfa restart`.
