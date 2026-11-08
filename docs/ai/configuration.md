# AI Configuration

Configure AI providers and model settings for the WitFoo Analytics AI assistant.

## Opening AI Setup

Open the **Settings** menu in the page header, then go to **General Settings** > **AI Setup**. The page needs the `ai:manage` permission.

## Provider Setup

The **AI Providers** section lists the configured providers. Click **Add Provider** to add one. Each row can be enabled, disabled, edited or deleted.

### Supported Providers

| Provider | Notes |
| --- | --- |
| **Anthropic Claude** | Needs an API key |
| **OpenAI** | Needs an API key |
| **Google Gemini** | Needs an API key |
| **IBM watsonx.ai** | Needs an API key and a project ID |
| **Ollama (Local)** | Needs a base URL instead of an API key |

### Configuration Fields

| Field | Description |
| --- | --- |
| **Provider** | AI service provider |
| **API Key** | Provider API key, encrypted at rest. Not shown for Ollama. |
| **Model ID** | The model to use. **Available Models** lists the models the provider offers. |
| **Project ID** | IBM watsonx.ai only |
| **Region** | IBM watsonx.ai only. Leave it blank for `us-south`. |
| **Base URL** | Ollama only. Default: `http://localhost:11434` |
| **Max Tokens** | Maximum response length (256 to 100,000) |
| **Temperature** | Response creativity (0 to 2) |

!!! note "Stored URLs are shown without credentials"
    The settings pages show a configuration's base URL without its user information, query or fragment. To remove a credential from a stored URL, clear the field, save, and enter the URL again.

### Other sections

AI Setup also holds the **Model Profile**, **Response Jobs** and **Summaries** settings.

## When a setting cannot be read

When AI Setup cannot read a setting, it shows an error and a **Retry** instead of default values. **Save** stays disabled until a retry succeeds, so a failed read can never be saved over your settings.

## MCP Authentication

The **MCP Authentication** section of AI Setup decides who can connect over MCP. It is shown to holders of `mcp:manage`. See [MCP Configuration](mcp/configuration.md).

## Permissions

| Action | Required Permission |
| --- | --- |
| Open AI Setup and change providers | `ai:manage` |
| Change the MCP mode and manage keys | `mcp:manage` |
