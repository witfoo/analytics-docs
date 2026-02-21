---
tags:
  - integration
  - endpoint
---

# Halcyon

Collects anti-ransomware event data from Halcyon.ai, including ransomware
detections, endpoint protection events, and device inventory.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.halcyon` |
| **Auth Method** | Username / Password → JWT |
| **Polling Interval** | 10 min (events), 1 hr (devices) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Halcyon Documentation](https://docs.halcyon.ai/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Halcyon.ai subscription. Admin account credentials with API
    access.

- [ ] Active Halcyon.ai subscription
- [ ] Admin account credentials
- [ ] Tenant ID from Halcyon portal
- [ ] Network: Conductor can reach `app.halcyon.ai` on port 443

## Step 1: Create API Credentials

Halcyon uses admin login credentials for API access (no separate API key):

1. Log in to the **Halcyon Console** at `https://app.halcyon.ai/`
2. Confirm your admin **username** (email) and **password**
3. Navigate to **Settings** → **Account** to find your **Tenant ID**

!!! tip "Dedicated API User"
    Consider creating a dedicated service account for the Conductor
    integration rather than using a personal admin account. This avoids
    disruption if the admin changes their password.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Halcyon**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `app.halcyon.ai` | Halcyon API endpoint |
    | **Username** | `<your-email>` | Admin account email |
    | **Password** | `<your-password>` | Admin account password |
    | **Tenant ID** | `<your-tenant-id>` | From Halcyon account settings |

5. Set the **Polling Interval** (recommended: 10 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "halcyon"
    ```

    Look for successful authentication and poll messages:
    ```
    [INFO] halcyon: authenticated, fetching events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Username** and **Password** are correct
- Ensure the account has not been locked or disabled
- Check if multi-factor authentication is blocking API access

### JWT Refresh Failures

- Halcyon uses short-lived JWT tokens obtained via username/password
  authentication
- If the refresh fails, the password may have been changed
- Update the password in the Conductor UI and save

### Forbidden (403)

- The account may not have admin-level access
- Verify the account role in the Halcyon console

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Tenant ID** is correct
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm ransomware events exist in the Halcyon console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
