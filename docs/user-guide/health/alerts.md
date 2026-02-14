# Alerts

Configurable notifications when container metrics exceed thresholds.

## Alert Types

| Type | Triggers On |
| --- | --- |
| **CPU** | CPU exceeds threshold for duration |
| **Memory** | Memory exceeds threshold |
| **Disk** | Disk exceeds threshold |
| **Container State** | Container stops/unhealthy/restarting |
| **Restart Count** | Restarts exceed N in window |

## Creating Alert Rules

1. Navigate to **Health** > **Alerts**
2. Click **Create Alert**
3. Select type, container, threshold, duration, severity
4. Choose notification channels
5. Click **Save**

The form adapts based on alert type — CPU/Memory/Disk show threshold/duration; Container State shows state selector; Restart Count shows count/window fields.

## Cooldown

Default 15-minute cooldown per alert type + severity + container combination. Prevents notification spam during sustained issues.

## Notification Channels

| Channel | Format |
| --- | --- |
| **Email** | HTML with severity-colored header |
| **Slack** | Block Kit structured message |
| **Webhook** | JSON payload |

Configure channels in **Admin** > **Settings** > **Notifications**.

## Alert History

Retained for 30 days with timestamp, type, severity, container, metric value, and notification status.
