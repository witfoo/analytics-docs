# MCP Errors

The responses an MCP client can receive from the appliance, and what to do about each.

## Where errors come from

Every MCP request passes three checks:

1. **The door** reads the credential, on each HTTP request or WebSocket connection.
2. **Admission** checks, on every request, that the user is still allowed to use MCP.
3. **Authorization** checks, on each `tools/call`, that the user holds the tool's permission.

Door and admission refusals arrive as plain HTTP responses, on `POST /mcp` and on the `/ws/chat` WebSocket alike. A WebSocket refusal carries its real HTTP status and message, for example `401` "MCP key expired". A dispatcher that cannot be reached is a `502`.

For an admission refusal the client gets a general message. The specific reason goes to the dispatcher log. A licence refusal is the exception: its body names the licence and the licences that include MCP.

## Responses at the door

| Status | Situation | Message |
| --- | --- | --- |
| 400 | A personal key in the URL, under any parameter name or encoding | Personal MCP keys must be sent in the X-MCP-Key or Authorization: Bearer header, never in the URL |
| 400 | The body is not exactly one JSON-RPC request: a batch, a second `method`, or a body not read within 15 seconds. For an access token, also a body over 1 MiB | Send exactly one JSON-RPC request |
| 401 | A retired org-wide `wfmcp_` key | Org-wide MCP keys were retired in 1.2.0. Create a personal MCP key under Profile → Security. |
| 401 | An unknown, revoked or malformed key | Invalid MCP key |
| 401 | An expired key | MCP key expired |
| 401 | No credential on `/mcp`, where the appliance is not set up for app sign-in | A personal MCP key is required |
| 401 | No credential on `/mcp`, where the appliance is set up for app sign-in | A valid MCP credential is required, with a `WWW-Authenticate` challenge: `Bearer resource_metadata="…", scope="mcp:read"` |
| 401 | An access token that does not verify, or whose user, app, grant or organization mode no longer allows it | The access token is invalid or has expired, with the `invalid_token` challenge. The reply never says which check refused. |
| 401 | Admission refused for a personal key or a browser session: an inactive user, no `mcp:connect`, keys not allowed for the organization, or a suspended tenant | MCP credential is not authorized |
| 403 | An access token without `mcp:write` calls a tool that is not read-only | This tool needs the mcp:write scope, with the `insufficient_scope` challenge |
| 403 | `Origin` is present and not allowed | Origin not allowed |
| 403 | The appliance licence does not include MCP | The `feature_not_available` body |
| 413 | A personal-key request on `/mcp` whose body is over 1 MiB | The request body is too large |
| 429 | An app over its volume limit, or with 8 requests already in progress | Too many requests for this connection, with `Retry-After` |
| 429 | A `/ws/chat` user already holds 5 open sessions, or the appliance is serving 100 | `too many open MCP sessions for this user; close one and retry`, or `this appliance is serving its maximum number of MCP sessions; retry shortly`, with `Retry-After: 30` |
| 503 | A storage read failed while admitting an access token | MCP is temporarily unavailable, with `Retry-After: 5` |
| 503 | The node has no MCP authority configured | MCP is unavailable on this node |
| 502 | The dispatcher cannot be reached | — |

### The licence refusal

A licence refusal is a `403` with a body like this one, from an Analytics Lite appliance:

```json
{
  "error": "feature_not_available",
  "feature": "mcp_connector",
  "product_type": "analytics",
  "tier": "lite",
  "licensed_for": ["analytics:max", "analytics:pro", "reporter:pro"],
  "message": "The MCP connector is not included in this appliance's license (Analytics Lite). It is included in Analytics Max, Analytics Pro and Reporter Pro."
}
```

A licence refusal is not a credential failure: keys and settings are untouched, and the throttle never counts it. On `/mcp`, a request admitted just before the licence changed gets, in place of its result, a JSON-RPC error whose message is `feature_not_available:` followed by the message above. See [Licensing](licensing.md).

### Other HTTP answers on /mcp

| Status | Situation |
| --- | --- |
| 404 | The HTTP transport is not turned on, so `/mcp` is not served at all. See [MCP Configuration](configuration.md). |
| 405 | `GET /mcp`. The HTTP transport is stateless and issues no `Mcp-Session-Id`. |

## Failed-authentication throttle on /mcp

Failed authentications on `/mcp` are counted per client address over a rolling minute. An IPv6 address is counted by its /64.

