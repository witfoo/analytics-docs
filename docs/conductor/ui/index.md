# Conductor UI Overview

The Conductor UI is a web-based management interface for configuring and monitoring the Conductor pipeline. It provides real-time dashboards, service configuration, user management, and system health monitoring.

## Access

The Conductor UI runs internally on port **8000** and is served externally via an HTTPS reverse proxy on port **443**.

```
https://<conductor-hostname>/
```

!!! danger "Default Credentials"
    The default administrator account is:

    - **Email:** `admin@witfoo.com`
    - **Password:** `F00theN0ise!`

    Change the default password immediately after first login via **Account Settings** (`/account`).

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | SvelteKit with Carbon Design System |
| Backend | Go with Echo framework |
| Database | SQLite (embedded) |
| Real-time | WebSocket with HTTP polling fallback (5-second interval) |
| Session | Encrypted cookies |

## Route Table

| Route | Purpose |
|-------|---------|
| `/` | [Dashboard](dashboard.md) (4 tabs: Overview, Pipeline, Service Status, Container Status) |
| `/auth/login` | Authentication |
| `/account` | User profile and password settings |
| `/admin/users` | [User Management](users.md) |
| `/admin/settings/processors` | [Parser Configuration](parsers.md) |
| `/admin/settings/integrations` | [API Integration Management](integrations.md) |
| `/admin/settings/artifact-exporters` | [Export Destination Configuration](exporters.md) |
| `/admin/settings/log-servers` | [Log Server Configuration](log-servers.md) |
| `/admin/settings/notifications` | [Notification Management](notifications.md) |

## Real-Time Updates

The dashboard uses WebSocket connections for real-time metric streaming. A pulsating dot indicator in the UI shows the WebSocket connection status:

- **Green (pulsating)** — WebSocket connected, receiving live updates
- **Gray** — Disconnected, automatic fallback to HTTP polling at 5-second intervals

The UI implements automatic WebSocket reconnection with metrics throttling (250 metric cap) to prevent UI flooding during high-throughput periods.