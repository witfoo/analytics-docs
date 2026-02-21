---
tags:
  - integration
---

# Integrations

WitFoo Conductor collects security log data from cloud platforms, endpoints,
identity providers, email security, network infrastructure, and more through
**pull-based API integrations**. The Signal Client service polls each
vendor's API on a configurable schedule and publishes artifacts to the
processing pipeline.

## Quick Start

1. Ensure you have the required vendor license and API access (see each guide's
   **Prerequisites** section)
2. Create API credentials in the vendor console
3. Open the **Conductor UI** → **Integrations** page
4. Select the vendor from the **Add Integration** dropdown
5. Enter your credentials and enable the integration
6. Validate data flow within 1–2 polling cycles

## Integration Catalog

### Endpoint Security

| Integration | Auth Method | Guide |
|---|---|---|
| Cisco AMP | Client ID + API Key | [Enable →](cisco-amp.md) |
| CrowdStrike Falcon | OAuth2 Client Credentials | [Enable →](crowdstrike-falcon.md) |
| Deep Instinct | API Key | [Enable →](deep-instinct.md) |
| SentinelOne | API Token | [Enable →](sentinelone.md) |
| Sophos Central | OAuth2 Client Credentials | [Enable →](sophos-central.md) |
| Carbon Black | API Key | [Enable →](carbon-black.md) |
| Halcyon | Username / Password | [Enable →](halcyon.md) |

### Cloud Security

| Integration | Auth Method | Guide |
|---|---|---|
| Azure Security | OAuth2 (Azure AD) | [Enable →](azure-security.md) |
| AWS GuardDuty | IAM Access Key | [Enable →](aws-guardduty.md) |
| AWS Security Hub | IAM Access Key | [Enable →](aws-securityhub.md) |
| Google Cloud SCC | Service Account JSON | [Enable →](gcp-scc.md) |
| Wiz | OAuth2 Client Credentials | [Enable →](wiz.md) |
| Oracle Cloud (OCI) | API Key (RSA Signing) | [Enable →](oci-cloud.md) |

### Network Security

| Integration | Auth Method | Guide |
|---|---|---|
| Cisco Meraki | API Key | [Enable →](cisco-meraki.md) |
| Cisco Umbrella | API Key + Secret | [Enable →](cisco-umbrella.md) |
| Stealthwatch | Username / Password | [Enable →](stealthwatch.md) |
| Palo Alto Cortex | API Key | [Enable →](pan-cortex.md) |
| Fortinet FortiAnalyzer | Session Token | [Enable →](fortianalyzer.md) |
| Zscaler ZIA | API Key + Session Cookie | [Enable →](zscaler-zia.md) |
| Darktrace | HMAC Token | [Enable →](darktrace.md) |

### Identity & Access

| Integration | Auth Method | Guide |
|---|---|---|
| Cisco Duo | Client ID + Secret | [Enable →](cisco-duo.md) |
| Okta | API Token | [Enable →](okta.md) |
| Auth0 | OAuth2 Client Credentials | [Enable →](auth0.md) |
| 1Password Events | API Token | [Enable →](onepassword-events.md) |
| CyberArk EPM | Username / Password | [Enable →](cyberark-epm.md) |
| Arista AGNI | API Key | [Enable →](arista-agni.md) |

### Email Security

| Integration | Auth Method | Guide |
|---|---|---|
| Mimecast | OAuth2 Client Credentials | [Enable →](mimecast.md) |
| Proofpoint CASB | Client ID + Secret | [Enable →](proofpoint-casb.md) |
| Proofpoint Protect | Client ID + Secret | [Enable →](proofpoint-protect.md) |
| Abnormal Security | API Token | [Enable →](abnormal-security.md) |

### SIEM

| Integration | Auth Method | Guide |
|---|---|---|
| Splunk | Token / Username + Password | [Enable →](splunk.md) |
| Rapid7 InsightIDR | API Key | [Enable →](rapid7-insightidr.md) |

### Infrastructure

| Integration | Auth Method | Guide |
|---|---|---|
| DNS Zone Transfer | None (AXFR) | [Enable →](dns-zone-transfer.md) |
| Druva | Client ID + Secret | [Enable →](druva.md) |
| LimaCharlie | API Key | [Enable →](limacharlie.md) |
| Netskope | API Token (v1/v2) | [Enable →](netskope.md) |

### Vulnerability Management

| Integration | Auth Method | Guide |
|---|---|---|
| Tenable | Access Key + Secret Key | [Enable →](tenable.md) |
| Qualys | Username / Password | [Enable →](qualys.md) |

## Common Configuration

All integrations share these common behaviors:

- **Polling Interval** — Configurable per integration (default varies by vendor).
  Lower intervals mean fresher data but higher API usage
- **Checkpoint Tracking** — Signal Client resumes from the last successful
  position after restarts, avoiding duplicate collection
- **Rate Limiting** — Built-in respect for vendor API quotas with exponential
  backoff on HTTP 429 responses
- **Enable/Disable** — Each integration can be toggled without removing its
  configuration

Configuration changes propagate within seconds via the NATS KV watch mechanism.
No container restart is required.

---

*See also: [Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
