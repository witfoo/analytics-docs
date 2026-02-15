# Integration Management

**URL:** `/admin/settings/integrations`

The Integration Management page configures pull-based API integrations for the Signal Client service. Each integration connects to an external cloud or security platform to collect log data on a scheduled basis.

## Supported Integrations

| Vendor | Integrations |
|--------|-------------|
| Microsoft | Azure Security, Defender, Sentinel, Entra ID, Office 365 |
| Cisco | AMP, Duo, Meraki, Umbrella |
| CrowdStrike | Falcon |
| Palo Alto | Cortex |
| Proofpoint | CASB, Protect |
| Deep Instinct | Deep Instinct |
| Druva | Druva |
| LimaCharlie | LimaCharlie |
| Mimecast | Mimecast |
| Netskope | Netskope |
| Okta | Okta |
| Splunk | Splunk (search-based collection) |
| Stealthwatch | Stealthwatch |
| Tenable | Tenable |
| DNS | DNS Zone Transfer |

## Configuration

Each integration has a dedicated settings form with vendor-specific fields:

### Common Fields

| Field | Description |
|-------|-------------|
| Enable/Disable Toggle | Activate or deactivate the integration |
| Polling Interval | How frequently to collect data (minutes) |

### Authentication Fields (varies by vendor)

| Field | Used By |
|-------|---------|
| API Key / Token | CrowdStrike, Mimecast, Netskope, Okta, Tenable |
| Client ID / Client Secret | Microsoft, Cisco Duo, Cisco AMP, Proofpoint |
| Tenant ID | Microsoft integrations |
| Workspace ID | Microsoft Sentinel |

## Status Tracking

Each integration displays:

- **Connection status** — Whether the last poll was successful
- **Last poll time** — When data was last collected
- **Error details** — Description of any failures (authentication errors, rate limiting, connectivity issues)

Changes are saved to the NATS KV `INTEGRATIONS` bucket and take effect within seconds.