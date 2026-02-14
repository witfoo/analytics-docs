# AI

AI assistant configuration and chat session management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/ai/configs` | `ai:manage` | List AI configurations |
| POST | `/v1/ai/configs` | `ai:manage` | Create AI config |
| PUT | `/v1/ai/configs/:id` | `ai:manage` | Update AI config |
| DELETE | `/v1/ai/configs/:id` | `ai:manage` | Delete AI config |
| GET | `/v1/ai/sessions` | `ai:read` | List chat sessions |
| POST | `/v1/ai/sessions` | `ai:read` | Create chat session |
| GET | `/v1/ai/sessions/:id` | `ai:read` | Get session with messages |
| POST | `/v1/ai/sessions/:id/messages` | `ai:read` | Send chat message |
| DELETE | `/v1/ai/sessions/:id` | `ai:write` | Delete session |
| GET | `/v1/ai/mcp/config` | `ai:manage` | Get MCP server config |
| PUT | `/v1/ai/mcp/config` | `ai:manage` | Update MCP config |
