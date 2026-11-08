# MCP Licensing

The MCP connector, both `/ws/chat` and `/mcp`, is a licensed feature, `mcp_connector`, included with Analytics Pro, Analytics Max and Reporter Pro.

## Which licences include MCP

| Licence | MCP connector |
| --- | --- |
| Analytics Pro, Analytics Max, Reporter Pro | Included |
| Analytics Lite, Reporter Lite, Conductor Lite, Conductor Pro, Conductor Max, Console Lite | Not included: MCP connections are refused |

The licence is per appliance. See [Product Tiers](../../reference/product-tiers.md) for every feature by SKU.

### When the licence is not known

An unresolved licence is never treated as a refusal. MCP is allowed when:

- the appliance has not yet learned its licence since it started, or cannot reach the licensing service;
- the licence names a product and tier this build does not know. The dispatcher logs a warning.

If a licence was learned and a later check fails, the last licence learned applies.

**Expiry is not an input.** As for every licence feature, the decision is made by SKU, not by expiry date.

## What happens on a licence without MCP

Nothing is deleted. Keys, the organization's mode and the key list are left as they are, so moving to a licence that includes MCP restores access with the existing keys.

### Clients

A refused request gets `403` on both transports, with a body like this:

```json
{"error":"feature_not_available","feature":"mcp_connector","product_type":"analytics","tier":"lite",
 "licensed_for":["analytics:max","analytics:pro","reporter:pro"],
 "message":"The MCP connector is not included in this appliance's license (Analytics Lite). It is included in Analytics Max, Analytics Pro and Reporter Pro."}
```

The body names the licence's product and tier, the feature and the SKUs that include it, and nothing else from the licence. A licence refusal is not a failed sign-in: it is not a `401`, and the failed-authentication throttle does not count it.

An open WebSocket closes with code `1008` and the reason "MCP connector is not licensed on this appliance".

### The product

- **AI Setup** and **Profile** > **Security** > **MCP connections** show a notice, **The MCP connector is not part of this license**, that names your licence and the SKUs that include the connector.
- On **Profile** > **Security**, creating and rotating a key are disabled. Revoking a key and the list still work.
- On **AI Setup**, turning MCP on is disabled. `PUT /api/v1/ai/mcp` answers `403` for a request that turns something on: **MCP Server Enabled** from off to on, or a mode other than **Browser chat sessions only** that is not the stored one. Turning MCP off, editing the other settings, and every read always work.
- `POST /api/v1/users/me/mcp-keys` and `POST /api/v1/users/me/mcp-keys/:id/rotate` answer `403`.
- App sign-in: the consent page refuses approval with `403 feature_not_available`. The token endpoint does not check the licence, so existing app connections survive a lapse and a renewal, but every request they make on `/mcp` is refused.

The API's refusals use the standard error envelope, with `code` `feature_not_available`, the same message, and the licence's facts under `details`.

## How long a licence change takes

A licence change reaches MCP within:

- the incident engine's licence check interval, `LICENSE_CHECK_INTERVAL` (1 hour by default; restarting the incident engine checks at once), plus
- up to 30 seconds for the dispatcher to read it, plus
- up to 60 seconds for an idle WebSocket to be re-checked.

`/mcp` is stateless, so a change applies to its next request.

## The relay and the exposure listener

- The [AI-connector relay](relay.md) is stricter than the appliance's own MCP endpoint: it needs a current licence that includes the MCP connector, and it refuses a licence it cannot place.
- The [exposure listener](exposure-listener.md) on port 8444 is not tied to a SKU. The requests it carries pass the same licence check as on `:443`.
