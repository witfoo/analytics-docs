# WFA Deployment

The WitFoo Appliance (WFA) CLI installs, configures and manages WitFoo Analytics on an appliance. The WFA daemon (`wfad`) creates and runs every container for the node's role.

## Installation

Install an Analytics node in four steps:

1. Run the configuration wizard. It writes `/witfoo/configs/node.json` and, for Analytics roles, `/witfoo/configs/analytics.json`:

    ```bash
    sudo wfa configure
    ```

2. Check the host against the role's minimum hardware:

    ```bash
    sudo wfa analytics install
    ```

3. Start the services. The wizard starts `wfad` when it finishes, so run this only if the services are stopped:

    ```bash
    sudo wfa start
    ```

4. List the role's expected services:

    ```bash
    sudo wfa analytics status
    ```

See [WFA Configure Wizard](../getting-started/wfa-configure.md) for every wizard prompt and [WFA CLI Reference](../conductor/wfa-cli.md) for every command.

### Analytics Roles

The wizard offers six roles. Four of them run Analytics:

| Wizard choice | Analytics role | Description |
| --- | --- | --- |
| Analytics AIO + Conductor | `analytics-aio-conductor` | All Analytics and Conductor services on one server |
| Analytics AIO | `analytics-aio` | All Analytics services, without Conductor |
| Analytics Processing Node | `analytics-processing-node` | Every service except Cassandra; connects to external data nodes |
| Analytics Data Node | `analytics-data-node` | Cassandra only, for a clustered deployment |

The other two roles are **Conductor** (signal collection and forwarding) and **Console** (fleet management). The wizard shows only the roles your licensed product allows.

## Configuration

Retention, UI modules and CyberGrid are not set in `wfa configure`. The wizard sets defaults, and you change them in the **Onboarding Wizard** of the Analytics web UI. Clustering (data node addresses, seed nodes) is asked by the wizard for the Processing and Data roles.

The MCP settings in `node.json` (`mcp_http_enabled`, `mcp_exposure_enabled`, `mcp_public_url`, `mcp_oauth_ui_url` and `mcp_oauth_cimd`) are not set by the wizard. Add them to `node.json` by hand, then run `sudo wfa restart`. They need WFA 2.5.1 or later. See [MCP Configuration](../ai/mcp/configuration.md).

## Management Commands

| Command | Description |
| --- | --- |
| `wfa start` | Start the `wfad` service and its containers |
| `wfa stop` | Stop the `wfad` service and all containers |
| `wfa restart` | Restart `wfad`, which stops and starts every container |
| `wfa status` | Show the `wfad` service state and recent errors |
| `wfa version` | Show the installed WFA version |
| `wfa analytics install` | Check the host against the Analytics role's minimum hardware |
| `wfa analytics status` | List the Analytics role's expected services |
| `wfa analytics upgrade --branch <version>` | Check an Analytics upgrade to the given branch or version |

## Current Version

**WFA 2.5.3** is the WFA release that ships with WitFoo Analytics 1.2.0. Install WFA 2.5.1 or later; we recommend 2.5.3. WFA 2.5.0 was published briefly and withdrawn: it reduced the database's memory on many appliances and could stop it under heavy load. 2.5.1 restores it.

Upgrade the Analytics images to 1.2.0 first, then install WFA 2.5.3 soon after. See [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md) for the full order.

WFA 2.5.1 and later change the appliance in these ways:

