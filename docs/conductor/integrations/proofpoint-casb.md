---
tags:
  - integration
  - email
---

# Proofpoint CASB

Collects cloud application security events from Proofpoint CASB (Cloud App
Security Broker), providing visibility into SaaS application threats,
compromised accounts, and data loss prevention events.

| | |
|---|---|
| **Category** | Email Security |
| **Connector Name** | `signal-client.proofpoint-casb` |
| **Auth Method** | Client ID + Client Secret + API Key (OAuth2) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Proofpoint CASB API](https://help.proofpoint.com/Proofpoint_CASB/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Proofpoint CASB subscription. Admin access required to generate
    API credentials.

- [ ] Active Proofpoint CASB subscription
- [ ] Admin access in the Proofpoint CASB console
- [ ] Network: Conductor can reach the Proofpoint CASB API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to the **Proofpoint CASB Console**
2. Navigate to **Settings** → **API Integrations**
3. Click **Create New API Credential**
4. Configure the credential:
    - **Name**: `WitFoo Conductor`
    - **Permissions**: Read-only access
5. Copy the **Client ID**, **Client Secret**, and **API Key**

!!! warning "Store Credentials Securely"
    API credentials grant access to your Proofpoint CASB data. Store them
    securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Proofpoint CASB**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `<api-endpoint>` | Proofpoint CASB API endpoint |
    | **Client ID** | `<your-client-id>` | Client ID from step 1 |
    | **Secret** | `<your-client-secret>` | Client secret from step 1 |
    | **API Key** | `<your-api-key>` | API key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "proofpoint-casb"
    ```

    Look for successful poll messages:
    ```
    [INFO] proofpoint-casb: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID**, **Client Secret**, and **API Key** are correct
- Ensure the credentials have not been revoked

### Forbidden (403)

- The API credential may lack read permissions
- Contact your Proofpoint CASB administrator to verify permissions

### Rate Limited (429)

- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity to the Proofpoint CASB API endpoint
- Confirm events exist in the Proofpoint CASB console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
