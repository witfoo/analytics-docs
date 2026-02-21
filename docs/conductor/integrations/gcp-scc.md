---
tags:
  - integration
  - cloud
---

# Google Cloud Security Command Center

Collects security findings from Google Cloud Security Command Center (SCC),
Google's centralized security and risk management platform for GCP resources.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.gcp-scc` |
| **Auth Method** | Service Account JSON Key |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [SCC API Documentation](https://cloud.google.com/security-command-center/docs/reference/rest) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Google Cloud organization with Security Command Center enabled
    (Standard or Premium tier). Organization-level access required.

- [ ] Active Google Cloud organization (not just a project)
- [ ] SCC Standard or Premium tier enabled
- [ ] IAM access to create service accounts
- [ ] Network: Conductor can reach `securitycenter.googleapis.com` on port 443

## Step 1: Create API Credentials

1. Sign in to the **Google Cloud Console** at `https://console.cloud.google.com/`
2. Select the project where you want to create the service account
3. Navigate to **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
5. Name the account (e.g., `witfoo-scc-reader`)
6. Click **Create and Continue**
7. Grant the role **Security Center Findings Viewer**
   (`roles/securitycenter.findingsViewer`)
8. Click **Done**
9. Select the new service account → **Keys** tab → **Add Key** →
   **Create New Key** → **JSON**
10. Download the JSON key file

!!! warning "Organization-Level Access"
    SCC operates at the **organization** level, not the project level.
    The service account must have the Findings Viewer role granted at the
    organization level in IAM.

### Grant Organization-Level Access

1. Navigate to **IAM & Admin** → **IAM** at the organization level
2. Click **Grant Access**
3. Enter the service account email
4. Assign role: **Security Center Findings Viewer**
5. Click **Save**

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Google Cloud SCC**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Organization ID** | `<your-org-id>` | GCP organization numeric ID |
    | **API Key** | *(paste full JSON key)* | Service account JSON key content |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

!!! tip "Finding Your Organization ID"
    Navigate to **Cloud Identity** → **Account** → **Account Settings** or
    run: `gcloud organizations list`

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "gcp-scc"
    ```

    Look for successful poll messages:
    ```
    [INFO] gcp-scc: fetched <N> findings
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Verify Credentials Locally

```bash
# Test the service account key (optional, from any machine with gcloud)
gcloud auth activate-service-account --key-file=<key-file>.json
gcloud scc findings list <organization-id> --source="-" --limit=5
```

## Troubleshooting

### Authentication Failed (401)

- Verify the JSON key content was pasted correctly (including all fields)
- Ensure the service account has not been deleted or disabled
- Regenerate the key if needed

### Forbidden (403)

- The service account likely lacks organization-level IAM binding
- Grant **Security Center Findings Viewer** at the **organization** level,
  not the project level
- Verify: `gcloud organizations get-iam-policy <org-id>`

### SCC Tier Limitations

- **Standard tier** provides limited finding types (Security Health Analytics)
- **Premium tier** adds Event Threat Detection, Container Threat Detection, etc.
- Check your SCC tier under **Security** → **Security Command Center** →
  **Settings**

### No Data Appearing

- Confirm SCC is enabled at the organization level
- Enable security sources (Security Health Analytics, Event Threat Detection)
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://securitycenter.googleapis.com`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
