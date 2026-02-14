# Notifications

Configure notification channels and rules for automated alerting.

## Notification Channels

### Email (SMTP)

| Setting | Description |
| --- | --- |
| **SMTP Host** | Mail server hostname |
| **SMTP Port** | Mail server port (25, 465, 587) |
| **Username** | SMTP authentication username |
| **Password** | SMTP authentication password |
| **From Address** | Sender email address |
| **TLS Mode** | None, StartTLS, or TLS |

### Slack

| Setting | Description |
| --- | --- |
| **Webhook URL** | Slack incoming webhook URL |
| **Channel** | Default channel (optional) |

### Webhook

| Setting | Description |
| --- | --- |
| **URL** | HTTP endpoint |
| **Method** | POST, PUT, or PATCH |
| **Auth Type** | None, Bearer token, or Basic auth |
| **Headers** | Custom HTTP headers |

## Testing Channels

Click **Test** on any channel to send a test notification and verify connectivity.

## Notification Rules

Create rules that trigger notifications on specific events:

- `incident.created` — New incident detected
- `incident.status_changed` — Incident status updated
- `incident.severity_changed` — Severity escalation/de-escalation
- `incident.assigned` — Incident assigned to analyst
- `incident.note_added` — Note added to incident

### Cooldown

Each rule has a cooldown period (default: 15 minutes) preventing duplicate notifications for the same condition.

## Configuration

Navigate to **Admin** > **Settings** > **Notifications**. Requires `settings:manage` permission.

!!! info "Encryption"
    Channel credentials are encrypted at rest. Set `AUTH_CONFIG_ENCRYPTION_KEY` environment variable.
