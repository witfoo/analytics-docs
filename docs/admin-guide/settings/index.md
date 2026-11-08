# Settings

System-wide configuration for WitFoo Analytics.

## Access

Open **Settings** (the gear icon in the page header) > **General Settings**. The settings pages are listed down the left side: **System Settings**, **Incident Naming**, **Authentication**, **Notifications**, **Notification Rules**, **Certificates**, **Branding**, **Business Metrics**, **Frameworks**, **AI Setup** and **Onboarding Wizard**.

The API behind these pages needs `settings:read` to read a setting and `settings:manage` to change it. Some pages check more: **AI Setup** needs `ai:manage`, and changing which frameworks are enabled needs `frameworks:write`.

## Settings Pages

### [Business Metrics](business-metrics.md)

Configure financial and operational metrics used by the Reporter module. Saving changes only the figures you send: per-product costs and the language of AI responses are kept.

### [Frameworks](frameworks.md)

Enable compliance frameworks and set the primary framework.

### [Authentication](authentication.md)

Configure LDAP, SAML, and local authentication settings. SAML and LDAP settings are saved only on this page.

### [SAML SSO](authentication.md)

Step-by-step guide for enabling SAML 2.0 SSO with Okta, Azure AD, Google Workspace, and other IdPs.

### [Notifications](notifications.md)

Set up email, Slack, and webhook notification channels.

### [Certificates](certificates.md)

Manage TLS certificates for HTTPS and internal service communication.

### AI Setup

Configure AI providers, routing, the AI profile and response automation, and MCP. The MCP sections of this page (**MCP Authentication**, **MCP Server Settings** and the relay card) are described in [MCP Configuration](../../ai/mcp/configuration.md).

## How the settings pages behave

- **Read failures are shown.** When a page cannot read its settings, it shows an error, a dash or a notice instead of default values or zeros. **System Settings** and **AI Setup** offer **Retry** and keep **Save** disabled until a retry succeeds. **Business Metrics** shows an error with **Retry**, and no **Save**, until the figures can be read.
- **Confirmation dialogs do not run on Enter.** A dialog with a red confirm button (Delete, Disable, Remove, Reset, Reboot Now and similar) does not submit on Enter, even while **Cancel** has focus. Click the confirm button to run the action.
