# WFA CLI Reference

The `wfa` command-line tool manages WitFoo Appliances. All commands require `sudo`. This page describes WFA 2.5.3, the release that shipped with WitFoo Analytics 1.2.0, and WFA 2.5.4, which has the same commands.

!!! warning "Never run `wfad --version`"
    `wfad` is the WFA daemon, not a command-line tool. Running `wfad --version` starts a second daemon. To read the installed version, run `sudo wfa version`, `rpm -q wfa` or `dpkg -s wfa`.

## `wfa configure`

Interactive setup wizard that generates `/witfoo/configs/node.json`, and `/witfoo/configs/analytics.json` for Analytics roles. The wizard walks through these steps:

| Step | Prompt | Details |
|------|--------|---------|
| 1 | **License Configuration** | Cloud: fetched automatically. On-prem: enter a license key, or request a 15-day trial (company name, contact name, contact email, and acceptance of the EULA). The organization ID and name come from the license |
| 1b | **Product Selection** | The WitFoo product and tier your license covers. It decides which roles the next step offers |
| 2 | **Node Role Selection** | AIO + Conductor, AIO, Conductor, Processing Node, Data Node or Console. Hardware check warns if the host is below the role's minimum RAM and CPU |
| — | **Appliance ID** | Keeps the existing appliance ID, or generates a new UUID |
| 4 | **Network Configuration** | Node hostname and node IP (Enter auto-detects the IP) |
| 5 | **Certificate Configuration** | Paths for client cert/key, server cert/key and CA cert (defaults under `/witfoo/certs/`) |
| 6 | **Web UI Port & Protocol** | `https` (default, port 443) or `http` (port 80). Not asked on a Data Node |
| 7 | **Admin Account** | Analytics roles: admin email (default `admin@witfoo.com`). All roles: a password of at least 8 characters and at most 72 bytes, entered twice |
| 8 | **Optional Features** | Local metrics, offline mode, metrics export to WitFoo (no default) and auto-update. Console and Data Node: offline mode and auto-update only |
| — | **Staff-requested jobs** | Whether WitFoo support staff may request jobs on this appliance. Default `n` on a new install |
| — | **Remote Console URL** | Optional. Not asked on a Console node |
| — | **Analytics Endpoint** | Conductor only: the Analytics receiver URL, for example `https://<analytics-host>:8443` |
| — | **Clustering Configuration** | Processing Node: data node addresses and the Cassandra password. Data Node: seed node IPs and listen address |
| — | **Review** | Display all settings, then `Save this configuration? (y/n)` |

After you confirm, the wizard writes `node.json` with mode `0600`, starts `wfad` and shows the initialization progress.

```bash
sudo wfa configure
```

Re-running `wfa configure` keeps the MCP settings in `node.json` and your staff-jobs choice, but not `trusted_proxies`. See [WFA Configure Wizard](../getting-started/wfa-configure.md).

## `wfa fetch`

Claims a configuration built in the Console from a one-time URL, instead of running the whole wizard. It pulls the license, organization, product, role, registry and ports, then asks only for this machine's details (appliance ID, hostname, IP, certificates) and the admin password. The URL works once. With no URL given, the command asks for it.

```bash
sudo wfa fetch <console-configuration-url>
```

| Flag | Description |
|------|-------------|
| `--url` | Console configuration URL (may include the token) |
| `--token` | One-time token, if the URL does not include it |
| `--insecure` | Skip TLS verification (self-signed Console certificate) |

Like `wfa configure`, a re-run keeps the MCP settings and drops `trusted_proxies`.

## `wfa user-reset`

Resets the initial administrator account for the **Analytics web UI** from the appliance
command line. Use it when nobody can sign in — a forgotten password, a mistyped email at
setup, or an account that was deactivated.

```bash
sudo wfa user-reset
```

The command is interactive. It shows the existing initial admin account (email, username,
name, organization, active state, and last login), offers to change the email address, then
prompts twice for a new password with masked input:

| Prompt | Rules |
|------|--------|
| **Change the admin email address?** | Optional. The email is the login username. Must contain `@` and `.` and no spaces. An address already used by a **different** account is refused — the database does not enforce email uniqueness, and a duplicate would silently shadow one account at login |
| **New admin password** | Required. Minimum 8 characters, entered twice |

If the account was deactivated, a successful reset also re-activates it.

The change is written directly to the Analytics database and **takes effect at the next
login — no service restart is required**.

!!! note "Which account this resets"
    It resets the *initial* admin account created when the appliance was provisioned — the
    one seeded as `admin@witfoo.com`. The account is identified by its fixed internal id
    rather than its email, so the reset still works if the email was changed earlier. Other
    user accounts are managed from **Admin → Users** in the web UI; see
    [User Management](../admin-guide/users.md).

### Requirements

- Analytics roles only — `aio`, `aio-conductor`, `processing`, or `data`. On any other role
  the command exits with an explanation, because the Analytics web UI admin account does not
  exist there.
- The Analytics stack must be running, since the command connects to the Analytics database
  using the credentials in `/witfoo/configs/node.json`. It waits up to 60 seconds for the
  database. If the database has never been seeded, start the stack once with `sudo wfa start`
  and retry.
