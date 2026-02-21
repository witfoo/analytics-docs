# Data Loss Prevention Rules

Detect data exfiltration attempts, unusually large transfers, and policy violations related to data handling.

**6 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-dlp-001` | Data Staging Activity | high | T1074 |
| `wf-dlp-002` | Data Exfiltration | critical | T1041 |
| `wf-dlp-003` | Data Destruction | critical | T1485 |
| `wf-dlp-004` | Large Outbound Data Transfer | high | T1048 |
| `wf-dlp-005` | Suspicious HTTP POST Exfiltration | high | T1048.003 |
| `wf-dlp-006` | Unauthorized File Transfer | high | T1041 |

## Rule Details

### Data Staging Activity

**ID:** `wf-dlp-001`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects data staging activity where an adversary collects and stages data
in preparation for exfiltration. This may include copying files to a
central location, archiving data, or staging data on network shares.


**Tags:** `attack.collection`, `attack.t1074`

??? example "Detection Logic"

    - **messageType**: `data_staging`

---

### Data Exfiltration

**ID:** `wf-dlp-002`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects data exfiltration events where sensitive data is being transferred
to unauthorized external destinations. This is a critical alert requiring
immediate investigation and response.


**Tags:** `attack.exfiltration`, `attack.t1041`

??? example "Detection Logic"

    - **messageType**: `data_exfiltration`

---

### Data Destruction

**ID:** `wf-dlp-003`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects data destruction events including unauthorized file deletion,
disk wiping, and database truncation. May indicate a disgruntled insider,
ransomware cleanup phase, or adversary covering tracks.


**Tags:** `attack.impact`, `attack.t1485`

??? example "Detection Logic"

    - **messageType**: `data_destruction`

---

### Large Outbound Data Transfer

**ID:** `wf-dlp-004`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects large outbound data transfers that exceed typical thresholds,
potentially indicating data exfiltration via network protocols. Focuses
on client-originated bytes to external destinations.


**Tags:** `attack.exfiltration`, `attack.t1048`

??? example "Detection Logic"

    - **clientBytes**: `52428800`

---

### Suspicious HTTP POST Exfiltration

**ID:** `wf-dlp-005`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects large HTTP POST requests to external servers that may indicate
data exfiltration via web protocols. Attackers commonly use HTTP/HTTPS
POST to exfiltrate data as it blends with normal web traffic.


**Tags:** `attack.exfiltration`, `attack.t1048.003`

??? example "Detection Logic"

    - **action**: `POST`
    - **clientBytes**: `10485760`

---

### Unauthorized File Transfer

**ID:** `wf-dlp-006`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects file transfer activity to destinations not on the approved list,
including FTP, SCP, and other file transfer protocols carrying potentially
sensitive data to unauthorized servers.


**Tags:** `attack.exfiltration`, `attack.t1041`

---

