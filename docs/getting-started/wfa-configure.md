# WFA Configure Wizard

The `sudo wfa configure` command launches an interactive wizard that configures a WitFoo Appliance for its intended role. This page documents every step of the wizard in WFA 2.5.3, the WFA release that ships with WitFoo Analytics 1.2.0, including the prompts, options, and role-specific differences.

## Overview

The wizard generates the configuration file `/witfoo/configs/node.json`, which the WFA daemon uses to determine which services to run and how to configure them. For Analytics roles it also writes `/witfoo/configs/analytics.json`. Run the wizard as root:

```bash
sudo wfa configure
```

The wizard writes `node.json` with mode `0600`, readable by root only. Press **Ctrl+C** at any time to cancel.

!!! note "Retention, UI modules and CyberGrid"
    The wizard no longer asks for data retention, UI modules or CyberGrid. It sets defaults, and you change them in the **Onboarding Wizard** of the Analytics web UI. See [First Login](first-login.md).

## Step Applicability by Role

Not every step applies to every role. Use this table as a quick reference:

| Step | Conductor | Console | Analytics |
|------|:---------:|:-------:|:---------:|
| 1. License Configuration | ✅ | ✅ | ✅ |
| 1b. Product Selection | ✅ | ✅ | ✅ |
| 2. Node Role Selection | ✅ | ✅ | ✅ |
| 3. Appliance ID | ✅ | ✅ | ✅ |
| 4. Network Configuration | ✅ | ✅ | ✅ |
| 5. Certificate Configuration | ✅ | ✅ | ✅ |
| 6. Web UI Port & Protocol | ✅ | ✅ | ✅ (not on a Data Node) |
| 7. Admin Account | ✅ | ✅ | ✅ |
| 8. Optional Features | ✅ | ✅ | ✅ |
| 9. Staff-Requested Jobs | ✅ | ✅ | ✅ |
| 10. Remote Console URL | ✅ | — | ✅ |
| 11. Analytics Endpoint | ✅ | — | — |
| 12. Clustering Configuration | — | — | Processing and Data Nodes |
| 13. Review and Save | ✅ | ✅ | ✅ |

The broker ports (client port 4223, leaf port 4443, maximum data 1024 MB) and the container registry are set automatically. The wizard does not ask for them.

## Step 1: License Configuration

A WitFoo license is required to pull container images and activate services. The organization ID and organization name are assigned from the license; the wizard does not ask for them.

**Cloud deployments** (AWS, Azure, Google Cloud marketplace instances): the wizard detects the cloud deployment and fetches the license automatically.

**On-premises deployments:**

```text
  1. I have a license key — enter it manually
  2. Request a 15-day trial — free, no credit card required

Select option (1-2):
```

**Option 1 — Enter license key.** License keys are UUID-formatted strings provided by WitFoo:

```text
Enter your license key: 00000000-0000-0000-0000-000000000000
  Verifying license with WitFoo licensing service...
  ✓ License verified and configured
```

**Option 2 — Request 15-day trial.** Accept the WitFoo End User License Agreement, then enter:

```text
Company name: My Company Inc.
Contact name: Jane Smith
Contact email: jane@example.com
```

The wizard prints the trial license key and its expiry date.

!!! tip "Trial Licenses"
    Trial licenses provide full functionality for 15 days. Contact WitFoo sales to convert to a permanent license before the trial expires.

## Step 1b: Product Selection

Select the WitFoo product and tier your license covers, for example Conductor Lite, Pro or Max, Analytics Lite, Pro or Max, Reporter Lite or Pro, or Console. The product decides which roles the next step offers.

## Step 2: Node Role Selection

Select the role this appliance will perform in your deployment. The menu shows only the roles your product allows. Type `b` to go back to product selection.

| # | Role | Description |
|---|------|-------------|
| 1 | Analytics AIO + Conductor | Everything on one server: signal collection, analytics, UI and database. Recommended for most users |
| 2 | Analytics AIO | Analytics without Conductor; signals come from a separate Conductor node |
| 3 | Conductor | Signal collection and forwarding only |
| 4 | Analytics Processing Node | API, UI and processing services; connects to external Cassandra data nodes |
| 5 | Analytics Data Node | Dedicated Cassandra database storage |
| 6 | Console | Central management dashboard for WitFoo appliances |

After selection, the wizard checks the host against the role's minimum RAM and CPU (logical CPUs):

