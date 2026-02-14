# Errors

API errors follow standard HTTP status codes with descriptive messages.

## Error Response Format

```json
{
  "success": false,
  "message": "Human-readable error description"
}
```

## Status Codes

| Code | Meaning |
| --- | --- |
| 200 | Success |
| 201 | Created |
| 400 | Bad Request — invalid input |
| 401 | Unauthorized — missing or invalid token |
| 403 | Forbidden — insufficient permissions |
| 404 | Not Found — resource doesn't exist |
| 409 | Conflict — duplicate resource |
| 422 | Unprocessable Entity — validation error |
| 500 | Internal Server Error |

## Common Errors

| Error | Cause | Fix |
| --- | --- | --- |
| "token expired" | JWT has expired | Login again to get new token |
| "permission denied" | Insufficient role | Contact admin for role change |
| "invalid UUID" | Malformed UUID parameter | Use valid UUID v4 format |
| "not found" | Resource doesn't exist | Verify the resource ID |
