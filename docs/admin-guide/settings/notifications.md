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

Open **Settings** (the gear icon in the page header) > **General Settings** > **Notifications**. Rules are on the **Notification Rules** page, listed beside it. Requires the `settings:manage` permission.

!!! info "Encryption"
    Notification-channel configurations are encrypted at rest with XChaCha20-Poly1305, under a per-organization key derived from `AUTH_CONFIG_ENCRYPTION_KEY`. On a WFA-managed appliance WFA supplies the key. On Docker Compose or a standalone stack the key is required: see [Upgrading to 1.2.0](../../reference/upgrade-1.2.0.md).

!!! note "Rule-driven notifications in 1.2.0"
    Before 1.2.0, rule-driven notifications (a work unit created or its status changed) could not open their channel, so they were never delivered and wrote no history. 1.2.0 fixes this: after the upgrade, rules that never delivered start delivering, beginning with the first matching event. The `NOTIFICATION_ENCRYPTION_KEY` setting and its startup warning are removed; channels use `AUTH_CONFIG_ENCRYPTION_KEY`.
