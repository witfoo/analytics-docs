# App Sign-in (OAuth 2.1)

The appliance can act as the OAuth 2.1 authorization server for the apps your users connect over MCP, so a user approves an app on a consent page instead of pasting a key into it.

## How it works

1. The app finds the appliance's sign-in endpoints from `/mcp` and its discovery documents.
2. The app sends the user's browser to the appliance's consent page.
3. The user signs in, reviews what the app asks for, and approves or denies it.
4. The app exchanges the approval for a 15-minute access token and a refresh token.
5. Every request the app makes on `/mcp` runs as that user, with that user's permissions, narrowed to the access the user approved.

Personal keys keep working beside app sign-in. A key and an app connection are separate credentials, listed and revoked separately.

## Requirements

App sign-in is available when all of these are true:

1. **The appliance is set up for it:** `MCP_PUBLIC_URL` and `MCP_OAUTH_UI_URL` are both set to valid values.
2. **The HTTP transport is on:** `mcp_http_enabled` (or `WF_MCP_HTTP_ENABLED`). See [Turning MCP On](configuration.md).
3. **The organization selects it:** an administrator with `mcp:manage` chooses **Browser chat sessions, personal keys and app sign-in** under **AI Setup** > **MCP Authentication**.
4. **The licence includes the MCP connector.** Consent is refused with `403 feature_not_available` where the licence is known not to include it. The token endpoint does not check the licence, so existing connections survive a lapse and a renewal. See [MCP Licensing](licensing.md).

!!! warning "Turn on the HTTP transport first"
    With `mcp_http_enabled` off, the appliance still serves the authorization-server document and the token endpoint, and still lets an administrator choose app sign-in. An app could then be approved and have nowhere to use its token. Enable the transport before you set up app sign-in.

## Operator settings

| `node.json` field (WFA 2.5.1 or later) | Docker Compose variable | Default | Rule |
| --- | --- | --- | --- |
| `mcp_public_url` | `MCP_PUBLIC_URL` | unset | The connector URL an app is given: `https`, a host, the path `/mcp` exactly, no trailing slash, no user information, query or fragment, in canonical form (lowercase host, no `:443`). It is the access token's audience, and the issuer is this URL without `/mcp`. |
| `mcp_oauth_ui_url` | `MCP_OAUTH_UI_URL` | unset | The `https` address of the analytics UI, normally its origin, where a signed-in user approves an app. A path prefix is accepted and kept, and trailing slashes are removed. The consent page is this URL followed by `/ui/oauth/authorize`. |
| `mcp_oauth_cimd` | `MCP_OAUTH_CIMD` | `on` | `on` or `off`. `off` means the appliance fetches no client metadata document, so only registered clients can start a new sign-in. Set it to `off` on an appliance whose only egress is a corporate proxy, because that fetch cannot use a proxy. Any other value reads as `off`. |

On a WFA appliance, set the fields in `/witfoo/configs/node.json` (WFA 2.5.1 or later; install WFA 2.5.3), then restart WFA:

```json
{
  "mcp_http_enabled": true,
  "mcp_public_url": "https://mcp.example.com/mcp",
  "mcp_oauth_ui_url": "https://analytics.example.com"
}
```

On Docker Compose, set `MCP_PUBLIC_URL`, `MCP_OAUTH_UI_URL` and, optionally, `MCP_OAUTH_CIMD` in the environment. The compose files pass them to the api and the dispatcher.

### Check the settings

WFA does not validate these values. An invalid value logs an error line that names the variable, and is read as unset (or, for `mcp_oauth_cimd`, as `off`). At start-up the api and the dispatcher each log one line that says which case applies:

- `MCP OAuth is available`, with the issuer and the audience (the connector URL), or
- `MCP OAuth is not available`.

Read that line before you point an app at the appliance. For a valid `/mcp` URL written in another spelling, the line prints the canonical form to use.

!!! tip "Enter the URL exactly as it is set"
    A trailing slash names another path. The exposure listener answers `/mcp/` with `404`, and the `:443` listener redirects it to `/mcp`.

## The connector URL

The connector URL is `MCP_PUBLIC_URL`. App sign-in is bound to it:

- An app that names a `resource` must name this URL (a spelling that canonicalises to it, such as capitals in the host or `:443`, is accepted). Any other value, such as another listener's host or port, is refused with `invalid_target` and receives no token.
- An access token's audience is this URL and no other.
- Personal keys work at every listener, whatever this setting holds.

