# Roles Reference

WitFoo Analytics 1.2.0 ships 9 built-in roles. This page lists what each one holds.

## Built-in roles

| Role | Description | Holds |
| --- | --- | --- |
| **Admin** | Full system access - all permissions | `admin`, so every permission |
| **Analyst** | Read-only access to all data, plus the AI chat assistant | Read permissions for signals, the graph, work units, Observer, reports, frameworks, Auditor, Certifications, CyberGrid publications and subscriptions, settings, users and roles; `ai:read` and `ai:write` |
| **ReadOnly** | Read-only access to all data, plus the AI chat assistant | The same as Analyst, without `auditor:read` and `certifications:read` |
| **Report Viewer** | View and export reports, plus the AI chat assistant | `reports:read`, `reports:export`, `frameworks:read`, `certifications:read`, `auditor:read`, `ai:read`, `ai:write` |
| **Report Admin** | Full reporter module administration | All four `reports:` permissions, all three `frameworks:` permissions, `certifications:read` and `certifications:write`, `settings:read`, `settings:write`, `settings:products:read`, `settings:products:write`, `auditor:read`, `ai:read`, `ai:write` |
| **CyberGrid Viewer** | View CyberGrid resources, plus the AI chat assistant | `cybergrid:publications:read`, `cybergrid:subscriptions:read`, `cybergrid:queue:monitor`, `cybergrid:directory:read`, `ai:read`, `ai:write` |
| **CyberGrid Admin** | Full CyberGrid administration | `cybergrid:manage` and every CyberGrid read and write permission, `ai:read`, `ai:write` |
| **Framework Manager** | Compliance framework administration | All three `frameworks:` permissions, `reports:read`, `settings:read`, `settings:write`, `ai:read`, `ai:write` |
| **Platform Admin** | Cross-tenant platform administrator with full platform management capabilities | `admin` and the six `platform:` permissions |

!!! note "Role descriptions on an existing appliance"
    The descriptions above are the ones 1.2.0 seeds for new installs and new tenants. An appliance that was installed earlier keeps the descriptions it already has.

Built-in roles are read-only: they cannot be edited or deleted. To give someone a different set of permissions, create a custom role. See [Admin Guide: Roles](../admin-guide/roles.md).

## Admin and Platform Admin

**Admin** holds `admin`, which grants every permission, including `mcp:connect`. It is also seeded with most permissions by name, among them `mcp:manage`.

**Platform Admin** holds `admin` and the platform permissions: `platform:read`, `platform:write`, `platform:manage`, `platform:conductor:admin`, `platform:users:admin` and `platform:switch`.

## Permission matrix of the other roles

A ✓ means the role is seeded with the permission. The [inclusion rules](permissions.md) still apply: for example, CyberGrid Admin's `cybergrid:manage` grants every `cybergrid:` permission.

| Permission | Analyst | ReadOnly | Report Viewer | Report Admin | Framework Manager | CyberGrid Viewer | CyberGrid Admin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `signals:read` | ✓ | ✓ |  |  |  |  |  |
| `nodes:read` | ✓ | ✓ |  |  |  |  |  |
| `edges:read` | ✓ | ✓ |  |  |  |  |  |
| `graph:read` | ✓ | ✓ |  |  |  |  |  |
| `work_units:read` | ✓ | ✓ |  |  |  |  |  |
| `work_definitions:read` | ✓ | ✓ |  |  |  |  |  |
| `observations:read` | ✓ | ✓ |  |  |  |  |  |
| `collections:read` | ✓ | ✓ |  |  |  |  |  |
| `reports:read` | ✓ | ✓ | ✓ | ✓ | ✓ |  |  |
| `reports:write` |  |  |  | ✓ |  |  |  |
| `reports:generate` |  |  |  | ✓ |  |  |  |
| `reports:export` |  |  | ✓ | ✓ |  |  |  |
| `frameworks:read` | ✓ | ✓ | ✓ | ✓ | ✓ |  |  |
| `frameworks:write` |  |  |  | ✓ | ✓ |  |  |
| `frameworks:manage` |  |  |  | ✓ | ✓ |  |  |
| `cybergrid:publications:read` | ✓ | ✓ |  |  |  | ✓ | ✓ |
| `cybergrid:publications:write` |  |  |  |  |  |  | ✓ |
| `cybergrid:subscriptions:read` | ✓ | ✓ |  |  |  | ✓ | ✓ |
| `cybergrid:subscriptions:write` |  |  |  |  |  |  | ✓ |
| `cybergrid:jobs:approve` |  |  |  |  |  |  | ✓ |
| `cybergrid:library:write` |  |  |  |  |  |  | ✓ |
| `cybergrid:queue:monitor` |  |  |  |  |  | ✓ | ✓ |
| `cybergrid:manage` |  |  |  |  |  |  | ✓ |
| `cybergrid:directory:read` |  |  |  |  |  | ✓ | ✓ |
| `settings:read` | ✓ | ✓ |  | ✓ | ✓ |  |  |
| `settings:write` |  |  |  | ✓ | ✓ |  |  |
| `settings:products:read` |  |  |  | ✓ |  |  |  |
| `settings:products:write` |  |  |  | ✓ |  |  |  |
| `users:read` | ✓ | ✓ |  |  |  |  |  |
| `roles:read` | ✓ | ✓ |  |  |  |  |  |
| `ai:read` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ai:write` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `auditor:read` | ✓ |  | ✓ | ✓ |  |  |  |
| `certifications:read` | ✓ |  | ✓ | ✓ |  |  |  |
| `certifications:write` |  |  |  | ✓ |  |  |  |

## MCP access

No built-in role is seeded with `mcp:connect`. Admin and Platform Admin can connect an MCP client because `admin` grants it. Any role that holds `mcp:manage` can too. Everyone else needs a custom role that holds `mcp:connect`. The platform-administrator flag and `platform:manage` do not grant it.

## The in-app AI assistant

Every built-in role holds `ai:read` and `ai:write`, directly or through `admin`. Reading your chat sessions needs `ai:read`. Sending a message, or starting, renaming or deleting a session, needs `ai:write`.

When an appliance first starts 1.2.0, every custom role that exists at that moment is given both permissions once. Removing them afterwards sticks. Custom roles created later do not get them automatically.
