# Getting Started

Welcome to WitFoo Analytics v1.0.0 — an enterprise security operations platform that ingests security artifacts, builds knowledge graphs, detects incidents, and generates compliance reports for your organization.

This guide walks you through deploying WitFoo Analytics for the first time using a WitFoo Appliance.

## Quick Start

Follow these three steps to get up and running:

1. **[Install a WitFoo Appliance](installation.md)** — Deploy a VM image, launch from a cloud marketplace, or run the bare metal installer.
2. **[First Login](first-login.md)** — Access the web UI, change default credentials, and complete the setup wizard.
3. **[Understand the Architecture](architecture.md)** — Learn how services communicate and how data flows through the platform.

## Planning Your Deployment

Before you begin, review the **[Deployment Roles](deployment-roles.md)** page to understand the available appliance roles and choose the right topology for your environment.

| Deployment Size | Recommended Topology |
|----------------|----------------------|
| Small / Evaluation | Precinct All-In-One (single node) |
| Medium | Conductor + Reporter + Console |
| Large / Enterprise | Precinct with dedicated Data Nodes and Streamer Nodes |

## Hardware at a Glance

| Tier | CPU Cores | RAM | Disk |
|------|-----------|-----|------|
| Minimum | 8 | 12 GB | 220 GB |
| Recommended | 16 | 32 GB | 1 TB |

Per-role requirements are detailed on the [Deployment Roles](deployment-roles.md) page.

## Prerequisites

- A supported hypervisor (VMware, Hyper-V, QEMU), cloud account (AWS, Azure, Google Cloud), or a bare metal server running Ubuntu 24 or RHEL 10
- Network access to the appliance on HTTPS port **443**
- An SSH client for initial configuration

!!! tip "Need help?"
    Visit the [WitFoo Community](https://community.witfoo.com) or contact WitFoo Support for assistance with your deployment.