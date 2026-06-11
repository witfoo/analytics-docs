---
tags:
  - auditor
  - cloud
---

# Amazon Web Services

Audits **Amazon Web Services** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Cloud Platform |
| **Connector Type** | `aws` |
| **Auth Method** | IAM access key (read-only) |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Amazon Web Services and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Amazon Web Services (step 1)
- [ ] Network: Analytics can reach the Amazon Web Services API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Amazon Web Services

1. Sign in to the **AWS Console** and open **IAM**.
2. Create (or choose) an IAM user for auditing and attach the AWS-managed **`SecurityAudit`** policy (read-only).
3. Under the user's **Security credentials**, create an **access key** pair.
4. Record the **Access Key ID** and **Secret Access Key**, and note the **region** to audit.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Amazon Web Services**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Access Key ID** | Yes | IAM access key id from step 1 |
    | **Secret Access Key** | Yes | IAM secret access key from step 1 |
    | **Region** | Yes | AWS region to audit, e.g. `us-east-1` |
    | **Session Token** | No | Only for temporary STS credentials |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Amazon Web Services findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — verify the access key pair and that the key is active.
- **Access denied** — confirm the `SecurityAudit` managed policy (or equivalent read-only permissions) is attached.
- **Wrong region** — the connector audits the configured region; add a connector per region if needed.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
