---
tags:
  - integration
  - identity
---

# 1Password Events

Collects security event data from 1Password Events Reporting API, including
sign-in attempts, item usage events, and audit log entries.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.1password-events` |
| **Auth Method** | API Token (Bearer) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [1Password Events API](https://developer.1password.com/docs/events-api/) |

## Prerequisites

!!! note "Vendor Requirements"
    1Password **Business** or **Enterprise** plan required. Events Reporting
    is not available on Teams or individual plans. Account owner or admin
    access required.

- [ ] 1Password Business or Enterprise plan
- [ ] Account owner or admin access
- [ ] Network: Conductor can reach `events.1password.com` on port 443

## Step 1: Create API Credentials

1. Sign in to **1Password** at `https://start.1password.com/`
2. Navigate to **Integrations** → **Directory**
3. Select **Events Reporting** under the "Other" category
4. Click **Create Events Reporting Integration**
5. Name the integration (e.g., "WitFoo Conductor")
6. Copy the generated **Bearer Token**

!!! warning "Token Storage"
    The token is only shown once at creation time. Store it securely.
    If lost, you must delete the integration and create a new one.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **1Password Events**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `events.1password.com` | 1Password Events API endpoint |
    | **API Token** | `<your-bearer-token>` | Token from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "1password"
    ```

    Look for successful poll messages:
    ```
    [INFO] 1password-events: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Event Types Collected

| Event Type | Description |
|------------|-------------|
| Sign-in Attempts | Successful and failed sign-in events |
| Item Usages | Password fills, item views, credential access |
| Audit Events | Admin actions, vault changes, group modifications |

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Token** is correct and was copied completely
- Ensure the Events Reporting integration has not been deleted in 1Password

### Plan Limitations

- Events Reporting requires 1Password **Business** or **Enterprise** plan
- If you receive a 403 error, verify your plan tier in 1Password billing

### Rate Limited (429)

- 1Password Events API has rate limits based on plan tier
- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- 1Password events may have a short delay before appearing in the API
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://events.1password.com`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
