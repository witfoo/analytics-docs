# Docker Compose Reference

WitFoo Analytics provides five Docker Compose files for different deployment topologies. All compose files are located in the `docker/` directory.

## Compose Files

| File | Role | Services | Description |
|---|---|---|---|
| `docker-compose.aio.yml` | AIO | 11 | All-in-One single-node deployment |
| `docker-compose.aio-conductor.yml` | AIO + Conductor | 16 | All services including Conductor pipeline |
| `docker-compose.data-node.yml` | Data Node | 1 | Cassandra-only storage node for clusters |
| `docker-compose.processing-node.yml` | Processing Node | 10 | All services except Cassandra |
| `docker-compose-conductor.yml` | Conductor add-on | 6 | Conductor services only (joins existing network) |

!!! tip "Choosing a Compose File"
    For most deployments, start with `docker-compose.aio.yml`. Add Conductor services later if you need log collection from syslog, Beats, or TLS sources.

## All-in-One (AIO)

The most common deployment. Runs all 11 Analytics services on a single node.

```bash
cd docker
docker compose -f docker-compose.aio.yml up -d --build
```

### Services Included

| Service | Container Name | Port(s) | Health Check |
|---|---|---|---|
| cassandra | witfoo-analytics-cassandra | 9042 | cqlsh DESCRIBE KEYSPACES |
| nats | witfoo-analytics-nats | 4222, 8222 | wget /healthz |
| artifact-ingestion | witfoo-analytics-artifact-ingestion | 8090 | -- |
| graph-processor | witfoo-analytics-graph-processor | -- | -- |
| incident-engine | witfoo-analytics-incident-engine | 8082 | wget /health |
| api | witfoo-analytics-api | 8080 | wget /health |
| dispatcher | witfoo-analytics-dispatcher | 8003 | wget /health |
| reverse-proxy | witfoo-analytics-reverse-proxy | 443, 8081 | wget /health |
| ui | witfoo-analytics-ui | 3000 | wget /ui/health |
| prometheus | witfoo-analytics-prometheus | 9090 | wget /-/healthy |
| grafana | witfoo-analytics-grafana | 3001 | wget /api/health |

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

This adds five Conductor services to the standard AIO deployment. See [Conductor Pipeline](conductor.md) for details on the Conductor services.

## Data Node

Deploys a single Cassandra instance configured for multi-node clustering.

```bash
NODE_IP=10.0.1.10 CASSANDRA_SEEDS=10.0.1.10,10.0.1.11 \
  docker compose -f docker-compose.data-node.yml up -d --build
```

| Variable | Default | Description |
|---|---|---|
| `NODE_IP` | `0.0.0.0` | Listen and broadcast address for this Cassandra node |
| `CASSANDRA_SEEDS` | `cassandra` | Comma-separated seed node addresses |
| `CASSANDRA_DC` | `dc1` | Datacenter name |
| `CASSANDRA_HEAP` | `6G` | Cassandra JVM heap size |
| `CASSANDRA_NEWSIZE` | `1200M` | Cassandra JVM new generation size |

Ports exposed: `9042` (CQL), `7000` (inter-node communication).

## Processing Node

Runs all application services except Cassandra, connecting to external data nodes for storage.

```bash
DATA_NODE_HOSTS=10.0.1.10:9042,10.0.1.11:9042 \
  docker compose -f docker-compose.processing-node.yml up -d --build
```

| Variable | Default | Description |
|---|---|---|
| `DATA_NODE_HOSTS` | `cassandra:9042` | Comma-separated Cassandra contact points |
| `CASSANDRA_DC` | `dc1` | Datacenter to connect to |

!!! warning "Network Connectivity"
    Processing nodes must be able to reach all data node addresses on port 9042. Ensure firewall rules allow this traffic.

## Conductor Add-on

Adds Conductor services to an existing Analytics deployment by joining the external `witfoo-analytics-net` network.

```bash
# Analytics stack must be running first
cd docker
docker compose -f docker-compose-conductor.yml up -d --build
```

!!! note "Prerequisite"
    The `witfoo-analytics-net` Docker network must already exist. Start the Analytics stack first.

## Common Configuration

### Network

All services communicate over the `witfoo-analytics-net` bridge network. No inter-service traffic is exposed to the host unless explicitly mapped via port bindings.

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
|---|---|---|
| `cassandra-data` | cassandra | Persistent database storage |
| `nats-data` | nats | JetStream message persistence |
| `certs` | reverse-proxy | TLS certificate storage |
| `prometheus-data` | prometheus | Metrics time-series data |
| `grafana-data` | grafana | Dashboard definitions and settings |

### Health Checks

All application services expose a `/health` endpoint. Health check configuration:

| Parameter | Value | Description |
|---|---|---|
| `interval` | 30s | Time between health checks |
| `timeout` | 5-10s | Maximum time for a health check response |
| `retries` | 3-5 | Failures before marking unhealthy |
| `start_period` | 10-120s | Grace period during startup |

Cassandra has the longest start period (60-120s) due to JVM warm-up and schema initialization.

### Restart Policy

All services except initialization containers use `restart: unless-stopped`. This ensures services restart after crashes but stay stopped if intentionally brought down.

### LISTEN_IP

The `LISTEN_IP` environment variable controls which network interface services bind to:

```bash
# Bind to all interfaces (default for most services)
LISTEN_IP=0.0.0.0

# Bind to localhost only (default for Prometheus/Grafana)
LISTEN_IP=127.0.0.1

# Bind to a specific interface
LISTEN_IP=10.0.1.10
```

### Build Secrets

Go services use BuildKit secrets to access private Git dependencies during build:

```yaml
secrets:
  git_credentials:
    file: ${HOME}/.git-credentials
```

Ensure your `~/.git-credentials` file contains a valid GitHub personal access token.

## Port Summary

| Port | Service | Protocol | Description |
|---|---|---|---|
| 443 | reverse-proxy | HTTPS | Primary TLS entry point |
| 3000 | ui | HTTP | Svelte web application |
| 3001 | grafana | HTTP | Metrics dashboards |
| 4222 | nats | TCP | NATS client connections |
| 8003 | dispatcher | HTTP | Job dispatch API |
| 8080 | api | HTTP | REST API |
| 8081 | reverse-proxy | HTTP | HTTP entry point |
| 8082 | incident-engine | HTTP | Incident analysis API |
| 8090 | artifact-ingestion | HTTP | Artifact submission |
| 8222 | nats | HTTP | NATS monitoring |
| 9042 | cassandra | CQL | Cassandra native protocol |
| 9090 | prometheus | HTTP | Prometheus web UI |
