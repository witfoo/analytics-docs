# Product Tiers

> **Source of truth:** every row on this page is TRANSCRIBED from executed output of
> `FeaturesForProduct`, `PriceForProduct` and `SupportForProduct` in
> `conductor_suite/common/domain/licensing/product.go` — the same functions the licensing service
> charges and the appliance gates on. It is never authored from a specification. Transcribed
> 2026-08-05 for the 12-SKU portfolio (#605, epic #596). Any portfolio change must re-transcribe
> this page in the same PR; there is no machine parity between the price book and this repository.

WitFoo ships **12 SKUs** across five products. Two of them are free.

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
| **monitor:lite** | $0 (free) | $0 (free) |
| **monitor:pro** | $5,000 | NZ$6,500 |
| **monitor:max** | $10,000 | NZ$13,000 |
| **console:lite** | $0 (free) | $0 (free) |

## Feature matrix

● = included · · = not included. These are the feature flags the appliance enforces; a surface
absent from a SKU's column is not merely unadvertised, it is gated off.

| Feature flag | conductor:lite | conductor:pro | conductor:max | analytics:lite | analytics:pro | analytics:max | reporter:lite | reporter:pro | monitor:lite | monitor:pro | monitor:max | console:lite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `advanced_auditor` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `advanced_compliance` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `ai_playbooks` | · | · | · | · | · | ● | · | · | · | · | · | · |
| `ai_providers` | · | · | · | · | ● | ● | · | ● | · | ● | ● | · |
| `ai_summaries` | · | · | · | · | ● | ● | · | ● | · | ● | ● | · |
| `assessments` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `certify` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `compliance_csc8` | · | · | · | ● | ● | ● | ● | · | · | · | · | · |
| `console` | · | · | · | · | · | · | · | · | · | · | · | ● |
| `core_integrations` | ● | ● | ● | · | · | · | · | · | · | · | · | · |
| `cost_savings` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `custom_integrations` | · | · | ● | · | · | ● | · | · | · | · | · | · |
| `cybergrid_publish` | ● | ● | ● | ● | ● | ● | ● | ● | · | · | · | · |
| `cybergrid_search` | ● | ● | ● | ● | ● | ● | ● | ● | · | · | · | · |
| `data_forwarding` | ● | ● | ● | ● | ● | ● | ● | ● | · | · | · | · |
| `forums` | · | · | · | · | ● | ● | · | · | · | ● | ● | · |
| `full_integrations` | · | ● | ● | · | · | · | · | · | · | · | · | · |
| `help_chatbot` | · | · | · | · | · | ● | · | · | · | · | ● | · |
| `incident_response` | · | · | · | ● | ● | ● | · | · | · | · | · | · |
| `itsm` | · | · | · | ● | ● | ● | · | · | ● | ● | ● | · |
| `kb` | · | · | · | · | ● | ● | · | · | · | ● | ● | · |
| `lms` | · | · | · | · | · | ● | · | · | · | · | ● | · |
| `monitor` | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | · |
| `multi_tenancy` | · | · | ● | · | · | ● | · | · | · | · | ● | · |
| `nbad` | · | · | · | · | ● | ● | · | · | · | · | · | · |
| `outage_detection` | · | · | · | · | ● | ● | · | · | · | ● | ● | · |
| `protograph` | ● | ● | ● | · | · | · | · | · | · | · | · | · |
| `signal_search` | · | · | · | ● | ● | ● | · | · | · | · | · | · |
| `soar_playbooks` | · | · | · | · | ● | ● | · | · | · | · | · | · |
| `stix_enrichment` | · | ● | ● | · | · | · | · | · | · | · | · | · |
| `threat_model` | · | · | · | · | ● | ● | · | ● | · | · | · | · |
| `tool_efficiency` | · | · | · | · | ● | ● | ● | ● | · | · | · | · |
| `unlimited_data` | ● | ● | ● | · | · | · | · | · | · | · | · | · |


## What the matrix means for Monitor

**Monitor is included with Analytics.** Every feature carried by `monitor:<tier>` is also carried
by `analytics:<tier>` at the same tier — that promise is executable, not editorial:
`TestMonitorSubsetOfAnalyticsPerTier` asserts the subset for lite, pro and max, so an Analytics
customer can never discover a Monitor capability they did not buy.

**No Monitor tier can forward data to an external destination.** `data_forwarding` is carried by
all eight conductor / analytics / reporter SKUs and by **none** of the Monitor tiers. A standalone
Conductor Lite ($15,000) can forward; the Conductor bundled inside Monitor cannot, at **any**
Monitor tier including Max. The denial comes from the absence of that flag, never from the tier.

**CyberGrid is not part of any Monitor tier.** Neither `cybergrid_publish` nor `cybergrid_search`
appears in a Monitor column.

## Support by SKU

Support is not a priced tier and there is no SLA SKU. `SupportForProduct` returns exactly two
distinct inclusions:

| SKU set | Channels | Hours | Response commitment | Warranty |
| --- | --- | --- | --- | --- |
| The two $0 products — **monitor:lite**, **console:lite** | documentation (<https://docs.witfoo.com>) | self-service | **None** — community/documentation support only | Provided AS IS; no conformance warranty on the free product |
| **All 10 paid SKUs** | email (<support@witfoo.com>) · support portal (<https://support.witfoo.com>) · phone (+1 503-445-6900) | 8:00 a.m. – 5:00 p.m. US Eastern (GMT-5), excluding US weekends and holidays | acknowledged within **15 minutes** by automated means, or during business hours by direct contact. No fixed resolution SLA | 90-day conformance-to-Documentation warranty from delivery |

Full terms are in the [EULA](eula-nz.md).
