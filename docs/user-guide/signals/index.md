# Signals

The Signals module is your primary interface for investigating security data flowing through WitFoo Analytics. Every log line, alert, and event ingested by the platform becomes a **signal** -- a searchable artifact enriched with context, classified by type, and evaluated against your lead rules.

## What Are Signals?

Signals are normalized security artifacts collected from your environment. Each signal contains:

- **Raw data** -- the original log entry or alert payload
- **Metadata** -- timestamps, source IP, destination IP, hostname, user, and other extracted fields
- **Classification** -- the artifact stream (IDS, authentication, firewall, DNS, endpoint, etc.)
- **Severity** -- a normalized severity level from informational to critical
- **Enrichment** -- additional context added by enrichment sources such as GeoIP location and threat intelligence feeds

When data enters the ingestion pipeline, WitFoo Analytics parses, normalizes, and stores it. Classification rules assign each artifact to a stream, enrichment sources add context, and lead rules evaluate whether the artifact warrants further investigation.

## Module Layout

The Signals section of the navigation contains the following pages:

| Page | Purpose |
|------|---------|
| **Search** | Query and filter artifacts with full-text search, date ranges, and field filters |
| **Lead Rules** | Define rules that flag artifacts as potential leads for investigation |
| **Classification Rules** | Manage rules that assign artifacts to streams (IDS, auth, firewall, etc.) |
| **Enrichment Settings** | Configure external data sources that add context to artifacts |

## Typical Workflow

1. **Search** for artifacts matching a time window, severity, or keyword
2. Review results and drill into individual signal details
3. Identify patterns that should trigger future leads by creating **lead rules**
4. Fine-tune how artifacts are categorized using **classification rules**
5. Add external context by enabling **enrichment sources**

!!! tip "Start with Search"
    Most analysts begin their day in the Search page. Use saved searches to quickly revisit common queries, and export results when you need to share findings with your team.

## Permissions

Access to the Signals module requires the `signals:read` permission. Creating and editing rules requires `signals:write`. Your administrator assigns these permissions through role-based access control in the Admin section.

!!! info "Data Retention"
    The volume of signals stored depends on your organization's retention settings. Administrators can configure retention periods in **Admin > Settings > Business Metrics**. Older signals are automatically purged when the retention window expires.

## Key Concepts

**Streams** -- Logical groupings of artifacts by source type. Common streams include IDS alerts, authentication events, firewall logs, DNS queries, and endpoint telemetry. Classification rules determine which stream an artifact belongs to.

**Leads** -- Artifacts that match a lead rule are flagged for analyst attention. A lead indicates that an artifact has characteristics worth investigating, such as a connection to a known malicious IP or an unusual authentication pattern.

**Enrichment** -- The process of augmenting raw artifact data with external context. GeoIP enrichment adds geographic location to IP addresses. Threat intelligence enrichment cross-references indicators against known threat feeds.

**Severity Levels** -- Each artifact carries a severity from informational through critical. Severity is determined during ingestion based on the source data and any matching classification rules.

## Next Steps

- [Search Artifacts](search.md) -- Learn the search syntax and filtering options
- [Lead Rules](lead-rules.md) -- Create rules that surface important artifacts
- [Classification Rules](classification-rules.md) -- Control how artifacts are categorized
- [Enrichment Settings](enrichment-settings.md) -- Add context from external sources
