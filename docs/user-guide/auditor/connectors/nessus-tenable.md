---
tags:
  - auditor
  - vulnerability
---

# Tenable.io / Nessus

Audits **Tenable.io / Nessus** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Vulnerability Scanner |
| **Connector Type** | `nessus` |
| **Auth Method** | API keys (access + secret) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [Tenable API documentation](https://docs.tenable.com/) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Tenable.io / Nessus and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Tenable.io / Nessus (step 1)
- [ ] Network: Analytics can reach the Tenable.io / Nessus API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Tenable.io / Nessus

1. Log in to **Tenable.io** (or your Nessus instance).
2. Open **My Account → API Keys** and generate keys.
3. Record the **Access Key** and **Secret Key**, and your **API URL** if not the default cloud endpoint.

!!! note "Not the same as the Conductor integration"
    The Conductor **Tenable / Nessus** integration ingests vulnerability artifacts into the
    signal pipeline and is configured in the Conductor UI. It is a separate,
    independent configuration from this Auditor connector. See
    [Tenable / Nessus integration](../../../conductor/integrations/tenable.md).

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Tenable.io / Nessus**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Access Key** | Yes | Tenable API access key |
    | **Secret Key** | Yes | Tenable API secret key |
    | **API URL** | No | Override for self-hosted Nessus, e.g. `https://<host>:8834` |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Tenable.io / Nessus findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — regenerate the API keys and confirm both are entered.
- **Forbidden** — ensure the account has permission to read scan results.
- **Self-hosted Nessus** — set the API URL to your Nessus host and port (default `8834`).

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