| Failures from the address in the last minute | What happens |
| --- | --- |
| Fewer than 10 | Every request is checked normally. |
| 10 to 99 | Only a well-formed personal key in a header is checked. Any other request gets `429` without being checked. |
| 100 or more | Every request from the address gets `429`, a valid key included. |

A `429` from the throttle carries `Retry-After: 60`. Only a refused credential (`401` or `400`) counts. A `503`, a licence refusal and a successful request never count.

Access tokens sit outside this throttle. Their volume is limited per app and user instead.

!!! warning "Clients that share an address share a count"
    These clients arrive with one address, so 100 failures from one of them refuse the others for up to a minute:

    - everyone behind a load balancer that is not declared as a trusted proxy;
    - clients that Docker relays to the reverse proxy, such as IPv6 clients and clients on the appliance host itself;
    - clients behind one NAT, and IPv6 clients in one /64.

    Declare the load balancer in front of the appliance before you enable `/mcp` behind it: `trusted_proxies` in `node.json` on a WFA appliance (WFA 2.5.1 or later), or `WF_TRUSTED_PROXIES` on a Docker Compose stack. A re-run of `wfa configure` or `wfa fetch` writes `node.json` without `trusted_proxies`, so add it again after each re-run, then run `wfa restart`.

## WebSocket close codes

An open `/ws/chat` socket is admitted again on every request except `ping` and `notifications/*`. An idle socket is re-checked every 60 seconds.

| Close code | Message | Cause |
| --- | --- | --- |
| 1008 | MCP credential is no longer valid | The key was revoked or expired, the user was disabled, `mcp:connect` was removed, the tenant was suspended, or personal keys were turned off |
| 1008 | MCP connector is not licensed on this appliance | The licence no longer includes MCP |
| 1009 | — | A message larger than the per-message limit (a little over 6 MB), or a notification larger than 512 KiB |

So a revocation stops an active client on its next request, and closes an idle socket within a minute. On HTTP `/mcp` every request is checked on its own, so a change applies to the next request.

## Errors inside a session

- **A method the server does not have.** Once a caller is admitted, a single JSON-RPC request for a method the server does not implement answers `404` with `application/json`:

    ```json
    {"jsonrpc":"2.0","id":1,"error":{"code":-32601,"message":"Method not found"}}
    ```

    A client that opens with a newer method, such as `server/discover`, can then fall back to `initialize`.

- **A tool the user may not call.** Authorization runs before the tool, so a denied call is refused and the tool does not run.
- **A grant narrowed to read.** When an app's grant is narrowed to `mcp:read` after its token was issued, a write tool is refused inside the session with a JSON-RPC error whose message begins `authorization: insufficient_scope`.

## Origin

A headless client sends no `Origin` header and needs no configuration. When a request carries `Origin`, the origin must be allowed, for keys, access tokens and browser sessions alike.

| Path | Who decides | Allowed origins |
| --- | --- | --- |
| A WebSocket through the reverse proxy (`/ws/chat`, `/ws/graph`, `/ws/events`) | The reverse proxy | The appliance's own origin, and the reverse proxy's `WF_ALLOWED_ORIGINS` |
| `POST /mcp` | The dispatcher | The dispatcher's `WF_ALLOWED_ORIGINS` only |

!!! note "A browser page that calls /mcp"
    Behind the reverse proxy the dispatcher does not see the appliance's own host name, so the appliance's own origin does not count on `/mcp`. A browser page that calls `/mcp` must be listed in the dispatcher's `WF_ALLOWED_ORIGINS`, even when the appliance serves the page.

The **Allowed Origins** field under **AI Setup** > **MCP Server Settings** is saved and shown only. No origin check reads it.

## "unexpected status 401" on most tool calls

Most tools call incident-engine on the user's behalf. If incident-engine and the dispatcher run different versions, most MCP tool calls fail with an "unexpected status 401" error.

Upgrade incident-engine and the dispatcher together, or incident-engine first. See [Upgrading to 1.2.0](../../reference/upgrade-1.2.0.md).

## Personal key refusals

Creating, rotating and revoking a personal key can be refused with a stable `code`: `personal_keys_disabled`, `personal_key_limit`, `key_rotation_conflict` or `key_not_active`. See [Personal MCP Keys](personal-keys.md).

## App sign-in errors

The token endpoint `/oauth/token` answers OAuth error codes such as `invalid_grant` and `invalid_target`. See [App Sign-in (OAuth 2.1)](oauth.md).
