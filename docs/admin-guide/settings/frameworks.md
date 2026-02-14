# Frameworks

Enable and configure compliance frameworks for the Compliance Readiness report.

## Available Frameworks

| Framework | Description |
| --- | --- |
| **CIS CSC v8** | Center for Internet Security Controls v8 |
| **NIST CSF** | NIST Cybersecurity Framework |
| **Custom** | Frameworks imported via Intel API |

## Enabling Frameworks

1. Navigate to **Admin** > **Settings** > **Frameworks**
2. Toggle frameworks on/off
3. Click **Save**

## Primary Framework

Set one framework as **Primary** for default selection in compliance views:

1. Click the **Primary** radio button next to the desired framework
2. The primary framework is auto-selected in Reporter compliance views

## Framework Sync

Frameworks sync from intel.witfoo.com when `WF_LICENSE` is configured. Without a license, frameworks use locally seeded data.

## Control Structure

Each framework contains controls with:

| Field | Description |
| --- | --- |
| **Control ID** | Unique identifier within the framework |
| **Name** | Human-readable control name |
| **Focus** | Type: computer, user, infrastructure device, or product |
| **Description** | What the control requires |
