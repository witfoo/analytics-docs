---
tags:
  - integration
  - syslog
  - ot
---

# Dragos

Sends Dragos Platform notifications to WitFoo Conductor in Common Event Format
(CEF) over syslog, so Dragos OT detections appear in WitFoo Analytics
alongside the rest of your security data.

| | |
|---|---|
| **Category** | OT Security |
| **Collection** | Push: CEF over syslog |
| **Parser** | Dragos Platform parser |
| **Conductor Listener** | Syslog TCP or UDP 514, or Secure Syslog TLS 6514 |
| **Vendor Docs** | Dragos Platform Syslog Integration Guide, in the Dragos Customer Portal |

!!! note "Parser availability"
    The Dragos Platform parser ships in a coming WitFoo parser update. A
    Conductor without it still receives these messages but does not parse them.

## Prerequisites

!!! note "Vendor Requirements"
    A Dragos Platform deployment (SiteStore) and an account that can manage
    integrations and notification rules.

- [ ] Access to the Dragos Platform **Admin** and **Notification** pages
- [ ] Network: the Dragos Platform can reach Conductor on TCP 514 (or TLS 6514).
      OT and IT networks are often separated by firewalls, so check the path first
- [ ] The matching listener is enabled on the Conductor
      [Log Server page](../ui/log-servers.md)

## Step 1: Enable the Syslog Listener on Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/log-servers`
2. Make sure **Syslog TCP** (port 514) is enabled. For encrypted transport,
   enable **Secure Syslog TLS** (port 6514)

## Step 2: Add Conductor as a Syslog Server in Dragos

1. In the Dragos Platform, navigate to **Admin → Integrations**
2. In the **Syslog** section, select **LAUNCH**
3. Select **ADD NEW SERVER**, then enter Conductor's IP address or host name,
   the port of the listener you enabled in Step 1 and its protocol
4. For TCP and TLS, set the message delimiter to **newline**. Conductor's TCP
   514 and TLS 6514 listeners read one record per line
5. Select **NEXT**
6. For the **Message Template**, use a CEF template whose header names Dragos
   and Platform as the vendor and product (`CEF:0|Dragos|Platform|...`), as in
   Dragos's own CEF examples. WitFoo recognizes Dragos messages by that header
7. Select **SAVE**

## Step 3: Create a Notification Rule

1. Navigate to **Notification → RULES** and select **NEW RULE**
2. Choose the notifications to forward, for example all detections, or
   detections above a severity you choose
3. Set the action to send to the syslog server you added in Step 2
4. Save the rule

## Step 4: Validate Data Flow

1. Wait for the next notification that matches the rule
2. In **Admin → Integrations**, check that the syslog server shows as
   **Connected**
3. In WitFoo Analytics, open **Signals → Search** and search for artifacts from
   the Dragos Platform's IP address

## What You Will See

- Each forwarded notification becomes an artifact. The assets it names appear
  on the graph with the connection between them, and notifications that match
  WitFoo's detection rules can open work units.
- Asset inventory, vulnerability and zone data from the Dragos Platform are not
  collected over syslog.

## Troubleshooting

### No Data Appearing

- In **Admin → Integrations**, check that the syslog server shows as
  **Connected**
- Check that the notification rule's criteria match the notifications you
  expect, and that its action sends to the Conductor server
- Confirm the listener is enabled on the Conductor Log Server page and that
  the port is open between the OT network and Conductor

### Messages Arrive but Are Not Parsed

- Check that your Conductor has the parser update that includes the Dragos
  Platform parser
- Check that the message template keeps the CEF header
  `CEF:0|Dragos|Platform|...` (see Step 2)
- If the messages that reach Conductor start with a number and a space (for
  example `123 <134>`), the sender is framing records by length. Set it to end
  each record with a newline instead, or ask WitFoo support which listener to
  use
- If the messages pass through a relay or log forwarder, send them straight
  from the Dragos Platform instead

!!! info "Unrecognized log lines"
    By default, WitFoo appliances send log lines they cannot parse to WitFoo,
    redacted according to the appliance's redaction setting, to help build new
    parsers. Until the Dragos Platform parser is on your Conductor, Dragos
    messages are such lines. If you do not want them sent, contact WitFoo
    support before you point the Dragos Platform at Conductor.
    A licensed appliance that is not in Offline mode also asks WitFoo for
    queued support jobs every 60 seconds; the released version has no setting
    specific to that channel. See WitFoo's diagnostic and telemetry disclosure.

---

*See also: [Syslog Sources](index.md) ·
[Signal Server](../signal-server.md) ·
[Log Server Configuration](../ui/log-servers.md) ·
[Parser Catalog](../parsers-catalog.md) ·
[Common Troubleshooting](../integrations/common-troubleshooting.md)*
