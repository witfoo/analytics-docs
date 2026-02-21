# Correlation Rules

Multi-event behavioral detections using Sigma v2 correlation syntax for event counting, value counting, and temporal ordering.

**8 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-corr-001` | Brute Force Attack Sequence | high | T1110 |
| `wf-corr-002` | Credential Spraying Attack | high | T1110.003 |
| `wf-corr-003` | Lateral Movement Chain | critical | T1021.002 |
| `wf-corr-004` | Data Exfiltration After Reconnaissance | critical | T1041, T1046 |
| `wf-corr-005` | Ransomware Kill Chain | critical | T1486 |
| `wf-corr-006` | Phishing to Account Compromise | critical | T1566, T1078 |
| `wf-corr-007` | Multi-Source C2 Beaconing | critical | T1071.001 |
| `wf-corr-008` | Repeated Policy Violations | high | T1078 |

## Rule Details

### Brute Force Attack Sequence

**ID:** `wf-corr-001`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Correlates multiple authentication failure events from the same source IP
within a 5-minute window. Five or more failures indicate a likely brute
force attack requiring investigation and potential IP blocking.


**Tags:** `attack.credential_access`, `attack.t1110`

**Type:** `event_count`  
**Group By:** `clientIP`  
**gte:** `5`  

---

### Credential Spraying Attack

**ID:** `wf-corr-002`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Correlates authentication failures targeting the same server with 10 or
more distinct usernames within 15 minutes. This pattern is characteristic
of credential spraying attacks where an adversary tries common passwords
across many accounts.


**Tags:** `attack.credential_access`, `attack.t1110.003`

**Type:** `value_count`  
**Group By:** `serverIP`  
**field:** `userName`  
**gte:** `10`  

---

### Lateral Movement Chain

**ID:** `wf-corr-003`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects a lateral movement chain where SMB connections between workstations
are followed by malicious session indicators from the same source IP
within 30 minutes. This ordered sequence suggests an attacker moving
through the network after initial compromise.


**Tags:** `attack.lateral_movement`, `attack.t1021.002`

**Type:** `temporal_ordered`  
**Group By:** `clientIP`  

---

### Data Exfiltration After Reconnaissance

**ID:** `wf-corr-004`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects the attack pattern of network reconnaissance (port scanning)
followed by data exfiltration from the same source IP within 60 minutes.
This ordered sequence indicates an adversary who has completed discovery
and is actively extracting data.


**Tags:** `attack.exfiltration`, `attack.t1041`, `attack.discovery`, `attack.t1046`

**Type:** `temporal_ordered`  
**Group By:** `clientIP`  

---

### Ransomware Kill Chain

**ID:** `wf-corr-005`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects the complete ransomware kill chain: payload download followed by
active encryption from the same source within 60 minutes. This is a
critical alert indicating a ransomware attack has progressed from
delivery to impact phase.


**Tags:** `attack.impact`, `attack.t1486`

**Type:** `temporal_ordered`  
**Group By:** `clientIP`  

---

### Phishing to Account Compromise

**ID:** `wf-corr-006`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects the phishing attack chain where a user clicks a phishing link
followed by a malicious session from the same user within 30 minutes.
This indicates successful credential harvesting leading to account
compromise.


**Tags:** `attack.initial_access`, `attack.t1566`, `attack.t1078`

**Type:** `temporal_ordered`  
**Group By:** `userName`  

---

### Multi-Source C2 Beaconing

**ID:** `wf-corr-007`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects a single C2 server receiving beaconing connections from 3 or more
distinct internal hosts within 60 minutes. Multiple infections communicating
with the same C2 infrastructure indicates a widespread compromise requiring
coordinated response.


**Tags:** `attack.command_and_control`, `attack.t1071.001`

**Type:** `value_count`  
**Group By:** `serverIP`  
**field:** `clientIP`  
**gte:** `3`  

---

### Repeated Policy Violations

**ID:** `wf-corr-008`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects users who trigger 5 or more security policy violations within a
24-hour period. Repeated violations may indicate a compromised account,
insider threat activity, or a user systematically circumventing controls.


**Tags:** `attack.defense_evasion`, `attack.t1078`

**Type:** `event_count`  
**Group By:** `userName`  
**gte:** `5`  

---

