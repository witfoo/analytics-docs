# Deployment Roles

WitFoo Analytics supports multiple deployment roles, allowing you to scale from a single all-in-one appliance to a distributed multi-node architecture. Each role runs a specific subset of services tailored to its function.

## Role Overview

| Role | Description |
|------|-------------|
| **Conductor** | Signal collection and forwarding — receives data from network sensors and endpoints |
| **Reporter** | Analytics processing — incident detection, reporting, and compliance scoring |
| **Console** | Web UI and API gateway — serves the user interface and proxies API requests |
| **Precinct All-In-One** | All services on a single node — Conductor, Reporter, and Console combined |
| **Precinct Data Node** | Dedicated Cassandra storage node for clustered deployments |
| **Precinct Streamer Node** | Dedicated artifact ingestion and graph processing node |
| **Precinct Mgmt Node** | Management and orchestration node for multi-node Precinct deployments |

## Hardware Requirements by Role

| Role | CPU Cores | RAM | Recommended Disk |
|------|-----------|-----|-----------------|
| Conductor | 4 | 8 GB | 220 GB |
| Reporter | 8 | 32 GB | 1 TB |
| Console | 4 | 8 GB | 220 GB |
| Precinct All-In-One | 8 | 32 GB | 1 TB |
| Precinct Data Node | 4 | 12 GB | 1 TB+ |
| Precinct Streamer Node | 4 | 12 GB | 500 GB |
| Precinct Mgmt Node | 4 | 8 GB | 220 GB |

!!! tip "Disk Sizing"
    Disk requirements depend heavily on log volume and retention periods. The values above are starting points. For environments ingesting more than 10,000 events per second, increase disk allocation on Data Nodes and Streamer Nodes accordingly.

## Role Details

### Conductor

The Conductor collects signals from network sensors, endpoints, and external feeds, then forwards parsed artifacts to the Analytics pipeline.

**Services included:**

- broker-edge
- signal-server
- signal-parser
- artifact-exporter

**When to use:** Deploy a dedicated Conductor when you need to separate signal collection from analytics processing, or when collecting from multiple network segments.

---

### Reporter

The Reporter handles the core analytics workload — incident detection, correlation, compliance scoring, and report generation.

**Services included:**

- Cassandra
- NATS
- incident-engine
- graph-processor
- artifact-ingestion
- Prometheus
- Grafana

**When to use:** Deploy a dedicated Reporter when you want to isolate compute-intensive analytics processing from the user-facing Console.

---

### Console

The Console serves the web UI and API gateway. It proxies requests to the Reporter and provides the user interface for security analysts.

**Services included:**

- reverse-proxy
- ui
- api
- dispatcher

**When to use:** Deploy a dedicated Console when you want to separate the user-facing web tier from backend processing, or when multiple analysts need a responsive UI independent of analytics load.

---

### Precinct All-In-One

The Precinct All-In-One (AIO) combines all services — Conductor, Reporter, and Console — on a single node. This is the simplest deployment topology.

**Services included:**

- All Conductor services (broker-edge, signal-server, signal-parser, artifact-exporter)
- All Reporter services (Cassandra, NATS, incident-engine, graph-processor, artifact-ingestion)
- All Console services (reverse-proxy, ui, api, dispatcher)
- Prometheus, Grafana

**When to use:** Small environments, proof-of-concept deployments, or evaluation installations where simplicity is preferred over scalability.

---

### Precinct Data Node

A dedicated Cassandra storage node for horizontally scaling database capacity in clustered deployments.

**Services included:**

- Cassandra (clustered mode)

**When to use:** Deploy one or more Data Nodes when your data volume exceeds what a single node can store, or when you need storage redundancy and high availability.

**Clustering configuration:**

During `wfa configure`, you will be prompted for:

- **Seed nodes** — IP addresses of other Data Nodes in the cluster
- **Listen address** — This node's IP address for inter-node communication
- **Data center name** — Logical data center identifier (default: `dc1`)

---

### Precinct Streamer Node

A dedicated node for artifact ingestion and graph processing. Streamer Nodes handle the high-throughput data pipeline, offloading this work from the Reporter.

**Services included:**

- artifact-ingestion
- graph-processor
- NATS

**When to use:** Deploy Streamer Nodes when ingestion volume is high and you want to scale the processing pipeline independently of incident analysis and reporting.

---

### Precinct Mgmt Node

The management node provides orchestration and monitoring for multi-node Precinct deployments.

**Services included:**

- Prometheus
- Grafana
- Management API

**When to use:** Deploy a Mgmt Node in large distributed environments to centralize monitoring and management of all Precinct nodes.

---

## Deployment Topologies

### Single Node (Evaluation)

The simplest deployment — a single Precinct All-In-One node:

```
┌─────────────────────────┐
│   Precinct All-In-One   │
│  (All services on one   │
│        node)            │
└─────────────────────────┘
```

**Best for:** Evaluation, small teams, low log volume.

### Three-Node (Small Production)

Separate Conductor, Reporter, and Console for better resource isolation:

```
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Conductor  │──▶│  Reporter   │◀──│   Console   │
│  (Signals)  │   │ (Analytics) │   │   (Web UI)  │
└────────────┘   └────────────┘   └────────────┘
```

**Best for:** Medium environments, 1,000–10,000 EPS.

### Clustered (Enterprise)

A fully distributed deployment with dedicated storage, processing, and management nodes:

```
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Conductor  │   │  Conductor  │   │   Console   │
│   Node 1    │   │   Node 2    │   │             │
└──────┬─────┘   └──────┬─────┘   └──────┬─────┘
       │                │                 │
       ▼                ▼                 ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Streamer   │   │  Streamer   │   │  Mgmt Node  │
│   Node 1    │   │   Node 2    │   │ (Monitoring) │
└──────┬─────┘   └──────┬─────┘   └─────────────┘
       │                │
       ▼                ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Data Node  │   │  Data Node  │   │  Data Node  │
│     1       │   │     2       │   │     3       │
└────────────┘   └────────────┘   └────────────┘
```

**Best for:** Large enterprises, 10,000+ EPS, high availability requirements.

## Selecting a Role

When you run `sudo wfa configure`, the wizard presents the available roles. Use the following decision guide:

1. **Starting out or evaluating?** → **Precinct All-In-One**
2. **Need to separate signal collection?** → Add a dedicated **Conductor**
3. **Heavy analytics workload?** → Dedicated **Reporter** + **Console**
4. **High data volume?** → Add **Data Nodes** for storage scaling
5. **High ingestion rate?** → Add **Streamer Nodes** for pipeline scaling
6. **Multi-node monitoring?** → Add a **Mgmt Node**

!!! tip "Start Simple, Scale Later"
    Begin with a Precinct All-In-One deployment. You can migrate to a distributed topology later by adding dedicated nodes and reconfiguring roles with `sudo wfa configure`.