| Role | RAM (min) | CPU (min) |
|------|-----------|-----------|
| Analytics AIO + Conductor | 28 GB | 6 |
| Analytics AIO | 20 GB | 4 |
| Conductor | 8 GB | 2 |
| Analytics Processing Node | 6 GB | 2 |
| Analytics Data Node | 12 GB | 2 |
| Console | 4 GB | 1 |

If the host does not meet the minimum, the wizard shows a warning with the required and detected values and asks `Continue anyway? (yes/no)`.

!!! tip "Choosing a Role"
    - **Analytics** is the primary platform — choose this for investigation, correlation, and reporting.
    - **Conductor** handles data ingestion from remote networks and forwards signals to Analytics.
    - **Console** provides centralized management of multiple Conductor and Analytics nodes.

    See [Deployment Roles](deployment-roles.md) for detailed guidance.

## Step 3: Appliance ID

An Appliance ID uniquely identifies this node. It is used for license binding, Console registration, and NATS authentication. If the node already has one, the wizard offers to keep it:

```text
  Found existing: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Use existing appliance ID? (Y/n):
```

Otherwise it generates a new UUID. On Analytics roles, the wizard also generates a random 32-character Cassandra password.

## Step 4: Network Configuration

Configure the network identity of this node.

```text
Node Hostname: wfa-analytics-01.example.local

Node IP [auto-detect]:
  ✓ Auto-detected: 192.0.2.50
```

- **Node Hostname** — Used to identify this node in the cluster and for TLS certificate validation. Use the machine's FQDN if available.
- **Node IP** — The address other nodes use to reach this machine. Press Enter to auto-detect it from the primary network interface, or type an address.

!!! tip "Static IP Recommended"
    For production deployments, assign a static IP address to the appliance before running the wizard. DHCP-assigned addresses may change, breaking inter-node communication.

## Step 5: Certificate Configuration

Configure TLS certificates for secure communication between WitFoo nodes. Press Enter at each prompt to use the default path. If you have no certificates yet, the defaults are fine: WFA generates self-signed certificates on first deployment.

| Prompt | Default |
|--------|---------|
| Client cert | `/witfoo/certs/client.crt` |
| Client key | `/witfoo/certs/client.key` |
| Server cert | `/witfoo/certs/server.crt` |
| Server key | `/witfoo/certs/server.key` |
| CA cert | `/witfoo/certs/ca.crt` |

!!! danger "Production TLS"
    Self-signed certificates are suitable for evaluation only. For production deployments, provide certificates signed by your organization's certificate authority or a trusted public CA.

## Step 6: Web UI Port & Protocol

Configure the port and protocol for the web UI on this node. This step is skipped on a Data Node.

```text
Web UI protocol [https]:
Web UI port [443]:
```

- **Protocol** — `https` (TLS-encrypted, recommended) or `http` (unencrypted, for development and testing only).
- **Port** — Defaults to `443` for `https` and `80` for `http`.

## Step 7: Admin Account

Set up the initial administrator account for the web UI.

```text
Admin email [admin@witfoo.com]:
Enter admin password: ********
Confirm admin password: ********
  ✓ Admin credentials saved
```

- **Admin email** — Asked on Analytics roles only. It is the login username of the Analytics web UI's initial administrator. Other roles use `admin` as the login username.
- **Password** — At least 8 characters and at most 72 bytes, with no white space at the start or the end. Input is masked and must be entered twice.
- The password is saved, readable by root only, to `/data/local/.passwd`.

!!! warning "WFA 2.5.1 and later may apply this password to the Analytics administrator"
    On the first start of WFA 2.5.1 or later, if the Analytics web UI administrator (`admin@witfoo.com`) still has the shipped default password:

    - When the password file from this step is still on the node, WFA applies it as the Analytics administrator password and signs that administrator's current sessions out.
    - When the file is no longer there, WFA leaves the password as it is and logs a warning that names `wfa user-reset`.

    A password anyone has already set, in the web UI or with `wfa user-reset`, is never changed. This can take up to an hour while the database starts. Before you upgrade, make sure you know the password last entered here, and update any script or integration that signs in as `admin@witfoo.com` with the default password. If you cannot sign in after the upgrade, run `sudo wfa user-reset`.

WFA 2.5.3 removes the password file once the Analytics administrator's password is no longer the seeded default.

## Step 8: Optional Features

The wizard presents role-specific optional features.

### Conductor and Analytics Options

```text
Enable local metrics? (y/n) [n]:
Enable offline mode? (y/n) [n]:
Send operational metrics and status logs from this appliance to WitFoo? ... (y/n):
Enable auto update? (y/n) [y]:
```

