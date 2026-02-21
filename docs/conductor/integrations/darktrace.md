---
tags:
  - integration
  - network
---

# Darktrace

Collects threat detection data from Darktrace, including model breaches,
AI Analyst incidents, and network anomaly detections from Darktrace's
self-learning AI platform.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.darktrace` |
| **Auth Method** | HMAC Token (Public + Private) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Darktrace API Documentation](https://customerportal.darktrace.com/product-guides/main/api-overview) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Darktrace deployment. Admin access to the Darktrace Threat
    Visualizer to create API tokens.

- [ ] Active Darktrace appliance
- [ ] Admin access to Darktrace Threat Visualizer
- [ ] Network: Conductor can reach the Darktrace appliance on port 443

## Step 1: Create API Credentials

1. Log in to the **Darktrace Threat Visualizer** at
   `https://<appliance-address>/`
2. Navigate to **System Config** → **API Tokens**
3. Click **Create Token**
4. Copy the **Public Token** and **Private Token**

!!! warning "Token Storage"
    The private token is only shown once at creation time. Store it securely.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Darktrace**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<appliance-address>` | Darktrace appliance URL or IP |
    | **Public Token** | `<your-public-token>` | Public API token from step 1 |
    | **Private Token** | `<your-private-token>` | Private API token from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

!!! info "HMAC Authentication"
    Darktrace uses HMAC-SHA1 request signing for API authentication.
    Conductor handles the signing automatically using the public and
    private tokens — no additional configuration needed.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "darktrace"
    ```

    Look for successful poll messages:
    ```
    [INFO] darktrace: fetched <N> model breaches
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Detection Types Collected

| Type | Description |
|------|-------------|
| Model Breaches | Rule-based anomaly detections |
| AI Analyst Incidents | AI-correlated security narratives |

## Troubleshooting

### Authentication Failed (401)

- Verify the **Public Token** and **Private Token** are correct
- Ensure the API token has not been revoked in Darktrace
- Clock skew between Conductor and Darktrace can cause HMAC signature
  failures — ensure both systems use NTP

### Network Connectivity

- The Darktrace appliance must be reachable from the Conductor host on
  port 443
- If using a self-signed TLS certificate on the appliance, see
  [Common Troubleshooting](common-troubleshooting.md#tls-certificate-errors)

### Forbidden (403)

- The API token may have restricted access scope
- Create a new token with broader permissions

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify model breaches exist in the Darktrace Threat Visualizer
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Confirm the appliance address is correct and reachable

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
