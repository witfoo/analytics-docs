# Artifacts

Artifacts represent raw security signals ingested into the analytics pipeline. They include IDS alerts, authentication events, firewall logs, DNS queries, and other telemetry collected from security tools and infrastructure.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/v1/artifacts` | Search artifacts with filters |
| GET | `/v1/artifacts/histogram` | Timeline counts for a search |
| GET | `/v1/artifacts/facet-counts` | Facet counts for a search |
| GET | `/v1/artifacts/facets` | Facet counts for the Signal Search sidebar |
| GET | `/v1/artifacts/stats` | Artifact statistics for a window |
| GET | `/v1/artifacts/:id` | Get one artifact |

Every request carries the bearer token of a signed-in user and reads only that user's organization.

!!! note "Ingesting artifacts"
    `POST /v1/artifacts` is removed and has no replacement. Artifacts reach the appliance through the artifact receiver.

---

## GET /v1/artifacts

Search and filter ingested artifacts, newest first.

### Query Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `time_start` | string | Start of the time range (RFC 3339) |
| `time_end` | string | End of the time range (RFC 3339) |
| `limit` | integer | Results per page. Absent or zero means the default of 100. |
| `offset` | integer | Results to skip. `offset` plus `limit` may not exceed 10,000. |
| `search` | string | A word or phrase the message must contain, ignoring upper and lower case. At least three bytes. |
| `stream_name` | string | Stream name (exact match) |
| `message_type` | string | Message type |
| `action` | string | Action (exact match) |
| `client_ip` | string | Client IP address |
| `server_ip` | string | Server IP address |
| `user_name` | string | User name |
| `vendor_code` | string | Vendor code |
| `node_id` | string | Artifacts that reference a graph node |
| `file_name_like` | string | File name pattern |
| `severity_min` | integer | Minimum severity (1-10) |
| `severity_max` | integer | Maximum severity (1-10) |
| `only_alarms` | boolean | Only artifacts that matched a lead rule |
| `matched_lead_rules` | string | Comma-separated lead rule IDs (any of them) |
| `stix_indicator_ids` | string | Comma-separated STIX indicator IDs |
| `attack_technique_ids` | string | Comma-separated MITRE ATT&CK technique IDs |
| `tags` | string | Tag; repeat the parameter for more than one |
| `filters` | JSON | A list of `{"field", "operator", "value"}` conditions. Operators: `=`, `!=`, `:` (contains), `>`, `>=`, `<`, `<=`. |

### Example Request

```bash
curl -G "https://analytics.example.com/api/v1/artifacts" \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "time_start=2026-11-01T00:00:00Z" \
  --data-urlencode "time_end=2026-11-02T00:00:00Z" \
  --data-urlencode "stream_name=ids" \
  --data-urlencode "limit=50"
```

---

## Search Time Window

`GET /v1/artifacts`, `/v1/artifacts/histogram` and `/v1/artifacts/facet-counts` serve a bounded time window. The limit is set per organization.

| Source of the limit | Limit |
| --- | --- |
| The organization's **Retention** > **Search** setting | That many days (1 to 365) |
| No setting, or a setting that cannot be read | The appliance's artifact retention, 30 days by default |
| A retention with no expiry | 7 days |

- Every successful search carries the limit in `meta.max_window_seconds`. Read it from the response; never hardcode it.
- A wider window is refused with **400** and the code `search_window_too_wide`. `details.limit_seconds` is the organization's limit.
- A half-open window is checked too. Each missing bound is filled on its own: the start defaults to 24 hours before now, and the end defaults to now. So `time_start` alone, far in the past, can be refused. Only a request with neither bound reads the default window.
- A window whose end is before its start is refused with the code `search_window_inverted`.

```json
{
  "success": false,
  "message": "Time range exceeds the maximum supported search window",
  "error": "search window of 739h28m39.977s exceeds the maximum of 168h0m0s",
  "code": "search_window_too_wide",
  "details": { "limit_seconds": 604800, "requested_seconds": 2662119 }
}
```

`GET /v1/artifacts/stats` keeps its own 30-day limit.

## Partial Reads (meta.scan)

Some filters are applied while the server reads the window, newest first: contains (`:`), not-equal (`!=`), comparisons on a number field, a Client IP or Server IP match on an IPv6 address, the location filter, and the `search` word.

Such a read is bounded. The result list and the timeline also stop after 10 seconds and answer with what they have read. When a read stopped early, the response carries `meta.scan`:

```json
"meta": { "scan": { "scanned": 10000, "cap": 10000, "incomplete": true, "reason": "rows" } }
```

| `reason` | Meaning |
| --- | --- |
| `rows` | The read reached its row limit. A re-run reads the same rows. Narrow the time range or add a filter. |
| `time` | The 10-second read limit ran out. |
| `partial` | Part of the range could not be read just now. A re-run may find more. |

When `incomplete` is true, matching records may be missing. Do not show a short or empty result as if the whole window was read. A client that meets a `reason` it does not know should treat the read as incomplete.

The facet counts carry their own `estimated` flag instead of `meta.scan`.

## Request Limits

A request the server cannot run as sent is refused with **400** and the code `invalid_parameter`. `details.parameter` names the parameter. The body never repeats the value.

| Limit | Value |
| --- | --- |
| A free-text value matched exactly | 8,192 bytes |
| A value matched with `:`, `!=` or a comparison, and `file_name_like` | 65,535 bytes |
| A list parameter (`tags`, `matched_lead_rules`, `stix_indicator_ids`, `attack_technique_ids`) | 100 values |
| The `filters` parameter | 128 entries |
| The query string | 256 parameters |
| `search` | At least 3 bytes |
| `client_ip`, `server_ip` | Must be an IP address |
| `offset` plus `limit` | At most 10,000 |
| `limit`, `offset` | Not negative |

## IP Address Parameters on the Timeline and Facet Counts

On the histogram and the facet counts, the `client_ip` and `server_ip` parameters apply an IPv6 address but not an IPv4 address. The result list applies both. To apply an IPv4 address on all three, send the condition in `filters`:

```text
filters=[{"field":"client_ip","operator":"=","value":"10.9.9.9"}]
```

---

## Error Responses

| Status | Description |
| --- | --- |
| 400 | A parameter the server cannot use (`invalid_parameter`), or a time window that is too wide or inverted |
| 401 | Missing or invalid token |
| 499 | The client went away before the answer |
| 500 | The artifact store could not be read. A search never answers an empty result in its place. |
| 503 | The read passed its deadline |
