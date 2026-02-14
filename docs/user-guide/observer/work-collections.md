# Work Collections

Work collections group related work units into logical investigations. They provide a high-level view of effort spent on a security incident or ongoing investigation.

## Work Collection Properties

| Field | Description |
| --- | --- |
| **Name** | Collection title |
| **Description** | Purpose and scope of the investigation |
| **Status** | Active, Complete, or Archived |
| **Owner** | Lead analyst for the collection |
| **Work units** | List of associated work units |
| **Total time** | Aggregated time from all work units |
| **Related incidents** | Linked incidents |
| **Created/Updated** | Timestamps |

## Creating Collections

1. Navigate to **Observer** > **Work Collections**
2. Click **Create Collection**
3. Enter a name and description
4. Assign an owner
5. Click **Save**

Add work units to a collection from either the collection detail page or when creating/editing individual work units.

## Aggregation

Work collections automatically aggregate metrics from their child work units:

- **Total time** — Sum of all work unit time entries
- **Status breakdown** — Count of open, in-progress, and complete units
- **Priority distribution** — Mix of priority levels across units

These aggregates flow into the Reporter module for cost and efficiency analysis.

## Use Cases

| Scenario | Collection Scope |
| --- | --- |
| **Incident response** | All work units related to a single incident |
| **Threat hunt** | Proactive investigation across multiple data sources |
| **Compliance audit** | Evidence gathering for a specific framework |
| **Recurring task** | Ongoing operational tasks (weekly review, etc.) |
