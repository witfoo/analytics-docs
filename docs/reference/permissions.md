# Permissions Reference

Complete list of WitFoo Analytics permissions.

## Permission List

| Permission | Description |
| --- | --- |
| `admin` | Full administrative access (grants all other permissions) |
| `signals:read` | View artifacts, incidents, nodes, edges |
| `signals:write` | Create/edit lead rules, classification rules, saved searches |
| `signals:manage` | Delete signals data, manage enrichment settings |
| `observer:read` | View work units, collections, MO definitions, observations |
| `observer:write` | Create/edit observer data |
| `observer:manage` | Delete observer data, manage MO definitions |
| `reports:read` | View all Reporter sections |
| `reports:write` | Export reports (CSV) |
| `reports:manage` | Configure report settings |
| `frameworks:read` | View compliance frameworks and controls |
| `frameworks:write` | Edit framework associations |
| `frameworks:manage` | Enable/disable frameworks, set primary, sync |
| `cybergrid:read` | View subscriptions, publications, library |
| `cybergrid:write` | Manage subscriptions, trigger syncs |
| `cybergrid:manage` | Create publications, manage feeds |
| `health:read` | View container metrics and health dashboard |
| `health:manage` | Configure health alerts |
| `metrics:read` | Access Prometheus metrics endpoint |
| `settings:read` | View system settings |
| `settings:manage` | Modify all settings (business, auth, notifications, certs) |
| `ai:read` | Use AI chat interface |
| `ai:write` | Manage chat sessions |
| `ai:manage` | Configure AI providers and MCP |
| `ai:export` | Export chat transcripts |
| `conductor:read` | View Conductor UI |
| `conductor:write` | Configure Conductor |
| `conductor:admin` | Full Conductor administration |

## Hierarchy

```text
admin → (all permissions)
resource:manage → resource:write → resource:read
```
