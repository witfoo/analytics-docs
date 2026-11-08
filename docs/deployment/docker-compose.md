# Docker Compose Reference

WitFoo Analytics provides Docker Compose files for different deployment topologies, and overlay files that add to them. All compose files are in the `docker/` directory of the checkout. A WFA-managed appliance does not use them: WFA builds its own containers (see [WFA deployment](wfa.md)).

## Compose Files

| File | Role | Services | Description |
| --- | --- | --- | --- |
| `docker-compose.aio.yml` | AIO | 11 | All-in-One single-node deployment (plus an optional `alloy` service under the `monitoring` profile) |
| `docker-compose.aio-conductor.yml` | AIO + Conductor | 18 | All 11 Analytics services, the 6 Conductor services and a test mail sink, on one node |
| `docker-compose.data-node.yml` | Data Node | 1 | Cassandra-only storage node for clusters |
| `docker-compose.processing-node.yml` | Processing Node | 10 | All Analytics services except Cassandra |
| `docker-compose-conductor.yml` | Conductor add-on | 6 | Conductor services only (joins an existing Analytics network) |
| `docker-compose.yml` | Development | 13 | The Analytics services plus ClamAV and the responder engine, for a stack built from the checkout |

Overlay files are added after a base file with a second `-f`:

| Overlay | What it adds |
| --- | --- |
| `docker-compose.lb.yml` | SSL load balancer mode on the reverse proxy: HTTP only on port 80 |
| `docker-compose.mcp-exposure.yml` | The MCP exposure listener on port 8444, and the dispatcher's HTTP MCP transport |

!!! tip "Choosing a Compose File"
    For most deployments, start with `docker-compose.aio.yml`. Add Conductor services later if you need log collection from syslog, Beats, or TLS sources.

!!! warning "Set the encryption key first"
    From 1.2.0 every compose file refuses to run, `ps` and `down` included, until `AUTH_CONFIG_ENCRYPTION_KEY` is set. Generate one with `openssl rand -base64 32` and put it in the root `.env`, or let the launch scripts generate it. A stack that ran an earlier release and never set a key of its own needs one more step first: see [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md).

## All-in-One (AIO)

The most common deployment. Runs all 11 Analytics services on a single node.

```bash
cd docker
docker compose -f docker-compose.aio.yml up -d --build
```

### Services Included

| Service | Container Name | Port(s) | Published on | Health Check |
| --- | --- | --- | --- | --- |
| cassandra | witfoo-analytics-cassandra | 9042 | `LISTEN_IP` | cqlsh DESCRIBE KEYSPACES |
| nats | witfoo-analytics-nats | 4222, 8222 | `INTERNAL_LISTEN_IP` | wget /healthz |
| artifact-ingestion | witfoo-analytics-artifact-ingestion | 8090, 8443 | `LISTEN_IP` | -- |
| graph-processor | witfoo-analytics-graph-processor | -- | -- | -- |
| incident-engine | witfoo-analytics-incident-engine | 8082 | `INTERNAL_LISTEN_IP` | wget /health |
| api | witfoo-analytics-api | 8080 | `INTERNAL_LISTEN_IP` | wget /health |
| dispatcher | witfoo-analytics-dispatcher | 8003 | `INTERNAL_LISTEN_IP` | wget /health |
| reverse-proxy | witfoo-analytics-reverse-proxy | 443, 8081 | `LISTEN_IP` | wget /health |
| ui | witfoo-analytics-ui | 3000 | `INTERNAL_LISTEN_IP` | wget /ui/health |
| prometheus | witfoo-analytics-prometheus | 9090 | `INTERNAL_LISTEN_IP` | wget /-/healthy |
| grafana | witfoo-analytics-grafana | 3001 | `INTERNAL_LISTEN_IP` | wget /api/health |

### Startup Order

Services start in dependency order enforced by health checks:

```text
cassandra, nats (foundation)
    --> artifact-ingestion, graph-processor, incident-engine (processing)
        --> api, dispatcher (application)
            --> reverse-proxy (routing)
                --> ui (frontend)
                    prometheus --> grafana (observability)
```

## AIO + Conductor

Combines all Analytics and Conductor services in a single compose file for single-node deployments with log collection.

```bash
cd docker
docker compose -f docker-compose.aio-conductor.yml up -d --build
```

This adds the Conductor services (broker edge, signal server, signal parser, artifact filter, artifact exporter and Conductor UI) to the standard AIO deployment. The signal server publishes 514 (TCP and UDP), 1514, 5044 and 6514; the broker edge publishes 4223 and 8223 on `INTERNAL_LISTEN_IP`. See [Conductor Pipeline](conductor.md) for details on the Conductor services.

This file sets `WF_JWT_SECRET`, which it requires (`openssl rand -hex 32`).

!!! note "NetFlow and IPFIX"
    The compose files do not publish port 2055/udp for the NetFlow and IPFIX listener. To use it, add `2055:2055/udp` to the signal server's ports, then enable the listener under **Log Servers** in the Conductor UI.

