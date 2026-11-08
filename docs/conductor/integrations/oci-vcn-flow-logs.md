---
tags:
  - integration
  - cloud
---

# OCI VCN Flow Logs

Pulls Oracle Cloud Infrastructure VCN flow log records from OCI Logging, through
the Logging Search API with OCI request signing, and summarizes them into
network conversations with the same flow engine as the on-premises
NetFlow/IPFIX collector and AWS VPC Flow Logs.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.oci-vcn-flow-pull` |
| **Auth Method** | API Key (RSA Signing) |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [VCN flow logs](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/vcn-flow-logs.htm) |

This connector collects flow logs. For audit events, logging data and Cloud
Guard problems, see [Oracle Cloud Infrastructure (OCI)](oci-cloud.md).

## Prerequisites

!!! note "Vendor Requirements"
    An active OCI tenancy with VCN flow logs, and IAM permission to create
    users, groups, policies and API keys.

- [ ] VCN flow logs enabled on the subnets or VNICs you want to collect
- [ ] IAM access to create a user, a group, a policy and an API signing key
- [ ] Network: Conductor can reach `logging.<region>.oci.oraclecloud.com` on port 443

## Step 1: Create API Credentials

### Generate an API Signing Key

1. Sign in to the **OCI Console**
2. Create a dedicated user for the connector, and a group that contains it
3. On the user, open **API Keys** and click **Add API Key**
4. Select **Generate API Key Pair**, download the private key, and click
   **Add**
5. Copy the **fingerprint** displayed

!!! warning "Unencrypted key"
    The private key must be unencrypted PEM. A passphrase-protected key is
    refused with an explicit message.

### Grant Least-Privilege Policies

Create a policy for the group, scoped to the compartment that holds the flow
log group:

```text
Allow group <your-group> to read log-content in compartment <your-compartment>
Allow group <your-group> to read log-groups in compartment <your-compartment>
```

### Collect Required OCIDs

| Value | Where to Find |
|-------|---------------|
| **Tenancy OCID** | **Governance** → **Tenancy Details** → OCID |
| **User OCID** | **Identity** → **Users** → select user → OCID |
| **Compartment OCID** | The compartment that holds the flow log group |
| **Log Group OCID** | The log group of the VCN flow log |
| **Flow Log OCID** | The VCN flow log itself |

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **OCI VCN Flow Logs**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Region** | `us-ashburn-1` | Lowercase OCI region identifier. A value with a dot, a slash or an `@` is refused |
    | **Tenancy OCID** | `ocid1.tenancy.oc1..<id>` | From Tenancy Details |
    | **User OCID** | `ocid1.user.oc1..<id>` | The API user whose signing key you supply |
    | **API Key Fingerprint** | `aa:bb:cc:...` | Fingerprint from step 1 |
    | **API Private Key (PEM)** | *(paste PEM content)* | Unencrypted RSA signing key. Never written to a log |
    | **Compartment OCID** | `ocid1.compartment.oc1..<id>` | The compartment holding the flow log group |
    | **Log Group OCID** | `ocid1.loggroup.oc1.<region>.<id>` | The flow log's log group |
    | **Flow Log OCID** | `ocid1.log.oc1.<region>.<id>` | The VCN flow log to read |

5. Toggle **Enabled** to on
6. Click **Save**

The three OCIDs together form the search scope: compartment, log group, log.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "oci"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for network flow artifacts from this
   source

### How Reading Works

- The connector reads the log in pages of up to 1,000 records and follows the
  API's page continuation, so a busy log is read to its end.
- Flow records become searchable some time after the flow starts, so the
  connector reads 4 minutes behind the present.
- If one instant of the log holds more than 10,000 records, the connector
  reads up to that limit, moves on, and logs a warning that names the
  instant.
- It logs a warning when a polling cycle ends more than 5 minutes behind the
  log.

!!! note "Long flows"
    An OCI flow that lasts longer than the connector's four-minute guard is
    never read. This is a known limit of this release.

## Troubleshooting

### Authentication Failed (401)

- Verify the **API Private Key** PEM content is pasted whole, including the
  header and footer lines, and is not passphrase-protected
- Ensure the **API Key Fingerprint** matches the key
- Check that the **User OCID** and **Tenancy OCID** are correct

### Forbidden (403) or Not Found (404)

- Check that the policies above apply to the user's group and the
  compartment that holds the log group
- Check the **Compartment OCID**, **Log Group OCID** and **Flow Log OCID**

### Invalid Region

- Use the region identifier (for example `us-ashburn-1`), not its display
  name

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm the VCN flow log is enabled and receiving records in the OCI Console
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
