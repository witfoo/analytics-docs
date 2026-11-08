# Deployment Overview

WitFoo Analytics is a containerized security analytics platform deployed via Docker Compose or the WFA (WitFoo Appliance) CLI. This section covers all deployment methods, service configuration, monitoring, TLS, and the Conductor signal pipeline.

## Supported Environments

| OS | Version | Architecture | WFA package |
|---|---|---|---|
| Ubuntu | 24.04 LTS | amd64 | `.deb` |
| Red Hat Enterprise Linux | 9 | amd64 | `.rpm` |
| Red Hat Enterprise Linux | 10 | amd64 | `.rpm` |

!!! warning "Hardware Requirements"
    Minimum hardware depends on the deployment role. See the [WFA Deployment](wfa.md) page for per-role specifications. An Analytics AIO + Conductor node needs at least 6 CPUs, 28 GB RAM and 200 GB of disk; an Analytics AIO node needs at least 4 CPUs, 20 GB RAM and 200 GB of disk.

## Upgrading to 1.2.0

Release 1.2.0 has steps to take before you upgrade:

- **Docker Compose and standalone stacks** must set `AUTH_CONFIG_ENCRYPTION_KEY`, the key that seals stored secrets. No default ships, and every `docker compose` command refuses to run until it is set.
- **WFA-managed appliances** update the Analytics images to 1.2.0 first, then install WFA 2.5.3 soon after. On an appliance WFA owns the encryption key, so do not edit it by hand.
- **Separate Conductor nodes** are upgraded with Analytics or before it.

See [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md) for every step and the known limitations.

## Deployment Methods

### Docker Compose

The standard deployment method for development and production environments. Several compose files support different deployment topologies.

```bash
# All-in-One (most common for single-node deployments)
docker compose -f docker/docker-compose.aio.yml up -d --build
```

See [Docker Compose Reference](docker-compose.md) for full details on all compose files and service definitions.

### WFA CLI

The WFA (WitFoo Appliance) CLI automates installation, configuration, and upgrades for appliance-based deployments.

```bash
sudo wfa configure
sudo wfa analytics install
```

`wfa configure` asks for the role and writes the node's configuration; `wfa analytics install` checks the host against the role's minimum hardware. See [WFA Deployment](wfa.md) for the interactive configuration wizard and all CLI commands.

## Deployment Roles

WitFoo Analytics supports four deployment roles that scale from a single node to a distributed cluster.

| Role | Description | Services | Use Case |
|---|---|---|---|
| **AIO** | All-in-One | 11 Analytics services | Single-node deployments |
| **AIO + Conductor** | All-in-One with signal pipeline | 11 Analytics services plus the Conductor services | Single-node with log collection |
| **Data Node** | Cassandra storage node | Cassandra only | Distributed storage cluster |
| **Processing Node** | Application services | 10 services (no local Cassandra) | Connects to external data nodes |

### Single-Node Architecture

The AIO role runs all services on a single machine. This is the simplest deployment and suitable for most organizations.

```text
Browser --> Reverse Proxy (443/8081) --> API (8080) --> Incident Engine (8082)
                                    --> UI (3000)
                                    --> Dispatcher (8003): /mcp, /ws/chat and the other WebSockets
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

!!! note "One Processing node per Data cluster"
    One Analytics Processing node per organization and Data cluster is supported in 1.2.0.

## Service Overview

WitFoo Analytics consists of the following core services:

| Service | Port | Description |
|---|---|---|
| **reverse-proxy** | 443, 8081 | HTTPS/HTTP entry point, routes to all backend services |
| **api** | 8080 | REST API, authentication, user management |
| **incident-engine** | 8082 | Incident analysis, work units, reporting |
| **dispatcher** | 8003 | WebSockets, the MCP endpoint and background job orchestration |
| **artifact-ingestion** | 8090, 8443 | Receives security artifacts over HTTP (8090) and HTTPS (8443) |
| **graph-processor** | -- | Background processor for graph node/edge creation |
| **ui** | 3000 | Svelte 5 web application |
| **cassandra** | 9042 | Primary data store (Cassandra 5.0) |
| **nats** | 4222 | Internal message broker |
| **prometheus** | 9090 | Metrics collection and storage |
| **grafana** | 3001 | Metrics dashboards and visualization |

On a WFA appliance running WFA 2.5.1 or later, the api (8080) and incident-engine (8082) ports are not published on the host, and NATS is published on `127.0.0.1` only. See [Architecture](../getting-started/architecture.md) for the published ports of each deployment.

## Quick Start

1. Clone the repository and ensure Docker is installed.

2. Set `AUTH_CONFIG_ENCRYPTION_KEY` in the root `.env` file to a random 32-byte value, base64-encoded:

    ```bash
    openssl rand -base64 32
    ```

    The key is part of your data: back it up with the database and store the two apart. The provided launch scripts generate a key when none is set.

3. Start all services with the AIO compose file:

    ```bash
    cd docker
    docker compose -f docker-compose.aio.yml up -d --build
    ```

4. Wait for all health checks to pass (approximately 2-3 minutes):

    ```bash
    docker compose -f docker-compose.aio.yml ps
    ```

5. Access the web UI at `https://localhost` or `http://localhost:8081`.

