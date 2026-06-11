---
tags:
  - auditor
  - cloud
---

# Microsoft Azure

Audits **Microsoft Azure** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Cloud Platform |
| **Connector Type** | `azure` |
| **Auth Method** | Entra app registration (client secret) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [Microsoft Entra app registration](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Microsoft Azure and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Microsoft Azure (step 1)
- [ ] Network: Analytics can reach the Microsoft Azure API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Microsoft Azure

1. In the **Azure Portal**, open **Microsoft Entra ID → App registrations** and register a new application.
2. Create a **client secret** under **Certificates & secrets**.
3. Assign the application the **Reader** role on the target subscription (**Subscriptions → Access control (IAM)**).
4. Record the **Tenant ID**, **Client ID**, **Client Secret**, and **Subscription ID**.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Microsoft Azure**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Tenant ID** | Yes | Entra tenant (directory) id |
    | **Client ID** | Yes | Application (client) id |
    | **Client Secret** | Yes | Client secret value from step 1 |
    | **Subscription ID** | Yes | Azure subscription to audit |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Microsoft Azure findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — verify the client secret value (not its id) and the tenant/client ids.
- **Authorization failed** — confirm the app has the **Reader** role on the subscription.
- **Secret expired** — Entra client secrets expire; rotate and update the connector.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
