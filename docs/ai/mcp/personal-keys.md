# Personal MCP Keys

A personal MCP key lets an AI client such as Claude Desktop, Cursor or Claude Code connect to WitFoo as you, with exactly your permissions.

## Before you start

- You need the **Connect MCP** (`mcp:connect`) permission. The key card is shown only to users who hold it. See [Authentication & Permissions](authentication.md).
- An administrator must have chosen **Browser chat sessions and personal keys** or **Browser chat sessions, personal keys and app sign-in** under **AI Setup** > **MCP Authentication**. See [Turning MCP On](configuration.md).
- The appliance licence must include the MCP connector. See [MCP Licensing](licensing.md).

## Create a key

1. Open **Profile** > **Security** and find the **MCP connections** card.
2. Enter a **Key name**, for example `Laptop` or `Claude Desktop`.
3. Enter **Expires in (days, 1-365)**. The default is 90.
4. Click **Create key**.
5. Under **Copy your key now**, copy the key and store it in your AI client.

!!! warning "The key is shown once"
    This is the only time the key is shown. Send it in the `X-MCP-Key` header, never in a URL. If you lose it, revoke it and create a new one.

Right after creation the card shows two ready-made snippets filled in with the new key: **Streamable HTTP client configuration** and **WebSocket client configuration**. See [Connecting AI Clients & Marketplaces](connect-clients.md).

## Key facts

| Fact | Value |
| --- | --- |
| Format | `wfmcpu_` followed by 64 lowercase hexadecimal characters. Only a SHA-256 hash of the key and a short display prefix are stored, so the key can never be shown again. |
| Lifetime | 1 to 365 days, default 90, chosen when you create the key. The key stops working at that moment. |
| Active keys | At most 5 active keys per user. Revoked and expired keys do not count. |
| Creation rate | At most 20 keys created in a rolling hour. A rotation counts as creating one. Past that the request is refused with `429` and a `Retry-After` header. |
| Inactive keys | A revoked or expired key stays in the list for 90 days after it stopped working, and is removed the next time you create or rotate a key after that. |
| Rows per user | At most 50 keys per user per organization, active and inactive together. When you hold 50 and create a key, your inactive keys that stopped working longest ago are removed first. |
| Rotation | Rotating issues a replacement with the same name and the same lifetime, then revokes the old key immediately. If the old key cannot be revoked, the replacement is revoked too, the old key keeps working, and the response says so. |
| Revocation | Immediate and permanent. A revoked key stays in the list, marked **Revoked**. |

## Key statuses

| Status | Meaning |
| --- | --- |
| **Active** | The key works. |
| **Expires in {days} days** | The key works, and expires within 14 days. |
| **Expired** | The key reached its expiry and no longer works. |
| **Revoked** | The key was revoked and no longer works. |
| **Retired** | A retired org-wide key from an earlier release. It no longer works. |
| **Not usable** | The organization's mode does not allow personal keys, so the dispatcher refuses every personal key. |

## Rotate or revoke a key

- **Rotate:** click **Rotate** on an active key and confirm. The current key stops working immediately, and the card shows the new key once.
- **Revoke:** click **Revoke** and confirm. Clients using the key stop working immediately.

An administrator with `mcp:manage` can also revoke any key in the organization under **AI Setup** > **MCP Authentication**. Administrators cannot create a key for someone else.

## When keys stop working

| Event | What happens to your keys |
| --- | --- |
| Your account is disabled | Every key is revoked. |
| Your account is enabled again | Every key you still own is revoked first. If that cannot finish, the enable fails with `503` and the account stays disabled. Old keys are never restored, so you create new ones. |
| Your password is reset or changed | Every key created before the reset stops working. The keys are not revoked, so the card keeps listing them as **Active** until they expire or you revoke them. Create new keys. |
| `mcp:connect` is removed from your roles | Your clients are refused on their next request. |
| The organization returns to **Browser chat sessions only** | Every key is refused, and the card shows them as **Not usable**. |

## What the card says when something is wrong

- **The list cannot be read:** the card shows an error with **Retry**, never "You have no MCP keys yet." A refresh that fails keeps the rows already shown and says they may be out of date.
- **Personal keys are off for the organization:** the card says so before you try anything. **Create key** is disabled, **Rotate** is not offered, **Revoke** and the list stay, and keys read **Not usable**. The card checks again when the window regains focus, so it opens without a reload once an administrator allows personal keys.
- **The licence does not include MCP:** the card shows a notice, and creating and rotating keys are disabled. See [MCP Licensing](licensing.md).

When a request is refused, the card explains it by its code:

| Code | Status | Meaning |
| --- | --- | --- |
| `personal_keys_disabled` | `409` | The organization's mode does not allow personal keys. |
| `personal_key_limit` | `409` | You already hold the most active keys allowed. Revoke keys you no longer use until you are under the limit, then try again. |
| `key_rotation_conflict` | `409` | The key was rotated or revoked by another request. The card refreshes the list. |
| `key_not_active` | `409` | Only an active key can be rotated, and this key is no longer active. The card refreshes the list. |

## Using a key

Send the key in a header:

- `X-MCP-Key: wfmcpu_xxxxxxxx` (preferred), or
- `Authorization: Bearer wfmcpu_xxxxxxxx`.

!!! warning "Never put a key in a URL"
    A personal key anywhere in a URL is refused with `400`, under any parameter name or encoding, on `/mcp` and on `/ws/chat`, `/ws/graph` and `/ws/events`. URLs end up in logs and browser history; headers do not.

### HTTP limits (`POST /mcp`)

- Each POST carries exactly one JSON-RPC request. A batch, even of one message, is refused with `400`.
- The body can be at most 1 MiB, and must be read within 15 seconds. A larger body is refused with `413`.

### WebSocket limits (`/ws/chat`)

- A message larger than about 6 MB closes the socket with close code `1009`. A notification larger than 512 KiB does the same.
- At most 5 open sessions per user, whatever the credential (your browser session and all your keys share this budget), and 100 in all on the appliance. Over either cap the connection is refused with `429` and `Retry-After: 30`.

## Self-service API

Every route needs `mcp:connect`, re-checked live against your current roles, active status and home organization.

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/users/me/mcp-keys` | List your keys: name, prefix, created, expires, last used and revoked. Never returns a secret. |
| `POST /api/v1/users/me/mcp-keys` | Create a key, with a body such as `{"name": "Laptop", "expires_in_days": 90}`. The response's `secret` is shown once. |
| `POST /api/v1/users/me/mcp-keys/:id/rotate` | Rotate an active key. The response carries the new `secret`. |
| `DELETE /api/v1/users/me/mcp-keys/:id` | Revoke one of your keys. |

Responses that carry a secret send `Cache-Control: no-store` and `Pragma: no-cache`.

## Audit

Every key event is written to the organization's audit log: `mcp_key_issued`, `mcp_key_rotated`, `mcp_key_revoked`, `mcp_key_revoked_by_admin` and `mcp_legacy_keys_revoked`. Entries record the address the request came from, and never a secret or a hash.

## Upgrade and downgrade notes

- **Downgrading** below 1.2.0 disables every personal key, because older builds do not recognise the `wfmcpu_` format.
- **Secret scanners** and client-side validators that match `^wfmcp_` do not match `wfmcpu_`. Update any pattern you maintain.
