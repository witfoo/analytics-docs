# Parser Management

**URL:** `/admin/settings/processors`

The Parser Management page provides control over the 200+ log parsers in the Conductor pipeline. Parsers can be individually enabled or disabled, and a master switch toggles all parsers at once.

## Features

### Master Switch

A global toggle at the top of the page enables or disables all parsers simultaneously. When disabled, no log parsing occurs and all messages route to the `artifacts.unknown` stream.

### Individual Parser Toggles

Each parser has a checkbox toggle for independent enable/disable control. Parsers are organized by category (firewall, IDS/IPS, authentication, DNS, cloud, endpoint, email, network, system).

### Parser Settings

- Settings are preserved when toggling parsers on and off
- Changes propagate to the Signal Parser service within seconds via the NATS KV `PARSERS` bucket
- No container restart is required for configuration changes

!!! note "Race Condition Guard"
    The UI implements a guard against rapid clicks on parser toggles. This prevents race conditions where multiple configuration updates could conflict during propagation to the NATS KV bucket.

## Parser Categories

Parsers are displayed in a searchable, filterable table organized by:

- **Vendor** — The product vendor (Cisco, Palo Alto, Microsoft, etc.)
- **Product** — The specific product or log source
- **Status** — Enabled or disabled

For a complete list of available parsers, see the [Parser Catalog](../parsers-catalog.md).