- An interactive terminal, because the password prompt is masked. It cannot be scripted or
  piped.

### Troubleshooting

| Message | Cause and fix |
|------|--------|
| `user-reset manages the Analytics web UI admin account, which does not exist on the "<role>" role` | You are on a Conductor, Console, or other non-Analytics node. Run it on the Analytics appliance |
| `error connecting to the Analytics database (is the analytics stack running?)` | The database is unreachable. Check `sudo wfa status` and start the stack with `sudo wfa start` |
| `Cassandra authentication failed` | The `cassandra_password` in `/witfoo/configs/node.json` no longer matches the database, or the database started in the last few minutes and has not set it yet. Wait until `docker logs analytics-cassandra-svc` prints `Cassandra schema initialization complete`, then retry |
| `Cannot resolve the Analytics database address` | On AIO, AIO + Conductor and Data nodes, WFA writes the database's name into `/etc/hosts` when `wfad` starts. Look for a `[WARN] /etc/hosts was not updated` line in the `wfad` log. On a Processing node, check the seed node addresses in `node.json` |
| `initial admin account not found — the Analytics database has not been seeded yet` | First-time appliance whose stack has not completed its first start. Run `sudo wfa start`, wait for the services to come up, and retry. The message also prints the steps to restore the initial administrator when the stack is already running |
| `failed to read password (user-reset requires an interactive terminal)` | The command was run without a TTY — for example over a non-interactive SSH command. Use an interactive session |

*Added in WFA 2.4.8. WFA 2.4.9 fixed a failure (`Undefined column name theme`) on appliances
whose Analytics stack predates the per-user theme column — upgrade to 2.4.9 or later if you
hit it.*

!!! info "Fixed in WFA 2.5.1 and later"
    - `wfa user-reset` works on appliances whose Analytics database was created by Analytics 1.1.x. It no longer fails with `Undefined column name sessions_valid_after`.
    - It stops at once on a rejected database credential or an address it cannot resolve.
    - It always writes a password hash the 1.2.0 api can check. If an administrator could not sign in after `wfa user-reset` was run on a FIPS host under WFA 2.4.14 to 2.4.16, run `wfa user-reset` again once the appliance runs WFA 2.5.1 or later (install WFA 2.5.3) and the 1.2.0 images.

## `wfa staff-jobs`

Shows or changes whether WitFoo support staff can request jobs on this appliance. Staff-requested jobs are support packs, log collection, diagnostics, update-and-reboot and trust reset. Turning them off stops every one of them. Support packs you create and send yourself with `wfa support` are not affected.

```bash
sudo wfa staff-jobs status
sudo wfa staff-jobs off
sudo wfa staff-jobs on
```

| Subcommand | Description |
|------|--------|
| `status` | Show whether staff-requested jobs are allowed, and which job types the setting covers |
| `off` | Turn staff-requested jobs off |
| `on` | Allow staff-requested jobs again |

- A new appliance starts with staff-requested jobs off. An appliance configured before WFA 2.5.1 keeps what it had.
- The setting is `staff_jobs_opt_out` in `node.json`. Only this command, `wfa configure` and, on a new install, `wfa fetch` write it. Re-running `wfa configure` or `wfa fetch` keeps your choice.
- The change takes effect when the `wfad-helper` service restarts. `off` and `on` restart it, unless a job is running in it.

*Added in WFA 2.5.1.*

## `wfa mcp-relay`

Turns the AI-connector relay on, keeps it acknowledged, shows its status, and turns it off. The relay gives an AI marketplace or MCP client an address that reaches this appliance's MCP endpoint through WitFoo, without an inbound port. It is off by default. Read [MCP Relay](../ai/mcp/relay.md), including the notice, before you turn it on.

| Subcommand | Description |
|------|--------|
| `enable` | Show the notice and register this appliance's relay address. Needs a terminal |
| `ack` | Show the current notice and acknowledge it again after a notice version change. Needs a terminal |
| `status` | Show whether the relay is on, its address, its acknowledgement and what the relay reports |
| `off` | Revoke the relay address and turn the relay off. Asks you to type `REVOKE`; `--yes` skips the prompt in a script |
| `revoke` | The same as `off` |

### Turning the relay on

```bash
sudo wfa mcp-relay enable
sudo wfa restart
```

1. `enable` shows the notice. Only typing `ENABLE` turns the relay on; anything else, or Enter, leaves it off. No flag, variable, file or Console message can turn it on.
2. `enable` registers the appliance, writes the address, credential and acknowledgement to `node.json`, and prints the address.
3. If `mcp_public_url` is empty, `enable` sets it to the relay address.
4. Run `sudo wfa restart`. `wfad` reads `node.json` only when it starts, so the relay carries nothing until the restart. The restart stops and starts every container on the appliance.

The relay needs the MCP HTTP transport (`mcp_http_enabled`); `enable` does not turn it on.

### Turning the relay off

```bash
sudo wfa mcp-relay off
sudo wfa restart
```