## Data Node

Deploys a single Cassandra instance configured for multi-node clustering.

```bash
NODE_IP=10.0.1.10 CASSANDRA_SEEDS=10.0.1.10,10.0.1.11 \
  docker compose -f docker-compose.data-node.yml up -d --build
```

| Variable | Default | Description |
| --- | --- | --- |
| `NODE_IP` | `0.0.0.0` | Listen address for this Cassandra node, and the address it advertises |
| `CASSANDRA_SEEDS` | `cassandra` | Comma-separated seed node addresses |
| `CASSANDRA_DC` | `dc1` | Datacenter name |

Ports exposed: `9042` (CQL), `7000` (inter-node communication).

!!! note "Cassandra heap"
    The Cassandra image ignores `MAX_HEAP_SIZE`, so `CASSANDRA_HEAP` and `CASSANDRA_NEWSIZE` do not change the heap. To size it, add `JVM_EXTRA_OPTS` to the `cassandra` service's environment, for example `JVM_EXTRA_OPTS: -Xms4G -Xmx4G`.

!!! note "IPv6-only Cassandra"
    An IPv6-only analytics Cassandra container refuses to start (exit 2, "container IP is empty or malformed") unless its address is given in `CASSANDRA_BROADCAST_RPC_ADDRESS`.

## Processing Node

Runs all application services except Cassandra, connecting to external data nodes for storage.

```bash
DATA_NODE_HOSTS=10.0.1.10:9042,10.0.1.11:9042 \
  docker compose -f docker-compose.processing-node.yml up -d --build
```

| Variable | Default | Description |
| --- | --- | --- |
| `DATA_NODE_HOSTS` | `cassandra:9042` | Comma-separated Cassandra contact points |
| `CASSANDRA_DC` | `dc1` | Datacenter to connect to |

!!! warning "Network Connectivity"
    Processing nodes must be able to reach all data node addresses on port 9042. Ensure firewall rules allow this traffic.

!!! warning "Same keys on every node"
    Every node that runs the api or incident-engine against the same Cassandra cluster needs the same `AUTH_CONFIG_ENCRYPTION_KEY` and `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS`. The launch script generates a key on any machine whose `.env` has none, so copy both variables from the first node's `.env` before a second node's first start.

## Conductor Add-on

Adds Conductor services to an existing Analytics deployment by joining the external `witfoo-analytics-net` network.

```bash
# Analytics stack must be running first
cd docker
docker compose -f docker-compose-conductor.yml up -d --build
```

!!! note "Prerequisite"
    The `witfoo-analytics-net` Docker network must already exist. Start the Analytics stack first.

## MCP Exposure Listener

The MCP exposure overlay adds a separate reverse-proxy listener on port 8444 for marketplace AI clients. It serves `/mcp` and the app sign-in endpoints and nothing else; every other path answers `404`. It also turns on the dispatcher's HTTP MCP transport (`WF_MCP_HTTP_ENABLED=true`), which `/mcp` needs.

```bash
cd docker
docker compose -f docker-compose.yml -f docker-compose.mcp-exposure.yml up -d
```

The overlay applies over `docker-compose.yml`, `docker-compose.aio.yml`, `docker-compose.aio-conductor.yml` and `docker-compose.processing-node.yml`. The main listeners (443, 8081) are unchanged.

!!! warning "The listener restricts no source"
    Decide which sources may reach port 8444, at the perimeter or on the host in the `DOCKER-USER` chain. INPUT-chain rules managed through ufw or firewalld do not filter a Docker-published port. Check that host port 8444 is free first, and prove the restriction with a probe from a source that must be refused. Behind a load balancer, set `WF_TRUSTED_PROXIES` on the reverse proxy first. See [MCP exposure listener](../ai/mcp/exposure-listener.md).

## Load Balancer Overlay

```bash
cd docker
docker compose -f docker-compose.yml -f docker-compose.lb.yml up -d
```

The overlay ships `WF_TRUSTED_PROXIES` commented out. Uncomment it and set your load balancer's address, so the reverse proxy believes `X-Forwarded-For` from that peer only. See [Configuration](configuration.md).

## Common Configuration

### Network

All services communicate over the `witfoo-analytics-net` bridge network. No inter-service traffic is exposed to the host unless explicitly mapped via port bindings.

### Published Addresses

Two variables choose the host address a port is published on:

- `LISTEN_IP` publishes the services that must be reachable from outside: the reverse proxy, the artifact receiver and Cassandra. The compose files default it to `0.0.0.0`; the example `.env` sets `127.0.0.1`.
- `INTERNAL_LISTEN_IP` (default `127.0.0.1`) publishes everything else: the api, incident-engine, dispatcher, UI, NATS, the broker edge, Prometheus and Grafana.

Restrict Cassandra's port 9042 at the host firewall.

### Logging

All services use the same JSON file logging driver:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
    compress: "true"
