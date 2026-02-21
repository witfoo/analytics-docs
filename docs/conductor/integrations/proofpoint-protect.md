---
tags:
  - integration
  - email
---

# Proofpoint Protect

Collects email threat events from Proofpoint Email Protection, providing
visibility into targeted attacks, phishing campaigns, malware delivery,
and email-borne threats.

| | |
|---|---|
| **Category** | Email Security |
| **Connector Name** | `signal-client.proofpoint-protect` |
| **Auth Method** | Service Principal + Secret (Basic Auth) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Proofpoint SIEM API](https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Proofpoint Email Protection subscription with TAP (Targeted Attack
    Protection). Admin access required to create service principals.

- [ ] Active Proofpoint Email Protection subscription with TAP
- [ ] Admin access in the Proofpoint TAP Dashboard
- [ ] Network: Conductor can reach `tap-api-v2.proofpoint.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Proofpoint TAP Dashboard** at `https://threatinsight.proofpoint.com/`
2. Navigate to **Settings** → **Connected Applications**
3. Click **Create New Credential**
4. Configure the credential:
    - **Name**: `WitFoo Conductor`
    - **Type**: Service Principal
5. Copy the **Service Principal** and **Secret**

!!! warning "Store Credentials Securely"
    API credentials grant access to your Proofpoint email threat data. Store
    them securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Proofpoint Protect**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Service Principal** | `<your-service-principal>` | Service principal from step 1 |
    | **Secret** | `<your-secret>` | Secret from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "proofpoint-protect"
    ```

    Look for successful poll messages:
    ```
    [INFO] proofpoint-protect: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Service Principal** and **Secret** are correct
- Ensure the credential has not been revoked in the TAP Dashboard

### Forbidden (403)

- The service principal may lack access to the SIEM API
- Contact your Proofpoint administrator to verify permissions

### Rate Limited (429)

- Proofpoint TAP API is limited to certain requests per minute
- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://tap-api-v2.proofpoint.com`
- Confirm threat events exist in the Proofpoint TAP Dashboard for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
