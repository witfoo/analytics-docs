---
tags:
  - integration
  - endpoint
---

# SentinelOne

Collects endpoint threat data from SentinelOne Singularity, including threat
detections, activity logs, and agent/device inventory.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.sentinelone` |
| **Auth Method** | API Token |
| **Polling Interval** | 5 min (threats), 10 min (activities), 1 hr (agents) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [SentinelOne API Documentation](https://usea1-partners.sentinelone.net/api-doc/overview) |

## Prerequisites

!!! note "Vendor Requirements"
    Active SentinelOne Singularity subscription. Admin access required to
    create service users and generate API tokens.

- [ ] Active SentinelOne subscription
- [ ] Admin access to the SentinelOne Management Console
- [ ] Network: Conductor can reach your SentinelOne management URL on port 443

## Step 1: Create API Credentials

1. Log in to the **SentinelOne Management Console** at
   `https://<your-instance>.sentinelone.net/`
2. Navigate to **Settings** → **Users** → **Service Users**
3. Click **Create Service User**
4. Set the role to **Viewer** (read-only access is sufficient)
5. Set the scope — Account-level for broadest visibility, or Site-level for
   specific sites
6. Click **Create**
7. Click **Generate API Token** on the new service user
8. Copy the **API Token**

!!! info "Token Scope"
    **Account-scoped** tokens collect data from all sites. **Site-scoped**
    tokens are limited to a specific site. Use account scope unless you need
    to restrict data collection.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **SentinelOne**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<your-instance>.sentinelone.net` | Management console URL |
    | **API Key** | `<your-api-token>` | API token from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for threats)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "sentinelone"
    ```

    Look for successful poll messages:
    ```
    [INFO] sentinelone: fetched <N> threats
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Token** is correct and has not expired
- SentinelOne API tokens have configurable expiry; re-generate if expired
- Ensure the token was copied completely

### Forbidden (403)

- The service user may not have sufficient role permissions
- Verify the user has at least **Viewer** role

### Rate Limited (429)

- SentinelOne enforces a rate limit of approximately 1000 requests per minute
- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Host** URL is correct (include the full management URL)
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm threats or activities exist in the SentinelOne console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
