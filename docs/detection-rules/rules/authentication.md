# Authentication Rules

Detect authentication-based attacks including brute force, credential stuffing, and MFA bypass attempts.

**8 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-auth-001` | Authentication Failure | medium | T1110 |
| `wf-auth-002` | Brute Force Indicator | high | T1110.001 |
| `wf-auth-003` | Credential Access Attempt | high | T1003 |
| `wf-auth-004` | Privilege Escalation | critical | T1068 |
| `wf-auth-005` | Administrative Account Activity | medium | T1078.002 |
| `wf-auth-006` | Malicious Session Detection | high | T1078 |
| `wf-auth-007` | Defense Evasion Activity | high | T1562 |
| `wf-auth-008` | Service Discovery Activity | medium | T1046 |

## Rule Details

### Authentication Failure

**ID:** `wf-auth-001`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects individual authentication failure events. While a single failure
may be benign, these events are the building blocks for brute force and
credential spray correlation rules.


**Tags:** `attack.credential_access`, `attack.t1110`

??? example "Detection Logic"

    - **messageType**: `auth_failure`

---

### Brute Force Indicator

**ID:** `wf-auth-002`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects high-severity authentication failures that may indicate active
brute force attempts. These single-event indicators are enriched by
WitFoo's lead rule engine to flag repeated failures.


**Tags:** `attack.credential_access`, `attack.t1110.001`

??? example "Detection Logic"

    - **messageType**: `auth_failure`
    - **severityLabel**: `['high', 'critical']`

---

### Credential Access Attempt

**ID:** `wf-auth-003`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects credential access attempts including credential dumping, token theft,
and keystroke logging indicators classified by WitFoo's artifact enrichment.


**Tags:** `attack.credential_access`, `attack.t1003`

??? example "Detection Logic"

    - **messageType**: `credential_access`

---

### Privilege Escalation

**ID:** `wf-auth-004`  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects privilege escalation events where a user or process gains elevated
access beyond their normal permissions. This is a critical security event
that may indicate exploitation of vulnerabilities or misconfigurations.


**Tags:** `attack.privilege_escalation`, `attack.t1068`

??? example "Detection Logic"

    - **messageType**: `privilege_escalation`

---

### Administrative Account Activity

**ID:** `wf-auth-005`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects activity by administrative or high-privilege accounts. While not
inherently malicious, tracking admin actions provides audit trail for
compliance and helps identify compromised privileged accounts.


**Tags:** `attack.persistence`, `attack.t1078.002`

??? example "Detection Logic"

    - **userName**: `['admin', 'root', 'Administrator']`
    - **severityLabel**: `['high', 'critical']`

---

### Malicious Session Detection

**ID:** `wf-auth-006`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects sessions classified as malicious by WitFoo's behavioral analysis.
This includes sessions exhibiting characteristics of account takeover,
session hijacking, or unauthorized access after credential compromise.


**Tags:** `attack.defense_evasion`, `attack.t1078`

??? example "Detection Logic"

    - **messageType**: `malicious_session`

---

### Defense Evasion Activity

**ID:** `wf-auth-007`  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects defense evasion techniques including log tampering, security tool
disabling, indicator removal, and other actions intended to avoid detection
by security monitoring systems.


**Tags:** `attack.defense_evasion`, `attack.t1562`

??? example "Detection Logic"

    - **messageType**: `defense_evasion`

---

### Service Discovery Activity

**ID:** `wf-auth-008`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects service discovery and network enumeration activity that may indicate
reconnaissance by an attacker who has gained initial access. Includes port
scanning, service fingerprinting, and network mapping.


**Tags:** `attack.discovery`, `attack.t1046`

??? example "Detection Logic"

    - **messageType**: `service_discovery`

---

