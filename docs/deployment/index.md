# Deployment Overview

WitFoo Analytics is a containerized security analytics platform deployed via Docker Compose or the WFA (WitFoo Appliance) CLI. This section covers all deployment methods, service configuration, monitoring, TLS, and the Conductor signal pipeline.

## Supported Environments

| OS | Version | Architecture | Status |
|---|---|---|---|
| Ubuntu | 22.04 LTS | amd64 | Fully supported |
| Ubuntu | 24.04 LTS | amd64 | Fully supported |

!!! warning "Hardware Requirements"
    Minimum hardware depends on the deployment role. See the [WFA Deployment](wfa.md) page for per-role specifications. All-in-One deployments require at least 8 CPU cores, 32 GB RAM, and 500 GB SSD storage.

## Deployment Methods

### Docker Compose

The standard deployment method for development and production environments. Five compose files support different deployment topologies.

```bash
# All-in-One (most common for single-node deployments)
docker compose -f docker/docker-compose.aio.yml up -d --build
```

See [Docker Compose Reference](docker-compose.md) for full details on all compose files and service definitions.

### WFA CLI

The WFA (WitFoo Appliance) CLI automates installation, configuration, and upgrades for appliance-based deployments.

```bash
wfa analytics install --role analytics-aio
```

See [WFA Deployment](wfa.md) for the interactive configuration wizard and all CLI commands.

## Deployment Roles

WitFoo Analytics supports four deployment roles that scale from a single node to a distributed cluster.

| Role | Description | Services | Use Case |
|---|---|---|---|
| **AIO** | All-in-One | 11 Analytics services | Single-node deployments |
| **AIO + Conductor** | All-in-One with signal pipeline | 11 Analytics + 5 Conductor services | Single-node with log collection |
| **Data Node** | Cassandra storage node | Cassandra only | Distributed storage cluster |
| **Processing Node** | Application services | 10 services (no local Cassandra) | Connects to external data nodes |

### Single-Node Architecture

The AIO role runs all services on a single machine. This is the simplest deployment and suitable for most organizations.

```text
Browser --> Reverse Proxy (443/8081) --> API (8080) --> Incident Engine (8082)
                                    --> UI (3000)
                                    --> Dispatcher (8003)
```

### Distributed Architecture

For larger deployments, separate data nodes (Cassandra) from processing nodes (application services).

```text
Processing Node                    Data Node(s)
+-------------------+             +-------------------+
| API, UI, Engine   |  ------->  | Cassandra (9042)  |
| Proxy, Dispatcher |             +-------------------+
| NATS, Ingestion   |             +-------------------+
| Graph Processor   |  ------->  | Cassandra (9042)  |
| Prometheus, Grafana|            +-------------------+
+-------------------+
```

## Service Overview

WitFoo Analytics consists of the following core services:

| Service | Port | Description |
|---|---|---|
| **reverse-proxy** | 443, 8081 | HTTPS/HTTP entry point, routes to all backend services |
| **api** | 8080 | REST API, authentication, user management |
| **incident-engine** | 8082 | Incident analysis, work units, reporting |
| **dispatcher** | 8003 | Background job orchestration |
| **artifact-ingestion** | 8090 | Receives security artifacts via HTTP |
| **graph-processor** | -- | Background processor for graph node/edge creation |
| **ui** | 3000 | Svelte 5 web application |
| **cassandra** | 9042 | Primary data store (Cassandra 5.0) |
| **nats** | 4222 | Internal message broker |
| **prometheus** | 9090 | Metrics collection and storage |
| **grafana** | 3001 | Metrics dashboards and visualization |

## Quick Start

1. Clone the repository and ensure Docker is installed.

2. Start all services with the AIO compose file:

    ```bash
    cd docker
    docker compose -f docker-compose.aio.yml up -d --build
    ```

3. Wait for all health checks to pass (approximately 2-3 minutes):

    ```bash
    docker compose -f docker-compose.aio.yml ps
    ```

4. Access the web UI at `https://localhost` or `http://localhost:8081`.

!!! info "Default Credentials"
    The default administrator account is `admin` / `F00theN0ise!`. Change this password immediately after first login.

## Next Steps

- [Docker Compose Reference](docker-compose.md) -- Compose file details, service definitions, and ports
- [Configuration](configuration.md) -- Environment variables for all services
- [WFA Deployment](wfa.md) -- Automated appliance deployment via CLI
- [Monitoring](monitoring.md) -- Prometheus metrics, Grafana dashboards, and alerting
- [TLS Configuration](tls.md) -- HTTPS setup and certificate management
- [Conductor Pipeline](conductor.md) -- Log collection and signal processing
