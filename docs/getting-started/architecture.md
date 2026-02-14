# Architecture

WitFoo Analytics is a microservices-based platform built on Go, SvelteKit, Cassandra, and NATS.

## Service Architecture

```mermaid
graph LR
    Browser["Browser"] --> RP["Reverse Proxy<br/>:8080"]
    RP --> API["API Service<br/>:8090"]
    RP --> UI["UI Service<br/>:5173"]
    RP --> CUI["Conductor UI<br/>:3000"]
    API --> IE["Incident Engine<br/>:8082"]
    IE --> Cassandra["Cassandra<br/>:9042"]
    IE --> NATS["NATS<br/>:4222"]
    AI["Artifact Ingestion<br/>:8003"] --> NATS
    NATS --> GP["Graph Processor"]
    NATS --> Dispatcher["Dispatcher"]
    GP --> Cassandra
    Dispatcher --> Cassandra
```

## Services

| Service | Port | Description |
| --- | --- | --- |
| Reverse Proxy | 8080 | Routes browser requests to API, UI, and Conductor UI |
| API | 8090 | REST API gateway — proxies to Incident Engine |
| Incident Engine | 8082 | Core business logic, domain operations, Cassandra access |
| UI | 5173 | SvelteKit frontend with Carbon Components |
| Artifact Ingestion | 8003 | Receives security artifacts via HTTP, publishes to NATS |
| Graph Processor | — | Consumes NATS events, builds node/edge graph in Cassandra |
| Dispatcher | — | Processes NATS events for incident correlation |
| Cassandra | 9042 | Primary data store |
| NATS | 4222 | Message broker for event-driven processing |

## Data Flow

```mermaid
sequenceDiagram
    participant Source as Security Source
    participant AI as Artifact Ingestion
    participant NATS as NATS Broker
    participant GP as Graph Processor
    participant D as Dispatcher
    participant IE as Incident Engine
    participant C as Cassandra

    Source->>AI: POST /v1/artifacts
    AI->>NATS: Publish artifact event
    NATS->>GP: Consume → build graph
    GP->>C: Write nodes/edges
    NATS->>D: Consume → correlate
    D->>IE: Create/update incidents
    IE->>C: Write incidents
```

!!! info "Coming Soon"
    Detailed architecture documentation including deployment topologies,
    scaling patterns, and high-availability configuration will be
    auto-generated from the WitFoo Analytics codebase on the next release.
