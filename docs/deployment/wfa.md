# WFA Deployment

The WitFoo Appliance (WFA) CLI provides automated deployment and management of WitFoo Analytics.

## Installation

```bash
wfa analytics install --role <role>
```

### Available Roles

| Role | Description |
| --- | --- |
| `aio` | All-in-One: all analytics services |
| `aio-conductor` | AIO + Conductor signal pipeline |
| `data-node` | Dedicated Cassandra database node |
| `processing-node` | Dedicated processing (external Cassandra) |

## Configuration

```bash
wfa analytics configure
```

The interactive wizard configures:

- **Retention** — Data retention periods
- **UI Modules** — Which modules to enable (all, search-only, search+observer)
- **CyberGrid** — Intelligence feed settings
- **Clustering** — Multi-node Cassandra configuration

## Management Commands

| Command | Description |
| --- | --- |
| `wfa analytics start` | Start all services |
| `wfa analytics stop` | Stop all services |
| `wfa analytics status` | Show service status |
| `wfa analytics upgrade` | Upgrade to new version |

## Hardware Validation

The `install` command validates hardware against the role's minimum requirements before proceeding:

| Role | Min CPU | Min RAM | Min Disk |
| --- | --- | --- | --- |
| AIO | 4 cores | 8 GB | 50 GB |
| AIO + Conductor | 8 cores | 16 GB | 100 GB |
| Data Node | 4 cores | 8 GB | 200 GB |
| Processing Node | 4 cores | 8 GB | 50 GB |
