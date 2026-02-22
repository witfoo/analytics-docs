# SAML SSO Enablement Guide

Configure SAML 2.0 Single Sign-On for WitFoo Analytics, Conductor-UI, and Console-UI.

## Overview

WitFoo supports SAML 2.0 SP-initiated SSO with the following identity providers:

- **Okta**
- **Azure AD (Entra ID)**
- **Google Workspace**
- **OneLogin**
- **PingFederate**
- **Any SAML 2.0 compliant IdP**

Each WitFoo component acts as a SAML Service Provider (SP). Users authenticate at the IdP and are redirected back with a signed SAML assertion.

## Prerequisites

- Administrative access to your Identity Provider
- `settings:manage` permission in WitFoo
- HTTPS configured on WitFoo (required for SAML security)
- IdP metadata URL or XML document

## Architecture

```
User → WitFoo Login → IdP SSO URL → IdP Authentication
                                         ↓
User ← JWT/Session ← WitFoo ACS ← SAML Response (signed)
```

**Security features:**

- XML signature verification on all assertions
- Assertion replay detection (24-hour window)
- Audience restriction validation
- `NotOnOrAfter` / `NotBefore` time-window validation
- SP private key encrypted at rest (AES-256-GCM)

## Step 1: Register WitFoo as a Service Provider

### Gather SP Information

| Property | Analytics | Conductor-UI | Console-UI |
|----------|-----------|-------------|------------|
| **Entity ID** | `https://<analytics-host>/api/v1/auth/saml/metadata` | `https://<conductor-host>/api/v1/auth/saml/metadata` | `https://<console-host>/api/v1/auth/saml/metadata` |
| **ACS URL** | `https://<analytics-host>/api/v1/auth/saml/acs` | `https://<conductor-host>/api/v1/auth/saml/acs` | `https://<console-host>/api/v1/auth/saml/acs` |
| **Name ID Format** | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` | Same | Same |
| **Binding** | HTTP-POST (ACS) | Same | Same |

### IdP-Specific Setup

#### Okta

1. Go to **Applications** > **Create App Integration** > **SAML 2.0**
2. Set **Single sign-on URL** to the ACS URL above
3. Set **Audience URI (SP Entity ID)** to the Entity ID above
4. Configure attribute statements:
    - `email` → `user.email`
    - `firstName` → `user.firstName`
    - `lastName` → `user.lastName`
    - `groups` → (Group attribute statement, filter: regex `.*`)
5. Assign users/groups to the application
6. Copy the **IdP metadata URL** from the Sign On tab

#### Azure AD (Entra ID)

1. Go to **Enterprise Applications** > **New Application** > **Create your own**
2. Select **Integrate any other application (Non-gallery)**
3. Go to **Single sign-on** > **SAML**
4. Set **Identifier (Entity ID)** and **Reply URL (ACS URL)** from the table above
5. Under **Attributes & Claims**, configure:
    - `emailaddress` → `user.mail`
    - `givenname` → `user.givenname`
    - `surname` → `user.surname`
    - `groups` → Group claim (Security groups)
6. Download **Federation Metadata XML** or copy the **App Federation Metadata Url**

#### Google Workspace

1. Go to **Admin Console** > **Apps** > **Web and mobile apps** > **Add custom SAML app**
2. Copy the **IdP metadata** (SSO URL, Entity ID, Certificate)
3. Set **ACS URL** and **Entity ID** from the table above
4. Set **Name ID format** to `EMAIL`
5. Add attribute mappings:
    - `email` → `Primary email`
    - `firstName` → `First name`
    - `lastName` → `Last name`

## Step 2: Configure SAML in WitFoo

### Analytics

1. Navigate to **Admin** > **Settings** > **Authentication**
2. Select the **SAML** tab
3. Enter your **IdP Metadata URL** or paste **IdP Metadata XML**
4. Click **Fetch Metadata** (if using URL) to auto-populate SSO URL and certificate
5. Configure **Attribute Mappings**:
    - Email attribute: `email` (or `emailaddress` for Azure AD)
    - Display name attribute: `displayName` (or `firstName` + `lastName`)
    - Groups attribute: `groups` (optional, for role mapping)
6. Configure **Group-to-Role Mapping** (optional):
    - Map IdP group names to WitFoo roles (e.g., `WitFoo-Admins` → `admin`)
7. Enable **SAML SSO**
8. Click **Save**

### Conductor-UI

1. Navigate to **Admin** > **Settings** > **General**
2. Scroll to the **SAML SSO** section
3. Enter the same IdP metadata URL and attribute mappings
4. Enable SAML and save

### Console-UI

1. Navigate to **Settings** > **Authentication** (superuser only)
2. Select the **SAML** tab
3. Configure identically to Analytics
4. Enable and save

## Step 3: Test SSO

1. Open a new incognito/private browser window
2. Navigate to the WitFoo login page
3. Click **Sign in with SSO**
4. Authenticate at your IdP
5. Verify you are redirected back to WitFoo and logged in

!!! tip "SP Metadata Download"
    Download SP metadata XML from `https://<host>/api/v1/auth/saml/metadata?org_id=<your-org-id>` if your IdP requires it for setup.

