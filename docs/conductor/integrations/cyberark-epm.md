---
tags:
  - integration
  - identity
---

# CyberArk EPM

Collects endpoint privilege management events from CyberArk Endpoint
Privilege Manager, including privilege elevation events, policy audit data,
and application control actions.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.cyberark-epm` |
| **Auth Method** | Username / Password → Session Token |
| **Polling Interval** | 10 min (events), 30 min (policy audit) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [CyberArk EPM REST API](https://docs.cyberark.com/epm/latest/en/content/webservices/webservicesintro.htm) |

## Prerequisites

!!! note "Vendor Requirements"
    Active CyberArk EPM SaaS subscription. Admin account with API access.

- [ ] Active CyberArk EPM subscription
- [ ] Admin account credentials
- [ ] Set ID (EPM set identifier)
- [ ] Network: Conductor can reach `<tenant>.epm.cyberark.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **CyberArk EPM Console** at
   `https://<tenant>.epm.cyberark.com/`
2. Navigate to **Administration** → **Account Management**
3. Create a new user (or use an existing admin account)
4. Assign the user the **Admin** or **Auditor** role
5. Record the **username** and **password**
6. Note the **Set ID** from the EPM console (visible in the URL or under
   **Sets** management)

!!! tip "Dedicated Service Account"
    Create a dedicated service account for the integration to avoid
    disruption if an admin changes their personal password.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **CyberArk EPM**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<tenant>.epm.cyberark.com` | EPM console URL |
    | **Username** | `<your-username>` | API user from step 1 |
    | **Password** | `<your-password>` | API user password |
    | **Set ID** | `<your-set-id>` | EPM set identifier |

5. Set the **Polling Interval** (recommended: 10 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "cyberark"
    ```

    Look for successful authentication messages:
    ```
    [INFO] cyberark-epm: authenticated, fetching events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Username** and **Password** are correct
- CyberArk EPM session tokens expire after approximately 20 minutes;
  Conductor handles automatic re-authentication
- If the password was recently changed, update it in the Conductor UI

### Forbidden (403)

- The user may not have sufficient role permissions
- Verify the user has **Admin** or **Auditor** role in EPM

### Token Expiry Issues

- CyberArk EPM uses short-lived session tokens (~20 minutes)
- Conductor automatically re-authenticates when tokens expire
- If repeated authentication failures occur, check the account lockout
  policy in CyberArk

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Set ID** is correct
- Check the **Host** URL matches your EPM tenant
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify events exist in the EPM console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
