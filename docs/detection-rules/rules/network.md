# Network Security Rules

Detect network-level threats including traffic anomalies, tunneling, beaconing, and suspicious connections.

**12 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-net-001` | DNS Tunneling Detection | high | T1071.004, T1048 |
| `wf-net-002` | C2 Beaconing Activity | high | T1071.001 |
| `wf-net-003` | Unusual Port Activity | medium | T1571 |
| `wf-net-004` | Large Data Transfer | high | T1048 |
| `wf-net-005` | Port Scan Detection | high | T1046 |
| `wf-net-006` | ICMP Anomaly Detection | medium | T1095 |
| `wf-net-007` | Non-Standard HTTP/HTTPS Port Usage | medium | T1571 |
| `wf-net-008` | Long-Lived Network Connection | medium | T1071 |
| `wf-net-009` | Suspicious SSL/TLS Certificate | medium | T1071.001 |
| `wf-net-010` | Executable File Transfer Over Network | high | T1105 |
| `wf-net-011` | NXDOMAIN/DGA Detection | high | T1568.002 |
| `wf-net-012` | SMB Lateral Movement | high | T1021.002 |

## Rule Details

### DNS Tunneling Detection

**ID:** `wf-net-001`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects potential DNS tunneling activity indicated by unusually long DNS query
domain names (>100 characters), which may indicate data exfiltration or C2
communication via DNS protocol.


**Tags:** `attack.command_and_control`, `attack.t1071.004`, `attack.exfiltration`, `attack.t1048`

??? example "Detection Logic"

    - **protocol**: `DNS`

---

### C2 Beaconing Activity

**ID:** `wf-net-002`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects potential command-and-control beaconing by identifying connections
to external servers classified as botnet or C2 activity by WitFoo lead rules.
Regular-interval check-ins are a hallmark of malware C2 communication.


**Tags:** `attack.command_and_control`, `attack.t1071.001`

??? example "Detection Logic"

    - **messageType**: `botnet_connection`

---

### Unusual Port Activity

**ID:** `wf-net-003`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects network connections on non-standard ports that may indicate evasion
techniques, backdoor communication, or misconfigurations. Focuses on
high-numbered ephemeral ports used as server-side listeners.


**Tags:** `attack.command_and_control`, `attack.t1571`

??? example "Detection Logic"

    - **protocol**: `['TCP', 'UDP']`

---

### Large Data Transfer

**ID:** `wf-net-004`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects unusually large outbound data transfers that may indicate data
exfiltration. Triggers when total bytes transferred exceeds 100MB in a
single connection/session.


**Tags:** `attack.exfiltration`, `attack.t1048`

??? example "Detection Logic"

    - **totalBytes**: `104857600`

---

### Port Scan Detection

**ID:** `wf-net-005`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects network reconnaissance through port scanning activity. Identified
by WitFoo's service discovery classification or IDS rule matches indicating
systematic port probing.


**Tags:** `attack.discovery`, `attack.t1046`

---

### ICMP Anomaly Detection

**ID:** `wf-net-006`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects anomalous ICMP traffic patterns that may indicate ICMP tunneling,
covert channels, or network reconnaissance. Large ICMP payloads or unusual
ICMP types can signify data exfiltration or C2 communication.


**Tags:** `attack.command_and_control`, `attack.t1095`

??? example "Detection Logic"

    - **protocol**: `ICMP`

---

### Non-Standard HTTP/HTTPS Port Usage

**ID:** `wf-net-007`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects HTTP or HTTPS traffic on non-standard ports, which may indicate
evasion of network security controls, malware C2 communication, or
unauthorized web services.


**Tags:** `attack.command_and_control`, `attack.t1571`

---

### Long-Lived Network Connection

**ID:** `wf-net-008`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects network connections with abnormally long durations that may indicate
persistent C2 channels, data exfiltration tunnels, or compromised hosts
maintaining backdoor connections. Flags connections classified as anomalous
behavior by WitFoo enrichment.


**Tags:** `attack.command_and_control`, `attack.t1071`

??? example "Detection Logic"

    - **messageType**: `anomalous_behavior`
    - **protocol**: `['TCP', 'SSL', 'TLS']`

---

### Suspicious SSL/TLS Certificate

**ID:** `wf-net-009`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects network connections involving suspicious SSL/TLS certificates,
including self-signed, expired, or certificates with anomalous attributes.
These may indicate man-in-the-middle attacks, malware C2 infrastructure,
or compromised certificate authorities.


**Tags:** `attack.command_and_control`, `attack.t1071.001`

---

### Executable File Transfer Over Network

**ID:** `wf-net-010`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects transfer of executable files over the network, which may indicate
malware delivery, lateral movement tool staging, or unauthorized software
distribution. Matches common executable extensions and binary content types.


**Tags:** `attack.command_and_control`, `attack.t1105`, `attack.lateral_movement`

---

### NXDOMAIN/DGA Detection

**ID:** `wf-net-011`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects high rates of DNS resolution failures (NXDOMAIN) that may indicate
domain generation algorithm (DGA) activity used by malware for C2 rendezvous.
DGA malware generates pseudo-random domain names, most of which fail to resolve.


**Tags:** `attack.command_and_control`, `attack.t1568.002`

??? example "Detection Logic"

    - **protocol**: `DNS`
    - **action**: `['NXDOMAIN', 'nxdomain', 'SERVFAIL']`

---

### SMB Lateral Movement

**ID:** `wf-net-012`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects SMB (Server Message Block) connections between workstations that may
indicate lateral movement. Legitimate SMB traffic typically flows from
workstations to file servers, not between workstations.


**Tags:** `attack.lateral_movement`, `attack.t1021.002`

??? example "Detection Logic"

    - **serverPort**: `['445', '139']`

---

