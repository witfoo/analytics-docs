---
tags:
  - integration
  - troubleshooting
---

# Common Integration Troubleshooting

This guide covers issues common to all Signal Client pull-based integrations.
For vendor-specific troubleshooting, see the individual
[integration guides](index.md).

## Connection Issues

### Cannot Reach Vendor API

Conductor must have outbound HTTPS (port 443) access to the vendor's API
endpoints. Verify connectivity from the Conductor host:

```bash
# Test basic connectivity
curl -I https://<vendor-api-endpoint>

# If behind a forward proxy
export HTTPS_PROXY=http://proxy:port
curl -I https://<vendor-api-endpoint>
```

If your environment uses a forward proxy, configure it in the Conductor
node settings via `wfa configure`.

### TLS Certificate Errors

If the vendor API endpoint uses a certificate signed by a private CA:

1. Copy the CA certificate to `/witfoo/certs/`
2. Run `sudo wfa configure` and update the CA certificate path
3. Restart Signal Client:

    ```bash
    docker restart signal-client-svc
    ```

### DNS Resolution Failures

If Signal Client logs show DNS errors:

1. Verify the Conductor host can resolve the vendor hostname:

    ```bash
    nslookup <vendor-api-endpoint>
    ```

2. Check `/etc/resolv.conf` for correct upstream DNS servers
3. If using internal DNS, ensure the vendor domain is not blocked

## Authentication Issues

### Token Expired

Most API tokens have expiration dates. If a previously working integration
stops collecting data:

1. Check Signal Client logs for `401` errors:

    ```bash
    docker logs signal-client-svc --tail=100 | grep "401"
    ```

2. Generate a new token in the vendor console
3. Update the credentials in the Conductor UI → Integrations
4. Click **Save** — new credentials take effect within seconds via NATS KV
   watch

### OAuth2 Token Refresh Failures

For OAuth2 integrations (Microsoft, CrowdStrike, Sophos, Wiz, etc.):

- Verify the **Client ID** and **Client Secret** are correct
- Check that the application/service principal has not been deleted
- Confirm required API scopes/permissions are still granted
- Some vendors require admin consent to be re-granted after scope changes

### IP Allowlist

Some vendors restrict API access by source IP address:

1. Determine the Conductor host's public IP
2. Add it to the vendor's API allowlist (often in Settings → API → IP
   Restrictions)
3. If Conductor uses a NAT gateway, add the NAT IP instead

## Rate Limiting

### HTTP 429 Too Many Requests

Signal Client implements automatic exponential backoff on 429 responses.
If you see persistent rate limiting:

1. **Increase the polling interval** — reduces the frequency of API calls
2. **Reduce concurrent integrations** — if many integrations poll the same
   vendor simultaneously
3. **Check vendor rate limits** — each vendor has different quotas:

    | Vendor | Typical Rate Limit |
    |--------|-------------------|
    | CrowdStrike | 100 req/min |
    | Microsoft Graph | 10,000 req/10min |
    | Okta | 600 req/min |
    | Tenable | 300-500 req/min |
    | SentinelOne | 1000 req/min |
    | Qualys | 300 req/hr |

4. Contact the vendor to request a rate limit increase if needed

## Data Issues

### No Artifacts Appearing

1. Verify the integration is **Enabled** in the Conductor UI
2. Check for errors in Signal Client logs:

    ```bash
    docker logs signal-client-svc --tail=100
    ```

3. Verify data exists in the vendor console for the polling time window
4. Check the NATS JetStream stream:

    ```bash
    docker exec broker-edge-svc nats stream info DATA
    ```

5. Confirm Artifact Exporter is running and connected to Analytics:

    ```bash
    docker logs artifact-exporter-svc --tail=50
    ```

### Duplicate Artifacts

WitFoo's ProtoGraph deduplication in the Artifact Filter service automatically
reduces duplicate events. If you see excessive duplicates:

1. Reduce the polling interval to avoid overlapping time windows
2. Check if multiple integration instances are configured for the same
   vendor account
3. Verify checkpoint tracking is working (Signal Client resumes from the
   last successful position)

### Missing Events

If some events appear but others are missing:

1. Check the vendor's data retention settings — some APIs only return recent
   data
2. Verify the API credentials have permissions for all required data types
3. Some integrations collect multiple data types on different schedules
   (e.g., alerts every 5min, assets every 1hr)

## Performance

### High Memory Usage

If Signal Client shows elevated memory usage:

- Reduce the number of concurrent polling integrations
- Increase polling intervals for less critical sources
- Check for vendors that return large batch responses (thousands of records
  per page)

### Slow Polling

Common causes of slow poll cycles:

- **Network latency** to the vendor API endpoint
- **Large data volumes** — consider narrower time windows or more frequent
  polling to keep batch sizes small
- **Vendor API rate limiting** — 429 responses trigger backoff delays
- **DNS resolution delays** — verify DNS is fast from the Conductor host

## Diagnostic Commands

Quick reference for troubleshooting from the Conductor host:

```bash
# Signal Client logs (last 100 lines)
docker logs signal-client-svc --tail=100

# Signal Client logs filtered by integration
docker logs signal-client-svc --tail=200 | grep "<connector-name>"

# Check container health
docker inspect --format='{{.State.Health.Status}}' signal-client-svc

# NATS stream statistics
docker exec broker-edge-svc nats stream info DATA

# Test outbound connectivity to a vendor
curl -sI -o /dev/null -w "%{http_code}" https://<vendor-api-endpoint>

# Check container resource usage
docker stats signal-client-svc --no-stream
```

---

*See also: [Integration Catalog](index.md) ·
[Signal Client](../signal-client.md) ·
[General Conductor Troubleshooting](../troubleshooting.md)*
