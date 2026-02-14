# Classification Rules

Manage automatic incident classification rules.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/classification-rules` | `signals:read` | List rules |
| GET | `/v1/classification-rules/:id` | `signals:read` | Get rule |
| POST | `/v1/classification-rules` | `signals:write` | Create rule |
| PUT | `/v1/classification-rules/:id` | `signals:write` | Update rule |
| DELETE | `/v1/classification-rules/:id` | `signals:manage` | Delete rule |

## Rule Object

```json
{
  "id": "uuid",
  "name": "Critical Infrastructure Alert",
  "priority": 10,
  "enabled": true,
  "severity": "critical",
  "target_infrastructure": true,
  "conditions": {}
}
```
