# Metrics and Monitoring

Monitor WitFoo Conductor pipeline health, performance, and resource usage through built-in metrics and dashboards.

## Real-Time Dashboard

The Conductor UI dashboard (`/`) provides real-time monitoring with four tabs:

- **Overview** — CPU, memory, and disk usage gauges
- **Pipeline** — Message throughput and pipeline stage counts
- **Service Status** — Per-service health indicators
- **Container Status** — Per-container resource usage

See [Dashboard](ui/dashboard.md) for detailed tab descriptions.

## Prometheus Metrics

Each Conductor service exposes Prometheus-compatible metrics:

| Service | Metric Prefix | Key Metrics |
|---------|--------------|-------------|
| signal-server | `signal_server_` | Messages received, bytes ingested, connection count |
| signal-client | `signal_client_` | API polls completed, records fetched, errors |
| signal-parser | `signal_parser_` | Messages parsed, parse duration, unknown count |
| artifact-filter | `artifact_filter_` | Messages filtered, duplicates detected |
| artifact-exporter | `artifact_exporter_` | Messages exported, batch count, export errors |
| broker-edge | `nats_` | Stream messages, consumer pending, bytes total |

### Pipeline Stage Metrics

The primary throughput metric is `pipeline_stage_count` with labels:

- `stage`: source_client, broker, filter, export
- `status`: success, error, dropped

## Grafana Cloud Integration

Conductor supports metrics export to Grafana Cloud via the grafana-agent service:

1. Enable "Local Metrics" during `wfa configure` (Step 10)
2. Metrics are scraped from all services and forwarded to Grafana Cloud
3. Pre-built dashboards available for pipeline throughput and service health

## Local Prometheus/Grafana Stack

For air-gapped or on-premises deployments:

```bash
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

Enable the local metrics stack during `wfa configure` by selecting "Local metrics" in the optional features step.

## Key Metrics to Monitor

| Metric | Warning Threshold | Description |
|--------|------------------|-------------|
| Pipeline throughput | < 100 msgs/sec | Messages processed per second |
| Parser unknown rate | > 10% | Percentage of unparsed messages |
| Export error rate | > 1% | Failed export operations |
| Disk usage | > 80% | `wfa diag` warns at this threshold |
| Container memory | > 90% of limit | Risk of OOM kill |

## Alert Configuration

Configure alerts through:

1. **Grafana Cloud** — Alert rules on exported metrics
2. **Conductor UI** — Service status warnings on the dashboard
3. **WFA Status** — `sudo wfa status` shows recent errors from the systemd journal

!!! tip
    Run `sudo wfa diag` regularly to verify all connectivity checks pass. This catches issues before they impact pipeline throughput.