```

### Volumes

| Volume | Service | Purpose |
| --- | --- | --- |
| `cassandra-data` | cassandra | Persistent database storage |
| `nats-data` | nats | JetStream message persistence |
| `certs` | reverse-proxy | TLS certificate storage |
| `prometheus-data` | prometheus | Metrics time-series data |
| `grafana-data` | grafana | Dashboard definitions and settings |

### Health Checks

All application services expose a `/health` endpoint. Health check configuration:

| Parameter | Value | Description |
| --- | --- | --- |
| `interval` | 30s | Time between health checks |
| `timeout` | 5-10s | Maximum time for a health check response |
| `retries` | 3-5 | Failures before marking unhealthy |
| `start_period` | 10-120s | Grace period during startup |

Cassandra has the longest start period (60-120s) due to JVM warm-up and schema initialization.

### Restart Policy

All services except initialization containers use `restart: unless-stopped`. This ensures services restart after crashes but stay stopped if intentionally brought down.

### Artifact Receiver Capacity

The artifact receiver (artifact-ingestion) limits what it holds in memory and how many connections it accepts. The defaults suit most stacks:

| Variable | Default | Description |
| --- | --- | --- |
| `WF_INGEST_PROFILE` | (unset) | `small` (body 32 MiB, budget 128 MiB) or `default` (body 64 MiB, budget 256 MiB). Unset, `WF_MEMORY_BUDGET_MB` below 768 selects the small profile |
| `WF_MEMORY_BUDGET_MB` | (unset) | The container's memory budget in MiB |
| `WF_INGEST_MAX_MESSAGE_MIB` | `9.5` | Largest WebSocket message; 9.5 MiB is also the largest artifact |
| `WF_CONN_MAX` | `1024` | Most connections on the plain listener (16 to 65536) |
| `WF_CONN_MAX_TLS` | `512` | Most connections on the TLS listener |
| `WF_CONN_MAX_PER_SOURCE` | `128` | Most connections from one source address |
| `WF_CONN_TRUSTED` | loopback only | CIDRs and addresses exempt from the per-source share |

Where many Conductors reach the receiver from one address (a NAT or a load balancer), they share one source's connections and memory. List that address in `WF_CONN_TRUSTED`. A batch of more than 1,000 artifacts is refused with `400`, and request headers over 12,288 bytes with `431`. The TLS port speaks HTTP/1.1 only. See [Environment Variables](../reference/environment-variables.md).

## Port Summary

| Port | Service | Protocol | Published on | Description |
| --- | --- | --- | --- | --- |
| 443 | reverse-proxy | HTTPS | `LISTEN_IP` | Primary TLS entry point |
| 3000 | ui | HTTP | `INTERNAL_LISTEN_IP` | Svelte web application |
| 3001 | grafana | HTTP | `INTERNAL_LISTEN_IP` | Metrics dashboards |
| 4222 | nats | TCP | `INTERNAL_LISTEN_IP` | NATS client connections |
| 8003 | dispatcher | HTTP | `INTERNAL_LISTEN_IP` | Dispatcher (WebSockets and `/mcp`) |
| 8080 | api | HTTP | `INTERNAL_LISTEN_IP` | REST API |
| 8081 | reverse-proxy | HTTP | `LISTEN_IP` | HTTP entry point |
| 8082 | incident-engine | HTTP | `INTERNAL_LISTEN_IP` | Incident analysis API |
| 8090 | artifact-ingestion | HTTP | `LISTEN_IP` | Artifact submission |
| 8443 | artifact-ingestion | HTTPS | `LISTEN_IP` | Artifact submission over TLS; Conductors send to `/v1/conductor/artifacts/batch` |
| 8444 | reverse-proxy | HTTPS | `LISTEN_IP` | MCP exposure listener (overlay only) |
| 8222 | nats | HTTP | `INTERNAL_LISTEN_IP` | NATS monitoring |
| 9042 | cassandra | CQL | `LISTEN_IP` | Cassandra native protocol |
| 9090 | prometheus | HTTP | `INTERNAL_LISTEN_IP` | Prometheus web UI |

The reverse proxy no longer serves an `/ingestion/` path. A Conductor whose artifact endpoint was typed by hand with that prefix gets `404`; point it at `https://<analytics-host>:8443/v1/conductor/artifacts/batch`.

## Verifying Image Signatures

WitFoo signs the published images with keyless signatures. Verify an image with `cosign verify`, against the OIDC issuer `https://token.actions.githubusercontent.com` and a certificate identity naming WitFoo's build workflow:

```bash
cosign verify \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github\.com/witfoo-dev/analytics/\.github/workflows/build-and-push\.yml@' \
  <image>@<digest>
```

For the appliance images signing is advisory: a build whose digest could not be validated is not signed. Registry clean-up may remove signature and attestation tags on its own schedule. From 1.2.0 the version and `latest` tags carry exactly the digest of the build they name.
