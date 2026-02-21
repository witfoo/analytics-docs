---
tags:
  - integration
  - infrastructure
---

# DNS Zone Transfer

Collects DNS zone records via AXFR (Authoritative Zone Transfer), providing
visibility into DNS infrastructure, record changes, and domain inventory.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.dns-zone-transfer` |
| **Auth Method** | None (AXFR protocol) |
| **Polling Interval** | 60 min (zone transfers) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [RFC 5936 — DNS Zone Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5936) |

## Prerequisites

!!! note "Requirements"
    Your DNS server must allow AXFR zone transfers from the Conductor host's
    IP address. This is a server configuration, not a vendor subscription.

- [ ] DNS server(s) configured to allow AXFR transfers
- [ ] Conductor host IP address allowlisted for zone transfers
- [ ] Network: Conductor can reach DNS server(s) on port 53 (TCP)

## Step 1: Configure DNS Server for AXFR

Zone transfer configuration varies by DNS server software. Ensure the
Conductor host is authorized.

=== "BIND"

    In `named.conf`, add the Conductor IP to `allow-transfer`:
    ```
    zone "example.com" {
        type master;
        file "/etc/bind/zones/example.com.zone";
        allow-transfer { <conductor-ip>; };
    };
    ```

=== "Windows DNS"

    1. Open **DNS Manager**
    2. Right-click the zone → **Properties** → **Zone Transfers** tab
    3. Select **Allow zone transfers** → **Only to the following servers**
    4. Add the Conductor host IP address

=== "Infoblox"

    1. Navigate to **Data Management** → **DNS** → **Zones**
    2. Edit the zone → **Zone Transfers** tab
    3. Add the Conductor host IP to the **Allow Transfer** list

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **DNS Zone Transfer**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **DNS Server IP** | `10.0.1.53` | Primary DNS server address |
    | **Forward Lookup Zones** | `example.com,internal.local` | Comma-separated zone names |

5. Set the **Polling Interval** (recommended: 60 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator after the first transfer
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "dns-zone-transfer"
    ```

    Look for successful transfer messages:
    ```
    [INFO] dns-zone-transfer: fetched <N> records
    ```

3. **Test manually** — Verify AXFR works from the Conductor host:

    ```bash
    dig @10.0.1.53 example.com AXFR
    ```

!!! tip "First Poll Timing"
    The first zone transfer occurs within the configured polling interval
    after saving. For a 60-minute interval, expect data within 1 hour.

## Troubleshooting

### Authentication Failed (401)

- DNS zone transfers do not use authentication — this error is not applicable
- If access is denied, see **Forbidden** below

### Forbidden (403)

- The DNS server is refusing the zone transfer
- Verify the Conductor host IP is in the server's `allow-transfer` list
- Check DNS server logs for transfer denied messages

### Rate Limited (429)

- DNS zone transfers are not rate limited in the traditional sense
- However, very frequent transfers may impact DNS server performance
- Keep the polling interval at 60 minutes or longer

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity on TCP port 53 to the DNS server
- Test manually: `dig @<dns-server> <zone> AXFR`
- Ensure the zone names are spelled correctly

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
