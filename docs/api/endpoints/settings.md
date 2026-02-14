# Settings

Organization-wide configuration management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/settings/business` | `settings:read` | Get business settings |
| PUT | `/v1/settings/business` | `settings:manage` | Update business settings |
| GET | `/v1/settings/products` | `settings:read` | List product costs |
| PUT | `/v1/settings/products` | `settings:manage` | Update product costs |

## Business Settings Object

```json
{
  "annual_revenue": 50000000,
  "annual_security_spend": 2500000,
  "fte_count": 5,
  "investigation_time_hours": 1.5,
  "restore_time_hours": 0.75,
  "fte_hourly_rate": 75.0,
  "product_costs": {
    "Palo Alto": 150000,
    "CrowdStrike": 200000
  }
}
```
