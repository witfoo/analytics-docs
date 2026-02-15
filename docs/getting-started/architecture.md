# Architecture

WitFoo Analytics uses a distributed, containerized architecture where each node role runs a specific set of services. This page describes the service architecture, inter-node communication, and data flow.

## Deployment Topology

A complete WitFoo Analytics deployment consists of up to three node roles working together:

```mermaid
graph TB
    subgraph "Data Sources"
        DS1[Firewalls]
        DS2[IDS/IPS]
        DS3[Endpoints]
        DS4[Cloud Services]
    end

    subgraph "Conductor Node"
        NATS_B[NATS Broker]
        SS[Signal Server]
        SP[Signal Parser]
        AE[Artifact Exporter]
        BE[Broker Edge]
    end

    subgraph "Analytics Node"
        RP[Reverse Proxy<br/>Port 443]
        UI[Web UI]
        API[API Service]
        IE[Incident Engine]
        GP[Graph Processor]
        AI_SVC[Artifact Ingestion]
        DISP[Dispatcher]
        NATS_A[NATS]
        CASS[(Cassandra)]
        PROM[Prometheus]
        GRAF[Grafana]
    end

    subgraph "Console Node"
        CON_UI[Console UI<br/>Port 443]
    end

    DS1 & DS2 & DS3 & DS4 -->|Signals| NATS_B
    NATS_B --> SS --> SP --> AE
    AE -->|Artifacts| NATS_A

    NATS_A --> AI_SVC --> GP --> CASS
    GP --> IE --> CASS
    IE --> DISP
    API --> CASS
    RP --> UI
    RP --> API
    PROM --> GRAF

    CON_UI -.->|Manages| NATS_B
    CON_UI -.->|Manages| RP
```

## Service Architecture — Analytics Node

The Analytics node is the primary platform, running all services required for investigation, correlation, and reporting.

```mermaid
graph LR
    subgraph "External Access"
        Browser[Web Browser]
    end

    subgraph "Edge Layer"
        RP[Reverse Proxy<br/>:443 HTTPS]
    end

    subgraph "Presentation Layer"
        UI[Web UI<br/>:3000]
        API[API Service<br/>:8080]
    end

    subgraph "Processing Layer"
        IE[Incident Engine<br/>:8082]
        GP[Graph Processor]
        AI_SVC[Artifact Ingestion<br/>:8081]
        DISP[Dispatcher<br/>:8083]
    end

    subgraph "Messaging Layer"
        NATS[NATS<br/>:4222]
    end

    subgraph "Storage Layer"
        CASS[(Cassandra<br/>:9042)]
    end

    subgraph "Observability"
        PROM[Prometheus<br/>:9090]
        GRAF[Grafana<br/>:3001]
    end

    Browser -->|HTTPS :443| RP
    RP --> UI
    RP --> API
    API --> IE
    API --> CASS
    IE --> CASS
    IE --> NATS
    GP --> CASS
    GP --> NATS
    AI_SVC --> NATS
    AI_SVC --> GP
    DISP --> NATS
    PROM --> GRAF
    PROM -.->|Scrape| API
    PROM -.->|Scrape| IE
    PROM -.->|Scrape| GP
```

### Analytics Services

| Service | Port | Description |
|---------|------|-------------|
| Reverse Proxy | 443 | TLS termination, routes requests to UI and API |
| Web UI | 3000 | Svelte-based user interface |
| API Service | 8080 | REST API, authentication, RBAC |
| Incident Engine | 8082 | Incident correlation, scoring, status management |
| Graph Processor | — | Builds and maintains the security knowledge graph |
| Artifact Ingestion | 8081 | Receives and normalizes incoming artifacts |
| Dispatcher | 8083 | WebSocket notifications and real-time event delivery |
| NATS | 4222 | Internal message bus for service communication |
| Cassandra | 9042 | Primary data store for all analytics data |
| Prometheus | 9090 | Metrics collection (bound to localhost) |
| Grafana | 3001 | Metrics visualization dashboards |

## Service Architecture — Conductor Node

The Conductor node handles data ingestion from remote networks and forwards processed signals to the Analytics node.

