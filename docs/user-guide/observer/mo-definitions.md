# MO Definitions

Modus operandi (MO) definitions capture known attack patterns, threat behaviors, and adversary techniques. They serve as institutional knowledge that helps analysts recognize recurring threats and respond consistently.

## MO Properties

| Field | Description |
| --- | --- |
| **Name** | Pattern identifier |
| **Description** | Detailed description of the attack pattern or behavior |
| **Category** | Classification (malware, phishing, lateral movement, etc.) |
| **Indicators** | Observable indicators associated with this MO |
| **TTPs** | Tactics, techniques, and procedures |
| **Severity** | Typical severity when this MO is observed |
| **Response playbook** | Recommended response steps |
| **Created by** | Analyst who defined the MO |

## Creating MO Definitions

1. Navigate to **Observer** > **MO Definitions**
2. Click **Create MO Definition**
3. Fill in the name, description, and category
4. Add indicators and TTPs
5. Document the recommended response
6. Click **Save**

## Using MO Definitions

During incident investigation, analysts can:

- **Match incidents to MOs** — Link an incident to a known MO definition
- **Create new MOs** — Document newly observed patterns for future reference
- **Search by indicators** — Find MOs matching observed indicators in current data

## Categories

| Category | Examples |
| --- | --- |
| **Malware** | Ransomware, trojan, worm, rootkit |
| **Phishing** | Spear phishing, credential harvesting, BEC |
| **Lateral Movement** | Pass-the-hash, RDP abuse, SMB pivoting |
| **Exfiltration** | DNS tunneling, cloud storage abuse, encrypted channels |
| **Persistence** | Scheduled tasks, registry modification, backdoor accounts |

## Relationship to Observations

MO definitions provide structure while [observations](observations.md) capture freeform context. An investigation typically involves linking an incident to an MO definition and recording specific observations about how the pattern manifested in that case.
