---
tags:
  - integration
  - email
---

# Mimecast

Collects email security events from Mimecast, providing visibility into
email threat detections, URL clicks, attachment analysis, and audit events.

| | |
|---|---|
| **Category** | Email Security |
| **Connector Name** | `signal-client.mimecast` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Mimecast API Documentation](https://developer.services.mimecast.com/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Mimecast subscription with API access. Administrator role required
    to create API applications.

- [ ] Active Mimecast subscription
- [ ] Mimecast Administrator account
- [ ] Network: Conductor can reach your regional Mimecast API server on port 443

## Step 1: Create API Credentials

1. Log in to the **Mimecast Administration Console** at `https://login.mimecast.com/`
2. Navigate to **Administration** → **Services** → **API and Platform Integrations**
3. Click **Add API Application**
4. Configure the application:
    - **Application Name**: `WitFoo Conductor`
    - **Category**: SIEM Integration
    - **Permissions**: Enable log access
5. Note the **Application ID** and generate a **Client ID** and **Client Secret**
6. Note your **API Server** (regional endpoint, e.g., `us-api.mimecast.com`, `eu-api.mimecast.com`)

!!! warning "Store Credentials Securely"
    API credentials grant access to your Mimecast log data. Store them securely
    and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Mimecast**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **API Server** | `us-api.mimecast.com` | Regional API endpoint |
    | **Client ID** | `<your-client-id>` | OAuth2 client ID from step 1 |
    | **Client Secret** | `<your-client-secret>` | OAuth2 client secret from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "mimecast"
    ```

    Look for successful poll messages:
    ```
    [INFO] mimecast: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the API application is still active in the Mimecast console
- Check that the **API Server** matches your Mimecast region

### Forbidden (403)

- The API application may lack required permissions
- Ensure the application has log access permissions

### Rate Limited (429)

- Mimecast enforces per-application rate limits
- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity to your Mimecast API server
- Confirm email security events exist in the Mimecast console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
