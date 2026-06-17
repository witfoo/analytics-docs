# Configuration Generator

The Configuration Generator is a secure, wizard-driven interface in the WitFoo Console for creating and provisioning initial appliance configurations. It provides a streamlined path for customers to generate custom configurations without direct access to configuration files, with all sensitive data encrypted and protected.

## Overview

The Configuration Generator reduces operational friction by automating the multi-step configuration process through an intuitive web interface. Generated configurations are delivered via secure, single-use URLs that expire after 72 hours, with additional protections including TLS-only transport, rate limiting, and encrypted storage.

### Key Benefits

- **Simplified Workflow:** Replace manual `sudo wfa configure` with a guided web wizard
- **Secure Delivery:** Single-use URLs with 72-hour expiration and TLS encryption
- **Centralized Management:** Administrators create configurations in the Console for remote appliances
- **Audit Trail:** All generated configurations are logged and auditable
- **Error Prevention:** Built-in validation ensures configurations are syntactically correct

### Requirements

- **User Role:** ORG_ADMIN or above (to generate configurations)
- **WFA Version:** 2.2.0 or later
- **Console Access:** Web UI with HTTPS connectivity

## Configuration Wizard

The Configuration Generator guides you through six sequential steps to define your appliance configuration.

### Step 1: Basics

Establish the foundation for your appliance.

**Fields:**

| Field | Type | Example | Required |
| --- | --- | --- | --- |
| Organization Name | Text | `Acme Corporation` | Yes |
| Appliance Name | Text | `analytics-prod-01` | Yes |
| Node Role | Select | Conductor / Analytics / Console | Yes |
| Deployment Type | Select | On-Premises / Cloud / Bare Metal | No |

**Guidance:**
- Use descriptive appliance names that reflect the node's purpose and environment
- Node role selection determines which services are installed and configured
- Appliance names must be unique within your organization

### Step 2: Licensing

Choose your licensing model.

**Options:**

**Trial License (15-day):**
- No license key required
- Automatically generated during configuration
- Expires after 15 days
- Full feature access during trial period
- Use case: Evaluation, proof of concept, testing

**Existing License:**
- Paste your organization's WitFoo license key
- Validates key format and expiration
- Required for production deployments
- Multiple keys can be imported for different appliances

**Selection Process:**
1. Choose **Trial** or **Existing License**
2. For existing licenses, paste the full license key (including `-----BEGIN LICENSE-----` markers)
3. Console validates the key and displays license details: organization, expiration date, feature entitlements
4. If validation fails, you can correct the key or switch to trial mode

### Step 3: Product & Role

Configure role-specific features and integrations.

**For Conductor Nodes:**

| Feature | Options |
| --- | --- |
| Signal Parser | Enable / Disable |
| Parser Catalog | Standard / Extended |
| Artifact Exporter | Enable / Disable |
| Exporters | Splunk / Elasticsearch / Syslog / Custom |

**For Analytics Nodes:**

| Feature | Options |
| --- | --- |
| Data Node (Cassandra) | Primary / Replica / Disable |
| Data Node Commitment | Confirm storage and cluster participation |
| AI/Chat Integration | Enable / Disable |
| Auditor Module | Enable / Disable |
| CyberGrid Integration | Enable / Disable |

**For Console Nodes:**

| Feature | Options |
| --- | --- |
| Authentication Backend | Local / LDAP / Okta |
| High Availability | Single-node / Multi-node cluster |
| Backup Integration | Enable / Disable |

**Selection Process:**
1. Review the available options for your selected node role
2. Enable or disable optional features based on your deployment
3. For integrations, select the relevant platforms you plan to use
4. Proceed to the next step

### Step 4: Network & Features

Define network configuration and optional features.

**Network Configuration:**

| Field | Type | Example | Required |
| --- | --- | --- | --- |
| Appliance Hostname | FQDN | `analytics-01.corp.example.com` | Yes |
| IPv4 Address | IP | `10.20.30.40` | Yes |
| IPv4 Gateway | IP | `10.20.30.1` | Yes |
| IPv4 Netmask | Netmask | `255.255.255.0` | Yes |
| DNS Servers | IP (comma-separated) | `8.8.8.8, 8.8.4.4` | Yes |
| NTP Servers | FQDN (comma-separated) | `ntp.ubuntu.com, ntp1.example.com` | Yes |

**Optional Features:**

| Feature | Description | Impact |
| --- | --- | --- |
| TLS Certificates | Upload custom certificates or use self-signed | Security, trust model |
| HTTP Proxy | For outbound connections in restricted networks | Network connectivity |
| Monitoring | Enable Prometheus metrics export | Observability |
| Syslog Forwarding | Forward logs to centralized syslog server | Operational visibility |
| High Availability | Configure cluster mode (for Console) | Redundancy, failover |

