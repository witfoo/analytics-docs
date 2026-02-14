# Monitoring

Monitor WitFoo Analytics using built-in Prometheus metrics and optional Grafana integration.

## Prometheus Metrics

Metrics are available at `/api/v1/metrics` (requires `metrics:read` permission).

### Container Metrics

Prefix: `witfoo_container_*`

| Metric | Type | Description |
| --- | --- | --- |
| `cpu_percent` | Gauge | Container CPU usage percentage |
| `memory_bytes` | Gauge | Container memory usage |
| `memory_percent` | Gauge | Container memory percentage |
| `network_rx_bytes` | Counter | Network bytes received |
| `network_tx_bytes` | Counter | Network bytes transmitted |

### WFA Metrics

Prefix: `witfoo_wfa_*`

WFA metrics track appliance-level statistics distinct from container metrics.

## Grafana Integration

### Remote Write

Enable Prometheus remote write to Grafana Cloud:

```bash
GRAFANA_REMOTE_WRITE_URL=https://prometheus-us-central1.grafana.net/api/prom/push
GRAFANA_INSTANCE_ID=123456
GRAFANA_API_KEY=your-api-key
```

### Dashboard

A pre-built Grafana dashboard JSON is available for import. It includes:

- Container CPU/memory panels with threshold coloring
- Network I/O rate graphs
- Service health status indicators
- Alert history timeline
