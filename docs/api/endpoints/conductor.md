# Conductor

Manage the Conductor signal pipeline.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/conductor/status` | `conductor:read` | Pipeline status |
| GET | `/v1/conductor/services` | `conductor:read` | List Conductor services |
| POST | `/v1/conductor/restart` | `conductor:admin` | Restart pipeline |

## Proxy Routes

Conductor UI requests are proxied through the Analytics reverse proxy at `/conductor/`. JWT tokens are validated and mapped to Conductor roles via the ConductorAuth middleware.

| Analytics Permission | Conductor Role |
| --- | --- |
| `conductor:admin` | Superuser |
| `conductor:write` | Admin |
| `conductor:read` | Staff |

## SAML Configuration Endpoints

These endpoints are available on the conductor-ui backend for SAML SSO configuration.

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
