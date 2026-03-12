# Localization

WitFoo Analytics supports multiple languages for the user interface, notifications, and AI-generated content.

## Supported Locales

| Locale Code | Language | Direction | Status |
| --- | --- | --- | --- |
| `en` | English | LTR | Default |
| `es` | Spanish (Espa&ntilde;ol) | LTR | Complete |
| `fr` | French (Fran&ccedil;ais) | LTR | Complete |
| `de` | German (Deutsch) | LTR | Complete |
| `ja` | Japanese (&#26085;&#26412;&#35486;) | LTR | Complete |
| `ar` | Arabic (&#1575;&#1604;&#1593;&#1585;&#1576;&#1610;&#1577;) | RTL | Complete |
| `mi` | Te Reo M&#257;ori | LTR | Complete |

All 7 locales have consistent translation keys with matching parameter placeholders, validated by automated tests.

## Changing Your Locale

Users can change their display language from the profile menu:

1. Click your **user avatar** in the top-right corner
2. Select **Profile**
3. Under **Language**, choose your preferred locale from the dropdown
4. The page reloads automatically with the selected language applied

The locale preference is stored per user and persists across sessions.

## AI Language Awareness

WitFoo's AI features automatically respond in the user's selected locale:

### Interactive Features

When a user interacts with AI-powered features (summaries, chat), the frontend passes the user's current locale to the backend. The AI system appends a language instruction to the end of its system prompt, ensuring responses are generated in the appropriate language.

- **AI Summaries**: Work unit and incident summaries are generated in the requesting user's locale
- **AI Chat**: Chat responses match the user's display language
- **English default**: When the locale is English, no additional language instruction is added (English is the base language for all prompts)

### Background AI Tasks

For automated AI tasks that run without a user session (such as playbook analysis), the system uses the organization's **Default Locale** setting:

1. Navigate to **Admin** > **Settings** > **Business Metrics**
2. Set the **Default Locale** field to the preferred language for background AI output
3. All automated playbook analyses and AI-generated reports will use this locale

!!! info "Default Locale Scope"
    The Default Locale setting in Business Metrics applies only to background AI tasks (e.g., automated playbook analysis). Interactive AI features always use the individual user's locale preference.

## Translation Coverage

All user-facing strings in the application are internationalized, including:

- Navigation menus and page titles
- Form labels, buttons, and validation messages
- Notification titles and descriptions
- Signal search facets and filter labels
- CyberGrid publications, subscriptions, and modals
- Reporter chart titles and data labels
- Admin settings pages
- Error messages and status indicators

!!! tip "Reporting Translation Issues"
    If you encounter untranslated text or incorrect translations, report the issue through the WitFoo support channel. Include the locale, the page where the issue appears, and the text in question.
