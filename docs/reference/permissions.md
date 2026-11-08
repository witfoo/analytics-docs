# Permissions Reference

WitFoo Analytics 1.2.0 defines 108 permissions across 22 categories. This page lists every one, with the label that **Role Management** shows for it.

## How permissions combine

Three rules decide what a role can do:

- `admin` grants every permission.
- `{resource}:manage` grants every `{resource}:*` permission. For example, `cybergrid:manage` grants every `cybergrid:` permission, and `mcp:manage` grants `mcp:connect`.
- `{resource}:write` grants `{resource}:read`.

```text
admin → (all permissions)
resource:manage → resource:* (write, read, delete, export, ...)
resource:write → resource:read
```

Two things do **not** grant `mcp:connect`: the platform-administrator flag on an account, and `platform:manage`. A user can connect an MCP client only when one of their roles holds `mcp:connect`, `mcp:manage` or `admin`.

!!! note "Reserved permissions"
    `users:write`, `roles:read` and `roles:write` are reserved. User and role administration is gated by the `admin` permission (label **Administrator**), and **Role Management** marks these three as reserved for it.

## Permission catalog

### Signals

| Permission | Label | Description |
| --- | --- | --- |
| `signals:read` | Read Signals | View signals page and search results |
| `signals:write` | Write Signals | Create and modify signal data |
| `signals:delete` | Delete Signals | Delete signal records |
| `signals:export` | Export Signals | Export signal data to CSV/JSON |
| `signals:manage` | Manage Signals | All signal operations (includes read, write, delete, export) |

### Graph - Nodes

| Permission | Label | Description |
| --- | --- | --- |
| `nodes:read` | Read Nodes | View graph nodes |
| `nodes:write` | Write Nodes | Create and modify graph nodes |
| `nodes:delete` | Delete Nodes | Delete graph nodes |
| `nodes:export` | Export Nodes | Export node data |
| `nodes:manage` | Manage Nodes | All node operations (includes read, write, delete, export) |

### Graph - Edges

| Permission | Label | Description |
| --- | --- | --- |
| `edges:read` | Read Edges | View graph edges |
| `edges:write` | Write Edges | Create and modify graph edges |
| `edges:delete` | Delete Edges | Delete graph edges |
| `edges:export` | Export Edges | Export edge data |
| `edges:manage` | Manage Edges | All edge operations (includes read, write, delete, export) |

### Graph

| Permission | Label | Description |
| --- | --- | --- |
| `graph:read` | Read Graph | View the whole graph surface (nodes and edges) |
| `graph:write` | Write Graph | Create and modify graph data (includes read) |

### Work Units

| Permission | Label | Description |
| --- | --- | --- |
| `work_units:read` | Read Work Units | View work units and incidents |
| `work_units:write` | Write Work Units | Modify work unit status and assignments |
| `work_units:delete` | Delete Work Units | Delete work units |
| `work_units:export` | Export Work Units | Export work unit data |
| `work_units:manage` | Manage Work Units | All work unit operations (includes read, write, delete, export) |

### Observer

| Permission | Label | Description |
| --- | --- | --- |
| `work_definitions:read` | Read Work Definitions | View MO definitions |
| `work_definitions:write` | Write Work Definitions | Create and modify MO definitions |
| `work_definitions:delete` | Delete Work Definitions | Delete MO definitions |
| `work_definitions:manage` | Manage Work Definitions | All work definition operations |
| `observations:read` | Read Observations | View observations |
| `observations:write` | Write Observations | Create and modify observations |
| `observations:delete` | Delete Observations | Delete observations |
| `observations:manage` | Manage Observations | All observation operations |
| `collections:read` | Read Collections | View work collections |
| `collections:write` | Write Collections | Create and modify work collections |

### Reporter

| Permission | Label | Description |
| --- | --- | --- |
| `reports:read` | Read Reports | View all reporter dashboards |
| `reports:write` | Write Reports | Modify report parameters |
| `reports:generate` | Generate Reports | Generate new reports on demand |
| `reports:export` | Export Reports | Export reports to PDF/CSV |
| `frameworks:read` | Read Frameworks | View compliance frameworks |
| `frameworks:write` | Write Frameworks | Modify framework assignments |
| `frameworks:manage` | Manage Frameworks | Full framework administration |