- **Every container is recreated on the first start.** Ingestion pauses while this happens. On a WitFoo test appliance the gap was 3.5 to about 9 minutes on an AIO + Conductor node and about 5 minutes on an AIO node. Plan the upgrade for a quiet period.
- **New service credentials and session secret.** On the first start, WFA replaces the service credentials and the session secret with random ones, once. This signs every user out.
- **`node.json` is readable by root only** (mode `0600`). A non-root reader you added loses access to it.
- **NATS and the broker edge listen on loopback only.** NATS (4222, 8222) and the broker edge (4223) are published on `127.0.0.1`. A client off the appliance that reached them directly loses access.
- **The api and incident-engine ports are not published.** The api (8080) and incident-engine (8082) are no longer published on the host. Reach them through the reverse proxy.
- **NetFlow port on Conductor roles.** On Conductor and AIO + Conductor appliances, WFA publishes 2055/udp and opens it in the host firewall. The NetFlow and IPFIX listener stays off until you enable it under **Log Servers** in the Conductor UI. See [Log Server Configuration](../conductor/ui/log-servers.md).
- **Memory limits.** The six first-party Analytics containers (artifact-ingestion, graph-processor, incident-engine, api, dispatcher and reverse-proxy) get a hard memory limit sized from the node's memory budget. Cassandra and NATS get no limit. Cassandra keeps its 8 GiB heap; on a host large enough for a bigger heap, WFA sets it through `JVM_EXTRA_OPTS`.
- **Cassandra commit log on `/cassandra_commit`.** On every role that runs Cassandra, the Cassandra container is recreated with its commit log on the host path `/cassandra_commit`. That path is on `/` unless you mount a dedicated disk there. The recreate waits up to 10 minutes for the old container to drain.
- **FIPS Compliance mode is removed.** `wfa configure` no longer asks about it. An appliance that an earlier WFA put in FIPS mode now runs without it, and `wfad` and `wfa` print a warning.
- **`wfa user-reset` fixes.** It now works on appliances whose Analytics database was created by Analytics 1.1.x, re-activates an inactive administrator, and waits up to 60 seconds for the database. See [WFA CLI Reference](../conductor/wfa-cli.md).
- **Staff-requested jobs.** New installs turn off the jobs WitFoo support staff can request on the appliance. An existing appliance keeps its setting. Change it with `wfa staff-jobs status|off|on`.
- **MCP settings in `node.json`.** WFA reads the MCP keys listed under [Configuration](#configuration), and `wfa mcp-relay` turns the AI-connector relay on and off. See [MCP Relay](../ai/mcp/relay.md).
- **Analytics administrator password.** On the first start, if the Analytics administrator (`admin@witfoo.com`) still has the shipped default password, WFA may apply the password from the wizard's Admin Account step. See [WFA Configure Wizard](../getting-started/wfa-configure.md).
- **RHEL.** On RHEL, auto-update forces a metadata refresh, and turning auto-update off removes the units earlier releases wrote. `logrotate.service` reports failed every hour on RHEL nodes because WFA keeps a backup of the rsyslog rotation file in `/etc/logrotate.d`; logs are still rotated.

!!! warning "Re-running `wfa configure` or `wfa fetch` drops `trusted_proxies`"
    A re-run of `wfa configure` or `wfa fetch` (including `wfa configure --license-file`) keeps the MCP settings but writes `node.json` without `trusted_proxies`. Add `trusted_proxies` again after each re-run, then run `sudo wfa restart`.

## Authentication Configuration

WFA deployments support SAML single sign-on configuration through the built-in wizard, available in both conductor-ui and console-ui settings pages. The wizard provides provider presets for Azure AD, Okta, OneLogin, and PingIdentity with automatic SP key pair generation.

For detailed SAML setup instructions, see [Authentication Settings](../admin-guide/settings/authentication.md). For the Conductor UI SAML changes in 1.2.0, see [User Management & Authentication](../conductor/ui/users.md).

## Hardware Validation

The wizard checks RAM and CPU when you choose a role, and `wfa analytics install` checks them again for the Analytics roles. CPU counts are logical CPUs (vCPUs).

| Role | Min RAM | Min CPU | Min Disk |
| --- | --- | --- | --- |
| Analytics AIO + Conductor | 28 GB | 6 | 200 GB |
| Analytics AIO | 20 GB | 4 | 200 GB |
| Analytics Processing Node | 6 GB | 2 | 100 GB |
| Analytics Data Node | 12 GB | 2 | 500 GB |
| Conductor | 8 GB | 2 | — |
| Console | 4 GB | 1 | — |

The disk figures are the role's declared minimum; the install check does not measure disk. If the host is below the minimum, the wizard warns and asks whether to continue.
