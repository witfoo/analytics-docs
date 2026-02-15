# Deployment Guide

## Production Deployment

In production, Conductor is deployed as a **WitFoo Appliance** — a dedicated Linux server running the WFA (WitFoo Agent) daemon as a systemd service.

### Prerequisites

- Ubuntu 22.04 or 24.04 LTS (AMD64)
- Minimum 4 CPU cores and 8 GB RAM
- Docker Engine installed
- Network access to the container registry (or offline image loading)
- WitFoo license key (or 15-day trial)

### Installation

1. Install the WFA package:

    ```bash
    sudo apt install wfa
    ```

2. Run the interactive configuration wizard:

    ```bash
    sudo wfa configure
    ```

    See the [WFA CLI Reference](wfa-cli.md) for details on each configuration step.

3. Start the WFA daemon:

    ```bash
    sudo wfa start
    ```

4. Enable auto-start at boot:

    ```bash
    sudo wfa enable
    ```

WFA will pull container images, create containers, and start all services in dependency order.

### Service Dependency Order

WFA starts containers in the following order to satisfy inter-service dependencies:

1. **broker-edge** — Must be healthy before any other service starts
2. **signal-server**, **signal-client**, **signal-parser** — Connect to broker on startup
3. **artifact-filter** — Consumes from signal-parser output
4. **artifact-exporter** — Consumes from artifact-filter output
5. **conductor-ui** — Connects to broker for configuration management

### Health Checks

WFA monitors container health using Docker health checks. The broker-edge container includes a built-in health check:

```bash
nats server ping --server=nats://127.0.0.1:4223
```

Downstream services wait for broker-edge to report healthy before starting their connection attempts.

## Development Deployment

For development and testing, Conductor can be deployed using Docker Compose.

### Building from Source

```bash
# Build all service binaries
./scripts/conductor-build.sh all

# Build Docker images
docker compose -f docker-compose-conductor.yml build
```

### Running with Docker Compose

```bash
# Start all services
docker compose -f docker-compose-conductor.yml up -d
```

### External Network

The Docker Compose configuration uses an external network (`witfoo-analytics-net`) for integration with the WitFoo Analytics stack. Create this network before starting:

```bash
docker network create witfoo-analytics-net
```

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `/witfoo/configs` | `/configs` (read-only) | Node configuration (`node.json`) |
| `/witfoo/certs` | `/certs` (read-only) | TLS certificates |
| `/data` | `/data` | Persistent data (NATS, SQLite) |
| `/logs` | `/logs` | Service log files |