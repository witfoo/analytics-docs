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
| **Polling Interval** | 5 min (checkpoint-resumed) |
| **Multi-Instance** | Yes (one instance per USM Anywhere tenant) |
| **API Base** | `https://<subdomain>.alienvault.cloud/api/2.0` |
| **Vendor Docs** | USM Anywhere API 2.0 (per-tenant Swagger UI at `https://<subdomain>.alienvault.cloud/api/2.0/`) |

!!! note "Availability"
    This connector was introduced in WitFoo 1.1.0. Alarm and event field
    extraction is built against the LevelBlue USM Anywhere API 2.0 reference
    and is being validated against production tenants. If records from your
    tenant classify unexpectedly, contact WitFoo support with a sample so the
    mapping can be confirmed.

## Prerequisites

!!! note "Vendor Requirements"
    An active USM Anywhere subscription and permission to create an API 2.0
    client-credentials application in your tenant.

- [ ] Active LevelBlue USM Anywhere subscription
- [ ] A USM Anywhere **API 2.0 client-credentials app** (Client ID + Secret)
- [ ] Your tenant **subdomain** — the bare DNS label from your USM Anywhere
  URL `https://<subdomain>.alienvault.cloud`
- [ ] Network: Conductor can reach `<subdomain>.alienvault.cloud` on port 443

## Step 1: Create API Credentials in USM Anywhere

1. Log in to your USM Anywhere tenant at
   `https://<subdomain>.alienvault.cloud/`
2. Open the **API access** settings and create a new **API 2.0 client**
   (the exact menu label varies by USM Anywhere version — see your vendor
   documentation)
3. Copy the generated **Client ID** and **Client Secret**

    !!! warning "Store the secret now"
        The client secret is shown only once. Record it before leaving the
        page — it cannot be retrieved later and must be regenerated if lost.

4. Note your **subdomain** — the label before `.alienvault.cloud` in your
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
    | **Secret** | `secret` | Yes | — | OAuth2 client secret. Write-only in the form. |
    | **Collect Alarms** | `collect_alarms` | No | `true` | Poll `/api/2.0/alarms`. |
    | **Collect Events** | `collect_events` | No | `false` | Poll `/api/2.0/events`. |
    | **Event Filter** | `event_filter` | No | — | Optional events-only query filter, e.g. `event_category=Application`. Ignored when only alarms are collected. |

    !!! info "Enable at least one source"
        At least one of **Collect Alarms** or **Collect Events** must be
        enabled — the connector rejects a configuration where both are off.

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

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

!!! info "Alarms create work units"
    Because USM Anywhere alarms are the SIEM's own detections, every collected
    alarm — including those that fall to the `siem_event` floor — generates a
    WitFoo work unit. Events (asset inventory) do not create work units. If
    alarm volume is high, tune the alarm scope in USM Anywhere or collect
    events only.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "usm-anywhere"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and filter for the `usm_anywhere` stream

## Behavior

- **Polling** — Each enabled source (alarms, events) is polled on the
  configured interval (default 5 minutes)
- **Checkpoint resume** — The connector tracks the last-seen record per source
  using an inclusive `timestamp_occured` watermark plus the boundary record
  UUID. On restart it re-fetches from the watermark and skips the already-seen
  UUID, so no records are gapped or duplicated across a restart
- **Rate limiting** — On HTTP 429 the connector honors the server's
  `Retry-After` header and resumes on the next cycle
- **Per-cycle page cap** — A single poll cycle reads at most 500 pages. If a
  source is further behind than one cycle can drain, the connector logs a
  warning and resumes from the checkpoint on the next cycle — no records are
  lost
- **Redirect safety** — All HTTP redirects are refused; the request host is
  always `<subdomain>.alienvault.cloud`

## Coexistence With LevelBlue Agents and Beats

This connector **pulls** from the USM Anywhere API. It does not change how any
data reaches USM Anywhere:

- **LevelBlue managed agents keep shipping to USM Anywhere unchanged.** The
  connector reads the resulting alarms and events from the API — there is no
  need to re-point or dual-home the managed collection agents (and doing so is
  not supported)
- **Beats / Windows Event Forwarding can coexist.** If you already forward
  logs to Conductor with OSS Filebeat / Winlogbeat or Windows Event
  Forwarding, that continues to work alongside this connector. (Running a
  second *osquery* agent pointed at Conductor is not supported.)

!!! note "Distinct from the USM Anywhere exporter"
    This ingest connector (`usm-anywhere-events`) is separate from the WitFoo
    outbound **exporter** integrations (`usm-anywhere` / `alien-vault`), which
    send WitFoo artifacts *to* an external system. Enabling this connector does
    not enable any exporter.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Client ID** and **Secret** were copied completely
- Confirm the API 2.0 client is still active in USM Anywhere and has not been
  revoked or expired
- Regenerate the client secret in USM Anywhere and update the Conductor
  settings if in doubt

### Subdomain Rejected

- The **Subdomain** must be a bare DNS label (letters, digits, hyphens) — do
  not include `https://`, a port, a path, or `.alienvault.cloud`
- Example: for `https://acme-soc.alienvault.cloud/`, enter `acme-soc`

### Checkpoint Not Advancing

- Confirm records exist in USM Anywhere for the polled source in the current
  window
- Check Signal Client logs for a page-cap warning — a large backlog drains
  over several cycles by design
- Verify the tenant clock and record timestamps are sane (a zero or missing
  `timestamp_occured` record is skipped)

### Rate Limited (429)

- Increase the **Polling Interval**
- The connector already honors the server `Retry-After` value automatically

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
