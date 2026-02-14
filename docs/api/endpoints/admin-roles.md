# Admin Roles

Manage role definitions and permission assignments.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/roles` | `admin` | List all roles |
| GET | `/v1/roles/:id` | `admin` | Get role details |
| POST | `/v1/roles` | `admin` | Create role |
| PUT | `/v1/roles/:id` | `admin` | Update role |
| DELETE | `/v1/roles/:id` | `admin` | Delete role |

## Role Object

```json
{
  "id": "uuid",
  "name": "analyst",
  "permissions": ["signals:read", "signals:write", "observer:read"],
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z"
}
```