**Configuration:**
1. Enter your network details
2. For security-critical deployments, upload custom TLS certificates
3. Enable monitoring and logging features as needed
4. Configure proxy settings if the appliance is behind an HTTP proxy
5. Proceed to review step

### Step 5: Review

Verify all configuration details before generation.

**Review Checklist:**
- Confirm organization and appliance names
- Verify node role and role-specific features
- Check all network parameters (hostname, IP, gateway, DNS)
- Validate optional features are as intended
- Ensure license is correctly selected

**Actions:**
- **Back:** Return to previous steps to make changes
- **Edit [Step]:** Jump to a specific step to modify details
- **Generate:** Proceed to configuration generation

!!! tip "Configuration Validation"
    The Console performs comprehensive validation during review:
    - Hostname resolves correctly (for on-premises deployments)
    - IP address is valid and not already in use
    - Network parameters are consistent (CIDR notation verified)
    - License is valid and not already assigned
    - No conflicting configurations exist in the organization

### Step 6: Publish

Generate and deliver the configuration via a secure URL.

**Generation Process:**
1. Configuration is encrypted at rest using AES-256-GCM
2. A single-use URL is generated with 72-hour expiration
3. The token is hashed before storage (plaintext not retained)
4. Rate limiting (10 downloads per token) is applied
5. TLS is enforced for all downloads

**Output:**

You receive:
- **Configuration URL:** A secure, single-use link
- **Token Expiration:** Exact time when the URL expires (72 hours)
- **QR Code:** For easy sharing to the target appliance
- **Configuration Checksum:** SHA-256 hash for integrity verification

**Sharing the Configuration:**

```bash
# Option A: Download and scp to target appliance
curl -H "Authorization: Bearer <token>" https://console.example.com/api/config/download/<config-id> > node.json
scp node.json witfooadmin@<target-appliance>:/tmp/

# Option B: Provide customer with URL for automated fetch
# See "Customer Deployment: wfa fetch" below
```

## Security Model

The Configuration Generator implements multiple layers of security to protect sensitive configuration data.

### URL Security

| Layer | Implementation | Benefit |
| --- | --- | --- |
| **Single-Use** | Token valid for exactly one download; subsequent attempts fail | Prevents credential leakage from URL logs |
| **72-Hour TTL** | URL expires automatically; no manual cleanup required | Limits exposure window for compromised URLs |
| **TLS-Only** | HTTP requests are rejected; HTTPS mandatory | Encrypts data in transit |
| **Rate Limiting** | Maximum 10 downloads per token (covers retries/failures) | Prevents brute force enumeration |
| **Rate Limiting (IP)** | Max 100 requests per IP per minute across all endpoints | Prevents DoS attacks |

### Data Protection

| Layer | Implementation | Benefit |
| --- | --- | --- |
| **Encryption at Rest** | AES-256-GCM encryption of configuration files | Protects data if database is compromised |
| **Token Hashing** | Tokens stored as SHA-256 hashes, not plaintext | Even Console administrators cannot retrieve tokens |
| **Admin Password** | Collected locally on appliance, never sent to Console | Admin credentials never traverse network |
| **Audit Logging** | All configuration generation/downloads logged with timestamp and IP | Forensic trail for security reviews |

### Client-Side Security

The appliance retrieves its configuration locally using the secure URL:

1. Appliance downloads configuration file
2. Configuration is verified against provided checksum (SHA-256)
3. Encryption key is derived locally (never transmitted)
4. Configuration file is written to `/witfoo/configs/node.json`
5. WFA daemon validates syntax before activation

## Customer Deployment: wfa fetch

Customers who receive a Configuration Generator URL can deploy it using the `wfa fetch` command.

### Prerequisites

- Fresh appliance with WFA installed
- Network access to the Console (HTTPS port 443)
- SSH access to the appliance

### Step-by-Step Deployment

**1. Receive Configuration URL from Administrator**

The administrator provides:
- Secure configuration URL (valid for 72 hours)
- QR code (optional, for mobile use)
- Configuration checksum (for verification)

Example URL:
```
https://console.example.com/api/config/download/abc123xyz789
```

**2. SSH to the Appliance**

```bash
ssh witfooadmin@<appliance-ip>
```

**3. Run wfa fetch**

```bash
sudo wfa fetch https://console.example.com/api/config/download/abc123xyz789
```

**4. Respond to Prompts**

The `wfa fetch` command prompts for:

| Prompt | Input | Notes |
| --- | --- | --- |
| Admin Email | `admin@example.com` | Default admin account for web UI |
| Admin Password | `SecurePassword123!` | Stored locally; never sent to Console |
| Confirm Network Settings | `yes/no` | Review auto-detected network config |
| Confirm Role & Features | `yes/no` | Verify services to be installed |

**5. Configuration Validation**

The appliance:
- Downloads the configuration file over HTTPS
- Verifies the checksum (SHA-256) matches
- Validates syntax and references
- Applies the configuration
- Starts all services for the selected role

