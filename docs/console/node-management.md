# Remote Node Lifecycle Management

The WitFoo Console provides remote lifecycle management capabilities for Analytics and Conductor nodes directly from the web interface. This feature enables administrators to perform essential maintenance operations such as starting, stopping, restarting, upgrading, and pulling container images without direct SSH access to the appliances.

## Overview

Remote node management is a key administrative feature that allows **ORG_ADMIN** and above to control node operations from a centralized location. This is particularly useful in multi-appliance deployments where direct access to individual nodes may be restricted or inconvenient.

### Requirements

- **User Role:** ORG_ADMIN or above
- **WFA Version:** 2.2.0 or later
- **Node Status:** Connected to the Console
- **Network:** Bidirectional connectivity between Console and target node

## Accessing Node Management

To manage a node's lifecycle:

1. Navigate to **Admin** > **Nodes**
2. Click on the target node to open its details panel
3. Select the **Node Actions** tab
4. Choose the desired action from the available options

## Available Actions

### Start Node

Starts a stopped or halted node.

- **Use case:** Bringing a node back online after maintenance or planned downtime
- **Impact:** Node services initialize and become available
- **Duration:** Typically 2-5 minutes depending on role and configuration

### Stop Node

Gracefully stops all services on the node.

- **Use case:** Planned maintenance or taking a node offline temporarily
- **Impact:** All services shut down; node becomes unavailable
- **Duration:** 30-60 seconds for graceful shutdown

### Restart Node

Performs a graceful restart of all services on the node.

- **Use case:** Applying configuration changes or recovering from service issues
- **Impact:** Temporary service interruption (2-5 minutes)
- **Cluster Impact:** For Analytics data nodes, temporary Cassandra quorum adjustment during restart

### Upgrade Node

Upgrades the node to a new WFA version.

- **Use case:** Deploying security patches, feature updates, or bug fixes
- **Impact:** Services restart with new version; configuration is preserved
- **Duration:** 5-10 minutes depending on services and role
- **Version Check:** Console validates compatibility before upgrade

### Pull Images

Pulls the latest container images for all services on the node.

- **Use case:** Ensuring the node has the most recent image builds without restarting
- **Impact:** New images are downloaded; running services continue until explicitly restarted
- **Duration:** 2-5 minutes depending on image sizes and network bandwidth

## Data Node Cluster Considerations

!!! warning "Data Node (Cassandra) Restart Impact"
    When restarting or upgrading an Analytics node configured as a **data node** (Cassandra), the following applies:

    - **Quorum Impact:** The node temporarily leaves the Cassandra cluster, reducing quorum availability
    - **Confirmation Required:** You must confirm cluster impact before proceeding with the restart or upgrade
    - **Cluster Validation:** The operation checks that the cluster can tolerate the node's absence
    - **Multi-Node Clusters:** In clusters with 3+ data nodes, quorum is maintained; in 2-node clusters, operations require explicit confirmation

## Job Result Tracking

Each remote management action creates a job that can be tracked in real-time:

1. After initiating an action, a notification appears with a job ID
2. Navigate to **Admin** > **Jobs** or **Health** > **Jobs** to view job status
3. Click the job to view:
   - Current status (Running, Completed, Failed)
   - Start and end times
   - Detailed logs from the WFA daemon
   - Any warnings or errors encountered

### Job States

| State | Description |
| --- | --- |
| **Running** | Action is in progress on the node |
| **Completed** | Action finished successfully |
| **Failed** | Action encountered an error; check logs for details |
| **Timeout** | Action did not complete within expected time window |

## Best Practices

- **Maintenance Windows:** Schedule node operations during low-traffic periods
- **Data Nodes:** In production Cassandra clusters, coordinate data node restarts to maintain quorum
- **Sequential Operations:** Allow previous operations to complete before starting new ones on the same node
- **Monitor Health:** Check the **Health** dashboard after operations complete
- **Backup:** For critical operations like upgrades, ensure recent backups are available

## Troubleshooting

### Node Appears Disconnected

If a node shows as disconnected and you cannot perform actions:

1. Verify network connectivity between Console and node
2. Check the node's WFA daemon status: `sudo wfa health`
3. Review Console logs for connection errors
4. Restart the Console if the node remains unreachable

### Action Fails With Timeout

If an action times out:

1. Check the node's actual status via SSH: `sudo wfa [role] status`
2. Review the job logs in the Console for specific error messages
3. Verify the node has sufficient disk space and resources
4. Retry the operation during a lower-load period

### Cassandra Quorum Warnings

If you see quorum warnings when restarting a data node:

1. Verify all other data nodes are healthy
2. Ensure bidirectional connectivity between data nodes
3. Check Cassandra cluster status via nodetool on one of the data nodes
4. In 2-node clusters, explicitly confirm the restart operation

## Related Documentation

- [Admin Guide](../admin-guide/index.md)
- [Deployment - WFA Integration](../deployment/wfa.md)
- [WFA CLI Reference](../conductor/wfa-cli.md)
