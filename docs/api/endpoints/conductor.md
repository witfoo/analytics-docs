# Conductor

Manage Conductor feeds, read Conductor integration health, and receive artifacts from Conductors.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/conductor/feeds` | `conductor:read` or `conductor:admin` | List the organization's Conductor feeds |
| GET | `/v1/conductor/feeds/status` | `conductor:read` or `conductor:admin` | Whether feed registration is enabled, with total and pending counts |
| GET | `/v1/conductor/feeds/pending` | `conductor:read` or `conductor:admin` | List pending feeds |
| PUT | `/v1/conductor/feeds/:id/approve` | `conductor:admin` | Approve a pending feed |
| PUT | `/v1/conductor/feeds/:id/reject` | `conductor:admin` | Reject a pending feed |
| DELETE | `/v1/conductor/feeds/:id` | `conductor:admin` | Delete a feed |
| GET | `/v1/conductor/integrations/health` | Any signed-in user | Health of the Conductor's integrations, relayed from the Conductor UI |

An organization holds at most 1,000 pending feeds, and a pending feed expires after 7 days. A decision on a feed that has expired answers `404`. See [Integration Management](../../conductor/ui/integrations.md).

## Artifact Receiver

Conductors send artifacts directly to the Analytics artifact receiver (artifact-ingestion), not through the reverse proxy:

| Method | URL | Authentication | Description |
| --- | --- | --- | --- |
| POST | `https://<analytics-host>:8443/v1/conductor/artifacts/batch` | HMAC-SHA256 signature, checked when `ANALYTICS_SECRET` is set on the receiver | Receive a batch of artifacts from a Conductor |

On an AIO + Conductor appliance the local Conductor uses the internal port 8090. WFA sets the endpoint when it provisions the Conductor.

!!! warning "The `/ingestion/` path is removed"
    The reverse proxy no longer serves the `/ingestion/` path. A Conductor whose artifact endpoint was typed by hand with an `/ingestion/` prefix now receives `404`. Point it at `https://<analytics-host>:8443/v1/conductor/artifacts/batch`. Who may reach the receiver's ports (8090 and 8443) is decided by your firewall and network placement.

### Limits

| Limit | Value |
| --- | --- |
| Artifacts in one batch | 1,000. A larger batch is answered `400` with `batch size exceeds maximum of 1000 artifacts` |
| Largest artifact | 9.5 MiB (9,961,472 bytes) |
| Request line and headers | 12,288 bytes in all. Over it, the receiver answers `431` |
| TLS port | HTTP/1.1 only. A client that offers only HTTP/2 fails its handshake |
| Receiver busy | `503` with `Retry-After: 1`. The exporter waits and sends again |
| Body over the limit | `413` |

## Proxy Routes

Conductor UI requests are proxied through the Analytics reverse proxy at `/conductor/`. JWT tokens are validated and mapped to Conductor roles via the ConductorAuth middleware.

| Analytics Permission | Conductor Role |
| --- | --- |
| `conductor:admin` | Superuser |
| `conductor:write` | Admin |
| `conductor:read` | Staff |

## SAML Configuration Endpoints

These endpoints are available on the conductor-ui backend for SAML SSO configuration. They are served only by a Conductor node that serves its own sign-in page; behind an appliance's Analytics proxy, the Conductor UI does not mount its SAML wizard routes, which answer `404`.

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| POST | `/api/auth/saml/test` | `conductor:admin` | Test SAML configuration by validating IdP metadata and connectivity |
| POST | `/api/auth/saml/generate-keypair` | `conductor:admin` | Generate a new SP (Service Provider) X.509 key pair for SAML signing |

### Test SAML Configuration

```json
POST /api/auth/saml/test
Content-Type: application/json

{
  "idp_metadata_url": "https://idp.example.com/metadata",
  "entity_id": "https://analytics.example.com/saml/metadata"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "SAML configuration is valid",
  "idp_entity_id": "https://idp.example.com",
  "sso_url": "https://idp.example.com/sso"
}
```

### Generate SP Key Pair

```json
POST /api/auth/saml/generate-keypair
```

**Response (200):**

```json
{
  "certificate": "-----BEGIN CERTIFICATE-----\n...",
  "generated_at": "2026-03-12T00:00:00Z"
}
```

!!! note
    The private key is stored server-side and encrypted with `AUTH_CONFIG_ENCRYPTION_KEY`. Only the public certificate is returned in the response.
