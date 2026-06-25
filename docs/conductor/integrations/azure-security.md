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
8. Navigate to **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**, and add the following **ten** application permissions (all read-only):

    | Permission | Unlocks |
    |------------|---------|
    | `SecurityIncident.Read.All` | Defender incidents |
    | `SecurityAlert.Read.All` | Defender alerts (v2) |
    | `AuditLog.Read.All` | Entra ID sign-in **and** directory audit logs |
    | `IdentityRiskEvent.Read.All` | Identity Protection risk detections |
    | `IdentityRiskyUser.Read.All` | Identity Protection risky users |
    | `SecurityEvents.Read.All` | Microsoft Secure Score |
    | `SignInIdentifier.Read.All` | User Identifiers |
    | `DeviceManagementManagedDevices.Read.All` | Intune managed-device & detected-app inventory (CSC8 2/4) |
    | `User.Read.All` | Entra ID user-account inventory (CSC8 5) |
    | `Device.Read.All` | Entra ID registered/joined device inventory |

    !!! note "Inventory licensing"
        User **sign-in activity** (`signInActivity` on `/users`) additionally requires
        **Entra ID P1/P2** plus `AuditLog.Read.All`. The optional
        `DeviceManagementConfiguration.Read.All` unlocks Intune compliance/configuration
        policy detail for control 4. These inventory pulls are snapshots on an hourly
        cadence and **auto-disable** if the tenant lacks the license/permission — the rest
        keep flowing.

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

    ```text
    [INFO] azure-security: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

### Data Collection Details

Each polling cycle, the connector pulls **twelve** Microsoft Graph v1.0 endpoints.
Every endpoint is collected independently: if your tenant is not licensed or
permissioned for one, only that endpoint is skipped (and reported as unavailable)
— the rest keep flowing. The four **inventory** endpoints are *snapshots* (the full
list is re-pulled on an hourly cadence, not every cycle).

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
| Managed devices *(snapshot)* | `/deviceManagement/managedDevices` | Intune device inventory + compliance state | `DeviceManagementManagedDevices.Read.All` | Microsoft Intune |
| Detected apps *(snapshot)* | `/deviceManagement/detectedApps` | Intune installed-software inventory | `DeviceManagementManagedDevices.Read.All` | Microsoft Intune |
| Entra users *(snapshot)* | `/users` | User-account inventory (enabled, last sign-in) | `User.Read.All` (+ `AuditLog.Read.All`) | Entra ID (P1/P2 for sign-in activity) |
| Entra devices *(snapshot)* | `/devices` | Registered/joined device inventory | `Device.Read.All` | Entra ID |

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

Grant these **ten** Microsoft Graph **application** permissions (admin-consented)
for full coverage of all twelve checks. `*.Read.All` is read-only and
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
| `DeviceManagementManagedDevices.Read.All` | Application | Managed devices **and** detected apps (Intune inventory) |
| `User.Read.All` | Application | Entra ID user-account inventory |
| `Device.Read.All` | Application | Entra ID registered/joined device inventory |

All ten require **admin consent**, and Microsoft does not apply a permission
change until an administrator re-consents.

!!! info "License-gated checks are expected, not errors"
    Some checks require a specific Microsoft license. Without **Entra ID P2**,
    *Risk detections* and *Risky users* are unavailable; without **P1**,
    *Sign-in logs*; without a **Defender** product, *Incidents* and *Alerts*.
    The connector keeps every licensed and permissioned check flowing and reports
    the rest as unavailable with the reason — add the matching license **and**
    confirm the permission is consented to enable a gated check.

## Phishing & Email Security

Microsoft Defender for Office 365 raises email-threat alerts on the v2 alerts endpoint
(`/security/alerts_v2`). WitFoo classifies each one into a `message_type`, and the analytics
**Phishing** detection chain turns the phishing ones into **work units** — no extra configuration
is required beyond the `SecurityAlert.Read.All` permission and a **Defender for Office 365 (Plan 1
or Plan 2)** license (Safe Links, ZAP, and anti-phishing generate these alerts).

| Defender for O365 signal | WitFoo `message_type` | Outcome |
|--------------------------|------------------------|---------|
| Email-threat alert with a **phishing** verdict — `ZapPhish` / `HighConfPhish` / `Phish` in the message threats (or a phishing threat family). Titles like *"Email messages removed after delivery"* or *"Messages containing malicious entity not removed after delivery"*. | `phishing_email` | Matches lead rule 13 → **Phishing** Modus Operandi → a phishing **work unit**. |
| **Safe Links time-of-click** alert — a user actually clicked a malicious URL. Defender's *"A potentially malicious URL click was detected"* / *"…clicked through to a potentially malicious URL"*. | `phishing_click` | Matches lead rule 14 → **Phishing** Modus Operandi → a phishing **work unit**. |
| Spam-foldered or benign delivered email (`Spam`-only threats, or no threat) — *"Email message received"*, delivered to inbox/junk. | `email_protection` | Email-protection telemetry — **not** phishing; does **not** create a phishing work unit. |

Each phishing artifact carries the email context already extracted from the alert evidence — the
**sender**, **subject**, and **recipient** (from the Mailbox/Message evidence), the embedded or
clicked **URLs**, the delivery disposition (delivered / blocked / quarantined, including ZAP
auto-purge), and the connector's `remediation_status`/`verdict` signals — plus a `phishing` tag for
filtering. The resulting **Phishing** work unit groups these so an analyst sees who was targeted,
what was sent, whether the user clicked, and how Defender disposed of it.

!!! info "phishing_click requires a Safe Links click"
    A `phishing_click` classification means Defender recorded a **user click** on a malicious URL
    (Safe Links time-of-click protection), which is distinct from a malicious URL merely *present in
    a delivered email* (that classifies as `phishing_email`). Click alerts appear only when Safe
    Links is enabled **and** a user actually clicked, so a tenant may see `phishing_email` work units
    long before any `phishing_click` ones.

    WitFoo distinguishes the two from the **alert title** — Defender's documented click-alert phrasing
    (*"…URL click was detected"* / *"…clicked through to a potentially malicious URL"*) classifies as
    `phishing_click`; every other Defender for O365 email-threat alert with a phishing verdict
    classifies as `phishing_email`.

This phishing coverage maps to **CSC8 Control 9 — Email & Web Browser Protections** (below).

## CSC8 Compliance Coverage

Once the Azure connector is collecting and the data reaches Analytics, these CIS Controls v8
(`csc8`) controls populate on the **Compliance Reporting** page, each attributed to the
detecting Microsoft product:

| CSC8 Control | Detecting product | Microsoft data source |
|--------------|-------------------|-----------------------|
| 1 — Inventory & Control of Enterprise Assets | Microsoft Defender | Defender for Endpoint device coverage (Intune/Entra device inventory supplements) |
| 2 — Inventory & Control of Software Assets | Microsoft Intune | Detected apps |
| 4 — Secure Configuration | Microsoft Intune | Managed-device compliance state |
| 5 — Account Management | Microsoft Entra ID | User accounts |
| 6 — Access Control Management | Microsoft Entra ID | Sign-in / directory audit |
| 7 — Continuous Vulnerability Management | Microsoft Defender | Defender for Endpoint alerts |
| 9 — Email & Web Browser Protections | Microsoft Defender | Defender for Office 365 alerts |
| 10 — Malware Defenses | Microsoft Defender | Defender Antivirus / Endpoint alerts |

!!! note "Coverage appears once the product is detected"
    A control lights up only when its Microsoft product is **detected in your environment**
    (data flowing). Controls 1/5/6/7/9/10 activate from the Defender and Entra streams already
    collected above; controls **2** and **4** require the Intune device/app inventory
    permission (`DeviceManagementManagedDevices.Read.All`) so the inventory snapshots flow. If
    a control still shows *"No detection configured"*, confirm the integration is connected and
    the relevant permission is admin-consented — see
    [Common Troubleshooting](common-troubleshooting.md).

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
