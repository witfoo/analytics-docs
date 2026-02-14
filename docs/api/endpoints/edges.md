# Edges

Edges represent relationships between nodes in the security knowledge graph. Each edge connects a source node to a target node with a typed relationship such as communication, authentication, or DNS resolution.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | `/v1/edges` | List edges with filters | `graph:read` |
| GET | `/v1/edges/:id` | Get edge details | `graph:read` |

---

## GET /v1/edges

List edges in the knowledge graph, optionally filtered by source node, target node, or relationship type.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_id` | UUID | No | Filter by source node ID |
| `target_id` | UUID | No | Filter by target node ID |
| `type` | string | No | Filter by edge type (e.g., `communicates_with`, `resolved_to`) |
| `start` | string | No | Start of time range (ISO 8601) |
| `end` | string | No | End of time range (ISO 8601) |
| `limit` | integer | No | Max results (default: 50, max: 1000) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/edges?source_id=node-abc-123&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "edges": [
      {
        "id": "edge-001",
        "org_id": "witfoo",
        "source_id": "node-abc-123",
        "target_id": "node-def-456",
        "type": "communicates_with",
        "weight": 15,
        "first_seen": "2026-02-10T08:00:00Z",
        "last_seen": "2026-02-14T10:30:00Z",
        "artifact_count": 15
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

---

## GET /v1/edges/:id

Retrieve details for a single edge including the connected source and target nodes.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Edge ID |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/edges/edge-001" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "id": "edge-001",
    "org_id": "witfoo",
    "source_id": "node-abc-123",
    "target_id": "node-def-456",
    "source": {"id": "node-abc-123", "type": "IP", "value": "10.0.1.50"},
    "target": {"id": "node-def-456", "type": "domain", "value": "malware.example.com"},
    "type": "communicates_with",
    "weight": 15,
    "first_seen": "2026-02-10T08:00:00Z",
    "last_seen": "2026-02-14T10:30:00Z",
    "artifact_count": 15
  }
}
```

---

## Edge Types

| Type | Description |
|------|-------------|
| `communicates_with` | Network communication between nodes |
| `resolved_to` | DNS resolution from domain to IP |
| `authenticated_as` | Authentication event linking user to host |
| `member_of` | Group or organizational membership |
| `related_to` | General correlation relationship |

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid query parameters or malformed UUID |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions (`graph:read` required) |
| 404 | Edge not found |
| 500 | Internal server error |