### CyberGrid

| Permission | Label | Description |
| --- | --- | --- |
| `cybergrid:publications:read` | Read CyberGrid Publications | View publications |
| `cybergrid:publications:write` | Write CyberGrid Publications | Create and modify publications |
| `cybergrid:subscriptions:read` | Read CyberGrid Subscriptions | View subscriptions |
| `cybergrid:subscriptions:write` | Write CyberGrid Subscriptions | Create and modify subscriptions |
| `cybergrid:jobs:approve` | Approve CyberGrid Jobs | Approve or reject pending jobs |
| `cybergrid:library:write` | Submit to CyberGrid Library | Submit IOCs to threat intelligence library |
| `cybergrid:queue:monitor` | Monitor CyberGrid Queue | View queue statistics and health |
| `cybergrid:manage` | Manage CyberGrid | Full CyberGrid administration |
| `cybergrid:directory:read` | Read CyberGrid Directory | View the CyberGrid user directory |

### Settings

| Permission | Label | Description |
| --- | --- | --- |
| `settings:read` | Read Settings | View business settings |
| `settings:write` | Write Settings | Modify business settings |
| `settings:products:read` | Read Product Catalog | View product catalog and costs |
| `settings:products:write` | Write Product Catalog | Modify product costs |
| `settings:manage` | Manage Settings | All settings operations |

### Administration

| Permission | Label | Description |
| --- | --- | --- |
| `users:read` | Read Users | View user accounts |
| `users:write` | Write Users | Reserved: user administration is gated by the Administrator permission |
| `roles:read` | Read Roles | Reserved: viewing roles is gated by the Administrator permission |
| `roles:write` | Write Roles | Reserved: role administration is gated by the Administrator permission |
| `admin` | Administrator | Global administrator with all permissions |

### Health Dashboard

| Permission | Label | Description |
| --- | --- | --- |
| `health:read` | Read Health | View health dashboards and container status |
| `health:manage` | Manage Health | Manage health alert configurations |
| `metrics:read` | Read Metrics | Access Prometheus /metrics endpoint |
| `metrics:export` | Export Metrics | Export historical metrics data |

### AI Assistant

| Permission | Label | Description |
| --- | --- | --- |
| `ai:read` | Read AI | View AI features and read chat assistant sessions |
| `ai:write` | Write AI | Send messages; start, rename and delete chat sessions |
| `ai:manage` | Manage AI | Configure AI providers and their API keys, and open the AI Setup page (the MCP Authentication card on that page is shown only to holders of `mcp:manage`) |
| `ai:export` | Export AI | Export chat history and conversations |
| `mcp:manage` | Manage MCP | Set the organization's MCP mode; list and revoke any MCP key in the organization; with app sign-in on, register, edit and revoke OAuth clients and list and revoke the organization's connected apps. Implies `mcp:connect` |
| `mcp:connect` | Connect MCP | Create, rotate and revoke your own personal MCP keys, approve and revoke the apps that connect as you, and open an MCP session whose tools run with your own permissions. Grants no data tool by itself |

### Conductor

| Permission | Label | Description |
| --- | --- | --- |
| `conductor:read` | Read Conductor | View Conductor UI and pipeline status |
| `conductor:write` | Write Conductor | Modify pipeline configuration |
| `conductor:admin` | Manage Conductor | Full Conductor administration |

### Dashboards

| Permission | Label | Description |
| --- | --- | --- |
| `dashboards:read` | Read Dashboards | View custom dashboards and mark a dashboard as a favorite |
| `dashboards:write` | Write Dashboards | Create, update, delete and clone custom dashboards |
| `dashboards:delete` | Delete Dashboards | Delete custom dashboards. The dashboard routes do not check it: deleting a dashboard needs `dashboards:write` |
| `dashboards:manage` | Manage Dashboards | All dashboard operations (includes read, write, delete) |

### Playbooks

| Permission | Label | Description |
| --- | --- | --- |
| `playbooks:read` | Read Playbooks | View playbook definitions and execution history |
| `playbooks:write` | Write Playbooks | Create and modify playbook definitions |
| `playbooks:delete` | Delete Playbooks | Delete playbook definitions |
| `playbooks:manage` | Manage Playbooks | All playbook operations (includes read, write, delete, execute) |

