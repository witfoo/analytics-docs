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
    This guide applies to a Conductor that has the WitFoo parser update which
    includes the Dragos Platform parser (stream name `dragos_platform`). A
    Conductor without it still receives these messages but does not parse them.

## Prerequisites

!!! note "Vendor Requirements"
    A Dragos Platform deployment (SiteStore) and an account that can manage
    integrations and notification rules.

- [ ] Access to the Dragos Platform **Admin** and **Notification** pages
- [ ] Network: the Dragos Platform can reach Conductor on TCP 514 (or 6514).
      OT and IT networks are often separated by firewalls, so check the path first
- [ ] The matching listener is enabled on the Conductor
      [Log Server page](../ui/log-servers.md)

## Step 1: Enable the Syslog Listener on Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/log-servers`
2. Make sure **Syslog TCP** (port 514) is enabled. For encrypted transport,
   enable **Secure Syslog TLS** (port 6514). Port 6514 uses TLS when TLS is
   enabled on the Conductor node (the configuration wizard's default); plain
   TCP otherwise

## Step 2: Add Conductor as a Syslog Server in Dragos

1. In the Dragos Platform, navigate to **Admin → Integrations**
2. In the **Syslog** section, select **LAUNCH**
3. Select **ADD NEW SERVER**, then enter Conductor's IP address or host name,
   the port of the listener you enabled in Step 1 and its protocol
4. For TCP and TLS, set the message delimiter to **newline**. Conductor's TCP
   514 and 6514 listeners read one record per line
5. Select **NEXT**
6. For the **Message Template**, use a CEF template whose header names Dragos
   and Platform as the vendor and product (`CEF:0|Dragos|Platform|...`), as in
   Dragos's own CEF examples. WitFoo recognizes Dragos messages by that header.
   The CEF text must start the message, after at most one standard syslog
   header, so do not add text of your own in front of it. A key=value or LEEF
   template is not recognized
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
   the Dragos Platform's IP address, or for `stream_name=dragos_platform` (use
   the equals sign: a colon is a text match that can miss a quiet source on a
   busy system)

## What You Will See

- Each forwarded notification becomes an artifact. It records the assets the
  notification names, with an address, MAC address or host name where the
  notification gives exactly one value for it, the notification's summary as
  the rule name, and its severity, detection type and ATT&CK text as tags.
- When the Conductor's optional deduplication is on, notifications that are
  alike (same sender, endpoints, type and severity) are combined, so there can
  be fewer artifacts than notifications.
- A notification about one asset records that asset on the graph, when the
  notification gives an address for it. A connection between two assets appears
  only when the notification names both, each with an address.
- Indicator, Modeling and Threat Behavior notifications are recorded as
  intrusion detection events, which WitFoo's detection rules score and can open
  work units from. A work unit opens only when the notification names both
  assets, each with an address, and the rule's conditions are met. On a
  licensed appliance those conditions include a syslog severity of 0 to 4 in
  the priority the Dragos syslog settings write; the common default (priority
  134, severity 6) does not qualify. Configuration notifications are recorded
  as network monitoring events, which no built-in detection rule keys on, and
  are kept for search.
- Other notifications, for example the platform's own sign-in notices, are
  recorded as generic events and kept for search.
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
  `CEF:0|Dragos|Platform|...` (see Step 2) and that nothing but one standard
  syslog header comes before it. A syslog header written without its
  structured-data field (RFC 5424 puts a `-` there) is not recognized either
- If the messages that reach Conductor start with a number and a space (for
  example `123 <134>`), the sender is framing records by length. Set it to end
  each record with a newline instead, or ask WitFoo support which listener to
  use
- If the messages pass through a relay or log forwarder, send them straight
  from the Dragos Platform instead

!!! info "Unrecognized log lines"
    By default, WitFoo appliances send log lines they cannot parse to WitFoo,
    redacted according to the appliance's redaction setting, to help build new
    parsers. Dragos messages that no parser recognizes, including all of them
    on a Conductor without the Dragos Platform parser, are such lines. If you
    do not want them sent, contact WitFoo support before you point the Dragos
    Platform at Conductor.
    A licensed appliance that is not in Offline mode also asks WitFoo for
    queued support jobs every 60 seconds; the released version has no setting
    specific to that channel.

---

*See also: [Syslog Sources](index.md) ·
[Signal Server](../signal-server.md) ·
[Log Server Configuration](../ui/log-servers.md) ·
[Parser Catalog](../parsers-catalog.md) ·
[Common Troubleshooting](../integrations/common-troubleshooting.md)*
