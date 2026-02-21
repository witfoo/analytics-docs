---
tags:
  - integration
  - network
---

# Zscaler ZIA

Collects web security and threat event data from Zscaler Internet Access
(ZIA), including web transactions, firewall logs, DNS logs, and threat events.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.zscaler-zia` |
| **Auth Method** | API Key + Admin Credentials |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Zscaler ZIA API](https://help.zscaler.com/zia/getting-started-zia-api) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Zscaler Internet Access subscription. Admin access to ZIA
    Admin Portal. API access must be enabled for your organization.

- [ ] Active ZIA subscription
- [ ] Admin access to ZIA Admin Portal
- [ ] API key from ZIA administration
- [ ] Network: Conductor can reach your ZIA admin portal on port 443

## Step 1: Create API Credentials

1. Log in to the **ZIA Admin Portal** at `https://admin.zs<cloud>.net/`
2. Navigate to **Administration** → **API Key Management**
3. Copy the **API Key** displayed
4. Note your admin **email** and **password** (used for API authentication)

!!! info "ZIA Cloud Identifiers"
    Zscaler uses cloud-specific admin portal URLs. Select the correct
    base URL:

    | Cloud | Admin URL |
    |-------|-----------|
    | Zscaler | `admin.zscaler.net` |
    | ZscalerOne | `admin.zscalerone.net` |
    | ZscalerTwo | `admin.zscalertwo.net` |
    | ZscalerThree | `admin.zscalerthree.net` |
    | ZscalerBeta | `admin.zscloud.net` |
    | Zscaler Gov | `admin.zscalergov.net` |

    Check your Zscaler documentation or account team if unsure which cloud
    you are on.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Zscaler ZIA**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Base URL** | `admin.zscaler.net` | ZIA admin portal URL (see table) |
    | **API Key** | `<your-api-key>` | From API Key Management |
    | **Username** | `<admin-email>` | Admin account email |
    | **Password** | `<admin-password>` | Admin account password |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "zscaler"
    ```

    Look for successful poll messages:
    ```
    [INFO] zscaler-zia: authenticated, fetching events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Key**, **Username**, and **Password** are correct
- Ensure the admin account is not locked or disabled
- Zscaler uses timestamp obfuscation for authentication; Conductor handles
  this automatically

### Wrong Cloud

- If you see connection errors, verify the **Base URL** matches your Zscaler
  cloud (see table above)
- The base URL is different from the user-facing ZIA service URL

### Forbidden (403)

- The admin account may not have API access enabled
- Contact your Zscaler admin to verify API access permissions

### Rate Limited (429)

- Increase the **Polling Interval** to 15 minutes
- Conductor automatically implements exponential backoff

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify web traffic is flowing through ZIA (check ZIA dashboard)
- Confirm the admin portal URL is correct

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
