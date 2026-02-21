---
tags:
  - integration
  - identity
---

# Okta

Collects system log events from Okta, providing visibility into
authentication activity, user lifecycle changes, and identity security
events across your Okta organization.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.okta` |
| **Auth Method** | API Token (SSWS) |
| **Polling Interval** | 5 min (system log) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Okta System Log API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/SystemLog/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Okta subscription (any edition). Super Admin or Read Only Admin
    role required to create API tokens.

- [ ] Active Okta organization
- [ ] Super Admin or Read Only Admin role
- [ ] Network: Conductor can reach `<your-org>.okta.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Okta Admin Console** at `https://<your-org>-admin.okta.com/`
2. Navigate to **Security** → **API** → **Tokens**
3. Click **Create Token**
4. Enter a name: `WitFoo Conductor`
5. Click **Create Token**
6. Copy the **Token Value** — it is only shown once

!!! warning "Store Credentials Securely"
    Okta API tokens inherit the permissions of the admin who creates them.
    Store them securely and do not share them in tickets or email.

!!! tip "Token Scope"
    Tokens created by Read Only Admins have read-only access. For
    least-privilege, use a Read Only Admin account.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Okta**
3. Enter a unique name for this instance (e.g., "Okta Production Org")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `<your-org>.okta.com` | Your Okta organization domain |
    | **API Token** | `<your-token>` | SSWS token from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "okta"
    ```

    Look for successful poll messages:
    ```
    [INFO] okta: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Token** is correct and has not been revoked
- Tokens expire if the creating admin's account is deactivated or their
  password is reset
- Regenerate the token if necessary

### Forbidden (403)

- The token's admin may lack access to the System Log API
- Use a token created by a Super Admin or Read Only Admin

### Rate Limited (429)

- Okta enforces per-org rate limits (varies by subscription tier)
- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://<your-org>.okta.com`
- Confirm log events exist in the Okta System Log for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
