# First Login

After deploying and configuring your WitFoo Appliance, this page guides you through your first login, changing default credentials, and completing the 12-step onboarding wizard.

## Default Credentials

!!! danger "Change All Default Passwords Immediately"
    WitFoo Appliances ship with default credentials that are publicly documented. **You must change these immediately** after first login to prevent unauthorized access.

### SSH Access

| Field | Value |
|-------|-------|
| Username | `witfooadmin` |
| Password | `F00theN0ise!` |

Connect via SSH and change the password:

```bash
ssh witfooadmin@<appliance-ip>
passwd
```

### Web UI Access

| Field | Value |
|-------|-------|
| URL | `https://<appliance-ip>` |
| Email | `admin@witfoo.com` |
| Password | `F00theN0ise!` |

The web UI is accessible via HTTPS on port 443.

!!! danger "Self-Signed Certificate Warning"
    If you are using the default self-signed certificates, your browser will display a security warning. Accept the warning to proceed, and plan to install trusted certificates for production use.

## Changing the Web UI Password

1. Open your browser and navigate to `https://<appliance-ip>`.
2. Log in with the default credentials (`admin@witfoo.com` / `F00theN0ise!`).
3. The onboarding wizard will appear on first login. Step 1 (**Create Admin**) prompts you to create a new admin user with a secure password.
4. After creating your admin account, log out and log back in with your new credentials.
5. Optionally, disable or delete the default `admin@witfoo.com` account from **Admin > Users**.

## Onboarding Wizard

On first login to an Analytics node, a full-screen onboarding wizard guides you through initial platform configuration. The wizard consists of 12 steps organized by priority.

### Step Categories

| Category | Meaning |
|----------|---------|
| **Critical** | Must be completed for the platform to function correctly |
| **Recommended** | Strongly suggested for production deployments |
| **Optional** | Enhance functionality but can be configured later |

!!! tip "Flexible Completion Order"
    Steps can be completed in any order — use the step navigation on the left side of the wizard to jump between steps. However, **Critical steps (0–3) should be completed before using the platform** for security operations.

!!! tip "Persistent Reminders"
    If you skip steps and close the wizard, a persistent banner appears after login reminding you of incomplete configuration. All settings can be changed later from the **Admin** panel.

### Step Overview

| Step | Name | Category | Description |
|------|------|----------|-------------|
| 0 | Welcome | Critical | Organization settings and preferences |
| 1 | Create Admin | Critical | First admin user account |
| 2 | Feature Selection | Critical | Enable/disable platform modules |
| 3 | Data Retention | Critical | Data lifecycle policies |
| 4 | CyberGrid | Optional | Threat intelligence sharing |
| 5 | General Settings Review | Recommended | Confirm organization settings |
| 6 | Business Metrics | Optional | ROI and cost reporting inputs |
| 7 | Compliance Frameworks | Recommended | Regulatory framework selection |
| 8 | Authentication | Recommended | Identity provider configuration |
| 9 | Notifications | Optional | Email and Slack alerting |
| 10 | AI Capabilities | Optional | AI assistant configuration |
| 11 | Summary | — | Completion checklist and launch |

---

### Step 0: Welcome (Critical)

Configure your organization's basic settings and preferences.

| Field | Description |
|-------|-------------|
| **Organization Name** | Display name for your organization (pre-populated from `wfa configure`) |
| **Timezone** | Primary timezone for date/time display across the platform |
| **Date/Time Format** | Choose between 12-hour and 24-hour formats, and date ordering (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD) |
| **Enable Notifications** | Toggle platform-wide notification delivery |

!!! tip "Timezone Matters"
    The timezone setting affects how timestamps are displayed throughout the platform, including in reports and incident timelines. Choose the timezone where your primary SOC operates.

### Step 1: Create Admin (Critical)

Create the first administrative user account. This replaces the default `admin@witfoo.com` account for day-to-day use.

| Field | Description |
|-------|-------------|
| **Full Name** | Administrator's display name |
| **Email** | Login email address (must be unique) |
| **Password** | Minimum 8 characters; strong password recommended |

If an admin user already exists (e.g., from a previous configuration), this step is automatically skipped.

!!! tip "Create a Personal Admin Account"
    Always create a named admin account for audit trail purposes. The default `admin@witfoo.com` account should be disabled after your personal account is created.

### Step 2: Feature Selection (Critical)

Toggle platform modules between three states:

| State | Behavior |
|-------|----------|
| **Full** | Module is fully enabled with UI navigation, background processing, and API access |
| **Background** | Module runs background processing but is hidden from the UI navigation |
| **Disabled** | Module is completely disabled — no processing, no UI, no API |

Available modules:

| Module | Description |
|--------|-------------|
| **Search** | Signal search, graph exploration, and artifact investigation |
| **Observer** | Real-time monitoring dashboards and alert management |
| **Reporter** | Compliance reports, executive summaries, and operational metrics |
| **CyberGrid** | Threat intelligence sharing and IOC enrichment |
| **Responder** | Incident response workflows and playbook automation |
| **AI** | AI-powered analysis assistant and natural language queries |

The wizard automatically resolves dependencies between modules. For example, enabling Reporter requires Search to be at least in Background mode.

### Step 3: Data Retention (Critical)

Configure how long different categories of data are retained in the database. Set retention periods between 1 and 365 days for each feature area.

