# Authentication

Configure authentication methods for WitFoo Analytics. Navigate to **Admin** > **Settings** > **Authentication** to manage these settings. Requires `settings:manage` permission.

!!! warning "Encryption Required"
    LDAP and SAML credentials are encrypted at rest using AES-256-GCM. Set the `AUTH_CONFIG_ENCRYPTION_KEY` environment variable before configuring external authentication.

## Local Authentication

Default method using username/password stored in Cassandra with bcrypt hashing. No external dependencies required.

- Users are created and managed within the WitFoo Admin panel
- Passwords must meet minimum complexity requirements
- Supports password reset via admin action

## LDAP

Connect to an LDAP directory (Active Directory, OpenLDAP) for centralized authentication.

| Setting | Description |
| --- | --- |
| **Server URL** | LDAP server address (`ldap://` or `ldaps://`) |
| **Bind DN** | Distinguished name for LDAP queries |
| **Bind Password** | Password for the bind account |
| **Search Base** | Base DN for user searches |
| **User Filter** | LDAP filter for matching users (e.g., `(uid=%s)`) |

!!! tip "Secure LDAP"
    Use `ldaps://` with a valid TLS certificate for production deployments. WitFoo uses `ldap.DialURL()` which supports TLS configuration.

## SAML

SAML 2.0 single sign-on integration for enterprise identity providers.

### Core Settings

| Setting | Description |
| --- | --- |
| **Entity ID** | Service provider entity ID (unique identifier for WitFoo) |
| **SSO URL** | Identity provider SSO endpoint |
| **SLO URL** | Identity provider Single Logout endpoint (optional) |
| **Certificate** | IdP X.509 certificate for signature validation |
| **SP Private Key** | Service provider private key (for signed requests) |
| **SP Certificate** | Service provider certificate (for signed requests) |
| **Attribute Mapping** | Map SAML attributes to WitFoo user fields (email, name, role) |

### SAML Provider Wizard

The SAML configuration wizard guides administrators through a 7-step setup process with provider-specific presets that pre-populate common settings.

#### Supported Providers

| Provider | Pre-populated Settings |
| --- | --- |
| **Azure AD / Entra ID** | Entity ID format, claim names (`http://schemas.xmlsoap.org/...`), logout URL pattern |
| **Okta** | SSO URL pattern, attribute mapping (firstName, lastName, email), name ID format |
| **OneLogin** | Issuer URL format, SLO endpoint, certificate location guidance |
| **PingIdentity** | Connection URL pattern, attribute contract mappings |
| **Manual** | No defaults -- full manual configuration for any SAML 2.0 IdP |

Each provider preset reduces configuration to entering your organization-specific values (tenant ID, app ID, etc.) while the wizard handles protocol-level defaults.

#### Wizard Steps

1. **Select Provider** -- Choose your identity provider or Manual
2. **IdP Configuration** -- Enter SSO URL, Entity ID, and IdP certificate
3. **SP Configuration** -- Configure service provider settings (auto-generated or manual)
4. **Attribute Mapping** -- Map SAML attributes to WitFoo user fields
5. **Authentication Mode** -- Choose SAML-only or Mixed mode
6. **Key Pair** -- Generate or upload SP signing key pair
7. **Review & Test** -- Validate configuration before saving

### Authentication Modes

| Mode | Value | Description |
| --- | --- | --- |
| **SAML Only** | `saml` | All users authenticate via the identity provider. Local login is hidden. |
| **Mixed (SAML + Local)** | `mixed_saml` | SAML is primary, but local authentication remains available as a fallback. Users see both login options. |

!!! info "Mixed Mode Recommendation"
    Use `mixed_saml` mode during initial SAML deployment. This ensures administrators can still log in with local credentials if SAML configuration issues arise.

### SP Key Pair Generation

WitFoo can automatically generate a service provider key pair for SAML request signing:

- **Algorithm**: RSA 2048-bit
- **Output**: PEM-encoded private key and self-signed X.509 certificate
- **Endpoint**: `POST /v1/admin/settings/auth/saml/generate-keypair`
- **Usage**: The generated key pair is used to sign SAML authentication requests sent to the IdP

The generated certificate can be uploaded to your identity provider's service provider configuration.

### IdP Metadata Fetch

If your identity provider publishes a metadata URL, WitFoo can automatically fetch and parse it:

- **Endpoint**: `POST /v1/admin/settings/auth/saml/fetch-metadata`
- **Input**: IdP metadata URL
- **Output**: Extracted SSO URL, Entity ID, and X.509 certificate

This eliminates manual copy-paste of IdP configuration values.

### SAML Configuration Test

Before saving, validate your SAML configuration using the built-in test endpoint. The test performs 4 checks:

| Check | Description |
| --- | --- |
| **Certificate Validity** | Verifies the IdP certificate is valid, not expired, and properly formatted |
| **SSO URL Reachability** | Confirms the SSO endpoint is reachable via HTTPS |
| **SP Key Pair Consistency** | Validates that the SP private key matches the SP certificate |
| **Attribute Mapping** | Confirms required attributes (email) are mapped |

- **Endpoint**: `POST /v1/admin/settings/auth/saml/test`
- **Response**: `SAMLTestResult` with pass/fail status for each check and descriptive messages

!!! example "Test Before Save"
    Always run the SAML configuration test before saving. A misconfigured SAML setup can lock all users out of the system if running in SAML-only mode.

### SAML Auth Fallback

WitFoo includes automatic redirect loop detection to prevent SAML misconfigurations from locking users out.

**How it works:**

1. On each failed SAML login attempt, a `saml_redirect_count` cookie is incremented (MaxAge: 60 seconds)
2. After **3 failed redirects within 60 seconds**, the system detects a loop
3. The user is redirected to the login page with `?auth_fallback=true`
4. When `auth_fallback=true` is present, the local authentication form is displayed regardless of the SAML-only setting

This fallback mechanism is implemented consistently across all three UI backends (analytics UI, conductor-ui, console-ui).

!!! warning "Fallback URL"
    If SAML is completely broken, navigate directly to:
    ```
    https://your-instance/ui/login?auth_fallback=true
    ```
    This forces the local login form to appear, allowing administrators to log in and fix the SAML configuration.

### Troubleshooting

#### Common SAML Errors

| Error | Cause | Solution |
| --- | --- | --- |
| **Redirect loop** | IdP rejecting authentication requests | Check IdP certificate expiry; verify Entity ID matches IdP configuration |
| **Invalid signature** | Certificate mismatch | Re-download IdP certificate; ensure no whitespace corruption in PEM |
| **Attribute not found** | Missing attribute mapping | Verify IdP sends required attributes (email at minimum); check claim URIs |
| **Clock skew** | Server time difference > 5 minutes | Synchronize NTP on both WitFoo and IdP servers |
| **SP key pair mismatch** | Private key doesn't match certificate | Regenerate the key pair using the built-in generator |

#### Recovering from Lockout

If all users are locked out due to SAML misconfiguration:

1. Access the login page with `?auth_fallback=true` parameter
2. Log in with a local administrator account
3. Navigate to **Admin** > **Settings** > **Authentication**
4. Switch to `mixed_saml` mode or fix the SAML configuration
5. Run the configuration test to validate before saving
