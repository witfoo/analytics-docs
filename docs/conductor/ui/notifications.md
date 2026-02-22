# Notifications

**URL:** `/admin/settings/notifications`

The Notifications page manages alerting channels and rules for Conductor system events. Configure email, Slack, and webhook destinations to receive automated alerts when pipeline issues occur.

## Notification Channels

Channels define where notifications are delivered. Multiple channels can be active simultaneously.

### Email (SMTP)

| Setting | Description |
| --- | --- |
| **SMTP Host** | Mail server hostname |
| **SMTP Port** | Mail server port (25, 465, 587) |
| **Username** | SMTP authentication username |
| **Password** | SMTP authentication password |
| **From Address** | Sender email address |
| **From Name** | Sender display name |
| **TLS Mode** | None, StartTLS, or TLS (minimum TLS 1.2) |
| **Recipients** | Comma-separated email addresses |

### Slack

| Setting | Description |
| --- | --- |
| **Webhook URL** | Slack incoming webhook URL |
| **Channel** | Target channel (e.g., `#alerts`) |
| **Username** | Bot display name |

### Webhook

| Setting | Description |
| --- | --- |
| **URL** | HTTP endpoint for notification delivery |
| **Method** | HTTP method (POST, PUT, PATCH) |
| **Auth Type** | None or Bearer token |
| **Auth Token** | Bearer token value (when auth type is Bearer) |
| **Headers** | Custom HTTP headers as key-value pairs |

!!! tip "Testing Channels"
    Click **Test** on any channel to send a test notification and verify connectivity before creating rules.

## Notification Rules

Rules define which system events trigger notifications and to which channels they are routed.

### Event Types

| Event | Description |
| --- | --- |
| `parser.failure` | Signal parser encountered a processing error |
| `exporter.failure` | Artifact exporter failed to deliver to destination |
| `system.capacity_warning` | Pipeline approaching capacity limits |
| `system.service_down` | A Conductor service is unreachable |
| `system.cert_expiring` | TLS certificate nearing expiration |
| `auth.failure` | Authentication attempt failed |
| `system.config_changed` | System configuration was modified |

### Rule Configuration

| Field | Description |
| --- | --- |
| **Name** | Human-readable rule name |
| **Description** | Purpose of the rule |
| **Event Types** | One or more events that trigger this rule |
| **Channels** | One or more channels to notify |
| **Cooldown** | Minimum minutes between repeated notifications (default: 15) |
| **Enabled** | Toggle rule on/off |

!!! info "Cooldown"
    The cooldown period prevents notification storms. If the same rule fires multiple times within the cooldown window, only the first notification is sent. Subsequent events are recorded in the history as `skipped`.

## Notification History

The History tab displays a log of all notification attempts with:

| Column | Description |
| --- | --- |
| **Timestamp** | When the notification was attempted |
| **Event Type** | The triggering event |
| **Channel** | Target channel name |
| **Rule** | Rule that triggered the notification |
| **Status** | `sent`, `failed`, or `skipped` |
| **Message** | Event details or error message |

## API Endpoints

All endpoints require session authentication.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/v1/notifications/channels` | List all channels |
| `POST` | `/api/v1/notifications/channels` | Create a channel |
| `GET` | `/api/v1/notifications/channels/:id` | Get channel by UUID |
| `PUT` | `/api/v1/notifications/channels/:id` | Update a channel |
| `DELETE` | `/api/v1/notifications/channels/:id` | Delete a channel |
| `POST` | `/api/v1/notifications/channels/:id/test` | Send test notification |
| `GET` | `/api/v1/notifications/rules` | List all rules |
| `POST` | `/api/v1/notifications/rules` | Create a rule |
| `GET` | `/api/v1/notifications/rules/:id` | Get rule by UUID |
| `PUT` | `/api/v1/notifications/rules/:id` | Update a rule |
| `DELETE` | `/api/v1/notifications/rules/:id` | Delete a rule |
| `GET` | `/api/v1/notifications/history` | List notification history |

!!! warning "Sensitive Fields"
    Channel credentials (passwords, tokens, webhook URLs) are redacted in API responses. To update credentials, include the new value in the PUT request body.