## Discovery

A request to `/mcp` with no credential gets `401` and this header, where `<origin>` is the origin of `MCP_PUBLIC_URL`:

```text
WWW-Authenticate: Bearer resource_metadata="<origin>/.well-known/oauth-protected-resource/mcp", scope="mcp:read"
```

| Document | Path |
| --- | --- |
| Protected-resource metadata | `/.well-known/oauth-protected-resource/mcp`, also served at `/.well-known/oauth-protected-resource` |
| Authorization-server metadata | `/.well-known/oauth-authorization-server` |

Both are built from the settings alone, never from the request's `Host` header, and are served with `Cache-Control: public, max-age=300` and `Access-Control-Allow-Origin: *`.

| Authorization-server member | Value |
| --- | --- |
| `issuer` | The origin of `MCP_PUBLIC_URL` |
| `authorization_endpoint` | `MCP_OAUTH_UI_URL` followed by `/ui/oauth/authorize` |
| `token_endpoint` | The origin of `MCP_PUBLIC_URL` followed by `/oauth/token` |
| `response_types_supported` | `code` |
| `response_modes_supported` | `query` |
| `grant_types_supported` | `authorization_code`, `refresh_token` |
| `code_challenge_methods_supported` | `S256` |
| `token_endpoint_auth_methods_supported` | `none`: every app is a public client |
| `authorization_response_iss_parameter_supported` | `true` |
| `scopes_supported` | `mcp:read`, `mcp:write` |
| `client_id_metadata_document_supported` | `true`. Absent when `MCP_OAUTH_CIMD` is `off`. |

There is no registration endpoint. Apps do not register themselves.

## The sign-in flow

| Step | Rules |
| --- | --- |
| Authorization request | PKCE with `S256` only. A request without `code_challenge_method=S256`, or with `plain`, is refused `invalid_request`. `state` can be at most 1,024 bytes. A sign-in older than 15 minutes is asked for again. The answer carries `code`, `state` and `iss`. |
| Token request | A `POST` of `application/x-www-form-urlencoded` to `/oauth/token`, with no query string and a body of at most 8 KiB. |
| Authorization code | Lives 60 seconds and works once. Presenting a used code again within those 60 seconds, with the same `code_verifier`, `client_id` and `redirect_uri`, revokes the connection's refresh tokens. |
| Access token | `token_type` `Bearer`, `expires_in` 900 (15 minutes). The app sends it as `Authorization: Bearer <access token>` on `/mcp`. |
| Refresh token | Rotates on every use: the one presented stops working. A refresh token unused for 14 days expires, and a connection ends 90 days after its code was redeemed, however often it is used. |
| Refresh token reuse | Presenting a refresh token that was already replaced revokes the connection's refresh tokens, so the app has to sign in again. A retry within 20 seconds of the rotation is honoured once, so an app whose reply was lost can repeat its request. |
| Refresh rate | A connection rotates at most once every 10 seconds. A sooner refresh is answered `429 temporarily_unavailable` with `Retry-After: 10`. |

### Token endpoint responses

