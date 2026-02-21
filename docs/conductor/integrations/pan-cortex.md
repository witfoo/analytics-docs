---
tags:
  - integration
  - network
---

# Palo Alto Cortex

Collects security incidents and alerts from Palo Alto Networks Cortex XDR,
providing visibility into endpoint and network threat detections across the
Cortex platform.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.pan-cortex` |
| **Auth Method** | API Key (x-xdr-auth-id + Authorization) |
| **Polling Interval** | 5 min (incidents), 10 min (alerts) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Cortex XDR API Reference](https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-API-Reference) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Palo Alto Networks Cortex XDR subscription. Instance Administrator
    role required to create API keys.

- [ ] Active Cortex XDR Pro or Prevent subscription
- [ ] Instance Administrator role in Cortex XDR
- [ ] Network: Conductor can reach your Cortex XDR API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to **Cortex XDR** at `https://<your-instance>.xdr.paloaltonetworks.com/`
2. Navigate to **Settings** → **Configurations** → **Integrations** → **API Keys**
3. Click **+ New Key**
4. Configure the key:
    - **Security Level**: **Advanced**
    - **Role**: **Viewer**
5. Click **Generate**
6. Copy the **API Key** and note the **API Key ID**
7. Note your **FQDN** — the full API URL (e.g., `api-<instance>.xdr.us.paloaltonetworks.com`)

!!! warning "Store Credentials Securely"
    API keys grant access to your Cortex XDR data. Store them securely and
    do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **PAN Cortex**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **FQDN** | `api-<instance>.xdr.us.paloaltonetworks.com` | Cortex XDR API FQDN |
    | **Client ID** | `<api-key-id>` | Numeric API key ID |
    | **Secret** | `<api-key>` | API key value from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "pan-cortex"
    ```

    Look for successful poll messages:
    ```
    [INFO] pan-cortex: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first data pull occurs within the configured polling interval after
    saving. For a 5-minute interval, expect data within 5 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key ID** and **API Key** are correct
- Ensure the API key has not been revoked in Cortex XDR
- Check that the **FQDN** matches your Cortex XDR instance region

### Forbidden (403)

- The API key may lack required permissions
- Ensure the key was created with at least **Viewer** role
- Verify the **Security Level** is set to **Advanced** (not Standard)

### Rate Limited (429)

- Cortex XDR API has per-minute rate limits
- Increase the **Polling Interval** to 10 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity to the Cortex XDR API FQDN
- Confirm incidents or alerts exist in the Cortex XDR console

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
