# Incidents

Incidents represent correlated security events that require investigation. The incident engine aggregates related artifacts, nodes, and observations into actionable incidents with severity ratings and status tracking.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | `/v1/incidents` | List incidents with filters | `incidents:read` |
| GET | `/v1/incidents/:id` | Get incident details | `incidents:read` |
| PUT | `/v1/incidents/:id/status` | Update incident status | `incidents:write` |

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
| `status` | integer | No | Filter by status ID (1-5) |
| `severity` | string | No | Filter by severity (`low`, `medium`, `high`, `critical`) |
| `start` | string | No | Start of time range (ISO 8601) |
| `end` | string | No | End of time range (ISO 8601) |
| `limit` | integer | No | Max results (default: 50, max: 1000) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/incidents?status=1&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "incidents": [
      {
        "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
        "org_id": "witfoo",
        "title": "Suspicious Outbound Traffic Detected",
        "severity": "high",
        "status": 1,
        "status_name": "New",
        "artifact_count": 12,
        "node_count": 3,
        "created_at": "2026-02-14T08:15:00Z",
        "updated_at": "2026-02-14T08:15:00Z"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

---

## GET /v1/incidents/:id

Retrieve full details for a single incident, including associated nodes and observations.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Incident ID |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/incidents/d290f1ee-6c54-4b01-90e6-d701748f0851" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "org_id": "witfoo",
    "title": "Suspicious Outbound Traffic Detected",
    "severity": "high",
    "status": 1,
    "status_name": "New",
    "artifact_count": 12,
    "node_count": 3,
    "nodes": [
      {"id": "abc-123", "type": "IP", "value": "10.0.1.50"}
    ],
    "observations": [
      {"id": "obs-456", "type": "network", "description": "C2 beacon pattern"}
    ],
    "created_at": "2026-02-14T08:15:00Z",
    "updated_at": "2026-02-14T08:15:00Z"
  }
}
```

---

## PUT /v1/incidents/:id/status

Update the status of an incident. Status transitions drive true positive and false positive classification.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Incident ID |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | integer | Yes | New status ID (1-5) |

### Example Request

```bash
curl -X PUT "https://analytics.example.com/api/v1/incidents/d290f1ee-6c54-4b01-90e6-d701748f0851/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": 3}'
```

### Example Response

```json
{
  "success": true,
  "message": "Incident status updated to Resolved",
  "data": {
    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "status": 3,
    "status_name": "Resolved"
  }
}
```

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid status value or malformed UUID |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions |
| 404 | Incident not found |
| 500 | Internal server error |
