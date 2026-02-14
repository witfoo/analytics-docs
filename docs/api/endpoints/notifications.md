# Notifications

Notification channel and rule management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/notification-channels` | `settings:manage` | List channels |
| POST | `/v1/notification-channels` | `settings:manage` | Create channel |
| PUT | `/v1/notification-channels/:id` | `settings:manage` | Update channel |
| DELETE | `/v1/notification-channels/:id` | `settings:manage` | Delete channel |
| POST | `/v1/notification-channels/:id/test` | `settings:manage` | Test channel |
| GET | `/v1/notification-rules` | `settings:manage` | List rules |
| POST | `/v1/notification-rules` | `settings:manage` | Create rule |
| PUT | `/v1/notification-rules/:id` | `settings:manage` | Update rule |
| DELETE | `/v1/notification-rules/:id` | `settings:manage` | Delete rule |

## Channel Types

- **email** — SMTP configuration
- **slack** — Webhook URL
- **webhook** — Custom HTTP endpoint
