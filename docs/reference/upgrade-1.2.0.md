# Upgrading to 1.2.0

WitFoo Analytics 1.2.0 was released on 2026-11-08. It is a minor release; the previous release is 1.1.5. This page lists what to do before and after you upgrade, what changes without any action, and the known limitations of 1.2.0.

The full release notes are on GitHub: [WitFoo Analytics 1.2.0](https://github.com/witfoo/release-notes/blob/main/releases/1.2.0.md). A summary is in the [Changelog](changelog.md).

Read the section for your deployment first:

- [WFA-managed appliances](#wfa-managed-appliances)
- [Docker Compose and standalone stacks](#docker-compose-and-standalone-stacks)

Then read the sections that apply to you.

## WFA-managed appliances

### Upgrade order

1. Update the analytics images to **1.2.0**.
2. Install **WFA 2.5.4** (the current release; 2.5.3 shipped with 1.2.0) soon after. If WFA automatic updates are off, note that WFA 2.5.3 is published before the 1.2.0 images: update the images first anyway.
3. Once the images are 1.2.0, run `wfa restart` once. An image update does not restart wfad, and WFA replaces the key that seals stored secrets only at a wfad start whose analytics images are 1.2.0.

- **WFA owns the encryption key.** Do not edit `AUTH_CONFIG_ENCRYPTION_KEY` by hand on an appliance. WFA 2.5.1 and later keep the old key until the images are 1.2.0, then replace it with a random key, so the order of the image and WFA updates does not affect stored secrets.
- **Why install WFA soon after the images.** Until WFA 2.5.1 or later runs, the broker holds about 30 KB of publish ids in memory for each artifact per second of ingest.
- **WFA 2.5.0 was withdrawn.** It reduced the database's memory on many appliances and could stop it under heavy load. WFA 2.5.1 restores it. Install WFA 2.5.4.

### Plan a quiet period

The first start of WFA 2.5.1 or later recreates every container, so ingestion pauses while it does. On a WitFoo test appliance the gap was between 3.5 and about 9 minutes on an AIO plus Conductor node, and about 5 minutes on an AIO node. Plan the WFA upgrade for a quiet period.

If your appliance already installed WFA 2.5.0, 2.5.1 or 2.5.2 (for example by automatic update), the one-time changes of the first start already happened and are not repeated. The upgrade to WFA 2.5.3 still restarts every container once.

### The administrator password (`admin@witfoo.com`)

WFA 2.5.1 and later may change the Analytics web UI administrator's password, on their first start, if that administrator still has the shipped default password:

- When the password file from the **Admin Account** step of `wfa configure` is still on the node, WFA sets it as the administrator's password and signs the administrator's current sessions out.
- When the file is gone, WFA leaves the password as it is and logs a warning that names `wfa user-reset`.

A password anyone has already set, in the web UI or with `wfa user-reset`, is never changed. This can take up to an hour while the database starts.

Before you upgrade:

- Make sure you know the password last entered at `wfa configure`.
- Update any script or integration that signs in as `admin@witfoo.com` with the default password.

If you cannot sign in after the upgrade, run `wfa user-reset` on the node.

### Other changes WFA 2.5.1 and later make

- **Everyone is signed out.** Each appliance gets random service credentials and a random session secret, once, at the first start. This ends every signed-in session.
- **node.json is root-only.** It becomes mode `0600`, so a non-root reader you added loses access.
- **Ports on loopback.** NATS (4222, 8222) and the broker edge (4223) are published on the appliance's loopback address only. The api (8080) and incident-engine (8082) are no longer published on the host.
- **NetFlow and IPFIX.** On Conductor and AIO-Conductor appliances, WFA publishes port 2055/udp and opens it in the host firewall. The listener stays off until you enable it under **Log Servers** in the Conductor UI. Under WFA 2.4.x, 2055/udp is not published.
- **Memory limits.** The six first-party analytics containers (artifact-ingestion, graph-processor, incident-engine, api, dispatcher, reverse-proxy) get a hard memory limit sized from the node's memory budget. Cassandra and NATS get none. WFA sets the Cassandra heap through `JVM_EXTRA_OPTS`.
- **Cassandra commit log.** On every role that runs Cassandra (all-in-one, all-in-one with Conductor, Data, Reporter), the Cassandra container is recreated with its commit log on the host path `/cassandra_commit`. That path is on `/` unless a dedicated disk is mounted there. The recreate waits up to 10 minutes for the old container to drain.
- **FIPS Compliance mode is removed.** `wfa configure` no longer asks about it, and `wfa fetch` and the Console's remote configuration refuse a configuration that turns it on. An appliance that WFA 2.4.14 to 2.4.16 put in FIPS mode now runs without it, with a warning.
- **`wfa user-reset` fixes.** It works on databases created by Analytics 1.1.x and re-activates an inactive administrator. If an administrator could not sign in after `wfa user-reset` was run on a FIPS host under WFA 2.4.14 to 2.4.16, run `wfa user-reset` again once the appliance runs WFA 2.5.1 or later and the 1.2.0 images.
- **Staff-requested jobs.** New installs turn them off by default; an existing appliance is not changed. `wfa staff-jobs status|off|on` changes the setting.
- **The wizard's administrator-password file.** WFA 2.5.3 makes it owner-only, and removes it once the administrator's password is no longer the seeded default.
- **Re-running `wfa configure` or `wfa fetch`** keeps the MCP settings (`mcp_http_enabled`, `mcp_exposure_enabled`, `mcp_public_url`, `mcp_oauth_ui_url`, `mcp_oauth_cimd` and the relay's `mcp_relay_` fields). It does **not** keep `trusted_proxies` or other settings no prompt asks for: set them again after a re-run, then run `wfa restart`.
- **Reboot Now** in the web UI reaches the appliance agent once the incident-engine container is recreated with the 1.2.0 image under WFA 2.5.1 or later.

See [WFA deployment](../deployment/wfa.md) and the [WFA CLI](../conductor/wfa-cli.md).

## Docker Compose and standalone stacks

### Set the key that seals stored secrets

`AUTH_CONFIG_ENCRYPTION_KEY` is now **required**. It seals LDAP and SAML secrets, TLS keys, AI-provider keys, notification-channel configurations, audit-connector credentials and Vrax connection credentials.

- The compose files no longer carry a default for it. Every `docker compose` command refuses to run until it is set.
- The services refuse to start with a value that is not 32 bytes of base64, or with the value earlier compose files used to ship.
- Generate a key with `openssl rand -base64 32` and put it in the root `.env`. If you start your stack with the provided launch scripts, they generate one and write it to `.env` when none is set.
- `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` lists the key or keys the current one replaced (comma-separated), so data sealed under them stays readable.
- **More than one node:** every node that runs the api or incident-engine against the same Cassandra cluster needs the same `AUTH_CONFIG_ENCRYPTION_KEY` and the same `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS`. Copy both from the first node's `.env` before a second node's first start: a node that generated its own key cannot open what the first one sealed.
- **The key is part of your data.** Back it up whenever you back up the database, and store the two apart.

A stack that has stored nothing sealed (no LDAP or SAML settings, TLS key, AI provider, notification channel, audit connector or Vrax connection was ever saved) has nothing to convert and only needs the new key.

### A stack that never set the key

Earlier compose files shipped one default key for every installation, a public value that protects nothing. A stack started from one of them that never set a key of its own holds its stored secrets sealed under that default. To move it:

1. **Back up** the database first.
2. Update the checkout to 1.2.0. Do not start anything yet.
3. In the root `.env`, set two variables:
    - `AUTH_CONFIG_ENCRYPTION_KEY` to a new key, the output of `openssl rand -base64 32`.
    - `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` to the value earlier compose files shipped.

    You do not need to look the old value up. When the launch script generates the new key, it explains what that means for a stack that already holds data, and prints the one command that adds `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` with that value to your `.env`. Run that command before the services start. The compose files' own error message names the value too.

4. Start everything with **one** `docker compose up -d`, so the images, the new key and the previous key change together.

If a stack starts with a new key and without the previous key, its stored secrets cannot be opened until you add `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` and recreate the api and incident-engine services. A restart is not enough: `docker restart` and `docker compose restart` keep the environment the container was created with, while `docker compose up -d` recreates a container whose environment changed.

### Check that it worked

Read incident-engine's log:

```bash
docker logs witfoo-analytics-incident-engine 2>&1 | grep -E 'SecretsStartupCheck|SecretsRekeyService'
```

- About 30 seconds after incident-engine starts, a start-up check reads every stored secret once and logs one line. `SecretsStartupCheck: every stored secret opens with the configured keys ...` means all is well. `SecretsStartupCheck: N of M stored secret(s) cannot be opened with the current master key ...` names the families it cannot open: set `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` to the key they were sealed under and recreate the api and incident-engine.
- While a previous key is set, incident-engine converts what is still under an older key. The first pass runs 10 minutes after the service starts, then every 6 hours. Each pass logs a `SecretsRekeyService <family>: ...` line per family.
- After two passes in a row that change nothing, incident-engine logs `SecretsRekeyService converged: ...`. Remove `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` the next time you recreate the services. The earliest this can appear is about 6 hours and 10 minutes after the services start.

If the old key is lost, the values sealed under it cannot be recovered: enter them again (the LDAP password, the SAML key, the TLS key, the provider keys, the notification channels, the connector credentials and the Vrax credentials). The conversion includes the saved Vrax credentials.

**Rolling back.** Once a conversion pass has run, the stored values are under the new key, and an earlier release cannot read them. Before you roll back, plan to enter those secrets again, or restore a backup taken before the upgrade.

### Published ports

- `INTERNAL_LISTEN_IP` (default `127.0.0.1`) now publishes NATS, the api, incident-engine, the dispatcher, the UI, Prometheus and Grafana, instead of `LISTEN_IP`.
- `LISTEN_IP` still publishes Cassandra, the artifact receiver and the reverse proxy. **Restrict Cassandra's ports (9042, 9160) at the host firewall.**
- The compose files do not publish 2055/udp for NetFlow and IPFIX. To use the listener, add `2055:2055/udp` to the signal server's ports.

See [Configuration](../deployment/configuration.md) and the [Docker Compose Reference](../deployment/docker-compose.md).

### SECRET_KEY for Conductor UI and Console UI

Conductor UI and Console UI refuse to start when `SECRET_KEY` holds the value earlier releases carried, the value the Console's example deployment files showed, or a value that is not a usable key. Before you upgrade, either:

- unset `SECRET_KEY`, so each program keeps a key of its own in `.secret_key` beside its database, or
- set it to a new value of 64 hexadecimal characters, for example the output of `openssl rand -hex 32`.

Keep `.secret_key` with the database: a program that finds its database without the file generates a new key, which ends every session.

## Separate Conductor nodes

Upgrade every Conductor, including separate or remote Conductor nodes, to the 1.2.0 images at the same time as analytics or before it. All-in-one appliances upgrade both together.

- A Conductor from an earlier release sending to 1.2.0 analytics keeps only about one record per page or poll for Azure Security, Microsoft Sentinel, Cisco AMP, Cisco Umbrella, Cisco Meraki, Splunk and Stealthwatch, and the batch is still answered as accepted.
- Earlier Conductors also send batches with no size bound, which a receiver on the small body profile (appliances with less than about 18.5 GiB of host memory) can refuse with `413`.

## Ports, load balancers and the edge

- **Trusted proxies.** With `WF_TRUSTED_PROXIES` unset, a TLS edge no longer believes any forwarder's `X-Forwarded-For`. An edge behind a load balancer (LB mode, or TLS disabled) keeps the old private-network list for one more release, with a startup WARN.
- **Declare your load balancer now:** `WF_TRUSTED_PROXIES` on Docker Compose, or `trusted_proxies` in `node.json` on a WFA appliance (WFA 2.5.1 or later). Re-running `wfa configure` or `wfa fetch` (including `wfa configure --license-file`) writes `node.json` without `trusted_proxies`: add it again after each re-run, then run `wfa restart`.
- **`X-Real-IP` is not read.** A load balancer that sends only `X-Real-IP` is keyed on its own address at the edge.
- **Before you enable the MCP exposure listener** behind a load balancer, declare the load balancer. Until it is declared, every client behind it shares one failed-authentication count on `/mcp`.

## Single sign-on and hand-typed Conductor addresses

- **Conductor UI SAML.** SAML sign-in now signs in only accounts whose Auth Source is **SAML (SSO)**. An account whose Auth Source is Local or LDAP is refused, and in SAML SSO mode the server refuses every local sign-in, so such an account cannot sign in at all, a local administrator included. Before you upgrade a Conductor node that serves its own sign-in page with Authentication Mode SAML SSO, convert those accounts. This does not apply on an all-in-one node, where Analytics signs users in. The steps, including the way back for a node that was upgraded first, are in [Conductor UI users](../conductor/ui/users.md).
- **Console UI SAML.** SAML sign-in now signs in only accounts whose auth mode is SAML. A SAML sign-in whose username matches no account creates one, with the Staff role and no organization: review new accounts on the Users page and assign them an organization.
- **Platform administrators and your SSO.** Platform administrators no longer sign in through an organization's SAML SSO or LDAP directory by default. To let your own organization's SSO sign them in, write that organization's ID to `/witfoo/configs/operator-identity-org` on the node that runs `analytics-api-svc` (owner root, mode `0644`) and restart `analytics-api-svc`. Only one organization can be named. LDAP sign-in of these accounts works only when the organization ID equals the first part of the account's mail domain. See [Authentication](../admin-guide/settings/authentication.md).
- **The `/ingestion/` path is removed.** The reverse proxy no longer serves it. Conductors send to the analytics host directly by default, so nothing changes for them. A Conductor whose artifact endpoint was typed by hand with an `/ingestion/` prefix now gets `404`: point it at `https://<analytics-host>:8443/v1/conductor/artifacts/batch`.
- **IPv6-only Cassandra.** An IPv6-only analytics Cassandra container now refuses to start (exit 2, "container IP is empty or malformed"). Give its IPv6 address in `CASSANDRA_BROADCAST_RPC_ADDRESS`.

## Public self-registration

If you allow public self-registration (`AUTH_PUBLIC_REGISTRATION_ENABLED`), set `AUTH_PUBLIC_REGISTRATION_DOMAINS` to comma-separated `domain=organization` pairs. Without it, registration creates no account.

- The organization a registration request names is ignored; the email domain chooses it.
- Domains are matched exactly, with no wildcard. One malformed entry rejects the whole map until it is fixed.
- Accounts are created **inactive**: an administrator must enable each one (**User Management**, **Enable**) before the person can sign in.

## MCP clients

- **Upgrade incident-engine and the dispatcher together**, or incident-engine first. If they run different versions, most MCP tool calls fail with an "unexpected status 401" error.
- **MCP is off by default.** Personal keys and app sign-in stay off until an administrator chooses them under **AI Setup** > **MCP Authentication**, and HTTP `/mcp` is not served until the operator turns on the HTTP transport (`mcp_http_enabled` in `node.json`, or `WF_MCP_HTTP_ENABLED` on Docker Compose). Browser chat sessions work in every mode. See [MCP Configuration](../ai/mcp/configuration.md).
- **Connect MCP is a new permission.** A user needs `mcp:connect` to connect an MCP client. Admin and Platform Admin hold it through `admin`, and any role with `mcp:manage` holds it; grant it to anyone else through a custom role.
- **Org-wide keys are retired.** Org-wide MCP keys (`wfmcp_…`) no longer authenticate, and issuing one returns `410`. They stay listed as **Org-wide (retired)**; clean them up with **Revoke all legacy keys** under **AI Setup** > **MCP Authentication**. Users create personal keys instead. See [Personal MCP keys](../ai/mcp/personal-keys.md).
- **Revoke retired keys before a downgrade.** The upgrade does not revoke them, and a 1.1.x build accepts them again.
- **Downgrading** below 1.2.0 disables every personal key. Secret scanners that match `^wfmcp_` do not match the new `wfmcpu_` keys.
- **Browser sessions on `/ws/chat`** now need a token with `aud` and `exp` claims and a user who holds `mcp:connect`. Older tokens are refused.
- **MCP is a licensed feature.** It is included with Analytics Pro, Analytics Max and Reporter Pro. On Analytics Lite or Reporter Lite a connection is refused. See [MCP licensing](../ai/mcp/licensing.md).

## Custom roles

- **Setup wizard steps.** The AI, DNS, frameworks and CyberGrid steps now need **Manage AI** (`ai:manage`), **Manage Signals** (`signals:manage`), **Write Frameworks** (`frameworks:write`) and **Manage CyberGrid** (`cybergrid:manage`) respectively, each together with `settings:manage`. The built-in Admin and Platform Admin roles are unaffected. A user with the Admin role adds the permission in **Role Management**, and the affected user signs in again.
- **Dashboards.** Creating, updating, deleting and cloning a dashboard now need `dashboards:write`. Marking a favorite still needs only `dashboards:read`.
- **Dashboard widgets.** A widget shows its data only to a user who may read that data elsewhere. A custom role that can read dashboards but not a widget's data source now sees "You do not have access to this widget's data." on that widget.
- **The in-app AI assistant** needs **Read AI** (`ai:read`) and **Write AI** (`ai:write`). Every built-in role has both, and every custom role that exists at the upgrade receives both once.
- **Classification rules, enrichment settings, compliance frameworks and CyberGrid** now check permissions on every request. See [Admin Guide: Roles](../admin-guide/roles.md).
- **User Management and Role Management** open only for the Administrator (`admin`) permission.

**When role changes apply.** A permission change reaches a user at their next sign-in (or when an API client refreshes its token), and the server may reuse a decision for up to 5 minutes after that. MCP connections read a user's roles on every request. A session that began before a role gained a permission does not carry it: the user signs in again.

## Changes that need no action

These change on upgrade without any action on your part:

| Change | Who is affected |
| --- | --- |
| Everyone is signed out once and signs in again (the session key changes; on a WFA appliance the first start of WFA 2.5.1 or later also replaces the session secret and service credentials once) | every user |
| Disabling a user, or suspending or deleting a tenant, refuses the user's sessions within seconds (requests) or a minute (open streams). Resetting or changing a password ends the user's sessions and stops their personal MCP keys working | every user |
| In User Management, **Delete** is now **Disable**, and a disabled user can be enabled again. There is no permanent delete. An administrator cannot disable their own account | anyone who administers users |
| An address typed for an account must be one plain address | registration, administrator create or update, first-administrator setup, tenant provisioning |
| Requests that switch one setting must state its value: the routes that turn a single thing on or off answer `400` when the body does not state it. Send `{"enabled": false}`; the Console organization update needs `is_active`, the Conductor appliance-configuration update needs `enabled` on every element, and the licensing administrator-flag update needs `is_admin` | scripts and integrations that sent an empty body to mean off |
| `PUT /api/v1/settings/business` changes only the keys the body carries; a key left out keeps its stored value | scripts that send a partial body |
| Artifact reads answer `500` when the artifact store cannot be read (1.1.5 answered `200` with an empty result), `499` when the client has gone away and `503` past the deadline. The incident routes answer `400` with code `invalid_parameter` for a malformed parameter, id or body, or a negative limit or offset | API clients and monitoring |
| The default platform user (`admin@witfoo.com`) is created only when the users table is empty. A database restart leaves existing users as they are | operators who delete or change the default platform user, or recover a lock-out by restarting the database container |
| Confirmation dialogs with a red confirm button (Delete, Disable, Remove, Reset, Reboot Now and similar) do not submit on Enter, in Analytics and the Console UI | people who confirm from the keyboard |
| The Compliance page's NIST CSF function rows change: mappings kept under the v1.1 key were credited one function too early, and now appear under the matching v2.0 function | customers upgrading from a release before 1.1.5 |
| The Work Units search offers only fields the list can answer. The Edges, Edge Type, Edge Label, Stream Name, Message, Artifact Severity, Server IP and Action fields and the "Filter by Alarm Rule..." dropdown are removed; a saved search or link that names one lists work units without that filter and shows a notice | analysts with saved searches or bookmarks |
| MCP: `get_executive_summary` refuses `start_date` and `end_date` | clients that send them |
| MCP is a licensed feature | organizations on Analytics Lite or Reporter Lite |
| The region of a Rapid7 InsightIDR, AWS GuardDuty, AWS Security Hub, AWS audit or OCI audit integration must be a region name only (letters, digits and hyphens). Check these region fields after the upgrade | users of those integrations |
| SAML and LDAP settings are saved and read only on the authentication settings page; `PUT /api/v1/settings` neither saves nor returns them | scripts that set SSO through the general settings API |
| `NOTIFICATION_ENCRYPTION_KEY` is removed, with its startup warning. Rule-driven notifications that never delivered start delivering | everyone using notification rules |
| The services create the ten new tables this release adds when they first start; there is no manual migration step | everyone |
| The Console runs one new migration step (0008, an index on the node status history) when it first starts | Console operators |
| Conductor UI and Console UI end every browser session once, because the session key changes (unless `SECRET_KEY` was already set to a key of your own). In the Console, a deployment configuration generated before the upgrade and not yet fetched can no longer be fetched: delete it and generate it again | Conductor UI and Console UI users |
| Health > Containers is empty for the first collection cycle (about 15 seconds), and containers removed before the upgrade are no longer listed | everyone |
| An appliance whose Cassandra serves no clients holds the dependent services at start-up (up to 20 minutes per attempt) | WFA appliances (with WFA 2.5.1 or later) and Compose stacks |
| On its first start, the analytics Cassandra container stops with a FATAL log line when its seed data does not apply completely | everyone |
| When the licence check fails, the system status reads "the licence check failed; the incident-engine log has the detail" | everyone |

### Artifact receiver capacity

- **Body profiles.** The receiver has two body profiles: the default (body 64 MiB, in-flight budget 256 MiB) and the small profile (body 32 MiB, budget 128 MiB, 1,024 stream connections). `WF_INGEST_PROFILE` chooses it; when that is unset, a memory budget (`WF_MEMORY_BUDGET_MB`) below 768 MiB runs the small profile. An appliance with less than about 18.5 GiB of host memory runs it.
- **Connection limits.** Each listener holds a number of connections set from its memory budget, and one source at most a share of them (128 plain and TLS). Settings: `WF_CONN_MAX`, `WF_CONN_MAX_TLS`, `WF_CONN_MAX_PER_SOURCE` and `WF_CONN_TRUSTED`.
- **Many Conductors behind one address.** Where more than about 40 to 60 Conductors reach the receiver from one address (a NAT or a load balancer) or one IPv6 /64, they share 128 connections. A deployment that sets the receiver's environment can list that address in `WF_CONN_TRUSTED`. A WFA appliance has no setting for the `WF_CONN_` variables in 1.2.0, so give those Conductors more than one address, or more than one receiver. Refused connections are retried by the exporter: nothing is lost, but throughput drops.
- **Message limit.** The largest artifact the receiver takes is 9.5 MiB. A batch of more than 1,000 artifacts is refused with `400`, and a request line and headers over 12,288 bytes with `431`. The TLS port speaks HTTP/1.1 only.

## Release integrity

Image signing and SBOM attestation sign only a validated digest. For the appliance images they are advisory: a build whose digest cannot be validated skips signing with a warning. Signatures are keyless. Verify them with `cosign verify` against the OIDC issuer `https://token.actions.githubusercontent.com` and a certificate identity naming WitFoo's build workflow, `https://github.com/witfoo-dev/analytics/.github/workflows/build-and-push.yml@` followed by the branch the image was built on:

```bash
cosign verify \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp '^https://github\.com/witfoo-dev/analytics/\.github/workflows/build-and-push\.yml@' \
  <image>@<digest>
```

Registry clean-up may remove signature and attestation tags on its own schedule. From 1.2.0, the version and `latest` image tags carry exactly the digest of the build they name, so signatures attached by digest follow them. Earlier version tags keep the digest they were published with.

## Known limitations in 1.2.0

### Signal Search

- In Signal Search, Escape does not close the Signal Details window when its field search has focus. Use the close button.
- On WFA appliances and the Compose bundle, a Signal Search that takes longer than about 17 seconds fails with an error. A long time range with few or no matches can take that long: narrow the time range or add a filter.
- A search with a filter the server applies row by row (contains, not-equal, a comparison, a Client IP or Server IP match on an IPv6 address, the Location filter or a word) reads a bounded number of the newest events in the range. If that is spent before the page is full, the search stops and says so, so a rare match in a long time range can be missing.
- A search by offset returns at most its first 10,000 results. A request whose offset plus limit is more than 10,000 is refused, and the page shows "The search was not accepted as typed". Narrow the time range or add a filter to reach older events.
- Typing `ip=`, `port=` or `hostname=` searches both sides at once: an event matches only when its client side and its server side both have that value. To match one side, use `client_ip=`, `server_ip=`, `client_port=`, `server_port=`, `client_hostname=` or `server_hostname=`.
- On the artifact search API (not the Signal Search page), on the timeline and the facet counts, the `client_ip` and `server_ip` parameters apply an IPv6 address but not an IPv4 address. To apply an IPv4 address, send the same condition in the `filters` parameter, for example `filters=[{"field":"client_ip","operator":"=","value":"10.9.9.9"}]`.
- For time ranges longer than six hours, a first or last hour that holds more than 50,000 events is counted whole by the timeline, including events outside the range. The filtered facet counts read each hour up to 100,000 events; an hour that reaches 100,000 makes the counts estimates.
- On a busy appliance, the timeline can show only part of the window or no bars at all, and it says the result is incomplete.
- When a Conductor's clock runs more than 30 days ahead, a Signal Search that gives both a start and an end time (and no message type, stream or action filter) can leave that Conductor's events out of the results list, while the timeline, the facet counts and the statistics still count them.
- `GET /api/v1/artifacts/stats` can answer `503` "Search timed out" on appliances with many artifacts. A repeated request usually completes, sometimes with empty breakdowns.
- Node Search's Node Type, Trusted and Internal counts reflect the loaded page of results (up to 200 nodes), not the whole result set.
- Node Search does not show the Compliance Frameworks section. The section has not appeared since 1.1.0.

### Work Units

- On some appliances, the incident engine generates leads but creates no work units for the traffic it sees.
- A node, ATT&CK technique or Client IP filter on Work Units lists only that item's newest work units, up to the page size, and the total counts only those.
- A work unit can outlive its edge records: its Edges section can read "Edges (0)" above a table of edges, and an edge's detail can open empty.
- A work unit that is still being updated after its 365th day keeps its title and status and loses its name, creation time and part numbers.
- Holding the Escape key down on the replay closes an open detail window and then leaves the replay. Press Escape once for each window.

### Dashboards and reports

- Dashboard widgets whose data source is Work Units show no data: a counter reads 0, and a chart or a table is empty, although the Work Units page holds and shows the data. Widgets whose data source is Nodes or Edges show their data.
- Dashboard widgets that count artifacts (signals), including the SOC Overview "Artifacts Today" and "Artifacts by Source" tiles, show "Not available yet" instead of a count. The artifacts themselves are stored and searchable in Signal Search as usual.
- A widget on the Artifacts source set to a fixed time range wider than your organization's search window (30 days unless **Retention → Search** is set), or to a range that ends before it starts, shows an error. Narrow its range to clear it. A relative range is shortened to the search window instead.
- On the Operational Health dashboard, the Error Rate Trend widget shows its empty state and the Error Count (24h) widget reads 0.
- The Compliance page's totals count every framework, whichever framework you select.
- The Compliance score tooltip still says scores are "based on node framework membership".
- After an appliance restart, the first scheduled report delivery can leave out the Audit and Threat Model reports. The next scheduled delivery includes them.
- On-demand report generation for an organization created after the appliance started answers `409` until the appliance's services restart.
- The Auditor Findings tab shows a refused read as "no findings" instead of saying you are not allowed to read it.

### Playbooks and responders

- A playbook run shows each step's result while it runs, but the results are not kept afterwards.
- A playbook with an incomplete or invalid step saves, and the problem appears only when the playbook runs.
- A playbook or responder detail page you are not allowed to read shows the refusal beside an editable form; saving from it is refused.

### MCP and the AI-connector relay

- **The MCP Server Settings card saves controls that do not decide who is admitted.** **AI Setup** > **MCP Server Settings** saves MCP Server Enabled, Allowed Origins and Max Concurrent Connections without changing which clients are admitted. Rate Limit (requests/min) applies only to apps that use app sign-in. "Who can connect over MCP" under **AI Setup** > **MCP Authentication** decides who is admitted, and `WF_ALLOWED_ORIGINS` sets browser origins.
- **App sign-in has limits:** no registration by the app itself, no custom-scheme return address, no client secrets, only the authorization-code flow with PKCE (refresh tokens renew it), no binding of tokens to a client key, and an access token works at `/mcp` only.
- **A contested relay address shows as "Status unavailable".** If another party presented this appliance's relay credential while its tunnel was up, the AI Setup card shows "Status unavailable" and `wfa mcp-relay status` shows "contested". Revoke the address (`wfa mcp-relay off`), enable the relay again (`wfa mcp-relay enable`), run `wfa restart`, give your MCP clients the new address and rotate the personal keys they held.
- **A relay address that cannot be revoked from the appliance.** If `node.json` holds only one of the relay's handle and credential, for example after a re-run of `wfa configure` or `wfa fetch` could not read the other, `wfa mcp-relay off` stops the relay, says the address is not revoked and exits non-zero, and `enable` refuses. Copy the missing value back from the `node.json.unreadable-<time>.bak` copy and run `off` again, or ask WitFoo support (`support@witfoo.com`) to revoke the address. Once support confirms, remove the remaining relay fields from `node.json` by hand before you enable again: `mcp_relay_handle` or `mcp_relay_credential`, `mcp_relay_enabled`, `mcp_relay_ack` and `mcp_relay_revoke_pending`, plus `mcp_public_url` if it holds the old relay address.
- **Plain-text refusals through the relay.** A refusal the MCP server writes as plain text (an unsupported content type, a malformed request, or a method it does not serve) reaches a relayed client as a status code without its text. Clients should read the status.

See [AI-connector relay](../ai/mcp/relay.md).

### Users and sign-in

- Console UI SAML sign-in signs in SAML accounts only, and creates an account for a username it does not know (Staff role, no organization).

### Vrax threat intelligence

- An appliance that cannot reach `app.vrax.io` keeps what it stored and shows the status; nothing is fetched until the next check. Allow outbound HTTPS to `app.vrax.io` if you use the Vrax import.
- The login connection and the feed connection store their data separately. Each organization has one of each, and a refusal on one does not stop the other.
- The Vrax import does not use an environment proxy, so an appliance that reaches the internet only through a proxy cannot use it.
- Vrax answers every authentication failure of its reports API with the same page, so a refused login cannot be told from a wrong industry, region or plan. A refusal stops the automatic schedule until the login, industry or region is saved again (**Run now** still tries once), so a wrong login is not retried on its own.

See [Vrax threat intelligence](../user-guide/signals/vrax.md).

### Conductor and flow connectors

- An OCI flow that lasts longer than the connector's four-minute guard is never read.
- One failed hand-off of the GCP flow-log connector's output to the pipeline pauses its pulls for ten minutes.
- When the NetFlow collector's flow-state store is full, a restart can read stale flow baselines.
- Syslog export is UDP only.
- An artifact whose id is replaced on receipt gets a new id each time it is received, so a resend that arrives after the receiver's one-minute duplicate window is stored twice.
- Where many Conductors share one address, an exporter whose `batch_size` is raised to 1000 with artifacts of 16 KiB or more can be slowed. The default batch size is not affected. Where you set the receiver's environment, list the senders' address in `WF_CONN_TRUSTED`; on a WFA appliance, keep `batch_size` at its default.
- Every Conductor exporter request has 15 seconds to complete, including the upload, so a flush near the exporter's 16 MiB bound needs an uplink of about 9 Mbit/s for that Conductor alone. At the default batch size of 100 artifacts this does not arise.
- When a connector cannot decode the settings an operator supplied, its health code is `decode_error` and the Conductor UI explains it as a provider response that could not be decoded, although no provider was contacted. The connector's own message, in the detail, names the settings.
- The Conductor dashboard's Container Status tab shows each container's run state only; a container whose health check is failing still reads Running there.
- A configuration pushed from the Console while only the node's Conductor UI is connected (and not its appliance helper) is marked sent, although nothing applied it.
- A node holds up to four Console connections; a fifth closes the oldest.
- A data node does not register with the Console and does not appear in its node list.
- On Console and Conductor nodes, the Console database and the TLS server and client keys are readable by local accounts on the appliance, and the UI session key is briefly readable when WFA starts. Limit shell access on appliances to administrators.

### Health and operations

- A running container that Docker marks unhealthy now counts as a down service: the Console shows its node as Error and a critical cluster problem report is raised. A container that was already unhealthy before the upgrade starts alerting once you upgrade (on WFA appliances, with WFA 2.5.1 or later).
- An exited or stopped container is not counted as a down service; only a running container that fails its health check is.
- On an appliance that is short of CPU, the Cassandra health check can time out for several minutes in a row. Cassandra then reads unhealthy and a problem report is raised, but nothing restarts it.
- The artifact-loss alarm is not shown in the page-top banner or in WFA's cluster problem report. The graph processor's health, its log, its metrics and the Health page show it.
- Health → Containers leaves the Container Name and Uptime columns blank. Container state, health, CPU, memory and restarts are shown.
- When Cassandra answers the graph processor's health probe but a single artifact write times out, the artifact is logged and acknowledged, and may not be stored. A Cassandra fault that keeps failing the probe holds ingest until the probe passes or the graph processor stops.
- A dispatcher event consumer left waiting ahead of its stream is repaired only when the dispatcher starts: restart the dispatcher to repair it. Events published while it was stuck are not replayed.
- The first disruption check after a restart reads every active incident of the past year in full (about 11 minutes at 100,000 incidents, measured on a test system). Later checks leave settled incidents alone.
- **Compose bundle:** `./wf up` can wait out its timeout and exit with an error on a node that lost artifacts in the last hour, because the graph processor reports unhealthy until the loss alarm clears; the stack itself keeps running.
- On RHEL nodes, `logrotate.service` reports failed every hour because WFA keeps its backup of the rsyslog rotation file in `/etc/logrotate.d`. Logs are still rotated.
- Under sustained NetFlow load on a test appliance running a pre-release 1.2.0 build, incident-engine on one Analytics all-in-one node grew its reserved heap by about 1.4 MiB an hour; no service restarted or ran out of memory.

### Capacity and platform

- One Analytics Processing node per organization and Data cluster is supported.
- The leads table keeps each organization's leads in one storage partition, so a very large lead history in one organization can slow lead reads.
- The retention period you set is not checked against the free disk space, and the two text-search indexes on artifacts take about four times the space of the artifact data itself. Plan disk for that when you raise retention.
- On a busy appliance, the 95th-percentile read time can exceed the 500 ms objective; listing graph nodes takes 0.5 to 1 s on appliance hardware.
- A chat session still in use after its 90th day can show as a blank entry in the session list, with its title and creation time gone.
- At desktop widths between 1056 and 1239 pixels, the header's actions can run past the right edge for an Admin.
- Stopping the demo-data container logs a segmentation fault; it has no effect on your data.
