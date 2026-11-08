---
tags:
  - integration
  - network
---

# SNMP Monitoring Poller

Polls the network devices you list over SNMP v2c or v3 for interface
counters, device health and reachability.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.snmp-poll` |
| **Auth Method** | SNMP v2c community, or SNMP v3 user (authPriv recommended) |
| **Polling Interval** | Per target: 60 s by default, 30 s minimum |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [RFC 3414: SNMPv3 User-based Security Model](https://datatracker.ietf.org/doc/html/rfc3414) |

This connector polls devices. It is separate from the `snmpd` parser, which
reads the log lines of the snmpd daemon sent over syslog. SNMPv1 is not
supported.

## Prerequisites

!!! note "Vendor Requirements"
    Devices that answer SNMP v2c or v3, and access to their SNMP
    configuration.

- [ ] SNMP v2c or v3 enabled on each device
- [ ] For v3: a read-only SNMP user on each device
- [ ] Network: Conductor can reach each device on its SNMP port (UDP 161 by default)

## Step 1: Create API Credentials

Create read-only SNMP credentials on each device. Use SNMP v3 with
**authPriv** where the device supports it:

| Setting | Supported values |
|---------|------------------|
| Security level | `noAuthNoPriv`, `authNoPriv`, `authPriv` |
| Authentication protocol | `SHA`, `SHA-224`, `SHA-256`, `SHA-384`, `SHA-512` (MD5 is not offered) |
| Privacy protocol | `AES`, `AES-192`, `AES-256` (DES is not offered) |

For SNMP v2c, set a read-only community string, and restrict which addresses
may query the device to the Conductor's address.

!!! warning "Read-only access"
    The poller only reads. Give the user or community read-only access to the
    MIB views it needs, never write access.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **SNMP Monitoring Poller**
3. Enter a unique name for this instance
4. For each device, fill in a target. Click **Add Target** to add another:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `192.0.2.10` or `switch1.example.com` | IP address or DNS name only: no scheme, no `:port`, no credentials |
    | **Port** | `161` | SNMP port, 1–65535 |
    | **SNMP Version** | `v3` | `v2c` or `v3` |
    | **Community String** | *(community)* | v2c only. Never logged |
    | **Security Level** | `authPriv` | v3 only |
    | **Security Name (User)** | *(user)* | v3 only |
    | **Authentication Protocol** | `SHA-256` | v3 with authNoPriv or authPriv |
    | **Authentication Passphrase** | *(passphrase)* | v3 with authNoPriv or authPriv. Never logged |
    | **Privacy Protocol** | `AES-256` | v3 with authPriv |
    | **Privacy Passphrase** | *(passphrase)* | v3 with authPriv. Never logged |
    | **Poll Interval (seconds)** | `60` | Minimum 30. A lower value is raised to 30 |
    | **Collect HOST-RESOURCES-MIB (CPU / memory / storage)** | Off | Also read CPU load and memory use |

5. Toggle **Enabled** to on
6. Click **Save**

An instance holds up to 512 targets.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**. The poller writes one summary line per cycle:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "snmp"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts of stream `snmp` and message
   type `network_monitor_event`

### What It Collects

| Group | Objects |
|-------|---------|
| SNMPv2-MIB | `sysUpTime`, `sysName`, `sysDescr` |
| IF-MIB `ifTable` | Interface index, description, speed, admin and operational status, octets, errors and discards |
| IF-MIB `ifXTable` (preferred) | Interface name, 64-bit octet counters, high speed, alias |
| HOST-RESOURCES-MIB (optional) | Processor load and memory use |

- Only interfaces that are administratively up are reported, up to 1,024
  interfaces per device.
- The first poll after start-up reports status only: utilization needs two
  readings.
- When a device restarts, its counters start again and that poll reports
  status only.
- Monitoring polls never create work units.

## Troubleshooting

### Device Reported Down

- A device that does not answer is reported as `device_down`. Reachability is
  data, not a pipeline error, so the other devices are still polled
- Check that the Conductor can reach the device on its SNMP port
- Check the community string, or the v3 user, protocols and passphrases

### Device Reported Degraded

- A device that answers the basic objects but fails an interface or
  host-resources walk is reported as `device_degraded`, naming the part that
  failed. Check the device's SNMP view

### No Utilization Values

- Utilization appears from the second poll onwards
- A device that reports no interface speed has no utilization percentage

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- If every target fails, the connector backs off: check the Conductor's route
  to the management network
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
