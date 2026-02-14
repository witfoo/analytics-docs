# AI & MCP

WitFoo Analytics includes an AI assistant powered by large language models, with a Model Context Protocol (MCP) server for tool-augmented conversations.

## Components

### [Configuration](configuration.md)

Configure AI providers, models, and API keys.

### [Chat Interface](chat.md)

Use the AI chat panel for security analysis assistance.

### [MCP Server](mcp/index.md)

Technical reference for the MCP server providing tool access to AI models.

## Overview

The AI assistant helps analysts with:

- Incident investigation and triage guidance
- Artifact analysis and enrichment interpretation
- Report generation and summary
- Compliance mapping assistance

## Permissions

| Permission | Access |
| --- | --- |
| `ai:read` | Use AI chat |
| `ai:write` | Manage chat sessions |
| `ai:manage` | Configure AI providers |
| `ai:export` | Export chat transcripts |
