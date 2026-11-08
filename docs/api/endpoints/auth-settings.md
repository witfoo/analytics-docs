# Authentication Settings

Configure LDAP, SAML, and local authentication.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/admin/settings/auth` | `settings:manage` | Get the organization's auth configuration (secrets redacted) |
| PUT | `/v1/admin/settings/auth` | `settings:manage` | Update the auth configuration |
| POST | `/v1/admin/settings/auth/ldap/test` | `settings:manage` | Test an LDAP connection |
| POST | `/v1/admin/settings/auth/saml/test` | `settings:manage` | Test a SAML configuration (4 checks) |
| POST | `/v1/admin/settings/auth/saml/generate-keypair` | `settings:manage` | Generate an SP signing key pair |
| POST | `/v1/admin/settings/auth/saml/fetch-metadata` | `settings:manage` | Fetch and parse IdP metadata from a URL |
| GET | `/v1/admin/settings/auth/saml/diagnostics` | `settings:manage` | Check the stored SAML configuration |
| GET | `/v1/settings/auth` | none | The sign-in options the login page shows (public) |

SAML and LDAP settings are saved and read only through these routes. `PUT /v1/settings` (the general system settings) neither saves nor returns them.

!!! note "Operator identity organization"
    When the appliance operator has named an organization in `/witfoo/configs/operator-identity-org`, only a platform administrator can change that organization's SAML or LDAP configuration. Anyone else gets `403` with the code `platform_admin_required`. See [Authentication](../../admin-guide/settings/authentication.md).

## Auth Config Object

```json
{
  "org_id": "example",
  "auth_mode": "mixed_saml",
  "ldap": {
    "enabled": false,
    "server_url": "ldaps://ldap.example.com:636",
    "bind_dn": "cn=admin,dc=example,dc=com",
    "bind_password": "***REDACTED***",
    "base_dn": "dc=example,dc=com",
    "user_filter": "(uid=%s)",
    "group_filter": "(memberUid=%s)",
    "tls_enabled": true,
    "tls_skip_verify": false,
    "group_role_map": {}
  },
  "saml": {
    "enabled": true,
    "entity_id": "https://analytics.example.com",
    "sso_url": "https://idp.example.com/sso",
    "slo_url": "https://idp.example.com/slo",
    "certificate": "***REDACTED***",
    "private_key": "***REDACTED***",
    "sp_certificate": "***REDACTED***",
    "name_id_format": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    "attribute_mappings": {
      "email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
      "first_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",
      "last_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"
    },
    "allow_idp_initiated": false,
    "sign_requests": true,
    "want_assertions_signed": true
  }
}
```

`auth_mode` is one of `local`, `ldap`, `saml`, `mixed` (local and LDAP) or `mixed_saml` (local and SAML).

!!! note
    Secrets are encrypted at rest. Responses replace the LDAP bind password, the SAML private key, both SAML certificates and inline IdP metadata with `***REDACTED***`. A `PUT` that sends a secret back as `***REDACTED***` keeps the stored value; if nothing is stored to keep, the request is refused with `400` and asks you to enter the secret.

## SAML Test Endpoint

Test a SAML configuration before saving. It runs 4 checks.

### Request

```text
POST /v1/admin/settings/auth/saml/test
Content-Type: application/json
```

```json
{
  "saml": {
    "entity_id": "https://analytics.example.com",
    "sso_url": "https://login.microsoftonline.com/{tenant}/saml2",
    "certificate": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
    "sp_certificate": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
    "idp_metadata_url": "https://login.microsoftonline.com/{tenant}/federationmetadata/2007-06/federationmetadata.xml"
  }
}
```

### Response

The result is in the response's `data`:

```json
{
  "status": "success",
  "checks": [
    { "name": "certificate_valid", "passed": true, "message": "Valid until 2027-03-15T00:00:00Z" },
    { "name": "key_pair_match", "passed": true, "message": "Private key matches certificate" },
    { "name": "metadata_fetchable", "passed": true, "message": "Metadata URL is accessible" },
    { "name": "sp_build_successful", "passed": true, "message": "Service Provider configuration is valid" }
  ]
}
```

`status` is `success`, `partial` or `failed`. The metadata check is skipped, and passes, when no `idp_metadata_url` is given.

## Generate SP Key Pair

Generate a service provider RSA 2048-bit key pair for SAML request signing.

### Request

```text
POST /v1/admin/settings/auth/saml/generate-keypair
Content-Type: application/json
```

```json
{
  "entity_id": "https://analytics.example.com"
}
```

`entity_id` is required.

### Response

The key pair is in the response's `data`:

```json
{
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
  "certificate": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
}
```

!!! warning "Key Security"
    The private key is returned only once. Store it securely or save the SAML configuration immediately.

## Fetch IdP Metadata

Fetch and parse SAML metadata from an identity provider's metadata URL. The URL must use `http` or `https` and name a host.

### Request

```text
POST /v1/admin/settings/auth/saml/fetch-metadata
Content-Type: application/json
```

```json
{
  "url": "https://login.microsoftonline.com/{tenant}/federationmetadata/2007-06/federationmetadata.xml"
}
```

### Response

The extracted values are in the response's `data`:

```json
{
  "sso_url": "https://login.microsoftonline.com/{tenant}/saml2",
  "slo_url": "https://login.microsoftonline.com/{tenant}/saml2",
  "certificate": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
}
```

## Public self-registration

`POST /v1/auth/register` is off unless the operator sets `AUTH_PUBLIC_REGISTRATION_ENABLED=true`. It then creates an account only when `AUTH_PUBLIC_REGISTRATION_DOMAINS` maps the address's domain to an organization, ignores any organization the request names, and creates the account inactive. It gives the same answer whether or not an account is created. See [Authentication](../../admin-guide/settings/authentication.md).
