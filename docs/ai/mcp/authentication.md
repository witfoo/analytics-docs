# MCP Authentication

MCP tool invocations are authenticated and authorized using the same JWT-based system as the REST API.

## Authentication Flow

1. User authenticates via the web UI (JWT token in session)
2. Chat messages carry the user's JWT
3. MCP tool invocations include the JWT for authorization
4. Each tool checks the user's permissions before executing

## Permission Enforcement

Every MCP tool maps to one or more API permissions. If the user lacks the required permission, the tool returns an error:

```json
{
  "error": "permission_denied",
  "message": "Requires signals:read permission"
}
```

## Org Isolation

MCP tools are scoped to the user's organization. A tool invocation can only access data belonging to the user's `org_id` from their JWT claims.
