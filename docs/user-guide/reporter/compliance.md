# Compliance Readiness

The Compliance Readiness report shows your organization's compliance posture against enabled security frameworks using focus-based scoring.

## Framework Selection

Select a framework from the dropdown. The primary framework is selected by default.

## Compliance Score

Overall score displayed as a gauge chart:

| Score Range | Color | Status |
| --- | --- | --- |
| > 75% | Green | Compliant |
| > 0% | Yellow | Partial |
| 0% | Red | Unmet |

### Focus-Based Scoring

Each control has a **focus type** determining the compliance denominator:

| Focus | Denominator |
| --- | --- |
| **Computer** | Managed nodes |
| **User** | User nodes |
| **Infrastructure Device** | Infrastructure nodes |
| **Product** | Security products |

Score = (green + yellow nodes) / auto-detectable nodes * 100. Manual-only controls excluded.

## Per-Control Table

| Column | Description |
| --- | --- |
| **Control ID** | Framework control identifier |
| **Control Name** | Human-readable name |
| **Focus** | Type (Computer=blue, User=purple, Infra=magenta, Product=green) |
| **Compliance %** | Calculated percentage |
| **Detection** | Product + confidence (e.g., "Palo Alto (95%)") |
| **Status** | Compliant / Partial / Unmet / Manual / N/A. **N/A** means no node is in the control's scope. |

### Capability provider

A control that WitFoo Analytics performs for the whole estate lists WitFoo Analytics in the **Detection** column with the note **performs this control**, and no coverage percentage. Hover the note for the full explanation: the Coverage figure on that row counts hosts running a contributing third-party sensor and is not a measure of the platform's own reach. For System Component Inventory, the inventory is a rolling 7-day observation of what has been seen, not a configuration management database.

## Filtering

Two combinable filter dimensions: Compliance status and Focus type. An **N/A** status filter appears when at least one control is N/A.

When you change the date range while an earlier request is still loading, the table shows the answer for the range you selected last.

## Audit Findings

Control rows backed by [Auditor](../auditor/index.md) checks show an **Audit findings (N)** link in the actions column, where N is the number of failing audit checks for that control. The link opens the Auditor **Findings** tab pre-filtered to that framework and control, so you can see and remediate the exact failing checks. It appears only when there are failing findings, independent of whether a detection product is deployed for the control.

## Delta Indicator

Shows compliance score change across date range snapshots.

## CSV Export

Exports per-control table with current filters. An N/A control reads `N/A` in the CSV. Filename: `{framework}_Compliance_{date}.csv`, with spaces in the framework name replaced by `_`.
