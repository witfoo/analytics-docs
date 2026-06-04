---
tags:
  - integration
  - cloud
---

# Azure Security

Collects security and identity telemetry from Microsoft Azure via the Microsoft
Graph API — Defender XDR incidents and alerts, Entra ID sign-in and directory
audit logs, Identity Protection risk detections and risky users, and Microsoft
Secure Score — providing visibility into cloud workload protection and identity
threats.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.azure-security` |
| **Auth Method** | OAuth2 (Azure AD — Client ID + Client Secret + Tenant ID) |
| **Polling Interval** | 5 min default (configurable) |
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
8. Navigate to **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**, and add the following **seven** application permissions (all read-only):

    | Permission | Unlocks |
    |------------|---------|
    | `SecurityIncident.Read.All` | Defender incidents |
    | `SecurityAlert.Read.All` | Defender alerts (v2) |
    | `AuditLog.Read.All` | Entra ID sign-in **and** directory audit logs |
    | `IdentityRiskEvent.Read.All` | Identity Protection risk detections |
    | `IdentityRiskyUser.Read.All` | Identity Protection risky users |
    | `SecurityEvents.Read.All` | Microsoft Secure Score |
    | `SignInIdentifier.Read.All` | User Identifiers |

9. Click **Grant admin consent for your tenant** and confirm every row shows **Granted**. Application permissions require admin consent, and any later change requires re-consent.

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

Each polling cycle, the connector pulls **eight** Microsoft Graph v1.0 endpoints.
Every endpoint is collected independently: if your tenant is not licensed or
permissioned for one, only that endpoint is skipped (and reported as unavailable)
— the rest keep flowing.

| Check | Graph endpoint | Data | Required permission | License |
|-------|----------------|------|---------------------|---------|
| Incidents | `/security/incidents` | Correlated Defender XDR incidents | `SecurityIncident.Read.All` | Microsoft Defender XDR |
| Alerts (v2) | `/security/alerts_v2` | Defender alerts with typed evidence | `SecurityAlert.Read.All` | A Microsoft Defender product |
| Sign-in logs | `/auditLogs/signIns` | Entra ID interactive sign-ins | `AuditLog.Read.All` | Entra ID **P1** or **P2** |
| Directory audits | `/auditLogs/directoryAudits` | Entra ID directory change audit | `AuditLog.Read.All` | Entra ID (any; P1/P2 for 30-day retention) |
| Risk detections | `/identityProtection/riskDetections` | Identity Protection risk events | `IdentityRiskEvent.Read.All` | Entra ID **P2** |
| Risky users | `/identityProtection/riskyUsers` | Identity Protection risky users | `IdentityRiskyUser.Read.All` | Entra ID **P2** |
| Secure Score | `/security/secureScores` | Microsoft Secure Score posture | `SecurityEvents.Read.All` | Microsoft 365 / Defender |
| User Identifiers | `/users` | Identifier-related fields | `SignInIdentifier.Read.All` | Entra ID (any) / Microsoft 365 E5 |

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

Grant these **seven** Microsoft Graph **application** permissions (admin-consented)
for full coverage of all eight checks. `*.Read.All` is read-only and
least-privilege, so the `*.ReadWrite.All` variants are never required.

| Permission | Type | Unlocks |
|------------|------|---------|
| `SecurityIncident.Read.All` | Application | Incidents |
| `SecurityAlert.Read.All` | Application | Alerts (v2) |
| `AuditLog.Read.All` | Application | Sign-in logs **and** directory audits |
| `IdentityRiskEvent.Read.All` | Application | Risk detections |
| `IdentityRiskyUser.Read.All` | Application | Risky users |
| `SecurityEvents.Read.All` | Application | Secure Score |
| `SignInIdentifier.Read.All` | Application | User Identifiers |

All seven require **admin consent**, and Microsoft does not apply a permission
change until an administrator re-consents.

!!! info "License-gated checks are expected, not errors"
    Some checks require a specific Microsoft license. Without **Entra ID P2**,
    *Risk detections* and *Risky users* are unavailable; without **P1**,
    *Sign-in logs*; without a **Defender** product, *Incidents* and *Alerts*.
    The connector keeps every licensed and permissioned check flowing and reports
    the rest as unavailable with the reason — add the matching license **and**
    confirm the permission is consented to enable a gated check.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Tenant ID**, **Client ID**, and **Client Secret** are correct
- Ensure the client secret has not expired
- Check that the app registration exists in the correct Azure AD tenant

### Forbidden (403) on one or more checks

- A 403 affects only the specific check whose permission or license is missing —
  the other checks keep collecting.
- Confirm the matching **application permission** from the table above is added
  **and** that **admin consent** has been (re-)granted — a permission added without
  re-consent still returns 403.
- If the permission is consented, confirm the tenant holds the required **license**
  for that check (Entra ID P1/P2, or a Defender product).

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
