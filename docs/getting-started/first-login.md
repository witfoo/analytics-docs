# First Login

After deploying and configuring your WitFoo Appliance, the next step is to access the web UI, change default credentials, and complete the initial setup wizard.

## Default Credentials

!!! danger "Change All Default Passwords Immediately"
    WitFoo Appliances ship with well-known default credentials for both SSH and the web UI. **You must change these passwords immediately after first login.** Failure to do so leaves your deployment vulnerable to unauthorized access.

### SSH Access

| Field | Value |
|-------|-------|
| Username | `witfooadmin` |
| Password | `F00theN0ise!` |

Change the SSH password from the command line:

```bash
passwd witfooadmin
```

### Web UI Access

| Field | Value |
|-------|-------|
| URL | `https://<appliance-ip-or-hostname>` |
| Email | `admin@witfoo.com` |
| Password | `F00theN0ise!` |

---

## Accessing the Web UI

1. Open a web browser and navigate to:

    ```
    https://<appliance-ip-or-hostname>
    ```

    The web UI is served over HTTPS on **port 443**.

2. If the appliance is using a self-signed TLS certificate, your browser will display a security warning. Accept the warning to proceed.

3. Enter the default email and password from the table above and click **Sign In**.

---

## Changing the Admin Password

Immediately after your first login, change the default admin password:

1. Click your **user avatar** or **account name** in the top-right corner of the UI.
2. Select **Account Settings**.
3. Navigate to the **Security** or **Change Password** section.
4. Enter the current password (`F00theN0ise!`), then enter and confirm your new password.
5. Click **Save**.

!!! tip "Password Requirements"
    Use a strong password with at least 12 characters, including uppercase letters, lowercase letters, numbers, and special characters.

---

## Initial Setup Wizard

On first login, WitFoo Analytics launches an **onboarding setup wizard** that guides you through essential configuration. The wizard covers the following steps:

### 1. Organization Details

- **Organization name** — The name of your company or security team.
- **Organization ID** — A unique identifier used internally (auto-generated if not specified).
- **Time zone** — The default time zone for reports and dashboards.

### 2. Admin Account

- Update the default admin email address to your actual email.
- Set a new secure password (if not already changed above).

### 3. Data Sources

- Configure initial log sources and artifact ingestion endpoints.
- Connect syslog forwarders, API integrations, or file-based inputs.

### 4. Retention Policy

- Review and adjust data retention periods:

    | Data Type | Default Retention |
    |-----------|------------------|
    | Artifacts | 7 days |
    | Work Units | 365 days |
    | Work Collections | 365 days |
    | Reports | 1,825 days (5 years) |

### 5. Notification Settings

- Configure email or webhook notifications for incidents and system alerts.

### 6. License Activation

- Enter your WitFoo license key to activate the platform.
- If you are evaluating WitFoo Analytics, you can proceed with the trial license.

### 7. UI Modules

- Select which UI modules to enable:

    | Mode | Modules |
    |------|---------|
    | All | Search, Observer, Reporter, CyberGrid, AI |
    | Search Only | Search |
    | Search + Observer | Search, Observer |

### 8. Review and Finish

- Review all settings and click **Complete Setup**.
- The wizard redirects you to the main dashboard.

---

## Next Steps

After completing the setup wizard:

- **Verify data ingestion** — Navigate to the **Search** module to confirm that artifacts are being received and processed.
- **Explore the dashboard** — The main dashboard provides an overview of incidents, artifacts, and system health.
- **Configure additional users** — Go to **Admin > Users** to create accounts for your security operations team.
- **Review the architecture** — Read the [Architecture](architecture.md) page to understand how data flows through the platform.

!!! tip "Health Dashboard"
    Navigate to **Health** in the main navigation to monitor service status, resource utilization, and pipeline throughput in real time.