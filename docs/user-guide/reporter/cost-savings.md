# Cost & Savings

Financial analysis of security operations including FTE requirements and automation savings.

## FTE Analysis

Gauge chart showing calculated analyst headcount:

```text
FTE Needed = (Total Incidents * Avg Hours per Incident) / 2,080
```

Avg Hours = Investigation Time + Restore Time (default: 2.25 hours). 2,080 = 40 hrs/week * 52 weeks.

Shows surplus (green) or deficit (red) versus configured FTE count.

## Profit & Loss Table

Financial summary in monospace format (IBM Plex Mono):

| Section | Contents |
| --- | --- |
| **Revenue** | Annual revenue |
| **Security Spend** | Annual security budget |
| **Product Costs** | Sum of product costs |
| **Personnel Costs** | FTE count * analyst salary |
| **Net Position** | Revenue impact |

## Security Spend Ratio

```text
Security Spend % = (Annual Security Spend / Annual Revenue) * 100
```

## Savings Histogram

Bar chart showing cost savings from automated vs manual investigation.