```mermaid
graph LR
    subgraph "Data Sources"
        SRC[Syslog / API / Agents]
    end

    subgraph "Conductor Services"
        NATS_B[NATS Broker<br/>:4223 client<br/>:4443 leaf]
        SS[Signal Server]
        SP[Signal Parser]
        AE[Artifact Exporter]
        BE[Broker Edge]
    end

    subgraph "Analytics Node"
        NATS_A[NATS :4222]
    end

    SRC -->|Signals| NATS_B
    NATS_B --> SS
    SS --> SP
    SP --> AE
    AE -->|Leaf Connection :4443| NATS_A
    BE --> NATS_B
```

### Conductor Services

| Service | Port | Description |
|---------|------|-------------|
| NATS Broker | 4223 (client), 4443 (leaf) | Message broker for signal ingestion and forwarding |
| Signal Server | — | Receives raw signals from data sources |
| Signal Parser | — | Parses and normalizes signals into structured artifacts |
| Artifact Exporter | — | Forwards processed artifacts to the Analytics node |
| Broker Edge | — | Manages broker cluster connectivity |

## Service Architecture — Console Node

The Console node is a lightweight management interface for monitoring and configuring remote Conductor and Analytics nodes.

```mermaid
graph LR
    subgraph "Admin Browser"
        Browser[Web Browser]
    end

    subgraph "Console Services"
        CON[Console Container<br/>:443 HTTPS]
    end

    subgraph "Managed Nodes"
        C1[Conductor 1]
        C2[Conductor 2]
        A1[Analytics 1]
    end

    Browser -->|HTTPS :443| CON
    CON -.->|Management API| C1
    CON -.->|Management API| C2
    CON -.->|Management API| A1
```

### Console Services

| Service | Port | Description |
|---------|------|-------------|
| Console | 443 | Single-container management UI and API |

## Data Flow

The following diagram shows how security data flows from ingestion to investigation:

```mermaid
flowchart TD
    A[Data Sources<br/>Firewalls, IDS, Endpoints] -->|Raw Signals| B[Conductor<br/>NATS Broker]
    B -->|Parsed Signals| C[Signal Parser]
    C -->|Normalized Artifacts| D[Artifact Exporter]
    D -->|NATS Leaf Connection| E[Analytics<br/>Artifact Ingestion]
    E -->|Structured Artifacts| F[Graph Processor]
    F -->|Nodes & Edges| G[(Cassandra<br/>Knowledge Graph)]
    F -->|Events| H[Incident Engine]
    H -->|Correlated Incidents| G
    H -->|Notifications| I[Dispatcher]
    I -->|WebSocket| J[Web UI]
    G -->|Query Results| K[API Service]
    K -->|REST API| J
    J -->|HTTPS :443| L[Analyst Browser]

    style A fill:#f9f,stroke:#333
    style G fill:#bbf,stroke:#333
    style L fill:#bfb,stroke:#333
```

### Data Flow Summary

1. **Ingestion** — Data sources send raw signals (syslog, API, agents) to the Conductor's NATS broker.
2. **Parsing** — The Signal Server and Signal Parser normalize raw signals into structured artifacts.
3. **Export** — The Artifact Exporter forwards normalized artifacts to the Analytics node via a NATS leaf connection.
4. **Processing** — Artifact Ingestion receives artifacts and passes them to the Graph Processor, which builds a security knowledge graph in Cassandra.
5. **Correlation** — The Incident Engine analyzes graph data to detect, score, and correlate security incidents.
6. **Notification** — The Dispatcher delivers real-time updates to connected web UI sessions via WebSocket.
7. **Investigation** — Analysts access the platform through the web UI (HTTPS on port 443), querying the API for incidents, graph data, and reports.

## Network Ports

| Port | Protocol | Service | Direction | Description |
|------|----------|---------|-----------|-------------|
| 443 | HTTPS | Reverse Proxy / Console | Inbound | Web UI and API access |
| 4223 | TCP | NATS Broker (Conductor) | Inbound | Signal ingestion from data sources |
| 4443 | TCP | NATS Broker (Conductor) | Inbound/Outbound | Leaf node connections to Analytics |
| 9042 | TCP | Cassandra | Internal | Database communication (not exposed externally) |
| 4222 | TCP | NATS (Analytics) | Internal | Internal message bus |

!!! tip "Minimal Firewall Configuration"
    For a single Analytics node deployment, only port **443** needs to be open to users. Ports 4223 and 4443 are only required when deploying Conductor nodes for remote data collection.