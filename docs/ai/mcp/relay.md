# AI-Connector Relay

The AI-connector relay gives an AI marketplace or MCP client an address that reaches your appliance's MCP endpoint through WitFoo, without opening an inbound port on the appliance.

## What it is

- The appliance makes **one outbound HTTPS connection** to `mcp-relay.witfoo.com` on port 443 and keeps it open. A client's request to the appliance's relay address travels down that connection, and the appliance's answer comes back up it.
- The relay carries **five paths and no others**: the MCP endpoint, its two protected-resource metadata documents, the authorization-server metadata document and the token endpoint. A request to any other path is refused at the relay and never reaches the appliance.
- The **consent page is not relayed**. It stays on the analytics UI, so for app sign-in the approving user's browser must reach the UI.
- **Every rule is unchanged.** The same permissions, personal keys, tools and admission checks apply to a relayed request. See [Authentication & Permissions](authentication.md).
- It is **off by default** for every organization and every appliance. Only an operator on the appliance can turn it on.

## Requirements

- WFA 2.5.1 or later on the appliance (install WFA 2.5.4, the current release), which provides `wfa mcp-relay`.
- Analytics 1.2.0 images.
- The MCP HTTP transport turned on: `"mcp_http_enabled": true` in `node.json`. `wfa mcp-relay enable` does not change it, and refuses while it is off, because a tunnel to an appliance whose MCP endpoint answers `404` relays nothing. See [Turning MCP On](configuration.md).
- A current licence that includes the MCP connector: Analytics Pro, Analytics Max or Reporter Pro. The relay is stricter than the appliance's own MCP endpoint: it refuses a licence it cannot place. See [MCP Licensing](licensing.md).
- Outbound HTTPS from the appliance to `mcp-relay.witfoo.com` on port 443. No inbound port is opened.

!!! note "No proxy, no offline mode"
    The relay connection uses no HTTP proxy, whether configured or ambient, and no setting can name another relay host. An appliance in `offline_mode` cannot register, and the relay stops while `offline_mode` is set. To resume after clearing `offline_mode`, run `wfa mcp-relay ack` if asked, then `wfa restart`.

## The notice

Turning the relay on shows this notice. You acknowledge it by typing `ENABLE`.

