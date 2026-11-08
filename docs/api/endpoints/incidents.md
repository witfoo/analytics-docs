# Incidents

Incidents represent correlated security events that require investigation. The UI shows them as work units. The incident engine aggregates related artifacts, nodes, and observations into actionable incidents with severity ratings and status tracking.

## Endpoints

| Method | Path | Description | Permission |
| --- | --- | --- | --- |
| GET | `/v1/incidents` | List incidents with filters | `work_units:read` |
| GET | `/v1/incidents/:id` | Get incident details | `work_units:read` |
| GET | `/v1/incidents/:id/artifacts` | Get the incident's artifacts | Read access to the incident |
| GET | `/v1/incidents/:id/graph/edges` | Get the incident's graph edges | Read access to the incident |
| GET | `/v1/incidents/:id/notes` | List notes | `work_units:read` |
| POST | `/v1/incidents/:id/notes` | Add a note | `work_units:write` |
| GET | `/v1/incidents/:id/audit` | Get the audit log | `work_units:read` |
| PUT | `/v1/incidents/:id/status-audit` | Update the status and record it in the audit log | `work_units:write` |

## Status Values

| ID | Name | Classification |
|----|------|----------------|
| 1 | New | -- |
| 2 | Investigating | -- |
| 3 | Resolved | True Positive |
| 4 | Closed | False Positive |
| 5 | Disrupted | True Positive |

---

## GET /v1/incidents

List incidents for the organization, with optional filtering and pagination.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status_id` | string | No | One status ID, or a comma-separated list of them (`status_id=4,5`). The parameter can also be repeated. |
| `suspicion_level` | string | No | `low`, `medium` or `high`, or a comma-separated list of them (`suspicion_level=low,high`). The parameter can also be repeated. |
| `severity_level` | integer | No | Severity level (1-10) |
| `min_suspicion` | number | No | Minimum suspicion score |
| `max_suspicion` | number | No | Maximum suspicion score |
| `node_id` | string | No | Incidents that include a graph node |
| `attack_technique_id` | string | No | Incidents that include a MITRE ATT&CK technique |
| `client_ip` | string | No | Incidents that include a client IP address |
| `limit` | integer | No | Max results (default 100, max 500) |
| `offset` | integer | No | Pagination offset. `limit` plus `offset` may not exceed 10,000. |

- A list of status IDs or suspicion levels returns incidents in **any** of them.
- An empty entry (`4,,5`), a value that is not a positive integer, or a suspicion level other than the three is refused with a **400** that names the parameter.
- A list of two or more statuses is read over the newest 10,000 incidents of the organization. When that read comes back full, the response sets `meta.capped: true`, a sign that older matches exist.
- A `node_id`, `attack_technique_id` or `client_ip` filter reads only that item's newest incidents, up to `limit`, and `total` counts only those. Beside a status, severity or work definition filter, `meta.capped` is true when that read comes back full.
- `time_start` and `time_end` are not filters of this route.

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/incidents?status_id=1,2&suspicion_level=high&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## GET /v1/incidents/:id

Retrieve full details for a single incident.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Incident ID |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/incidents/d290f1ee-6c54-4b01-90e6-d701748f0851" \
  -H "Authorization: Bearer $TOKEN"
```

---

## GET /v1/incidents/:id/artifacts

Return the incident's artifacts, oldest first. The work-unit detail page reads them once for its histogram, table and timeline.

| Parameter | Type | Description |
| --- | --- | --- |
| `limit` | integer | Page size (default 500, max 1,000) |
| `page` | integer | 1-based page number (default 1) |

The incident is read first, so a caller can read only the artifacts of an incident it can already read. An unknown or another organization's ID answers **404**.

---

## GET /v1/incidents/:id/graph/edges

Return the incident's graph edges with their time fields, ordered by when they started. Work-unit **Replay** uses this endpoint.

| Parameter | Type | Description |
| --- | --- | --- |
| `limit` | integer | Page size (default 500, max 1,000) |
| `page` | integer | 1-based page number (default 1) |

The response carries `meta.truncated` when the edge set is incomplete: a very busy node, or an incident of more than 2,000 nodes, made the read stop short. The Replay view shows at most 600 nodes and says so when it leaves some out.

---

## PUT /v1/incidents/:id/status-audit

Update the status of an incident and record the change in its audit log. Status transitions drive true positive and false positive classification.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status_id` | integer | Yes | New status ID (1-5) |

### Example Request

```bash
curl -X PUT "https://analytics.example.com/api/v1/incidents/d290f1ee-6c54-4b01-90e6-d701748f0851/status-audit" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status_id": 3}'
```

---

## Work Collections

`POST` and `PUT` on `/v1/work-collections` change only what the request states.

- Every member (`name`, `description`, `criteria` or `criteria_json`, `enabled`, `assigned_to`, `status_id`) is optional.
- A member the body leaves out, or sets to null, keeps its stored value. A member it states, empty included, replaces it.
- Members the server owns (counts, dates, creator, organization, ID) are ignored.
- A collection created without `enabled` is stored disabled.
- A request that states nothing, that states both `criteria` and `criteria_json`, or whose collection does not validate is a **400**.

Reading collections needs `collections:read`; creating and changing them needs `collections:write`.

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | A malformed parameter, ID or JSON body, or a negative `limit` or `offset`. The code is `invalid_parameter` and the response names the parameter. |
| 401 | Missing or invalid token |
| 403 | Insufficient permissions |
| 404 | Incident not found |
| 500 | Internal server error |
