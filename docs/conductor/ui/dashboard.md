# Dashboard

**URL:** `/`

The Dashboard provides real-time visibility into the Conductor pipeline through four tabs. All metrics update in real time via WebSocket connection, with automatic fallback to HTTP polling at 5-second intervals.

## Overview Tab

The Overview tab displays system-level health indicators:

- **Host Gauges** — CPU core count, memory usage percentage, and disk usage percentage
- **Message Throughput** — Counters showing messages processed per pipeline stage
- **Pipeline Stage Health** — Status indicators for each stage (ingestion, parsing, filtering, export)

## Pipeline Tab

The Pipeline tab provides detailed pipeline performance metrics:

- **Time-Series Charts** — Visualizations of `pipeline_stage_count` metrics over time
- **Message Flow** — Real-time message flow through the pipeline
- **Stage Filters** — Filter views by pipeline stage:
    - `source_client` — Ingestion stage
    - `broker` — Message broker
    - `filter` — Artifact filtering
    - `export` — Export stage

## Service Status Tab

The Service Status tab shows the health of each Conductor service:

- **Per-Service Health** — Status derived from WFA report events
- **Error Indicators** — Warning and error counts per service
- **Service Uptime** — Time since last restart

## Container Status Tab

The Container Status tab displays Docker container metrics:

- **Per-Container CPU Usage** — CPU utilization percentage for each container
- **Per-Container Memory Usage** — Memory consumption for each container
- **Container Uptime** — How long each container has been running
- **Container State** — Running, stopped, or restarting status

## WebSocket Connection

A pulsating dot indicator shows the real-time connection status. When the WebSocket connection drops, the UI automatically falls back to HTTP polling at 5-second intervals and attempts to re-establish the WebSocket connection.