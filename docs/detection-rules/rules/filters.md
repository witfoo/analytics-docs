# Filter Rules

Noise reduction rules that suppress known benign activity to reduce false positives.

**5 rules** in this category.

## Rule Summary

| ID | Title | Level | ATT&CK |
|-----|-------|-------|--------|
| `wf-filter-001` | Internal Scanner False Positive Filter | medium | T1046 |
| `wf-filter-002` | Backup Transfer False Positive Filter | medium | T1048 |
| `wf-filter-003` | Service Account Auth False Positive Filter | medium | T1110 |
| `wf-filter-004` | CDN/Health Check DNS False Positive Filter | medium | T1071.004 |
| `wf-filter-005` | Monitoring Agent Connection False Positive Filter | medium | T1071 |

## Rule Details

### Internal Scanner False Positive Filter

**ID:** `wf-filter-001`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Filters out port scan detections originating from known authorized
vulnerability scanners and asset discovery tools. Customize the
scanner IP list to match your environment.


**Tags:** `attack.discovery`, `attack.t1046`

??? example "Detection Logic"

    - **messageType**: `service_discovery`

---

### Backup Transfer False Positive Filter

**ID:** `wf-filter-002`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Filters out large data transfer alerts caused by authorized backup
operations. Customize the backup server IPs and schedule windows
to match your backup infrastructure.


**Tags:** `attack.exfiltration`, `attack.t1048`

??? example "Detection Logic"

    - **totalBytes**: `104857600`

---

### Service Account Auth False Positive Filter

**ID:** `wf-filter-003`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Filters out authentication failure events from known service accounts.
Service accounts may generate periodic auth failures during credential
rotation or configuration changes. Customize the service account list
to match your environment.


**Tags:** `attack.credential_access`, `attack.t1110`

??? example "Detection Logic"

    - **messageType**: `auth_failure`

---

### CDN/Health Check DNS False Positive Filter

**ID:** `wf-filter-004`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Filters out DNS tunneling false positives caused by CDN health check
domains, cloud service discovery domains, and other legitimate long
DNS names. Customize domain patterns to match your environment.


**Tags:** `attack.command_and_control`, `attack.t1071.004`

??? example "Detection Logic"

    - **protocol**: `DNS`

---

### Monitoring Agent Connection False Positive Filter

**ID:** `wf-filter-005`  
**Level:** medium  
**Status:** stable  
**Author:** WitFoo

Filters out long-lived connection alerts from known monitoring agents
and management tools that maintain persistent connections by design.
Customize agent patterns to match your monitoring infrastructure.


**Tags:** `attack.command_and_control`, `attack.t1071`

??? example "Detection Logic"

    - **messageType**: `anomalous_behavior`

---

