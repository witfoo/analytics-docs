# Authentication Settings

Configure LDAP, SAML, and local authentication.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/settings/auth` | `settings:read` | Get auth configuration |
| PUT | `/v1/settings/auth` | `settings:manage` | Update auth configuration |
| POST | `/v1/settings/auth/test` | `settings:manage` | Test auth connection |

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
    "certificate": "..."
  }
}
```

!!! note
    Credentials are encrypted at rest. API responses redact sensitive fields.
