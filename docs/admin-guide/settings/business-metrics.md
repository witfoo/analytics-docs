# Business Metrics

Configure financial and operational parameters used by the Reporter module for cost/savings analysis.

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| **Annual Revenue** | $0 | Organization's annual revenue |
| **Annual Security Spend** | $0 | Total security budget |
| **FTE Count** | 3 | Security team headcount |
| **Investigation Time** | 1.5 hours | Average investigation time per incident |
| **Restore Time** | 0.75 hours | Average remediation time per incident |
| **FTE Hourly Rate** | $75 | Average analyst hourly rate |

## Product Costs

Configure annual costs for each security product. Products appear in the Tool Effectiveness report.

1. Click **Add Product**
2. Enter product name and annual cost
3. Default cost: $100,000 if not specified

## How Settings Are Used

- **FTE Needed** = (Incidents * (Investigation + Restore Time)) / 2,080 hours
- **Security Spend %** = Annual Security Spend / Annual Revenue * 100
- **Cost per Incident** = (Personnel + Product Costs) / Total Incidents

## Configuration

Navigate to **Admin** > **Settings** > **Business Metrics**. Requires `settings:manage` permission.

!!! info "Financial Defaults"
    Financial fields intentionally default to zero. The system does not auto-fill these values because organizations may set them to zero deliberately.
