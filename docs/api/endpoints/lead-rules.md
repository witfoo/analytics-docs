# Lead Rules

Lead rules define the criteria for promoting observations into investigative leads. Each rule specifies matching conditions on artifact attributes, and when triggered, generates a lead that feeds into the incident correlation engine.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | `/v1/lead-rules` | List lead rules | `signals:read` |
| GET | `/v1/lead-rules/:id` | Get rule details | `signals:read` |
| POST | `/v1/lead-rules` | Create a lead rule | `signals:manage` |
| PUT | `/v1/lead-rules/:id` | Update a lead rule | `signals:manage` |
| DELETE | `/v1/lead-rules/:id` | Delete a lead rule | `signals:manage` |

---

## GET /v1/lead-rules

List all lead rules for the organization.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enabled` | boolean | No | Filter by enabled/disabled status |
| `limit` | integer | No | Max results (default: 50) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/lead-rules?enabled=true" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "rules": [
      {
        "id": "rule-001",
        "org_id": "witfoo",
        "name": "Brute Force Detection",
        "description": "Triggers on repeated failed authentication attempts",
        "enabled": true,
        "conditions": {
          "source": "auth",
          "pattern": "failed_login",
          "threshold": 10,
          "window": "5m"
        },
        "severity": "high",
        "created_at": "2026-01-10T12:00:00Z",
        "updated_at": "2026-02-01T09:30:00Z"
      }
    ],
    "total": 1,
    "limit": 50,
    "offset": 0
  }
}
```

---

## POST /v1/lead-rules

Create a new lead rule.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Rule name |
| `description` | string | No | Human-readable description |
| `enabled` | boolean | No | Whether the rule is active (default: `true`) |
| `conditions` | object | Yes | Matching conditions |
| `conditions.source` | string | No | Artifact source filter |
| `conditions.pattern` | string | Yes | Pattern to match |
| `conditions.threshold` | integer | No | Event count threshold |
| `conditions.window` | string | No | Time window (e.g., `5m`, `1h`) |
| `severity` | string | No | Severity assigned to generated leads |

### Example Request

```bash
curl -X POST "https://analytics.example.com/api/v1/lead-rules" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Port Scan Detection",
    "description": "Detects horizontal port scanning activity",
    "conditions": {
      "source": "firewall",
      "pattern": "port_scan",
      "threshold": 50,
      "window": "10m"
    },
    "severity": "medium"
  }'
```

### Example Response

```json
{
  "success": true,
  "message": "Lead rule created",
  "data": {
    "id": "rule-002",
    "name": "Port Scan Detection",
    "enabled": true,
    "created_at": "2026-02-14T11:00:00Z"
  }
}
```

---

## PUT /v1/lead-rules/:id

Update an existing lead rule. Only provided fields are modified.

### Example Request

```bash
curl -X PUT "https://analytics.example.com/api/v1/lead-rules/rule-002" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

---

## DELETE /v1/lead-rules/:id

Delete a lead rule by ID.

### Example Response

```json
{
  "success": true,
  "message": "Lead rule deleted",
  "data": null
}
```

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request body or parameters |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions (`signals:read` or `signals:manage` required) |
| 404 | Rule not found |
| 500 | Internal server error |
