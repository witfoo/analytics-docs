---
tags:
  - auditor
  - vulnerability
---

# Qualys

Audits **Qualys** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Vulnerability Scanner |
| **Connector Type** | `qualys` |
| **Auth Method** | Basic Auth (API user) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [Qualys API documentation](https://qualysguard.qualys.com/qwebhelp/fo_portal/api_doc/) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Qualys and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Qualys (step 1)
- [ ] Network: Analytics can reach the Qualys API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Qualys

1. Log in to the **Qualys Console** and open **Users** (under Administration).
2. Add (or choose) a user and assign the **API** role.
3. Record the **username** and **password**, and your platform **API URL** (region-specific).

!!! note "Not the same as the Conductor integration"
    The Conductor **Qualys** integration ingests vulnerability artifacts into the
    signal pipeline and is configured in the Conductor UI. It is a separate,
    independent configuration from this Auditor connector. See
    [Qualys integration](../../../conductor/integrations/qualys.md).

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Qualys**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Username** | Yes | Qualys API user |
    | **Password** | Yes | Qualys API user password |
    | **API URL** | No | Platform API URL, e.g. `https://qualysapi.qualys.com` (region-specific) |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Qualys findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed (401)** — verify the username/password and that the user has the API role.
- **Forbidden (403)** — ensure the user has the Vulnerability Management module.
- **Wrong platform URL** — Qualys API URLs are region-specific; verify the correct endpoint.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
