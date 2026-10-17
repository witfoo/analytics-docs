---
tags:
  - integration
  - siem
---

# LevelBlue USM Anywhere

Pulls **alarms** and **events** from the LevelBlue USM Anywhere platform
(formerly AT&T Cybersecurity / AlienVault) through its **API 2.0**, using
OAuth2 client-credentials authentication. This lets an MSSP or SOC ingest a
USM Anywhere tenant's detections into WitFoo by provisioning a single API
client credential — the managed LevelBlue collection agents keep shipping to
USM Anywhere unchanged.

| | |
|---|---|
| **Category** | SIEM |
| **Connector Name** | `signal-client.usm-anywhere-events` |
| **Auth Method** | OAuth2 Client Credentials |
| **Polling Interval** | About every 60 seconds (built in, not configurable) |
| **Multi-Instance** | One instance per Conductor (see [One instance per Conductor](#one-instance-per-conductor)) |
| **API Base** | `https://<subdomain>.alienvault.cloud/api/2.0` |
| **Vendor Docs** | [LevelBlue: API Clients](https://docs.levelblue.com/documentation/usm-anywhere/user-guide/user-management/api-clients) |

!!! note "Availability"
    This connector was introduced in WitFoo 1.1.0. Alarm and event field
    extraction is built against the LevelBlue USM Anywhere API 2.0 reference.
    If records from your tenant classify unexpectedly, contact WitFoo support
    with a sample so the mapping can be confirmed.

## Prerequisites

!!! note "Vendor Requirements"
    An active USM Anywhere subscription whose edition includes the API
    (LevelBlue documents the API as available in the Standard and Premium
    editions) and permission to create an API client in your tenant.

- [ ] Active LevelBlue USM Anywhere subscription with API access
- [ ] A USM Anywhere **API client** (Client ID + Secret)
- [ ] Your tenant **subdomain** — the bare DNS label from your USM Anywhere
  URL `https://<subdomain>.alienvault.cloud`
- [ ] Network: Conductor can reach `<subdomain>.alienvault.cloud` on port 443

## Step 1: Create API Credentials in USM Anywhere

1. Log in to your USM Anywhere tenant
2. In the USM Anywhere web UI secondary menu, select **Profile Settings**,
   open the **API Clients** tab and click **New Client** (menu names follow
   the LevelBlue documentation and can change between USM Anywhere versions)
3. Copy the generated **Client ID** and **Client Secret**

    !!! warning "Protect the secret"
        Treat the client secret like a password. Store it in your secrets
        manager and do not paste it into tickets or chat.

4. Make sure the API client is **enabled** — the API Clients tab shows an
   enable toggle for each client
5. Note your **subdomain** — the label before `.alienvault.cloud` in your
   tenant URL. For `https://acme-soc.alienvault.cloud/`, the subdomain is
   `acme-soc`

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at
   `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **LevelBlue USM Anywhere**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | JSON key | Required | Default | Notes |
    |-------|----------|----------|---------|-------|
    | **Subdomain** | `subdomain` | Yes | — | Bare DNS label only — do **not** include `https://` or `.alienvault.cloud`. Must match `^[a-z0-9-]{1,63}$`; the request host is always composed as `<subdomain>.alienvault.cloud`. |
    | **Client ID** | `client_id` | Yes | — | OAuth2 client id (sent as the HTTP Basic username during the token grant). |
    | **Secret** | `secret` | Yes | — | OAuth2 client secret. Masked in the form. |
    | **Collect Alarms** | `collect_alarms` | No | `true` | Poll `/api/2.0/alarms`. |
    | **Collect Events** | `collect_events` | No | `false` | Poll `/api/2.0/events`. |
    | **Event Filter** | `event_filter` | No | — | Optional events-only filter written as a URL query string, e.g. `event_category=Application`. Ignored when only alarms are collected. The connector sets `page`, `size`, `sort` and `timestamp_occured_gte` itself and removes them from the filter if present. |

    !!! info "Enable at least one source"
        At least one of **Collect Alarms** or **Collect Events** must be
        enabled — the connector rejects a configuration where both are off.

5. Toggle **Enabled** to on
6. Click **Save**

!!! tip "Why a subdomain, not a full URL"
    The connector accepts only a DNS label and always composes the request
    host as `<subdomain>.alienvault.cloud`. This prevents a mistyped or
    hostile value from redirecting traffic to another host (SSRF protection),
    so a full URL, scheme, port, or path is rejected by design.

### What Gets Collected

| Source | Toggle | WitFoo Classification |
|--------|--------|-----------------------|
| Alarms | `collect_alarms` | Correlated SIEM detections (see below) |
| Events | `collect_events` | Asset inventory for the observing host |

**Alarms** are USM Anywhere's own correlated detections. WitFoo classifies
each alarm by its `rule_intent` (kill-chain stage):

| USM `rule_intent` | WitFoo message type |
|-------------------|---------------------|
| Reconnaissance & Probing | `network_scan` |
| Exploitation & Installation | `exploit_attempt` |
| System Compromise / Delivery & Attack | `malicious_behavior` |
| Any other / unset intent (e.g. Environmental Awareness) | `siem_event` |

**Events** classify as `asset_inventory` — the source host the event was
observed on becomes the inventoried asset. Both sources are tagged with the
`usm_anywhere` stream; a recognized USM record is never dropped as `unknown`.

!!! info "Alarms feed work units"
    Because USM Anywhere alarms are the SIEM's own detections, WitFoo's
    default lead rules treat every collected alarm as a lead — including
    alarms that fall to the `siem_event` floor — and leads feed the incident
    correlation engine that builds work units. Events (asset inventory) match
    no default lead rule. If alarm volume is high, tune the alarm scope in USM
    Anywhere or collect events only.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within a couple of minutes of saving
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "usm-anywhere"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and filter for the `usm_anywhere` stream

## Behavior

- **Polling** — Each poll reads every enabled source (alarms, events). The
  next poll starts about 60 seconds after the previous one finishes. The
  interval is built in; there is no polling-interval setting for this
  connector
- **Checkpoint resume** — At the end of a poll the connector saves its
  position for each source: an inclusive `timestamp_occured` watermark plus
  the UUIDs of the records already delivered at that timestamp. The next
  poll re-fetches from the watermark and skips those UUIDs, so a record that
  was already delivered is not delivered again. The position is saved when a
  poll ends, so a restart in the middle of a poll can deliver that poll's
  records again
- **Rate limiting and errors** — On HTTP 429 the connector waits for the
  server's `Retry-After` time (kept between 1 second and 15 minutes) before
  its next poll. With no usable `Retry-After`, and after other temporary
  errors, it waits a random time that grows with each consecutive failure,
  up to 10 minutes
- **Per-poll page cap** — A poll reads at most 500 pages (100 records each)
  for each enabled source. If a source is further behind than that, the
  connector logs a warning and the next poll resumes from the checkpoint;
  the cap delays records, it does not drop them
- **Redirect safety** — All HTTP redirects are refused; the request host is
  always `<subdomain>.alienvault.cloud`

## One instance per Conductor

The Conductor UI lets you add more than one instance of this connector, but
every instance saves its position (its checkpoint) in the same file on the
Conductor and loads that file when it starts. With two or more instances, an
instance can start from another tenant's position, so records can be skipped
or fetched again. Add one USM Anywhere instance per Conductor; an MSSP with
several tenants should use a separate Conductor for each tenant.

## Coexistence With LevelBlue Agents and Beats

This connector **pulls** from the USM Anywhere API. It does not change how any
data reaches USM Anywhere:

- **LevelBlue managed agents keep shipping to USM Anywhere unchanged.** The
  connector reads the resulting alarms and events from the API — there is no
  need to re-point the managed collection agents
- **Beats / Windows Event Forwarding are unaffected.** If you already forward
  logs to Conductor with OSS Filebeat / Winlogbeat or Windows Event
  Forwarding, that continues to work alongside this connector

!!! note "Distinct from the USM Anywhere exporter"
    This ingest connector (`usm-anywhere-events`) is separate from the WitFoo
    outbound **exporter** integrations (`usm-anywhere` / `alien-vault`), which
    send WitFoo artifacts *to* an external system. Enabling this connector does
    not enable any exporter.

## Troubleshooting

### Authentication Failed (401 or 403)

- Verify the **Client ID** and **Secret** were copied completely
- Confirm the API client is still **enabled** in USM Anywhere (**Profile
  Settings** → **API Clients**) and has not been deleted
- If in doubt, create a new API client in USM Anywhere and update the
  Conductor settings with its credentials

### Subdomain Rejected

- The **Subdomain** must be a bare DNS label (lowercase letters, digits,
  hyphens) — do not include `https://`, a port, a path, or `.alienvault.cloud`
- Example: for `https://acme-soc.alienvault.cloud/`, enter `acme-soc`

### Checkpoint Not Advancing

- Confirm records exist in USM Anywhere for the polled source in the current
  window
- Check Signal Client logs for a page-cap warning — a large backlog drains
  over several polls by design
- Verify the tenant clock and record timestamps are sane (a zero or missing
  `timestamp_occured` record is skipped)

### Rate Limited (429)

- The connector already waits for the server's `Retry-After` value before its
  next poll
- Reduce the load: turn off **Collect Events** if you only need alarms, or
  narrow events with the **Event Filter**
- If 429 responses continue, ask LevelBlue about the API rate limits for your
  tenant

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm at least one of **Collect Alarms** / **Collect Events** is on
- Verify the tenant subdomain is correct and reachable on port 443
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

!!! note "Credentials in logs"
    The connector's logger never writes the Client ID, Secret, or bearer
    token. If you enable the shared low-level request-tracing mode (`DEBUG=1`)
    for deep diagnostics, request headers may be written to disk — use it only
    in a controlled environment and clear the output afterward.

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
