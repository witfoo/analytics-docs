# Observations

Observations are structured analytical findings derived from artifact analysis. They capture specific behaviors, patterns, or indicators discovered during the security analysis pipeline and serve as building blocks for incident correlation.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | `/v1/observations` | List observations | `observations:read` |
| GET | `/v1/observations/:id` | Get observation details | `observations:read` |
| POST | `/v1/observations` | Create an observation | `observations:write` |
| PUT | `/v1/observations/:id` | Update an observation | `observations:write` |
| DELETE | `/v1/observations/:id` | Delete an observation | `observations:write` |

---

## GET /v1/observations

List observations with optional filtering by type, severity, or time range.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Filter by observation type (e.g., `network`, `auth`, `malware`) |
| `severity` | string | No | Filter by severity level |
| `start` | string | No | Start of time range (ISO 8601) |
| `end` | string | No | End of time range (ISO 8601) |
| `limit` | integer | No | Max results (default: 50, max: 1000) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/observations?type=network&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "observations": [
      {
        "id": "obs-456",
        "org_id": "witfoo",
        "type": "network",
        "description": "C2 beacon pattern detected",
        "severity": "high",
        "node_ids": ["node-abc-123"],
        "artifact_ids": ["art-789"],
        "created_at": "2026-02-14T09:00:00Z"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

---

## GET /v1/observations/:id

Retrieve a single observation with full details.

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/observations/obs-456" \
  -H "Authorization: Bearer $TOKEN"
```

---

## POST /v1/observations

Create a new observation.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Observation type |
| `description` | string | Yes | Human-readable description |
| `severity` | string | No | Severity level (default: `medium`) |
| `node_ids` | array | No | Related node IDs |
| `artifact_ids` | array | No | Related artifact IDs |

### Example Request

```bash
curl -X POST "https://analytics.example.com/api/v1/observations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "network",
    "description": "Repeated DNS queries to known DGA domain",
    "severity": "high",
    "node_ids": ["node-abc-123"]
  }'
```

### Example Response

```json
{
  "success": true,
  "message": "Observation created",
  "data": {
    "id": "obs-789",
    "type": "network",
    "description": "Repeated DNS queries to known DGA domain",
    "severity": "high",
    "created_at": "2026-02-14T11:00:00Z"
  }
}
```

---

## PUT /v1/observations/:id

Update an existing observation. Only provided fields are modified.

### Example Request

```bash
curl -X PUT "https://analytics.example.com/api/v1/observations/obs-789" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"severity": "critical"}'
```

---

## DELETE /v1/observations/:id

Delete an observation by ID.

### Example Request

```bash
curl -X DELETE "https://analytics.example.com/api/v1/observations/obs-789" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "Observation deleted",
  "data": null
}
```

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request body or parameters |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions |
| 404 | Observation not found |
| 500 | Internal server error |