**Sample Output:**

```
$ sudo wfa fetch https://console.example.com/api/config/download/abc123xyz789
Downloading configuration...
Verifying checksum...
Parsing configuration...
Admin Email: admin@example.com
Admin Password: ••••••••••••
Confirm network: eth0 (10.20.30.40/24)? [yes/no] yes
Confirm role: Analytics with data node? [yes/no] yes
Applying configuration...
Starting services...
Configuration applied successfully. Access UI at https://10.20.30.40/
```

**6. Complete Web UI Onboarding**

Once `wfa fetch` completes:
1. Navigate to `https://<appliance-ip>`
2. Log in with the admin email and password from step 4
3. Complete the 12-step onboarding wizard

## Step-by-Step Usage Guide

### For Administrators: Creating a Configuration

1. **Navigate to Configuration Generator**
   - In Console, go to **Admin** > **Configuration**
   - Click **Create New Configuration**

2. **Complete the Wizard**
   - Step 1: Enter organization, appliance name, role
   - Step 2: Choose trial or existing license
   - Step 3: Select role-specific features
   - Step 4: Enter network details and optional features
   - Step 5: Review all settings
   - Step 6: Generate and publish

3. **Distribute the URL**
   - Copy the secure URL or QR code
   - Share with customer or deployment team
   - Communicate expiration time (72 hours)

4. **Track Configuration**
   - Navigate to **Admin** > **Configurations**
   - View list of generated configurations with status
   - See download history and timestamps

### For Customers: Deploying a Configuration

1. **Receive Configuration URL**
   - Administrator provides secure URL and expiration time
   - Verify URL is from trusted Console instance

2. **SSH to Appliance**
   - Deploy a fresh WFA appliance image
   - Connect via SSH as `witfooadmin`

3. **Run wfa fetch**
   - Execute `sudo wfa fetch <url>`
   - Answer prompts for admin credentials and network confirmation
   - Command downloads, validates, and applies configuration

4. **Access Web UI**
   - Open browser to `https://<appliance-ip>`
   - Log in with admin credentials from `wfa fetch`
   - Complete onboarding wizard

5. **Connect to Console**
   - Navigate to **Appliance** > **Console Connection**
   - Follow prompts to establish trust and pair with Console
   - Appliance appears in Console's **Admin** > **Nodes** after pairing

## Security Admonition

!!! warning "Configuration Generator Security Considerations"
    
    - **URL Expiration:** Shared URLs expire after 72 hours. Keep administrative contact information current to ensure timely re-generation if needed.
    
    - **Admin Password:** The appliance collects and stores the admin password locally during `wfa fetch`. The password is never transmitted to the Console. Change this password immediately after first login to the web UI.
    
    - **URL Sharing:** Treat Configuration Generator URLs as sensitive as passwords. Do not share via unencrypted email or public channels. Use encrypted communication or QR codes.
    
    - **Token Hashing:** Even Console administrators cannot retrieve original tokens. If a URL is compromised, request the administrator generate a new one; the old URL automatically expires.
    
    - **Audit Trail:** Enable Console audit logging to track all configuration generations. Review logs periodically for unauthorized access attempts.
    
    - **Air-Gapped Networks:** For disconnected deployments, use the `wfa configure` command instead of `wfa fetch`. Configuration Generator requires HTTPS connectivity to the Console.

## Troubleshooting

### URL Expiration

**Problem:** "This configuration URL has expired"

**Solution:**
1. Contact your administrator
2. Request a new configuration be generated
3. Use the new URL within 72 hours
4. Ensure system clocks are synchronized between Console and appliance

### Checksum Mismatch

**Problem:** "Configuration checksum verification failed"

**Solution:**
1. Verify the configuration URL is correct (copy-paste carefully)
2. Check for network interruptions during download
3. Retry the `wfa fetch` command
4. If problem persists, request a new configuration from administrator

### Network Configuration Errors

**Problem:** "Network configuration invalid: gateway not reachable"

**Solution:**
1. Verify appliance network connectivity: `ping <gateway-ip>`
2. Confirm IP address is not already in use: `arp-scan -l`
3. Check DNS resolution: `nslookup <hostname>`
4. In `wfa fetch`, select "no" at the network confirmation prompt and retry

### TLS Certificate Errors

**Problem:** "Cannot download configuration: certificate validation failed"

**Solution:**
1. Verify Console's TLS certificate is valid and not expired
2. Ensure appliance can reach Console's hostname (DNS resolution)
3. For self-signed certificates, configure appliance to trust the certificate
4. Contact your administrator for certificate troubleshooting

## Related Documentation

- [Admin Guide - Nodes](../admin-guide/nodes.md)
- [Deployment - WFA](../deployment/wfa.md)
- [WFA CLI Reference](../conductor/wfa-cli.md)
- [Deployment Roles](../getting-started/deployment-roles.md)
