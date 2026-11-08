# Turning MCP On

MCP connections by personal key, by app sign-in and over HTTP `/mcp` need two switches, and both are off by default: the organization's mode, and the HTTP transport on the appliance.

| Switch | Who sets it | Where | Default |
| --- | --- | --- | --- |
| Organization mode | An administrator with `mcp:manage` | **AI Setup** > **MCP Authentication** | **Browser chat sessions only** |
| HTTP transport | The appliance operator | `node.json` (`mcp_http_enabled`), or `WF_MCP_HTTP_ENABLED` on Docker Compose | Off |

A WebSocket client on `/ws/chat` needs only the organization mode. An HTTP client on `/mcp` needs both.

## Switch 1: the organization mode

1. Navigate to **Settings** > **General Settings** > **AI Setup**.
2. In **MCP Authentication**, under **Who can connect over MCP**, choose a mode.
3. Click **Save Authentication**.

| Choice | Stored `auth_mode` | Personal keys | App sign-in | Browser chat sessions |
| --- | --- | --- | --- | --- |
| **Browser chat sessions only** (default) | `off` | Cannot be created, and existing keys are refused | Refused | Work, for users who hold `mcp:connect` |
| **Browser chat sessions and personal keys** | `api_key` | Can be created and used | Refused | Work, for users who hold `mcp:connect` |
| **Browser chat sessions, personal keys and app sign-in** | `oauth` | Can be created and used | Allowed | Work, for users who hold `mcp:connect` |

The same change through the API:

```text
PUT /api/v1/ai/mcp   {"auth_mode": "api_key"}
```

### Who can change it

- Changing the mode needs the **Manage MCP** (`mcp:manage`) permission. A platform administrator also passes this check.
- The AI Setup page itself opens only for users who hold **Manage AI** (`ai:manage`), and the MCP Authentication card is shown only to holders of `mcp:manage`.
- Any signed-in user of the organization can read the stored mode with `GET /api/v1/ai/mcp`.

### What each change does

- **Back to Browser chat sessions only.** Personal keys cannot be created (`409 personal_keys_disabled`), and existing keys are refused on their next request. An idle WebSocket closes within a minute.
- **App sign-in** can be chosen only when the appliance's `MCP_PUBLIC_URL` and `MCP_OAUTH_UI_URL` settings are both valid. Otherwise the save is refused with `409 oauth_unavailable`, and the page says that app sign-in is not available on this appliance. See [App Sign-in (OAuth 2.1)](oauth.md).
- **Leaving app sign-in** revokes every connected app in the organization before the new mode is saved. If that revocation fails, the save answers `500` and the mode stays as it was.
- **Licence.** On a licence that does not include the MCP connector, a save that turns something on is refused with `403`. Turning MCP off always works. See [MCP Licensing](licensing.md).

## Switch 2: the HTTP transport

Claude Desktop, Cursor and Claude Code use Streamable HTTP, so most clients need `POST /mcp`. Without this switch the route is not registered at all, and `/mcp` answers `404`.

### WFA appliance

1. Add the field to `/witfoo/configs/node.json` (WFA 2.5.1 or later; install WFA 2.5.3):

    ```json
    {
      "mcp_http_enabled": true
    }
    ```

2. Restart WFA:

    ```bash
    wfa restart
    ```

WFA sets `WF_MCP_HTTP_ENABLED=true` on the dispatcher container, `analytics-dispatcher-svc`.

### Docker Compose

Set `WF_MCP_HTTP_ENABLED=true` in the environment. Every compose file that builds a dispatcher passes it through, with a default of `false`.

### Check that it took effect

If `mcp_http_enabled: true` appears to do nothing:

1. Check the running WFA version with `wfa version`, or with `rpm -q wfa` or `dpkg -s wfa`.
2. Check that the dispatcher has the variable:

    ```bash
    docker inspect analytics-dispatcher-svc | grep WF_MCP_HTTP_ENABLED
    ```

!!! warning "Never run `wfad --version`"
    `wfad --version` starts a second WFA daemon. Use `wfa version`, `rpm -q wfa` or `dpkg -s wfa` to read the version.

The transport switch is separate from the organization mode on purpose: an organization that allowed keys for a WebSocket client does not silently gain an HTTP endpoint that can be reached from outside.

## Browser origins

A headless AI client sends no `Origin` header and needs no origin configuration. When a request does carry `Origin`, the origin must be allowed, for personal keys, access tokens and browser sessions alike. There is no bypass.

| Path | Who decides | Setting |
| --- | --- | --- |
| `/ws/chat`, `/ws/graph` and `/ws/events` through the reverse proxy | The reverse proxy, before it contacts the dispatcher | The reverse proxy's `WF_ALLOWED_ORIGINS`. The appliance's own origin is always accepted. |
| `POST /mcp` | The dispatcher | The dispatcher's `WF_ALLOWED_ORIGINS` |

Behind the reverse proxy the dispatcher sees its own internal host name, so a browser page that calls `POST /mcp` must be listed in the dispatcher's `WF_ALLOWED_ORIGINS`, even when the page is served by the appliance itself. A refused origin gets `403` with `{"error":"Origin not allowed"}`. See [Environment Variables](../../reference/environment-variables.md).

## MCP Server Settings

The **MCP Server Settings** section of AI Setup saves four values with `PUT /api/v1/ai/mcp`.

!!! note "Known limitation"
    Of the four MCP Server Settings fields, only the rate limit has an effect, and only for apps that use app sign-in. **Who can connect over MCP** under **MCP Authentication** decides who is admitted, and `WF_ALLOWED_ORIGINS` decides browser origins.

| Field | Saved as | Effect in 1.2.0 |
| --- | --- | --- |
| **MCP Server Enabled** | `enabled` | Saved and shown. It does not change which clients are admitted. |
| **Allowed Origins (comma-separated)** | `allowed_origins` | Saved and shown. No origin check uses it: origins come from `WF_ALLOWED_ORIGINS`. |
| **Rate Limit (requests/min)** | `rate_limit_per_min` | 1 to 10,000, default 60. Applies to apps that use app sign-in only. A personal key or a browser session is not limited by it. |
| **Max Concurrent Connections** | `max_concurrent` | Saved and shown. Nothing limits connections by it. |

To stop personal-key and app clients, choose **Browser chat sessions only** under **MCP Authentication**.

## Next steps

- [Authentication & Permissions](authentication.md): grant `mcp:connect` to the users who should connect.
- [Personal MCP Keys](personal-keys.md): create a key.
- [Exposure Listener (Port 8444)](exposure-listener.md) or [AI-Connector Relay](relay.md): reach the appliance from a hosted marketplace client.
