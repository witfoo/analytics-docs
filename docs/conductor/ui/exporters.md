# Exporter Configuration

**URL:** `/admin/settings/artifact-exporters`

The Exporter Configuration page manages the destinations where processed artifacts are delivered. Multiple exporters can be active simultaneously, each with independent configuration.

## Export Destinations

| Exporter | What it does |
|----------|--------------|
| **WitFoo Analytics (HTTP)** | Sends artifacts over HTTP to the artifact receiver of a WitFoo Analytics appliance, each batch signed with an HMAC-SHA256 secret. On an all-in-one Conductor it is configured automatically |
| **Analytics Reporter (WebSocket)** | Sends artifacts to a WitFoo Analytics appliance over a secure WebSocket (TLS) connection |
| **Splunk** | Sends to a Splunk HTTP Event Collector (HEC) endpoint |
| **OpenSearch** | Sends to an OpenSearch endpoint |
| **Microsoft Sentinel** | Sends to a Microsoft Sentinel workspace through the Data Collector API |
| **CrowdStrike Falcon Next-Gen SIEM** | Sends to CrowdStrike Falcon Next-Gen SIEM through an HEC / HTTP Event Data Connector |
| **USM Anywhere** | Sends batched JSON by webhook to LevelBlue USM Anywhere |
| **S3 Object Storage** | Writes compressed NDJSON objects to S3-compatible object storage |
| **Azure Blob Storage** | Writes compressed NDJSON blobs to Azure Blob Storage |
| **Google Cloud Storage** | Writes compressed NDJSON objects to Google Cloud Storage |
| **SCP Transfer** | Writes files up to a size limit and transfers them over SSH |
| **UDP Syslog** | Sends to a syslog server over UDP |
| **Local Filesystem** | Writes files up to a size limit to another directory or mount on the same machine |

The [Integration Catalog](../../reference/integration-catalog.md) lists every exporter in this release.

!!! warning "Two ways to reach Analytics"
    **WitFoo Analytics (HTTP)** and **Analytics Reporter (WebSocket)** both deliver to a WitFoo Analytics appliance. Enable one or the other for an appliance: with both enabled, each artifact is delivered twice unless their filters or artifact sources differ. The page shows a warning when two enabled exporters deliver to the same host. It compares host names only, so two names for one machine are not caught.

## Features

### Enable/Disable Per Exporter

Each exporter has an independent toggle. Multiple exporters can be active simultaneously to send artifacts to multiple destinations. An exporter you remove stays removed.

### STIX Enrichment Toggle

A global toggle enables STIX threat intelligence enrichment for all exported artifacts. When enabled, the Artifact Filter's STIX enrichment stage adds threat indicator metadata before export.

### Filter Configuration

Predicate-based filter rules can be configured to control which artifacts reach each exporter. This allows different destinations to receive different subsets of the artifact stream.

### OCSF 1.8 Export

The **S3 Object Storage**, **Azure Blob Storage**, **Google Cloud Storage** and **OpenSearch** exporters have an **Export Format** field under **Export Encoding**:

| Export Format | Output |
|---------------|--------|
| **Artifact JSON (default)** | The native WitFoo artifact shape, unchanged |
| **OCSF 1.8** | Open Cybersecurity Schema Framework 1.8.0 class objects, for data lakes and SIEMs (for example AWS Security Lake, Tenzir and Splunk) |

The OCSF mapping is applied when the artifact is exported. It does not change the artifact in the pipeline. An artifact that cannot be mapped is still exported, as an OCSF Base Event carrying the raw data.

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

### UDP Syslog

The syslog exporter sends over UDP only in 1.2.0. TCP and TLS syslog export are not available in this release.

All configuration changes are saved to the NATS KV `EXPORTERS` bucket and propagate to the Artifact Exporter service within seconds. The USM Anywhere, Azure Blob Storage and Google Cloud Storage settings save numbers and switches in the form their exporters read.

## Connector Health and Retries

The retry rules apply to the exporters and to the pull connectors of the Signal Client.

- **Transient failures are retried quickly.** A connector whose run ends for a transient reason (the destination is down or busy, an HTTP 408, 429 or 5xx, a failed connection) is re-attempted after 5, 10, 20, 40, then 60 seconds. The ladder starts again after a run of 5 minutes.
- **Permanent failures wait 15 minutes.** A failure that waiting cannot fix (a credential, a setting or an endpoint) is retried after 15 minutes.
- **The status says the real wait,** for example `re-attempting in ~40s`. "Verify credentials/permissions" appears only for a failure that waiting cannot fix.
- **A busy receiver is waited for.** When the Analytics receiver answers the two WitFoo Analytics exporters busy (503, 429 or another 5xx), the exporter waits, honouring `Retry-After` up to 30 seconds, and does not count it as a connector failure.
- **Refused batches are split.** When the Analytics receiver refuses a batch from one of the two WitFoo Analytics exporters for what it holds (400, 413 or 422), the exporter divides the batch until it finds the artifact the receiver refuses. Three refused flushes in a row stop the instance with `the receiver refuses every artifact it is sent`; nothing is discarded.

### The `decode_error` Health Code

A connector that cannot decode what it was given reports the health code `decode_error`. It is a transient code: the connector keeps retrying. The Conductor UI explains it as follows:

> The provider answered successfully but WitFoo could not decode the response — a WitFoo bug or a provider format change, NOT a credential or permission problem. No operator action: the connector keeps retrying. Report it if it persists across an upgrade.

The connector's own message is shown in the detail. A connector whose saved settings cannot be decoded (for example the SCP Transfer, Local Filesystem, Reporter or Abnormal Security settings) also reports `decode_error`, although no provider was contacted and the settings are not retried: read the connector's own message, which names the settings, and correct them.
