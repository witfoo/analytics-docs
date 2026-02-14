# Nodes

Nodes represent entities in the security knowledge graph. Each node is a distinct object such as an IP address, domain name, hostname, user account, or email address. Nodes are connected by edges and may be flagged with classification attributes.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| GET | `/v1/nodes` | Search nodes with filters | `graph:read` |
| GET | `/v1/nodes/:id` | Get node details | `graph:read` |
| PUT | `/v1/nodes/:id/flags` | Update node flags | `graph:write` |

## Node Types

| Type | Description |
|------|-------------|
| `IP` | IPv4 or IPv6 address |
| `domain` | DNS domain name |
| `host` | Hostname or FQDN |
| `user` | User account identifier |
| `email` | Email address |

---

## GET /v1/nodes

Search the knowledge graph for nodes matching specified criteria.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Filter by node type |
| `value` | string | No | Search by node value (partial match) |
| `managed` | boolean | No | Filter by managed flag |
| `internal` | boolean | No | Filter by internal flag |
| `trusted` | boolean | No | Filter by trusted flag |
| `infrastructure` | boolean | No | Filter by infrastructure flag |
| `frameworks` | string | No | Comma-separated framework indices |
| `limit` | integer | No | Max results (default: 50, max: 1000) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/nodes?type=IP&managed=true&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "nodes": [
      {
        "id": "node-abc-123",
        "org_id": "witfoo",
        "type": "IP",
        "value": "10.0.1.50",
        "flags": {
          "managed": true,
          "internal": true,
          "trusted": false,
          "infrastructure": false
        },
        "frameworks": [3, 4],
        "edge_count": 7,
        "created_at": "2026-01-15T12:00:00Z"
      }
    ],
    "total": 1,
    "limit": 20,
    "offset": 0
  }
}
```

---

## GET /v1/nodes/:id

Retrieve detailed information for a single node, including its flags and connected edges.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Node ID |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/nodes/node-abc-123" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "id": "node-abc-123",
    "org_id": "witfoo",
    "type": "IP",
    "value": "10.0.1.50",
    "flags": {
      "managed": true,
      "internal": true,
      "trusted": false,
      "infrastructure": false
    },
    "frameworks": [3, 4],
    "edges": [
      {"id": "edge-001", "target_id": "node-def-456", "type": "communicates_with"}
    ],
    "edge_count": 7,
    "created_at": "2026-01-15T12:00:00Z"
  }
}
```

---

## PUT /v1/nodes/:id/flags

Update classification flags on a node. Flags control how the node is treated in compliance calculations and graph analysis.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Node ID |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `managed` | boolean | No | Node is managed by the organization |
| `internal` | boolean | No | Node is on the internal network |
| `trusted` | boolean | No | Node is explicitly trusted |
| `infrastructure` | boolean | No | Node is an infrastructure device |

### Example Request

```bash
curl -X PUT "https://analytics.example.com/api/v1/nodes/node-abc-123/flags" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"managed": true, "infrastructure": true}'
```

### Example Response

```json
{
  "success": true,
  "message": "Node flags updated",
  "data": {
    "id": "node-abc-123",
    "flags": {
      "managed": true,
      "internal": true,
      "trusted": false,
      "infrastructure": true
    }
  }
}
```

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid query parameters or malformed UUID |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions (`graph:read` or `graph:write` required) |
| 404 | Node not found |
| 500 | Internal server error |
