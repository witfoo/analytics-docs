# Authentication

WitFoo Analytics uses JWT (JSON Web Tokens) with HS256 signing for API authentication.

## Login

```text
POST /api/v1/auth/login
```

**Request:**

```json
{
  "email": "admin@witfoo.com",
  "password": "password"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbG...",
    "user": {
      "id": "uuid",
      "email": "admin@witfoo.com",
      "role": "admin"
    }
  }
}
```

## Using Tokens

Include the JWT in the `Authorization` header:

```text
Authorization: Bearer eyJhbG...
```

## Token Contents

| Claim | Description |
| --- | --- |
| `sub` | User ID |
| `email` | User email |
| `org_id` | Organization ID |
| `role` | User role name |
| `permissions` | Array of granted permissions |
| `exp` | Expiration timestamp |

## Token Refresh

Tokens expire after the configured duration (default: 24 hours). Obtain a new token by logging in again.
