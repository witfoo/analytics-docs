# Product Tiers

This page lists each SKU's price and the licence features the appliance enforces for it in WitFoo Analytics 1.2.0.

WitFoo 1.2.0 ships **9 SKUs** across four products: Conductor, Analytics, Reporter and Console. Console is free.

## Prices

Annual list price per appliance. NZD is the portfolio-wide ×1.3 conversion.

| SKU | USD / yr | NZD / yr |
| --- | ---: | ---: |
| **conductor:lite** | $15,000 | NZ$19,500 |
| **conductor:pro** | $40,000 | NZ$52,000 |
| **conductor:max** | $60,000 | NZ$78,000 |
| **analytics:lite** | $25,000 | NZ$32,500 |
| **analytics:pro** | $75,000 | NZ$97,500 |
| **analytics:max** | $120,000 | NZ$156,000 |
| **reporter:lite** | $20,000 | NZ$26,000 |
| **reporter:pro** | $50,000 | NZ$65,000 |
| **console:lite** | $0 (free) | $0 (free) |

## Feature matrix

● = included · · = not included. These are the feature flags the appliance enforces; a surface
absent from a SKU's column is not merely unadvertised, it is gated off.

| Feature flag | conductor:lite | conductor:pro | conductor:max | analytics:lite | analytics:pro | analytics:max | reporter:lite | reporter:pro | console:lite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `advanced_auditor` | · | · | · | · | ● | ● | · | ● | · |
| `advanced_compliance` | · | · | · | · | ● | ● | · | ● | · |
| `ai_playbooks` | · | · | · | · | · | ● | · | · | · |
| `ai_summaries` | · | · | · | · | ● | ● | · | ● | · |
| `certify` | · | · | · | · | ● | ● | · | ● | · |
| `compliance_csc8` | · | · | · | ● | ● | ● | ● | · | · |
| `console` | · | · | · | · | · | · | · | · | ● |
| `core_integrations` | ● | ● | ● | · | · | · | · | · | · |
| `cost_savings` | · | · | · | · | ● | ● | · | ● | · |
| `custom_integrations` | · | · | ● | · | · | ● | · | · | · |
| `full_integrations` | · | ● | ● | · | · | · | · | · | · |
| `incident_response` | · | · | · | ● | ● | ● | · | · | · |
| [`mcp_connector`](../ai/mcp/licensing.md) | · | · | · | · | ● | ● | · | ● | · |
| `multi_tenancy` | · | · | ● | · | · | ● | · | · | · |
| `protograph` | ● | ● | ● | · | · | · | · | · | · |
| `signal_search` | · | · | · | ● | ● | ● | · | · | · |
| `soar_playbooks` | · | · | · | · | ● | ● | · | · | · |
| `stix_enrichment` | · | ● | ● | · | · | · | · | · | · |
| `threat_model` | · | · | · | · | ● | ● | · | ● | · |
| `tool_efficiency` | · | · | · | · | ● | ● | ● | ● | · |
| `unlimited_data` | ● | ● | ● | · | · | · | · | · | · |

## Bundled Conductor

Analytics and Reporter SKUs include a Conductor tier.

| SKU | Included Conductor tier |
| --- | --- |
| **analytics:lite** | lite |
| **analytics:pro** | pro |
| **analytics:max** | pro |
| **reporter:lite** | lite |
| **reporter:pro** | pro |

## Support by SKU

Support is not a priced tier and there is no SLA SKU. Every paid SKU includes the Maintenance and
Support Services in Exhibit B of the EULA, while the support term is current:

| Channels | Hours | Response commitment | Warranty |
| --- | --- | --- | --- |
| email (<support@witfoo.com>) · support portal (<https://support.witfoo.com>) · phone (+1 503-445-6900) | 8:00 a.m. – 5:00 p.m. US Eastern (GMT-5), excluding weekends and holidays | acknowledged within **15 minutes** by automated means, or during business hours by direct contact. No fixed resolution SLA | 90-day conformance-to-Documentation warranty from delivery |

**console:lite** is free. Its documentation is this site (<https://docs.witfoo.com>).

Full terms are in the EULA ([U.S.A.](eula-usa.md), [New Zealand](eula-nz.md)).
