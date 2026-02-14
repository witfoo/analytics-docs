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

## Dashboard Layout

1. **KPI tiles** — Large-format cards with trend indicators
2. **Incident timeline** — Bar chart of incident creation over time
3. **Severity distribution** — Breakdown by Critical, High, Medium, Low, Info
4. **Status distribution** — Current status of incidents in the period

## True Positive Classification

TP/FP classification uses incident status IDs:

- **True Positive**: Status is `disrupted` (5) or `resolved` (3)
- **False Positive**: Status is `closed` (4)

## Trend Indicators

Each KPI shows a trend arrow comparing the current period to the previous period of equal length.
