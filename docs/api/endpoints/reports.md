# Reports

Report data and snapshot management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/reports/executive` | `reports:read` | Executive summary data |
| GET | `/v1/reports/compliance` | `reports:read` | Compliance readiness data |
| GET | `/v1/reports/tool-effectiveness` | `reports:read` | Tool effectiveness data |
| GET | `/v1/reports/cost-savings` | `reports:read` | Cost & savings data |
| GET | `/v1/reports/snapshots` | `reports:read` | List report snapshots |

## Query Parameters

| Parameter | Description |
| --- | --- |
| `start` | Start date (ISO 8601) |
| `end` | End date (ISO 8601) |
| `framework_id` | Framework filter (compliance only) |
| `format` | Response format: `json` (default) or `csv` |
