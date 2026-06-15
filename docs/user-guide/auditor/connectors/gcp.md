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
2. Create a service account with read-only roles (see [Required APIs and permissions](#required-apis-and-permissions) below).
3. Create a **JSON key** for the service account and download it.
4. Note the **Project ID** to audit.

### Required APIs and permissions

*Test Connection* only needs `resourcemanager.projects.get`. A full **audit run** calls five
Google APIs — **each must be enabled on the audited project** and the service account needs the
matching read permission. A disabled API is the usual cause of a *"Corporate login required"*
error (the request is rejected before authentication is evaluated).

Enable all required APIs in one command:

```bash
gcloud services enable \
  cloudresourcemanager.googleapis.com iam.googleapis.com \
  storage.googleapis.com compute.googleapis.com sqladmin.googleapis.com \
  --project <PROJECT_ID>
```

| Audit check | Google API | Service-account permission (role) |
| --- | --- | --- |
| Project access (Test Connection) | `cloudresourcemanager.googleapis.com` | `resourcemanager.projects.get` (**roles/browser** or **roles/viewer**) |
| Org-policy domain restriction | `cloudresourcemanager` / `orgpolicy.googleapis.com` | `resourcemanager.projects.getIamPolicy`, `orgpolicy.policy.get` (**roles/iam.securityReviewer**) |
| Audit logging config | `cloudresourcemanager.googleapis.com` | `resourcemanager.projects.getIamPolicy` (**roles/iam.securityReviewer**) |
| Service-account key rotation | `iam.googleapis.com` | `iam.serviceAccounts.list`, `iam.serviceAccountKeys.list` (**roles/iam.securityReviewer**) |
| Public buckets | `storage.googleapis.com` | `storage.buckets.list`, `storage.buckets.getIamPolicy` (**roles/iam.securityReviewer** + a list role) |
| Default network | `compute.googleapis.com` | `compute.networks.list` (**roles/compute.viewer**) |
| Cloud SQL SSL | `sqladmin.googleapis.com` | `cloudsql.instances.list`, `cloudsql.instances.get` (**roles/cloudsql.viewer**) |

Simplest grant (covers all checks):

```bash
for ROLE in roles/iam.securityReviewer roles/cloudsql.viewer roles/compute.viewer roles/storage.objectViewer; do
  gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="serviceAccount:<SA_EMAIL>" --role="$ROLE"
done
```

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
- **Permission denied** — ensure the service account has the roles in [Required APIs and permissions](#required-apis-and-permissions).
- **Wrong project** — verify the Project ID matches the project you intend to audit.
- **HTTP 404 on `cloudresourcemanager.googleapis.com/v1/projects/<id>`** — confirm the Project ID is correct and the service account has `resourcemanager.projects.get` (Browser/Viewer) on it. (The connector uses the per-service host; the legacy `www.googleapis.com` host returns 404 for every project.)
- **"Corporate login required"** — a required **Google API is not enabled** on the project. Run the `gcloud services enable …` command above. If your org uses Context-Aware Access / VPC Service Controls, also confirm the service account is not excluded by an access-level policy.
- **"Cloud SQL requires SSL"** — if shown as a **finding** (not an error), the check is working as designed: the instance *requires* SSL = **compliant**. If shown as a hard **error** during the run, enable `sqladmin.googleapis.com` and grant **roles/cloudsql.viewer**.

---

*See also: [Auditor](../index.md) · [Audit Report](../../reporter/audit-report.md)*
