---
tags:
  - integration
  - network
---

# Cloudflare

Collects Cloudflare account audit logs and per-zone WAF and firewall events
with a scoped API token.

| | |
|---|---|
| **Category** | Network Security |
| **Connector Name** | `signal-client.cloudflare-security-events` |
| **Auth Method** | API Token (scoped) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [Create API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) |

## Prerequisites

!!! note "Vendor Requirements"
    A Cloudflare account, and permission to create API tokens. The scoped
    token works on every Cloudflare plan for audit and firewall events.

- [ ] Cloudflare account with the zones you want to collect from
- [ ] Permission to create a custom API token
- [ ] Your 32-character **Account ID** and the **Zone IDs** of the zones to collect
- [ ] Network: Conductor can reach `api.cloudflare.com` on port 443

## Step 1: Create API Credentials

Create a custom API token that grants only what each data family needs.

1. In the Cloudflare dashboard, open **My Profile** → **API Tokens**
2. Click **Create Token**, then choose a **Custom token**
3. Add the permissions for the families you will collect:

    | Family | Permission |
    |--------|------------|
    | Audit logs | **Account** → **Account Settings** → **Read** |
    | Firewall events | **Account** → **Account Analytics** → **Read**, with the zones you want under **Zone Resources** |

4. Create the token and copy it. It is shown once.
5. Copy the **Account ID** and each **Zone ID** from the dashboard

!!! warning "Use a scoped token"
    The legacy Global API Key is not supported, because it cannot be scoped
    down. If you collect audit logs only, the Account Analytics permission is
    not needed.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Cloudflare**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **API Token** | *(paste token)* | The scoped API token from step 1 |
    | **Account ID** | 32 hex characters | Account ID from the Cloudflare dashboard |
    | **Zone IDs** | `<zone-id-1>,<zone-id-2>` | Comma-separated 32-character Zone IDs, at most 40. Required when **Collect Firewall Events** is on |
    | **Collect Audit Logs** | On | Poll account audit logs (Audit Logs v2). On by default |
    | **Collect Firewall Events** | On | Poll WAF and firewall events for each zone. On by default |

5. Toggle **Enabled** to on
6. Click **Save**

!!! tip "More than 40 zones"
    Each zone costs at least one query per cycle, so one instance takes at
    most 40 zones. Split a larger estate across more instances (up to 5).

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "cloudflare"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Data Sources

| Source | Data Type | Default Interval |
|--------|-----------|-----------------|
| Audit Logs v2 | Account audit events | 5 min |
| Firewall events (`firewallEventsAdaptive`) | WAF and firewall events, per zone | 5 min |

!!! note "Zero Trust Gateway events are not collected"
    Every Gateway dataset Cloudflare documents for its GraphQL Analytics API
    is an aggregate, so the connector does not collect Zero Trust Gateway
    events.

!!! note "Lookback after an outage"
    A zone with no saved position starts at the last hour. After an outage
    longer than 24 hours, the connector asks for the last 24 hours only, so
    the older part of the gap is not collected. The skipped span is logged
    as a warning that names both ends.

## Troubleshooting

### Authentication Failed (401 or 403)

Cloudflare answers a wrong Account ID, a zone the token cannot read, a token
without the permission a family needs, and a revoked token with the same two
statuses. The instance shows Failure with the health code `auth_failed`, and
is retried after 15 minutes.

- Check that the Account ID and Zone IDs belong to the token's account
- Check that the token carries the permission for each enabled family
- Check that the token is a scoped API token, not a Global API Key

### Rate Limited (429)

- A 429 ends the polling cycle, and the connector waits for the time
  Cloudflare gives in `Retry-After` before the next poll
- Other dashboards, tokens or tools that use the same Cloudflare user share
  its API budget. Reduce their use, or split zones across instances

### One Bad Zone Stops the Instance

- A Zone ID that is not found, or that the token cannot read, fails the whole
  instance for 15 minutes at a time, including the audit logs and the other
  zones. Correct or remove the zone

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm **Collect Firewall Events** has at least one Zone ID
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
