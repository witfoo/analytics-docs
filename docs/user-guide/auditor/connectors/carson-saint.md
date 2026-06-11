---
tags:
  - auditor
  - vulnerability
---

# Carson & SAINT

Audits **Carson & SAINT** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Vulnerability Scanner |
| **Connector Type** | `carson_saint` |
| **Auth Method** | REST API token |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [SAINT Security Suite documentation](https://www.carson-saint.com/) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Carson & SAINT and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Carson & SAINT (step 1)
- [ ] Network: Analytics can reach the Carson & SAINT API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Carson & SAINT

1. Log in to the **SAINT Security Suite**.
2. Generate a **REST API token** for an account with read access to scan results.
3. Record the **API token** and your **API URL** if not the default.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Carson & SAINT**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **API Token** | Yes | SAINT REST API token |
    | **API URL** | No | SAINT Security Suite API endpoint |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Carson & SAINT findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — regenerate the API token and confirm it is entered in full.
- **Forbidden** — ensure the token's account can read scan results.
- **Connection errors** — verify the API URL and network reachability to the Security Suite.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
