# Authentication

Configure authentication methods for WitFoo Analytics. Open **Settings** (the gear icon in the page header) > **General Settings** > **Authentication**. Requires the `settings:manage` permission.

SAML and LDAP settings are saved and read only on this page. The general system settings API (`PUT /api/v1/settings`) neither saves nor returns them.

!!! warning "Encryption Required"
    LDAP bind passwords and SAML private keys are encrypted at rest with XChaCha20-Poly1305, under a per-organization key derived from `AUTH_CONFIG_ENCRYPTION_KEY`. Values written by releases before the cipher change were sealed with AES-256-GCM and are still read. On a WFA-managed appliance WFA supplies the key; do not edit it. On Docker Compose or a standalone stack the key is required from 1.2.0: see [Upgrading to 1.2.0](../../reference/upgrade-1.2.0.md).

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
- **Endpoint**: `POST /api/v1/admin/settings/auth/saml/generate-keypair` (the request names the `entity_id`)
- **Usage**: The generated key pair is used to sign SAML authentication requests sent to the IdP

The generated certificate can be uploaded to your identity provider's service provider configuration.

### IdP Metadata Fetch

If your identity provider publishes a metadata URL, WitFoo can automatically fetch and parse it:

- **Endpoint**: `POST /api/v1/admin/settings/auth/saml/fetch-metadata`
- **Input**: IdP metadata URL
- **Output**: Extracted SSO URL, SLO URL, and X.509 certificate

This eliminates manual copy-paste of IdP configuration values.

### SAML Configuration Test

Before saving, validate your SAML configuration using the built-in test endpoint. The test performs 4 checks:

| Check | Description |
| --- | --- |
| `certificate_valid` | The IdP certificate is PEM, parses as X.509, and has not expired |
| `key_pair_match` | The SP private key matches the SP certificate (or the IdP certificate when no SP certificate is given) |
| `metadata_fetchable` | The IdP metadata URL answers `200`; skipped when no metadata URL is set |
| `sp_build_successful` | A service provider can be built from the configuration |

- **Endpoint**: `POST /api/v1/admin/settings/auth/saml/test`
- **Response**: an overall `status` (`success`, `partial` or `failed`) and a pass/fail result with a message for each check

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

    ```text
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
| **"SAML SSO is not configured properly. Contact your administrator."** | The login flow could not load an *enabled* SAML config for the appliance's organization. Most often: SAML is saved but disabled, the SP secret was overwritten by the redaction placeholder on a re-save, or the appliance predates the org-aware SSO-login resolution | Confirm SAML is **enabled** (auth mode `saml` or `mixed_saml`) and saved; re-save **without re-typing the secrets** (the `***REDACTED***` placeholder is preserved server-side); run the diagnostic at the bottom of the Authentication page; ensure the appliance is on a build with org-aware SSO login (see the note below) |
| **Conductor SSO wizard "Invalid request body" at Test Connection** | A freshly-built wizard config sent empty server-managed timestamps (`created_at`/`updated_at`) the backend could not parse | Update conductor to a build where the SAML config tolerates empty timestamps, then re-run the wizard |

!!! note "SSO login binds to the appliance's primary organization"
    The **diagnostic** validates the SAML config for the *signed-in administrator's* organization, while the unauthenticated **"Sign in with SSO"** button resolves the appliance's **primary organization** (`WF_ORG_ID`). On a single-tenant appliance these are the same, so configure SAML while signed in as an administrator of the primary organization. If the diagnostic passes but SSO login reports "not configured", the appliance likely predates the org-aware login resolution — update to the latest build.

#### Recovering from Lockout

If all users are locked out due to SAML misconfiguration:

1. Access the login page with `?auth_fallback=true` parameter
2. Log in with a local administrator account
3. Open **Settings** > **General Settings** > **Authentication**
4. Switch to `mixed_saml` mode or fix the SAML configuration
5. Run the configuration test to validate before saving

## Platform administrators and single sign-on

From 1.2.0, an organization's SAML identity provider and LDAP directory cannot sign in a platform administrator by default. A platform administrator is an account with the platform-administrator flag, or with a role that holds a `platform:` permission, such as the built-in Platform Admin role. A refused SAML sign-in returns to the login page with "Your account cannot sign in right now. Contact your administrator." Local password sign-in is not affected.

The appliance operator can exempt **one** organization, normally their own, with a file on the node that runs `analytics-api-svc`:

| Setting | Value |
| --- | --- |
| File | `/witfoo/configs/operator-identity-org` |
| Owner and mode | `root:root`, `0644` |
| Content | One organization ID and nothing else |
| Read | Once, when `analytics-api-svc` starts |

To set it, as root on that node:

```bash
printf '%s\n' <org-id> > /witfoo/configs/operator-identity-org
chown root:root /witfoo/configs/operator-identity-org && chmod 0644 /witfoo/configs/operator-identity-org
docker restart analytics-api-svc
docker logs --since 5m analytics-api-svc 2>&1 | grep 'Operator identity organization'
```

When the file is valid, the api logs `Operator identity organization in force` with the organization's ID. A file it cannot use exempts nothing and logs `[ERROR] /configs/operator-identity-org cannot be used`. To remove the exemption, delete the file and restart `analytics-api-svc`.

What the exemption allows:

- **SAML:** the organization's identity provider can sign in its platform administrators, whatever the organization ID is.
- **LDAP:** only when the organization ID equals the first label of the account's mail domain. For example, `holder@example.com` signs in to the organization `example`. For any other organization ID, use SAML for these accounts.
- While the file names an organization, only a platform administrator can change that organization's SAML or LDAP settings. Anyone else is refused with `403` `platform_admin_required`.

## When a person has no account

The analytics server does not create accounts at the first SSO sign-in. A person who signs in through SAML and has no account here, or whose identity provider sends a different email address than the account holds, is told that an administrator must create the account first and that the address must match. Create the account under **Settings** > **User Management** with the same email address the identity provider sends.

## Public self-registration

Public self-registration is off by default. Two environment variables on the api control it:

| Variable | Default | Description |
| --- | --- | --- |
| `AUTH_PUBLIC_REGISTRATION_ENABLED` | `false` | Turns on `POST /api/v1/auth/register`. It gives the same answer whether or not an account is created, and allows 10 requests an hour per client |
| `AUTH_PUBLIC_REGISTRATION_DOMAINS` | (empty) | Comma-separated `<email-domain>=<org_id>` pairs, for example `example.com=acme,corp.example.org=globex` |

How registration behaves in 1.2.0:

- An account is created only when `AUTH_PUBLIC_REGISTRATION_DOMAINS` maps the address's domain to an organization. Domains are matched exactly, with no subdomain or wildcard match.
- The organization a registration request names is ignored. The email domain chooses the organization.
- **Fail-closed:** one malformed entry rejects the whole map. The api logs one `[ERROR]` naming the entry's position, and registration creates no account until the map is fixed.
- The address is not verified, so every account created this way is **inactive**. An administrator must enable it (**Settings** > **User Management** > **Enable**) before the person can sign in.
