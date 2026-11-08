# User Management & Authentication

## User Management

**URL:** `/admin/users`

The User Management page provides administration of Conductor UI user accounts. On an all-in-one node, the page is reached at `/conductor/admin/users` through the Analytics web UI.

### Creating Users

New users are created with:

- **Username** — The login identifier
- **Password** — For local accounts
- **Display Name** — Shown in the UI
- **Email** — The account's email address
- **Role** — Superuser, Admin, Staff or User
- **Auth Source** — **Local (password)**, **SAML (SSO)** or **LDAP**. The form defaults to Local (password)
- **Is Active** — Whether the account can sign in

### Editing Users

Administrators can modify:

- Display name
- Email address
- Role assignment
- Auth Source
- Is Active

The Users page lists each account's Auth Source in the **Auth Mode** column.

### Who Can Change Whom

- Only a Superuser can give an account the Admin or Superuser role, or deactivate an Admin or Superuser account.
- No one can deactivate their own account.
- A Superuser can edit any account except the one they are signed in to. An Admin can edit only Staff and User accounts.
- The New User and Edit forms offer only the roles the signed-in user may give. A refused change shows the service's message and keeps the form open.

### Deactivating and Reactivating Users

Users are soft-deleted (deactivated) rather than permanently removed. The page provides two tabs:

| Tab | Content |
|-----|---------|
| **Active** | Currently active accounts with pagination |
| **Inactive** | Deactivated accounts that can be reactivated, with separate pagination |

Saving a user as Inactive deactivates the account and ends the sessions it holds. Saving it Active again reactivates it. Inactive users cannot sign in.

## Authentication Modes

The Conductor UI supports four authentication modes, set under **Conductor Admin > Settings > General** in **Authentication Mode**:

| Mode | Description |
|------|-------------|
| **Local** | Users sign in only with their local credentials |
| **Local/LDAP (Mixed)** | Users sign in with their local or LDAP credentials |
| **SAML SSO** | Users sign in only through SAML single sign-on. Local sign-in is disabled |
| **Local/SAML (Mixed)** | Users sign in with their local credentials or through SAML single sign-on |

## SAML Sign-In in 1.2.0

From release 1.2.0, Conductor UI SAML sign-in signs in only accounts whose **Auth Source** is **SAML (SSO)**. An account whose Auth Source is Local or LDAP is refused, and the browser returns to the sign-in page with a generic SSO error.

This applies to a Conductor node that serves its own sign-in page. On an all-in-one node, Analytics signs users in, and this page does not apply.

How SAML sign-in finds the account:

- The account is found by username: the identity provider's username attribute or, when the assertion carries none, the part of the e-mail address before `@`.
- When the identity provider states an e-mail address and the account stores one, the two must match (case is ignored). Otherwise the sign-in is refused.
- A username with no account creates a new SAML account with the Staff role.

!!! danger "Nodes in SAML SSO mode: convert accounts before you upgrade"
    In **SAML SSO** mode the server refuses every local sign-in. After the upgrade, an account left on Local or LDAP cannot sign in at all, a local administrator included. Convert the accounts before you upgrade a node whose Authentication Mode is SAML SSO.

### Before You Upgrade

On each Conductor node whose Authentication Mode is **SAML SSO**:

1. Open **Conductor Admin > Users**.
2. For each Local or LDAP account that signs in through SAML, edit the account, set **Auth Source** to **SAML (SSO)**, and save. Converting an account does not stop it signing in by SAML on the release you are upgrading from.
3. Make the **Email** stored on each of those accounts the address the identity provider asserts for that person. After the upgrade, a sign-in whose stated address differs from the stored address is refused.
4. After each save, check that the account's **Auth Mode** column reads SAML.
5. Deal with the Superuser accounts. The Users page does not let a Superuser change their own Auth Source, so a Superuser account is converted by a different Superuser. If the only Superuser is an account that signs in through SAML, do one of the following:
    - Create a second Superuser with the **SAML (SSO)** Auth Source and the username that SAML sign-in derives for another person. Sign in as that person and convert the first account.
    - Or set **Authentication Mode** to **Local/SAML (Mixed)** until the accounts are converted. In this mode an account that is still Local, and whose password you know, can sign in. Return to **SAML SSO** once the accounts are converted.

To pre-create an account for SAML sign-in, choose **SAML (SSO)** as the Auth Source in the New User form.

!!! note "Converted accounts and passwords"
    An account converted from Local keeps its old password hash, but that password is not accepted while the account's Auth Source is SAML or LDAP, in every mode. Converting the account back to Local makes the old password valid again, so set a new password when you convert an account back.

### If the Node Was Upgraded First

If the node was upgraded before the accounts were converted, and no Superuser or Admin can sign in, the product offers no way back in through the UI. The way back is to change the Conductor UI database on the node:

- The database is the SQLite file `/data/local/collector.db` on the host (`/data/collector.db` inside the Conductor UI container, which has no shell or SQLite client). Confirm the path on your node before you edit it, and back up the file first.
- The edit needs an SQLite client on the host, and normally root.
- Setting an account's `auth_mode` to `saml` in the `users` table converts it, and the change applies at once.
- Setting `auth_mode` to `mixed_saml` in the `system_settings` table allows local sign-in again within 30 seconds, without a restart.
- Setting an account's `auth_mode` back to `local` makes the password hash still in its row valid again. Set a new password afterwards.

## Account Settings

**URL:** `/account`

Individual users can manage their own account:

- **Profile Editing** — Update display name and email
- **Password Change** — Change password (local accounts only)

## Session Management

Sessions are managed via encrypted cookies. The session encryption key is configured via the `SECRET_KEY` environment variable.

!!! warning "`SECRET_KEY` values refused from 1.2.0"
    The Conductor UI refuses to start when `SECRET_KEY` holds a value an earlier release carried, the value the Console's example deployment files showed, or a value that is not a usable key. Before you upgrade, either unset `SECRET_KEY`, so the program keeps a key of its own in `.secret_key` beside its database, or set it to 64 hexadecimal characters (for example the output of `openssl rand -hex 32`). Keep `.secret_key` with the database: without it, the program generates a new key, which ends every session.
