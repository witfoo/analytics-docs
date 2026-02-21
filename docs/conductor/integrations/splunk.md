---
tags:
  - integration
  - siem
---

# Splunk

Collects search results from Splunk via the REST API, providing the ability
to forward Splunk search results into WitFoo Analytics for correlated
analysis alongside other security data sources.

| | |
|---|---|
| **Category** | SIEM |
| **Connector Name** | `signal-client.splunk` |
| **Auth Method** | Token or Username + Password |
| **Polling Interval** | 15 min (search-based) |
| **Multi-Instance** | Yes |
| **Vendor Docs** | [Splunk REST API Reference](https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog) |

## Prerequisites

!!! note "Vendor Requirements"
    Active Splunk Enterprise or Splunk Cloud subscription. Admin access
    required to create API tokens or service accounts.

- [ ] Active Splunk Enterprise or Splunk Cloud deployment
- [ ] Admin or equivalent role to create tokens/users
- [ ] Network: Conductor can reach the Splunk management port (default 8089)

## Step 1: Create API Credentials

=== "Token Authentication (Recommended)"

    1. Log in to the **Splunk Web UI** at `https://<splunk-server>:8000/`
    2. Navigate to **Settings** → **Tokens** (under Data)
    3. Click **New Token**
    4. Configure the token:
        - **User**: Select a user with search permissions
        - **Audience**: `WitFoo Conductor`
        - **Expiration**: Set per your security policy
    5. Copy the generated **Token**

=== "Username/Password Authentication"

    1. Log in to the **Splunk Web UI** at `https://<splunk-server>:8000/`
    2. Navigate to **Settings** → **Access Controls** → **Users**
    3. Click **New User**
    4. Configure the user:
        - **Username**: `witfoo-conductor`
        - **Role**: Assign a role with search permissions (e.g., `user`)
        - **Password**: Set a strong password
    5. Note the **Username** and **Password**

!!! warning "Store Credentials Securely"
    Splunk credentials grant access to your indexed data. Store them securely
    and do not share them in tickets or email.

## Step 2: Configure in Conductor

1. Open the **Conductor UI** at `https://<conductor-ip>/admin/settings/integrations`
2. From the **Add Integration** dropdown, select **Splunk**
3. Enter a unique name for this instance (e.g., "Splunk Production")
4. Fill in the settings form:

    | Field | Value | Description |
    |-------|-------|-------------|
    | **URL** | `https://<splunk-server>:8089` | Splunk REST API endpoint |
    | **Username** | `witfoo-conductor` | Username (if using basic auth) |
    | **Password** | `<password>` | Password (if using basic auth) |
    | **Auth Token** | `<token>` | Bearer token (if using token auth) |
    | **Custom Search** | `index=main earliest=-15m` | Optional: custom SPL query |
    | **Poll Interval** | `15` | Minutes between searches |

5. Toggle **Enabled** to on
6. Click **Save**

!!! tip "Custom Search Queries"
    Leave the **Custom Search** field empty to use the default search, or
    provide a custom SPL query. The query runs on each polling cycle.

## Step 3: Validate Data Flow

After saving, verify the integration is working:

1. **Check connection status** — The integration tile should show a green
   status indicator within 1–2 polling cycles
2. **Check Signal Client logs**:

    ```bash
    docker logs signal-client-svc --tail=50 | grep "splunk"
    ```

    Look for successful poll messages:
    ```
    [INFO] splunk: fetched <N> events
    ```

3. **Check artifacts in Analytics** — Navigate to the WitFoo Analytics
   **Signals → Search** page and search for artifacts from this source

!!! tip "First Poll Timing"
    The first search runs within the configured polling interval after saving.
    For a 15-minute interval, expect results within 15 minutes.

## Troubleshooting

### Authentication Failed (401)

- Verify the credentials (token or username/password) are correct
- For tokens, ensure the token has not expired
- For Splunk Cloud, verify the REST API endpoint is correct

### Forbidden (403)

- The user or token may lack search permissions
- Ensure the user has a role with `search` capability

### Rate Limited (429)

- Increase the **Polling Interval** to 30 minutes
- Conductor automatically implements exponential backoff on 429 responses

### No Data Appearing

- Confirm the integration shows **Enabled** in the Conductor UI
- Check Signal Client logs for errors: `docker logs signal-client-svc --tail=100`
- Verify network connectivity: `curl -k -I https://<splunk-server>:8089`
- Test the search query directly in the Splunk Web UI
- Ensure data exists in the target index for the polling time window

---

*See also: [Integration Catalog](index.md) ·
[Integration Management](../ui/integrations.md) ·
[Signal Client](../signal-client.md) ·
[Common Troubleshooting](common-troubleshooting.md)*
