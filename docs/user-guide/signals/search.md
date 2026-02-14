# Search

The Search page is the primary investigation tool in WitFoo Analytics. Use it to query artifacts across your entire data set, apply filters, visualize geographic distribution, and export results for further analysis.

## Accessing Search

Navigate to **Signals > Search** from the main navigation bar. The page loads with a default time range showing recent artifacts.

## The Search Interface

The Search page is organized into several areas:

- **Search bar** -- Enter keywords, field queries, or free-text searches with autocomplete suggestions
- **Time range picker** -- Select predefined ranges (last 15 minutes, 1 hour, 24 hours, 7 days) or set a custom absolute date range
- **Filter bar** -- Active filters displayed as removable tags below the search bar
- **Results table** -- Paginated list of matching artifacts with configurable columns
- **Detail panel** -- Click any row to inspect the full artifact, view its graph relationships, and take action

## Searching Artifacts

### Basic Search

Type a keyword into the search bar and press Enter. The search matches against all indexed fields including IP addresses, hostnames, usernames, and raw log content.

### Field-Specific Search

Narrow your query by targeting specific fields:

| Field | Example | Description |
|-------|---------|-------------|
| `src_ip` | `src_ip:192.168.1.100` | Source IP address |
| `dst_ip` | `dst_ip:10.0.0.5` | Destination IP address |
| `hostname` | `hostname:web-server-01` | Hostname of the source or target |
| `user` | `user:jsmith` | Username associated with the event |
| `severity` | `severity:critical` | Severity level (informational, low, medium, high, critical) |
| `stream` | `stream:ids` | Artifact stream / classification |

### Combining Filters

Apply multiple filters simultaneously to narrow results. Each active filter appears as a tag in the filter bar. Remove a filter by clicking the close icon on its tag.

!!! tip "Filter Stacking"
    Filters are combined with AND logic. Adding a severity filter of "high" and a stream filter of "authentication" returns only high-severity authentication artifacts.

## Time Range Selection

Click the time range picker to choose from preset windows or define a custom range.

**Preset Ranges:**

| Preset | Window |
|--------|--------|
| Last 15 minutes | Rolling 15-minute window |
| Last 1 hour | Rolling 1-hour window |
| Last 24 hours | Rolling 24-hour window |
| Last 7 days | Rolling 7-day window |
| Last 30 days | Rolling 30-day window |

**Custom Range:** Select "Custom" to pick specific start and end dates using the date picker calendar.

!!! warning "Large Time Ranges"
    Queries spanning more than 30 days may take longer to return results. Consider narrowing your time range or adding additional filters to improve performance.

## Working with Results

### Column Configuration

Click the **Settings** icon in the toolbar to open the column configurator. Toggle columns on or off and drag to reorder them. Your column preferences are saved in your browser.

### Viewing Artifact Details

Click any row to open the signal detail modal. The detail view shows:

1. **Summary** -- Key fields including timestamp, source, destination, severity, and stream
2. **Raw Data** -- The original log entry or event payload in JSON format
3. **Graph View** -- A mini graph showing the artifact's relationships with nodes (IPs, domains, hosts)
4. **Enrichment** -- GeoIP data, threat intelligence matches, and other enriched context

### Geographic Visualization

When artifacts contain IP addresses with GeoIP data, a world map heatmap appears above the results table. Countries are shaded by artifact volume, and country flags appear next to geographic data in the results.

!!! info "Internal IPs"
    Private IP addresses (RFC 1918 ranges such as 10.x.x.x, 172.16-31.x.x, and 192.168.x.x) do not have geographic data and will not appear on the map.

## Saved Searches

Save frequently used search criteria for quick access later.

1. Configure your search term, filters, and time range
2. Click the **Save** icon in the toolbar
3. Enter a descriptive name for the saved search
4. Click **Save**

To load a saved search, click the **Folder** icon and select from your list of saved searches.

### Sharing Searches

Saved searches can generate a share link. Recipients who have access to the same organization can open the link to load the exact same search criteria in their browser.

## Exporting Results

Click the **Download** button in the toolbar to export the current results. Exported data includes all visible columns and respects your active filters and time range.

## Creating Incidents from Search

When you identify artifacts that require a coordinated response:

1. Select one or more artifacts in the results table
2. Click **Create Incident** in the toolbar
3. The selected artifacts are attached to a new incident for tracking through the investigation lifecycle

## Adding to Work Collections

Selected artifacts can also be added to an existing work collection in the Observer module:

1. Select artifacts in the results table
2. Click **Add to Collection**
3. Choose the target work collection from the dropdown
4. The artifacts are linked to the collection for organized investigation

## Performance Tips

- Use specific field filters rather than broad keyword searches
- Narrow the time range to the smallest window that covers your investigation
- The search page prefetches the next page of results in the background for faster navigation
- Results are cached briefly to speed up pagination through the same result set
