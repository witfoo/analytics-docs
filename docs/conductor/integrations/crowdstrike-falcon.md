---
tags:
  - integration
  - endpoint
---

# CrowdStrike Falcon

Collects endpoint detection and device inventory data from CrowdStrike Falcon,
providing visibility into endpoint threats, detections, and managed host assets.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.crowdstrike-falcon` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 10 min (detections), 1 hr (devices) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [CrowdStrike API Reference](https://developer.crowdstrike.com/docs/openapi/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active CrowdStrike Falcon subscription with API access enabled.
    Falcon Administrator role required to create API clients.

- [ ] Active CrowdStrike Falcon subscription
- [ ] Falcon Administrator role in the CrowdStrike console
- [ ] Network: Conductor can reach your CrowdStrike API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to the **Falcon Console** at `https://falcon.crowdstrike.com/`

    !!! tip "Cloud-Specific URLs"
        Your API base URL depends on your CrowdStrike cloud environment:

        | Cloud | Console URL | API Base URL |
        |-------|------------|--------------|
        | US-1 | `falcon.crowdstrike.com` | `api.crowdstrike.com` |
        | US-2 | `falcon.us-2.crowdstrike.com` | `api.us-2.crowdstrike.com` |
        | EU-1 | `falcon.eu-1.crowdstrike.com` | `api.eu-1.crowdstrike.com` |
        | US-GOV-1 | `falcon.laggar.gcw.crowdstrike.com` | `api.laggar.gcw.crowdstrike.com` |

2. Navigate to **Support and resources** → **API Clients and Keys**
3. Click **Add new API Client**
4. Configure the API client:
    - **Client Name**: `WitFoo Conductor`
    - **Description**: `Read-only access for security log collection`
    - **Scopes**:
        - `Detections` → **Read**
        - `Hosts` → **Read**
5. Click **Create**
6. Copy the **Client ID** and **Client Secret** — the secret is only shown once

!!! warning "Store Credentials Securely"
    The Client Secret is displayed only at creation time. Store it securely and
    do not share it in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **CrowdStrike Falcon**
3. Enter a unique name for this instance (e.g., "CrowdStrike US-2 Production")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api.crowdstrike.com` | API base URL for your cloud (see table above) |
    | **Client ID** | `<your-client-id>` | From step 1 |
    | **Client Secret** | `<your-client-secret>` | From step 1 |

5. Set the **Polling Interval** (recommended: 10 minutes for detections)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "crowdstrike"
    ```

    Look for successful poll messages:
    ```
    [INFO] crowdstrike-falcon: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 10-minute interval, expect data within 10 minutes.

### Data Collection Details

The CrowdStrike connector collects data from multiple API endpoints on
different schedules:

| Endpoint | Interval | Description |
|----------|----------|-------------|
| Detection IDs + Details | 10 min | Active detections (alerts). Batches at 1,000-item boundary. |
| Device Details (v2) | 1 hr | Managed host inventory via `getDeviceDetailsV2`. String offset pagination. |
| Combined Device/Host | 1 hr | Supplemental host data from combined endpoint. |

!!! info "Alert Batching"
    The connector fetches detection IDs first, then batches detail requests
    in groups of 1,000. Large environments may see multiple batch cycles per
    polling interval.

### GovCloud Configuration

For US Government cloud deployments, use the GovCloud-specific URLs:

| Setting | Value |
|---------|-------|
| **FQDN** | `api.laggar.gcw.crowdstrike.com` |
| **Console** | `falcon.laggar.gcw.crowdstrike.com` |

All other settings remain the same. GovCloud environments enforce
FedRAMP-compliant authentication.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the API client has not been revoked in the Falcon Console
- Check that the **FQDN** matches your CrowdStrike cloud (US-1, US-2, EU-1, US-GOV-1)

### Forbidden (403)

- The API client may lack the required scopes
- Required scopes: `Detections: Read`, `Hosts: Read`
- Edit the API client in the Falcon Console to add missing scopes

### Rate Limited (429)

- CrowdStrike rate limits are per-customer and shown in response headers
  (`X-RateLimit-Limit`, `X-RateLimit-Remaining`)
- Increase the **Polling Interval** to 15 minutes if rate limiting occurs frequently
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api.crowdstrike.com`
- Confirm detections or device data exists in the Falcon Console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
