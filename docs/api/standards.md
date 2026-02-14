# API Standards

All API endpoints follow consistent conventions.

## Response Format

Every response uses this envelope:

```json
{
  "success": true,
  "message": "Optional message",
  "data": { }
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

## HTTP Methods

| Method | Usage |
| --- | --- |
| GET | Retrieve resources |
| POST | Create resources |
| PUT | Update resources (full replacement) |
| DELETE | Remove resources |

## Pagination

List endpoints support pagination:

| Parameter | Default | Description |
| --- | --- | --- |
| `limit` | 25 | Items per page (max 100) |
| `offset` | 0 | Number of items to skip |

## Content Type

All requests and responses use `application/json` unless otherwise noted (e.g., CSV export uses `text/csv`).

## Date Formats

All timestamps use ISO 8601 format: `2026-01-15T10:30:00Z`
