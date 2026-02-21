---
tags:
  - integration
  - identity
---

# Cisco Duo

Collects authentication and security events from Cisco Duo, providing
visibility into multi-factor authentication activity, enrollment status,
and access policy enforcement.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.cisco-duo` |
| **Auth Method** | Integration Key + Secret Key (HMAC-SHA1) |
| **Polling Interval** | 5 min (auth logs), 1 hr (admin logs) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Duo Admin API](https://duo.com/docs/adminapi) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Cisco Duo subscription (any edition). Admin API application
    required — must be created by a Duo admin with **Owner** role.

- [ ] Active Cisco Duo account
- [ ] Duo admin with **Owner** role
- [ ] Network: Conductor can reach `api-<hex>.duosecurity.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Duo Admin Panel** at `https://admin.duosecurity.com/`
2. Navigate to **Applications** → **Protect an Application**
3. Search for **Admin API** and click **Protect**
4. Configure the application:
    - **Name**: `WitFoo Conductor`
    - **Permissions**: Grant **Read Log** permission
5. Note the three credential values:
    - **Integration Key** (ikey)
    - **Secret Key** (skey)
    - **API Hostname** (e.g., `api-XXXXXXXX.duosecurity.com`)

!!! warning "Store Credentials Securely"
    Duo API credentials grant access to your authentication log data. Store them
    securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Cisco Duo**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api-XXXXXXXX.duosecurity.com` | API hostname from step 1 |
    | **Integration Key (ikey)** | `<your-ikey>` | Integration key from step 1 |
    | **Secret Key (skey)** | `<your-skey>` | Secret key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for auth logs)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "cisco-duo"
    ```

    Look for successful poll messages:
    ```
    [INFO] cisco-duo: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Integration Key** and **Secret Key** are correct
- Ensure the Admin API application has not been deleted in the Duo Admin Panel
- Check that the **FQDN** matches your Duo API hostname

### Forbidden (403)

- The Admin API application may lack **Read Log** permission
- Edit the application in the Duo Admin Panel to add the permission

### Rate Limited (429)

- Duo rate limits are per-integration and per-endpoint
- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api-XXXXXXXX.duosecurity.com`
- Confirm authentication events exist in the Duo Admin Panel for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
