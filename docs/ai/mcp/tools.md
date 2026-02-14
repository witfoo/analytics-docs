# MCP Tools

Reference for available MCP tools that the AI assistant can invoke.

## Search Tools

| Tool | Description | Permission |
| --- | --- | --- |
| `search_artifacts` | Search artifacts by query | `signals:read` |
| `search_nodes` | Search graph nodes | `signals:read` |
| `search_incidents` | Search incidents | `signals:read` |

## Analysis Tools

| Tool | Description | Permission |
| --- | --- | --- |
| `get_incident` | Get incident details | `signals:read` |
| `get_node` | Get node details with edges | `signals:read` |
| `get_artifact` | Get artifact details | `signals:read` |

## Report Tools

| Tool | Description | Permission |
| --- | --- | --- |
| `get_executive_summary` | Executive report data | `reports:read` |
| `get_compliance` | Compliance readiness data | `reports:read` |
| `get_tool_effectiveness` | Tool effectiveness data | `reports:read` |

## Tool Invocation

Tools are invoked automatically by the AI model when relevant to the conversation. Users see tool invocations and results in the chat interface.
