---
tags:
  - integration
  - cloud
---

# AWS Security Hub

Collects aggregated security findings from AWS Security Hub, which
consolidates alerts from GuardDuty, Inspector, Macie, IAM Access Analyzer,
Firewall Manager, and third-party tools into the AWS Security Finding Format
(ASFF).

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.aws-securityhub` |
| **Auth Method** | IAM Access Key + Secret Key |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [AWS Security Hub API](https://docs.aws.amazon.com/securityhub/latest/APIReference/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active AWS account with Security Hub enabled. IAM permissions to create
    users and/or roles.

- [ ] Active AWS account
- [ ] Security Hub enabled in the target region
- [ ] IAM access to create users or roles
- [ ] Network: Conductor can reach `securityhub.<region>.amazonaws.com` on port 443

## Step 1: Create API Credentials

If you already have AWS credentials for [GuardDuty](aws-guardduty.md), you
can reuse the same IAM user — just add the Security Hub policy.

1. Sign in to the **AWS Console** at `https://console.aws.amazon.com/`
2. Navigate to **IAM** → **Users** → **Create user** (or select existing user)
3. Name the user (e.g., `witfoo-securityhub-reader`)
4. Attach the managed policy: **`AWSSecurityHubReadOnlyAccess`**
5. If using an existing GuardDuty IAM user, add this policy to the same user
6. Create an **Access Key** (programmatic access)
7. Copy the **Access Key ID** and **Secret Access Key**

### Enable Security Hub (if not already enabled)

1. Navigate to **Security Hub** in the AWS Console
2. Click **Go to Security Hub** → **Enable Security Hub**
3. Select security standards to enable (CIS, PCI DSS, AWS Foundational)

!!! info "Security Hub vs GuardDuty"
    Security Hub aggregates findings from multiple AWS security services
    including GuardDuty. If you only need GuardDuty findings, use the
    [AWS GuardDuty integration](aws-guardduty.md) instead. Use both if you
    want findings from all integrated AWS security services.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **AWS Security Hub**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Region** | `us-east-1` | AWS region where Security Hub is enabled |
    | **Access Key ID** | `<your-access-key>` | IAM access key from step 1 |
    | **Secret Access Key** | `<your-secret-key>` | IAM secret key from step 1 |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "securityhub"
    ```

    Look for successful poll messages:
    ```
    [INFO] aws-securityhub: fetched <N> findings
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401/403)

- Verify the **Access Key ID** and **Secret Access Key** are correct
- Ensure the IAM user has the `AWSSecurityHubReadOnlyAccess` policy attached
- Check that the access key is active

### Wrong Region

- Security Hub is region-specific — configure one integration per region
- Findings are not cross-region unless using Organizations delegated admin

### No Data Appearing

- Confirm Security Hub is enabled in the target region
- Enable at least one security standard (CIS, PCI DSS) to generate findings
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://securityhub.<region>.amazonaws.com`

---

*See also: [Integration Catalog](index.md) ·
[AWS GuardDuty](aws-guardduty.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
