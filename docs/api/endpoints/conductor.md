# Conductor

Manage the Conductor signal pipeline.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/conductor/status` | `conductor:read` | Pipeline status |
| GET | `/v1/conductor/services` | `conductor:read` | List Conductor services |
| POST | `/v1/conductor/restart` | `conductor:admin` | Restart pipeline |

## Proxy Routes

Conductor UI requests are proxied through the Analytics reverse proxy at `/conductor/`. JWT tokens are validated and mapped to Conductor roles via the ConductorAuth middleware.

| Analytics Permission | Conductor Role |
| --- | --- |
| `conductor:admin` | Superuser |
| `conductor:write` | Admin |
| `conductor:read` | Staff |
