---
tags:
  - integration
  - endpoint
---

# Cisco AMP

Collects endpoint security events from Cisco AMP (Advanced Malware Protection)
for Endpoints, providing visibility into malware detections, file convictions,
and endpoint threat activity.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.cisco-amp` |
| **Auth Method** | Client ID + API Key (Basic Auth) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Cisco AMP API Documentation](https://api-docs.amp.cisco.com/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Cisco Secure Endpoint (AMP for Endpoints) subscription.
    Admin access required to generate API credentials.

- [ ] Active Cisco Secure Endpoint subscription
- [ ] Admin role in the AMP Console
- [ ] Network: Conductor can reach your AMP API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to the **AMP Console** at `https://console.amp.cisco.com/`

    !!! tip "Regional Endpoints"
        North America: `api.amp.cisco.com` · Europe: `api.eu.amp.cisco.com` ·
        Asia Pacific: `api.apjc.amp.cisco.com`

2. Navigate to **Accounts** → **API Credentials**
3. Click **New API Credential**
4. Configure the credential:
    - **Application Name**: `WitFoo Conductor`
    - **Scope**: **Read-only**
5. Click **Create**
6. Copy the **Client ID** (3rd Party API Client ID) and **API Key**

!!! warning "Store Credentials Securely"
    API credentials grant read access to your AMP data. Store them securely and
    do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Cisco AMP**
3. Enter a unique name for this instance (e.g., "Cisco AMP North America")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api.amp.cisco.com` | API endpoint for your region |
    | **Client ID** | `<your-client-id>` | 3rd Party API Client ID |
    | **Client Secret** | `<your-api-key>` | API key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "cisco-amp"
    ```

    Look for successful poll messages:
    ```
    [INFO] cisco-amp: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **API Key** are correct
- Ensure the API credential has not been revoked in the AMP Console
- Check that the **FQDN** matches your AMP cloud region

### Forbidden (403)

- The API credential may have been created with insufficient scope
- Recreate with **Read-only** scope at minimum

### Rate Limited (429)

- Cisco AMP enforces per-minute API rate limits
- Increase the **Polling Interval** to 10 minutes if rate limiting occurs
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://api.amp.cisco.com`
- Confirm events exist in the AMP Console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
