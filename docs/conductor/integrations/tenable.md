---
tags:
  - integration
  - vulnerability
---

# Tenable

Collects vulnerability scan results and asset data from Tenable.io (Tenable
Vulnerability Management), providing visibility into vulnerability posture,
scan findings, and asset inventory.

| | |
|---|---|
| **Category** | Vulnerability Management |
| **Connector Name** | `signal-client.tenable` |
| **Auth Method** | Access Key + Secret Key |
| **Polling Interval** | 30 min (vulnerabilities), 1 hr (assets) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Tenable.io API Documentation](https://developer.tenable.com/reference/navigate) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Tenable.io (Tenable Vulnerability Management) subscription.
    Admin access required to generate API keys.

- [ ] Active Tenable.io subscription
- [ ] Admin or Standard user with API key generation permissions
- [ ] Network: Conductor can reach `cloud.tenable.com` on port 443

## Step 1: Create API Credentials

1. Log in to **Tenable.io** at `https://cloud.tenable.com/`
2. Click your account icon (top-right) → **My Account**
3. Navigate to the **API Keys** tab
4. Click **Generate**
5. Copy the **Access Key** and **Secret Key**

!!! warning "Store Credentials Securely"
    Tenable API keys grant access to your vulnerability data. Store them
    securely and do not share them in tickets or email. The secret key is
    only shown once.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Tenable**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `cloud.tenable.com` | Tenable.io API endpoint |
    | **Client ID** | `<your-access-key>` | Access key from step 1 |
    | **API Secret** | `<your-secret-key>` | Secret key from step 1 |

5. Set the **Polling Interval** (recommended: 30 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "tenable"
    ```

    Look for successful poll messages:
    ```
    [INFO] tenable: fetched <N> vulnerabilities
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 30-minute interval, expect data within 30 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Access Key** and **Secret Key** are correct
- Ensure the API keys have not been regenerated (regenerating invalidates
  previous keys)

### Forbidden (403)

- The API keys may belong to a user without scan result access
- Ensure the user has at least Standard or Admin permissions

### Rate Limited (429)

- Tenable.io enforces a rate limit of 300-500 requests per minute
  (varies by subscription tier)
- Increase the **Polling Interval** to 60 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://cloud.tenable.com`
- Confirm vulnerability scans have completed in Tenable.io
- Ensure scan results exist for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
