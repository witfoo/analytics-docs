# Enrichment Settings

Enrichment settings control how WitFoo Analytics augments artifacts and nodes with additional context during processing. Enrichments add metadata such as geolocation, DNS resolution, WHOIS data, and threat intelligence scoring.

## Enrichment Types

| Type | Description | Applied To |
| --- | --- | --- |
| **GeoIP** | Geographic location lookup for IP addresses | IP nodes |
| **DNS** | Reverse DNS and forward resolution | IP and domain nodes |
| **WHOIS** | Domain registration and ownership data | Domain nodes |
| **Threat Intel** | Reputation scoring from CyberGrid feeds | IP, domain, hash nodes |
| **ASN** | Autonomous System Number lookup | IP nodes |

## Configuration

Navigate to **Search** > **Node Enrichment** to manage enrichment configuration. The page is headed **Node Enrichment Settings** and needs the `signals:manage` permission.

### Enable or Disable Enrichments

Each enrichment type can be independently enabled or disabled. Disabled enrichments are skipped during artifact processing.

### Rate Limiting

External enrichment sources have configurable rate limits to prevent API throttling:

| Setting | Default | Description |
| --- | --- | --- |
| Max requests per minute | 60 | Throttle for external API calls |
| Cache TTL | 24 hours | How long enrichment results are cached |
| Retry on failure | 3 | Number of retry attempts for failed lookups |

## Viewing Enrichment Data

Enrichment results appear on node detail pages in the **Enrichment** tab. Each enrichment shows:

- Source name and type
- Timestamp of last enrichment
- Raw enrichment data
- Confidence score (when available)

## Vrax Threat Intelligence

The Node Enrichment page also holds the **Vrax threat intelligence** and **Vrax feed (MISP)** cards. They import the reports your Vrax account holds and show them in a node's detail window. See [Vrax Threat Intelligence](vrax.md).

## Permissions

| Action | Required Permission |
| --- | --- |
| View settings | `signals:read` |
| Modify settings | `signals:manage` |

!!! note "Upgrading to 1.2.0"
    From 1.2.0 the enrichment settings API (`/api/v1/enrichment-settings`) checks `signals:read` to read and `signals:manage` to change, on every request. Admin and Platform Admin are unchanged, and Analyst and ReadOnly can still read. Give `signals:manage` to any custom role that should change enrichment settings.

    A request that turns an enrichment setting on or off must state the value, for example `{"enabled": false}`. An empty body is refused with HTTP 400.