!!! note "Relay notice (version 2)"
    **R1.** While the relay is on, your AI assistant's requests and your appliance's answers pass through WitFoo's relay service. The relay reads each one into memory to pass it on, so the sign-in tokens, personal keys and content in it can be read by the relay's software while they pass through. This applies to requests sent to the relay's address; an AI assistant that connects to your appliance's own address does not pass through the relay. Your appliance's own calls to the relay (to register, connect, acknowledge, report its status and revoke) also reach the relay readable, and carry your licence key or the relay credential.

    **R2.** The relay's address is served through Cloudflare, which acts as a proxy in front of WitFoo's relay. Cloudflare ends the encrypted connection at its network edge and passes the traffic on to WitFoo, so Cloudflare can also see what passes through: requests, answers, access and refresh tokens, personal keys, your licence key when the appliance registers, reports its status or revokes, and the relay credential when it connects and acknowledges. The registration and tunnel connections use the same address, so they pass through Cloudflare too. Cloudflare also sees the details of each connection: the network addresses of the caller and of your appliance, the time, the sizes, and the address's handle. Cloudflare keeps its own records of some requests, such as those its security rules block or limit, including the caller's network address and the path, for up to 30 days.

    **R3.** WitFoo's relay holds the content of requests and answers, and any token or key in them or sent with them, in memory only while it passes them on, and writes none of it to its database or logs. It keeps a one-way hash of the credential your appliance uses to connect for as long as the address exists. Its encrypted backups keep that hash until they are deleted: up to 37 days after the address is revoked, plus the time until the database's next clean-up (R4).

    **R4.** The relay's logs record, for each request, a request identifier, the address's handle, the method, the path, the time, the status, the sizes, the duration and the outcome. The method is the text the caller sent, kept up to 256 bytes, so a caller that puts anything other than a method there puts it in the log. They also record when a tunnel comes up or goes down, with the code that says why it closed, when an address is created, acknowledged or revoked, and an alert when a registering licence looks like a trial, cloud or offer licence. Some of those lines carry a short one-way fingerprint of your licence key or of the relay credential: the first eight characters of its SHA-256 hash. Until the address is revoked, the relay keeps a record of your organisation and appliance identifiers and the name your appliance gave as the person who switched the relay on. Anyone who holds your licence key can read that name. If your licence lapses, or your appliance is lost, the record stays until the address is revoked. The relay also keeps a second record of your organisation's entitlement (organisation, product, tier, expiry and the time it was last checked). It is rewritten about every 15 minutes while a tunnel is up. It expires 48 hours after it was last written and is removed from the database's storage 3 days after that write, plus the time until the database's next clean-up, so it can outlast a revocation. Event records that name the person who switched the relay on expire after 7 days and are removed from storage 8 days after they were written, plus the time until the database's next clean-up; the name kept in the first record above is not part of them, and stays until the address is revoked. Logs are kept for 30 days and are gone about a day after that. WitFoo backs up the relay's database every night, and again within an hour after an address is created or revoked. Each backup is encrypted before it leaves the relay's server, is stored in WitFoo's Oracle Cloud storage in Chicago, and is deleted automatically 35 days after it was made, or about a day later at most; the relay's server also keeps its own copy of each backup for up to 5 days. A backup holds the database's storage as it was when the backup was made, including records that had already expired or been cleared but were not yet removed from storage, so a record described in R3 and R4 can remain in a backup until that backup is deleted: up to 36 days after the record was removed from the database's storage. So that restoring a backup does not bring a revoked address back into use, the relay also keeps a list of when each address was created and revoked, naming only the address's handle, encrypted in the same storage and kept for the same 35 days.

    **R5.** The network address the relay sees for the machine that connects to it is passed to your appliance with each relayed request, so your own logs may record it, and a support pack made from those logs can reach WitFoo. The relay does not write it to its logs, database or metrics. It keeps it in memory as a rate-limit key.

    **R6.** The relay runs on Oracle Cloud Infrastructure in Chicago. Cloudflare handles the traffic at its own network edge, which may be outside that region.

    **R7.** It is off by default for every organisation and every appliance, and turning it on is your act on this appliance. When you turn it off and the relay can be reached, the address is revoked and the relay clears its record linking the address to your appliance from its tables. A small record that the address existed and was revoked stays, and event records and log lines already written expire on their own schedule. Backups made before the cleared record was removed from the database's storage keep it until they are deleted: up to 37 days after the address is revoked, plus the time until the database's next clean-up (R4). WitFoo's restore procedure keeps a restored relay closed to outside connections until it has revoked again every address that the list described in R4 records as revoked (if the list cannot be read, the relay stays closed until WitFoo reopens it by hand, and a revocation made after that backup was taken can then be undone), and shortly after each time the relay starts it revokes again the addresses revoked in the previous 7 days. A revocation made shortly before the relay's server is lost, and not yet copied off that server (which normally happens within about two minutes), can also be undone by a restore. Apart from these cases, a revocation is final once the relay has confirmed it. Turning the relay on again gives a new address. If your appliance can no longer revoke the address, ask WitFoo support (<support@witfoo.com>) to revoke it.

    **R8.** It does not make the appliance reachable for anything but five paths: the MCP endpoint, its two protected-resource metadata documents, the authorization-server metadata document and the token endpoint. The consent page stays on the analytics UI and is not relayed.

    **R9.** An air-gapped or privacy-sensitive deployment should leave it off.

    **R10.** Prefer short-lived keys, or OAuth sign-in where it is available through the relay, and rotate personal keys after you revoke the relay address.

When the notice changes version, a relay acknowledged at the old version stops. Run `wfa mcp-relay ack`, read and acknowledge the new notice, then run `wfa restart`. The address does not change. While the relay is stopped, AI Setup shows no relay card, and `wfa mcp-relay status` reports "re-acknowledgement required".

## Turn it on

Run these steps on the appliance, as an administrator.

1. Make sure the MCP HTTP transport is on (`"mcp_http_enabled": true` in `node.json`).
2. Run:

    ```bash
    wfa mcp-relay enable
    ```

    The command needs a terminal. It shows the notice, and anything other than the word `ENABLE` leaves the relay off; the default is No. No flag, environment variable, file or Console message can turn the relay on.

3. The command registers the appliance with the relay, writes the address, a credential and your acknowledgement to `node.json`, and prints the address.
4. Run:

    ```bash
    wfa restart
    ```

    WFA reads `node.json` only when it starts, so the relay carries nothing until the restart. `wfa restart` stops and starts every container on the appliance. The Console Restart job for the node does the same.

5. List the printed address in each marketplace, and give each client a personal key to send.

The address has this form, where the handle is 26 characters from `a-z` and `2-7`:

```text
https://mcp-relay.witfoo.com/h/<handle>/mcp
```

If `mcp_public_url` was empty, `enable` sets it to the relay address, so that sign-in challenges name it. If it already held another address, it is left as it is, and app sign-in stays on that address and is not offered through the relay. While the relay is stopped, its address is not offered as the sign-in address.

