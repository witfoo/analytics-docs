# Roles

Roles define what users can access in WitFoo Analytics. Each user is assigned exactly one role.

## Built-in Roles

| Role | Description | Key Permissions |
| --- | --- | --- |
| **Admin** | Full system access | All permissions |
| **Analyst** | Security analyst | Signals, graph, observer, reports |
| **Auditor** | Compliance auditor | Read-only reports and frameworks |
| **ReadOnly** | Stakeholder view | Read-only dashboards |
| **HealthMonitor** | Operations staff | Health and metrics |
| **CyberGridManager** | Intel analyst | CyberGrid operations |
| **Reporter** | Report consumer | Reports read-only |
| **AIUser** | AI assistant user | AI chat and read access |

## Permission Inclusion Rules

- `admin` permission grants ALL other permissions
- `resource:manage` grants `resource:write` and `resource:read`
- `resource:write` grants `resource:read`

## Custom Roles

1. Navigate to **Admin** > **Roles**
2. Click **Create Role**
3. Enter a role name
4. Select permissions from the checklist
5. Click **Save**

## Role Assignment

Change a user's role from **Admin** > **Users** > Edit user > Role dropdown.
