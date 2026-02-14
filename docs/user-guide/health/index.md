# Health

Real-time monitoring of your WitFoo Analytics deployment.

## Components

### [Containers](containers.md)

Real-time and historical metrics for all Docker containers. Auto-refreshes every 15 seconds.

### [Alerts](alerts.md)

Configurable alert rules for container metrics and service availability.

## Dashboard Overview

- **Service status cards** — Clickable tiles showing container state with CPU/memory gauges
- **KPI tiles** — Total containers, healthy count, average CPU/memory
- **Historical charts** — Time-series resource usage (limited to 100 data points)

## Container States

| State | Color |
| --- | --- |
| **Running** | Green |
| **Unhealthy** | Yellow |
| **Stopped** | Red |
| **Restarting** | Orange |

## Auto-Refresh

Updates every 15 seconds via silent background requests.

## Permissions

| Action | Required Permission |
| --- | --- |
| View health data | `health:read` |
| Configure alerts | `health:manage` |
| View metrics | `metrics:read` |