`off` clears the address only after the relay confirms the revocation. If the relay cannot be reached, the revocation stays pending and the command exits non-zero: run it again. A revoked address is never restored. Turning the relay on again gives a new address.

### Re-acknowledging the notice

When the relay notice changes version, a relay acknowledged at the old version stops. Run `sudo wfa mcp-relay ack`, read and acknowledge the new notice, then run `sudo wfa restart`. The address does not change. The relay accepts three acknowledgements for an address at once and then one a minute.

!!! note "Offline mode"
    The relay stops while `offline_mode` is set, and `wfa mcp-relay ack` refuses. To resume after you clear `offline_mode`, run `sudo wfa mcp-relay ack` if asked, then `sudo wfa restart`.

*Added in WFA 2.5.1.*

## `wfa status`

Displays WFA version, `wfad` systemd service state, error count since start, and the last 10 error log entries from the journal.

```bash
sudo wfa status
```

## `wfa diag`

Runs connectivity and system diagnostics with formatted output:

**Connectivity checks:**

| Check | Target |
|-------|--------|
| WitFoo Metrics | Metrics endpoint reachability |
| WitFoo Intel | `intel.witfoo.com` |
| WitFoo Licensing | `licensing.witfoo.com` |
| Docker Registry | Container image registry (if configured) |
| Cassandra Seeds | Port 9042 (if configured) |

**System checks:**

| Check | Description |
|-------|-------------|
| Kafka Topics | Topic health (Streamer roles) |
| Disk Usage | Warns at >80% utilization |

Output is a formatted table with check name, result, and status (pass/fail).

```bash
sudo wfa diag
```

## `wfa support`

Generates a comprehensive support bundle with 19 diagnostic categories:

| Category | Contents |
|----------|----------|
| Docker Inspect | Container configuration details |
| Docker PS | Running container list |
| Docker Logs | Last 500 lines per container |
| Docker Images | Installed image list |
| Journal | Last 24 hours of systemd journal |
| Disk Usage | Filesystem utilization |
| Hosts File | `/etc/hosts` contents |
| Users | System user list |
| Var Log | Regular files under `/var/log` (500 MB limit); what was left out is listed in `COLLECTION-MANIFEST.txt` |
| Node Config | `/witfoo/configs/node.json`, with credentials masked |
| Cassandra | nodetool (describecluster, ring, info, status, tablestats), CQL schema |
| Netstat | Network connections |
| IP Route | Routing table |
| IPTables | Firewall rules |
| Listening Ports | `ss -tulpn` output |
| Docker Networks | Network configuration |
| NATS | Server info, stream/consumer reports, KV bucket contents |
| Pipeline Metrics | conductor-ui API metrics, Docker stats |
| Extended Logs | Last 2000 lines per pipeline service |

Output: `support-{org_id}-{timestamp}.zip`

The bundle uploads to WitFoo Intel (`intel.witfoo.com`) with the appliance's license key. Without a license, the file is saved locally. Support packs mask the MCP relay's handle and credential.

```bash
sudo wfa support
```

## `wfa certs`

Displays certificate status in a table format showing CA, server cert/key, and client cert/key with their source type (embedded, customer, or generated).

```bash
sudo wfa certs
```

Force re-extract embedded certificates and regenerate the CA bundle:

```bash
sudo wfa certs --refresh
```

Accept a changed CA fingerprint for a peer:

```bash
sudo wfa certs --accept-peer <host:port>
```

## `wfa images`

Offline container image management for air-gapped deployments.

List required images and their local availability:

```bash
sudo wfa images --list
```

Pull and save all required images to a tar file:

```bash
sudo wfa images --save
```

Output: `/witfoo/images/{role}-images.tar`

Load images from a tar file into Docker:

```bash
sudo wfa images --load
```

!!! tip "Offline Deployment Workflow"
    For air-gapped environments:

    1. On an internet-connected machine: `sudo wfa images --save`
    2. Transfer `/witfoo/images/{role}-images.tar` to the air-gapped node (USB, SCP, etc.)
    3. On the air-gapped node: `sudo wfa images --load`
    4. Start services: `sudo wfa start`

## `wfa start`

Starts the `wfad` systemd service. Enables the service if not already enabled.

```bash
sudo wfa start
```

## `wfa stop`

Stops the `wfad` systemd service and all managed containers.

```bash
sudo wfa stop
```

## `wfa restart`

Restarts the `wfad` systemd service, which triggers a full container lifecycle restart. `wfad` reads `node.json` only when it starts, so run `wfa restart` after you edit `node.json` by hand.

```bash
sudo wfa restart
```

## `wfa enable`

Enables the `wfad` service for automatic start at boot via `systemctl enable wfad`.

```bash
sudo wfa enable
```

## `wfa reboot`

Stops `wfad` and `wfad-helper`, runs system package updates (`apt update` and `apt upgrade -y`, or `dnf upgrade -y` on RHEL), then reboots the system. The reboot still runs if the package update fails.

```bash
sudo wfa reboot
```

## `wfa version`

Displays the installed WFA version, for example `WFA 2.5.3`.

```bash
sudo wfa version
```
