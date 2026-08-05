---
tags:
  - integration
  - cloud
---

# Microsoft Sentinel

Pulls security incidents from a Microsoft Sentinel workspace via the Azure
Management (ARM) incidents API, bringing Sentinel's correlated incident data —
including incidents raised by your Sentinel analytics rules — into the WitFoo
pipeline.

| | |
|---|---|
| **Category** | Cloud Security / SIEM |
| **Connector Name** | `signal-client.ms-sentinel` |
| **Auth Method** | OAuth2 client credentials (Azure AD — Tenant ID + Client ID + Client Secret) |
| **Token Scope** | `https://management.azure.com/.default` |
| **Polling Interval** | 5 min default (configurable) |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [Microsoft Sentinel Incidents REST API](https://learn.microsoft.com/en-us/rest/api/securityinsights/incidents) |

!!! info "This is the PULL connector"
    This page covers pulling incidents **from** Sentinel into WitFoo. For
    pushing WitFoo detections and dashboards **to** Sentinel, see
    [Microsoft Sentinel detection rules](../../detection-rules/platforms/sentinel.md).
    For collecting Defender XDR / Entra ID telemetry via Microsoft Graph, see
    [Azure Security](azure-security.md) — a separate connector with different
    permissions.

## Prerequisites

!!! note "Vendor Requirements"
    A Microsoft Sentinel workspace (Log Analytics workspace with Sentinel
    enabled). Azure AD access sufficient to register an application and assign
    an Azure RBAC role on the workspace's resource group.

- [ ] Microsoft Sentinel enabled on a Log Analytics workspace
- [ ] Permission to register an Azure AD application and assign RBAC roles
- [ ] Network: Conductor can reach `management.azure.com` and `login.microsoftonline.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Azure Portal** at `https://portal.azure.com/`
2. Navigate to **Microsoft Entra ID** → **App registrations** → **New registration**
3. Configure the application:
    - **Name**: `WitFoo Conductor Sentinel`
    - **Supported account types**: Accounts in this organizational directory only
4. Click **Register**
5. Note the **Application (client) ID** and **Directory (tenant) ID** from the overview page
6. Navigate to **Certificates & secrets** → **New client secret**
    - **Description**: `WitFoo Conductor Sentinel`
    - **Expires**: 24 months (recommended)
7. Copy the secret **Value** — it is only shown once

!!! warning "Secret Value, not Secret ID"
    Copy the secret **Value** column, not the **Secret ID** (a GUID). Pasting
    the Secret ID is the most common setup mistake and fails with
    `AADSTS7000215: Invalid client secret provided`.

## Step 2: Assign the Azure RBAC Role

!!! info "No Graph API permissions needed"
    Unlike [Azure Security](azure-security.md), this connector needs **no
    Microsoft Graph API permissions and no admin consent**. Authorization is
    entirely through Azure RBAC: one role assignment on the resource group.

1. Navigate to the **resource group** that contains your Sentinel workspace
2. Open **Access control (IAM)** → **Add** → **Add role assignment**
3. Role: **Microsoft Sentinel Reader**
4. Assign access to: **User, group, or service principal** → select the
   `WitFoo Conductor Sentinel` app registration
5. Click **Review + assign**

!!! warning "RBAC propagation can take up to 60 minutes"
    Azure role assignments can take up to an hour to propagate. A `403
    AuthorizationFailed` immediately after assignment is expected — wait and
    let the connector retry before changing anything.

## Step 3: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Microsoft Sentinel**
3. Enter a unique name for this instance (e.g., "Sentinel Production")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Tenant ID** | `<your-tenant-id>` | Azure AD directory (tenant) ID |
    | **Client ID** | `<your-client-id>` | Application (client) ID from Step 1 |
    | **Client Secret** | `<your-client-secret>` | Secret **Value** from Step 1 |
    | **Subscription ID** | `<your-subscription-id>` | Subscription containing the workspace |
    | **Resource Group** | `<your-resource-group>` | Resource group containing the workspace |
    | **Workspace Name** | `<your-workspace-name>` | Log Analytics workspace **name** (not the workspace GUID) |

5. Toggle **Enabled** to on
6. Click **Save**

## Step 4: Validate Data Flow

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 2>&1 | grep -i sentinel
    ```

    Look for: `successfully authenticated with sentinel client`

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

The connector checkpoints on incident `lastModifiedTimeUtc`, so each poll
fetches only incidents created or modified since the previous poll.

## Troubleshooting

### AADSTS7000215: Invalid client secret provided

- The configured secret is the **Secret ID** (a GUID), not the secret
  **Value**. Create a new client secret and paste the **Value** column —
  the value is only visible at creation time.
- On Conductor releases before 1.8.2 the sibling Azure Security connector
  showed **no error at all** for this mistake — upgrade and the failure
  becomes visible in integration health with this exact hint.

### Authentication Failed (401)

- Verify the **Tenant ID**, **Client ID**, and **Client Secret** are correct
- Ensure the client secret has not expired
- Check that the app registration exists in the correct Azure AD tenant

### AuthorizationFailed (403)

The token was issued but the service principal cannot read Sentinel incidents:

```json
{"error":{"code":"AuthorizationFailed","message":"The client '<appId>' with object id '<oid>' does not have authorization to perform action 'Microsoft.SecurityInsights/incidents/read' over scope '/subscriptions/…/resourceGroups/…'"}}
```

- Assign **Microsoft Sentinel Reader** on the workspace's **resource group**
  (Step 2) — a Graph permission or a role on a different scope does not grant this
- If the role was just assigned, wait for RBAC propagation (up to 60 minutes)
- Verify the **Subscription ID**, **Resource Group**, and **Workspace Name**
  point at the workspace that actually holds the role assignment

### Rate Limited (429)

- The Azure Management API throttles per-principal and per-subscription
- The connector cools down for 10 minutes and resumes automatically
- Increase the **Polling Interval** if throttling recurs

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://management.azure.com`
- Confirm incidents exist in **Sentinel → Threat management → Incidents** for
  the polling window — the connector pulls incidents, not raw log rows

---

*See also: [Integration Catalog](index.md) ·
[Azure Security](azure-security.md) ·
[Sentinel detection rules (push)](../../detection-rules/platforms/sentinel.md) ·
[Integration Management](../ui/integrations.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
