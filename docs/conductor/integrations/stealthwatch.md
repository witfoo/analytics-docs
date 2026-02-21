---
tags:
  - integration
  - network
---

# Stealthwatch

Collects network flow analytics and security events from Cisco Stealthwatch
(Secure Network Analytics), providing visibility into internal network threats,
anomalous behaviors, and flow data.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.stealthwatch` |
| **Auth Method** | Username + Password (Session Cookie) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Stealthwatch API Documentation](https://developer.cisco.com/docs/stealthwatch/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Cisco Secure Network Analytics (Stealthwatch) deployment.
    Admin access required to create API users.

- [ ] Active Stealthwatch Management Console (SMC)
- [ ] Admin access to create user accounts
- [ ] Network: Conductor can reach the Stealthwatch Management Console on port 443

## Step 1: Create API Credentials

1. Log in to the **Stealthwatch Management Console** at `https://<smc-address>/`
2. Navigate to **Configuration** → **User Management**
3. Click **Add User**
4. Configure the user:
    - **Username**: `witfoo-conductor`
    - **Role**: **Analyst** (read-only access)
    - **Password**: Set a strong password
5. Note the **Domain ID** — visible on the SMC dashboard or under **Domains**

!!! warning "Store Credentials Securely"
    API credentials grant access to your Stealthwatch data. Store them securely
    and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Stealthwatch**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<smc-address>` | Stealthwatch Management Console IP or hostname |
    | **Domain ID** | `<your-domain-id>` | Stealthwatch domain identifier |
    | **Username** | `witfoo-conductor` | API user from step 1 |
    | **Password** | `<password>` | Password from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "stealthwatch"
    ```

    Look for successful poll messages:
    ```
    [INFO] stealthwatch: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Username** and **Password** are correct
- Ensure the user account has not been locked or disabled
- Check that the Stealthwatch session has not expired

### Forbidden (403)

- The user may lack required role permissions
- Ensure the user has at least **Analyst** role

### Rate Limited (429)

- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity from Conductor to the SMC
- Confirm the **Domain ID** is correct
- Ensure flow data is being collected by the Stealthwatch Flow Collectors

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
