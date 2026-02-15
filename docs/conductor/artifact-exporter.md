# Artifact Exporter

The Artifact Exporter delivers finalized artifacts from the `artifacts.final` NATS stream to one or more external destinations. Each export destination runs as an independent connector with its own batching, retry, and formatting logic.

## Export Destinations

### WitFoo Analytics (Reporter)

Exports artifacts to WitFoo Analytics using HMAC-SHA256 authenticated HTTP POST requests. This is the primary export path for organizations using the full WitFoo platform.

| Setting | Description |
|---------|-------------|
| Analytics URL | WitFoo Analytics endpoint |
| Shared Secret | HMAC-SHA256 authentication key |

### Splunk HEC

Exports to Splunk via the HTTP Event Collector protocol.

| Setting | Description |
|---------|-------------|
| URL | Splunk HEC endpoint |
| Token | HEC authentication token |
| Index | Target Splunk index |
| Source Type | Splunk source type for events |

### OpenSearch

Exports to OpenSearch using the bulk indexing API.

| Setting | Description |
|---------|-------------|
| URL | OpenSearch cluster endpoint |
| Index | Target index name |
| Auth Mode | `basic` (username/password), `apikey`, or `none` |

### Microsoft Sentinel

Exports to Microsoft Sentinel via the Log Analytics Data Collector API.

| Setting | Description |
|---------|-------------|
| Workspace ID | Log Analytics workspace identifier |
| Shared Key | Primary or secondary workspace key |

### AlienVault

Exports to AlienVault USM/OSSIM.

| Setting | Description |
|---------|-------------|
| Server URL | AlienVault server endpoint |
| API Key | Authentication key |

### SCP Transfer

Exports artifacts as files transferred via SCP to a remote server.

| Setting | Description |
|---------|-------------|
| Host | Remote server hostname or IP |
| Path | Remote directory path |
| Credentials | SSH key or password authentication |
| Row Limits | Maximum rows per file |

### UDP Syslog

Exports artifacts as syslog messages over UDP.

| Setting | Description |
|---------|-------------|
| Host | Destination syslog server |
| Port | UDP port number |

### Local FileSystem

Writes artifacts to files on the local filesystem.

| Setting | Description |
|---------|-------------|
| Output Directory | Path for output files |

## Configuration

All exporters are configured via the NATS KV `EXPORTERS` bucket and managed through the [Conductor UI Exporter Configuration page](ui/exporters.md).

Each exporter supports:

- **Enable/disable toggle** — Activate or deactivate individual exporters
- **Batch size** — Number of artifacts per batch (where applicable)
- **Retry settings** — Automatic retry with backoff on transient failures
- **STIX enrichment toggle** — Enable threat intelligence enrichment before export

## Metrics

Each exporter connector exposes pipeline metrics:

| Metric | Description |
|--------|-------------|
| `pipeline_messages_consumed_total` | Artifacts consumed from `artifacts.final` |
| `pipeline_messages_published_total` | Artifacts successfully exported |
| `pipeline_errors_total` | Export failures |