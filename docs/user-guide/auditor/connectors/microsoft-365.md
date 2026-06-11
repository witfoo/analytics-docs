---
tags:
  - auditor
  - cloud
---

# Microsoft 365

Audits **Microsoft 365** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Cloud Platform |
| **Connector Type** | `microsoft_365` |
| **Auth Method** | Entra app registration (Graph application permissions) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [Microsoft Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-reference) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Microsoft 365 and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Microsoft 365 (step 1)
- [ ] Network: Analytics can reach the Microsoft 365 API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Microsoft 365

1. In the **Azure Portal**, open **Microsoft Entra ID → App registrations** and register an application for the tenant.
2. Add read-only **Microsoft Graph application permissions** and grant admin consent.
3. Create a **client secret**.
4. Record the **Tenant ID**, **Client ID**, and **Client Secret**.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Microsoft 365**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Tenant ID** | Yes | Entra tenant (directory) id |
    | **Client ID** | Yes | Application (client) id |
    | **Client Secret** | Yes | Client secret value from step 1 |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Microsoft 365 findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — verify the client secret and tenant/client ids.
- **Insufficient privileges** — ensure read-only Graph application permissions are granted with admin consent.
- **Secret expired** — rotate the Entra client secret and update the connector.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
