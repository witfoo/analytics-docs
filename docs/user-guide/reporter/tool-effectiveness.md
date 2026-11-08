# Tool Effectiveness

Analyzes how security products contribute to incident detection and response.

## Sankey Flow Diagram

Shows artifact flows from products through types to incident severities. Products ranked by artifact count, top-N shown individually, remainder as "Other".

The Incident Flow chart draws only the flows the report holds. A tool that has incidents but no flow data is named in a note under the chart and is not drawn.

## Product Coverage Venn

Overlap between security products. 1-4 products use fixed geometric layouts; 5-8 use radial layout.

The **Product Incident Overlap** diagram draws the incident counts, exclusive counts and overlaps computed from each product's incidents, with no estimates. A report without them shows the **Likely True+ Incidents** diagram when it has data.

## Product Metrics Table

| Column | Description |
| --- | --- |
| **Product** | Security product name |
| **Artifacts** | Total artifacts generated |
| **Incidents** | Incidents from this product |
| **TP Rate** | True positive rate |
| **Coverage** | Compliance controls detected |
| **Cost** | Annual product cost |
| **Cost per Incident** | Product cost / incidents |

Help tooltips explain calculations. Chart toolbars disabled for clean presentation.
