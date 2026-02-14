# MCP Configuration

Configure which MCP tools are available to the AI assistant.

## Enabling MCP

1. Navigate to **Admin** > **AI** > **MCP Configuration**
2. Toggle MCP server on/off
3. Select which tool categories to enable
4. Click **Save**

## Tool Categories

Enable or disable tool categories independently:

| Category | Default | Description |
| --- | --- | --- |
| **Search** | Enabled | Artifact and node search |
| **Incidents** | Enabled | Incident queries and details |
| **Reports** | Enabled | Report data access |
| **Admin** | Disabled | Administrative operations |

## Configuration via API

```text
GET /api/v1/ai/mcp/config
PUT /api/v1/ai/mcp/config
```

Requires `ai:manage` permission.
