# Installation

This guide covers deploying a WitFoo Appliance (WFA) — the production deployment method for WitFoo Analytics. The WFA daemon manages containers, configuration, and lifecycle for all node roles.

## Prerequisites

- Network access to the target host via SSH (port 22) and HTTPS (port 443)
- A WitFoo license key, or plan to request a 15-day trial during configuration
- Hardware meeting the minimum requirements for your chosen [deployment role](deployment-roles.md)

### Hardware Requirements

| Tier | CPU Cores | RAM | Disk |
|------|-----------|-----|------|
| **Minimum** | 8 | 12 GB | 220 GB |
| **Recommended** | 16 | 32 GB | 1 TB |

#### Per-Role Minimums

| Role | CPU (min) | RAM (min) | Disk (min) |
|------|-----------|-----------|------------|
| Conductor | 4 | 8 GB | 220 GB |
| Console | 4 | 8 GB | 220 GB |
| Analytics | 8 | 12 GB | 220 GB |

## Installation Overview

Deploying WitFoo Analytics follows three steps regardless of your infrastructure:

1. **Deploy** a WitFoo Appliance image or run an install script
2. **Configure** the appliance role with `sudo wfa configure`
3. **Access** the web UI via HTTPS (port 443) and complete the onboarding wizard

## Step 1: Deploy a WitFoo Appliance

Choose the deployment method that matches your infrastructure. All appliance images and scripts are available from the [witfoo-appliances](https://github.com/witfoo/witfoo-appliances) repository.

### Option A: On-Premises VM

Pre-built Ubuntu 24 virtual machine images are available for the following hypervisors:

1. Download the appropriate image from [github.com/witfoo/witfoo-appliances](https://github.com/witfoo/witfoo-appliances):
    - **VMware** — OVA format
    - **Hyper-V** — VHDX format
    - **QEMU/KVM** — QCOW2 format

2. Import the image into your hypervisor and allocate resources according to the [hardware requirements](#hardware-requirements) for your intended role.

3. Boot the virtual machine. The appliance will start with a default network configuration using DHCP.

4. Connect via SSH to the appliance:

    ```bash
    ssh witfooadmin@<appliance-ip>
    ```

!!! danger "Change Default Credentials Immediately"
    The default SSH credentials are `witfooadmin` / `F00theN0ise!`. Change these immediately after first login. See [First Login](first-login.md) for details.

### Option B: Cloud Marketplace

WitFoo Appliances are available on major cloud marketplaces:

1. Launch a WitFoo Appliance instance from your cloud provider's marketplace:
    - **AWS Marketplace** — Search for "WitFoo Appliance"
    - **Azure Marketplace** — Search for "WitFoo Appliance"
    - **Google Cloud Marketplace** — Search for "WitFoo Appliance"

2. Select an instance size that meets the [hardware requirements](#hardware-requirements) for your intended role.

3. Configure your security group or firewall rules to allow:
    - **Port 22** — SSH (administration)
    - **Port 443** — HTTPS (web UI)

4. Connect via SSH using your cloud provider's key pair or the default credentials.

!!! tip "Cloud Instance Sizing"
    For an Analytics node, start with at least 8 vCPUs and 12 GB RAM. For production workloads, 16 vCPUs and 32 GB RAM with 1 TB disk is recommended.

### Option C: Bare Metal

Install the WitFoo Appliance directly on a physical or virtual server using the provided install scripts:

**Ubuntu 24:**

1. Start with a fresh Ubuntu 24 server installation.

2. Download and run the install script:

    ```bash
    curl -fsSL https://raw.githubusercontent.com/witfoo/witfoo-appliances/main/ubuntu-install.sh -o ubuntu-install.sh
    chmod +x ubuntu-install.sh
    sudo ./ubuntu-install.sh
    ```

3. The script installs all dependencies, creates the `witfooadmin` user, and installs the WFA daemon.

**RHEL 10:**

1. Start with a fresh RHEL 10 server installation.

2. Download and run the install script:

    ```bash
    curl -fsSL https://raw.githubusercontent.com/witfoo/witfoo-appliances/main/rhel-install.sh -o rhel-install.sh
    chmod +x rhel-install.sh
    sudo ./rhel-install.sh
    ```

3. The script installs all dependencies, creates the `witfooadmin` user, and installs the WFA daemon.

## Step 2: Configure the Appliance

Once the appliance is deployed, run the interactive configuration wizard to select a role and configure services:

```bash
sudo wfa configure
```

The wizard walks you through organization setup, role selection, licensing, networking, and optional features. It generates the configuration file at `/witfoo/configs/node.json`.

For a detailed walkthrough of every prompt and option, see [WFA Configure Wizard](wfa-configure.md).

## Step 3: Access the Web UI

After configuration completes, the WFA daemon starts all services for your selected role. For Analytics nodes:

1. Open a web browser and navigate to:

    ```
    https://<appliance-ip>
    ```

2. Log in with the default web UI credentials:
    - **Email:** `admin@witfoo.com`
    - **Password:** `F00theN0ise!`

3. Complete the 12-step onboarding wizard to configure your organization, users, and integrations.

See [First Login](first-login.md) for detailed instructions on the onboarding process.

!!! danger "Change Default Passwords"
    Both the SSH and web UI default passwords must be changed immediately after first login. See [First Login](first-login.md) for instructions.

## Verifying the Installation

After completing configuration, verify that services are running:

```bash
sudo wfa analytics status
```

This command lists all expected services and their current state. All services should report as running within a few minutes of configuration completing.

!!! tip "Cassandra Startup Time"
    The Cassandra database may take 2–5 minutes to fully initialize on first boot. Other services will wait for Cassandra before becoming available.

## Next Steps

- [Choose a deployment role](deployment-roles.md) if you haven't already
- [Walk through the configure wizard](wfa-configure.md) in detail
- [Complete first login and onboarding](first-login.md)
- [Understand the architecture](architecture.md)

---

!!! note "For Developers"
    This guide covers production deployment via WitFoo Appliances. If you are a developer working on WitFoo Analytics itself, see the **Deployment** section of the documentation for Docker Compose development workflows.