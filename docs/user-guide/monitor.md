# Monitor

Monitor is WitFoo's IT-operations product: network and application health, an ITSM ticket desk,
and — on the paid tiers — outage detection, a knowledge base, community forums and in-product
training.

> **Where the numbers live.** This page describes what each tier is *for*. The authoritative,
> per-feature grid — prices in USD and NZD, and every capability by SKU — is
> [Product Tiers](../reference/product-tiers.md), which is transcribed from executed output of the
> same functions the appliance gates on. Where the two disagree, the grid is right and this page is
> stale; please file it.

## The three tiers

| Tier | Price / yr | What it adds |
| --- | ---: | --- |
| **Monitor Lite** | Free | Network, application and device monitoring, plus the ITSM ticket desk. |
| **Monitor Pro** | $5,000 | Adds outage detection, the knowledge base, community forums, and AI assistance (summaries and your own AI provider configuration). |
| **Monitor Max** | $10,000 | Adds the in-product help chatbot, the in-product training library, and multi-tenancy for managing several organizations from one appliance. |

Each tier is cumulative: Pro carries everything Lite carries, and Max carries everything Pro
carries.

## What every tier includes

**Monitoring.** Flow, interface, device and application health, with hourly rollups, ranked
talkers and conversations, and scheduled reports.

**ITSM.** Tickets with assignment, comments, status workflow and export — the desk an IT team
works out of day to day.

## What the paid tiers add

**Outage detection (Pro, Max).** Confirmed outages are raised from your own telemetry — an
interface held down across consecutive polls, or a device whose uptime counter went backwards
(an inferred reboot) — and become work units rather than another dashboard to watch. Two further
detectors ship switched off by default and can be enabled per organization; see
[Configuration](../deployment/configuration.md).

**Knowledge base and forums (Pro, Max).** A KB for your own runbooks and a discussion forum for
your team, both inside the appliance. They are deliberately separate surfaces: a forum thread is
not a KB article and neither writes into the other.

**AI assistance (Pro, Max).** AI summaries, and the provider-configuration screens that let you
point the appliance at your own AI provider. All AI capability is a paid-tier feature; the free
tier carries none of it.

**Help chatbot (Max).** A support assistant grounded in your knowledge base and your tickets. It
answers only from sources it actually retrieved and cites them; when it cannot, it says so and
offers to open a ticket instead of guessing.

**In-product training (Max).** A course library served from the appliance itself, with per-user
progress. The pages fetch nothing from outside the appliance; where a lesson has a video, it is a
plain link you can choose to open.

**Multi-tenancy (Max).** Manage several organizations from one appliance, with a combined
cross-tenant view of tickets and monitoring.

## Two boundaries worth knowing before you buy

**Monitor is included with Analytics.** Every capability carried by a Monitor tier is also carried
by the Analytics tier of the same name. That is not an editorial promise — it is asserted by a test
against the licensing source (`TestMonitorSubsetOfAnalyticsPerTier`), so an Analytics customer can
never find a Monitor capability they did not already buy. If you run Analytics, you do not need to
add Monitor.

**No Monitor tier forwards data to an external destination.** Monitor bundles a Conductor for
ingest, but forwarding processed data out to a third-party destination is a Conductor / Analytics /
Reporter entitlement and is absent from **every** Monitor tier, Max included. A standalone
Conductor Lite can forward; the Conductor bundled inside Monitor cannot. If external forwarding is
what you need, the product is Conductor, not Monitor.

**CyberGrid is not part of Monitor.** Neither threat-intelligence publishing nor searching appears
in any Monitor tier. Monitor is IT operations, not threat intel.

## Support

Monitor Lite is a free product and carries **documentation-only** support with no response
commitment and no conformance warranty. Monitor Pro and Max carry the same paid-tier support as
every other paid SKU — email, support portal and phone, US-Eastern business hours, acknowledgement
within 15 minutes by automated means, and a 90-day conformance-to-Documentation warranty. The exact
wording is in [Support](../reference/product-tiers.md#support-by-sku) and the
[EULA](../reference/eula-nz.md).

## Related

- [Product Tiers](../reference/product-tiers.md) — the full per-SKU capability and price grid
- [Roles and permissions](../admin-guide/roles.md) — who can see and change what
- [Health](health/index.md) — the appliance's own health dashboard, which is a different thing from
  Monitor's view of your network
