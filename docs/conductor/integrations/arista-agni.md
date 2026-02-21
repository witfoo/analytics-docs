---
tags:
  - integration
  - identity
---

# Arista AGNI

Collects network identity and access data from Arista AGNI (formerly
CloudVision Guardian), including user sessions, client connections,
and network access events.

| | |
|---|---|
| **Category** | Identity & Access |
| **Connector Name** | `signal-client.arista-agni` |
| **Auth Method** | API Key (Bearer) |
| **Polling Interval** | 10 min (events), 1 hr (assets) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Arista CloudVision API](https://www.arista.com/en/support/product-documentation) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Arista AGNI or CloudVision deployment with API access.
    Admin access required to generate API keys.

- [ ] Active Arista AGNI / CloudVision subscription
- [ ] Admin access to the CloudVision portal
- [ ] Network: Conductor can reach your CloudVision instance on port 443

## Step 1: Create API Credentials

1. Log in to the **Arista CloudVision** portal
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Copy the **API Key** and note the **API Value** (secret)
5. Record the **Organization ID** from the portal settings

!!! warning "Store Credentials Securely"
    The API value is only shown once at creation time. Store it securely.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Arista AGNI**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<your-cloudvision-url>` | CloudVision instance URL |
    | **API Key** | `<your-api-key>` | API key from step 1 |
    | **API Value** | `<your-api-value>` | API secret from step 1 |

5. Set the **Polling Interval** (recommended: 10 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "arista"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key** and **API Value** are correct
- Ensure the key has not been revoked or expired

### Forbidden (403)

- The API key may not have sufficient access scope
- Verify the key has read permissions for AGNI data

### Rate Limited (429)

- Increase the **Polling Interval** to 30 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify the **Host** URL is correct and reachable
- Ensure the **Organization ID** matches your CloudVision deployment
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
