---
tags:
  - integration
  - cloud
---

# Azure Security

Collects security alerts and incidents from Microsoft Azure Security services
including Microsoft Defender for Cloud, Sentinel, and Entra ID, providing
visibility into cloud workload protection and identity threats.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.azure-security` |
| **Auth Method** | OAuth2 (Azure AD — Client ID + Client Secret + Tenant ID) |
| **Polling Interval** | 5 min (alerts), 15 min (incidents) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Microsoft Graph Security API](https://learn.microsoft.com/en-us/graph/api/resources/security-api-overview) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Microsoft Azure subscription with Microsoft Defender for Cloud or
    Microsoft 365 Defender. Azure AD admin access required to register an
    application.

- [ ] Active Azure subscription with security services enabled
- [ ] Global Administrator or Application Administrator role in Azure AD
- [ ] Network: Conductor can reach `graph.microsoft.com` and `login.microsoftonline.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Azure Portal** at `https://portal.azure.com/`
2. Navigate to **Azure Active Directory** → **App registrations** → **New registration**
3. Configure the application:
    - **Name**: `WitFoo Conductor`
    - **Supported account types**: Accounts in this organizational directory only
4. Click **Register**
5. Note the **Application (client) ID** and **Directory (tenant) ID** from the overview page
6. Navigate to **Certificates & secrets** → **New client secret**
    - **Description**: `WitFoo Conductor`
    - **Expires**: 24 months (recommended)
7. Copy the **Value** (client secret) — it is only shown once
8. Navigate to **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**
    - Add: `SecurityEvents.Read.All`
    - Add: `SecurityAlert.Read.All` (for v2 alerts)
9. Click **Grant admin consent** for your organization

!!! warning "Store Credentials Securely"
    The client secret grants access to your Azure security data. Store it
    securely and do not share it in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Azure Security**
3. Enter a unique name for this instance (e.g., "Azure Production Tenant")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Tenant ID** | `<your-tenant-id>` | Azure AD directory (tenant) ID |
    | **Client ID** | `<your-client-id>` | Application (client) ID from app registration |
    | **Client Secret** | `<your-client-secret>` | Secret value from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for alerts)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "azure"
    ```

    Look for successful poll messages:
    ```
    [INFO] azure-security: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

### Data Collection Details

The Azure Security connector collects data from two Microsoft Graph API
versions:

| Endpoint | Version | Interval | Description |
|----------|---------|----------|-------------|
| Security Alerts | v1 | 5 min | Microsoft Defender for Cloud alerts |
| Security Alerts v2 | v2 | 5 min | Enhanced alerts with typed evidence |
| Incidents | v1 | 15 min | Correlated incident data from Sentinel |

#### V2 Alert Evidence Types

The v2 alerts endpoint (`/security/alerts_v2`) returns structured evidence
objects. The connector processes these typed evidence payloads:

| Evidence Type | Description |
|---------------|-------------|
| **Mailbox** | Compromised or targeted mailbox details |
| **Message** | Email message artifacts (subject, sender, recipients) |
| **URL** | Suspicious or malicious URL indicators |
| **MailCluster** | Grouped email cluster analysis data |

Pagination is handled automatically via `@odata.nextLink` response links.

!!! info "Rate Limiting Behavior"
    Microsoft Graph API returns HTTP 429 with a `Retry-After` header.
    The connector implements a **10-minute cooldown** with context-aware
    retry on 429 responses. HTTP 403 responses are handled silently
    (permission warning logged) to prevent blocking other data collection.

### Required API Permissions

| Permission | Type | Purpose |
|------------|------|--------|
| `SecurityEvents.Read.All` | Application | Read security events (v1 API) |
| `SecurityAlert.Read.All` | Application | Read security alerts (v2 API) |

Both permissions require **admin consent** to be granted.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Tenant ID**, **Client ID**, and **Client Secret** are correct
- Ensure the client secret has not expired
- Check that the app registration exists in the correct Azure AD tenant

### Forbidden (403)

- The app registration may lack required API permissions
- Required: `SecurityEvents.Read.All` and `SecurityAlert.Read.All`
- Ensure **admin consent** has been granted for the permissions

### Rate Limited (429)

- Microsoft Graph API has per-app and per-tenant throttling limits
- Increase the **Polling Interval** to 10 minutes if rate limiting occurs
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://graph.microsoft.com`
- Confirm security alerts exist in the Azure Security Center for the polling time window
- Ensure Microsoft Defender for Cloud or another security service is generating alerts

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
