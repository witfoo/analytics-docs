# Authentication

Configure authentication methods for WitFoo Analytics.

## Authentication Methods

### Local Authentication

Default method using username/password stored in Cassandra with bcrypt hashing.

### LDAP

Connect to an LDAP directory (Active Directory, OpenLDAP) for centralized authentication.

| Setting | Description |
| --- | --- |
| **Server URL** | LDAP server address (ldap:// or ldaps://) |
| **Bind DN** | Distinguished name for LDAP queries |
| **Bind Password** | Password for the bind account |
| **Search Base** | Base DN for user searches |
| **User Filter** | LDAP filter for matching users |

### SAML

SAML 2.0 single sign-on integration for enterprise identity providers.

| Setting | Description |
| --- | --- |
| **Entity ID** | Service provider entity ID |
| **SSO URL** | Identity provider SSO endpoint |
| **Certificate** | IdP X.509 certificate for signature validation |
| **Attribute Mapping** | Map SAML attributes to user fields |

## Configuration

Navigate to **Admin** > **Settings** > **Authentication**. Requires `settings:manage` permission.

!!! warning "Encryption Required"
    LDAP and SAML credentials are encrypted at rest using AES-256-GCM. Set `AUTH_CONFIG_ENCRYPTION_KEY` environment variable.
