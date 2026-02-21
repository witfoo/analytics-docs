# Compliance Rules

Detect compliance policy violations including unencrypted traffic, retention issues, and regulatory control failures.

**5 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-comp-001` | IDS Event Detection | high | T1190 |
| `wf-comp-002` | IPS Action Taken | high | T1190 |
| `wf-comp-003` | Content Filter Match | medium | T1071 |
| `wf-comp-004` | Indicator of Compromise Match | critical | T1071 |
| `wf-comp-005` | Indicator of Misconfiguration Match | medium | T1562 |

## Rule Details

### IDS Event Detection

**ID:** `wf-comp-001`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects intrusion detection system (IDS) alerts forwarded through WitFoo's
artifact pipeline. These are network-based or host-based IDS signatures
that matched suspicious or malicious traffic patterns.


**Tags:** `attack.initial_access`, `attack.t1190`

??? example "Detection Logic"

    - **messageType**: `ids_event`

---

### IPS Action Taken

**ID:** `wf-comp-002`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects intrusion prevention system (IPS) events where protective action
was taken (block, drop, reset). These indicate the IPS actively prevented
a detected attack from succeeding.


**Tags:** `attack.initial_access`, `attack.t1190`

??? example "Detection Logic"

    - **messageType**: `ids_action`

---

### Content Filter Match

**ID:** `wf-comp-003`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects content filtering events where web content, email content, or
file content matched a DLP or content inspection policy. May indicate
sensitive data exposure or policy violations.


**Tags:** `attack.command_and_control`, `attack.t1071`

??? example "Detection Logic"

    - **messageType**: `content_filter`

---

### Indicator of Compromise Match

**ID:** `wf-comp-004`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects matches against known indicators of compromise (IOCs) from threat
intelligence feeds. This includes IP addresses, domain names, file hashes,
and URLs associated with known threat actors or malware campaigns.


**Tags:** `attack.command_and_control`, `attack.t1071`

??? example "Detection Logic"

    - **messageType**: `ioc_match`

---

### Indicator of Misconfiguration Match

**ID:** `wf-comp-005`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects indicators of misconfiguration (IOMs) that may create security
vulnerabilities. Includes open ports, weak encryption, missing patches,
and non-compliant configurations detected by vulnerability scanners
or configuration audit tools.


**Tags:** `attack.defense_evasion`, `attack.t1562`

??? example "Detection Logic"

    - **messageType**: `iom_match`

---

