# Edges

Edges represent observed relationships between nodes in the knowledge graph. When the Graph Processor identifies that two entities appear together in an artifact, it creates or updates an edge recording that relationship.

## Edge Properties

| Property | Description |
| --- | --- |
| **Source node** | The originating entity |
| **Target node** | The destination entity |
| **Relationship type** | Category of the connection |
| **First seen** | Timestamp of the earliest observation |
| **Last seen** | Timestamp of the most recent observation |
| **Artifact count** | Number of artifacts creating this relationship |
| **Weight** | Calculated significance based on frequency and recency |

## Relationship Types

| Type | Example | Description |
| --- | --- | --- |
| **communicated_with** | IP to IP | Network communication observed |
| **resolved_to** | Domain to IP | DNS resolution |
| **authenticated_as** | IP to User | Authentication event |
| **accessed** | User to Hostname | System access |
| **contains** | Hostname to Hash | File observed on system |
| **associated_with** | Generic | Artifact co-occurrence |

## Browsing Edges

1. Navigate to **Graph** > **Edges**
2. Filter by source/target node type or relationship type
3. Use the time range selector to view edges within a specific window
4. Click an edge to see the underlying artifacts

### Edge Detail

The edge detail view shows:

- **Source and target nodes** with links to their detail pages
- **Timeline** of observations (first seen through last seen)
- **Artifact list** — All artifacts that contributed to this edge
- **Related incidents** — Incidents that include artifacts from this edge

## Graph Traversal

Edges enable graph traversal for incident investigation. Starting from any node, follow edges to discover related entities and understand the full scope of an incident. The correlation engine uses this traversal to automatically group related artifacts into incidents.
