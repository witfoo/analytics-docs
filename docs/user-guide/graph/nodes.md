# Nodes

Nodes are the fundamental entities in the WitFoo Analytics knowledge graph. Each node represents a distinct object observed in your security data.

## Node Types

| Type | Example | Description |
| --- | --- | --- |
| **IP** | `192.168.1.100` | IPv4 or IPv6 address |
| **Domain** | `example.com` | DNS domain name |
| **User** | `jsmith` | User account identifier |
| **Hostname** | `workstation-01` | System hostname |
| **Hash** | `a1b2c3...` | File hash (MD5, SHA1, SHA256) |
| **Email** | `user@example.com` | Email address |
| **URL** | `https://example.com/path` | Full URL |

## Node Properties

Each node stores:

- **Value** — The entity identifier (IP, domain, etc.)
- **Type** — Entity type from the table above
- **First seen** — Timestamp of earliest artifact referencing this node
- **Last seen** — Timestamp of most recent artifact
- **Artifact count** — Number of artifacts associated with this node
- **Frameworks** — Compliance framework indices where this node appears
- **Flags** — Classification flags (managed, internal, trusted, infrastructure)

## Classification Flags

| Flag | Purpose |
| --- | --- |
| **Managed** | Part of your managed infrastructure — counts toward compliance denominators |
| **Internal** | Inside your network boundary |
| **Trusted** | Known-good entity — reduces incident severity |
| **Infrastructure** | Network infrastructure device — used in infrastructure-focus compliance |

Flags are set automatically by framework-based classification rules and can be manually overridden.

## Searching Nodes

1. Navigate to **Graph** > **Nodes**
2. Enter a search term (IP, domain, username, etc.)
3. Filter by node type, flags, or framework association
4. Click a node to view its detail page

### Node Detail Page

The detail page shows:

- **Summary** — Node value, type, flags, first/last seen
- **Edges** — All relationships to other nodes
- **Artifacts** — Artifacts that reference this node
- **Incidents** — Incidents containing this node
- **Enrichments** — GeoIP, DNS, WHOIS, threat intel data (when available)

## Framework Association

Nodes are associated with compliance frameworks via integer indices. The indices are assigned by sorting enabled framework machine names alphabetically. This mapping is used by compliance calculations to count nodes per framework.
