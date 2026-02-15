# Exporter Configuration

**URL:** `/admin/settings/artifact-exporters`

The Exporter Configuration page manages the destinations where processed artifacts are delivered. Multiple exporters can be active simultaneously, each with independent configuration.

## Export Destinations

| Exporter | Configuration Fields |
|----------|---------------------|
| **Splunk HEC** | URL, token, index, source type |
| **OpenSearch** | URL, index, auth mode (basic, API key, none) |
| **Microsoft Sentinel** | Workspace ID, shared key |
| **AlienVault** | Server URL, API key |
| **SCP Transfer** | Host, path, credentials, row limits |
| **UDP Syslog** | Host, port |
| **Local FileSystem** | Output directory path |
| **Reporter** | WitFoo Analytics Reporter integration |

## Features

### Enable/Disable Per Exporter

Each exporter has an independent toggle. Multiple exporters can be active simultaneously to send artifacts to multiple destinations.

### STIX Enrichment Toggle

A global toggle enables STIX threat intelligence enrichment for all exported artifacts. When enabled, the Artifact Filter's STIX enrichment stage adds threat indicator metadata before export.

### Filter Configuration

Predicate-based filter rules can be configured to control which artifacts reach each exporter. This allows different destinations to receive different subsets of the artifact stream.

## Configuration Details

### OpenSearch Auth Modes

| Mode | Fields Required |
|------|----------------|
| Basic | Username, password |
| API Key | API key value |
| None | No authentication |

### SCP Transfer

| Field | Description |
|-------|-------------|
| Host | Remote server hostname or IP |
| Path | Remote directory for file delivery |
| Credentials | SSH key or password |
| Row Limits | Maximum rows per exported file |

All configuration changes are saved to the NATS KV `EXPORTERS` bucket and propagate to the Artifact Exporter service within seconds.