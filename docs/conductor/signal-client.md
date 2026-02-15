# Signal Client (Pull Ingestion)

Signal Client handles pull-based log collection from cloud services and security platforms. It polls external APIs on configurable schedules, collecting events and publishing them to the NATS `artifacts.raw` stream.

## Architecture

Signal Client follows the same **Source → Flow → Sink** pattern as Signal Server, but uses pull-based collection instead of push-based listeners:

- **Source** — API poller (HTTP client with authentication)
- **Flow** — Transform API responses to artifact format
- **Sink** — NATS publisher to `artifacts.raw` subject

Each integration runs as an independent connector with its own polling schedule, credentials, and checkpoint tracking.

## Key Features

- **Scheduled Polling** — Configurable intervals per integration (typically 1–15 minutes)
- **Credential Management** — Supports OAuth2, API keys, client ID/secret, and tenant-specific authentication
- **Checkpoint Tracking** — Resumes from the last successful position to avoid duplicate collection
- **Rate Limiting** — Respects API quotas and implements backoff on rate limit responses

## Configuration

Signal Client is configured via the NATS KV `INTEGRATIONS` bucket. Each integration stores its configuration as JSON:

```json
{
  "enabled": true,
  "integration_type": "microsoft_graph",
  "poll_interval_minutes": 5,
  "credentials": {
    "client_id": "...",
    "client_secret": "...",
    "tenant_id": "..."
  }
}
```

Integrations are managed through the [Conductor UI Integrations page](ui/integrations.md).

## Supported Integrations

Signal Client supports all 19 API-based integrations listed on the [Integration Management](ui/integrations.md) page, including Microsoft, Cisco, CrowdStrike, Palo Alto, Proofpoint, and other security vendors.

!!! note
    Configuration changes propagate from the Conductor UI to Signal Client within 5–10 seconds via the NATS KV watch mechanism. No container restart is required.