## Step 4: Validate Data Flow

After successful login, verify:

- User appears in **Admin** > **Users** with correct email and role
- If group-to-role mapping is configured, the assigned role matches expectations
- The user's display name is populated from SAML attributes

## Attribute Mapping Reference

| WitFoo Field | Common SAML Attributes |
|-------------|----------------------|
| Email | `email`, `emailaddress`, `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` |
| Display Name | `displayName`, `name`, `cn` |
| First Name | `firstName`, `givenname`, `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` |
| Last Name | `lastName`, `surname`, `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` |
| Groups | `groups`, `memberOf`, `http://schemas.xmlsoap.org/claims/Group` |

## Group-to-Role Mapping

Map IdP group names to WitFoo roles for automatic role assignment on login.

| IdP Group (example) | WitFoo Role |
|---------------------|-------------|
| `WitFoo-Admins` | `admin` |
| `WitFoo-Analysts` | `analyst` |
| `WitFoo-Viewers` | `viewer` |
| `SOC-Staff` | `org_staff` |

If no group mapping matches, new users are assigned the default role (`viewer`).

## Troubleshooting

### "SAML response signature verification failed"

- Verify the IdP certificate in WitFoo matches the signing certificate from your IdP
- Check if the IdP rotated its signing certificate
- Re-fetch metadata if using a metadata URL

### "Assertion has expired"

- Ensure server clocks are synchronized (NTP)
- WitFoo allows 5 minutes of clock skew by default

### "Audience mismatch"

- The Entity ID configured in the IdP must exactly match the WitFoo SP Entity ID
- Check for trailing slashes or protocol differences (http vs https)

### "User not found after SSO"

- Verify the email attribute mapping returns a valid email address
- Check that the SAML attribute name in WitFoo matches the attribute name sent by the IdP
- Review the SAML response in browser dev tools (Network tab → ACS POST → form data → `SAMLResponse` → base64 decode)

### "Replay detected"

- This occurs if the same SAML assertion is submitted twice within 24 hours
- Clear browser cache and re-authenticate

### Login page shows no SSO button

- Verify SAML is enabled in the authentication settings
- Ensure the auth mode is set to `saml` (not `local` or `ldap`)

## Security Considerations

- Always use HTTPS for all WitFoo endpoints
- Rotate IdP signing certificates on a regular schedule
- Monitor SAML assertion logs for anomalies
- Use group-based role mapping to enforce least-privilege access
- The SP private key is encrypted at rest using AES-256-GCM; protect the `AUTH_CONFIG_ENCRYPTION_KEY`
