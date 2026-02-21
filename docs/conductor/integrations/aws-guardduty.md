---
tags:
  - integration
  - cloud
---

# AWS GuardDuty

Collects threat detection findings from Amazon GuardDuty, Amazon's managed
threat detection service that monitors for malicious activity and anomalous
behavior across AWS accounts and workloads.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.aws-guardduty` |
| **Auth Method** | IAM Access Key + Secret Key |
| **Polling Interval** | 5 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [AWS GuardDuty API](https://docs.aws.amazon.com/guardduty/latest/APIReference/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active AWS account with GuardDuty enabled. IAM permissions to create
    users and/or roles.

- [ ] Active AWS account
- [ ] GuardDuty enabled in the target region
- [ ] IAM access to create users or roles
- [ ] Network: Conductor can reach `guardduty.<region>.amazonaws.com` on port 443

## Step 1: Create API Credentials

1. Sign in to the **AWS Console** at `https://console.aws.amazon.com/`
2. Navigate to **IAM** → **Users** → **Create user**
3. Name the user (e.g., `witfoo-guardduty-reader`)
4. Select **Programmatic access** (Access key)
5. Attach the managed policy: **`AmazonGuardDutyReadOnlyAccess`**
6. Complete user creation
7. Copy the **Access Key ID** and **Secret Access Key**

!!! tip "Cross-Account Collection"
    For multi-account environments, create an IAM role with an external ID
    instead of an IAM user. The role should trust the Conductor account and
    have `AmazonGuardDutyReadOnlyAccess` attached.

### Enable GuardDuty (if not already enabled)

1. Navigate to **GuardDuty** in the AWS Console
2. Click **Get Started** → **Enable GuardDuty**
3. GuardDuty begins analyzing VPC Flow Logs, CloudTrail events, and DNS logs

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **AWS GuardDuty**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Region** | `us-east-1` | AWS region where GuardDuty is enabled |
    | **Access Key ID** | `<your-access-key>` | IAM access key from step 1 |
    | **Secret Access Key** | `<your-secret-key>` | IAM secret key from step 1 |
    | **Detector ID** | *(optional)* | Leave blank for auto-discovery |

5. Set the **Polling Interval** (recommended: 5 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

!!! info "Detector ID Auto-Discovery"
    If the **Detector ID** field is left blank, Conductor will automatically
    discover the GuardDuty detector in the configured region using the
    `ListDetectors` API.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "guardduty"
    ```

    Look for successful poll messages:
    ```
    [INFO] aws-guardduty: fetched <N> findings
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

!!! note "GuardDuty Severity Scale"
    GuardDuty findings use a severity scale of 0–8.9. Conductor normalizes
    these to WitFoo severity levels automatically.

## Troubleshooting

### Authentication Failed (401/403)

- Verify the **Access Key ID** and **Secret Access Key** are correct
- Ensure the IAM user has the `AmazonGuardDutyReadOnlyAccess` policy attached
- Check that the IAM user or access key is not disabled

### Wrong Region

- GuardDuty is region-specific — ensure the **Region** field matches where
  GuardDuty is enabled
- If GuardDuty is enabled in multiple regions, create one integration per region

### No Data Appearing

- Confirm GuardDuty is enabled in the target AWS region
- GuardDuty may take up to 24 hours to generate initial findings
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://guardduty.<region>.amazonaws.com`

---

*See also: [Integration Catalog](index.md) ·
[AWS Security Hub](aws-securityhub.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
