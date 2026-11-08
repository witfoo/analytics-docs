# Admin Users

Manage user accounts, roles, and account status.

## Endpoints

Every `/v1/admin/users` route needs the `admin` permission.

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/admin/users` | `admin` | List the organization's users |
| POST | `/v1/admin/users` | `admin` | Create a user |
| GET | `/v1/admin/users/:id` | `admin` | Get a user and their roles |
| PUT | `/v1/admin/users/:id` | `admin` | Update a user's name or email |
| DELETE | `/v1/admin/users/:id` | `admin` | Disable a user (the account and its data stay) |
| POST | `/v1/admin/users/:id/enable` | `admin` | Enable a disabled user |
| POST | `/v1/admin/users/:id/roles` | `admin` | Assign roles |
| POST | `/v1/admin/users/:id/reset-password` | `admin` | Reset a user's password |
| PUT | `/v1/admin/users/:id/locale` | `admin` | Set a user's locale |
| GET | `/v1/users` | `users:read` | List users, for assignment pickers |

## Disable and enable

`DELETE /v1/admin/users/:id` is a soft disable: the account and its data stay, with `active` set to `false`. There is no hard delete in 1.2.0. `POST /v1/admin/users/:id/enable` enables the account again, and is a no-op for an active user.

| Status | Code | When |
| --- | --- | --- |
| 200 | | The user was disabled or enabled |
| 400 | | The user ID is not valid |
| 403 | `platform_admin_required` | The account carries the platform-administrator flag or holds a role with a `platform:` permission, and the caller is not a platform administrator |
| 404 | | No such user in the caller's organization |
| 409 | `cannot_disable_self` | The caller tried to disable their own account |
| 409 | `cannot_enable_self` | The caller tried to enable their own account |
| 503 | | Enable only: the user's earlier personal MCP keys could not be revoked, so the user was not enabled. Try again |

Disabling a user revokes their personal MCP keys and ends their sessions. Enabling revokes any remaining keys first; keys are never restored.

## Update a user

`PUT /v1/admin/users/:id` changes `first_name`, `last_name` and `email`. A request that changes `active` is refused with `400` and the code `active_not_updatable`; use the disable and enable routes instead. A request that repeats the current status is accepted.

An email address must be one plain address. A request with an address that is blank or not one plain address is refused with `400`.

## User Object

```json
{
  "id": "uuid",
  "username": "jsmith",
  "email": "analyst@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role_ids": ["uuid"],
  "org_id": "example",
  "active": true,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z",
  "last_login": "2026-01-15T10:30:00Z",
  "locale": "en"
}
```

`GET /v1/admin/users` and `GET /v1/admin/users/:id` also return `roles` (the role objects) and `permissions` (the union of the roles' permissions).

## Create a user

```json
{
  "email": "analyst@example.com",
  "username": "jsmith",
  "password": "a-strong-password",
  "first_name": "Jane",
  "last_name": "Smith",
  "role_ids": ["uuid"],
  "active": true
}
```

`email`, `username`, `password` (8 to 72 characters), `first_name`, `last_name` and at least one entry in `role_ids` are required.
