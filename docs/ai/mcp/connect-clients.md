# Connecting AI Clients & Marketplaces

Connect an AI client to your appliance with a personal key, or let an app sign in through the appliance's own OAuth 2.1 server.

## Before you start

- MCP is turned on for the organization, and the HTTP transport is on for HTTP clients. See [Turning MCP On](configuration.md).
- You hold **Connect MCP** (`mcp:connect`). See [Authentication & Permissions](authentication.md).
- The appliance licence includes the MCP connector. See [MCP Licensing](licensing.md).

## Choose a route

| Where the client runs | Route | Address |
| --- | --- | --- |
| On your network, such as a desktop client or Claude Code on a laptop | The main listener | `https://<appliance>/mcp` |
| On a vendor's servers, such as claude.ai or ChatGPT, with an inbound port you can open | The [exposure listener](exposure-listener.md) on port 8444 | `https://<published name>/mcp`, through the proxy or load balancer in front of port 8444 |
| On a vendor's servers, with no inbound port | The [AI-connector relay](relay.md) | `https://mcp-relay.witfoo.com/h/<handle>/mcp` |
| An air-gapped appliance | The main listener, from clients on your own network only | `https://<appliance>/mcp` |

## Connect with a personal key

Create a key under **Profile** > **Security** > **MCP connections** first. See [Personal MCP Keys](personal-keys.md). The card shows the snippets below filled in with your key right after you create it.

Replace `<appliance>` with your appliance's address and `wfmcpu_xxxxxxxx` with your key.

=== "Claude Code"

    ```bash
    claude mcp add --transport http witfoo https://<appliance>/mcp \
      --header "X-MCP-Key: wfmcpu_xxxxxxxx"
    ```

=== "Claude Desktop"

    Add the server to `claude_desktop_config.json`:

    ```json
    {
      "mcpServers": {
        "witfoo": {
          "type": "http",
          "url": "https://<appliance>/mcp",
          "headers": { "X-MCP-Key": "wfmcpu_xxxxxxxx" }
        }
      }
    }
    ```

=== "Cursor"

    Add the server to `.cursor/mcp.json`:

    ```json
    {
      "mcpServers": {
        "witfoo": {
          "type": "http",
          "url": "https://<appliance>/mcp",
          "headers": { "X-MCP-Key": "wfmcpu_xxxxxxxx" }
        }
      }
    }
    ```

=== "WebSocket client"

    Connect to `wss://<appliance>/ws/chat` and send the same header on the upgrade request:

    ```text
    X-MCP-Key: wfmcpu_xxxxxxxx
    ```

!!! warning "Send the key in a header"
    Never put a key in a URL. A key in a URL is refused with `400`.

### A hosted connector for a whole organization

A hosted connector that takes one static credential for everyone in the organization shares that credential between all of them. Give it the personal key of a dedicated user who holds only the permissions the connector needs, never an administrator's.

## Connect with app sign-in

App sign-in needs the appliance set up for it and the organization in **Browser chat sessions, personal keys and app sign-in** mode. See [App Sign-in (OAuth 2.1)](oauth.md). The app is given the connector URL, `MCP_PUBLIC_URL`, for example `https://mcp.example.com/mcp`.

=== "Claude and Claude Code"

    Claude and Claude Code publish a client metadata document, so they do not need to be registered.

    1. An administrator (`admin`) opens **AI Setup** > **MCP Authentication** > **Client policy**, uses **Add to the allow list** to add **Claude** or **Claude Code**, and clicks **Save policy**.
    2. The user adds the connector URL in the app and starts the sign-in.
    3. The user signs in to WitFoo if asked, reviews the consent page, and clicks **Approve**.
    4. The connection appears under **Profile** > **Security** > **Connected apps**.

    Claude can also be registered as a client with the **Claude** preset, as for Cursor.

=== "Cursor and MCP Inspector"

    1. An administrator with `mcp:manage` opens **AI Setup** > **MCP Authentication** > **OAuth clients**, clicks **Add client**, and uses **Fill in from a known app** to choose **Cursor** or **MCP Inspector**.
    2. The administrator saves the client and gives the user its **Client ID** (`wfmcpc_…`).
    3. The user enters the connector URL and the Client ID in the app and starts the sign-in.
    4. The user signs in to WitFoo if asked, reviews the consent page, and clicks **Approve**.
    5. The connection appears under **Profile** > **Security** > **Connected apps**.

Check a preset's return addresses against what the app actually sends. Apps that need a custom-scheme return address such as `cursor://` cannot be registered.

For a hosted app, the vendor's servers must reach `/mcp`, the discovery documents and `/oauth/token`, and the approving user's browser must reach the analytics UI.

## ChatGPT

ChatGPT can connect to an appliance's MCP endpoint in 1.2.0. This was verified against a test rig, not yet against a live 1.2.0 appliance.

ChatGPT first calls `server/discover`, a method this server does not have. The appliance answers an unknown method with `404` and the JSON-RPC error `-32601` (`Method not found`), and ChatGPT then falls back to `initialize`. Claude clients connect either way.

ChatGPT is a hosted app, so its servers need a route to the appliance that they can reach, such as the [exposure listener](exposure-listener.md). ChatGPT has not been verified through the [relay](relay.md).

## Long-running tools over HTTP

The reverse proxy in front of HTTP `/mcp` closes a request at 120 seconds. `generate_report` can hold a call open for up to five minutes, so over HTTP `/mcp` a report that takes longer ends in a transport error instead of the tool's answer.

## Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| `/mcp` answers `404` | The HTTP transport is off | Set `mcp_http_enabled` and restart WFA. See [Turning MCP On](configuration.md). |
| `401` "MCP credential is not authorized" | The user lacks `mcp:connect`, is inactive, or the organization does not allow personal keys | Check the user's roles and the organization's mode. The specific reason is in the dispatcher log. |
| `401` "Org-wide MCP keys were retired in 1.2.0. …" | The client uses an old `wfmcp_` key | Create a personal key. See [Personal MCP Keys](personal-keys.md). |
| `401` "MCP key expired" | The key reached its expiry | Create or rotate a key. |
| `400` for a key in the URL | The key is in the query string | Send it in the `X-MCP-Key` header. |
| `403` "Origin not allowed" | A browser page sent an `Origin` that is not allowed | Add the origin to the right `WF_ALLOWED_ORIGINS`. See [Turning MCP On](configuration.md). |
| `403` `feature_not_available` | The licence does not include the MCP connector | See [MCP Licensing](licensing.md). |
| `403` `insufficient_scope` | An app approved for read only called a tool that changes state | Approve the app again with changes allowed, if the organization permits it. |
| `429` | Too many failed sign-ins from one address, too many open WebSocket sessions, or an app over its rate limit | Wait for `Retry-After`. Behind a load balancer, declare it in `trusted_proxies` or `WF_TRUSTED_PROXIES`. |
| Most tool calls fail with `unexpected status 401` | The incident engine and the dispatcher run different versions | Upgrade them together. See [Architecture](architecture.md). |
| A certificate error from a hosted client | The appliance presents its self-signed certificate | Terminate TLS in front of the listener with a certificate for the published name. See [Exposure Listener (Port 8444)](exposure-listener.md). |

See [Errors](errors.md) for every response an MCP client can receive.
