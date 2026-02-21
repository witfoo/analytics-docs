---
tags:
  - integration
  - network
---

# Cisco Meraki

Collects network security events from Cisco Meraki cloud-managed networks,
providing visibility into network threats, content filtering, and device
connectivity.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.cisco-meraki` |
| **Auth Method** | API Key (X-Cisco-Meraki-API-Key) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Meraki Dashboard API](https://developer.cisco.com/meraki/api-v1/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Cisco Meraki license. Organization-level API access must be enabled
    by a Meraki Dashboard administrator.

- [ ] Active Cisco Meraki subscription
- [ ] Organization admin access in the Meraki Dashboard
- [ ] API access enabled for the organization
- [ ] Network: Conductor can reach `api.meraki.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Meraki Dashboard** at `https://dashboard.meraki.com/`
2. Navigate to **Organization** → **Settings**
3. Under **Dashboard API access**, enable the API
4. Click your username (top-right) → **My profile**
5. Scroll to **API access** and click **Generate new API key**
6. Copy the **API Key** — it is only shown once

!!! warning "Store Credentials Securely"
    The Meraki API key grants organization-level access. Store it securely and
    do not share it in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Cisco Meraki**
3. Enter a unique name for this instance (e.g., "Meraki Production Org")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api.meraki.com` | Meraki API endpoint |
    | **Auth Token** | `<your-api-key>` | API key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "cisco-meraki"
    ```

    Look for successful poll messages:
    ```
    [INFO] cisco-meraki: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key** is correct and has not been revoked
- Ensure API access is still enabled at the organization level

### Forbidden (403)

- The API key may not have access to the target organization
- Ensure you generated the key with an organization admin account

### Rate Limited (429)

- Meraki enforces a limit of 10 API calls per second per organization
- Increase the **Polling Interval** if rate limiting occurs
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api.meraki.com`
- Confirm security events exist in the Meraki Dashboard for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
