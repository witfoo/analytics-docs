# Admin Users

Manage user accounts, roles, and authentication status.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/users` | `admin` | List all users |
| GET | `/v1/users/:id` | `admin` | Get user details |
| POST | `/v1/users` | `admin` | Create user |
| PUT | `/v1/users/:id` | `admin` | Update user |
| DELETE | `/v1/users/:id` | `admin` | Delete user |

## User Object

```json
{
  "id": "uuid",
  "email": "analyst@example.com",
  "name": "Jane Smith",
  "role_id": "uuid",
  "role_name": "analyst",
  "active": true,
  "last_login": "2026-01-15T10:30:00Z"
}
```
