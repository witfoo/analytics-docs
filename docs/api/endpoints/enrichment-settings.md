# Enrichment Settings

Configure artifact and node enrichment.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/enrichment-settings` | `signals:read` | Get settings |
| PUT | `/v1/enrichment-settings` | `signals:manage` | Update settings |

## Settings Object

```json
{
  "geoip_enabled": true,
  "dns_enabled": true,
  "whois_enabled": false,
  "threat_intel_enabled": true,
  "rate_limit": 60,
  "cache_ttl_hours": 24
}
```
