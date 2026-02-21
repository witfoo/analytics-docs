---
tags:
  - integration
  - network
---

# Cisco Umbrella

Collects DNS security and web proxy events from Cisco Umbrella, providing
visibility into DNS-layer threats, blocked domains, and web traffic activity.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.cisco-umbrella` |
| **Auth Method** | API Key + Secret (Basic Auth) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Umbrella API Documentation](https://developer.cisco.com/docs/cloud-security/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Cisco Umbrella subscription (DNS Security or Secure Internet Gateway).
    Admin access required to generate API keys.

- [ ] Active Cisco Umbrella subscription
- [ ] Full admin access in the Umbrella Dashboard
- [ ] Network: Conductor can reach `api.umbrella.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Umbrella Dashboard** at `https://dashboard.umbrella.com/`
2. Navigate to **Admin** → **API Keys**
3. Click **Create API Key**
4. Select **Umbrella Reporting** scope
5. Copy the **Key** and **Secret**

!!! warning "Store Credentials Securely"
    API credentials grant access to your Umbrella reporting data. Store them
    securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Cisco Umbrella**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api.umbrella.com` | Umbrella API endpoint |
    | **Key** | `<your-api-key>` | API key from step 1 |
    | **Secret** | `<your-api-secret>` | API secret from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "cisco-umbrella"
    ```

    Look for successful poll messages:
    ```
    [INFO] cisco-umbrella: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Key** and **Secret** are correct
- Ensure the API key has not been revoked in the Umbrella Dashboard

### Forbidden (403)

- The API key may lack the Reporting scope
- Recreate with **Umbrella Reporting** scope

### Rate Limited (429)

- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api.umbrella.com`
- Confirm security events exist in the Umbrella Dashboard for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
