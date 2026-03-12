# MCP Tools

Reference for all 51 MCP tools available to the AI assistant. Tools are organized by category and require appropriate permissions for invocation.

## Security Analysis (Tools 1-6)

Core tools for searching and inspecting security data.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 1 | `search_artifacts` | Search artifacts by query, time range, and filters | `signals:read` |
| 2 | `search_nodes` | Search graph nodes by type, properties, or relationships | `signals:read` |
| 3 | `search_edges` | Search graph edges connecting nodes | `signals:read` |
| 4 | `get_artifact_details` | Get full details for a specific artifact by ID | `signals:read` |
| 5 | `get_node_details` | Get node details including properties and connected edges | `signals:read` |
| 6 | `get_graph_neighbors` | Get neighboring nodes and edges for a given node | `signals:read` |

## Incident Management (Tools 7-15)

Tools for querying and inspecting incidents, work units, collections, and detection data.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 7 | `list_incidents` | List incidents with pagination and filtering | `signals:read` |
| 8 | `get_incident` | Get full incident details including suspicion score breakdown | `signals:read` |
| 9 | `search_work_units` | Search work units by status, assignee, or date range | `observer:read` |
| 10 | `get_work_unit` | Get work unit details with related artifacts and nodes | `observer:read` |
| 11 | `list_work_collections` | List work collections with summary statistics | `observer:read` |
| 12 | `get_work_collection` | Get work collection details and member work units | `observer:read` |
| 13 | `list_observations` | List observations with MO definition matches | `observer:read` |
| 14 | `get_observation` | Get observation details | `observer:read` |
| 15 | `get_lead_rules` | Get lead rule definitions and match statistics | `signals:read` |

## System & Chat (Tools 16-20)

System health, notification, classification, and chat tools.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 16 | `get_system_health` | Get system health status for all services | `health:read` |
| 17 | `get_notification_channels` | List configured notification channels | `settings:read` |
| 18 | `get_classification_rules` | Get signal classification rules | `signals:read` |
| 19 | `send_chat_message` | Send a message to a chat room | `chat:write` |
| 20 | `list_chat_rooms` | List available chat rooms | `chat:read` |

## Reports (Tools 21-25)

Tools for retrieving report data from the Reporter module.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 21 | `get_executive_report` | Get executive summary report data | `reports:read` |
| 22 | `get_investigation_report` | Get investigation status report data | `reports:read` |
| 23 | `get_daily_report` | Get daily summary report data | `reports:read` |
| 24 | `get_vulnerability_report` | Get vulnerability assessment report data | `reports:read` |
| 25 | `get_tool_effectiveness_report` | Get tool effectiveness and coverage report data | `reports:read` |

## MCP Infrastructure (Tool 26)

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 26 | `mcp_info` | Get MCP server metadata, version, and available tool count | None |

## Incident Lifecycle (Tools 27-37)

Tools for creating, updating, and managing incident state transitions.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 27 | `create_incident` | Create a new incident with title and description | `signals:write` |
| 28 | `update_incident` | Update incident properties (severity, status, assignee) | `signals:write` |
| 29 | `close_incident` | Close an incident with resolution notes | `signals:write` |
| 30 | `add_incident_note` | Add a note or comment to an incident | `signals:write` |
| 31 | `update_incident_status` | Change incident status (open, investigating, resolved, etc.) | `signals:write` |
| 32 | `assign_incident` | Assign an incident to an analyst | `signals:write` |
| 33 | `merge_incidents` | Merge related incidents into a single parent | `signals:manage` |
| 34 | `split_incident` | Split an incident into separate work units | `signals:manage` |
| 35 | `escalate_incident` | Escalate incident priority and notify stakeholders | `signals:write` |
| 36 | `link_incidents` | Create a relationship link between two incidents | `signals:write` |
| 37 | `get_incident_timeline` | Get chronological timeline of incident events | `signals:read` |

## Workflow Automation (Tools 38-48)

Tools for playbook execution, responder actions, and task management.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 38 | `execute_playbook` | Execute a playbook against an incident | `playbooks:execute` |
| 39 | `list_playbooks` | List available playbooks with criteria | `playbooks:read` |
| 40 | `get_playbook` | Get playbook definition and step details | `playbooks:read` |
| 41 | `get_playbook_execution` | Get execution status and results for a playbook run | `playbooks:read` |
| 42 | `trigger_responder` | Trigger a responder action (e.g., block IP, disable user) | `responders:execute` |
| 43 | `list_responders` | List available responder templates | `responders:read` |
| 44 | `create_task` | Create a task within a work unit | `observer:write` |
| 45 | `update_task` | Update task status or assignee | `observer:write` |
| 46 | `list_tasks` | List tasks for a work unit or collection | `observer:read` |
| 47 | `create_work_unit` | Create a new work unit | `observer:write` |
| 48 | `update_work_unit` | Update work unit properties | `observer:write` |

## CyberGrid (Tools 49-51)

Tools for CyberGrid intelligence sharing and search jobs.

| # | Tool | Description | Permission |
| --- | --- | --- | --- |
| 49 | `search_cybergrid_jobs` | Search and list CyberGrid search jobs | `cybergrid:read` |
| 50 | `list_cybergrid_publications` | List CyberGrid publications for the organization | `cybergrid:read` |
| 51 | `list_cybergrid_subscriptions` | List CyberGrid subscriptions and feed status | `cybergrid:read` |

## Tool Invocation

Tools are invoked automatically by the AI model when relevant to the conversation. Users see tool invocations and results in the chat interface.

### Rate Limiting

MCP tools are rate-limited per organization to prevent abuse. The default rate limit allows reasonable interactive use. Background AI tasks (e.g., playbook analysis) share the same rate limit pool.

### Audit Logging

All MCP tool invocations are logged to the audit trail with the invoking user, tool name, parameters, and timestamp. This provides full traceability for AI-assisted investigations.

### Error Handling

Tools return structured error responses with error codes and human-readable messages. Common error scenarios:

| Error Code | Description |
| --- | --- |
| `permission_denied` | User lacks the required permission for this tool |
| `not_found` | Requested resource does not exist |
| `rate_limited` | Too many requests; retry after the indicated delay |
| `validation_error` | Invalid parameters provided |
| `internal_error` | Server-side error; contact administrator |
