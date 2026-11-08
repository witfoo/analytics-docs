# Admin Guide

The Admin Guide covers system configuration and user management for WitFoo Analytics administrators.

## Sections

### [Users](users.md)

Create, edit, disable and enable user accounts.

### [Roles](roles.md)

Configure role-based access control with predefined and custom roles.

### [Permissions](permissions.md)

Understand the permission system: 108 permissions across 22 categories. The full list is in the [Permissions Reference](../reference/permissions.md).

### [Settings](settings/index.md)

Configure business metrics, compliance frameworks, authentication, notifications, and certificates.

### [Conductor](conductor.md)

Manage the Conductor signal pipeline for log collection.

## Quick Reference

The **Settings** menu is the gear icon in the page header.

| Task | Location |
| --- | --- |
| Create a user | **Settings** > **User Management** > **Create User** |
| Disable or enable a user | **Settings** > **User Management** > **Disable** or **Enable** on the user's row |
| Change a role | **Settings** > **Role Management** |
| Set primary framework | **Settings** > **General Settings** > **Frameworks** |
| Configure SMTP | **Settings** > **General Settings** > **Notifications** |
| Upload TLS cert | **Settings** > **General Settings** > **Certificates** |
| Configure AI and MCP | **Settings** > **General Settings** > **AI Setup** |

**User Management** and **Role Management** appear only for users who hold the `admin` permission (the built-in Admin and Platform Admin roles).
