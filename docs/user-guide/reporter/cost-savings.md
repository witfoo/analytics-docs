# Cost & Savings

Financial analysis of security operations including FTE requirements and automation savings.

## Cost & Savings Waterfall

The **Cost & Savings Waterfall** shows how gross protection value nets against security costs. Each savings driver rises, each cost falls, and the net equals savings minus costs.

| Step | Kind |
| --- | --- |
| Prevented Revenue Loss | Savings |
| Prevented Brand Damage | Savings |
| Prevented Legal Costs | Savings |
| IT Labor Savings | Savings |
| Insurance Coverage | Savings |
| Total Protection | Subtotal |
| Security Spend | Cost |
| False Positive Cost | Cost |
| Net Savings | Result |

Use **View as table** to read the same steps as a table. When the date range holds no cost or savings, the chart says "No cost or savings in range".

## FTE Analysis

A summary line states the calculated analyst headcount against the budgeted headcount, as a surplus or a deficit. The page has no FTE gauge.

```text
FTE Needed = (Total Incidents * Avg Hours per Incident) / 2,080
```

Avg Hours = Investigation Time + Restore Time (default: 2.25 hours). 2,080 = 40 hrs/week * 52 weeks.

## Profit & Loss Summary

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

## Savings by Category

Bar chart showing the cost savings by category.

Percentages are rounded as your browser formats numbers, so -15.45 shows as -15.5%.
