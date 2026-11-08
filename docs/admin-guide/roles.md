# Roles

Roles define what users can access in WitFoo Analytics. A user can hold one or more roles, and holds the permissions of all of them together.

## Built-in Roles

WitFoo Analytics 1.2.0 ships 9 built-in roles. They cannot be edited or deleted.

| Role | Description | Key Permissions |
| --- | --- | --- |
| **Admin** | Full system access - all permissions | `admin` (every permission) |
| **Analyst** | Read-only access to all data, plus the AI chat assistant | Read access to signals, the graph, work units, Observer, reports, frameworks, Auditor, Certifications and CyberGrid; the AI assistant |
| **ReadOnly** | Read-only access to all data, plus the AI chat assistant | The same as Analyst, without Auditor and Certifications |
| **Report Viewer** | View and export reports, plus the AI chat assistant | Read and export reports; read frameworks, Auditor and Certifications; the AI assistant |
| **Report Admin** | Full reporter module administration | Reports, frameworks, Certifications, business settings and the product catalog; read Auditor; the AI assistant |
| **CyberGrid Viewer** | View CyberGrid resources, plus the AI chat assistant | Read CyberGrid publications, subscriptions, queue and directory; the AI assistant |
| **CyberGrid Admin** | Full CyberGrid administration | `cybergrid:manage`; the AI assistant |
| **Framework Manager** | Compliance framework administration | Frameworks, read reports, business settings; the AI assistant |
| **Platform Admin** | Cross-tenant platform administrator with full platform management capabilities | `admin` and every `platform:` permission |

These descriptions are the ones 1.2.0 seeds for new installs and new tenants. An appliance installed earlier keeps the descriptions it already has. The full permission matrix is in the [Roles Reference](../reference/roles.md).

## Permission Inclusion Rules

- The `admin` permission grants every other permission.
- `{resource}:manage` grants every `{resource}:*` permission, so `mcp:manage` grants `mcp:connect`.
- `{resource}:write` grants `{resource}:read`.

The platform-administrator flag and `platform:manage` do not grant `mcp:connect`.

## MCP access

No built-in role is seeded with **Connect MCP** (`mcp:connect`). Admin and Platform Admin can connect an MCP client because they hold `admin`, and so can any role that holds **Manage MCP** (`mcp:manage`). To let anyone else connect an AI client, give them a custom role that holds `mcp:connect`. Each tool still needs its own permission. See [MCP Authentication](../ai/mcp/authentication.md).

## Custom Roles

1. Open **Settings** > **Role Management** (the gear icon in the page header).
2. Click **Create Role**.
3. Enter a role name and, optionally, a description.
4. Select permissions from the list.
5. Click **Save**.

**Role Management** opens only for users who hold the `admin` permission (label **Administrator**). It marks **Write Users**, **Read Roles** and **Write Roles** as reserved for that permission.

### What custom roles need in 1.2.0

Some actions now check a permission they did not check before. If your administrators or analysts use custom roles, check these:

| Action | Permission the role needs |
| --- | --- |
| The setup wizard's AI step | **Manage AI** (`ai:manage`) together with **Manage Settings** (`settings:manage`) |
| The setup wizard's DNS step | **Manage Signals** (`signals:manage`) together with `settings:manage` |
| The setup wizard's frameworks step | **Write Frameworks** (`frameworks:write`) together with `settings:manage` |
| The setup wizard's CyberGrid step | **Manage CyberGrid** (`cybergrid:manage`) together with `settings:manage` |
| Create, update, delete or clone a dashboard | **Write Dashboards** (`dashboards:write`). Marking a dashboard as a favorite still needs only **Read Dashboards** |
| See a dashboard widget's data | The read permission of the widget's data: Work Units read for Work Units widgets, Signals read for artifact widgets, any of Graph, Nodes or Edges read for node and edge widgets, Reports read for report widgets, Frameworks read or Reports read for framework widgets, Health read for health widgets |
| Use the in-app AI assistant | **Read AI** (`ai:read`) to read your sessions, **Write AI** (`ai:write`) to send messages and start, rename or delete sessions |
| Connect an MCP client | **Connect MCP** (`mcp:connect`) |
| Read classification rules | `signals:read` or `settings:manage`. Changing them needs `signals:manage` or `settings:manage` |
| Read enrichment settings | `signals:read`. Changing them needs `signals:manage` |
| Read compliance frameworks | `frameworks:read` or `reports:read`. Changing them needs `frameworks:write` |

A user without a widget's read permission sees "You do not have access to this widget's data." on that widget. The dashboard's other widgets are unaffected.

When an appliance first starts 1.2.0, every custom role that exists at that moment receives **Read AI** and **Write AI** once. Removing them afterwards sticks. Custom roles created later do not get them automatically.

## When role changes apply

- A permission change reaches a user at their next sign-in, or when an API client refreshes its token.
- After that, the server may reuse an earlier allow or deny decision for up to 5 minutes.
- MCP connections read the user's roles on every request, so they see a change on the next request.
- A session that began before a role gained a permission does not carry it. The user signs in again to get it.

## Role Assignment

Assign roles to a user from **Settings** > **User Management**: open the user's row actions and choose **Assign Roles**.
