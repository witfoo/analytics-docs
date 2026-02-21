---
tags:
  - integration
  - infrastructure
---

# LimaCharlie

Collects endpoint detection and telemetry events from LimaCharlie, providing
visibility into endpoint activity, detections, and sensor health across
your LimaCharlie organization.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.limacharlie` |
| **Auth Method** | API Key (Bearer) + Organization ID |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [LimaCharlie API Documentation](https://doc.limacharlie.io/docs/api/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active LimaCharlie organization. Admin access required to generate
    API keys.

- [ ] Active LimaCharlie organization
- [ ] Admin access in the LimaCharlie web console
- [ ] Network: Conductor can reach `api.limacharlie.io` on port 443

## Step 1: Create API Credentials

1. Log in to the **LimaCharlie Console** at `https://app.limacharlie.io/`
2. Select your organization
3. Navigate to **Access Management** → **REST API**
4. Click **Create API Key**
5. Configure the key:
    - **Name**: `WitFoo Conductor`
    - **Permissions**: **Read** access to detections and telemetry
6. Copy the **API Key**
7. Note your **Organization ID** from the organization settings page

!!! warning "Store Credentials Securely"
    API keys grant access to your LimaCharlie telemetry data. Store them
    securely and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **LimaCharlie**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `api.limacharlie.io` | LimaCharlie API endpoint |
    | **Organization ID** | `<your-org-id>` | Organization ID from step 1 |
    | **API Key** | `<your-api-key>` | API key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "limacharlie"
    ```

    Look for successful poll messages:
    ```
    [INFO] limacharlie: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key** is correct and has not been revoked
- Ensure the **Organization ID** matches the key's organization

### Forbidden (403)

- The API key may lack required permissions
- Ensure the key has read access to detections

### Rate Limited (429)

- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api.limacharlie.io`
- Confirm events exist in the LimaCharlie console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
