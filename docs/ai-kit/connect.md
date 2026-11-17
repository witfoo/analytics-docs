# Connect Your Assistant to WitFoo

Part of [the WitFoo AI desktop kit](index.md). This page connects Claude or ChatGPT to your WitFoo Analytics 1.2.0 appliance. The [MCP Server](../ai/mcp/index.md) pages hold the full reference for every step.

WitFoo Analytics 1.2.0 includes an MCP connector. MCP (Model Context Protocol) is an open standard that AI assistants such as Claude and ChatGPT use to reach outside tools. With it, your assistant can read your WitFoo work units and their evidence, signals, nodes, compliance figures, reports, playbook runs and platform health, limited to what your WitFoo role can see. With app sign-in, it can make changes for you, such as running a playbook, only if you allow them; a personal key can make any change your role allows.

## Before you start

| What | Needed |
| --- | --- |
| Licence | Analytics Pro, Analytics Max or Reporter Pro. Other licences refuse MCP connections. Playbooks need Analytics Pro or Max. See [MCP Licensing](../ai/mcp/licensing.md). |
| Appliance | WitFoo Analytics 1.2.0 or later, with WFA 2.5.1 or later, and MCP turned on as described below. |
| MCP address | An `https` address ending in `/mcp`, for example `https://mcp.example.com/mcp`, that your AI provider's servers can reach from the internet on the standard HTTPS port, 443. Claude and ChatGPT connect from their own servers, not from your computer. |
| Your account | A WitFoo account that holds **Connect MCP** (`mcp:connect`). The built-in **Admin** and **Platform Admin** roles have it. No other built-in role does, so give anyone else a custom role that includes it. Connect MCP grants no tool by itself. The custom role also needs each job's permissions: **Read Work Units** (`work_units:read`) for the brief; **Write Work Units** (`work_units:write`), **Manage Playbooks** (`playbooks:manage`) and **Read Users** (`users:read`) for incident response; **Read Reports** (`reports:read`) and **Read Work Units** (`work_units:read`) for the board briefing; **Read Reports** (`reports:read`) and **Read Auditor** (`auditor:read`) for the questionnaire. A write permission includes read, and a manage permission includes both. See [Authentication & Permissions](../ai/mcp/authentication.md). |
| Your AI app | A Claude or ChatGPT plan that lets you add a custom connector. On a Claude Team plan, an owner adds the connector in the organization's settings, and each member then connects it. On a ChatGPT business plan, a workspace administrator may need to allow WitFoo before members can connect it. |

## Turn it on

MCP is off until two switches are on: the HTTP transport on the appliance, which the appliance operator sets, and the organization's mode in WitFoo, which an administrator sets. See [Turning MCP On](../ai/mcp/configuration.md).

### On the appliance (operator)

1. In `/witfoo/configs/node.json`, set `"mcp_http_enabled": true`. Without it, `/mcp` answers `404`.
2. For Claude and ChatGPT to sign in through your appliance, also set the appliance's MCP address (`mcp_public_url`) and the web address of WitFoo where users approve apps (`mcp_oauth_ui_url`). See [App Sign-in (OAuth 2.1)](../ai/mcp/oauth.md#operator-settings).
3. Run `wfa restart`.

```json
{
  "mcp_http_enabled": true,
  "mcp_public_url": "https://mcp.example.com/mcp",
  "mcp_oauth_ui_url": "https://analytics.example.com"
}
```

Enter the MCP address exactly as it is set, with no trailing slash.

**Publishing the MCP address.** To publish only what Claude and ChatGPT need, use the appliance's optional [exposure listener](../ai/mcp/exposure-listener.md) on port 8444 (`"mcp_exposure_enabled": true`). It serves `/mcp` and the sign-in endpoints and nothing else. Put it behind a proxy or load balancer that answers on port 443 with a certificate for the name you publish, declare that proxy to the appliance as a trusted proxy, and restrict who can reach the port at your perimeter, because the listener itself restricts no sources. Your own browser must still reach the WitFoo web interface, where you approve the app. If you cannot open an inbound port, see the relay under [Where your data goes](index.md#where-your-data-goes). For Claude or ChatGPT to sign in through the relay, leave `mcp_public_url` empty before you run `wfa mcp-relay enable`; `enable` then sets it to the relay address. If `mcp_public_url` already holds another address, app sign-in stays on that address and is not offered through the relay. Set `mcp_oauth_ui_url` as usual: the approval page is not relayed, so your browser must reach the WitFoo web interface.

### In WitFoo (administrator)

1. Open **Settings** > **General Settings** > **AI Setup** and find **MCP Authentication**. The page needs the **Manage AI** permission and the card needs **Manage MCP**. The built-in Admin role has both.
2. Under **Who can connect over MCP**, the default is **Browser chat sessions only**, so no personal key and no app can connect. Choose **Browser chat sessions and personal keys**, or **Browser chat sessions, personal keys and app sign-in**. Claude and ChatGPT need the second to sign in through your appliance, and it can be chosen only when the appliance's MCP address and web address are set. Click **Save Authentication**.
3. Under **Client policy** (this needs the `admin` permission), add the apps that may sign in. The default, **Only apps on the allow list**, admits no app until you add one.
    - For Claude, use **Add to the allow list** > **Claude**.
    - For ChatGPT, add the host `chatgpt.com` to the **Allow list** on its own line. This is the host ChatGPT identified itself from when WitFoo tested it. ChatGPT's client document address varies, and a host entry admits every app whose metadata document is at `chatgpt.com`, not only yours. Each user still approves on the appliance's page, so check the app's host there.
4. **Most access an app with a metadata document can be given** is read-only (`mcp:read`) by default. Raise it only if you want users to be able to let an app make changes. Click **Save policy**.

