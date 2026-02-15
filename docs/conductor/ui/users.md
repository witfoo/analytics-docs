# User Management & Authentication

## User Management

**URL:** `/admin/users`

The User Management page provides administration of Conductor UI user accounts.

### Creating Users

New users are created with:

- **Email** — Used as the login identifier
- **Display Name** — Shown in the UI
- **Role** — Permission level assignment

### Editing Users

Administrators can modify:

- Display name
- Email address
- Role assignment

### Deactivating and Reactivating Users

Users are soft-deleted (deactivated) rather than permanently removed. The page provides two tabs:

| Tab | Content |
|-----|---------|
| **Active Users** | Currently active accounts with pagination |
| **Inactive Users** | Deactivated accounts that can be reactivated, with separate pagination |

## Authentication Modes

The Conductor UI supports three authentication modes:

| Mode | Description |
|------|-------------|
| **Local Only** | Authentication against the local SQLite database |
| **LDAP Only** | Authentication against an external LDAP/Active Directory server |
| **Mixed** | LDAP authentication with local account fallback |

Authentication mode is configured in the system settings.

## Account Settings

**URL:** `/account`

Individual users can manage their own account:

- **Profile Editing** — Update display name and email
- **Password Change** — Change password (local accounts only)

## Session Management

Sessions are managed via encrypted cookies. The session encryption key is configured via the `SECRET_KEY` environment variable.