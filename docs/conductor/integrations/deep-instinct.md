---
tags:
  - integration
  - endpoint
---

# Deep Instinct

Collects threat event data from Deep Instinct's deep learning-based endpoint
protection platform, providing visibility into malware prevention, detection
events, and device inventory.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.deep-instinct` |
| **Auth Method** | API Key (Bearer Token) |
| **Polling Interval** | 5 min (events) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Deep Instinct API Documentation](https://help.deepinstinct.com/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Deep Instinct subscription with API access. Admin role required
    to generate API keys.

- [ ] Active Deep Instinct D-Appliance or D-Cloud subscription
- [ ] Administrator access to the Deep Instinct Management Console
- [ ] Network: Conductor can reach your Deep Instinct management server on port 443

## Step 1: Create API Credentials

1. Log in to the **Deep Instinct Management Console** at `https://<your-instance>.deepinstinctweb.com/`
2. Navigate to **Settings** → **API Keys**
3. Click **Generate New API Key**
4. Configure the key:
    - **Name**: `WitFoo Conductor`
    - **Permissions**: **Read-only**
5. Copy the generated **API Key**

!!! warning "Store Credentials Securely"
    API keys grant access to your Deep Instinct data. Store them securely and
    do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Deep Instinct**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<your-instance>.deepinstinctweb.com` | Management server URL |
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
    docker logs signal-client-svc --tail=50 | grep "deep-instinct"
    ```

    Look for successful poll messages:
    ```
    [INFO] deep-instinct: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key** is correct and has not been revoked
- Ensure the key has not expired in the Deep Instinct Console

### Forbidden (403)

- The API key may lack read permissions
- Generate a new key with appropriate permissions

### Rate Limited (429)

- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://<your-instance>.deepinstinctweb.com`
- Confirm events exist in the Deep Instinct console for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
