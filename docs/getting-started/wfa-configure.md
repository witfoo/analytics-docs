# WFA Configure Wizard

The `sudo wfa configure` command launches an interactive wizard that configures a WitFoo Appliance for its intended role. This page documents every step of the wizard, including the exact prompts, options, and role-specific differences.

## Overview

The wizard generates the configuration file `/witfoo/configs/node.json`, which the WFA daemon uses to determine which services to run and how to configure them. Run the wizard as root:

```bash
sudo wfa configure
```

## Step Applicability by Role

Not every step applies to every role. Use this table as a quick reference:

| Step | Conductor | Console | Analytics |
|------|:---------:|:-------:|:---------:|
| 1. Organization Information | ✅ | ✅ | ✅ |
| 2. Role Selection | ✅ | ✅ | ✅ |
| 3. License Configuration | ✅ | ✅ | ✅ |
| 4. Appliance ID | ✅ | — | ✅ |
| 5. Node Hostname and IP | ✅ | ✅ | ✅ |
| 6. Network Configuration | ✅ | — | — |
| 7. Registry Configuration | ✅ | ✅ | ✅ |
| 8. Certificate Configuration | ✅ | ✅ | ✅ |
| 9. Admin Password | ✅ | ✅ | ✅ |
| 10. Optional Features | ✅ | ✅ | ✅ |
| 11. Review and Save | ✅ | ✅ | ✅ |

## Step 1: Organization Information

The wizard begins by collecting your organization details.

```
=== Organization Information ===
Organization ID: mycompany
Organization Name: My Company Inc.
```

- **Organization ID** — A DNS-valid, lowercase identifier for your organization (e.g., `mycompany`). This is used internally for data partitioning and must be consistent across all nodes in your deployment.
- **Organization Name** — The human-readable display name for your organization.

!!! tip "Organization ID Format"
    The Organization ID must be lowercase, contain only letters, numbers, and hyphens, and be valid as a DNS label. Choose this carefully — it cannot be changed after deployment without data migration.

## Step 2: Role Selection

Select the role this appliance will perform in your deployment.

```
=== Role Selection ===
Select appliance role:
  1) Conductor
  2) Console
  3) Analytics

Enter selection [1-3]: 3
```

After selection, the wizard performs a hardware check against the minimum requirements for the chosen role:

| Role | CPU (min) | RAM (min) | Disk (min) |
|------|-----------|-----------|------------|
| Conductor | 4 | 8 GB | 220 GB |
| Console | 4 | 8 GB | 220 GB |
| Analytics | 8 | 12 GB | 220 GB |

If the host does not meet the minimum requirements, the wizard displays a warning:

```
⚠ WARNING: This host has 4 CPU cores but the Analytics role requires a minimum of 8.
  Performance may be degraded. Continue anyway? [y/N]:
```

!!! tip "Choosing a Role"
    - **Analytics** is the primary platform — choose this for investigation, correlation, and reporting.
    - **Conductor** handles data ingestion from remote networks and forwards signals to Analytics.
    - **Console** provides centralized management of multiple Conductor and Analytics nodes.

    See [Deployment Roles](deployment-roles.md) for detailed guidance.

## Step 3: License Configuration

The wizard configures your WitFoo license, which determines available features and container registry access.

**Cloud deployments** (AWS, Azure, Google Cloud marketplace instances):

```
=== License Configuration ===
Cloud deployment detected. Fetching license from licensing.witfoo.com...
License validated successfully.
  Organization: My Company Inc.
  Tier: Enterprise
  Expiration: 2026-03-15
```

The license is automatically retrieved from `licensing.witfoo.com` based on the cloud instance metadata.

**On-premises deployments:**

```
=== License Configuration ===
Select license method:
  1) Enter license key
  2) Request 15-day trial

Enter selection [1-2]:
```

**Option 1 — Enter license key:**

```
License Key: XXXX-XXXX-XXXX-XXXX
Validating license... ✓
```

**Option 2 — Request 15-day trial:**

