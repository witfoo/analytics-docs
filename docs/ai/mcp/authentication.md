# Authentication & Permissions

Every MCP connection runs as a user, with that user's live permissions, and an administrator can list and revoke the credentials that make those connections.

## Three kinds of credential

| Credential | Used by | Accepted on | Details |
| --- | --- | --- | --- |
| Browser session | The analytics UI in a signed-in browser | `/ws/chat` | See [Browser sessions](#browser-sessions) below |
| Personal MCP key (`wfmcpu_…`) | A developer tool or a desktop client that a user configures | `/mcp` and `/ws/chat` | See [Personal MCP Keys](personal-keys.md) |
| App access token | An app that the user approved through app sign-in | `/mcp` only | See [App Sign-in (OAuth 2.1)](oauth.md) |

A personal key and an app connection are separate credentials. They are listed and revoked separately.

### Browser sessions

The browser session path on `/ws/chat` is kept, with four changes in 1.2.0:

- The session token must carry the `aud` and `exp` claims. **Tokens without them are refused**, so a token issued before the upgrade does not work. Upgrading signs everyone out once anyway.
- The token's own list of permissions is ignored. The session is admitted live, from the user's current roles.
- The user must hold `mcp:connect`.
- The session closes at the first 60-second check at or after the token expires. A request after expiry is refused at once.

## Who can connect: `mcp:connect`

**Connect MCP** (`mcp:connect`) is new in 1.2.0. A user can use MCP only while they hold it, and it is checked live on every request, so granting or removing it takes effect on the user's next call.

- **No built-in role is seeded with it.** **Admin** and **Platform Admin** hold it through `admin`, which grants every permission.
- **`mcp:manage` implies it.** A custom role that holds `mcp:manage` can connect too, by the rule that `{resource}:manage` grants every `{resource}:*` permission.
- **The platform-administrator flag and `platform:manage` do not grant it.**
- **Everyone else needs a custom role** that holds `mcp:connect`. See [Permissions](../../reference/permissions.md).

!!! note "A gate, not a grant"
    `mcp:connect` lets a user connect. It does not grant any data. A connected user reaches only the tools, and the `manage_*` actions, whose permissions they also hold. The two tools that need no other permission, `mcp_info` and `get_system_health`, need only `mcp:connect`. See [Tools](tools.md).

With `mcp:connect` a user can:

- create, rotate and revoke their own personal keys, while the organization's mode allows personal keys;
- approve and revoke the apps that connect as them, when the organization's mode includes app sign-in;
- open an MCP session whose tools run with their own permissions.

Holding `mcp:connect` does not let a user see anyone else's keys.

## Who manages MCP: `mcp:manage`

**Manage MCP** (`mcp:manage`) governs the organization's MCP settings. Its holder can:

- set the organization's mode under **AI Setup** > **MCP Authentication**;
- list and revoke any MCP key in the organization;
- with the organization in app sign-in mode, register, edit and revoke OAuth clients, and list and revoke the organization's connected apps.

`mcp:manage` cannot create an org-wide key, and cannot create a key for another user. It implies `mcp:connect`, so its holder can create their own personal key. `mcp:manage` and **Manage AI** (`ai:manage`) are separate permissions, and neither implies the other. The AI Setup page opens only for holders of `ai:manage`, so an MCP administrator needs both to use the page.

### What needs `admin` itself

These actions need the `admin` permission, not only `mcp:manage`:

- marking an OAuth client as trusted;
- changing the return addresses of a trusted client;
- reading or changing the client policy for apps that publish a client metadata document.

See [App Sign-in (OAuth 2.1)](oauth.md).

## Administering keys

The **MCP Authentication** card of **AI Setup** lists every key in the organization for holders of `mcp:manage`.

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/ai/mcp/keys` | Every key in the organization, with type, owner (email), prefix, created, expires and last used |
| `DELETE /api/v1/ai/mcp/keys/:id` | Revoke any key in the organization. Answers `404` if the key does not exist. |
| `POST /api/v1/ai/mcp/keys/revoke-legacy` | Revoke every retired org-wide key that is not yet revoked |
| `POST /api/v1/ai/mcp/keys` | Retired. Answers `410`. |

The page notes: "Administrators can revoke any key but cannot create one for someone else." The owner column names a key's owner only when that user belongs to the administrator's organization.

## Org-wide keys are retired

The org-wide `wfmcp_…` keys of earlier releases are retired in 1.2.0.

- **They no longer authenticate.** Presenting one returns `401` with the message: "Org-wide MCP keys were retired in 1.2.0. Create a personal MCP key under Profile → Security."
- **They cannot be created.** `POST /api/v1/ai/mcp/keys` answers `410` with the code `org_keys_retired`.
- **They stay listed** as **Org-wide (retired)**, so you can clean them up. The 90-day removal of inactive personal keys never removes them.
- **Clean them up** with **Revoke all legacy keys** in the key table, or with `POST /api/v1/ai/mcp/keys/revoke-legacy`.

!!! warning "Revoke retired keys before a downgrade"
    Upgrading does not revoke org-wide keys. A 1.1.x build accepts them again, so if you might downgrade, click **Revoke all legacy keys** first.

## When revocation takes effect

| Transport | When a revocation applies |
| --- | --- |
| HTTP (`/mcp`) | On the next request. Each request is authenticated and admitted on its own. |
| WebSocket (`/ws/chat`) | On the next request on the socket. An idle socket is re-checked every 60 seconds, so it closes within a minute. |

A refused WebSocket closes with code `1008` and the reason "MCP credential is no longer valid".

So revoking a key, disabling a user, removing `mcp:connect`, suspending the tenant or turning off personal keys stops an active client on its next request, and an idle one within a minute. For an app, revoking its grant or the app, removing `mcp:connect` or leaving app sign-in stops it at its next request, whatever time its access token has left.

## Ending every session on an install

Disabling a user is the control for one account: the account is refused on every request, including its personal keys and app connections.

To end every signed-in session on an install at once:

- **Docker Compose or self-managed install:** give every service a new `JWT_SECRET` (and `WF_JWT_SECRET` where it is set), then recreate the containers. Browser sessions and the 15-minute access tokens of connected apps stop working, and every user signs in again.
- **WFA appliance:** WFA supplies this secret. Do not set it by hand.

!!! note "What rotating the secret does not end"
    Rotating `JWT_SECRET` does not revoke personal MCP keys, and does not end app connections: an app's refresh token does not depend on the secret, so the app gets a new access token at its next refresh. Revoke keys under **AI Setup** > **MCP Authentication**, and revoke app connections under **Connected apps in this organization**.

## Related pages

- [Personal MCP Keys](personal-keys.md)
- [App Sign-in (OAuth 2.1)](oauth.md)
- [Permissions](../../reference/permissions.md)
- [Errors](errors.md)
