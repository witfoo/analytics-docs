---
tags:
  - integration
  - endpoint
---

# Sophos Central

Collects endpoint protection and security event data from Sophos Central,
including malware detections, web filtering events, and endpoint inventory.

| | |
|---|---|
| **Category** | Endpoint Security |
| **Connector Name** | `signal-client.sophos-central` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | 5 min (alerts), 1 hr (endpoints) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Sophos Central API](https://developer.sophos.com/intro) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Sophos Central subscription. Super Admin or Admin role required
    to create API credentials.

- [ ] Active Sophos Central account
- [ ] Super Admin or Admin role
- [ ] Network: Conductor can reach `id.sophos.com` and regional API
  endpoints on port 443

## Step 1: Create API Credentials

1. Log in to **Sophos Central** at `https://central.sophos.com/`
2. Navigate to **Global Settings** → **API Credentials Management**
3. Click **Add Credential**
4. Name the credential (e.g., "WitFoo Conductor")
5. Assign the role: `Service Principal ReadOnly` (minimum required)
6. Click **Add**
7. Copy the **Client ID** and **Client Secret**

!!! info "Region Auto-Discovery"
    Sophos Central uses a `/whoami` endpoint to automatically determine
    your regional API endpoint. Conductor handles this automatically — you
    only need to provide the Client ID and Client Secret.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Sophos Central**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Client ID** | `<your-client-id>` | From step 1 |
    | **Client Secret** | `<your-client-secret>` | From step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes for alerts)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "sophos"
    ```

    Look for successful authentication and poll messages:
    ```
    [INFO] sophos-central: authenticated via OAuth2
    [INFO] sophos-central: fetched <N> alerts
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Client Secret** are correct
- Ensure the credential has not been deleted in Sophos Central
- Check that the credential role has sufficient permissions

### Forbidden (403)

- The API credential may have insufficient role scope
- Verify at least `Service Principal ReadOnly` is assigned

### Rate Limited (429)

- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify events exist in Sophos Central for the polling window
- Confirm network connectivity to `id.sophos.com`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
