# Infrastructure Rules

Detect infrastructure health issues including service degradation, certificate problems, and configuration drift.

**5 rules** in this category.

[:material-download: Download all Sigma rules (.zip)](../sigma_rules.zip){ .md-button download="sigma_rules.zip" }

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-infra-001` | Service Disruption | high | T1499 |
| `wf-infra-002` | Degraded Hardware Alert | medium | T1499 |
| `wf-infra-003` | Degraded Service Alert | medium | T1499 |
| `wf-infra-004` | Financial System Anomaly | high | T1565 |
| `wf-infra-005` | Infrastructure Exploit Attempt | critical | T1190 |

## Rule Details

### Service Disruption

**ID:** `wf-infra-001`  
**Source:** [`wf_infra_001.yml`](../sigma/infrastructure/wf_infra_001.yml){ download="wf_infra_001.yml" }  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects service disruption events including denial of service indicators,
service outages, and availability degradation. May indicate active DDoS
attacks, resource exhaustion, or infrastructure failures.

**Tags:** `attack.impact`, `attack.t1499`

??? example "Detection Logic"

    - **messageType**: `service_disruption`

---

### Degraded Hardware Alert

**ID:** `wf-infra-002`  
**Source:** [`wf_infra_002.yml`](../sigma/infrastructure/wf_infra_002.yml){ download="wf_infra_002.yml" }  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects hardware health degradation alerts from infrastructure monitoring
systems. Includes disk failures, memory errors, CPU thermal events, and
power supply issues that may affect system availability.

**Tags:** `attack.impact`, `attack.t1499`

??? example "Detection Logic"

    - **messageType**: `degraded_hardware`

---

### Degraded Service Alert

**ID:** `wf-infra-003`  
**Source:** [`wf_infra_003.yml`](../sigma/infrastructure/wf_infra_003.yml){ download="wf_infra_003.yml" }  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Detects service health degradation including increased latency, elevated
error rates, connection pool exhaustion, and service dependency failures
reported by application performance monitoring tools.

**Tags:** `attack.impact`, `attack.t1499`

??? example "Detection Logic"

    - **messageType**: `degraded_service`

---

### Financial System Anomaly

**ID:** `wf-infra-004`  
**Source:** [`wf_infra_004.yml`](../sigma/infrastructure/wf_infra_004.yml){ download="wf_infra_004.yml" }  
**Level:** high  
**Status:** stable  
**Author:** WitFoo

Detects anomalous activity in financial systems including unauthorized
transaction patterns, accounting system modifications, and payment
processing irregularities that may indicate fraud or data manipulation.

**Tags:** `attack.impact`, `attack.t1565`

??? example "Detection Logic"

    - **messageType**: `financial_anomaly`

---

### Infrastructure Exploit Attempt

**ID:** `wf-infra-005`  
**Source:** [`wf_infra_005.yml`](../sigma/infrastructure/wf_infra_005.yml){ download="wf_infra_005.yml" }  
**Level:** critical  
**Status:** stable  
**Author:** WitFoo

Detects exploit attempts targeting infrastructure components including
web servers, application servers, databases, and network devices. Matches
events classified as exploit attempts with associated CVE identifiers.

**Tags:** `attack.initial_access`, `attack.t1190`

---
