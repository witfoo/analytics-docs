# First Login

After installation, access the WitFoo Analytics web interface to complete initial setup.

## Access the Web UI

Open your browser and navigate to:

```text
http://localhost:8080
```

!!! tip "Remote Access"
    If accessing from a different machine, replace `localhost` with the server's IP address or hostname.

## Default Credentials

| Field | Value |
| --- | --- |
| Username | `admin` |
| Password | `F00theN0ise!` |

!!! danger "Change the Default Password"
    Change the default admin password immediately after first login. The default credentials are published in documentation and should never be used in production.

## Initial Setup

### 1. Change Admin Password

1. Click your username in the top-right corner
2. Select **Profile**
3. Enter a new password (minimum 12 characters recommended)
4. Click **Save**

### 2. Create Additional Users

1. Navigate to **Admin** → **Users**
2. Click **Create User**
3. Enter the user's email, name, and temporary password
4. Assign an appropriate role:

| Role | Use Case |
| --- | --- |
| Admin | Full system access — use sparingly |
| Analyst | Security analysts — search, investigate, report |
| Auditor | Compliance auditors — read-only with report access |
| ReadOnly | Stakeholders — view-only access to dashboards |

See [Roles](../admin-guide/roles.md) for the complete role reference.

### 3. Configure Business Settings

Navigate to **Admin** → **Settings** → **Business Metrics** to configure:

- **Annual Revenue** — Used for security spend percentage calculations
- **Annual Security Spend** — Total security budget
- **FTE Count** — Number of security team members
- **Investigation Time** — Average hours per incident investigation

These settings power the Reporter module's cost/savings analysis.

### 4. Enable Compliance Frameworks

Navigate to **Admin** → **Settings** → **Frameworks** to enable compliance frameworks:

- **CIS CSC v8** — Center for Internet Security Controls
- **NIST CSF** — NIST Cybersecurity Framework
- **Custom frameworks** — Import via the WitFoo Intel API

Set one framework as **Primary** for default compliance views.

## Next Steps

- [Architecture Overview](architecture.md) — Understand the service architecture
- [Signals User Guide](../user-guide/signals/index.md) — Start searching and classifying artifacts
- [Admin Guide](../admin-guide/index.md) — Complete system configuration
