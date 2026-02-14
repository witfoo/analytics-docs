# Reporter

The Reporter module generates executive-level reports on your security operations posture. It combines data from incidents, compliance frameworks, security products, and business settings.

## Report Sections

### [Executive Summary](executive.md)

High-level KPIs including incident counts, true positive/false positive ratios, mean time to detect, and mean time to respond.

### [Compliance Readiness](compliance.md)

Framework-by-framework compliance scoring with per-control drill-down, focus-based filtering, and delta indicators.

### [Tool Effectiveness](tool-effectiveness.md)

Sankey flow diagrams showing artifact-to-incident pipelines, Venn diagrams of product coverage overlap, and per-product detection metrics.

### [Cost & Savings](cost-savings.md)

FTE analysis, profit & loss table, savings histograms, and security spend as a percentage of revenue.

## Date Range Selection

All reports are filtered by date range. Click the date tag in the report header to open the date range picker. Select from preset ranges (7 days, 30 days, 90 days, 1 year) or choose custom dates.

## CSV Export

Each report section supports CSV export. Click the **Download** button to export data. Filenames include report type and current date.

## Permissions

| Action | Required Permission |
| --- | --- |
| View reports | `reports:read` |
| Export reports | `reports:write` |
| Configure settings | `reports:manage` |

## Business Settings Dependency

Reporter calculations depend on settings in **Admin** > **Settings** > **Business Metrics**. See [Business Metrics](../../admin-guide/settings/business-metrics.md).
