# Authentication Settings

Configure LDAP, SAML, and local authentication.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/settings/auth` | `settings:read` | Get auth configuration |
| PUT | `/v1/settings/auth` | `settings:manage` | Update auth configuration |
| POST | `/v1/settings/auth/test` | `settings:manage` | Test auth connection |
| POST | `/v1/admin/settings/auth/saml/test` | `settings:manage` | Test SAML configuration (4 checks) |
| POST | `/v1/admin/settings/auth/saml/generate-keypair` | `settings:manage` | Generate SP signing key pair |
| POST | `/v1/admin/settings/auth/saml/fetch-metadata` | `settings:manage` | Fetch and parse IdP metadata from URL |

## Auth Config Object

```json
{
  "method": "local",
  "ldap": {
    "server_url": "ldaps://ldap.example.com",
    "bind_dn": "cn=admin,dc=example,dc=com",
    "search_base": "ou=users,dc=example,dc=com",
    "user_filter": "(uid=%s)"
  },
  "saml": {
    "entity_id": "witfoo-analytics",
    "sso_url": "https://idp.example.com/sso",
    "slo_url": "https://idp.example.com/slo",
    "certificate": "...",
    "sp_private_key": "...",
    "sp_certificate": "...",
    "provider": "azure_ad",
    "mode": "mixed_saml",
    "attribute_mapping": {
      "email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
      "first_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",
      "last_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"
    }
  }
}
```

!!! note
    Credentials are encrypted at rest. API responses redact sensitive fields (`sp_private_key`, `certificate`).

## SAML Test Endpoint

Test your SAML configuration before saving. Performs 4 validation checks.

### Request

```text
POST /v1/admin/settings/auth/saml/test
Content-Type: application/json
```

```json
{
  "entity_id": "witfoo-analytics",
  "sso_url": "https://login.microsoftonline.com/{tenant}/saml2",
  "certificate": "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----",
  "sp_private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----",
  "sp_certificate": "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----",
  "attribute_mapping": {
    "email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
  }
}
```

### Response

```json
{
  "success": true,
  "checks": [
    {
      "name": "certificate_validity",
      "passed": true,
      "message": "IdP certificate is valid (expires 2027-03-15)"
    },
    {
      "name": "sso_url_reachable",
      "passed": true,
      "message": "SSO endpoint is reachable"
    },
    {
      "name": "sp_keypair_valid",
      "passed": true,
      "message": "SP private key matches SP certificate"
    },
    {
      "name": "attribute_mapping",
      "passed": true,
      "message": "Required attribute 'email' is mapped"
    }
  ]
}
```

## Generate SP Key Pair

Generate a service provider RSA 2048-bit key pair for SAML request signing.

### Request

```text
POST /v1/admin/settings/auth/saml/generate-keypair
```

No request body required.

### Response

```json
{
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----",
  "certificate": "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----"
}
```

!!! warning "Key Security"
    The private key is returned only once. Store it securely or save the SAML configuration immediately.

## Fetch IdP Metadata

Fetch and parse SAML metadata from an identity provider's metadata URL.

### Request

```text
POST /v1/admin/settings/auth/saml/fetch-metadata
Content-Type: application/json
```

```json
{
  "metadata_url": "https://login.microsoftonline.com/{tenant}/federationmetadata/2007-06/federationmetadata.xml"
}
```

### Response

```json
{
  "entity_id": "https://sts.windows.net/{tenant}/",
  "sso_url": "https://login.microsoftonline.com/{tenant}/saml2",
  "slo_url": "https://login.microsoftonline.com/{tenant}/saml2",
  "certificate": "-----BEGIN CERTIFICATE-----\nMIIC...\n-----END CERTIFICATE-----"
}
```
