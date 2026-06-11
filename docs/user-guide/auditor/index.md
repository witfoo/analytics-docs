---
tags:
  - auditor
  - compliance
---

# Auditor

Auditor performs periodic configuration assessment of your cloud platforms and
vulnerability scanners against CIS Benchmarks. Each run produces findings with a
severity, evidence, compliance-framework mappings, and structured remediation
guidance, so you can see where a configuration drifts from best practice and exactly
how to fix it.

Audits run on a per-connector schedule (default `0 */6 * * *` — every 6 hours).
Findings are retained for 90 days and run history for 180 days.

!!! info "License availability"
    Auditor is included in **Analytics Pro**, **Analytics Max**, and
    **Reporter Pro** licenses (previously Analytics Max only). Lite tiers do not
    include Auditor.

## Framework coverage

Every check carries direct per-check mappings to every supported compliance
framework, derived from the CIS official control mappings. The compliance view is
filtered to your **org-enabled frameworks** and offers a framework selector with an
**All frameworks** option.

Two accuracy notes:

- **ISO 27001** control identifiers reflect the platform's current Annex A
  vocabulary, which is a dated control set.
- **PCI DSS** means version 4.0 on-platform; PCI DSS 3.2 is intentionally not
  represented.

## Reading audits and fixing issues

The Auditor lives at **Reporter → Auditor** and has four tabs, all deep-linkable via
query parameters (`?tab=overview|findings|runs|connectors`, plus `?framework=` and
`?control=`):

- **Overview** — overall and per-framework compliance, a framework selector, and a
  30-day compliance trend.
- **Findings** — every finding, filterable by framework, platform, severity, and
  status. Selecting a row opens the finding detail.
- **Runs** — audit run history per connector with pass/fail/error counts.
- **Connectors** — connector configuration (see [Connector setup](#connector-setup)).

The **finding detail** shows the severity and status, the evidence collected, the
framework mappings, and the related MITRE ATT&CK technique ids.

**Structured remediation** is presented as: a summary, numbered fix steps, the
console path, a copyable CLI command, and vendor documentation links.

!!! warning "Offline networks"
    Vendor documentation links open external sites and are unreachable on
    disconnected networks. The platform never fetches these links; they are
    pointers for operators with internet access.

For the org-wide snapshot view, see the [Audit Report](../reporter/audit-report.md)
page. The [Compliance Readiness](../reporter/compliance.md) report also shows
**Audit findings (N)** links that jump from a control row directly to its backing
findings, pre-filtered to that framework and control.

## Permissions

| Action | Required Permission |
| --- | --- |
| View findings, runs, and checks | `auditor:read` |
| Create / modify connectors | `auditor:write` |
| Delete connectors | `auditor:delete` |
| Trigger runs / test connections | `auditor:execute` |
| All auditor operations | `auditor:manage` |

## Connector setup

Auditor connectors are configured in the Analytics UI under
**Reporter → Auditor → Connectors**.

| Connector | Category |
| --- | --- |
| [Amazon Web Services](connectors/aws.md) | Cloud Platform |
| [Google Cloud Platform](connectors/gcp.md) | Cloud Platform |
| [Microsoft Azure](connectors/azure.md) | Cloud Platform |
| [Microsoft 365](connectors/microsoft-365.md) | Cloud Platform |
| [Oracle Cloud Infrastructure](connectors/oci.md) | Cloud Platform |
| [Qualys](connectors/qualys.md) | Vulnerability Scanner |
| [Nessus / Tenable](connectors/nessus-tenable.md) | Vulnerability Scanner |
| [Carson & SAINT](connectors/carson-saint.md) | Vulnerability Scanner |

---

*See also: [Audit Report](../reporter/audit-report.md) ·
[Compliance Readiness](../reporter/compliance.md) ·
[Reporter](../reporter/index.md)*