## Commands

| Command | What it does |
| --- | --- |
| `wfa mcp-relay enable` | Shows the notice, and on `ENABLE` registers the appliance and writes the relay's fields to `node.json`. Needs a terminal. Refuses while this appliance already holds a relay address, while a revocation is pending, in offline mode, and while `mcp_http_enabled` is false. |
| `wfa mcp-relay ack` | Shows the current notice and records a new acknowledgement after a notice version change. Needs a terminal. The address does not change. Refused while `offline_mode` is set. |
| `wfa mcp-relay status` | Shows what `node.json` holds and how the relay says it is doing. |
| `wfa mcp-relay off` | Revokes the address for good and turns the relay off. Asks you to type `REVOKE`; in a script, add `--yes`. |
| `wfa mcp-relay revoke` | The same as `off`. |

After `enable`, `ack` or `off`, run `wfa restart`. Until then the running containers keep the settings they started with, and `wfa mcp-relay status` reports what `node.json` says.

### Re-acknowledging

The relay accepts three acknowledgements for an address at once, and then one a minute. Past that, `wfa mcp-relay ack` says the relay is limiting requests and to try again in a minute. Once the current notice is acknowledged, running `ack` again changes nothing and does not contact the relay.

### Status

`wfa mcp-relay status` shows whether the relay is on, the address, the acknowledgement (notice version, who and when), `mcp_public_url` when it holds another address, and the relay's own report: its state, connected since and last request. It also names the stopped states, such as "re-acknowledgement required", a pending revocation and offline mode, and warns when `mcp_http_enabled` is false.

If the status reports the address as revoked or not listed, the relay no longer serves it: run `wfa mcp-relay off`, then `wfa mcp-relay enable` for a new address.

## Turn it off

1. Run:

    ```bash
    wfa mcp-relay off
    ```

2. Type `REVOKE`. Anything else changes nothing.
3. The command asks the relay to revoke the address. Only once the relay confirms, or says the address is already gone, does it clear the address, the credential and the acknowledgement from `node.json`. If `mcp_public_url` held the relay address, it is cleared too.
4. Run `wfa restart`.

If the relay cannot be reached, the revocation stays pending: the credential is kept so the revocation can be retried, the relay is turned off in `node.json`, and the command exits non-zero. Run `wfa mcp-relay off` again when the relay can be reached. Until `wfa restart`, a pending revocation keeps the tunnel up, and the relay can still carry requests to the appliance.

Revocation is permanent. A revoked address is never restored, turning the relay on again gives a new address, and every client configured with the old address stops working until it is given the new one. Rotate the personal keys those clients held.