Under **MCP Authentication** you see every personal key in the organization and, under **Connected apps in this organization**, every connected app, and you can revoke any of them at any time. See [Client policy](../ai/mcp/oauth.md#client-policy).

## Connect Claude

Claude changes its menu names from time to time. These are as of November 2026.

### On a Team or Enterprise plan

An owner adds WitFoo once for the organization:

1. Open **Organization settings** > **Connectors** and click **Add**. Choose **Custom**, then **Web**.
2. Enter the name **WitFoo** and your appliance's MCP address, then click **Continue**.
3. Choose a sign-in option, not **No sign in**. Under **OAuth client**, choose **Use Claude's published identity (Recommended)**. That is the identity the **Claude** entry on your client policy admits.
4. Leave **Request headers** empty. A personal key entered there would give everyone who uses the connector that key's access.
5. Click **Add**.

Each member then connects it:

1. Open **Customize** > **Connectors**, find WitFoo in the list (it usually has a **Custom** label), and click **Connect**.
2. Continue with [Approve on your appliance](#approve-on-your-appliance).

### On an individual plan

1. Open **Customize** > **Connectors**, click **+ Add**, then **Add custom connector**.
2. Follow steps 2 to 5 of the owner's steps above.
3. Continue with [Approve on your appliance](#approve-on-your-appliance).

### Approve on your appliance

1. Your browser opens your appliance's page, **Connect an app to WitFoo**. Sign in if asked. The appliance asks when your last sign-in is more than 15 minutes old.
2. The page says **This app will be able to read what you can read in WitFoo.** Check that the app's name and the host the approval goes to are the app you are connecting (`claude.ai` for Claude). If not, click **Deny**. Otherwise click **Approve**.
3. Back in Claude, WitFoo shows as connected and lists its tools. WitFoo marks each tool as either read-only or one that makes changes, and Claude can use that mark to ask you before it runs a tool that makes a change.

The connection is listed under **Profile** > **Security** > **Connected apps** in WitFoo.

## Connect ChatGPT

ChatGPT can connect to a 1.2.0 appliance's MCP address. This was verified against a test setup, not yet against a live 1.2.0 appliance, and ChatGPT has not been verified through the relay. You do not need developer mode. These menu names are as of November 2026.

1. In ChatGPT on the web (`chatgpt.com`), open **Plugins**.
2. Choose the **+** button, then **Add custom MCP server**.
3. Name it WitFoo and enter your appliance's MCP address.
4. Choose OAuth for authentication, with a client metadata document (CIMD) rather than static credentials. Read the risk warning, choose **I understand and want to continue**, then **Create** as a plugin.
5. Your browser opens your appliance's page, **Connect an app to WitFoo**. Sign in if asked and read what you are agreeing to. Check that the app's name and the host the approval goes to are ChatGPT's own. If not, click **Deny**. Otherwise click **Approve**.
6. Install the plugin. In a chat, type `@` and choose WitFoo.

On a ChatGPT business plan, a workspace administrator may need to allow WitFoo before members can connect it. Before any of this works, an administrator must have added ChatGPT to the client policy's allow list (see [Turn it on](#in-witfoo-administrator)).

## Use a personal key instead

A personal key suits clients that let you set a request header, such as Claude Code, Cursor or Claude Desktop's configuration file. Personal keys work only when your administrator has chosen a mode that includes them.

1. In WitFoo, open the user menu > **Profile**, then the **Security** tab, and find **MCP connections**.
2. Enter a **Key name** and **Expires in (days, 1-365)**, which is 90 unless you change it. Click **Create key**.
3. Under **Copy your key now**, copy it. This is the only time the key is shown.

Treat the key like a password. Send it only in the `X-MCP-Key` header, never in a URL. A key carries all of your WitFoo permissions, with no read-only limit. For a connector the whole organization shares, use the key of a dedicated user who holds only the permissions the connector needs, never an administrator's. The configuration for each client is in [Connecting AI Clients & Marketplaces](../ai/mcp/connect-clients.md), and the key rules are in [Personal MCP Keys](../ai/mcp/personal-keys.md).

## When the assistant wants to change something

Three things decide what an app can do, and the narrowest wins: your WitFoo role, what you approved, and your organization's client policy.

- An approval is read-only unless you turn on **Also let this app make changes for you**, an option that is off by default and lists the tools that make changes. The option appears only when the app asks to make changes and your organization allows it. If your organization allows apps read-only access, the page says so instead.
- If you approved read access and the app later wants to make a change, it asks you to sign in again (Claude shows **Authentication required to use this tool**), and your appliance's page offers the option then.
- Once you allow changes, your appliance does not ask again for each change. The kit's jobs tell your assistant to ask you before every change, and your assistant may show its own prompt as well.
- To take it back, revoke the app under **Profile** > **Security** > **Connected apps** and connect it again without the option.

For an app that signs in through your appliance, nothing changes unless you allowed changes when you approved it. A personal key has no such limit.

!!! note "Reading tasks, notes and playbooks on 1.2.0"
    In 1.2.0, the tools that list a work unit's response tasks, notes and assignments, and the organization's playbooks, are marked as tools that make changes, because the same tools also write. An app approved read-only is refused them (`403 insufficient_scope`), so the assistant cannot read those lists, or suggest a playbook, until you allow changes. See [MCP Tools](../ai/mcp/tools.md).

## If something does not work

The troubleshooting table in [Connecting AI Clients & Marketplaces](../ai/mcp/connect-clients.md#troubleshooting) covers the common answers, and [MCP Errors](../ai/mcp/errors.md) lists every response an MCP client can receive.

---

*Claude is a trademark of Anthropic, PBC. ChatGPT is a trademark of OpenAI. Other product names are trademarks of their owners, used here only to identify the products. No endorsement or partnership is implied.*
