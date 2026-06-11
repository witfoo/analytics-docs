---
tags:
  - auditor
  - cloud
---

# Google Cloud Platform

Audits **Google Cloud Platform** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Cloud Platform |
| **Connector Type** | `gcp` |
| **Auth Method** | Service account JSON key (viewer) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [GCP IAM documentation](https://cloud.google.com/iam/docs) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Google Cloud Platform and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Google Cloud Platform (step 1)
- [ ] Network: Analytics can reach the Google Cloud Platform API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Google Cloud Platform

1. Open the **Google Cloud Console** and go to **IAM & Admin → Service Accounts**.
2. Create a service account with read-only **Viewer** (or Security Reviewer) roles.
3. Create a **JSON key** for the service account and download it.
4. Note the **Project ID** to audit.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Google Cloud Platform**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Service Account JSON** | Yes | Full JSON key file contents from step 1 |
    | **Project ID** | Yes | GCP project to audit |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Google Cloud Platform findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — confirm the JSON key is pasted in full and not expired.
- **Permission denied** — ensure the service account has Viewer/Security Reviewer roles on the project.
- **Wrong project** — verify the Project ID matches the project you intend to audit.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
