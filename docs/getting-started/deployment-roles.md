# Deployment Roles

WitFoo Appliances support three node roles, each designed for a specific function within your security operations infrastructure. This page helps you understand each role and choose the right deployment topology.

## Role Overview

| Role | Purpose | Typical Deployment |
|------|---------|-------------------|
| **Conductor** | Data ingestion and signal processing | Remote offices, network segments, cloud VPCs |
| **Console** | Centralized management and monitoring | Headquarters or management network |
| **Analytics** | Security analytics, investigation, and reporting | SOC or data center |

## Analytics

The Analytics node is the primary WitFoo platform. It performs security investigation, incident correlation, compliance reporting, and provides the main user interface for security analysts.

### Purpose and Use Case

- Core security operations platform for your SOC
- Receives processed artifacts from Conductor nodes (or ingests directly)
- Correlates events into incidents using the knowledge graph and incident engine
- Generates compliance reports, executive summaries, and operational metrics
- Provides the web UI for analysts, investigators, and management

### Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 8 cores | 16 cores |
| RAM | 12 GB | 32 GB |
| Disk | 220 GB | 1 TB |

### Services

The Analytics node runs the full service stack:

| Service | Description |
|---------|-------------|
| Cassandra | Primary data store and knowledge graph |
| NATS | Internal message bus |
| Artifact Ingestion | Receives and normalizes artifacts |
| Graph Processor | Builds the security knowledge graph |
| Incident Engine | Correlates events into scored incidents |
| API Service | REST API with authentication and RBAC |
| Dispatcher | Real-time WebSocket notifications |
| Reverse Proxy | TLS termination and request routing |
| Web UI | Analyst-facing user interface |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |

### When to Choose Analytics

- **Always** — Every WitFoo deployment requires at least one Analytics node
- You need a single-node deployment for evaluation or small environments
- You are building a SOC and need investigation, correlation, and reporting capabilities

!!! tip "Start Here"
    If you're deploying WitFoo for the first time, start with a single Analytics node. You can add Conductor and Console nodes later as your deployment grows.

## Conductor

The Conductor node handles data ingestion and signal processing. It collects signals from data sources, parses them into structured artifacts, and forwards them to the Analytics node for analysis.

### Purpose and Use Case

- Deployed at the network edge or in remote locations where data sources reside
- Collects syslog, API feeds, and agent data from firewalls, IDS/IPS, endpoints, and cloud services
- Parses and normalizes raw signals before forwarding to Analytics
- Reduces bandwidth by processing data locally and sending only structured artifacts

### Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 220 GB | 500 GB |

### Services

| Service | Description |
|---------|-------------|
| NATS Broker | Message broker for signal ingestion (ports 4223, 4443) |
| Signal Server | Receives raw signals from data sources |
| Signal Parser | Parses and normalizes signals into artifacts |
| Artifact Exporter | Forwards processed artifacts to Analytics via NATS leaf |
| Broker Edge | Manages broker cluster connectivity |

### When to Choose Conductor

- You have data sources in remote offices, branch locations, or separate network segments
- You want to process and filter data locally before sending it to Analytics
- You need to collect data from cloud VPCs (AWS, Azure, Google Cloud)
- You want to reduce WAN bandwidth usage between sites

!!! tip "Multiple Conductors"
    Deploy one Conductor per network segment or remote location. All Conductors forward their processed artifacts to a central Analytics node.

## Console

The Console node provides a centralized management and monitoring interface for your entire WitFoo deployment. It is a lightweight, single-container deployment.

### Purpose and Use Case

- Centralized dashboard for monitoring the health and status of all Conductor and Analytics nodes
- Remote configuration and management of appliances
- Deployment oversight for multi-site environments

### Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 4 cores |
| RAM | 8 GB | 8 GB |
| Disk | 220 GB | 220 GB |

### Services

| Service | Description |
|---------|-------------|
| Console | Single container providing management UI and API (port 443) |

### When to Choose Console

- You manage multiple Conductor and/or Analytics nodes across different sites
- You need centralized visibility into appliance health and configuration
- You want a single pane of glass for deployment management

!!! tip "Console Is Optional"
    The Console node is not required for single-site deployments. A single Analytics node (or Analytics + Conductor) works without a Console. Add a Console when you manage three or more appliances.

## Deployment Topologies

### Single Node (Evaluation / Small)

Deploy a single **Analytics** node for evaluation, lab environments, or small organizations.

```
[Data Sources] → [Analytics]
```

- Simplest deployment
- All ingestion and analysis on one node
- Recommended hardware: 16 CPU, 32 GB RAM, 1 TB disk

### Two Nodes (Small / Medium)

Deploy a **Conductor** for data collection and an **Analytics** node for analysis.

```
[Data Sources] → [Conductor] → [Analytics]
```

- Separates ingestion from analysis
- Conductor can be placed in a DMZ or remote network
- Analytics node is dedicated to processing and UI

### Multi-Site (Enterprise)

Deploy **Conductors** at each site, a central **Analytics** node, and a **Console** for management.

```
[Site A Sources] → [Conductor A] ──┐
[Site B Sources] → [Conductor B] ──┤→ [Analytics] ← [Console]
[Cloud Sources]  → [Conductor C] ──┘
```

- Conductors at each remote site or cloud VPC
- Central Analytics node for correlation and reporting
- Console for centralized management of all nodes

## Hardware Summary

| Role | CPU (min) | RAM (min) | Disk (min) |
|------|-----------|-----------|------------|
| Conductor | 4 | 8 GB | 220 GB |
| Console | 4 | 8 GB | 220 GB |
| Analytics | 8 | 12 GB | 220 GB |

!!! tip "Right-Sizing Your Deployment"
    Start with the minimum requirements and scale up based on data volume. Monitor resource usage from the **Admin > Health** dashboard (Analytics) or Grafana (if local metrics are enabled on Conductor). The recommended specs for Analytics (16 CPU, 32 GB RAM, 1 TB disk) support most production workloads.