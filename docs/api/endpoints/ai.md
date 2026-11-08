# AI

AI provider configuration, chat sessions, and MCP administration.

Paths in the tables below are relative to `/api` unless they start with `/oauth` or `/.well-known`, which are served at the root of the appliance.

## AI Configuration

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/configs` | Any signed-in user | List AI provider configurations. The API key is never returned, and `base_url` is shown without its user information, query or fragment. |
| GET | `/v1/ai/configs/:id` | Any signed-in user | Get one configuration |
| POST | `/v1/ai/configs` | `ai:manage` | Create a configuration |
| PUT | `/v1/ai/configs/:id` | `ai:manage` | Update a configuration |
| DELETE | `/v1/ai/configs/:id` | `ai:manage` | Delete a configuration |
| PUT | `/v1/ai/configs/:id/enable` | `ai:manage` | Enable or disable a configuration. The body must state the value, for example `{"enabled": false}`. |
| GET | `/v1/ai/configs/:id/models` | `ai:manage` | List the models a stored configuration can use |
| GET | `/v1/ai/providers` | `ai:manage` | List the supported providers |
| POST | `/v1/ai/providers/:provider/models` | `ai:manage` | List a provider's models before the configuration is saved |
| GET | `/v1/ai/purpose-routing` | Any signed-in user | Read which configuration serves each purpose |
| PUT | `/v1/ai/purpose-routing` | `ai:manage` | Change the purpose routing |
| GET | `/v1/ai/response-automation` | Any signed-in user | Read the response automation settings |
| PUT | `/v1/ai/response-automation` | `ai:manage` | Change the response automation settings |
| GET | `/v1/ai/profile` | `ai:manage` | Read the model profile |
| PUT | `/v1/ai/profile` | `ai:manage` | Change the model profile |

## Chat Sessions

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/chat/sessions` | `ai:read` | List your chat sessions |
| POST | `/v1/ai/chat/sessions` | `ai:write` | Create a chat session |
| GET | `/v1/ai/chat/sessions/:id` | `ai:read` | Get a session |
| GET | `/v1/ai/chat/sessions/:id/messages` | `ai:read` | Get a session's messages |
| POST | `/v1/ai/chat/sessions/:id/messages` | `ai:write` | Send a message |
| PUT | `/v1/ai/chat/sessions/:id/title` | `ai:write` | Rename a session |
| DELETE | `/v1/ai/chat/sessions/:id` | `ai:write` | Delete a session |

## MCP Configuration

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/mcp` | Any signed-in user | Read the organization's MCP settings, including `auth_mode` |
| PUT | `/v1/ai/mcp` | `mcp:manage` | Change the MCP settings, for example `{"auth_mode": "api_key"}` |
| GET | `/v1/ai/mcp/relay` | `mcp:manage` | Read the MCP relay status shown on AI Setup |

`auth_mode` is `off` (the default), `api_key` or `oauth`.

- `PUT` answers `409` with the code `oauth_unavailable` when `oauth` is chosen on an appliance that is not set up for app sign-in.
- Moving the organization out of `oauth` revokes every app grant first. If that revocation fails, the `PUT` answers `500` and the mode stays as it was.
- On a licence that does not include MCP, a `PUT` that turns something on answers `403` with `feature_not_available`.

See [MCP Configuration](../../ai/mcp/configuration.md).

## MCP Keys (administration)

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/mcp/keys` | `mcp:manage` | List every key in the organization, with type, owner email, prefix, created, expires and last used |
| DELETE | `/v1/ai/mcp/keys/:id` | `mcp:manage` | Revoke any key in the organization. `404` if it does not exist. |
| POST | `/v1/ai/mcp/keys/revoke-legacy` | `mcp:manage` | Revoke every retired org-wide key that is not yet revoked |
| POST | `/v1/ai/mcp/keys` | `mcp:manage` | Retired. Answers `410` with the code `org_keys_retired`. |

An administrator can list and revoke any key, but cannot create a key for someone else.

## Personal MCP Keys

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/users/me/mcp-keys` | `mcp:connect` | List your keys. Never returns a secret. |
| POST | `/v1/users/me/mcp-keys` | `mcp:connect` | Create a key: `{"name": "…", "expires_in_days": 90}`. The response `secret` is shown once. |
| POST | `/v1/users/me/mcp-keys/:id/rotate` | `mcp:connect` | Rotate an active key. The response carries the new `secret`. |
| DELETE | `/v1/users/me/mcp-keys/:id` | `mcp:connect` | Revoke one of your keys |

Responses that carry a secret send `Cache-Control: no-store`. See [Personal MCP Keys](../../ai/mcp/personal-keys.md).

## App Sign-in Administration

These routes answer `404` unless the appliance is set up for app sign-in and the organization's `auth_mode` is `oauth`. A caller without the permission is refused first.

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/mcp/grants` | `mcp:manage` | List every live app grant in the organization |
| DELETE | `/v1/ai/mcp/grants/:grant_id` | `mcp:manage` | Revoke one grant |
| GET | `/v1/ai/mcp/oauth-clients` | `mcp:manage` | List the registered clients |
| POST | `/v1/ai/mcp/oauth-clients` | `mcp:manage`; also `admin` to set `trusted` | Register a client: `{"name": "…", "redirect_uris": ["…"], "trusted": false}`. The response carries its Client ID. |
| PATCH | `/v1/ai/mcp/oauth-clients/:id` | `mcp:manage`; also `admin` to change trust or a trusted client's return addresses | Change a client's name, return addresses or trust |
| DELETE | `/v1/ai/mcp/oauth-clients/:id` | `mcp:manage` | Revoke a client and every grant held for it |
| GET | `/v1/ai/mcp/oauth-policy` | `admin` | Read the client policy for apps that publish a client metadata document |
| PUT | `/v1/ai/mcp/oauth-policy` | `admin` | Replace the client policy. A save that denies an app revokes that app's grants. |
| GET | `/v1/users/me/mcp-grants` | `mcp:connect` | List the apps connected as you |
| DELETE | `/v1/users/me/mcp-grants/:grant_id` | `mcp:connect` | Revoke one of your app connections |
| POST | `/v1/oauth/authorize/describe` | `mcp:connect` | Used by the consent page to describe a request |
| POST | `/v1/oauth/authorize/decision` | `mcp:connect` | Used by the consent page to approve or deny a request |

See [App Sign-in (OAuth 2.1)](../../ai/mcp/oauth.md).

## OAuth Endpoints

These are served at the root of the appliance once `MCP_PUBLIC_URL` and `MCP_OAUTH_UI_URL` are both set to valid values.

| Method | Path | Description |
| --- | --- | --- |
| POST | `/oauth/token` | Token endpoint. A form POST of at most 8 KiB. Every response sends `Cache-Control: no-store`. |
| GET | `/.well-known/oauth-protected-resource` | Protected-resource metadata |
| GET | `/.well-known/oauth-protected-resource/mcp` | Protected-resource metadata for `/mcp` |
| GET | `/.well-known/oauth-authorization-server` | Authorization-server metadata |

There is no registration endpoint.

## Errors

For MCP-specific responses, see [MCP Errors](../../ai/mcp/errors.md).
