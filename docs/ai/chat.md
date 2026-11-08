# Chat Interface

The AI chat panel provides conversational access to AI-powered security analysis within WitFoo Analytics.

## Accessing Chat

- **Chat Panel** — Click the chat icon in the page header, or press `Ctrl+/` (`Cmd+/` on a Mac), to open the side panel
- **Chat Page** — Open the dedicated chat page for full-screen conversations

The panel's **AI** tab appears when the user holds `ai:read` and at least one AI provider is enabled. See [AI Configuration](configuration.md).

## Features

- **Context-aware** — The AI has access to your current page context (incidents, nodes, reports)
- **Multi-session** — Maintain multiple chat sessions for different investigations
- **Tool-augmented** — The AI can look up data through a set of read-only tools, with your own permissions
- **History** — Chat sessions are kept and can be resumed

## Chat Panel

The chat panel slides in from the right side of the screen (400px wide). It can be maximized, or detached into its own window.

The panel can also hold the team chat tabs, **Channels** and **Direct Message**, for users who hold a chat permission.

### Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl+/` | Open the panel on the **AI** tab, or close it |
| `Ctrl+Shift+C` | Open the panel on the **Channels** tab, or close it |

On a Mac, use `Cmd` in place of `Ctrl`.

## Sessions

### Create a Session

Click **New chat** to start a fresh conversation. Each session maintains its own context and history.

### Resume a Session

Click any session in the session list to resume the conversation.

### Rename or Delete a Session

Use the rename and delete controls on a session. Deleting a session removes it and its message history.

### How long history is kept

Chat history is kept for 90 days.

!!! warning "Known limitation"
    A chat session still in use after its 90th day can show as a blank entry in the session list, with its title and creation time gone.

## Tools the assistant uses

The assistant looks up data with five read-only tools: `search_nodes`, `search_artifacts`, `search_observations`, `get_audit_remediation` and `search_directory`. Each call is checked against your own permissions, so the assistant can only read what you can read. See [In-app AI assistant](mcp/tools.md).

The in-app assistant does not use an MCP connection, so it does not need `mcp:connect`.

## Permissions

| Action | Required Permission |
| --- | --- |
| Open your chat sessions and read them | `ai:read` |
| Send a message, or start, rename or delete a session | `ai:write` |

A user with `ai:read` but not `ai:write` can open their sessions but cannot send or change anything. Every built-in role holds both.
