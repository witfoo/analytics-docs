# Installation

WitFoo Analytics is deployed as a **WitFoo Appliance (WFA)** — a purpose-built system image that includes the operating system, container runtime, and all required services. The installation process has three steps:

1. Deploy a WitFoo Appliance
2. Run the configuration wizard
3. Access the web UI

## Prerequisites

- Network connectivity and a static IP address (recommended)
- DNS record pointing to the appliance IP (optional but recommended for TLS)
- SSH client for initial access

## Hardware Requirements

| Tier | CPU Cores | RAM | Disk |
|------|-----------|-----|------|
| Minimum | 8 | 12 GB | 220 GB |
| Recommended | 16 | 32 GB | 1 TB |

See [Deployment Roles](deployment-roles.md) for per-role hardware specifications.

---

## Step 1: Deploy a WitFoo Appliance

Choose one of the three deployment methods below. All appliance images and scripts are available from the [witfoo-appliances](https://github.com/witfoo/witfoo-appliances) repository.

### Option A: On-Premises VM Image

Pre-built Ubuntu 24 virtual machine images are available for the following hypervisors:

| Hypervisor | Image Format |
|-----------|--------------|
| VMware vSphere / ESXi | OVA |
| Microsoft Hyper-V | VHDX |
| QEMU / KVM | QCOW2 |

1. Download the appropriate image from the [witfoo-appliances releases](https://github.com/witfoo/witfoo-appliances/releases).
2. Import the image into your hypervisor.
3. Allocate CPU, RAM, and disk according to the [hardware requirements](#hardware-requirements).
4. Boot the virtual machine.
5. Connect via SSH using the default credentials (see below).

### Option B: Cloud Marketplace

WitFoo Appliance images are available on the following cloud marketplaces:

| Cloud Provider | Marketplace Listing |
|---------------|-------------------|
| AWS | AWS Marketplace — search "WitFoo" |
| Microsoft Azure | Azure Marketplace — search "WitFoo" |
| Google Cloud | Google Cloud Marketplace — search "WitFoo" |

1. Navigate to your cloud provider's marketplace and search for **WitFoo**.
2. Launch the appliance image, selecting an instance size that meets the [hardware requirements](#hardware-requirements).
3. Ensure the security group or firewall allows inbound traffic on **port 443** (HTTPS) and **port 22** (SSH).
4. Connect via SSH using the default credentials.

### Option C: Bare Metal Installation

For bare metal servers, use the provided installation scripts:

| Operating System | Script |
|-----------------|--------|
| Ubuntu 24 | `ubuntu-install.sh` |
| RHEL 10 | `rhel-install.sh` |

1. Start with a fresh installation of Ubuntu 24 or RHEL 10.
2. Clone the appliance repository:

    ```bash
    git clone https://github.com/witfoo/witfoo-appliances.git
    cd witfoo-appliances
    ```

3. Run the appropriate installation script:

    ```bash
    # Ubuntu 24
    sudo bash ubuntu-install.sh

    # RHEL 10
    sudo bash rhel-install.sh
    ```

4. The script installs all dependencies, the container runtime, and the WFA management daemon.

!!! danger "Default SSH Credentials"
    All WitFoo Appliances ship with the following default SSH credentials:

    - **Username:** `witfooadmin`
    - **Password:** `F00theN0ise!`

    **Change this password immediately** after your first SSH connection:

    ```bash
    passwd witfooadmin
    ```

---

## Step 2: Configure the Appliance

Once the appliance is running, SSH into the system and launch the interactive configuration wizard:

```bash
sudo wfa configure
```

The wizard prompts you to:

1. **Select the appliance role** — Choose the deployment role for this node (e.g., Precinct All-In-One, Conductor, Reporter). See [Deployment Roles](deployment-roles.md) for guidance.
2. **Configure networking** — Set the node IP address and hostname.
3. **Set data retention** — Define how long artifacts, work units, and reports are retained.
4. **Configure clustering** — If deploying Data Nodes or Streamer Nodes, provide seed node addresses.

The wizard generates configuration files at `/witfoo/configs/node.json` and `/witfoo/configs/analytics.json`, then pulls container images and starts all services for the selected role.

!!! tip "Validate the installation"
    After configuration completes, check the status of all services:

    ```bash
    sudo wfa analytics status
    ```

    All services should report a **running** state.

---

## Step 3: Access the Web UI

1. Open a web browser and navigate to:

    ```
    https://<appliance-ip-or-hostname>
    ```

    The web UI is served over **HTTPS on port 443**.

2. Log in with the default web UI credentials and complete the setup wizard. See [First Login](first-login.md) for details.

!!! danger "TLS Certificate"
    The appliance ships with a self-signed TLS certificate. Your browser will display a security warning on first access. For production deployments, replace the self-signed certificate with a certificate from your organization's certificate authority.

---

## For Developers

The installation steps above are for **production deployments** using the WitFoo Appliance. If you are a developer working on WitFoo Analytics, Docker Compose templates are available for local development environments. See the [Deployment](../deployment/index.md) section for Docker Compose setup instructions.