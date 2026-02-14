# Artifacts

Artifacts represent raw security signals ingested into the analytics pipeline. They include IDS alerts, authentication events, firewall logs, DNS queries, and other telemetry collected from security tools and infrastructure.

## Endpoints

| Method | Path | Description | Permission |
|--------|------|-------------|------------|
| POST | `/v1/artifacts` | Ingest new artifacts | `signals:write` |
| GET | `/v1/artifacts` | Search artifacts with filters | `signals:read` |

---

## POST /v1/artifacts

Ingest one or more security artifacts into the processing pipeline. Artifacts are queued for parsing, enrichment, and correlation via the data pipeline.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `artifacts` | array | Yes | Array of artifact objects |
| `artifacts[].source` | string | Yes | Source identifier (e.g., `suricata`, `auth`, `firewall`) |
| `artifacts[].raw` | string | Yes | Raw log or event data |
| `artifacts[].timestamp` | string | No | ISO 8601 timestamp; defaults to server time |
| `artifacts[].metadata` | object | No | Additional key-value metadata |

### Example Request

```bash
curl -X POST https://analytics.example.com/api/v1/artifacts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "artifacts": [
      {
        "source": "suricata",
        "raw": "ET MALWARE Trickbot Checkin",
        "timestamp": "2026-02-14T10:30:00Z",
        "metadata": {"sensor": "ids-01"}
      }
    ]
  }'
```

### Example Response

```json
{
  "success": true,
  "message": "Artifacts accepted for processing",
  "data": {
    "accepted": 1,
    "rejected": 0
  }
}
```

---

## GET /v1/artifacts

Search and filter ingested artifacts. Results are paginated and sorted by timestamp descending.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source` | string | No | Filter by artifact source |
| `start` | string | No | Start of time range (ISO 8601) |
| `end` | string | No | End of time range (ISO 8601) |
| `query` | string | No | Full-text search query |
| `limit` | integer | No | Max results to return (default: 50, max: 1000) |
| `offset` | integer | No | Pagination offset |

### Example Request

```bash
curl -X GET "https://analytics.example.com/api/v1/artifacts?source=suricata&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Example Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "artifacts": [
      {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "org_id": "witfoo",
        "source": "suricata",
        "raw": "ET MALWARE Trickbot Checkin",
        "timestamp": "2026-02-14T10:30:00Z",
        "metadata": {"sensor": "ids-01"},
        "created_at": "2026-02-14T10:30:01Z"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid request body or query parameters |
| 401 | Missing or invalid JWT token |
| 403 | Insufficient permissions (`signals:read` or `signals:write` required) |
| 500 | Internal server error |
