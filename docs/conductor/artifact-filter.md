# Artifact Filter

The Artifact Filter is the quality gate between parsing and export. It deduplicates redundant events, optionally enriches artifacts with threat intelligence, and applies predicate-based filter rules before publishing export-ready artifacts.

## Pipeline

The filter implements a three-stage processing pipeline:

```
artifacts.parsed → Deduplication → STIX Enrichment → Predicate Filter → artifacts.final
```

### Stage 1: ProtoGraph Deduplication

ProtoGraph reduces noise by hashing artifacts using an 11-tuple key. Duplicate artifacts within a configurable sliding window are collapsed into a single event with a count.

| Category | Fields |
|----------|--------|
| **Host** | SenderHost |
| **Network** | ClientIP, ServerIP, ServerPort, Protocol |
| **Identity** | UserName |
| **Content** | FileName, StreamName, MessageType, Action |
| **Severity** | SeverityLabel |

For example, 1000 identical SSH login failure events from the same source within the deduplication window produce a single artifact with a count of 1000.

!!! tip
    High compression ratios (>5x) indicate effective deduplication. For every 8 raw syslog messages, approximately 1 artifact is exported in typical deployments.

### Stage 2: STIX Enrichment (Optional)

When enabled, the STIX enrichment stage checks artifact fields (IPs, domains, file hashes) against configured threat intelligence feeds. Matched indicators are added as metadata to the artifact before it continues through the pipeline.

Enriched artifacts are published to the `artifacts.enriched` subject and re-consumed by the filter for predicate processing.

### Stage 3: Predicate Filtering

Predicate filters apply rule-based inclusion and exclusion logic:

- **Field matching** — Include or exclude based on specific field values
- **Regex patterns** — Pattern matching on artifact content
- **Severity thresholds** — Filter by severity level
- **Stream-based rules** — Filter specific log sources

When no filter rules are configured, all artifacts pass through to `artifacts.final`.

## Configuration

The Artifact Filter is configured via the NATS KV `FILTERS` bucket. Configuration includes:

- Deduplication window duration (default: 10 minutes)
- STIX enrichment enable/disable and feed URL
- Predicate filter rules

Configuration is managed through the [Conductor UI Exporter page](ui/exporters.md) (STIX toggle) and directly via the NATS KV bucket for advanced predicate rules.

## Metrics

| Metric | Description |
|--------|-------------|
| `pipeline_messages_consumed_total` | Artifacts consumed from `artifacts.parsed` |
| `pipeline_messages_published_total` | Artifacts published to `artifacts.final` |
| `pipeline_messages_rejected_total` | Artifacts rejected by predicate filters |
| `pipeline_errors_total` | Processing errors |