---
tags:
  - integration
  - endpoint
---

# Carbon Black

Collects endpoint alerts and device inventory from VMware Carbon Black Cloud
(now Broadcom), including malware detections, suspicious activity alerts, and
endpoint asset data.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.carbon-black` |
| **Auth Method** | API Key + API ID (X-Auth-Token) |
| **Polling Interval** | 5 min (alerts), 1 hr (devices) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Carbon Black Cloud API](https://developer.carbonblack.com/reference/carbon-black-cloud/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Carbon Black Cloud subscription. Administrator access required
    to create API keys.

- [ ] Active Carbon Black Cloud subscription
- [ ] Administrator access to the CBC console
- [ ] Organization Key (found in console settings)
- [ ] Network: Conductor can reach your CBC instance on port 443

## Step 1: Create API Credentials

1. Log in to the **Carbon Black Cloud Console** at
   `https://defense.conferdeploy.net/` (or your regional instance)
2. Navigate to **Settings** → **API Access**
3. Click **Add API Key**
4. Select **Custom** as the access level type
5. Set permissions: `org.alerts: READ`
6. Name the key (e.g., "WitFoo Conductor")
7. Click **Save**
8. Copy the **API ID** and **API Secret Key**
9. Note the **Org Key** from **Settings** → **API Access** (shown at the top)

!!! warning "API Key Types"
    Carbon Black Cloud has multiple API key types: **API**, **SIEM**, and
    **Custom**. Use **Custom** type with specific read permissions for
    WitFoo integration. SIEM keys provide different endpoint access.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Carbon Black**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `defense.conferdeploy.net` | CBC console URL (varies by region) |
    | **Org Key** | `<your-org-key>` | Organization key from API Access page |
    | **API Key** | `<your-api-secret-key>` | API secret key from step 1 |
    | **API ID** | `<your-api-id>` | API ID from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for alerts)
6. Toggle **Enabled** to on
7. Click **Save**

!!! tip "Finding Your Org Key"
    The Org Key is displayed at the top of the **Settings → API Access**
    page in the Carbon Black Cloud console. It is a short alphanumeric
    string (e.g., `ABCD1234`).

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "carbon-black"
    ```

    Look for successful poll messages:
    ```
    [INFO] carbon-black: fetched <N> alerts
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **API ID** and **API Secret Key** are correct
- Ensure the header format is correct: `X-Auth-Token: <API_SECRET_KEY>/<API_ID>`
- Confirm the API key has not been revoked

### Forbidden (403)

- The API key may not have the required permissions
- Verify `org.alerts: READ` is granted on the Custom API key
- Check that the **Org Key** is correct

### Rate Limited (429)

- Carbon Black Cloud rate limits vary by subscription tier
- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Host** URL matches your CBC instance region
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm alerts exist in the CBC console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
