# Lead Rules

Lead rules automatically flag artifacts that match specified criteria, surfacing them as potential leads for analyst investigation. Rather than manually searching for patterns, you define the conditions once and let WitFoo Analytics continuously evaluate incoming data against your rules.

## What Is a Lead?

A lead is an artifact that has been flagged by one or more lead rules as potentially significant. When an artifact matches a lead rule, it is marked as a lead and becomes visible in lead-focused views throughout the platform. Leads feed into the incident analysis pipeline, where they may contribute to the creation or escalation of incidents.

## Accessing Lead Rules

Navigate to **Signals > Lead Rules** from the main navigation. This page displays a table of all configured lead rules for your organization.

!!! info "Required Permission"
    Viewing lead rules requires `signals:read`. Creating or editing lead rules requires `signals:write`.

## Lead Rules Table

The lead rules table shows all existing rules with the following columns:

| Column | Description |
|--------|-------------|
| **Name** | A descriptive name for the rule |
| **Description** | A brief summary of what the rule detects |
| **Stream** | Which artifact stream the rule applies to (IDS, auth, firewall, etc.) |
| **Severity** | The severity level assigned to matching leads |
| **Status** | Whether the rule is enabled or disabled |
| **Match Count** | The number of artifacts that have matched this rule |
| **Last Match** | Timestamp of the most recent match |

## Creating a Lead Rule

1. Click the **Create Rule** button in the toolbar
2. Fill in the rule definition form:
    - **Name** -- A clear, descriptive name (e.g., "Brute Force SSH Attempts")
    - **Description** -- What the rule is designed to detect
    - **Stream** -- Select the artifact stream to evaluate (or "All" for cross-stream rules)
    - **Severity** -- The severity level to assign when matched (informational, low, medium, high, critical)
    - **Conditions** -- Define the matching criteria (see below)
3. Click **Save** to create the rule in an enabled state

### Defining Conditions

Conditions specify which artifact fields to evaluate and what values to match. Each condition consists of:

- **Field** -- The artifact field to inspect (e.g., `src_ip`, `dst_ip`, `hostname`, `user`)
- **Operator** -- How to compare the field value (equals, contains, starts with, regex)
- **Value** -- The target value to match against

You can add multiple conditions to a single rule. All conditions must match for the rule to trigger (AND logic).

!!! tip "Use Regex for Complex Patterns"
    The regex operator supports regular expressions for advanced pattern matching. For example, use `user:admin.*` to match any username starting with "admin".

## Editing a Lead Rule

1. Click on a rule row in the table to open the edit form
2. Modify the fields you want to change
3. Click **Save** to apply your changes

Changes take effect immediately. Existing artifacts are not retroactively re-evaluated, but all new incoming artifacts will be checked against the updated rule.

## Enabling and Disabling Rules

Toggle a rule's status to temporarily disable it without deleting the configuration:

1. Click on the rule to open the edit form
2. Toggle the **Enabled** switch
3. Click **Save**

Disabled rules are shown with a dimmed appearance in the table and do not evaluate incoming artifacts.

!!! warning "Disabling vs. Deleting"
    Disable a rule when you want to temporarily stop it. Delete a rule only when you are certain it is no longer needed. Deleted rules cannot be recovered.

## Deleting a Lead Rule

1. Click on the rule to open the edit form
2. Click the **Delete** button
3. Confirm the deletion in the dialog

## How Lead Rules Are Evaluated

When an artifact is ingested:

1. The artifact is classified into a stream by classification rules
2. All enabled lead rules for that stream (and any "All" stream rules) are evaluated
3. If the artifact's fields satisfy all conditions of a rule, the artifact is marked as a lead
4. The lead is tagged with the rule name and assigned the rule's severity
5. Leads flow into the incident analysis pipeline for correlation

Multiple rules can match the same artifact. In this case, the artifact carries all matching lead tags and the highest matched severity applies.

## Best Practices

- **Name rules clearly** -- Use names that describe the threat or behavior being detected, such as "Lateral Movement via RDP" or "DNS Tunneling Indicators"
- **Start broad, then narrow** -- Begin with simple conditions and refine as you observe match volumes
- **Monitor match counts** -- A rule with zero matches may have overly restrictive conditions; a rule with thousands of matches may need tightening
- **Use severity wisely** -- Reserve critical and high severity for rules that detect confirmed threats or policy violations
- **Review regularly** -- Periodically audit your lead rules to retire stale rules and add new ones based on emerging threats

## Relationship to Incidents

Leads generated by lead rules feed into the incident analysis engine. When multiple leads correlate around the same entities (IPs, users, hosts), the system may group them into an incident. The lead rule's severity influences the incident's overall severity assessment.

See the [Observer](../observer/index.md) module for how leads connect to work units and investigations.
