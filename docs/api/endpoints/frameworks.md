# Frameworks

Compliance framework management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/frameworks` | `frameworks:read` | List all frameworks |
| GET | `/v1/frameworks/enabled` | `frameworks:read` | List enabled frameworks |
| PUT | `/v1/frameworks/:id/enable` | `frameworks:manage` | Enable framework |
| PUT | `/v1/frameworks/:id/disable` | `frameworks:manage` | Disable framework |
| PUT | `/v1/frameworks/:id/primary` | `frameworks:manage` | Set as primary |
| GET | `/v1/frameworks/:id/controls` | `frameworks:read` | List controls |
| POST | `/v1/frameworks/sync` | `frameworks:manage` | Sync from Intel API |

## Framework Object

```json
{
  "id": "uuid",
  "name": "CIS CSC v8",
  "machine_name": "cis_csc_v8",
  "enabled": true,
  "is_primary": true,
  "control_count": 153
}
```
