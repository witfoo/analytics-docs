# Cassandra Schema

Overview of the WitFoo Analytics Cassandra database schema.

## Keyspace

```sql
CREATE KEYSPACE IF NOT EXISTS witfoo
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```

## Core Tables

| Table | Partition Key | Description |
| --- | --- | --- |
| `artifacts` | `org_id, artifact_id` | Security artifacts |
| `incidents` | `org_id, incident_id` | Correlated incidents |
| `graph_nodes` | `org_id, node_id` | Entity nodes |
| `graph_edges` | `org_id, edge_id` | Relationship edges |
| `users` | `org_id, user_id` | User accounts |
| `roles` | `org_id, role_id` | Role definitions |

## Settings Tables

| Table | Partition Key | Description |
| --- | --- | --- |
| `business_settings` | `org_id` | Financial/operational settings |
| `frameworks` | `org_id, framework_id` | Compliance frameworks |
| `framework_controls` | `org_id, framework_id, control_id` | Framework controls |
| `product_framework_controls` | `org_id` | Product-control mapping |

## Observer Tables

| Table | Partition Key | Description |
| --- | --- | --- |
| `work_units` | `org_id, work_unit_id` | Analyst work tasks |
| `work_collections` | `org_id, collection_id` | Work groups |
| `mo_definitions` | `org_id, mo_id` | MO patterns |
| `observations` | `org_id, observation_id` | Investigation notes |

## Health Tables

| Table | Partition Key | Description |
| --- | --- | --- |
| `container_metrics` | `org_id, container_name, metric_id` | Container stats |
| `health_alerts` | `org_id, alert_id` | Alert rules |

## Notification Tables

| Table | Partition Key | Description |
| --- | --- | --- |
| `notification_channels` | `org_id, channel_id` | Notification channels |
| `notification_rules` | `org_id, rule_id` | Notification rules |
| `notification_history` | `org_id, rule_id, incident_id, delivery_id` | Delivery log (TTL 30 days) |

## Schema Initialization

Schema is initialized from `cassandra/init-schema.cql` on first boot. Seed data is applied from `cassandra/seeders/`.
