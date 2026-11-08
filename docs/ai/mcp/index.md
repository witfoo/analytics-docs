# MCP Server

WitFoo Analytics lets AI clients such as Claude Desktop, Cursor and Claude Code connect to your appliance over the Model Context Protocol (MCP), and every connection acts as a real user with that user's permissions.

## What is MCP?

The Model Context Protocol is an open standard for connecting AI clients to external data and tools. WitFoo's MCP server exposes 44 tools that an AI client can call during a conversation: 28 read-only tools and 16 that change state. See [Tools](tools.md) for the full list.

## How MCP works in 1.2.0

- **Every connection is a real user.** An AI client connects with a credential that belongs to one user. It reaches only the tools, and the actions, that user's own permissions allow, and those permissions are checked live on every request.
- **Administrators see and end connections.** An administrator can list and revoke every personal key and every connected app in the organization.
- **Off by default.** Connections by personal key, by app sign-in and over HTTP `/mcp` are off until you turn them on. See [Turning MCP On](configuration.md).
- **Air-gapped appliances are supported.** The MCP server runs on the appliance itself and needs no outside service.

### Two transports

| Transport | Path | Credentials accepted |
| --- | --- | --- |
| Streamable HTTP (opt-in) | `POST /mcp` | A personal MCP key or, when the organization's mode is app sign-in (`oauth`), an access token the appliance issued to an app |
| WebSocket | `/ws/chat` | A personal MCP key, or a browser session |

`/ws/chat` never accepts an app's access token, and `/mcp` never accepts a browser session.

## What changed since 1.1.x

| Area | 1.1.x | 1.2.0 |
| --- | --- | --- |
| Credentials | Optional org-wide `wfmcp_` keys | Personal keys (`wfmcpu_`) that each user creates, and app sign-in with OAuth 2.1. Org-wide keys are retired. |
| Permissions | Org-wide identity | The connected user's own permissions, checked on every request. A new **Connect MCP** (`mcp:connect`) permission controls who may connect. |
| Tools | 51 tools listed | 44 tools, each marked read-only or state-changing. Seven tools that always failed are removed. |
| Licence | Not licensed separately | Included with Analytics Pro, Analytics Max and Reporter Pro |
| Reaching the appliance | Main listener only | Main listener, an optional exposure listener on port 8444, or the optional AI-connector relay |

!!! warning "Org-wide keys no longer work"
    Keys that start `wfmcp_` stop authenticating after the upgrade. Each user creates a personal key instead. See [Authentication & Permissions](authentication.md).

## Quick start

1. Check that your licence includes the MCP connector: Analytics Pro, Analytics Max or Reporter Pro. See [MCP Licensing](licensing.md).
2. For HTTP clients, turn on the HTTP transport on the appliance (`"mcp_http_enabled": true` in `node.json`, then restart WFA). See [Turning MCP On](configuration.md).
3. Choose who can connect: under **Settings** > **General Settings** > **AI Setup** > **MCP Authentication**, select **Browser chat sessions and personal keys** (or **Browser chat sessions, personal keys and app sign-in**) and click **Save Authentication**.
4. Give each user who should connect the **Connect MCP** (`mcp:connect`) permission through a custom role. Administrators already hold it. See [Authentication & Permissions](authentication.md).
5. Each user creates a personal key under **Profile** > **Security** > **MCP connections**. See [Personal MCP Keys](personal-keys.md).
6. Add the appliance's `/mcp` address and the key to the AI client. See [Connecting AI Clients & Marketplaces](connect-clients.md).

## Pages in this section

- [Architecture](architecture.md): where the MCP server runs and the checks every request passes.
- [Turning MCP On](configuration.md): the organization mode, the HTTP transport switch and allowed origins.
- [Authentication & Permissions](authentication.md): the three kinds of credential, `mcp:connect` and `mcp:manage`, retired org-wide keys and revocation.
- [Personal MCP Keys](personal-keys.md): creating, using, rotating and revoking your own keys.
- [App Sign-in (OAuth 2.1)](oauth.md): letting apps sign in through the appliance's own authorization server.
- [MCP Licensing](licensing.md): which licences include MCP and what a refusal looks like.
- [Exposure Listener (Port 8444)](exposure-listener.md): a separate listener for marketplace clients.
- [AI-Connector Relay](relay.md): reaching the appliance through WitFoo without an inbound port.
- [Connecting AI Clients & Marketplaces](connect-clients.md): configuration for Claude, Cursor, ChatGPT and other clients.
- [Tools](tools.md): the 44 tools and the permission each one needs.
- [Errors](errors.md): the responses MCP clients can receive and what they mean.
