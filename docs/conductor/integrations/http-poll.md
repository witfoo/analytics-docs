---
tags:
  - integration
  - network
---

# HTTP/HTTPS Monitor

Probes the web endpoints you list and records response time, status code and
TLS certificate expiry. A confirmed change from up to down raises a Service
Disruption.

| | |
|---|---|
| **Category** | Infrastructure |
| **Connector Name** | `signal-client.http-poll` |
| **Auth Method** | None (no credentials are sent) |
| **Polling Interval** | Per target: 60 s by default, 30 s minimum |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110) |

## Prerequisites

!!! note "Vendor Requirements"
    HTTP or HTTPS endpoints that answer without sign-in, such as a health or
    status URL.

- [ ] An `http` or `https` URL for each endpoint to monitor
- [ ] Network: Conductor can reach each endpoint on its port

## Step 1: Create API Credentials

The monitor sends no credentials, so there is nothing to create. Choose an
endpoint that answers without sign-in, such as a health-check URL, and note
the status codes that mean "up" for it.

!!! warning "No credentials in URLs"
    A URL that carries a user name or password (`user:pass@`) is refused.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **HTTP/HTTPS Monitor**
3. Enter a unique name for this instance
4. For each endpoint, fill in a target. Click **Add Target** to add another:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **URL** | `https://app.example.com/health` | Full `http` or `https` URL, with no credentials |
    | **Label** | `Billing API` | Optional friendly name. Defaults to the URL's host |
    | **Method** | `GET` | `GET` or `HEAD` |
    | **Poll Interval (seconds)** | `60` | Minimum 30. A lower value is raised to 30 |
    | **Timeout (seconds)** | `10` | Must be shorter than the interval |
    | **Expected Status** | `200-399` | Codes or ranges counted as up, for example `200-399` or `200,301,302` |

5. Toggle **Enabled** to on
6. Click **Save**

An instance holds up to 512 targets.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "http"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts of stream `http_monitor`

### What It Records

Every check produces one artifact with the action `http_up`, `http_down` or
`cert_expiring`. It carries the response time, the HTTP status, the label and,
for HTTPS, the days until the certificate expires.

When a target fails 2 checks in a row after being up, the monitor emits one
Service Disruption artifact. A single failed check never does. While the
target stays down, it repeats at most once every 60 minutes. On a Docker
Compose stack you can change these with `HTTP_POLL_CONFIRM_CHECKS` and
`HTTP_POLL_COOLDOWN_MINUTES` on the signal client.

!!! info "Redirects are recorded, not followed"
    A `30x` answer is the recorded status. The monitor never follows the
    redirect, so list the final URL if that is what you want to watch.

## Troubleshooting

### Target Always Down

- Check that the Conductor can reach the URL, and resolve its host name
- Check **Expected Status**: a status outside it, such as a `401` with the
  default `200-399`, counts as down
- Raise **Timeout (seconds)** for a slow endpoint, keeping it below the
  interval

### URL Refused

- Use an `http` or `https` URL with no `user:pass@`
- Loopback and link-local addresses, including the cloud metadata address
  `169.254.169.254`, are refused when the connection is made. Private network
  addresses are allowed

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
