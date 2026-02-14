# AI Configuration

Configure AI providers and model settings for the WitFoo Analytics AI assistant.

## Provider Setup

Navigate to **Admin** > **AI** > **Configuration** to manage AI providers.

### Supported Providers

| Provider | Models | Description |
| --- | --- | --- |
| **Anthropic** | Claude family | Recommended for security analysis |
| **OpenAI** | GPT family | Alternative provider |

### Configuration Fields

| Field | Description |
| --- | --- |
| **Provider** | AI service provider |
| **API Key** | Provider API key (encrypted at rest) |
| **Model** | Specific model to use |
| **Temperature** | Response creativity (0.0 - 1.0) |
| **Max Tokens** | Maximum response length |

## MCP Configuration

Configure which MCP tools are available to the AI assistant. See [MCP Configuration](mcp/configuration.md) for details.

## Permissions

Requires `ai:manage` permission to access configuration pages.