```
Company Name: My Company Inc.
Contact Name: Jane Smith
Contact Email: jane@mycompany.com
CPU Core Count: 16

Requesting trial license... ✓
Trial license activated. Expires: 2026-02-01
```

!!! tip "Trial Licenses"
    Trial licenses provide full functionality for 15 days. Contact WitFoo sales to convert to a permanent license before the trial expires.

## Step 4: Appliance ID

An Appliance ID uniquely identifies this node within your deployment. This step is **skipped for Console nodes**, which manage other appliances rather than processing data directly.

```
=== Appliance ID ===
Auto-generated Appliance ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Accept this ID? [Y/n]:
```

The wizard auto-generates a UUID. Accept the default or enter a custom UUID if replacing an existing node.

!!! tip "Console Nodes"
    Console nodes skip this step because they do not have their own Appliance ID — they manage the IDs of the Conductor and Analytics nodes they monitor.

## Step 5: Node Hostname and IP

Configure the network identity of this node.

```
=== Node Hostname and IP ===
Hostname [wfa-analytics-01]: wfa-analytics-01
Detected IP address: 10.0.1.50
Use detected IP? [Y/n]:
```

- **Hostname** — The hostname for this node. Auto-detected from the system hostname.
- **IP Address** — The primary IP address. Auto-detected from the active network interface with an option to override manually.

If you decline the detected IP:

```
Enter IP address: 10.0.1.100
```

!!! tip "Static IP Recommended"
    For production deployments, assign a static IP address to the appliance before running the wizard. DHCP-assigned addresses may change, breaking inter-node communication.

## Step 6: Network Configuration (Conductor Only)

This step configures the NATS message broker ports and limits. It appears **only for Conductor nodes**.

```
=== Network Configuration ===
Broker client port [4223]: 4223
Broker leaf node port [4443]: 4443
Max data size (MB) [1024]: 1024
```

- **Broker client port** — The port that data sources connect to for signal submission (default: `4223`).
- **Broker leaf node port** — The port used for leaf node connections between Conductor and Analytics nodes (default: `4443`).
- **Max data size** — Maximum message payload size in megabytes (default: `1024` MB).

!!! tip "Firewall Rules for Conductor"
    Ensure your firewall allows inbound connections on the broker client port (default 4223) from data sources, and on the leaf node port (default 4443) from Analytics nodes.

## Step 7: Registry Configuration

Configure access to the WitFoo container registry for pulling service images.

```
=== Registry Configuration ===
Container registry credentials populated from license validation.
  Registry: registry.witfoo.com
  Username: mycompany
  Status: ✓ Authenticated
```

Registry credentials are automatically populated from the license validation performed in Step 3. If credentials need to be entered manually:

```
Registry URL [registry.witfoo.com]: registry.witfoo.com
Registry Username: mycompany
Registry Password: ********
Validating credentials... ✓
```

## Step 8: Certificate Configuration

Configure TLS certificates for secure communication between nodes and with the web UI.

```
=== Certificate Configuration ===
Configure custom TLS certificates? [y/N]:
```

If you accept the defaults, the wizard uses self-signed certificates stored under `/witfoo/certs/`. To provide your own certificates:

```
Configure custom TLS certificates? [y/N]: y

Client certificate path [/witfoo/certs/client-cert.pem]: /path/to/client-cert.pem
Client key path [/witfoo/certs/client-key.pem]: /path/to/client-key.pem
Server certificate path [/witfoo/certs/server-cert.pem]: /path/to/server-cert.pem
Server key path [/witfoo/certs/server-key.pem]: /path/to/server-key.pem
CA certificate path [/witfoo/certs/ca-cert.pem]: /path/to/ca-cert.pem

Validating certificates... ✓
```

!!! danger "Production TLS"
    Self-signed certificates are suitable for evaluation only. For production deployments, provide certificates signed by your organization's certificate authority or a trusted public CA.

!!! tip "Certificate Paths"
    Default certificate paths are under `/witfoo/certs/`. You can place your certificates there before running the wizard to accept the defaults.

## Step 9: Admin Password

Set the administrative password for the appliance.