If your appliance can no longer revoke the address, ask WitFoo support (<support@witfoo.com>) to revoke it. See [Known limitations](#known-limitations).

## The AI Setup relay card

**Settings** > **General Settings** > **AI Setup** > **MCP relay** needs the `mcp:manage` permission, and is shown **only while the relay is enabled** on the appliance. When the relay is off, stopped for re-acknowledgement, or the page cannot read the API's relay status, there is no card. Use `wfa mcp-relay status` on the appliance instead.

The card is read-only. It reads once when the page opens and again each time you click **Refresh**. It shows:

| Field | Meaning |
| --- | --- |
| **Address for AI clients** | The relay address to give your clients |
| State | One of the states below |
| **Connected since** | When the current tunnel came up |
| **Last request** | When the relay last carried a request |
| **Relay client** | The version of the appliance's relay client |
| **Turned on by** and **Turned on at** | Who turned the relay on and when, as recorded by the appliance |
| **Notice (version {version})** | The notice that was acknowledged |

| State | Meaning |
| --- | --- |
| **Connected** | The relay reports that this appliance is connected. |
| **Not connected** | The relay lists this address, but reports no tunnel from this appliance right now. Requests to the address fail until the appliance connects. |
| **Revoked** | The relay reports this address as revoked. Run `wfa mcp-relay off` and then `wfa mcp-relay enable` for a new address. |
| **Not listed** | The relay does not list this address. Run `wfa mcp-relay off` and then `wfa mcp-relay enable` for a new one. |
| **Status unavailable** | The relay's status could not be read just now. This does not mean the relay is off or that the appliance is disconnected. It is also shown when the address is contested (see [Known limitations](#known-limitations)). |

## Configuration reference

The relay's `node.json` fields are written only by `wfa mcp-relay`. No wizard question, Console message or environment variable sets them, and a re-run of `wfa configure` or `wfa fetch` keeps them.

| `node.json` field | Purpose |
| --- | --- |
| `mcp_relay_enabled` | `true` while the relay is on |
| `mcp_relay_handle` | The address's handle: 26 characters from `a-z` and `2-7` |
| `mcp_relay_credential` | The secret the appliance authenticates its tunnel with |
| `mcp_relay_ack` | The `version`, `at` and `by` of the notice the operator acknowledged |
| `mcp_relay_revoke_pending` | `true` after `wfa mcp-relay off` could not reach the relay |

WFA passes the relay's settings to the containers as environment variables:

| Environment variable | Container | Purpose |
| --- | --- | --- |
| `MCP_RELAY_ENABLED` | reverse proxy, api | Exactly `true` while the relay runs |
| `MCP_RELAY_HANDLE` | reverse proxy, api | The handle |
| `MCP_RELAY_CREDENTIAL` | reverse proxy only | The tunnel credential |
| `MCP_RELAY_REACK_REQUIRED` | api only | Exactly `true` while the relay is stopped for a new acknowledgement |

The relay host is not a setting: `mcp-relay.witfoo.com` is built in, and no field or variable names another host.

### Re-running `wfa configure` or `wfa fetch`

A re-run keeps every `mcp_` field of `node.json`, the relay's included. A value that cannot be read is named and left out, and the old file is kept beside the new one as `node.json.unreadable-<time>.bak`. If the lost value is the relay's switch, its pending revocation or its acknowledgement, the relay is stopped and `wfa mcp-relay status` says so: `wfa mcp-relay ack` turns it back on at the same address, and `off` revokes it.

Other `node.json` settings that no `wfa configure` prompt asks for, such as `trusted_proxies`, are not kept. Set them again after a re-run, then run `wfa restart`.

### Support packs

Support packs mask the relay's handle and credential, including the handle inside a saved address.

## Which clients work

The relay forwards each request as it arrived, so a client works when it can do what the appliance's MCP endpoint asks of it:

- **A client that can send a static credential** works, configured with a personal key, such as a command-line or desktop client. A hosted connector that takes one static credential for a whole organization shares it between everyone in that organization, so give it the personal key of a dedicated user who holds only the permissions the connector needs, never an administrator's.
- **An app that signs in with OAuth** works when app sign-in is configured on the appliance (`mcp_public_url` and `mcp_oauth_ui_url`) and the browser of the person who approves can reach the analytics UI. See [App Sign-in (OAuth 2.1)](oauth.md).

See [Connecting AI Clients & Marketplaces](connect-clients.md).

## Limits

- An organization can hold relay addresses for up to **four appliances** at a time. An address counts until it is revoked, including while that appliance's relay is stopped.
- An organization whose licence came from a WitFoo promotional offer, such as the Black October offer, can hold **one**; a second is refused until the first one's address is revoked. WitFoo's operations team is told when an offer licence registers. The one-appliance limit and that notice take effect once WitFoo's licensing service is updated; until then an offer licence is held to four appliances like any other. An organization on an offer licence that needs more appliances can ask WitFoo to lift it to four.
- Once WitFoo's licensing service is updated, an offer licence stays an offer licence when its term is extended. The one-appliance limit is checked when an appliance registers, so an appliance already registered when the limit takes effect keeps its address.

## Known limitations

- **A contested address shows as "Status unavailable".** If another party presented this appliance's relay credential while its tunnel was up (in the last 15 minutes), the AI Setup card shows "Status unavailable" and `wfa mcp-relay status` shows `contested`. A second party may hold the credential, for example from a copied `node.json`. Revoke the address (`wfa mcp-relay off`), enable the relay again (`wfa mcp-relay enable`), run `wfa restart`, give your MCP clients the new address and rotate the personal keys they held.
- **An address that cannot be revoked from the appliance.** If `node.json` holds only one of the relay's handle and credential, for example after a re-run of `wfa configure` or `wfa fetch` could not read the other, `wfa mcp-relay off` stops the relay, says the address is not revoked and exits non-zero, and `enable` refuses. Copy the missing value back from the `node.json.unreadable-<time>.bak` copy and run `off` again, or ask WitFoo support (<support@witfoo.com>) to revoke the address. Once support confirms, remove the remaining relay fields from `node.json` by hand before you enable again: `mcp_relay_handle` or `mcp_relay_credential`, `mcp_relay_enabled`, `mcp_relay_ack` and `mcp_relay_revoke_pending`, plus `mcp_public_url` if it holds the old relay address.
- **Plain-text refusals reach the client as a status code only.** Through the relay, a refusal the MCP server writes as plain text (an unsupported content type, a malformed request, or a method it does not serve) reaches the client as a status code without its explanatory text. Clients should read the status.
