# AI & MCP

WitFoo Analytics includes an in-app AI assistant and a Model Context Protocol (MCP) connector that lets AI clients work with your appliance's data.

## Components

### [Configuration](configuration.md)

Configure AI providers, models, and API keys.

### [Chat Interface](chat.md)

Use the AI chat panel for security analysis assistance.

### [MCP Connector](mcp/index.md)

Connect AI clients such as Claude Desktop, Claude Code and Cursor to your appliance.

## Overview

The AI assistant helps analysts with:

- Incident investigation and triage guidance
- Artifact analysis and enrichment interpretation
- Report generation and summary
- Compliance mapping assistance

## MCP

AI clients connect to the appliance over MCP. Every connection acts as a real user, with that user's live permissions, and an administrator can see and end any of them.

- Users connect with a [personal MCP key](mcp/personal-keys.md) they create under **Profile** > **Security** > **MCP connections**.
- Apps can sign in through the appliance's own authorization server. See [App sign-in (OAuth 2.1)](mcp/oauth.md).
- An optional [relay](mcp/relay.md), off until an operator turns it on, reaches the appliance's MCP endpoint without an inbound port.
- MCP is included with Analytics Pro, Analytics Max and Reporter Pro. See [Licensing](mcp/licensing.md).

Connections by personal key, by app sign-in and over HTTP `/mcp` are off by default. See [MCP Configuration](mcp/configuration.md) and the [tool reference](mcp/tools.md).

## Permissions

| Permission | Name | Access |
| --- | --- | --- |
| `ai:read` | Read AI | View AI features and read chat assistant sessions |
| `ai:write` | Write AI | Send messages; start, rename and delete chat sessions |
| `ai:manage` | Manage AI | Configure AI providers and their API keys, and open the AI Setup page |
| `ai:export` | Export AI | Export chat history and conversations |
| `mcp:connect` | Connect MCP | Create, rotate and revoke your own personal MCP keys, approve and revoke the apps that connect as you, and open an MCP session that runs with your own permissions |
| `mcp:manage` | Manage MCP | Set the organization's MCP mode, list and revoke any MCP key in the organization, and manage app sign-in clients and connected apps |

- Every built-in role holds `ai:read` and `ai:write`, directly or through Administrator.
- A user with **Read AI** but not **Write AI** can open their chat sessions but cannot send or change anything.
- No built-in role is seeded with `mcp:connect`. **Admin** and **Platform Admin** hold it through Administrator, and any role that holds `mcp:manage` holds it too. Grant it to anyone else through a custom role.
- The AI Setup page opens for `ai:manage`. Its MCP Authentication section is shown to holders of `mcp:manage`, so an administrator who manages MCP in the UI needs both.

!!! info "Custom roles and the assistant at upgrade"
    On the first start of 1.2.0, existing custom roles receive `ai:read` and `ai:write` once. Removing them afterwards sticks. Custom roles created later do not get them automatically.

    Permission changes reach a user at their next sign-in, and the server may reuse a decision for up to 5 minutes after that. MCP connections read a user's roles on every request and see a change on the next one.

See [Permissions](../reference/permissions.md) for the full catalog.
