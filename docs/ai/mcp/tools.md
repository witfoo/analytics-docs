# MCP Tools

WitFoo Analytics 1.2.0 serves 44 MCP tools: 28 read-only and 16 state-changing.

## How tools are authorized

Every tool call runs as the connected user, with that user's live permissions. Two checks run:

1. **Admission**, on every request. The user must still be active, must hold `mcp:connect`, and the credential must still be valid.
2. **Authorization**, on each `tools/call`. The user must hold the permission the tool needs, as listed in the tables below.

`mcp:connect` is a gate, not a grant. A connected user reaches only the tools whose permissions they also hold. `mcp_info` and `get_system_health` need only `mcp:connect`.

For the eight `manage_*` tools, the permission depends on the `action` argument. The arguments must carry exactly one string `action`. A missing, repeated, differently-cased or unlisted action is denied. See [Permissions for the manage tools](#permissions-for-the-manage-tools).

!!! info "Apps that sign in with OAuth"
    An access token also carries a scope. The scope is a second limit, never a grant beyond the tables.

    - A read-only tool needs the scope `mcp:read`.
    - Every other tool needs `mcp:write`. A token without it is answered `403` with an `insufficient_scope` challenge.
    - Under `mcp:read` alone, the user's permissions are narrowed to the `:read` permissions they hold.

    See [App sign-in (OAuth 2.1)](oauth.md).

## Titles and annotations

Every tool carries a display title. The same text is in the tool's `title` field and in `annotations.title`, so every client shows the same name.

Each tool is also marked read-only or state-changing:

- A read-only tool sets `readOnlyHint: true`.
- A state-changing tool sets `destructiveHint: true`, so a client can ask before it runs.

The eight `manage_*` tools are marked state-changing and destructive, because one tool name covers both reads and changes. Their `list` and `get` actions only read.

The 16 state-changing tools are `create_dashboard`, `create_responder_job`, `execute_playbook`, `execute_responder_job`, `generate_report`, `send_chat_message`, `update_dashboard`, `update_incident_status`, and the eight `manage_*` tools.

## Tool reference

### Incidents

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_incidents` | Search Incidents | Yes | `work_units:read` |
| `get_incident_details` | Get Incident Details | Yes | `work_units:read` |

### Nodes

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_nodes` | Search Nodes | Yes | `graph:read` |

### Artifacts

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_artifacts` | Search Artifacts | Yes | `signals:read` |

### Dashboards

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `list_dashboards` | List Dashboards | Yes | `dashboards:read` |
| `create_dashboard` | Create Dashboard | No | `dashboards:write` |
| `update_dashboard` | Update Dashboard | No | `dashboards:write` |

### Responder

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `list_responder_jobs` | List Responder Jobs | Yes | `responders:read` |
| `get_responder_job` | Get Responder Job | Yes | `responders:read` |
| `create_responder_job` | Create Responder Job | No | `responders:write` |
| `execute_responder_job` | Execute Responder Job | No | `responders:manage` |

### Audit

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_audit_findings` | Search Audit Findings | Yes | `auditor:read` |
| `get_audit_compliance` | Get Audit Compliance | Yes | `auditor:read` |
| `get_audit_remediation` | Get Audit Remediation | Yes | `auditor:read` |

### Directory

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_directory` | Search Directory | Yes | `cybergrid:publications:read` |

### Chat

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `search_chat_rooms` | Search Chat Rooms | Yes | `chat:read` |
| `search_chat_messages` | Search Chat Messages | Yes | `chat:read` |
| `send_chat_message` | Send Chat Message | No | `chat:write` |

### Reports

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `get_executive_summary` | Get Executive Summary | Yes | `reports:read` |
| `get_compliance_status` | Get Compliance Status | Yes | `reports:read` |
| `get_cost_savings` | Get Cost Savings | Yes | `reports:read` |
| `get_tool_effectiveness` | Get Tool Effectiveness | Yes | `reports:read` |
| `generate_report` | Generate Report | No | `reports:generate` |

### Infrastructure

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `mcp_info` | MCP Info | Yes | None (`mcp:connect` only) |

### Incident lifecycle

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `manage_incident_notes` | Manage Incident Notes | No | By action |
| `manage_incident_assignments` | Manage Incident Assignments | No | By action |
| `search_observations` | Search Observations | Yes | `observations:read` |
| `get_incident_linked` | Get Incident Linked | Yes | `work_units:read` |
| `get_incident_suspicion_details` | Get Incident Suspicion Details | Yes | `work_units:read` |
| `get_incident_audit_log` | Get Incident Audit Log | Yes | `work_units:read` |
| `get_incident_facets` | Get Incident Facets | Yes | `work_units:read` |
| `get_incident_observation_matches` | Get Incident Observation Matches | Yes | `work_units:read` |
| `update_incident_status` | Update Incident Status | No | `work_units:write` |

### Workflow and automation

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `manage_playbooks` | Manage Playbooks | No | By action |
| `execute_playbook` | Execute Playbook | No | `playbooks:manage` |
| `get_playbook_executions` | Get Playbook Executions | Yes | `playbooks:read` |
| `manage_tasks` | Manage Tasks | No | By action |
| `manage_work_collections` | Manage Work Collections | No | By action |
| `manage_collection_members` | Manage Collection Members | No | By action |
| `search_users` | Search Users | Yes | `users:read` |
| `manage_business_settings` | Manage Business Settings | No | By action |
| `get_system_health` | Get System Health | Yes | None (`mcp:connect` only) |

### Detection management

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `manage_observations` | Manage Observations | No | By action |

### Collection details

| Tool | Title | Read-only | Permission |
| --- | --- | --- | --- |
| `get_work_collection_details` | Get Work Collection Details | Yes | `collections:read` |

### Permissions for the manage tools

| Tool | `action` | Permission |
| --- | --- | --- |
| `manage_business_settings` | `get` | `settings:read` |
| `manage_business_settings` | `update` | `settings:manage` |
| `manage_collection_members` | `list` | `collections:read` |
| `manage_collection_members` | `add` | `collections:write` |
| `manage_collection_members` | `remove` | `collections:write` |
| `manage_incident_assignments` | `list` | `work_units:read` |
| `manage_incident_assignments` | `assign` | `work_units:write` |
| `manage_incident_assignments` | `unassign` | `work_units:write` |
| `manage_incident_notes` | `list` | `work_units:read` |
| `manage_incident_notes` | `create` | `work_units:write` |
| `manage_observations` | `create` | `observations:write` |
| `manage_observations` | `update` | `observations:write` |
| `manage_observations` | `delete` | `observations:delete` |
| `manage_playbooks` | `list` | `playbooks:read` |
| `manage_playbooks` | `get` | `playbooks:read` |
| `manage_playbooks` | `create` | `playbooks:write` |
| `manage_playbooks` | `delete` | `playbooks:delete` |
| `manage_tasks` | `list` | `work_units:read` |
| `manage_tasks` | `create` | `work_units:write` |
| `manage_tasks` | `update_status` | `work_units:write` |
| `manage_work_collections` | `list` | `collections:read` |
| `manage_work_collections` | `get` | `collections:read` |
| `manage_work_collections` | `create` | `collections:write` |
| `manage_work_collections` | `delete` | `collections:write` |

!!! note "OAuth tokens and the manage tools"
    Every action of the eight `manage_*` tools, reads included, needs the `mcp:write` scope on an access token.

## Removed tools

These seven tools were listed by earlier releases but always failed. They are removed in 1.2.0:

- `search_attachment_metadata`
- `get_framework_controls`
- `create_search_job`
- `list_search_jobs`
- `search_lead_rules`
- `search_leads`
- `manage_lead_rules`

## Behaviour notes

### Incidents

- `search_incidents` and `get_incident_details` return results.
- `search_incidents` returns up to `limit` incidents (default 50, at most 100), newest first. `limit` plus `offset` may not exceed 10,000. Use a result's `next_offset` to continue.
- A search result carries no node or edge count. The detail's `node_count` and `edge_count` are the numbers of node ids and edge ids the incident carries.
- To read who is assigned, call `manage_incident_assignments` with the action `list`.

### Optional arguments

Optional arguments are optional. `search_nodes` does not require `limit`, `search_incidents` does not require `limit` or `offset`, and `search_artifacts` does not require `only_alarms`, `limit` or `offset`.

Time arguments are RFC 3339 timestamps. The `node_type` filter of `search_nodes` includes `file`. `execute_responder_job` takes a `trigger_type` of `manual`, `playbook` or `mcp`.

### search_artifacts

`search_artifacts` reads one page and does not count every match. Its answer says what that page can claim:

| Field | Meaning |
| --- | --- |
| `total` | The number of artifacts in this answer, not a count of every match. When `capped` is true it is a floor. |
| `capped` | `true` when the answer filled `limit`, so more artifacts may match. |
| `next_offset` | Present only when `capped` is true. Pass it as `offset` to continue. |
| `incomplete` | `true` when matches may be missing from this answer, whatever its size. `capped: false` means complete only when `incomplete` is false too. |
| `incomplete_reason` | Present only when `incomplete` is true. `partial`: part of the read failed for a moment, and a re-run may find more. `rows`: the read stopped at its row bound, so narrow the time range or add a filter. `time`: a read time budget ran out. |

- `limit` plus `offset` may not exceed 10,000. A deeper request is refused with a tool error.
- The time window may not be wider than the organization's search window, the same limit Signal Search uses. A wider window is refused before anything is read.
- Each missing time bound is filled on its own: the start defaults to 24 hours before now, and the end defaults to now. So a lone `time_start` 30 days back is a 30-day window and can be refused. A call with neither bound reads the last 24 hours.

### search_nodes

- `ip` and `hostname` are exact lookups. They find a host by any IP address or hostname it has, not only the one it was first seen with.
- A lookup returns at most one node. With neither `ip` nor `hostname`, `node_type` filters a scan.
- `capped` is always present. It is `true` when a scan filled `limit` (default 50, at most 1,000), so more nodes may match. An `ip` or `hostname` lookup is never capped.
- A lookup that cannot be completed is an error ("the node lookup could not be completed; this does not mean no such node exists"), never an empty list.

### get_audit_remediation

`get_audit_remediation` returns the check's `resource_type` when it is called with a `check_id`, as it does when it is called with a `finding_id`.

### Report tools

- `get_executive_summary`, `get_compliance_status`, `get_cost_savings` and `get_tool_effectiveness` read the latest stored snapshot.
- A snapshot that is empty or cannot be read is an error that names the report date, never a report of zeros.
- Each answer carries the snapshot's `confidence` flag. `low_confidence_inputs_not_ready` means the figures may be understated.
- `get_executive_summary` takes no inputs. It refuses `start_date` and `end_date`.

### generate_report

`generate_report` regenerates the report snapshots for the caller's organization and answers when the pass has finished. It holds the call open for up to five minutes.

!!! warning "HTTP requests close at 120 seconds"
    The reverse proxy in front of HTTP `/mcp` closes a request at 120 seconds. Over HTTP `/mcp`, a pass that takes longer ends in a transport error instead of the tool's answer. A pass that fails is an error result.

### Dashboards and attribution

Dashboard tools work for holders of the `dashboards:*` permissions. Tools that record who acted record the connected user.

## In-app AI assistant

The in-app AI assistant uses the same tool handlers through a bridge. It does not connect over `/ws/chat`. It offers five read-only tools:

| Tool | Permission |
| --- | --- |
| `search_nodes` | `graph:read` |
| `search_artifacts` | `signals:read` |
| `search_observations` | `observations:read` |
| `get_audit_remediation` | `auditor:read` |
| `search_directory` | `cybergrid:publications:read` |

- Each tool call is authorized with the caller's own permissions, by the same rule as an MCP `tools/call`.
- The permissions come from the caller's signed-in session. A permission removed from a role stops working for the assistant when the caller's session token is next replaced.
- A `limit` larger than 200 is run at 200.
- `search_artifacts` is held to the organization's search window.

In an AI analysis of a work unit, `search_artifacts` answers "artifact search is not available on this service". `search_nodes` works there as usual.

See [Chat Interface](../chat.md).

## Errors

For the responses a client can receive at connection and on each request, see [MCP Errors](errors.md).
