# IDS/IPS Rules

Detect intrusion attempts using signature-based alert analysis and evasion detection techniques.

**5 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-ids-001` | Suricata High Severity Alert | critical | T1190 |
| `wf-ids-002` | Suricata ATT&CK Mapped Alert | high | T1059 |
| `wf-ids-003` | Zeek Notice Event | high | T1046 |
| `wf-ids-004` | Deprecated TLS Version Usage | medium | T1573 |
| `wf-ids-005` | Anomalous Network Behavior | medium | T1071 |

## Rule Details

### Suricata High Severity Alert

**ID:** `wf-ids-001`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects high-severity Suricata IDS alerts (severity 1-2) forwarded through
WitFoo's artifact pipeline. These represent the most critical network-based
threat detections requiring immediate investigation.


**Tags:** `attack.initial_access`, `attack.t1190`

??? example "Detection Logic"

    - **streamName**: `suricata`
    - **severityCode**: `['1', '2']`

---

### Suricata ATT&CK Mapped Alert

**ID:** `wf-ids-002`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects Suricata alerts that have been enriched with MITRE ATT&CK technique
mappings, indicating that the IDS signature corresponds to a known adversary
technique. These are higher-confidence detections with tactical context.


**Tags:** `attack.execution`, `attack.t1059`

??? example "Detection Logic"

    - **streamName**: `suricata`
    - **attackTechniqueIds**: `T\d{4}`

---

### Zeek Notice Event

**ID:** `wf-ids-003`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects Zeek (formerly Bro) notice events, which are higher-level network
analysis findings including protocol violations, certificate anomalies,
and behavioral detections from Zeek's scripting engine.


**Tags:** `attack.discovery`, `attack.t1046`

??? example "Detection Logic"

    - **streamName**: `['zeek_notice', 'zeek_weird']`

---

### Deprecated TLS Version Usage

**ID:** `wf-ids-004`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects usage of deprecated TLS versions (TLS 1.0 and TLS 1.1) that are
no longer considered secure. These connections may be targeted for
downgrade attacks and violate modern compliance requirements.


**Tags:** `attack.command_and_control`, `attack.t1573`

---

### Anomalous Network Behavior

**ID:** `wf-ids-005`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects anomalous network behavior events that deviate from established
baselines. These behavioral anomalies may indicate novel attacks, insider
threats, or compromised systems exhibiting unusual communication patterns.


**Tags:** `attack.command_and_control`, `attack.t1071`

??? example "Detection Logic"

    - **messageType**: `anomalous_behavior`

---

