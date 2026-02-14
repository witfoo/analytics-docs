# Health Dashboard

Container metrics and system health monitoring.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/health/containers` | `health:read` | List container metrics |
| GET | `/v1/health/containers/:name` | `health:read` | Container detail |
| GET | `/v1/health/containers/:name/history` | `health:read` | Historical metrics |
| GET | `/v1/health/alerts` | `health:read` | List active alerts |
| POST | `/v1/health/alerts` | `health:manage` | Create alert rule |
| PUT | `/v1/health/alerts/:id` | `health:manage` | Update alert rule |
| DELETE | `/v1/health/alerts/:id` | `health:manage` | Delete alert rule |
| GET | `/v1/metrics` | `metrics:read` | Prometheus metrics |
