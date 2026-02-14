# Permissions

WitFoo Analytics uses a granular permission system with 63 permissions across 11 categories.

## Permission Categories

| Category | Permissions | Description |
| --- | --- | --- |
| **signals** | read, write, manage | Artifact search and incident management |
| **observer** | read, write, manage | Work tracking and observations |
| **reports** | read, write, manage | Reporter module access |
| **frameworks** | read, write, manage | Compliance framework management |
| **cybergrid** | read, write, manage | Threat intelligence operations |
| **health** | read, manage | System health monitoring |
| **metrics** | read | Prometheus metrics access |
| **settings** | read, manage | System configuration |
| **admin** | (grants all) | Full administrative access |
| **ai** | read, write, manage, export | AI assistant features |
| **conductor** | read, write, admin | Conductor pipeline management |

## Permission Hierarchy

```text
manage → write → read
```

Granting `manage` automatically includes `write` and `read`. Granting `write` includes `read`.

## Service-Level Rules

- The `admin` permission grants all permissions in all categories
- Permission checks use constant-time comparison
- Permissions are stored in JWT tokens and validated on each request
