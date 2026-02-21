---
tags:
  - integration
  - infrastructure
---

# Druva

Collects backup and data protection events from Druva inSync, providing
visibility into data protection status, anomalous activity, and backup
compliance across endpoints and cloud workloads.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.druva` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 15 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Druva API Documentation](https://developer.druva.com/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Druva subscription (inSync or Phoenix). Admin access required to
    create API credentials.

- [ ] Active Druva subscription
- [ ] Admin access in the Druva Cloud Platform Console
- [ ] Network: Conductor can reach `apis.druva.com` on port 443

## Step 1: Create API Credentials

1. Log in to the **Druva Cloud Platform Console** at `https://login.druva.com/`
2. Navigate to **Druva Cloud Settings** → **API Credentials**
3. Click **Create Credentials**
4. Configure the credential:
    - **Name**: `WitFoo Conductor`
    - **Scope**: Read-only
5. Copy the **Client ID** and **Client Secret**

!!! warning "Store Credentials Securely"
    API credentials grant access to your Druva data protection events. Store
    them securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Druva**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `apis.druva.com` | Druva API endpoint |
    | **Client ID** | `<your-client-id>` | Client ID from step 1 |
    | **Client Secret** | `<your-client-secret>` | Client secret from step 1 |

5. Set the **Polling Interval** (recommended: 15 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "druva"
    ```

    Look for successful poll messages:
    ```
    [INFO] druva: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 15-minute interval, expect data within 15 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the credentials have not been revoked in the Druva console

### Forbidden (403)

- The API credential may lack required permissions
- Recreate with appropriate read scope

### Rate Limited (429)

- Increase the **Polling Interval** to 30 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://apis.druva.com`
- Confirm events exist in the Druva console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
