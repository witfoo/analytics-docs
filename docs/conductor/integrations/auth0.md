---
tags:
  - integration
  - identity
---

# Auth0

Collects authentication and authorization event logs from Auth0 (Okta
Customer Identity Cloud), including login events, failed authentication
attempts, and admin audit logs.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.auth0` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Auth0 Management API](https://auth0.com/docs/api/management/v2) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Auth0 subscription. Admin access required to create Machine-to-Machine
    applications.

- [ ] Active Auth0 tenant
- [ ] Admin access to the Auth0 Dashboard
- [ ] Network: Conductor can reach your Auth0 domain on port 443

## Step 1: Create API Credentials

1. Log in to the **Auth0 Dashboard** at `https://manage.auth0.com/`
2. Navigate to **Applications** → **Applications**
3. Click **Create Application**
4. Select **Machine to Machine Applications**
5. Name it (e.g., "WitFoo Conductor")
6. Select the **Auth0 Management API** as the authorized API
7. Grant the scope: **`read:logs`**
8. Click **Authorize**
9. Note the **Domain**, **Client ID**, and **Client Secret** from the
   application settings

!!! info "Auth0 Domain Format"
    Your Auth0 domain has the format `<your-tenant>.us.auth0.com` (or
    `.eu.auth0.com` for EU tenants). Custom domains are also supported.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Auth0**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Domain** | `<tenant>.us.auth0.com` | Auth0 tenant domain |
    | **Client ID** | `<your-client-id>` | Machine-to-Machine app Client ID |
    | **Client Secret** | `<your-client-secret>` | Machine-to-Machine app secret |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "auth0"
    ```

    Look for successful poll messages:
    ```
    [INFO] auth0: fetched <N> log events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the application is authorized for the Management API with `read:logs`
- Check that the **Domain** format is correct (include `.auth0.com`)

### Forbidden (403)

- The application may lack the `read:logs` scope
- Re-authorize the application in **Applications** → select app →
  **APIs** tab → **Auth0 Management API** → add `read:logs`

### Rate Limited (429)

- Auth0 rate limits vary by plan tier (50 req/sec on free plan)
- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### Log Retention

- Auth0 log retention varies by plan:
    - **Free**: 2 days
    - **Developer**: 2 days
    - **Developer Pro**: 10 days
    - **Enterprise**: 30 days
- If gaps appear in data, increase polling frequency to stay within
  retention window

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify authentication events exist: test by logging into your Auth0-powered app
- Verify network connectivity: `curl -I https://<tenant>.us.auth0.com`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
