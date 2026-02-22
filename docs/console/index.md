# WitFoo Console

The WitFoo Console is the centralized management interface for multi-appliance WitFoo deployments. It provides fleet-wide visibility, appliance registration, and configuration management.

## Overview

| Component | Technology |
|-----------|-----------|
| Frontend | SvelteKit with Carbon Design System |
| Backend | Go with Echo framework |
| Database | SQLite (embedded) |
| Real-time | WebSocket |

## Key Features

### Appliance Management
- Register and monitor Conductor and Analytics appliances
- View real-time health status across the fleet
- Approve or reject appliance registration requests

### User Management
- Local and LDAP authentication
- Role-based access control (Administrator, Analyst, Viewer)
- Session-based security with encrypted cookies

### Disconnected Network Support
- Self-hosted IBM Plex fonts for air-gapped deployments
- No external CDN dependencies
- All static assets bundled locally

## Access

The Console runs on the designated Console node and is accessed via HTTPS:

```
https://<console-hostname>/
```

## Deployment

The Console is deployed as a Docker container managed by WFA:

```
ghcr.io/witfoo-dev/console-ui:main
```

For deployment configuration, see the [WFA Integration](../conductor/wfa-integration.md) guide.
