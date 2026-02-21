---
tags:
  - integration
  - vulnerability
---

# Qualys

Collects vulnerability scan results and host detection data from Qualys
Vulnerability Management, providing visibility into vulnerability posture
across your infrastructure.

| | |
|---|---|
| **Category** | Vulnerability Management |
| **Connector Name** | `signal-client.qualys` |
| **Auth Method** | Basic Auth (Username + Password) |
| **Polling Interval** | 30 min |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Qualys API Documentation](https://qualysguard.qualys.com/qwebhelp/fo_portal/api_doc/) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Qualys subscription with API access enabled. Manager or higher
    role required to create API users.

- [ ] Active Qualys subscription with API access
- [ ] Manager role or higher in Qualys
- [ ] Know your Qualys platform URL (varies by subscription region)
- [ ] Network: Conductor can reach your Qualys API endpoint on port 443

## Step 1: Create API Credentials

1. Log in to the **Qualys Console** at your platform URL
2. Navigate to **Users** (under Administration)
3. Click **Add User** or select an existing user
4. Assign the **API** role to the user
5. Record the **username** and **password**

!!! info "Qualys Platform URLs"
    Qualys uses region-specific platform URLs. Select the correct base URL
    for your subscription:

    | Platform | API URL |
    |----------|---------|
    | US Platform 1 | `qualysapi.qualys.com` |
    | US Platform 2 | `qualysapi.qg2.apps.qualys.com` |
    | US Platform 3 | `qualysapi.qg3.apps.qualys.com` |
    | EU Platform 1 | `qualysapi.qualys.eu` |
    | EU Platform 2 | `qualysapi.qg2.apps.qualys.eu` |
    | India | `qualysapi.qg1.apps.qualys.in` |
    | Canada | `qualysapi.qg1.apps.qualys.ca` |
    | UAE | `qualysapi.qg1.apps.qualys.ae` |

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Qualys**
3. Enter a unique name for this instance
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **Host** | `qualysapi.qualys.com` | Platform API URL (see table above) |
    | **Username** | `<your-username>` | API user from step 1 |
    | **Password** | `<your-password>` | API user password |

5. Set the **Polling Interval** (recommended: 30 minutes)
6. Toggle **Enabled** to on
7. Click **Save**

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "qualys"
    ```

    Look for successful poll messages:
    ```
    [INFO] qualys: fetched host detections
    ```

3. **Check artifacts in Analytics** — Navigate to WitFoo Analytics
   **Signals → Search** and search for artifacts from this source

## Troubleshooting

### Authentication Failed (401)

- Verify the **Username** and **Password** are correct
- Ensure the user has the **API** role assigned in Qualys
- Basic Auth sends credentials as `Base64(username:password)` — special
  characters in passwords are supported

### Forbidden (403)

- The user may lack the required module subscriptions
- Ensure the user has access to the Vulnerability Management module

### Rate Limited (429)

- Qualys enforces a rate limit of approximately 300 requests per hour
- Increase the **Polling Interval** to 60 minutes
- Conductor automatically implements exponential backoff on 429 responses

### Wrong Platform URL

- If you see `404` or connection errors, verify you are using the correct
  platform URL for your subscription region (see table above)
- The URL is **not** the web console URL; it is the API-specific endpoint

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -I https://<your-qualys-api-url>`
- Confirm completed scans exist in Qualys for the polling window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
