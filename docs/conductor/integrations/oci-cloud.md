---
tags:
  - integration
  - cloud
---

# Oracle Cloud Infrastructure (OCI)

Collects security and audit data from Oracle Cloud Infrastructure, including
audit events, logging service data, and Cloud Guard problem detections.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.oci-cloud` |
| **Auth Method** | API Key (RSA Signing) |
| **Polling Interval** | 5 min (audit), 30 min (Cloud Guard) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [OCI API Documentation](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Oracle Cloud Infrastructure tenancy. IAM permissions to create
    users and API keys.

- [ ] Active OCI tenancy
- [ ] IAM access to create users and generate API keys
- [ ] Network: Conductor can reach OCI API endpoints on port 443

## Step 1: Create API Credentials

### Generate an API Signing Key

1. Sign in to the **OCI Console** at `https://cloud.oracle.com/`
2. Navigate to **Identity** → **Users** → select your user (or create a
   dedicated service user)
3. Under **Resources**, click **API Keys**
4. Click **Add API Key**
5. Select **Generate API Key Pair**
6. Click **Download Private Key** and save the PEM file securely
7. Click **Add**
8. Copy the **fingerprint** displayed

### Collect Required OCIDs

| Value | Where to Find |
|-------|---------------|
| **Tenancy OCID** | **Governance** → **Tenancy Details** → OCID |
| **User OCID** | **Identity** → **Users** → select user → OCID |
| **Compartment OCID** | **Identity** → **Compartments** → select compartment → OCID |

!!! tip "Broadest Collection"
    Use the **Tenancy root compartment OCID** (same as Tenancy OCID) to
    collect from all compartments. Use a specific compartment OCID to limit
    scope.

### Grant Required Policies

Create an IAM policy for the API user:

```
Allow user <username> to read audit-events in tenancy
Allow user <username> to read log-content in tenancy
Allow user <username> to read cloud-guard-problems in tenancy
```

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Oracle Cloud (OCI)**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Tenancy OCID** | `ocid1.tenancy.oc1..aaa...` | From Tenancy Details |
    | **User OCID** | `ocid1.user.oc1..aaa...` | API user OCID |
    | **Fingerprint** | `aa:bb:cc:...` | API key fingerprint from step 1 |
    | **Private Key** | *(paste PEM content)* | RSA private key content |
    | **Region** | `us-ashburn-1` | OCI region identifier |
    | **Compartment OCID** | `ocid1.compartment.oc1..aaa...` | Scope compartment |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

!!! info "OCI Region Identifiers"
    Common regions: `us-ashburn-1`, `us-phoenix-1`, `eu-frankfurt-1`,
    `eu-amsterdam-1`, `uk-london-1`, `ap-tokyo-1`, `ap-sydney-1`.
    Full list: [OCI Regions](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm)

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "oci"
    ```

    Look for successful poll messages:
    ```
    [INFO] oci-cloud: fetched <N> audit events
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

### Data Sources

OCI integration collects from three sources:

| Source | Data Type | Default Interval |
|--------|-----------|-----------------|
| Audit Events | IAM, resource, and network activity | 5 min |
| Logging Search | Custom log queries | 5 min |
| Cloud Guard Problems | Security findings and recommendations | 30 min |

!!! note "Cloud Guard Availability"
    Cloud Guard may not be enabled in all tenancies. To enable: navigate to
    **Security** → **Cloud Guard** → **Enable Cloud Guard** in the OCI Console.

## Troubleshooting

### Authentication Failed (401)

- Verify the **Private Key** PEM content is pasted correctly (including
  `-----BEGIN RSA PRIVATE KEY-----` header/footer)
- Ensure the **Fingerprint** matches the API key
- Check that the **User OCID** and **Tenancy OCID** are correct

### Forbidden (403)

- The IAM policies may not be configured for the user
- Verify the audit/logging/cloud-guard read policies are applied

### Invalid Region

- Ensure the **Region** identifier uses the correct format
  (e.g., `us-ashburn-1`, not `US East (Ashburn)`)

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Verify audit events exist in OCI: **Governance** → **Audit**
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Ensure the compartment has active resources generating events

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
