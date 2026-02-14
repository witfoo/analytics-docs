# Chat Interface

The AI chat panel provides conversational access to AI-powered security analysis within WitFoo Analytics.

## Accessing Chat

- **Chat Panel** — Click the chat icon in the navigation bar or press `Ctrl+/` to toggle the side panel
- **Chat Page** — Navigate to the dedicated chat page for full-screen conversations

## Features

- **Context-aware** — The AI has access to your current page context (incidents, nodes, reports)
- **Multi-session** — Maintain multiple chat sessions for different investigations
- **Tool-augmented** — The AI can query your data through MCP tools when enabled
- **History** — Chat sessions are persisted and can be resumed

## Chat Panel

The chat panel slides in from the right side of the screen (400px width). It renders on any page when the user has `ai:read` permission.

### Keyboard Shortcut

Press `Ctrl+/` to toggle the chat panel open/closed.

## Sessions

### Create a Session

Click **New Chat** to start a fresh conversation. Each session maintains its own context and history.

### Resume a Session

Click any session in the session list to resume the conversation.

### Delete a Session

Click the delete icon on a session to remove it and its message history.

## Permissions

| Action | Required Permission |
| --- | --- |
| Use chat | `ai:read` |
| Delete sessions | `ai:write` |
| Export transcripts | `ai:export` |