| Status | When |
| --- | --- |
| `400` | `{"error": "<code>"}` with `invalid_request`, `invalid_client`, `invalid_grant`, `invalid_target`, `invalid_scope` or `unsupported_grant_type` |
| `401` | `invalid_client` for a request that carried an `Authorization: Basic` header, with `WWW-Authenticate: Basic realm="oauth"` |
| `429` | `temporarily_unavailable` with `Retry-After: 10` inside the 10-second refresh floor, or with `Retry-After: 60` past the failure limit (see [Traffic limits](#traffic-limits)) |
| `503` | `server_error`: the appliance could not complete the request for a reason of its own, such as storage being unavailable |
| `405` | A request that is not a `POST`, with `Allow: POST` |
| `404` | Every request, when the appliance is not set up for app sign-in |

Every response from the token endpoint carries `Cache-Control: no-store` and `Pragma: no-cache`.

## Which apps can connect

An app names itself with a `client_id`, in one of two ways. An organization can use both.

### Registered clients

An administrator with `mcp:manage` registers the app:

1. Navigate to **Settings** > **General Settings** > **AI Setup** > **MCP Authentication** > **OAuth clients**.
2. Click **Add client**.
3. Optionally, use **Fill in from a known app** to fill in the return addresses of a known app.
4. Enter a **Name** (up to 64 characters) and 1 to 10 return addresses, one per line.
5. Optionally, select **Trusted client**. This needs the `admin` permission.
6. Save, then copy the **Client ID** and enter it in the app. A Client ID is `wfmcpc_` followed by 32 hexadecimal characters.

| Preset | Return addresses |
| --- | --- |
| Claude | `https://claude.ai/api/mcp/auth_callback` |
| Cursor | `https://www.cursor.com/agents/mcp/oauth/callback`, `http://localhost:8787/callback` |
| MCP Inspector | `http://localhost:6274/oauth/callback`, `http://127.0.0.1:6276/oauth/callback` |

Check the presets against what the app actually sends.

- Changing a client's return addresses revokes no existing approval, but a trusted client's earlier approvals stop letting it skip the consent page.
- Revoking a client revokes every approval given to it.
- Marking a client trusted, or changing the return addresses of a trusted client, needs `admin` itself.

### Apps that publish a client metadata document

Some apps identify themselves with the URL of a JSON client metadata document instead of a Client ID.

- The `client_id` is an `https` URL with a host name (not an IP address), a path beyond `/`, no query, fragment or user information, at most 512 bytes, in canonical spelling.
- The document lists the app's return addresses (`redirect_uris`, 1 to 10) and may name the app (`client_name`). It must name its own URL as its `client_id`, and must not carry a `client_secret`.
- The appliance fetches the document only after the client policy admits it, and only while `MCP_OAUTH_CIMD` is `on`. It connects directly, with no proxy, to public addresses only, follows no redirect, accepts at most 5 KiB, waits at most 5 seconds and keeps a successful fetch for up to 5 minutes.
- If the appliance cannot reach the host, or `MCP_OAUTH_CIMD` is `off`, register the app as a client instead.

### Client policy

The client policy decides which apps that publish a metadata document may ask your users to connect. It needs the `admin` permission.

1. Navigate to **AI Setup** > **MCP Authentication** > **Client policy**.
2. Choose the mode for **Apps that publish a client metadata document**:
    - **Only apps on the allow list** (`allowlist`, the default). An organization that has entered nothing admits no such app.
    - **Any app** (`any`). Every app that is not on the deny list.
3. Fill in the **Allow list** and **Deny list**, one app address or host per line, up to 100 entries each. An app address names that one document; a host names every app at exactly that host. The deny list wins over the allow list.
4. Set **Most access an app with a metadata document can be given**. The default is `mcp:read`. A registered client is not limited by it.
5. Click **Save policy**.

**Add to the allow list** offers two presets:

| Preset | Entry |
| --- | --- |
| Claude | `https://claude.ai/oauth/mcp-oauth-client-metadata` |
| Claude Code | `https://claude.ai/oauth/claude-code-client-metadata` |

Saving a policy that denies an app revokes that app's approvals in the organization. Removing an app from the allow list, or lowering the most access, applies only to approvals given from then on.

### Return addresses

- A return address is an absolute `https` address, or an `http` address on `localhost`, `127.0.0.1` or `[::1]`, with no fragment and no user information.
- A custom scheme such as `cursor://` is refused, for a registration and for a metadata document alike. A metadata document that lists one is refused as a whole.
- A return address in a request must equal a registered one exactly. For a loopback address the port is ignored.

## The consent page

The consent page is part of the analytics UI, at `MCP_OAUTH_UI_URL` followed by `/ui/oauth/authorize`. It needs a signed-in user who holds `mcp:connect`, whose home organization is the one the request is for, and who signed in within the last 15 minutes.

The page, **Connect an app to WitFoo**, shows:

- the app's name and identifier. For an app that publishes a metadata document, the name is marked **declared by the app itself**. For a registered client, the page shows the Client ID, who registered it and when;
- the host the approval is delivered to, and any other host the app may return to;
- a warning when the return address is on the user's own computer, and a warning when an address is on a shared hosting service where anyone can publish a page;
- "This app will be able to read what you can read in WitFoo.";
- when the app asked to make changes and the organization allows it, an option, **off by default**, to let the app make changes, listing the titles of the tools that change state;
- the date of the user's earlier approval of this app, when one still counts.

The user clicks **Approve** or **Deny**. A denial returns `access_denied` to the app.

A **trusted** registered client skips the page when the same user approved it in the last 30 days, for the same return addresses, the same connector URL (`MCP_PUBLIC_URL`) and at least the same access, and their sessions have not been ended since. Turning the relay on can change the connector URL, and then the page is shown again. A return address on the user's own computer always shows the page.

### Scopes

| Scope | Allows |
| --- | --- |
| `mcp:read` (default) | The tools marked read-only. The user's permissions are narrowed to the `:read` permissions they hold. |
| `mcp:write` | Every tool. It includes `mcp:read`. |
| `offline_access` | Accepted and ignored, because a refresh token is always issued. |

Any other scope is refused with `invalid_scope`. Neither scope gives an app more than the user has. An app with `mcp:read` only that calls a tool that changes state gets `403` with an `insufficient_scope` challenge. See [Tools](tools.md).

## Connected apps

An approval creates a **grant**, one for each user and app.

- **Users** see and revoke their own apps under **Profile** > **Security** > **Connected apps**.
- **Administrators** with `mcp:manage` see and revoke every app in the organization under **AI Setup** > **MCP Authentication** > **Connected apps in this organization**.
- When a grant is created, the user receives an **App connected** notification that names the app and its access, and says where to revoke it.
- Leaving app sign-in revokes every grant in the organization. An approval in progress at that instant can escape the revocation, but nothing can use it until the organization chooses app sign-in again.

The organization's audit log records consent granted and denied, grants revoked, clients created, edited and revoked, policy changes, and refresh-token reuse. It never records a secret.

## Traffic limits

| Where | Limit |
| --- | --- |
| `/mcp`, per organization, user and app | The **Rate Limit (requests/min)** setting of MCP Server Settings (`rate_limit_per_min`, default 60), refilled continuously. A request costs 1, and a call to a tool that changes state costs 4. Over the limit: `429` with `Retry-After`. |
| `/mcp`, per app and user | At most 8 requests in progress at once. Over the limit: `429` with `Retry-After`. |
| Token endpoint, per source address and app | 300 requests refused with a protocol error in a minute. After that: `429` with `Retry-After: 60`, unless the request presents an unused code or a refresh token that exists. |
| Consent page | 10 requests a minute for each user, and 60 a minute for each organization. |

## Network requirements

- The user's browser must reach `MCP_OAUTH_UI_URL`, the consent page and the UI, normally on `:443`.
- The app must reach the origin of `MCP_PUBLIC_URL` for `/mcp`, the discovery documents and `/oauth/token`. A local app reaches it from the user's computer, and a hosted app from its vendor's servers. The [exposure listener](exposure-listener.md) serves exactly those paths.
- A WAF or bot filter in front of the appliance must let the apps' requests through. Anthropic publishes the addresses its servers connect from on its [IP addresses](https://docs.claude.com/en/api/ip-addresses) page. Read the current list there before you rely on it. A rule that blocks those addresses breaks sign-in even when `/mcp` is reachable.

!!! warning "Keep tokens off plain-HTTP hops"
    Where the appliance is configured for plain HTTP (`disable_tls` or `LB_MODE`), the hop from the load balancer carries authorization codes, access tokens and refresh tokens in cleartext. A refresh token is a bearer credential: whoever holds it can use it. Admit `/oauth/token` and `/mcp` only from the addresses of the apps you use, on every listener that serves them: the main listener (`:443`), the exposure listener (8444) and, with TLS on, the plain-HTTP port 8081.

If you run a load balancer or proxy in front of the appliance, declare it in `trusted_proxies` (WFA) or `WF_TRUSTED_PROXIES` (Docker Compose). A re-run of `wfa configure` or `wfa fetch` writes `node.json` without `trusted_proxies`, so add it again after each re-run and run `wfa restart`.

## Not supported

- Registration by the app itself (dynamic client registration).
- Return addresses with a custom scheme, such as `cursor://`.
- Client secrets: every app is a public client.
- Authorization flows other than the authorization code flow with `S256` PKCE: no implicit, password or client-credentials grant, and no `plain` challenge.
- Binding tokens to a client key (DPoP or mTLS).
- Using an access token anywhere except `/mcp`. The API, the incident engine and the WebSockets refuse it.
