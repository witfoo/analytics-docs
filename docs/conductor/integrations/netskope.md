---
tags:
  - integration
  - infrastructure
---

# Netskope

Collects cloud security event data from Netskope, including DLP alerts,
cloud application events, web transaction logs, and audit events from
Netskope's Security Service Edge (SSE) platform.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.netskope` |
| **Auth Method** | API Token (v1 or v2) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Netskope REST API](https://docs.netskope.com/en/rest-api-v2-overview.html) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Netskope subscription. Admin access to create API tokens.
    Netskope API v1 or v2 access enabled.

- [ ] Active Netskope subscription
- [ ] Admin access to the Netskope tenant
- [ ] Network: Conductor can reach `<tenant>.goskope.com` on port 443

## Step 1: Create API Credentials

Netskope supports both v1 and v2 API tokens. **v2 tokens are recommended**
as they support scoped permissions.

=== "API v2 (Recommended)"

    1. Log in to the **Netskope Admin Console** at
       `https://<tenant>.goskope.com/`
    2. Navigate to **Settings** → **Tools** → **REST API v2**
    3. Click **New Token**
    4. Name the token (e.g., "WitFoo Conductor")
    5. Select required scopes:
        - `/api/v2/events/data/alert` (alerts)
        - `/api/v2/events/data/page` (web transactions)
        - `/api/v2/events/data/application` (app events)
        - `/api/v2/events/data/audit` (audit logs)
    6. Set token expiry (maximum recommended)
    7. Click **Save**
    8. Copy the **Token**

=== "API v1 (Legacy)"

    1. Log in to the **Netskope Admin Console**
    2. Navigate to **Settings** → **Tools** → **REST API v1**
    3. Copy the existing **Token** or generate a new one
    4. Note: v1 tokens have global scope (no per-endpoint scoping)

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Netskope**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Base URL** | `<tenant>.goskope.com` | Netskope tenant URL |
    | **API Token** | `<your-token>` | v1 or v2 API token from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "netskope"
    ```

    Look for successful poll messages:
    ```
    [INFO] netskope: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Event Types Collected

| Type | Description |
|------|-------------|
| Alerts | DLP violations, malware detections, anomaly alerts |
| Page Events | Web transaction data |
| Application Events | Cloud app activity |
| Audit Events | Admin actions and configuration changes |

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Token** is correct
- For v2 tokens, ensure the token has not expired
- For v1 tokens, confirm the token is still active in Settings → REST API v1

### Forbidden (403)

- For v2 tokens, the token may lack required scopes
- Add the needed event type scopes to the token in Netskope admin

### Rate Limited (429)

- Netskope rate limits vary by license tier
- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Base URL** includes your tenant name (e.g., `acme.goskope.com`)
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm traffic is flowing through Netskope (check Netskope dashboard)

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
