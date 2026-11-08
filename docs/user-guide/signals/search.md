# Search

The Search page is the primary investigation tool in WitFoo Analytics. Use it to query artifacts across your entire data set, apply filters, visualize geographic distribution, and export results for further analysis.

## Accessing Search

Navigate to **Search** > **Signals** from the main navigation bar. The page loads with a default time range showing recent artifacts. It needs the `signals:read` permission.

## The Search Interface

The Search page is organized into several areas:

- **Search bar** -- Enter keywords and field filters, with autocomplete suggestions
- **Time range picker** -- Select a predefined range or set a custom absolute date range
- **Filter bar** -- Active filters displayed as removable tags below the search bar
- **Timeline** -- A histogram of the matching events over the time range
- **Facets** -- Counts of the matching events by field, for quick filtering
- **Results table** -- Paginated list of matching artifacts with configurable columns
- **Detail panel** -- Click anywhere in a row to inspect the full artifact, view its graph relationships, and take action

## Searching Artifacts

### Basic Search

Type a word into the search bar and press Enter. A word typed without a field name matches events whose message contains it, ignoring upper and lower case. A phrase with spaces is matched as one piece of text. The word must be at least three bytes long.

### Field-Specific Search

Narrow your query by targeting specific fields with an operator:

| Operator | Meaning | Example |
| --- | --- | --- |
| `=` | Equals | `stream_name=ids` |
| `!=` | Does not equal | `action!=allowed` |
| `:` | Contains | `user_name:admin` |
| `>`, `>=`, `<`, `<=` | Comparison, on a number field only | `server_port>=1024` |

Comparisons work on number fields such as client port, server port, bytes sent, bytes received, duration and file size. Contains works on text fields only.

### Client and Server Fields

Most events have a client side and a server side.

| You type | Matches |
| --- | --- |
| `ip=`, `port=`, `hostname=` | Both sides at once: an event matches only when its client side **and** its server side both have that value |
| `client_ip=`, `server_ip=`, `client_port=`, `server_port=`, `client_hostname=`, `server_hostname=` | One side only |

`client_ip=` and `server_ip=` accept an IPv4 or an IPv6 address.

### Combining Filters

Apply multiple filters simultaneously to narrow results. Each active filter appears as a tag in the filter bar. Remove a filter by clicking the close icon on its tag.

!!! tip "Filter Stacking"
    Filters are combined with AND logic. Adding a severity filter of "high" and a stream filter of "authentication" returns only high-severity authentication artifacts.

### Filters Apply to the Whole Range

Every filter in the search bar, including contains, not-equal, comparisons, Client IP and Server IP matches, the Location filter and a free word, applies to the whole time range. It narrows the result list, the timeline and the facet counts, and every later page of results uses the same filters.

### When a Search Is Not Accepted

A filter the search cannot apply as typed is refused with the notice "The search was not accepted as typed. Check the filters and the search word, then try again." For example:

- a comparison on a text field;
- a contains on a number field;
- a value that is not a number where a number is needed;
- a word shorter than three bytes;
- a page deeper than the first 10,000 results.

A refusal for permission reads "You do not have permission to run this search." Neither offers Retry.

## Time Range Selection

Click the time range picker to choose from preset windows or define a custom range.

**Custom Range:** Select "Custom" to pick specific start and end dates using the date picker calendar.

### How Far Back You Can Search

A search can cover up to your organization's search window. The window equals the **Retention** > **Search** setting. When that is not set, it is 30 days.

A wider range is refused: "That time range is too wide. Searches are limited to {limit} — narrow the range and try again."

## When a Search Reads Only Part of the Range

A filter such as contains, not-equal or a word is applied while the server reads the events, newest first. Such a read is bounded, and the result list, the timeline and the filtered facet counts each stop after 10 seconds.

When a search did not read the whole range, the page says so:

- A warning above the results says why: the search reached its read limit, ran out of time, or could not read part of the range.
- A line under the timeline says its bars or their colours may undercount.
- The filtered facet counts show a plus sign (`+`), meaning the count is a floor.

!!! tip "Seeing everything"
    Narrow the time range, or add a filter on severity, message type or source.

Results by offset stop at the first 10,000. To reach older events, narrow the time range or add a filter.

## Working with Results

### Column Configuration

Click the **Settings** icon in the toolbar to open the column configurator. Toggle columns on or off and drag to reorder them. Your column preferences are saved in your browser.

### Viewing Artifact Details

Click anywhere in a row to open the Signal Details window. The detail view shows:

1. **Summary** -- Key fields including timestamp, source, destination, severity, and stream
2. **Raw Data** -- The original log entry or event payload in JSON format
3. **Graph View** -- A mini graph showing the artifact's relationships with nodes (IPs, domains, hosts)
4. **Enrichment** -- GeoIP data, threat intelligence matches, and other enriched context

### Grouping the Timeline

Use the timeline's Group-by menu to split the bars by a field. Grouping by Client IP or Server IP groups by the actual addresses, IPv4 or IPv6. A number with no stored value, such as a missing port, is its own "unknown" group. The Group-by menu no longer offers Alarm Rule. The page remembers your choice in your browser.

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

**Auto-delete after (days)** sets when a saved search ends: the day it was created plus the days you choose. `0` means it never expires. From 1.2.0 this setting is honoured. Before 1.2.0 a saved search could lose its contents 7 days after it was last saved, whatever this setting said, and a search lost before the upgrade cannot be recovered.

### Sharing Searches

Saved searches can generate a share link. Recipients who have access to the same organization can open the link to load the exact same search criteria in their browser.

## Exporting Results

Click the **Download** button in the toolbar to export the current results. Exported data includes all visible columns and respects your active filters and time range.

## Creating Work Units from Search

When you identify artifacts that require a coordinated response:

1. Click the **Add to Work Unit** icon in the toolbar
2. Enter a **Work Unit Name** and an optional description
3. Optionally choose a work collection to add the work unit to
4. Click **Add to Work Unit**

The new work unit holds up to 50 artifacts from the current search results.

## Performance Tips

- Use specific field filters rather than broad keyword searches
- Narrow the time range to the smallest window that covers your investigation
- The search page prefetches the next page of results in the background for faster navigation
- Results are cached briefly to speed up pagination through the same result set

## Known Limitations

- On WFA appliances and the Compose bundle, a search that takes longer than about 17 seconds fails with an error. A long time range with few or no matches can take that long. Narrow the time range or add a filter.
- In the Signal Details window, Escape does not close the window while its field search has focus. Use the close button.
- A search with a filter applied row by row reads a bounded number of the newest events in the range. If that is spent before the page is full, the search stops and says so, so a rare match in a long time range can be missing.
