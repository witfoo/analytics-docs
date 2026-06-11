---
tags:
  - auditor
  - cloud
---

# Oracle Cloud Infrastructure

Audits **Oracle Cloud Infrastructure** configuration against CIS Benchmarks and maps findings to
your enabled compliance frameworks.

| | |
|---|---|
| **Category** | Cloud Platform |
| **Connector Type** | `oci` |
| **Auth Method** | API signing key |
| **Default Schedule** | `0 */6 * * *` (every 6 hours) |
| **Vendor Docs** | [OCI API signing keys](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) |

## Prerequisites

!!! note "Requirements"
    Read-only audit access to Oracle Cloud Infrastructure and an [`auditor:write`](../index.md#permissions)
    permission to add the connector in Analytics.

- [ ] Read-only audit credentials in Oracle Cloud Infrastructure (step 1)
- [ ] Network: Analytics can reach the Oracle Cloud Infrastructure API endpoint on port 443
- [ ] `auditor:write` to add the connector; `auditor:execute` to run it on demand

## Step 1: Create credentials in Oracle Cloud Infrastructure

1. In the **OCI Console**, open the auditing IAM **user**'s profile.
2. Under **API keys**, add an **API signing key** (RSA) and download the private key (PEM).
3. Record the **Tenancy OCID**, **User OCID**, key **Fingerprint**, the **private key** (PEM), and the **region**.
4. Optionally note a **Compartment OCID** to scope the audit.

## Step 2: Configure in Analytics

1. Open **Reporter → Auditor** and select the **Connectors** tab.
2. Click **Add Connector** and choose **Oracle Cloud Infrastructure**.
3. Fill in the connector form:

    | Field | Required | Description |
    | --- | --- | --- |
    | **Tenancy OCID** | Yes | Tenancy OCID |
    | **User OCID** | Yes | IAM user OCID |
    | **Fingerprint** | Yes | API key fingerprint |
    | **Private Key** | Yes | API signing key, PEM format |
    | **Region** | Yes | OCI region, e.g. `us-ashburn-1` |
    | **Compartment OCID** | No | Limit the audit to a compartment |

4. Set the **Schedule** (default `0 */6 * * *` — every 6 hours).
5. Toggle **Enabled** on and click **Save**.

## Step 3: Validate

1. Click **Test Connection** on the connector row to confirm the credentials.
2. Click **Run Now** (requires `auditor:execute`) to trigger an immediate audit.
3. After the run completes, open the **Findings** tab — Oracle Cloud Infrastructure findings appear
   with severity, evidence, framework mappings, and remediation guidance.

## Troubleshooting

- **Authentication failed** — verify the tenancy/user OCIDs, fingerprint, and that the PEM private key matches the uploaded key.
- **Not authorized** — ensure the user has read (inspect) policies on the audited resources.
- **Wrong region** — confirm the region matches your tenancy's home or subscribed region.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