### Tasks

| Permission | Label | Description |
| --- | --- | --- |
| `tasks:read` | Read Tasks | View task work items |
| `tasks:write` | Write Tasks | Create and modify task work items |
| `tasks:delete` | Delete Tasks | Delete task work items |
| `tasks:manage` | Manage Tasks | All task operations (includes read, write, delete) |

### Responders

| Permission | Label | Description |
| --- | --- | --- |
| `responders:read` | Read Responders | View responder job definitions and execution history |
| `responders:write` | Write Responders | Create and modify responder job definitions |
| `responders:delete` | Delete Responders | Delete responder job definitions |
| `responders:manage` | Manage Responders | All responder operations (includes read, write, delete, execute) |

### Platform Administration

| Permission | Label | Description |
| --- | --- | --- |
| `platform:read` | Read Platform | View platform dashboards and tenant listings |
| `platform:write` | Write Platform | Create and modify tenant configurations |
| `platform:manage` | Manage Platform | Full platform administration (grants all platform:*) |
| `platform:conductor:admin` | Platform Conductor Admin | Approve and reject Conductor registrations across tenants |
| `platform:users:admin` | Platform Users Admin | Manage users across all tenants |
| `platform:switch` | Platform Switch Tenant | Switch active tenant context for cross-tenant operations |

### Auditor

| Permission | Label | Description |
| --- | --- | --- |
| `auditor:read` | Read Auditor | View audit findings, runs, and check definitions |
| `auditor:write` | Write Auditor | Create and modify connector configurations |
| `auditor:delete` | Delete Auditor | Delete connector configurations |
| `auditor:execute` | Execute Auditor | Trigger audit runs and test connections |
| `auditor:manage` | Manage Auditor | All auditor operations (includes read, write, delete, execute) |

### Certifications

| Permission | Label | Description |
| --- | --- | --- |
| `certifications:read` | Read Certifications | View certification packages, questions, and exports |
| `certifications:write` | Write Certifications | Create, edit, and export certification packages |

### Chat

| Permission | Label | Description |
| --- | --- | --- |
| `chat:read` | Read Chat | View chat rooms and messages |
| `chat:write` | Write Chat | Send messages and create chat rooms |
| `chat:manage` | Manage Chat | Manage room membership, delete rooms (includes read, write) |
| `chat:ai` | Chat AI | Invoke @AI assistant in chat rooms |

### Attachments

| Permission | Label | Description |
| --- | --- | --- |
| `attachments:read` | Read Attachments | View and download file attachments |
| `attachments:write` | Write Attachments | Upload file attachments |
| `attachments:delete` | Delete Attachments | Delete file attachments |
| `attachments:manage` | Manage Attachments | All attachment operations (includes read, write, delete) |

## AI and MCP permissions

AI configuration and MCP access are separate permissions in 1.2.0:

| Permission | What it controls |
| --- | --- |
| `ai:read` | Read your own chat sessions with the in-app AI assistant |
| `ai:write` | Send messages, and start, rename and delete chat sessions |
| `ai:manage` | AI providers and their API keys, and the **AI Setup** page |
| `mcp:manage` | The organization's MCP mode, every MCP key in the organization, and (with app sign-in on) OAuth clients and connected apps |
| `mcp:connect` | Your own personal MCP keys, the apps that connect as you, and MCP sessions |

Some MCP actions need `admin` itself, even with `mcp:manage`: marking an OAuth client as trusted, changing a trusted client's return addresses, and the client policy. `mcp:manage` cannot create a key for another user.

`mcp:connect` is a gate, not a grant. A connected user reaches only the tools whose permissions they also hold. Two tools, `mcp_info` and `get_system_health`, need only `mcp:connect`. See [MCP Authentication](../ai/mcp/authentication.md) and [MCP Tools](../ai/mcp/tools.md).

## Related pages

- [Roles Reference](roles.md): what each built-in role holds
- [Admin Guide: Permissions](../admin-guide/permissions.md)
- [Admin Guide: Roles](../admin-guide/roles.md)
