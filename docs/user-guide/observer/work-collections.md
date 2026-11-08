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

## How Long Collections Are Kept

Work collections and their notes do not expire. A collection's audit log is kept for 90 days.

## Deleting a Collection

Deleting a work collection also deletes its members, assignments, tasks, notes and the notes' files. Deleting a task does the same for what belongs to the task.

A delete that fails keeps the collection or task, so you can repeat it.

## Updating a Collection Through the API

`POST` and `PUT` on `/api/v1/work-collections` change only what the request states:

- Every member (`name`, `description`, `criteria` or `criteria_json`, `enabled`, `assigned_to`, `status_id`) is optional.
- A member the body leaves out, or sets to null, keeps its stored value. A member it states, empty included, replaces it.
- An update writes only what it states, so it never overwrites the collection's statistics.
- A collection created without `enabled` is stored disabled.
- A request that states nothing, that states both `criteria` and `criteria_json`, or whose collection does not validate is refused with HTTP 400.

See [Incidents API](../../api/endpoints/incidents.md).

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
