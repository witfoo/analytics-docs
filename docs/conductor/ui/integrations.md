# Integration Management

**URL:** `/admin/settings/integrations`

The Integration Management page configures pull-based API integrations for the Signal Client service. Each integration connects to an external cloud or security platform to collect log data on a scheduled basis.

!!! tip "Looking for step-by-step setup instructions?"
    See the [Integration Guides](../integrations/index.md) for vendor-specific prerequisites, credential creation walkthroughs, and troubleshooting for the supported pull connectors.

## Supported Integrations

| Vendor | Integrations |
|--------|-------------|
| Microsoft | Azure Security, Microsoft Sentinel, MS Defender Vulnerability Mgmt, Azure VNet Flow Logs |
| Amazon Web Services | AWS GuardDuty, AWS Security Hub, AWS VPC Flow Logs |
| Google Cloud | Google Cloud SCC, GCP VPC Flow Logs |
| Oracle Cloud | OCI VCN Flow Logs |
| Cloudflare | Cloudflare |
| Cisco | AMP, Duo, Meraki, Secure Access, Umbrella |
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
| Monitoring | SNMP Monitoring Poller, HTTP/HTTPS Monitor |

The [Integration Catalog](../../reference/integration-catalog.md) lists every pull connector in this release.

### New in 1.2.0

Seven pull connectors are new, each with its own form on this page:

| Connector | Guide |
|-----------|-------|
| Cloudflare | [Cloudflare](../integrations/cloudflare.md) |
| AWS VPC Flow Logs | [AWS VPC Flow Logs](../integrations/aws-vpc-flow-logs.md) |
| Azure VNet Flow Logs | [Azure VNet Flow Logs](../integrations/azure-vnet-flow-logs.md) |
| GCP VPC Flow Logs | [GCP VPC Flow Logs](../integrations/gcp-vpc-flow-logs.md) |
| OCI VCN Flow Logs | [OCI VCN Flow Logs](../integrations/oci-vcn-flow-logs.md) |
| SNMP Monitoring Poller | [SNMP Monitoring Poller](../integrations/snmp-poll.md) |
| HTTP/HTTPS Monitor | [HTTP/HTTPS Monitor](../integrations/http-poll.md) |

The four flow-log connectors summarize flow records into network conversations with the same flow engine as the NetFlow/IPFIX collector on the [Log Servers](log-servers.md) page.

## Configuration

Each integration has a dedicated settings form with vendor-specific fields:

### Common Fields

| Field | Description |
|-------|-------------|
| Enable/Disable Toggle | Activate or deactivate the integration |

Polling intervals are built into each connector and cannot be changed. The
Splunk form is the exception: it has a **Poll Interval** field (seconds). The
SNMP Monitoring Poller and HTTP/HTTPS Monitor forms also have a **Poll Interval
(seconds)** field for each target.

### Authentication Fields (varies by vendor)

| Field | Used By |
|-------|---------|
| API Key / Token | CrowdStrike, Mimecast, Netskope, Okta, Tenable, Cloudflare |
| Client ID / Client Secret | Microsoft, Cisco Duo, Cisco AMP, Proofpoint |
| Tenant ID | Microsoft integrations |
| Workspace ID | Microsoft Sentinel |

## Connector Changes in 1.2.0

- **Cisco Meraki** — The connector reads events in the format Meraki documents, follows its paging, keeps its progress when a pass runs out of time, reports rate limits, and keeps going when one organization's networks are refused. A redirect is followed only over HTTPS on port 443, to one of the documented Meraki API hosts or a `meraki.com` subdomain.
- **DNS Zone Transfer** — The connector asks the DNS server for each zone's SOA serial and transfers a zone only when the serial changed, could not be read, or the zone was last sent 12 hours ago or more. It polls every 60 minutes and transfers each zone over its own connection. A restart of the connector transfers every zone again. If the artifact filter's deduplication window is 12 hours or more, the 12-hour re-send is dropped as a duplicate.
- **One artifact per record** — Connectors that pull a page or a poll of records (Cisco AMP, Umbrella and Meraki, Azure Security, Microsoft Sentinel, Splunk and Stealthwatch) give every record its own artifact id, so records that arrive together are no longer collapsed into one.
- **Rejected API keys** — When a provider rejects the API key a connector sends (HTTP 401), the Signal Client reports the failure on that connector and keeps running.
- **Retries** — A transient failure is re-attempted after 5, 10, 20, 40, then 60 seconds; a permanent one after 15 minutes. See [Exporter Configuration](exporters.md).

!!! warning "Upgrade separate Conductors with Analytics"
    A Conductor on 1.1.5 or older sending to 1.2.0 Analytics keeps only about one record per page or poll for Azure Security, Microsoft Sentinel, Cisco AMP, Cisco Umbrella, Cisco Meraki, Splunk and Stealthwatch. Upgrade every Conductor at the same time as Analytics or before it.

## Status Tracking

Each integration displays:

- **Connection status** — Whether the last poll was successful
- **Last poll time** — When data was last collected
- **Error details** — Description of any failures (authentication errors, rate limiting, connectivity issues), and a health code such as `auth_failed`, `rate_limited` or `decode_error`

Changes are saved to the NATS KV `INTEGRATIONS` bucket and take effect within seconds.

## Feed Approval

When a Conductor sends its first batch to Analytics, Analytics records it as a pending feed for an administrator to approve or reject.

- An organization holds at most 1,000 pending feeds. A registration that would make the 1,001st is dropped; the feed registers again once feeds are decided or deleted.
- A pending feed expires after 7 days and registers again, as a new one, when its Conductor next sends a batch.
- Approving or rejecting a feed keeps the decision with no expiry. Pending feeds written by an earlier release have no expiry and stay until an administrator decides or deletes them.
- The approval page lists at most 2,000 feeds of an organization. Delete old feeds to see the rest.
- A decision on a feed that has expired answers 404.
