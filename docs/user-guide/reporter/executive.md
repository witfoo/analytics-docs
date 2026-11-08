# Executive Summary

The Executive Summary provides high-level KPIs for security operations leadership.

## Key Metrics

| Metric | Description | Calculation |
| --- | --- | --- |
| **Total Incidents** | Incidents in the date range | Count of all incidents |
| **True Positives** | Confirmed security incidents | Status: Disrupted (5) or Resolved (3) |
| **False Positives** | Non-incidents | Status: Closed (4) |
| **TP/FP Ratio** | Classification accuracy | True positives / false positives |
| **MTTD** | Mean time to detect | Avg time from first artifact to incident creation |
| **MTTR** | Mean time to respond | Avg time from creation to resolution |

## Page Layout

The Executive Summary page leads with key figures and has no gauges.

1. **Key figures** — WitFoo Readiness, Return on Investment, FTE Headcount, FTE Ratio and Compliance, as large-format figures
2. **Attainment vs Target** — Key figures against their targets
3. **Executive Trends (Daily)** — Daily WitFoo Readiness, ROI and CSC compliance percentages across the selected window
4. **Investigation Snapshot** — MTTD/MTTR metrics, closure rates, and analyst workload
5. **Daily Incident Summary** — Incidents per day by status. Click a bar to drill into the underlying work units.
6. **Analyst Workload** — Per-analyst incident assignments and resolution metrics
7. **Vulnerability Summary** — Host vulnerability scan results from graph node analysis

FTE Ratio is FTE Needed ÷ FTE Budgeted × 100. Lower is better: at or below 100% means budgeted staff can cover the workload.

Percentages are rounded as your browser formats numbers, so -15.45 shows as -15.5%.

## True Positive Classification

TP/FP classification uses incident status IDs:

- **True Positive**: Status is `disrupted` (5) or `resolved` (3)
- **False Positive**: Status is `closed` (4)

## Trend Indicators

Each KPI shows a trend arrow comparing the current period to the previous period of equal length.
