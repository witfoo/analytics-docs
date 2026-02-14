# Installation

Deploy WitFoo Analytics using Docker Compose. All services run as containers with health checks and automatic restart policies.

## Prerequisites

- Docker 24.0 or later
- Docker Compose v2.20 or later
- Git (for cloning the repository)
- 8 GB RAM minimum (16 GB recommended)
- 50 GB available disk space

## 5-Minute Quickstart

=== "Docker Compose (AIO)"

    ```bash
    # Clone the repository
    git clone https://github.com/witfoo-dev/analytics.git
    cd analytics

    # Configure environment
    cp docker/.env.example docker/.env
    # Edit docker/.env with your settings

    # Start all services
    docker compose -f docker/docker-compose.yml up -d

    # Verify services are healthy
    docker compose -f docker/docker-compose.yml ps
    ```

=== "WFA CLI"

    ```bash
    # Install using WFA (WitFoo Appliance) CLI
    wfa analytics install --role aio

    # Follow the configuration wizard
    wfa analytics configure

    # Start services
    wfa analytics start
    ```

## Service Startup Order

Docker Compose manages service dependencies automatically:

1. **Cassandra** starts first (database)
2. **NATS** starts next (message broker)
3. **Incident Engine** starts after Cassandra and NATS are healthy
4. **API** starts after Incident Engine is ready
5. **UI**, **Graph Processor**, **Dispatcher**, and **Artifact Ingestion** start last

!!! info "First startup takes longer"
    On first boot, Cassandra initializes its schema and seed data. This may take 2-3 minutes. Subsequent startups are faster.

## Verify Installation

After all services show as `healthy`:

```bash
# Check service health
curl -s http://localhost:8080/api/v1/status | jq .

# Expected response:
# {"success": true, "data": {"status": "healthy"}}
```

Open your browser to `http://localhost:8080` to access the web UI.

## Configuration

Key environment variables in `docker/.env`:

| Variable | Default | Description |
| --- | --- | --- |
| `CASSANDRA_HOST` | `cassandra` | Cassandra hostname |
| `NATS_URL` | `nats://nats:4222` | NATS connection URL |
| `JWT_SECRET` | (required) | Secret key for JWT token signing |
| `ORG_ID` | `witfoo` | Organization identifier |

See [Configuration](../deployment/configuration.md) for the complete environment variable reference.

## Troubleshooting

!!! warning "Port Conflicts"
    WitFoo Analytics uses ports 8080 (web UI), 9042 (Cassandra), and 4222 (NATS). Ensure these ports are not in use by other services.

**Services not starting?**

```bash
# Check container logs
docker compose -f docker/docker-compose.yml logs incident-engine

# Restart a specific service
docker compose -f docker/docker-compose.yml restart incident-engine
```

**Cassandra connection errors?**

Wait 60 seconds after starting Cassandra for schema initialization to complete, then restart the dependent services.
