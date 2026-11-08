# Work Units

Work units represent individual tasks or investigation steps performed by security analysts. Each work unit tracks what was done, who did it, and how long it took.

## Work Unit Properties

| Field | Description |
| --- | --- |
| **Title** | Short description of the task |
| **Description** | Detailed explanation of work performed |
| **Assignee** | Analyst responsible for the work |
| **Status** | Current state (New, Investigating, Resolved, Closed, Disrupted) |
| **Priority** | Task priority (Low, Medium, High, Critical) |
| **Time spent** | Hours invested in this task |
| **Related incident** | Link to the associated incident (optional) |
| **Work collection** | Parent collection grouping related units |
| **Created/Updated** | Timestamps for tracking |

## Creating Work Units

1. Navigate to **Observer** > **Work Units**
2. Click **Create Work Unit**
3. Fill in the title, description, and assignee
4. Optionally link to an incident or work collection
5. Click **Save**

Work units can also be created directly from an incident detail page.

## Work Unit Detail Page

### Triage Summary

The detail page opens on a triage summary. The header shows:

- the work unit's name, its status and its suspicion verdict;
- a severity band and its MO tag;
- a scope line that counts its artifacts, nodes, users and IP addresses.

The response actions stay in a bar that is visible on every tab: AI summary, share to chat, share to CyberGrid, refresh, **Add to Collection**, update status, and **Replay**.

The identifiers, dates and score breakdown are in a **Details** section that starts closed. The score breakdown shows the component weights (Node Score, MO Coverage, Alarm Density, Entity Diversity) and an outlier warning when a score was dampened.

### Tabs

| Tab | Contents |
| --- | --- |
| **Graph** | Interactive graph of the work unit's nodes and edges |
| **Evidence** | Sections for the work unit's **Nodes**, **Edges** and a **Map** of where its nodes are |
| **Artifacts** | The work unit's artifacts, as a histogram, a table and a timeline |
| **Activity** | Notes and the audit log |
| **Response** | Tasks and playbooks. The tab shows the number of open tasks. |

Each tab loads the first time you open it and then stays loaded. The page reads the work unit's artifacts once, and the histogram, the table and the timeline share that set. The open-task count on the **Response** tab appears when that tab is first opened.

When the **Response** tab's read fails, it is tried once and offers **Retry**.

### Edge and Signal Details

The **edge** window opens on the relationship: a sentence that names both ends over the edge type, the observed time span with the number of observations and, when there are enough observations, a small sparkline. Below it are the evidence (bytes, protocols and the matched rules), the two endpoints (select one to open its node) and the observed signals. Editing and the raw fields are in an **Advanced** section.

The **signal** window opens on the event: a sentence of who did what to whom, its time, its severity verdict (critical, high, medium or low, shown with the vendor's own label) and the ATT&CK techniques it matched, by name. Below it are what happened, who and where, and why it matters.

### Node Relationship Graph

In a node's detail, the relationship graph grows on request:

1. It opens with the node's top-ranked relationships.
2. **Show 5 more** adds the next five without moving what is already on screen. A line reads "Showing X of Y relationships".
3. **Undo** removes the last batch, and **Reset graph** returns to the first view.

The graph stops growing at 200 nodes and says so.

## Replay

Replay rebuilds a work unit in the order it was observed. Open it with **Replay** in the response bar, or **Replay timeline** beside the graph.

- Nodes and edges appear as time advances, the artifacts stream into a list at the side, and the MITRE techniques seen so far gather under their tactics.
- Play, pause, previous and next event, a playback speed and a draggable timeline control it. The elapsed-time readout accepts a typed time.
- The replay shows at most 600 nodes. It says "Replaying top N of M nodes" when it leaves some out.
- Escape closes a detail window opened over the replay, or cancels an edit of the elapsed time. Escape with nothing open leaves the replay.

Replay opens only for a role that can read it.

!!! note "Escape key"
    Holding Escape down closes an open detail window and then leaves the replay. Press Escape once for each window.

## Status Workflow

| ID | Status |
| --- | --- |
| 1 | New |
| 2 | Investigating |
| 3 | Resolved |
| 4 | Closed |
| 5 | Disrupted |

## Time Tracking

Time spent on work units feeds into the Reporter module's cost/savings analysis. The total investigation time across all work units contributes to:

- **FTE calculations** — How many full-time analysts are needed
- **Cost per incident** — Average cost based on analyst hourly rates
- **Savings analysis** — Time saved through automation vs manual investigation

## Filtering and Search

The Work Units list shows the node data it holds: its Countries column, Geo Heatmap and Graph views, and its Node Type, Location and Country filters are filled.

- Searches on Node IP, Node Hostname, Node Type, Node MAC, Node Username, Node Internal and Node Managed return the matching work units.
- The Status facet lists the work units in **any** of the statuses you tick. The suspicion level filter works the same way.
- A link to Work Units (from a node's details, the ATT&CK page or a status link) applies the filters it carries, ahead of any filters the search bar remembers.
- The list shows the result of your latest filter or page change, even when an earlier request finishes last.

When a list with more than one status is read over only the newest 10,000 work units, the page says: "This list covers only your organization's newest work units, so older work units with the selected statuses are not shown."

### Removed Search Fields

The Work Units search offers only fields the list can answer. These fields are removed: Edges, Edge Type, Edge Label, Stream Name, Message, Artifact Severity, Server IP and Action, and the **Filter by Alarm Rule...** dropdown.

A saved search or link that still names one lists work units without that filter and shows a notice: "These filters were not applied, because this list cannot filter on them: …"

The time range on the Work Units page is labelled **Time range for CyberGrid jobs:**. It sets only the window of the CyberGrid jobs created from the page. The list itself is not limited by time.

!!! warning "Known limitation"
    A node, ATT&CK technique or Client IP filter reads only that item's newest work units, up to the page size, and the total counts only those.
