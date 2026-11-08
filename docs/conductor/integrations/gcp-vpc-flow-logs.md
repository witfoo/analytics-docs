---
tags:
  - integration
  - cloud
---

# GCP VPC Flow Logs

Pulls Google Cloud VPC flow log records from a Pub/Sub subscription, fed by a
Cloud Logging sink, and summarizes them into network conversations with the
same flow engine as the on-premises NetFlow/IPFIX collector and AWS VPC Flow
Logs.

| | |
|---|---|
| **Category** | Cloud Security |
| **Connector Name** | `signal-client.gcp-vpc-flow-pull` |
| **Auth Method** | Service Account JSON |
| **Polling Interval** | 2 min |
| **Multi-Instance** | Yes (up to 5) |
| **Vendor Docs** | [About VPC Flow Logs records](https://cloud.google.com/vpc/docs/about-flow-logs-records) |

## Prerequisites

!!! note "Vendor Requirements"
    A Google Cloud project with VPC Flow Logs, and IAM permission to create a
    Cloud Logging sink, a Pub/Sub topic and subscription, and a service
    account.

- [ ] VPC Flow Logs enabled on the subnets you want visibility into
- [ ] Permission to create a Cloud Logging sink, a Pub/Sub topic and a pull subscription
- [ ] Permission to create a service account and a key for it
- [ ] Network: Conductor can reach the Google Cloud APIs (`*.googleapis.com`) on port 443

## Step 1: Create API Credentials

### Route Flow Logs to Pub/Sub

1. Enable VPC Flow Logs on the subnets you want to collect
2. Create a Cloud Logging **sink** to a Pub/Sub topic with this filter:

    ```text
    resource.type="gce_subnetwork" AND logName:"logs/compute.googleapis.com%2Fvpc_flows"
    ```

3. Create a **pull** subscription on that topic

### Create a Service Account

1. Create a service account for the connector
2. Grant it `roles/pubsub.subscriber` on the subscription only. The connector
   only pulls and acknowledges messages, so it needs nothing more
3. Create a JSON key for the service account and download it

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **GCP VPC Flow Logs**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Project ID** | `my-gcp-project` | The project that owns the Pub/Sub subscription |
    | **Pub/Sub Subscription** | `vpc-flows-sub` | The subscription ID, or the full `projects/PROJECT/subscriptions/NAME` path the console shows |
    | **Service Account Key (JSON)** | *(paste key file)* | The whole downloaded key file. It is stored with the integration's settings and never written to a log |

5. Toggle **Enabled** to on
6. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep -i "gcp"
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for network flow artifacts from this
   source

!!! note "No TCP flags"
    The VPC Flow Logs record format carries byte and packet counts but no TCP
    flag field, so the SYN, RST and FIN counters are zero for this source. A
    zero there means "not reported by GCP", not "none observed".

## Troubleshooting

### Authentication Failed (401 or 403)

- Paste the whole service account key file, including the braces
- Check that the service account has `roles/pubsub.subscriber` on the
  subscription
- Check that **Project ID** is the project that owns the subscription

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Confirm the Cloud Logging sink uses the filter above and writes to the
  topic the subscription is attached to
- Confirm the subscription is a **pull** subscription
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`

### Pulls Pause for Ten Minutes

- One failed hand-off of the connector's output to the pipeline pauses its
  pulls for ten minutes. This is a known limit of this release; collection
  resumes on its own

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
