---
tags:
  - integration
  - syslog
  - ot
---

# Nozomi Networks

Sends alerts, health events and audit events from Nozomi Networks Guardian
sensors or the Central Management Console (CMC) to WitFoo Conductor in Common
Event Format (CEF) over syslog. Conductor parses them with the `nozomi_n2os`
parser, so OT alerts appear in WitFoo Analytics alongside the rest of your
security data.

| | |
|---|---|
| **Category** | OT Security |
| **Collection** | Push: CEF over syslog |
| **Parser** | `nozomi_n2os` |
| **Conductor Listener** | Syslog TCP or UDP 514, or Secure Syslog TLS 6514 |
| **Vendor Docs** | [Nozomi Networks: Common Event Format (CEF)](https://technicaldocs.nozominetworks.com/guardian/latest/products/n2os/topics/administration/settings/data-integration/c_n2os_admin_settings_data-integration_cef.html) |

!!! note "Parser availability"
    This guide applies to a Conductor that has the WitFoo parser update which
    includes the `nozomi_n2os` parser. A Conductor without it still receives
    these messages but does not parse them.

## Prerequisites

!!! note "Vendor Requirements"
    A Nozomi Networks Guardian sensor or CMC running N2OS, and an administrator
    account on it.

- [ ] Administrator access to the Guardian or CMC web console
- [ ] Network: the Guardian or CMC can reach Conductor on TCP 514 (or 6514).
      OT and IT networks are often separated by firewalls, so check the path first
- [ ] The matching listener is enabled on the Conductor
      [Log Server page](../ui/log-servers.md)

## Step 1: Enable the Syslog Listener on Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/log-servers`
2. Make sure **Syslog TCP** (port 514) is enabled. For encrypted transport,
   enable **Secure Syslog TLS** (port 6514). Port 6514 uses TLS when TLS is
   enabled on the Conductor node (the configuration wizard's default); plain
   TCP otherwise

!!! tip "Prefer TCP or TLS"
    UDP syslog can drop messages under load. Use TCP 514 or 6514 for alerts
    you need to keep.

## Step 2: Add a CEF Endpoint in Nozomi

1. In the Guardian or CMC web console, select the **gear icon** in the top
   navigation bar to open **Administration**
2. Under **Settings**, select **Data integration**
3. In the top right, select **Add**
4. From the **Choose a configuration** list, select **CEF**
5. Enter Conductor's IP address or host name and the port of the listener you
   enabled in Step 1
6. For encrypted transport, select **TLS**. To have the sensor check
   Conductor's certificate against a certificate authority, also select
   **CA-emitted TLS certificate**
7. Save the endpoint

!!! warning "Send straight to Conductor"
    The parser reads CEF records as N2OS sends them, with or without a standard
    syslog header (RFC 3164 or RFC 5424). A relay or log forwarder that adds its
    own header or prefix in front of the record stops the parser from
    recognizing it. Point the Guardian or CMC directly at Conductor.

## Step 3: Validate Data Flow

1. Wait for the next alert or health event from the sensor
2. In WitFoo Analytics, open **Signals → Search** and search for artifacts from
   the Guardian or CMC IP address, or for `stream_name=nozomi_n2os` (use the
   equals sign: a colon is a text match that can miss a quiet source on a busy
   system)
3. Open an alert artifact and check that the source and destination assets,
   the rule name and the severity are filled in

## What You Will See

- **Alerts** become artifacts with the source and destination assets (IP
  address, port, MAC address and host name where Nozomi sends them), the
  protocol, the rule name and a severity derived from Nozomi's risk score.
  Nozomi's MITRE ATT&CK technique and tactic labels are kept as tags.
- **Audit events** record the user name N2OS sends as the acting user and the
  appliance; what was changed stays in the message text.
- **Health events** record the sensor's own status.
- Alerts that Nozomi marks as security alerts are recorded as intrusion
  detection events, which WitFoo's detection rules score and can open work
  units from. Other alerts, such as a learned-behavior change or a link check,
  are recorded as network monitoring events, which no built-in detection rule
  keys on, and are kept for search. An alert that names only one node is
  recorded as that node, with no connection.
- Audit and health events are kept for search; they do not open work units by
  themselves.
- Asset inventory and vulnerability data from Nozomi's API are not collected
  over syslog.

## Troubleshooting

### No Data Appearing

- Confirm the CEF endpoint is saved on the Guardian or CMC
- Confirm the listener is enabled on the Conductor Log Server page and that
  the port is open between the OT network and Conductor
- For TLS 6514 with **CA-emitted TLS certificate** selected, Conductor's
  certificate must be issued by a certificate authority the sensor trusts

### Messages Arrive but Are Not Parsed

- Check that your Conductor has the parser update that includes `nozomi_n2os`
- If the messages pass through a relay or log forwarder, send them straight
  from the sensor instead (see Step 2)
- Only one standard syslog header may come before the CEF text. A second
  header, a date written as `YYYY-MM-DD HH:MM:SS`, and a syslog header without
  its structured-data field (RFC 5424 puts a `-` there) are not recognized
- If the messages that reach Conductor start with a number and a space (for
  example `123 <134>`), the sender is framing records by length. Set it to end
  each record with a newline instead, or ask WitFoo support which listener to
  use

!!! info "Unrecognized log lines"
    By default, WitFoo appliances send log lines they cannot parse to WitFoo,
    redacted according to the appliance's redaction setting, to help build new
    parsers. Nozomi messages that no parser recognizes, including all of them
    on a Conductor without the `nozomi_n2os` parser, are such lines. If you do
    not want them sent, contact WitFoo support before you point the sensor at
    Conductor.
    A licensed appliance that is not in Offline mode also asks WitFoo for
    queued support jobs every 60 seconds; the released version has no setting
    specific to that channel.

---

*See also: [Syslog Sources](index.md) ·
[Signal Server](../signal-server.md) ·
[Log Server Configuration](../ui/log-servers.md) ·
[Parser Catalog](../parsers-catalog.md) ·
[Common Troubleshooting](../integrations/common-troubleshooting.md)*