- **Local metrics** — Expose a local Prometheus metrics endpoint and Grafana dashboards for monitoring node performance.
- **Offline mode** — Prevent this node from making any outbound internet connections. Only enable this for air-gapped or isolated environments. It disables auto-updates, cloud licensing, Intel API sync and CyberGrid.
- **Metrics export** — Send operational metrics (CPU, disk, memory, container and service health, runtime counters) and status logs to WitFoo's monitoring service. This question has no default: answer `y` or `n`. Choosing No does not affect the appliance's own monitoring.
- **Auto-update** — Automatically apply software updates and security patches. Disable only if you require manual change control.

### Console and Data Node Options

A Console node and a Data Node ask only for **offline mode** (`[n]`) and **auto-update** (`[y]`).

!!! note "FIPS Compliance mode"
    WFA 2.5.1 and later do not offer FIPS Compliance mode, and the wizard no longer asks about it.

## Step 9: Staff-Requested Jobs

```text
Allow WitFoo support staff to request jobs on this appliance? ... (y/n) [n]:
```

Staff-requested jobs are support packs, log collection, diagnostics, update-and-reboot and trust reset. Choosing `n` stops every job WitFoo staff request. Support packs you create and send yourself are not affected. The default is `n` on a new appliance; a re-run offers the answer `node.json` already holds. Change it later with `sudo wfa staff-jobs off` or `sudo wfa staff-jobs on`. See [WFA CLI Reference](../conductor/wfa-cli.md).

## Step 10: Remote Console URL

If you have a WitFoo Console node for centralized management, enter its root URL, for example `https://console.example.com`. This node then sends health and status reports to that Console. Leave it empty if you have no Console or will configure it later. This step is skipped on a Console node.

## Step 11: Analytics Endpoint (Conductor Only)

Enter the URL of the Analytics receiver, so this Conductor can send artifacts to the Analytics node. Port 8443 is the TLS ingestion port:

```text
Analytics endpoint [none]: https://<analytics-host>:8443
```

Leave it empty if you will configure the exporter in the Conductor UI later.

## Step 12: Clustering Configuration

Distributed deployments need the nodes to know about each other. On a Data Node this step comes right after the Admin Account step; on a Processing Node it comes after the Remote Console URL.

- **Analytics Processing Node** — Enter the data node addresses as comma-separated `IP:port` pairs (for example `192.0.2.10:9042,192.0.2.11:9042`), then the Cassandra password that was generated on your Data Node.
- **Analytics Data Node** — Enter the seed node IPs of every data node in the Cassandra cluster, including this node's own IP, and the listen address Cassandra binds to (Enter uses the node IP).

## Step 13: Review and Save

The wizard displays a summary of all configured settings and asks `Save this configuration? (y/n)`. After you confirm, it:

1. Writes `/witfoo/configs/node.json` (and `analytics.json` on Analytics roles).
2. Starts the `wfad` service.
3. Shows the initialization progress: image pulls (up to 8 minutes), container health (up to 2 minutes), then the web UI address.

Monitoring is non-fatal: if the containers take longer, the wizard prints a warning with manual checks (`docker ps`, `docker images | grep witfoo`).

## Re-running the Wizard

You can re-run `sudo wfa configure` (or `sudo wfa fetch`) to change settings.

- **The MCP settings are kept.** A re-run keeps `mcp_http_enabled`, `mcp_exposure_enabled`, `mcp_public_url`, `mcp_oauth_ui_url`, `mcp_oauth_cimd` and the relay's `mcp_relay_` fields. A value that cannot be read is named and left out, and the old file is kept beside the new one as `node.json.unreadable-<time>.bak`.
- **Your staff-jobs choice is kept.**
- **Other settings that no prompt asks for are not kept.** This includes `trusted_proxies`.

!!! warning "Add `trusted_proxies` again after every re-run"
    A re-run of `wfa configure` or `wfa fetch` (including `wfa configure --license-file`) writes `node.json` without `trusted_proxies`. Add it again after each re-run, then run `sudo wfa restart`. See [TLS Configuration](../deployment/tls.md).

The wizard does not set the MCP keys. To turn on MCP, add them to `node.json` by hand and run `sudo wfa restart`. They need WFA 2.5.1 or later. See [MCP Configuration](../ai/mcp/configuration.md).

## What Happens Next

After the wizard completes:

1. The WFA daemon pulls container images from the configured registry
2. Services start in dependency order (Cassandra first, then dependent services)
3. For **Analytics** nodes, the web UI becomes available on port 443 within a few minutes
4. Proceed to [First Login](first-login.md) to change default passwords and complete the onboarding wizard
