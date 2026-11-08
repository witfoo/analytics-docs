---
tags:
  - integration
  - cloud
---

# Azure VNet Flow Logs

Pulls Azure Network Watcher flow-log JSON blobs from a Storage account and
summarizes them into network conversations with the same flow engine as the
on-premises NetFlow/IPFIX collector. It can also read legacy NSG flow log
records.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.azure-vnet-flow-pull` |
| **Auth Method** | Microsoft Entra app (client credentials) or Storage SAS token |
| **Polling Interval** | 60 s |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [Virtual network flow logs](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview) |

This connector is separate from **Azure Security** (Microsoft Graph alerts)
and **Microsoft Sentinel** (incidents).

## Prerequisites

!!! note "Vendor Requirements"
    An Azure subscription with Network Watcher flow logs written to a Storage
    account, and permission to grant read access to that account.

- [ ] Virtual network flow logs (or legacy NSG flow logs) written to a Storage account
- [ ] Permission to create a Microsoft Entra app registration and assign it a role, or to create a SAS token
- [ ] Network: Conductor can reach the Storage account and, for an Entra app, Microsoft Entra ID, on port 443

## Step 1: Create API Credentials

Choose one way to authenticate.

### Option A: Microsoft Entra App (Recommended)

1. In the Azure portal, register an application in **Microsoft Entra ID**
2. Copy the **Directory (tenant) ID** and the **Application (client) ID**
3. Under **Certificates & secrets**, create a client secret and copy its
   **Value** (not the secret ID). It is shown once
4. On the Storage account, assign the app the **Storage Blob Data Reader**
   role. Grant nothing broader

### Option B: Storage SAS Token

1. On the Storage account, create a SAS token for the flow-log container
2. Grant **Read** and **List** only
3. Copy the SAS token

### Find the Container

| Flow log | Container |
|----------|-----------|
| Virtual network flow logs | `insights-logs-flowlogflowevent` |
| Legacy NSG flow logs | `insights-logs-networksecuritygroupflowevent` |

Configure one integration for each container.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Azure VNet Flow Logs**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Storage Account** | *(account name)* | The account that receives the flow logs: 3–24 lowercase letters and numbers |
    | **Container** | `insights-logs-flowlogflowevent` | The flow-log container |
    | **Blob Prefix (optional)** | *(blank)* | Only blobs whose name starts with this text are read. Leave empty to read the whole container |
    | **Azure Cloud** | Public (core.windows.net) | Or US Government (core.usgovcloudapi.net), or China 21Vianet (core.chinacloudapi.cn) |
    | **Authentication** | Microsoft Entra app (client credentials) | Or Storage SAS token |
    | **Directory (tenant) ID** | *(tenant ID)* | Entra app only |
    | **Application (client) ID** | *(client ID)* | Entra app only |
    | **Client Secret** | *(secret value)* | Entra app only. Enter the secret VALUE, not the secret ID |
    | **SAS Token** | *(SAS token)* | SAS only. A read and list SAS for the container |
    | **Also accept legacy NSG Flow Log records** | On | Read legacy NSG flow log records too. On by default for a new integration |

5. Toggle **Enabled** to on
6. Click **Save**

!!! info "Blob Prefix is case-sensitive"
    The prefix is compared exactly with the start of each blob name, upper and
    lower case included. Virtual network flow-log blob names start with
    `flowLogResourceID=/`, then the subscription ID **in upper case**, then
    `_NETWORKWATCHERRG/NETWORKWATCHER_`, the region and the flow log's name.
    The portal shows the subscription ID in lower case, which matches nothing.
    Legacy NSG names start with `resourceId=/SUBSCRIPTIONS/`. A prefix that
    matches nothing is not an error: the connector logs one warning and reads
    nothing.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "azure"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for network flow artifacts from this
   source

### How Reading Works

- Each blob is read forward from a saved position. A record Azure has only
  partly written is left unread and picked up on a later cycle.
- At most 32 blobs are read per cycle. This is a limit of the connector, not
  of Azure. In a very large container, a blob can wait several cycles for its
  turn.
- **Blobs not modified within the last 24 hours are not read**, so a
  connector stopped for longer than that does not fill the gap.
- Records refused while legacy NSG acceptance was off are not read again
  when you turn it on.

!!! note "NSG flow logs retire"
    Microsoft retires NSG flow logs on 30 September 2027. Move to virtual
    network flow logs.

## Troubleshooting

### Authentication Failed (401 or 403)

- Entra app: verify the tenant ID, client ID and secret **value**, and that
  the app has **Storage Blob Data Reader** on the Storage account
- SAS: verify the token grants **Read** and **List** on the container and has
  not expired
- Check that **Azure Cloud** matches the cloud of the Storage account

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm the **Container** is the one your flow logs write to
- Check the **Blob Prefix**: the subscription ID must be in upper case. Clear
  the prefix to read the whole container
- For legacy NSG records, turn on **Also accept legacy NSG Flow Log records**
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
