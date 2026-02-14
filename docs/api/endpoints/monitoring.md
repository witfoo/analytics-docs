# Monitoring

System monitoring and Prometheus metrics export.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/metrics` | `metrics:read` | Prometheus format metrics |
| GET | `/v1/status` | (none) | Basic health check |

## Prometheus Metrics

Metrics are exported with the `witfoo_container_*` prefix:

- `witfoo_container_cpu_percent` — Container CPU usage
- `witfoo_container_memory_bytes` — Container memory usage
- `witfoo_container_network_rx_bytes` — Network received
- `witfoo_container_network_tx_bytes` — Network transmitted

## Grafana Integration

Metrics can be scraped by Prometheus or forwarded to Grafana Cloud via remote write. Configure the `GRAFANA_REMOTE_WRITE_URL` environment variable.
