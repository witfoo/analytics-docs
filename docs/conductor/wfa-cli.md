# WFA CLI Reference

The `wfa` command-line tool manages WitFoo Appliances. All commands require `sudo`.

## `wfa configure`

Interactive setup wizard that generates `/witfoo/configs/node.json`. The wizard walks through 12 configuration steps:

| Step | Prompt | Details |
|------|--------|---------|
| 1 | **Organization Info** | Organization ID (DNS-valid, lowercase) and Organization Name |
| 2 | **Role Selection** | Conductor or Console. Hardware check warns if below minimum (Conductor: 4 CPU, 8 GB RAM) |
| 3 | **License** | Cloud: auto-fetch from `licensing.witfoo.com`. On-prem: manual key entry or 15-day trial request (company, contact, email, core count) |
| 4 | **Appliance ID** | Auto-generated UUID (Conductor only; Console skips this step) |
| 5 | **Network** | Hostname and IP address (auto-detect with manual override) |
| 6 | **Broker Config** | Conductor only: client port (4223), leaf port (4443), max data (1024 MB) |
| 7 | **Registry** | Container registry (auto-configured from license) |
| 8 | **TLS Certificates** | Paths for client cert/key, server cert/key, CA cert (defaults: `/witfoo/certs/`) |
| 9 | **Admin Password** | Minimum 8 characters, masked input with confirmation. Saved to `/data/local/.passwd` |
| 10 | **Features** | Conductor: local metrics, offline mode, metrics export, auto-update, console FQDN. Console: offline mode, auto-update only |
| 11 | **Review** | Display all settings for confirmation (y/n) |
| 12 | **Save** | Write `/witfoo/configs/node.json` with permissions `0600` |

```bash
sudo wfa configure
```

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
| **New admin password** | Required. Minimum 8 characters, entered twice. Same rules as step 9 of `wfa configure` |

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
  using the credentials in `/witfoo/configs/node.json`. If the database has never been
  seeded, start the stack once with `sudo wfa start` and retry.
- An interactive terminal, because the password prompt is masked. It cannot be scripted or
  piped.

### Troubleshooting

| Message | Cause and fix |
|------|--------|
| `user-reset manages the Analytics web UI admin account, which does not exist on the "<role>" role` | You are on a Conductor, Console, or other non-Analytics node. Run it on the Analytics appliance |
| `error connecting to the Analytics database (is the analytics stack running?)` | The database is unreachable. Check `sudo wfa status` and start the stack with `sudo wfa start` |
| `Cassandra authentication failed` | The `cassandra_password` in `/witfoo/configs/node.json` no longer matches the database |
| `initial admin account not found — the Analytics database has not been seeded yet` | First-time appliance whose stack has not completed its first start. Run `sudo wfa start`, wait for the services to come up, and retry |
| `failed to read password (user-reset requires an interactive terminal)` | The command was run without a TTY — for example over a non-interactive SSH command. Use an interactive session |

*Added in WFA 2.4.8. WFA 2.4.9 fixed a failure (`Undefined column name theme`) on appliances
whose Analytics stack predates the per-user theme column — upgrade to 2.4.9 or later if you
hit it.*

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
| Grafana Cloud | Metrics endpoint reachability |
| Intel | `intel.witfoo.com` |
| Library | `library.witfoo.com` |
| Licensing | `licensing.witfoo.com` |
| Docker Registry | Container image registry |
| Cassandra Seeds | Port 9042 (if applicable) |

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
| Var Log | `/var/log` contents (500 MB limit) |
| Node Config | `/witfoo/configs/node.json` |
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

The bundle auto-uploads to `library.witfoo.com` if a license is configured. Without a license, the file is saved locally.

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

Restarts the `wfad` systemd service, which triggers a full container lifecycle restart.

```bash
sudo wfa restart
```

## `wfa enable`

Enables the `wfad` service for automatic start at boot via `systemctl enable wfad`.

```bash
sudo wfa enable
```

## `wfa reboot`

Stops `wfad`, runs system package updates (`apt update && apt upgrade -y`), then reboots the system.

```bash
sudo wfa reboot
```

## `wfa version`

Displays the current WFA version string.

```bash
sudo wfa version
```
