# Vrax Threat Intelligence

Import the threat-intelligence reports your Vrax account holds, and see them beside the nodes they mention.

## What It Does

Vrax (`app.vrax.io`) publishes completed threat-intelligence reports to its customers. An administrator gives the appliance a Vrax login. The appliance then:

1. Pulls the reports that login is entitled to, for your industry and region, on a schedule.
2. Stores them on the appliance.
3. Shows the stored reports that mention a node's addresses, domains, URLs or file hashes in the node's detail window.

It is a one-way import. The appliance sends Vrax your login, your industry and region, and an optional date. It never sends a node, an address or an indicator from your data. Nothing it stores changes a node's classification, a score, a work unit or a report.

There are two separate connections. You can use either or both:

| Card | Credential | What it reads |
| --- | --- | --- |
| **Vrax threat intelligence** | Your Vrax username and password | Vrax's completed reports |
| **Vrax feed (MISP)** | A feed credential: an Auth ID and a secret | Vrax's feed in MISP format |

## Where to Find It

Navigate to **Search** > **Node Enrichment**. The page is headed **Node Enrichment Settings**, and both Vrax cards are on it.

## Permissions

| Action | Required Permission |
| --- | --- |
| Set up, test, run and delete a connection | `signals:manage` |
| See the Vrax panel in a node's detail window | `signals:read` |

There is no separate permission and no licence feature for Vrax. The import is available at every tier.

## Setting Up the Report Import

!!! tip "Use a dedicated Vrax user"
    Vrax recommends a dedicated Vrax user for each customer, with permissions limited to this feed. The appliance stores the login, so a user that can do nothing else limits what a leaked login could do.

1. Open **Search** > **Node Enrichment** and find the **Vrax threat intelligence** card.
2. Choose the **Industry** and **Region** your Vrax account holds.
3. Enter the **Vrax username** and **Vrax password**.
4. Choose the **Poll interval**: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours (the default), 2 days, 3 days or 7 days.
5. Turn on **Import Vrax reports** and click **Save**.
6. Click **Test connection** to send one validation request. The result can take up to about 90 seconds.
7. Click **Run now** to start a pull at once.

When a login is already saved, leaving both credential fields empty keeps it, and entering both replaces it. The login is stored encrypted and is never shown again.

## Setting Up the MISP Feed

1. On Vrax's Subscriptions page, create a feed credential for this appliance. The same page lets you rotate and deactivate credentials.
2. Open **Search** > **Node Enrichment** and find the **Vrax feed (MISP)** card.
3. Choose the **Industry** and **Region**, and enter the **Vrax feed Auth ID** and **Vrax feed secret**.
4. Choose the **Poll interval**, turn on **Read the Vrax feed** and click **Save**.
5. Click **Test connection** to request the feed's list of events once, or **Run now** to start a read.

The Auth ID may not contain a colon. Neither value may start or end with a space.

A feed with many events takes more than one run to read in full: one run reads at most 200 new or changed events. **Run now** continues it sooner.

## Status

| Status | Meaning |
| --- | --- |
| Idle | Nothing has run yet. Save, enable and click **Run now**. |
| Running | A pull is in progress. |
| Last run succeeded | The last pull finished. |
| Last run partly succeeded | It finished, but some records could not be read or stored, or a limit stopped it. |
| Refused | Vrax refused the request. See below. |
| Cannot reach Vrax | The connection failed, timed out or got a server error. The stored reports remain available, and it retries after a wait. |
| Rate limited | Vrax asked for fewer requests. It retries after a wait. |
| Settings not valid | The stored industry, region or login is not usable. Choose them again and save. |
| Unexpected response | Vrax answered in a form the appliance does not read. It retries after a wait. |
| Held back (size check) | A pull would have removed too much of the stored data, so nothing from it was applied. Nothing is lost. |

### A refusal stops the schedule

Vrax answers every authentication failure with the same page, so the appliance cannot tell a wrong password from a wrong industry, region or plan. The card says "the credentials, the industry and region, or the plan may be wrong".

Repeated failed logins can lock a Vrax account, so a refusal stops the automatic schedule. No further automatic pull runs until an administrator saves new credentials or changes the industry or region. **Run now** still tries once when you ask.

## What Appears on Nodes

When a stored report or feed event mentions one of a node's values, the node's detail window shows a panel headed "Vrax reports that list values of this node". Each entry names its source, **Vrax REST import** or **Vrax MISP feed**.

- The lookup reads the data stored on the appliance. Nothing is sent to Vrax to look a node up.
- Only external values are looked up. An address in your own network is never looked up.
- When no stored report mentions the node, the panel is not shown. An empty panel would read as reassurance the data cannot give.
- The panel lists at most 20 reports and says "Showing N of M" when more matched.
- Everything Vrax wrote is shown as plain text. A link is offered only for a plain `https` address.

## Deleting a Connection

**Delete connection** removes the saved credential and turns the connection off. With the box ticked, it also deletes the reports or events, the indicators and the sync state stored for that connection. The other connection's data is not touched.

## Network and Security

- The appliance contacts only `app.vrax.io` on port 443. Allow outbound HTTPS to it if you use either connection.
- The import does not use an environment proxy. An appliance that reaches the internet only through a proxy cannot use it.
- Redirects are never followed.
- Credentials are sealed with the appliance's encryption key, `AUTH_CONFIG_ENCRYPTION_KEY`. If you replace that key and lose the old one, enter the credentials again.
- An appliance that cannot reach `app.vrax.io` keeps what it stored and shows the status. Nothing new is fetched until the next check.

## API

The routes are under `/api/v1/vrax`. The MISP feed's routes are under `/api/v1/vrax/misp`.

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/vrax/connection` | `signals:read` | Settings without the login, the sync status and counts, and the last test result |
| PUT | `/v1/vrax/connection` | `signals:manage` | Save settings. `enabled` and `interval_minutes` are required. |
| DELETE | `/v1/vrax/connection` | `signals:manage` | Remove the login. `?purge=true` also deletes the stored data. |
| POST | `/v1/vrax/connection/test` | `signals:manage` | Run one validation request in the background (answers `202`) |
| POST | `/v1/vrax/sync/run` | `signals:manage` | Start a pull (answers `202`) |
| GET | `/v1/vrax/reports` | `signals:read` | The newest stored reports. `?kind=misp` lists feed events. |
| POST | `/v1/vrax/lookup` | `signals:read` | Look up values in the stored data |
| GET | `/v1/vrax/misp/connection` | `signals:read` | The feed connection's settings and status |
| PUT | `/v1/vrax/misp/connection` | `signals:manage` | Save the feed settings |
| DELETE | `/v1/vrax/misp/connection` | `signals:manage` | Remove the feed credential. `?purge=true` also deletes the stored events. |
| POST | `/v1/vrax/misp/connection/test` | `signals:manage` | Test the feed credential |
| POST | `/v1/vrax/misp/sync/run` | `signals:manage` | Start a feed read |

No response, header, log line or error carries the login or the feed secret.

## Known Limitations

- **Context is as current as the last successful check.** An appliance that cannot reach `app.vrax.io` keeps what it stored.
- **The two connections are separate.** Each organization has one login connection and one feed connection. They store their data separately, and a refusal on one does not stop the other.
- **No proxy support.** See [Network and Security](#network-and-security).
- **A refused login is not retried on its own.** See [A refusal stops the schedule](#a-refusal-stops-the-schedule).
