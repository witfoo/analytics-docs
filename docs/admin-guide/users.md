# Users

Manage user accounts for your WitFoo Analytics deployment. Open **Settings** > **User Management** (the gear icon in the page header).

**User Management** opens only for users who hold the `admin` permission (label **Administrator**), such as the built-in Admin and Platform Admin roles.

## User Properties

| Field | Description |
| --- | --- |
| **Username** | Account name |
| **Email** | Sign-in address (unique) |
| **Name** | First and last name |
| **Roles** | Assigned roles; the user holds the permissions of all of them |
| **Status** | Active or disabled |
| **Last Login** | Most recent sign-in |

## Creating Users

1. Open **Settings** > **User Management**.
2. Click **Create User**.
3. Enter the username, email, first and last name, and a password.
4. Select one or more roles.
5. Click **Save**.

### Email addresses

An email address typed for an account must be one plain address. This applies when an administrator creates or updates a user, at registration, at first-administrator setup and at tenant provisioning. These are refused with a clear message:

- a comment or display name wrapped in extra text
- two addresses
- a trailing comma or semicolon
- a second `@`
- an embedded space or tab
- a `mailto:` prefix
- an IPv6-literal domain
- a `DOMAIN\user` form

A pasted mailbox of the form `Name <user@example.com>` is still reduced to the address. Existing accounts keep signing in and editing as before.

## Editing Users

Click a user row to edit. You can change:

- First and last name, and email
- Assigned roles (**Assign Roles**)
- The password (**Reset Password**)

A user's status is not changed by an edit. Use **Disable** or **Enable** instead.

## Disabling and Enabling Users

Users are disabled, not deleted. In 1.2.0, **Delete** is replaced by **Disable**, and there is no way to delete a user permanently.

- **Disable** keeps the account and its data. A disabled user cannot sign in.
- **Enable** lets a disabled user sign in again.
- You cannot disable or enable your own account. The page says "You cannot disable your own account. Ask another administrator." Another administrator must do it.

Confirmation dialogs with a red confirm button, such as **Disable**, do not run on Enter. Click the confirm button.

### What a disable ends

Disabling a user, or suspending or deleting a tenant, ends that user's existing sessions:

- requests are refused within seconds
- open live connections (Conductor, the graph and event streams, and idle MCP connections) close within a minute

Resetting or changing a user's password ends their sessions in the same way.

### MCP keys

- Disabling a user revokes their personal MCP keys.
- **Enable** revokes any of the user's remaining keys first. If it cannot, the user is not enabled and the page asks you to try again. Keys are never restored: the user creates new ones.
- Resetting or changing a password makes the user's personal MCP keys stop working. The keys are not revoked, so the user's key card keeps listing them as Active until they expire or are revoked.

## Platform administrator accounts

Only a platform administrator can edit, disable, enable, re-role or reset the password of an account that carries the platform-administrator flag or holds a role with a `platform:` permission. Anyone else is refused, and the page says "Only a platform administrator can change this user's status."

## Signed out at upgrade

Upgrading to 1.2.0 signs every user out once. Users sign in again.

## Self-registration

Public self-registration is off by default. When an operator turns it on, accounts are created inactive, and an administrator must use **Enable** before the person can sign in. See [Authentication](settings/authentication.md).

## Default Admin Account

| Field | Value |
| --- | --- |
| Email | `admin@witfoo.com` |
| Password | `F00theN0ise!` |

!!! danger "Change Default Password"
    Change the default admin password immediately after first login.

On a WFA-managed appliance where this account still has the default password, WFA 2.5.1 and later may set it from the **Admin Account** step of `wfa configure`. See [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md).

The default platform user is created only when the users table is empty. Restarting the database leaves existing users as they are.

### Locked out?

If nobody can sign in — a forgotten password, a mistyped email at setup, or a deactivated
account — reset the initial admin account from the appliance command line:

```bash
sudo wfa user-reset
```

It shows the existing account, optionally changes the login email, and sets a new password.
The change takes effect at the next login with no service restart. Run it on an Analytics
appliance (`aio`, `aio-conductor`, `processing`, or `data`); see
[`wfa user-reset`](../conductor/wfa-cli.md) for the full reference.

## Conductor UI and Console UI

The Conductor UI and the Console UI manage their own accounts, with their own rules:

- **Conductor UI:** saving a user as **Inactive** deactivates the account and ends its sessions. Only a Superuser can give an account the Administrator or Superuser role, or deactivate an Administrator or Superuser account. No one can deactivate their own account. See [Conductor UI users](../conductor/ui/users.md).
- **Console UI:** the Users page still offers **Delete**. Only a Superuser can give an account the Org Admin or Superuser role, or delete an Org Admin or Superuser account. No one can delete their own account.
