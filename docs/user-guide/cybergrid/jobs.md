# Jobs

Background synchronization jobs for threat intelligence feeds.

## Job Types

| Type | Direction | Description |
| --- | --- | --- |
| **Sync** | Inbound | Download from subscribed feed |
| **Publish** | Outbound | Upload to a publication |
| **Enrich** | Internal | Apply indicators to nodes |

## Job Properties

| Column | Description |
| --- | --- |
| **Job ID** | Unique identifier |
| **Type** | Sync, Publish, or Enrich |
| **Status** | Pending, Running, Complete, Failed |
| **Started** | Start timestamp |
| **Duration** | Execution time |
| **Indicators** | Indicators processed |

Failed jobs are automatically retried. Click **Run Now** on any subscription for immediate sync.

## Job History

Retained for 30 days with automatic cleanup.
