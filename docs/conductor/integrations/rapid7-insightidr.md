---
tags:
  - integration
  - siem
---

# Rapid7 InsightIDR

Collects investigation and alert data from Rapid7 InsightIDR, Rapid7's
cloud SIEM and XDR platform for threat detection, investigation, and response.

| | |
|---|---|
| **Category** | SIEM |
| **Connector Name** | `signal-client.rapid7-insightidr` |
| **Auth Method** | API Key |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [InsightIDR API](https://docs.rapid7.com/insightidr/api-overview/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Rapid7 InsightIDR subscription. Platform Admin access required
    to generate API keys.

- [ ] Active Rapid7 InsightIDR subscription
- [ ] Platform Admin access to Rapid7 Insight Platform
- [ ] Network: Conductor can reach your Rapid7 regional endpoint on port 443

## Step 1: Create API Credentials

1. Log in to the **Rapid7 Insight Platform** at `https://insight.rapid7.com/`
2. Navigate to **Platform Settings** → **API Keys**
3. Click **New User Key** (or **New Organization Key** for shared access)
4. Name the key (e.g., "WitFoo Conductor")
5. Click **Generate**
6. Copy the **API Key**

!!! info "Regional Endpoints"
    Rapid7 uses regional API endpoints. Select the region that matches
    your Insight Platform account:

    | Region | API Endpoint |
    |--------|-------------|
    | US 1 | `us.api.insight.rapid7.com` |
    | US 2 | `us2.api.insight.rapid7.com` |
    | US 3 | `us3.api.insight.rapid7.com` |
    | EU | `eu.api.insight.rapid7.com` |
    | Canada | `ca.api.insight.rapid7.com` |
    | Australia | `au.api.insight.rapid7.com` |
    | Japan | `ap.api.insight.rapid7.com` |

    Check your account URL to determine your region.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Rapid7 InsightIDR**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Region** | `us` | Regional identifier (see table above) |
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
    docker logs signal-client-svc --tail=50 | grep "rapid7"
    ```

    Look for successful poll messages:
    ```
    [INFO] rapid7-insightidr: fetched <N> investigations
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Data Types Collected

| Type | Description |
|------|-------------|
| Investigations | Threat investigations with alerts and evidence |
| Alerts | Detection rule triggers and anomaly alerts |

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key** is correct and was copied completely
- Ensure the key has not been revoked in the Insight Platform
- Check that the key is a **User Key** (not an Organization Key with
  restrictions)

### Wrong Region

- If you see 404 errors, verify the **Region** matches your Insight Platform
  account region
- Check the URL in your browser when logged into Rapid7

### Forbidden (403)

- The API key user may not have InsightIDR access
- Verify the user has Platform Admin or at least read access to InsightIDR

### Rate Limited (429)

- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify investigations or alerts exist in InsightIDR
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm the regional endpoint is reachable

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
