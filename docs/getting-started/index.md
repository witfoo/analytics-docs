# Getting Started

Welcome to WitFoo Analytics v1.0.0 — an enterprise security operations platform for investigation, correlation, and reporting. This guide walks you through deploying your first WitFoo Appliance and completing initial configuration.

## Quick Start Path

Follow these steps to go from zero to a running WitFoo Analytics instance:

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **1. Install a WitFoo Appliance**

    ---

    Deploy a WitFoo Appliance via VM image, cloud marketplace, or bare metal script.

    [:octicons-arrow-right-24: Installation](installation.md)

-   :material-server-network:{ .lg .middle } **2. Choose a Deployment Role**

    ---

    Understand the three node roles: Conductor, Console, and Analytics.

    [:octicons-arrow-right-24: Deployment Roles](deployment-roles.md)

-   :material-cog:{ .lg .middle } **3. Configure the Appliance**

    ---

    Run `sudo wfa configure` to select a role and configure services.

    [:octicons-arrow-right-24: WFA Configure Wizard](wfa-configure.md)

-   :material-login:{ .lg .middle } **4. Log In and Onboard**

    ---

    Access the web UI, change default passwords, and complete the onboarding wizard.

    [:octicons-arrow-right-24: First Login](first-login.md)

-   :material-sitemap:{ .lg .middle } **5. Understand the Architecture**

    ---

    Learn how services, data, and nodes work together.

    [:octicons-arrow-right-24: Architecture](architecture.md)

</div>

## Hardware Requirements at a Glance

| Tier | CPU Cores | RAM | Disk |
|------|-----------|-----|------|
| **Minimum** | 8 | 12 GB | 220 GB |
| **Recommended** | 16 | 32 GB | 1 TB |

See [Deployment Roles](deployment-roles.md) for per-role hardware requirements.

## What You'll Need

Before you begin, ensure you have:

- A supported hypervisor (VMware, Hyper-V, QEMU), cloud account (AWS, Azure, Google Cloud), or bare metal server running Ubuntu 24 or RHEL 10
- Network access to the appliance on port **443** (HTTPS)
- A WitFoo license key (or request a 15-day trial during configuration)

!!! tip "Evaluation Deployments"
    For evaluation purposes, a single **Analytics** node is the fastest path to a working platform. You can add Conductor and Console nodes later as your deployment grows.