```
=== Admin Password ===
Enter admin password (min 8 characters): ********
Confirm admin password: ********
Admin password saved.
```

- Minimum 8 characters required
- Input is masked (not displayed)
- Confirmation must match
- Password is saved to `/data/local/.passwd`

!!! danger "Choose a Strong Password"
    This password is used for appliance-level administration. Choose a strong, unique password and store it securely. It is separate from the web UI admin password.

## Step 10: Optional Features

The wizard presents role-specific optional features. Available options vary by role.

### Conductor Options

```
=== Optional Features ===
Enable local metrics (Prometheus/Grafana)? [y/N]: y
Enable offline mode? [y/N]: n
Enable metrics export? [y/N]: y
Enable auto-update? [y/N]: y
Remote console FQDN (leave blank to skip): console.mycompany.com
```

- **Local metrics** — Deploy Prometheus and Grafana containers for local monitoring of the Conductor node.
- **Offline mode** — Operate without internet connectivity. Requires pre-loaded container images.
- **Metrics export** — Export Conductor metrics to an external monitoring system.
- **Auto-update** — Automatically pull and apply updates from the WitFoo registry.
- **Remote console FQDN** — The fully qualified domain name of the Console node that manages this Conductor.

### Console Options

```
=== Optional Features ===
Enable offline mode? [y/N]: n
Enable auto-update? [y/N]: y
```

- **Offline mode** — Operate without internet connectivity.
- **Auto-update** — Automatically pull and apply updates from the WitFoo registry.

### Analytics Options

```
=== Optional Features ===
Configure data retention policies? [y/N]: y
  Artifact retention (days) [7]: 30
  Work unit retention (days) [365]: 365
  Work collection retention (days) [365]: 365
  Report retention (days) [1825]: 1825

Configure UI module visibility? [y/N]: y
  Module visibility [all/search_only/search_observer]: all

Enable CyberGrid integration? [y/N]: y
  CyberGrid mode [consumer/contributor/full]: consumer

Configure clustering? [y/N]: n
```

- **Data retention policies** — Set how long different data types are retained in the database.
- **UI module visibility** — Control which modules appear in the web UI (all, search only, or search + observer).
- **CyberGrid integration** — Enable threat intelligence sharing. Choose Consumer (receive only), Contributor (send and receive), or Full participation.
- **Clustering** — Configure multi-node Cassandra clustering for horizontal scaling. Prompts for seed nodes and data node addresses.

!!! tip "Analytics Retention Defaults"
    The default retention periods are optimized for most deployments. Artifacts (raw data) default to 7 days, while work units, collections, and reports are retained for 1–5 years. Adjust based on your compliance requirements and available disk space.

## Step 11: Review and Save

The wizard displays a summary of all configured settings for review.

```
=== Configuration Summary ===
Organization ID:    mycompany
Organization Name:  My Company Inc.
Role:               Analytics
Appliance ID:       a1b2c3d4-e5f6-7890-abcd-ef1234567890
Hostname:           wfa-analytics-01
IP Address:         10.0.1.50
Registry:           registry.witfoo.com
TLS:                Custom certificates
Auto-update:        Enabled
Data Retention:     Artifacts: 30d, Work Units: 365d, Reports: 1825d
UI Modules:         All
CyberGrid:          Consumer

Save this configuration? [Y/n]: y

Configuration saved to /witfoo/configs/node.json
Starting services...
```

After confirmation, the wizard writes the configuration to `/witfoo/configs/node.json` and the WFA daemon begins pulling container images and starting services.

!!! tip "Re-running the Wizard"
    You can re-run `sudo wfa configure` at any time to modify settings. The wizard will load existing values from `/witfoo/configs/node.json` as defaults, allowing you to change only what's needed.

## What Happens Next

After the wizard completes:

1. The WFA daemon pulls container images from the configured registry
2. Services start in dependency order (Cassandra first, then dependent services)
3. For **Analytics** nodes, the web UI becomes available on port 443 within a few minutes
4. Proceed to [First Login](first-login.md) to change default passwords and complete the onboarding wizard