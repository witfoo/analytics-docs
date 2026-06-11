---
tags:
  - reporter
  - auditor
  - compliance
---

# Audit Report

The Audit Report is the organization-wide snapshot view of the
[Auditor](../auditor/index.md). It summarizes the latest configuration-audit results
across every connector and compliance framework.

## What the report shows

- **Overall compliance** — the org-wide pass rate, plus total checks, passes, and
  failures.
- **Findings by severity** — failing findings grouped by critical, high, medium, low,
  and info.
- **Framework coverage** — per-framework compliance cards and a gauge for the selected
  framework.
- **Per-connector results** — pass/fail rollups for each configured platform.
- **Top failing checks** — the ten highest-severity failing checks, each with a
  remediation summary and a **View findings** link into the live Auditor.
- **30-day trend** — a daily compliance trend line.

## Date range

The report is snapshot-based and uses the same date-range picker as the other
Reporter pages. Click the date tag in the header to choose a preset or custom range.

## AI Analysis

The **AI Analysis** button generates an on-demand natural-language summary of the
report. Audit snapshots are not summarized automatically — analysis runs only when you
request it.

## Export

- **CSV** — the **Download** button exports the top failing checks and framework
  rollups. Filenames include the current date.
- **Print** — the **Print / Save as PDF** button uses the browser print dialog with
  print styling. There is no separate PDF export.

## Drill-down and cross-links

Full findings are not embedded in the snapshot. Use **Open live Auditor** (or the
**View findings** links) to drill into the live [Auditor](../auditor/index.md), where
findings load on demand. The [Compliance Readiness](compliance.md) report also links
from individual controls to their backing audit findings.

## Permissions

| Action | Required Permission |
| --- | --- |
| View the Audit Report | `reports:read` |
| Drill into findings (live Auditor) | `auditor:read` |
