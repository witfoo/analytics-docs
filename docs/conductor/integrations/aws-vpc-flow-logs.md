---
tags:
  - integration
  - cloud
---

# AWS VPC Flow Logs

Pulls Amazon VPC flow log objects from S3, using SQS event notifications as
the work queue, and summarizes them into network conversations with the same
flow engine as the on-premises NetFlow/IPFIX collector.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.aws-vpc-flow-pull` |
| **Auth Method** | IAM Access Key |
| **Polling Interval** | Drains the queue, then waits 5 min |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [Publish flow logs to Amazon S3](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html) |

This connector pulls flow logs from AWS directly. It is separate from the
`awsvpcflow` parser, which reads VPC flow lines that something else forwards
over syslog.

## Prerequisites

!!! note "Vendor Requirements"
    An AWS account with VPC flow logs, and IAM access to create a policy, a
    user or role with an access key, an S3 event notification and an SQS
    queue.

- [ ] VPC flow logs published to an S3 bucket in **text** format (the default, gzip-compressed). Parquet delivery is not read
- [ ] An S3 bucket whose name has **no dots**
- [ ] An SQS queue that receives the bucket's `ObjectCreated` event notifications
- [ ] Network: Conductor can reach the SQS and S3 endpoints of the region on port 443

## Step 1: Create API Credentials

### Publish Flow Logs and Notifications

1. Publish your VPC flow logs to an S3 bucket. Any flow log format is read,
   but prefer a custom format that includes `flow-direction` (a version 5
   field). The default format has no direction column, so each record's
   client and server are decided from port numbers alone. For example:

    ```text
    ${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${tcp-flags} ${pkt-srcaddr} ${pkt-dstaddr} ${flow-direction}
    ```

2. Add an S3 event notification for `ObjectCreated` events that targets an
   SQS queue. Raw S3 notifications and SNS-wrapped delivery both work.
3. Set the queue's default **visibility timeout to at least 300 seconds**.
   With a lower value (30 seconds is the AWS default), SQS delivers messages
   again while large objects are still being processed. Duplicates are
   detected and skipped, but the work is wasted.

### Grant Least-Privilege Access

Create an IAM user or role for the connector with only this policy, then
create an access key for it. Replace the placeholders with your own values:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::YOUR_FLOW_LOG_BUCKET/*"
    }
  ]
}
```

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **AWS VPC Flow Logs**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Region** | `us-east-1` | AWS region of the queue and bucket |
    | **Access Key ID** | *(access key ID)* | IAM access key |
    | **Secret Access Key** | *(secret)* | IAM secret, never logged |
    | **SQS Queue URL** | `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>` | The queue that receives the S3 event notifications |
    | **Log Format (optional)** | *(blank)* | Used only for objects delivered without a header line. Each object's own header line always wins |

5. Toggle **Enabled** to on
6. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "vpc"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for network flow artifacts from this
   source

### Throughput

Each poll drains the queue: it keeps receiving until the queue is empty, up
to **500 messages per cycle**, then waits five minutes. A backlog that
outlasts that is logged as `vpc flow queue backlog`. If you see it, split the
flow logs across a second connector instance with its own queue.

## Troubleshooting

### Authentication Failed (401 or 403)

- Verify the **Access Key ID** and **Secret Access Key**
- Check that the policy grants the three SQS actions on the queue and
  `s3:GetObject` on the bucket
- Check that the **Region** matches the queue

### Bucket Name Contains a Dot

- The connector reads objects at `<bucket>.s3.<region>.amazonaws.com`, and
  S3's certificate does not cover a dotted bucket name there, so the
  connection fails. The log says `s3 bucket name contains a dot` and the
  message stays on the queue. Deliver the flow logs to a bucket whose name
  has no dots

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm the S3 event notification targets the queue named in the form
- Confirm the flow log file format is text. Parquet objects are skipped, and
  the connector logs a warning with the count skipped
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

### Duplicate Deliveries

- Raise the queue's visibility timeout to at least 300 seconds

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
