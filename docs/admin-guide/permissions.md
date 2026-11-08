# Permissions

WitFoo Analytics 1.2.0 uses a granular permission system with 108 permissions across 22 categories. Every permission is listed, with its label and description, in the [Permissions Reference](../reference/permissions.md).

## Permission Categories

| Category | Permissions | Description |
| --- | --- | --- |
| **Signals** | read, write, delete, export, manage | Signal Search and artifact data |
| **Graph - Nodes** | read, write, delete, export, manage | Graph nodes |
| **Graph - Edges** | read, write, delete, export, manage | Graph edges |
| **Graph** | read, write | The whole graph surface (nodes and edges) |
| **Work Units** | read, write, delete, export, manage | Work units (incidents) |
| **Observer** | `work_definitions:*`, `observations:*`, `collections:read`, `collections:write` | Work Definitions, observations and work collections |
| **Reporter** | `reports:read`, `reports:write`, `reports:generate`, `reports:export`, `frameworks:read`, `frameworks:write`, `frameworks:manage` | Reporter pages and compliance frameworks |
| **CyberGrid** | publications, subscriptions, jobs, library, queue, directory, manage | Threat-intelligence sharing |
| **Settings** | `settings:read`, `settings:write`, `settings:products:read`, `settings:products:write`, `settings:manage` | System and business settings, product catalog |
| **Administration** | `users:read`, `users:write`, `roles:read`, `roles:write`, `admin` | User and role administration |
| **Health Dashboard** | `health:read`, `health:manage`, `metrics:read`, `metrics:export` | System health and metrics |
| **AI Assistant** | `ai:read`, `ai:write`, `ai:manage`, `ai:export`, `mcp:manage`, `mcp:connect` | The in-app assistant, AI providers and MCP |
| **Conductor** | read, write, admin | Conductor pipeline management |
| **Dashboards** | read, write, delete, manage | Custom dashboards |
| **Playbooks** | read, write, delete, manage | Playbooks |
| **Tasks** | read, write, delete, manage | Tasks |
| **Responders** | read, write, delete, manage | Responder jobs |
| **Platform Administration** | `platform:read`, `platform:write`, `platform:manage`, `platform:conductor:admin`, `platform:users:admin`, `platform:switch` | Cross-tenant administration |
| **Auditor** | read, write, delete, execute, manage | Auditor findings, runs and connectors |
| **Certifications** | read, write | Certify packages |
| **Chat** | read, write, manage, `chat:ai` | Chat rooms |
| **Attachments** | read, write, delete, manage | File attachments |

## Permission Hierarchy

```text
admin → (all permissions)
resource:manage → resource:* (write, read, delete, export, ...)
resource:write → resource:read
```

- `admin` grants every permission in every category.
- `{resource}:manage` grants every `{resource}:*` permission. `mcp:manage` grants `mcp:connect`.
- `{resource}:write` grants `{resource}:read`.

The platform-administrator flag and `platform:manage` do not grant `mcp:connect`.

## Service-Level Rules

- A route that requires a permission answers `403` when the caller lacks it.
- The `admin` permission (label **Administrator**) gates user and role administration. `users:write`, `roles:read` and `roles:write` are reserved for it.
- The api reads permissions from the user's session token, which is issued at sign-in. A role change reaches a user at their next sign-in, and a cached decision can last up to 5 more minutes. MCP connections read the user's roles on every request. See [When role changes apply](roles.md).

## Permissions that changed in 1.2.0

| Permission | Change |
| --- | --- |
| `mcp:connect` (Connect MCP) | New. Needed to connect an MCP client, create personal MCP keys and approve app sign-ins |
| `mcp:manage` (Manage MCP) | Sets the organization's MCP mode and manages every MCP key and connected app in it. It can no longer create organization-wide keys, which are retired |
| `ai:read`, `ai:write` | Now gate the in-app AI assistant. Every built-in role holds both, and every custom role that existed at the upgrade was given both once |
| `dashboards:write` | Now needed to create, update, delete and clone a dashboard. Marking a favorite still needs only `dashboards:read` |
| `signals:read`, `signals:manage` | Now checked on classification rules and enrichment settings |
| `frameworks:read`, `frameworks:write` | Now checked on the compliance frameworks API |
| CyberGrid permissions | Now checked on every CyberGrid route |
