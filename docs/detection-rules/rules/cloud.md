# Cloud Security Rules

Detect cloud infrastructure threats including misconfiguration, privilege escalation, and API abuse.

**6 rules** in this category.

[:material-download: Download all Sigma rules (.zip)](../sigma_rules.zip){ .md-button download="sigma_rules.zip" }

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-cloud-001` | Cloud Privilege Escalation | critical | T1078.004 |
| `wf-cloud-002` | Cloud Configuration Change | high | T1562.007 |
| `wf-cloud-003` | Cloud API Abuse | high | T1106 |
| `wf-cloud-004` | Phishing Email Detection | high | T1566 |
| `wf-cloud-005` | Phishing Link Click | critical | T1204.001 |
| `wf-cloud-006` | Policy Violation | medium | T1078 |

## Rule Details

### Cloud Privilege Escalation

**ID:** `wf-cloud-001`  
**Source:** [`wf_cloud_001.yml`](../sigma/cloud/wf_cloud_001.yml){ download="wf_cloud_001.yml" }  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects privilege escalation events in cloud environments including
IAM role assumption, service account key creation, and permission
boundary modifications.

**Tags:** `attack.privilege_escalation`, `attack.t1078.004`

??? example "Detection Logic"

    - **messageType**: `privilege_escalation`
    - **streamName**: `['aws', 'azure', 'gcp', 'cloud']`

---

### Cloud Configuration Change

**ID:** `wf-cloud-002`  
**Source:** [`wf_cloud_002.yml`](../sigma/cloud/wf_cloud_002.yml){ download="wf_cloud_002.yml" }  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects infrastructure configuration changes in cloud environments that
may weaken security posture, including security group modifications,
firewall rule changes, and logging configuration alterations.

**Tags:** `attack.defense_evasion`, `attack.t1562.007`

??? example "Detection Logic"

    - **messageType**: `config_change`
    - **streamName**: `['aws', 'azure', 'gcp', 'cloud']`

---

### Cloud API Abuse

**ID:** `wf-cloud-003`  
**Source:** [`wf_cloud_003.yml`](../sigma/cloud/wf_cloud_003.yml){ download="wf_cloud_003.yml" }  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects anomalous cloud API call patterns that may indicate compromised
credentials, unauthorized automation, or adversary reconnaissance of
cloud infrastructure.

**Tags:** `attack.execution`, `attack.t1106`

??? example "Detection Logic"

    - **streamName**: `['aws_cloudtrail', 'azure_activity', 'gcp_audit']`
    - **severityLabel**: `['high', 'critical']`

---

### Phishing Email Detection

**ID:** `wf-cloud-004`  
**Source:** [`wf_cloud_004.yml`](../sigma/cloud/wf_cloud_004.yml){ download="wf_cloud_004.yml" }  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects phishing emails identified by email security gateways or
WitFoo's threat intelligence enrichment. Phishing is one of the most
common initial access vectors for cyber attacks.

**Tags:** `attack.initial_access`, `attack.t1566`

??? example "Detection Logic"

    - **messageType**: `phishing_email`

---

### Phishing Link Click

**ID:** `wf-cloud-005`  
**Source:** [`wf_cloud_005.yml`](../sigma/cloud/wf_cloud_005.yml){ download="wf_cloud_005.yml" }  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects when a user clicks on a phishing link, indicating potential
credential compromise or malware delivery. This is a high-priority event
requiring immediate user notification and credential reset evaluation.

**Tags:** `attack.initial_access`, `attack.t1204.001`

??? example "Detection Logic"

    - **messageType**: `phishing_click`

---

### Policy Violation

**ID:** `wf-cloud-006`  
**Source:** [`wf_cloud_006.yml`](../sigma/cloud/wf_cloud_006.yml){ download="wf_cloud_006.yml" }  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects security policy violations including acceptable use violations,
data handling policy breaches, and compliance control failures detected
by DLP, CASB, or policy enforcement tools.

**Tags:** `attack.defense_evasion`, `attack.t1078`

??? example "Detection Logic"

    - **messageType**: `policy_violation`

---
