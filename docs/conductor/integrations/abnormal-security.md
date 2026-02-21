---
tags:
  - integration
  - email
---

# Abnormal Security

Collects threat detection data from Abnormal Security, including business
email compromise (BEC), phishing, account takeover, and other advanced email
threats identified by Abnormal's behavioral AI platform.

| | |
|---|---|
| **Category** | Email Security |
| **Connector Name** | `signal-client.abnormal-security` |
| **Auth Method** | API Token (Bearer) |
| **Polling Interval** | 10 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Abnormal Security API](https://app.abnormalsecurity.com/docs) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Abnormal Security subscription with API access enabled.
    Admin role required to generate API tokens.

- [ ] Active Abnormal Security subscription
- [ ] Admin access to the Abnormal Security portal
- [ ] Network: Conductor can reach `api.abnormalplatform.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Abnormal Security Portal** at
   `https://portal.abnormalplatform.com/`
2. Navigate to **Settings** → **Integrations**
3. Select **REST API**
4. Click **Generate Token**
5. Copy the generated **API Token**

!!! warning "Token Expiry"
    Abnormal Security API tokens typically expire annually. Set a calendar
    reminder to rotate the token before expiry to avoid data collection
    interruptions.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Abnormal Security**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `api.abnormalplatform.com` | Abnormal API endpoint |
    | **API Key** | `<your-api-token>` | Bearer token from step 1 |

5. Set the **Polling Interval** (recommended: 10 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "abnormal"
    ```

    Look for successful poll messages:
    ```
    [INFO] abnormal-security: fetched <N> threats
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Token** is correct and has not expired
- Regenerate the token in the Abnormal Security portal if needed
- Ensure the token was copied completely (no trailing whitespace)

### Forbidden (403)

- The token may belong to a user without sufficient permissions
- Confirm the user has Admin access in the Abnormal Security portal

### Rate Limited (429)

- Abnormal Security enforces API rate limits based on subscription tier
- Increase the **Polling Interval** to 30 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify threats exist in the Abnormal Security console for the polling window
- Confirm network connectivity: `curl -I https://api.abnormalplatform.com`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
