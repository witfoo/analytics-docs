# Subscriptions

Connect to external threat intelligence feeds via CyberGrid.

## Managing Subscriptions

1. Navigate to **CyberGrid** > **Subscriptions**
2. Browse available feeds
3. Click **Subscribe** and configure sync schedule
4. Set confidence thresholds (optional)

## Subscription Properties

| Field | Description |
| --- | --- |
| **Feed name** | Intelligence feed name |
| **Publisher** | Organization providing the feed |
| **Status** | Active, Paused, or Error |
| **Last sync** | Most recent successful sync |
| **Indicator count** | Indicators from this feed |
| **Sync schedule** | Update frequency |

## Indicator Types

Feeds can include IPs, domains, file hashes, URLs, and email addresses.

## Enrichment Integration

Matched indicators update node threat scores, affecting incident severity and compliance calculations.
