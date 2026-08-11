# Users

Manage user accounts for your WitFoo Analytics deployment.

## User Properties

| Field | Description |
| --- | --- |
| **Email** | Login identifier (unique) |
| **Name** | Display name |
| **Role** | Assigned role determining permissions |
| **Status** | Active or Disabled |
| **Last login** | Most recent authentication |

## Creating Users

1. Navigate to **Admin** > **Users**
2. Click **Create User**
3. Enter email, name, and temporary password
4. Select a role
5. Click **Save**

The user must change their temporary password on first login.

## Editing Users

Click a user row to edit. You can change:

- Name and email
- Assigned role
- Account status (active/disabled)

## Deleting Users

Click **Delete** on a user row. Deleted users cannot log in but their historical work data is preserved.

## Default Admin Account

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `F00theN0ise!` |

!!! danger "Change Default Password"
    Change the default admin password immediately after first login.

### Locked out?

If nobody can sign in — a forgotten password, a mistyped email at setup, or a deactivated
account — reset the initial admin account from the appliance command line:

```bash
sudo wfa user-reset
```

It shows the existing account, optionally changes the login email, and sets a new password.
The change takes effect at the next login with no service restart. Run it on an Analytics
appliance (`aio`, `aio-conductor`, `processing`, or `data`); see
[`wfa user-reset`](../conductor/wfa-cli.md#wfa-user-reset) for the full reference.