!!! info "Default Credentials"
    The default administrator account is `admin@witfoo.com` / `F00theN0ise!`. Change this password immediately after first login.

## Production Readiness Checklist

Before deploying WitFoo Analytics to production, verify the following:

### Load Balancer Configuration

- [ ] **HSTS headers** enabled on the load balancer or reverse proxy (`Strict-Transport-Security: max-age=31536000; includeSubDomains`)
- [ ] **SSL termination** configured with valid TLS certificates
- [ ] Health check endpoint configured (e.g., `/api/v1/status`)

### Trusted Proxies

- [ ] Declare each load balancer in front of the reverse proxy: `WF_TRUSTED_PROXIES` on Docker Compose (comma-separated addresses or CIDRs), or `trusted_proxies` in `node.json` on a WFA appliance (WFA 2.5.1 or later)
- [ ] Make sure the load balancer sends `X-Forwarded-For` and `X-Forwarded-Proto`. The reverse proxy does not read `X-Real-IP`
- [ ] On a WFA appliance, add `trusted_proxies` again after every `wfa configure` or `wfa fetch` re-run: a re-run writes `node.json` without it

See [TLS Configuration](tls.md) for what the reverse proxy trusts when the list is unset.

### Security Headers

The reverse-proxy automatically applies 7 OWASP security headers to all responses:

| Header | Value |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `0` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Content-Security-Policy` | Restrictive default policy |
| `Permissions-Policy` | Restrictive feature policy |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |

### Database Credentials

- [ ] Cassandra credentials are auto-generated per node during WFA installation -- do not use default credentials in production
- [ ] Verify Cassandra is not exposed on public network interfaces

### Network Hardening

- [ ] On Docker Compose, `INTERNAL_LISTEN_IP` (default `127.0.0.1`) publishes NATS, the api, incident-engine, the dispatcher, the UI, Prometheus and Grafana. `LISTEN_IP` still publishes Cassandra (9042), the artifact receiver (8090, 8443) and the edge (443, 8081), so restrict Cassandra's ports at the host firewall
- [ ] Only expose the reverse-proxy port (443) to users, and the artifact receiver (8443) to your Conductors
- [ ] Configure firewall rules to limit inter-node communication to required ports

!!! warning "Environment Variables"
    See the [Environment Variables](../reference/environment-variables.md) reference for all security-related configuration options including `WF_TRUSTED_PROXIES`, `AUTH_CONFIG_ENCRYPTION_KEY`, and `WF_JWT_SECRET`.

## Next Steps

- [Docker Compose Reference](docker-compose.md) -- Compose file details, service definitions, and ports
- [Configuration](configuration.md) -- Environment variables for all services
- [WFA Deployment](wfa.md) -- Automated appliance deployment via CLI
- [Monitoring](monitoring.md) -- Prometheus metrics, Grafana dashboards, and alerting
- [TLS Configuration](tls.md) -- HTTPS setup and certificate management
- [Conductor Pipeline](conductor.md) -- Log collection and signal processing
- [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md) -- Steps before and after the upgrade
