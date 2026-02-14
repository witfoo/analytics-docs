# WFA

WitFoo Appliance (WFA) management endpoints.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/wfa/health` | `health:read` | WFA health status |
| GET | `/v1/wfa/stats` | `metrics:read` | WFA statistics |
| GET | `/v1/wfa/config` | `settings:read` | Current WFA configuration |
| PUT | `/v1/wfa/config` | `settings:manage` | Update WFA configuration |

## WFA Health Response

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "role": "analytics-aio",
    "uptime": "7d 12h 30m",
    "version": "1.0.0"
  }
}
```

## WFA Metrics

Metrics use the `witfoo_wfa_*` Prometheus prefix, distinct from `witfoo_container_*` infrastructure metrics.
