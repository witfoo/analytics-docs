# CyberGrid

Threat intelligence feed management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/cybergrid/subscriptions` | `cybergrid:read` | List subscriptions |
| POST | `/v1/cybergrid/subscriptions` | `cybergrid:write` | Subscribe to feed |
| DELETE | `/v1/cybergrid/subscriptions/:id` | `cybergrid:write` | Unsubscribe |
| GET | `/v1/cybergrid/publications` | `cybergrid:read` | List publications |
| POST | `/v1/cybergrid/publications` | `cybergrid:manage` | Create publication |
| GET | `/v1/cybergrid/jobs` | `cybergrid:read` | List sync jobs |
| POST | `/v1/cybergrid/sync` | `cybergrid:write` | Trigger manual sync |
| GET | `/v1/cybergrid/library` | `cybergrid:read` | Browse library |
| GET | `/v1/cybergrid/search` | `cybergrid:read` | Search indicators |
