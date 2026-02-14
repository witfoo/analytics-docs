# Containers

Detailed metrics for every Docker container in your deployment.

## Container List

Each container displays as a clickable card with name, state, health, CPU %, memory, and uptime.

### Color-Coded Metrics

| Threshold | Color |
| --- | --- |
| < 70% | Normal |
| 70-90% | Yellow |
| > 90% | Red |

## Container Detail

### Current Metrics

| Metric | Source |
| --- | --- |
| **CPU %** | `(cpuDelta / systemDelta) * numCPUs * 100` |
| **Memory** | RSS from Docker stats |
| **Network I/O** | Bytes received/transmitted |
| **Disk I/O** | Bytes read/written |
| **PIDs** | Process count |

### Historical Charts

Time-series bar charts stored in Cassandra using TimeUUID ordering.

## Core Services

| Container | Service |
| --- | --- |
| `witfoo-analytics-cassandra` | Cassandra database |
| `witfoo-analytics-nats` | NATS message broker |
| `witfoo-analytics-incident-engine` | Core business logic |
| `witfoo-analytics-api` | API gateway |
| `witfoo-analytics-ui` | SvelteKit frontend |
| `witfoo-analytics-artifact-ingestion` | Artifact receiver |
| `witfoo-analytics-graph-processor` | Graph builder |
| `witfoo-analytics-dispatcher` | Event dispatcher |
| `witfoo-analytics-reverse-proxy` | Request router |

## Prometheus Integration

Metrics exported at `/api/v1/metrics` with `witfoo_container_*` prefix.
