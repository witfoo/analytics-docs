# Saved Searches

Manage saved search queries for quick access.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/saved-searches` | `signals:read` | List saved searches |
| GET | `/v1/saved-searches/:id` | `signals:read` | Get saved search |
| POST | `/v1/saved-searches` | `signals:write` | Create saved search |
| PUT | `/v1/saved-searches/:id` | `signals:write` | Update saved search |
| DELETE | `/v1/saved-searches/:id` | `signals:write` | Delete saved search |

## Saved Search Object

```json
{
  "id": "uuid",
  "name": "Critical Firewall Alerts",
  "query": "severity:critical AND source:firewall",
  "filters": {},
  "created_by": "uuid",
  "shared": false
}
```
