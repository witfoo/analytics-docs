---
tags:
  - integration
  - network
---

# Fortinet FortiAnalyzer

Collects log and event data from Fortinet FortiAnalyzer, the centralized
logging and analytics platform for Fortinet security fabric devices.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.fortianalyzer` |
| **Auth Method** | Session Token (JSON-RPC) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [FortiAnalyzer REST API](https://docs.fortinet.com/document/fortianalyzer/7.4.0/administration-guide/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active FortiAnalyzer deployment (physical or virtual appliance).
    Admin access to create API administrator accounts.

- [ ] Active FortiAnalyzer instance (v7.0+)
- [ ] Admin access to the FortiAnalyzer web UI
- [ ] ADOM (Administrative Domain) name
- [ ] Network: Conductor can reach the FortiAnalyzer IP on port 443

## Step 1: Create API Credentials

1. Log in to the **FortiAnalyzer** web UI at `https://<fortianalyzer-ip>/`
2. Navigate to **System Settings** → **Admin** → **Administrators**
3. Click **Create New**
4. Set the **Admin Profile** to `Standard_User` or a custom read-only profile
5. Configure the following:
    - Username and password
    - Enable **JSON API Access** (set to **Read-Only**)
    - Restrict **Trusted Hosts** to the Conductor IP if desired
6. Click **OK** to save

!!! info "ADOM Concept"
    FortiAnalyzer uses Administrative Domains (ADOMs) to organize logs by
    customer or network segment. Use `root` for the default domain, or
    specify the ADOM that contains the logs you want to collect.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **FortiAnalyzer**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `<fortianalyzer-ip>` | FortiAnalyzer IP or hostname |
    | **Username** | `<your-username>` | API admin from step 1 |
    | **Password** | `<your-password>` | API admin password |
    | **ADOM** | `root` | Administrative Domain (default: `root`) |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "fortianalyzer"
    ```

    Look for successful session messages:
    ```
    [INFO] fortianalyzer: session established, fetching logs
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Username** and **Password** are correct
- Ensure **JSON API Access** is enabled for the admin account
- Check that the admin account is not locked

### Forbidden (403)

- The admin profile may not have read access to the specified ADOM
- Verify the admin has access to the target ADOM in FortiAnalyzer

### Session Timeout

- FortiAnalyzer sessions have configurable idle timeouts
- Conductor handles automatic re-authentication when sessions expire
- If persistent failures occur, check admin session settings in FortiAnalyzer

### Wrong ADOM

- If data appears from the wrong devices, verify the **ADOM** field
- Use `root` for the default domain
- List available ADOMs in FortiAnalyzer under **System Settings** → **All ADOMs**

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check the FortiAnalyzer has devices forwarding logs to it
- Verify network connectivity: `curl -k https://<fortianalyzer-ip>/jsonrpc`
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