| Data Type | Default | Description |
|-----------|---------|-------------|
| Artifacts | 7 days | Raw ingested data (logs, events, signals) |
| Work Units | 365 days | Incidents, investigations, cases |
| Work Collections | 365 days | Grouped work items and campaigns |
| Reports | 1,825 days (5 years) | Generated compliance and operational reports |

!!! tip "Disk Space Planning"
    Longer retention periods require more disk space. Monitor disk usage from the **Admin > Health** dashboard and adjust retention policies as needed. For high-volume environments, start with shorter artifact retention and increase as you understand your storage consumption.

### Step 4: CyberGrid (Optional)

Configure participation in WitFoo's CyberGrid threat intelligence network.

| Mode | Description |
|------|-------------|
| **Consumer** | Receive threat intelligence from the CyberGrid network |
| **Contributor** | Share anonymized threat data and receive intelligence |
| **Full** | Full bidirectional sharing with attribution |

Select your participation level or skip this step to disable CyberGrid.

### Step 5: General Settings Review (Recommended)

A read-only confirmation screen displaying the settings configured in Step 0 (Welcome). Review your organization name, timezone, date/time format, and notification preferences.

No input is required — confirm the settings are correct and proceed.

### Step 6: Business Metrics (Optional)

Provide business context for ROI calculations and executive reporting. These values are used by the Reporter module to generate cost-savings and efficiency reports.

| Field | Description |
|-------|-------------|
| **FTE Annual Cost** | Fully loaded cost per full-time security employee |
| **Annual Revenue** | Organization's annual revenue (for risk calculations) |
| **Annual Security Spend** | Total annual security operations budget |
| **Mean Time to Detect** | Average time to detect a security incident (hours) |
| **Mean Time to Respond** | Average time to respond to a security incident (hours) |

!!! tip "Estimate If Unsure"
    These values are used for reporting only and can be updated at any time. Reasonable estimates are better than skipping this step entirely, as they enable ROI dashboards from day one.

### Step 7: Compliance Frameworks (Recommended)

Enable the compliance frameworks relevant to your organization and designate a primary framework.

Available frameworks include industry standards such as:

- CIS Controls (CSC v7, CSC v8)
- NIST Cybersecurity Framework (CSF)
- NIST 800-53
- ISO 27001
- PCI DSS
- HIPAA
- SOC 2

Toggle each framework on or off, then select one as your **primary framework**. The primary framework determines the default compliance view in Reporter dashboards.

### Step 8: Authentication (Recommended)

Configure how users authenticate to the platform.

| Method | Description |
|--------|-------------|
| **Local** | Username/password stored in the WitFoo database |
| **LDAP** | Authenticate against an LDAP or Active Directory server |
| **SAML SSO** | Single sign-on via a SAML 2.0 identity provider |
| **Mixed** | Local accounts for admins, LDAP/SAML for standard users |

For LDAP and SAML configurations, the wizard provides **Test Connection** buttons to validate connectivity before saving.

| LDAP Fields | Description |
|-------------|-------------|
| Server URL | LDAP server address (e.g., `ldaps://ldap.mycompany.com:636`) |
| Bind DN | Distinguished name for LDAP binding |
| Bind Password | Password for the bind DN |
| Search Base | Base DN for user searches |
| User Filter | LDAP filter for user lookup |

| SAML Fields | Description |
|-------------|-------------|
| IdP Metadata URL | URL to the identity provider's SAML metadata |
| Entity ID | Service provider entity ID |
| ACS URL | Assertion Consumer Service URL (auto-populated) |

### Step 9: Notifications (Optional)

Configure notification channels for alerts, incident updates, and system events.

**SMTP Email:**

| Field | Description |
|-------|-------------|
| SMTP Server | Mail server hostname and port |
| From Address | Sender email address |
| Username | SMTP authentication username |
| Password | SMTP authentication password |
| Use TLS | Enable TLS encryption |

**Slack Webhook:**

| Field | Description |
|-------|-------------|
| Webhook URL | Slack incoming webhook URL |
| Default Channel | Channel for notifications (overridden by webhook config) |

Both channels provide a **Test Send** button to verify configuration before saving.

### Step 10: AI Capabilities (Optional)

Configure the AI assistant for natural language investigation queries and automated analysis.

| Field | Description |
|-------|-------------|
| **AI Provider** | Select from Anthropic, OpenAI, or Google |
| **API Key** | Your API key for the selected provider |
| **Model** | Specific model to use (e.g., `claude-sonnet-4-20250514`, `gpt-4o`) |
| **Temperature** | Response creativity (0.0 = deterministic, 1.0 = creative) |
| **Max Tokens** | Maximum response length |

!!! tip "AI API Keys"
    AI features require an API key from a supported provider. Your API key is encrypted at rest and never shared. You can change providers or disable AI at any time from **Admin > AI Settings**.

### Step 11: Summary

The final step displays a progress checklist showing the completion status of all previous steps.

| Element | Description |
|---------|-------------|
| **Step Checklist** | Each step shown with ✅ (complete) or ⚠️ (skipped/incomplete) |
| **Completion Percentage** | Overall configuration progress |
| **Launch Platform** | Button to close the wizard and enter the platform |

Clicking **Launch Platform** closes the wizard and takes you to the main dashboard. Any incomplete steps will trigger a persistent banner reminder.

!!! tip "All Settings Are Editable"
    Every setting configured in the onboarding wizard can be modified later from the **Admin** panel. The wizard is a convenience for initial setup — it does not lock in any configuration permanently.