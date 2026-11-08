# Settings

Organization-wide configuration management.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/settings` | `settings:read` | Get the organization's system settings |
| PUT | `/v1/settings` | `settings:manage` | Update the organization's system settings |
| GET | `/v1/settings/business` | `settings:read` | Get business settings |
| PUT | `/v1/settings/business` | `settings:manage` | Update business settings (partial) |
| GET | `/v1/settings/detected-products` | `settings:read` | List detected products and their configured annual costs |

`PUT /v1/settings` neither saves nor returns SAML or LDAP settings. Use [Authentication Settings](auth-settings.md) for those.

## Business Settings Object

```json
{
  "org_id": "example",
  "fte_cost": 120000,
  "fte_count": 5,
  "annual_revenue": 50000000,
  "annual_spend": 2500000,
  "it_outage_revenue": 0,
  "brand_damage": 0,
  "legal_costs": 0,
  "insurance_coverage": 0,
  "restore_time_hours": 0.75,
  "complex_incident_hours": 8,
  "routine_incident_hours": 1,
  "investigation_time_hours": 1.5,
  "catastrophic_recovery_hours": 72,
  "currency_symbol": "$",
  "default_locale": "en",
  "product_costs": {
    "Palo Alto": 150000,
    "CrowdStrike": 200000
  }
}
```

## Partial updates

From 1.2.0, `PUT /v1/settings/business` changes only the keys the request body carries. A key the body leaves out keeps its stored value. In 1.1.5 a missing key was stored as zero or empty.

- A `product_costs` object in the body replaces the whole map. An explicit `null` or `{}` clears it.
- If the stored settings cannot be read, nothing is written and the request answers `500`.
- A body that is not a JSON object is refused with `400`.

Scripts that send a partial body to clear values must now send those keys with the values they want.

## Routes that switch one setting

From 1.2.0, a route that turns a single thing on or off answers `400` when the request body does not state the value. An empty body no longer means off. The web interface always states the value.

This applies to the switch routes of lead rules, AI provider configurations, classification rules, CyberGrid subscriptions, node enrichment settings, the compliance framework switch, observations, Work Definitions, playbooks, MOS detection and incident-naming words, and to the CyberGrid library settings, the AI profile and response automation settings, the onboarding CyberGrid step and the publication update.

| To turn off | Send |
| --- | --- |
| Any of the routes above | `{"enabled": false}` |
| The Console organization update | the `is_active` field |
| The Conductor appliance-configuration update | `enabled` on every update element |
| The licensing administrator-flag update | the `is_admin` field |
