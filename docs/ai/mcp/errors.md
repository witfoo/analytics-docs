# MCP Errors

Error handling for MCP tool invocations.

## Error Format

```json
{
  "error": "error_code",
  "message": "Human-readable description"
}
```

## Error Codes

| Code | Description |
| --- | --- |
| `permission_denied` | User lacks required permission |
| `not_found` | Requested resource not found |
| `invalid_input` | Tool parameters are invalid |
| `rate_limited` | Too many tool invocations |
| `internal_error` | Server-side error |
| `tool_disabled` | Tool category is disabled in MCP config |

## Troubleshooting

| Error | Cause | Solution |
| --- | --- | --- |
| Permission denied | Insufficient role | Admin assigns appropriate role |
| Tool disabled | MCP category off | Admin enables category in MCP config |
| Rate limited | Excessive tool calls | Wait and retry; reduce query frequency |
| Internal error | Backend issue | Check Incident Engine logs |
