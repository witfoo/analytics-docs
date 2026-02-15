# Broker Edge (NATS JetStream)

Broker Edge is the central message broker for the Conductor pipeline. All inter-service communication flows through this NATS JetStream server, providing persistent streams for artifact data, configuration distribution via KV buckets, and monitoring endpoints.

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 4223 | NATS | Client connections (all pipeline services) |
| 4443 | NATS | Leaf node and cluster connections |
| 8223 | HTTP | Monitoring and management API |

## Streams

Broker Edge auto-creates all required streams on first startup. Streams are created with appliance-specific suffixes to isolate data per deployment.

| Stream | Purpose | Consumers |
|--------|---------|-----------|
| `DATA` | Artifact pipeline (raw → parsed → enriched → final → unknown) | signal-parser, artifact-filter, artifact-exporter |
| `EVENTS` | System events and status updates | WFA, monitoring tools |
| `LOGS` | Centralized service log collection | Log aggregators |
| `METRICS` | Pipeline metrics (Prometheus format) | Grafana Cloud, local Prometheus |
| `STATUSES` | Service health and status reports | WFA orchestration |

The DATA stream uses a hierarchical subject pattern for pipeline stages:

```
{applianceID}.data.artifacts.{stage}
```

Where `{stage}` is one of: `raw`, `parsed`, `enriched`, `final`, `unknown`.

## KV Buckets

Runtime configuration for all pipeline services is stored in JetStream KV buckets. The Conductor UI writes configuration to these buckets, and each service watches its respective bucket for changes.

| Bucket | Purpose | Writer | Reader |
|--------|---------|--------|--------|
| `SERVERS` | Push-based listener configuration | conductor-ui | signal-server |
| `INTEGRATIONS` | Pull-based API collector configuration | conductor-ui | signal-client |
| `PARSERS` | Parser enable/disable state | conductor-ui | signal-parser |
| `FILTERS` | Filter and deduplication rules | conductor-ui | artifact-filter |
| `EXPORTERS` | Export destination configuration | conductor-ui | artifact-exporter |

## Health Check

Verify broker health from any container on the Conductor network:

```bash
docker exec broker-edge-svc nats server ping --server=nats://127.0.0.1:4223
```

## Monitoring

The HTTP monitoring endpoint on port 8223 provides server information, connection details, and stream statistics:

```bash
# Stream status
docker exec broker-edge-svc nats stream ls

# Detailed stream info
docker exec broker-edge-svc nats stream info DATA

# Consumer lag (pending messages)
docker exec broker-edge-svc nats consumer info DATA <consumer-name>

# KV bucket contents
docker exec broker-edge-svc nats kv ls
```

## Clustering

Broker Edge supports leaf node connections on port 4443 for multi-node deployments. In a clustered configuration, leaf nodes connect to a central broker to form a unified messaging fabric. Clustering is configured through the `wfa configure` wizard and managed by the WFA daemon.

!!! warning
    If broker-edge fails to start, all downstream services will be unable to communicate. Check `docker logs broker-edge-svc` for startup errors, and verify that ports 4223 and 4443 are not in use by another process.