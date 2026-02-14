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
| **Status** | Compliant / Partial / Unmet / Manual |

## Filtering

Two combinable filter dimensions: Compliance status and Focus type.

## Delta Indicator

Shows compliance score change across date range snapshots.

## CSV Export

Exports per-control table with current filters. Filename: `{framework}_compliance_{date}.csv`.
