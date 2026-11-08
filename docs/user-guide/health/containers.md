# Containers

Detailed metrics for every Docker container in your deployment.

## Container List

Open **Health** > **Containers**. The page lists every container in a table with the columns **Container Name**, **State**, **Health**, **CPU %**, **Memory %**, **Uptime** and **Restarts**. Click a container to open its detail.

The page works on an appliance that has been running for a long time. A slow container-health read answers "service unavailable" promptly instead of an error after 30 seconds.

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

## Down and Unhealthy Containers

A running container that Docker marks unhealthy counts as a down service. The Console shows its node as **Error**, and a critical cluster problem report is raised.

- A container that was already unhealthy before the upgrade to 1.2.0 starts alerting once you upgrade. On WFA appliances this needs WFA 2.5.1 or later.
- An exited or stopped container is not counted as a down service. Only a running container that fails its health check is.
- The analytics Cassandra health check notices a node that has stopped serving clients, for example on a full data disk, instead of reading healthy while sign-ins fail.

## Licence Status

The Health page shows the licence's days remaining only for a licence it can read: active, expiring or expired.

When the last licence check failed, the page says "The last license check failed, so the license status shown may be out of date. The incident-engine log has the reason."

## Known Limitations

- **Two columns are blank.** The table leaves the **Container Name** and **Uptime** columns blank. State, health, CPU, memory and restarts are shown.
- **Empty after the upgrade.** The page is empty for the first collection cycle, about 15 seconds, after the upgrade. Containers removed before the upgrade are no longer listed.
- **Cassandra on a CPU-starved appliance.** On an appliance that is short of CPU, the Cassandra health check can time out for several minutes in a row. Cassandra then reads unhealthy and a problem report is raised, but nothing restarts it.

## Prometheus Integration

Metrics exported at `/api/v1/metrics` with `witfoo_container_*` prefix.
