---
tags:
  - integration
  - cloud
---

# Wiz

Collects cloud security findings from Wiz, including misconfigurations,
vulnerabilities, and threat detections across multi-cloud environments
(AWS, Azure, GCP, OCI).

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.wiz` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 5 min (issues), 30 min (vulnerabilities) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Wiz API Documentation](https://docs.wiz.io/wiz-docs/docs/using-the-wiz-api) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Wiz subscription. Admin access required to create service accounts.

- [ ] Active Wiz subscription
- [ ] Admin access to the Wiz console
- [ ] Network: Conductor can reach your Wiz regional API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to **Wiz** at `https://app.wiz.io/`
2. Navigate to **Settings** → **Service Accounts**
3. Click **Create Service Account**
4. Name the account (e.g., "WitFoo Conductor")
5. Assign scopes: `read:resources` and `read:issues`
6. Click **Create**
7. Copy the **Client ID** and **Client Secret**

!!! info "Regional API Endpoints"
    Wiz uses regional API endpoints. Select the correct one for your
    tenant:

    | Region | API Endpoint | Auth Endpoint |
    |--------|-------------|---------------|
    | US | `api.us1.app.wiz.io` | `auth.app.wiz.io` |
    | EU | `api.eu1.app.wiz.io` | `auth.app.wiz.io` |
    | US 2 | `api.us2.app.wiz.io` | `auth.app.wiz.io` |

    If unsure, check your browser's address bar when logged into Wiz.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Wiz**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **API Endpoint** | `api.us1.app.wiz.io` | Regional API URL (see table) |
    | **Auth Endpoint** | `auth.app.wiz.io` | OAuth2 token endpoint |
    | **Client ID** | `<your-client-id>` | From step 1 |
    | **Client Secret** | `<your-client-secret>` | From step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for issues)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "wiz"
    ```

    Look for successful poll messages:
    ```
    [INFO] wiz: fetched <N> issues
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the service account has not been deleted in Wiz
- Check the **Auth Endpoint** is correct (`auth.app.wiz.io`)

### Forbidden (403)

- The service account may lack required scopes
- Verify `read:resources` and `read:issues` are assigned

### Wrong API Endpoint

- If you see connection errors, verify the **API Endpoint** matches your
  Wiz region (US, EU, etc.)
- The API endpoint is different from the console URL

### Rate Limited (429)

- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Ensure cloud accounts are connected in Wiz (Settings → Cloud Accounts)
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify there are active issues in the Wiz console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
