# Parser Catalog

WitFoo Conductor includes 200+ log parsers covering a wide range of security products, network infrastructure, operating systems, and cloud platforms. Parsers follow a `vendor-product` naming convention and are organized by category.

## Parsers by Category

### Firewall

| Parser | Description |
|--------|-------------|
| `checkpoint_firewall` | Check Point Firewall (multiple variants for different log types) |
| `checkpoint_firewall_app_control` | Check Point Application Control |
| `checkpoint_firewall_https_inspection` | Check Point HTTPS Inspection |
| `checkpoint_firewall_identity_awareness` | Check Point Identity Awareness |
| `checkpoint_firewall_url_filtering` | Check Point URL Filtering |
| `checkpoint_harmony_email` | Check Point Harmony Email |
| `checkpoint_smart1` | Check Point SmartConsole |
| `cisco_asa` | Cisco ASA Firewall |
| `cisco_pix` | Cisco PIX Firewall |
| `cisco_firepower` | Cisco Firepower Threat Defense |
| `cisco_firepower_discovery` | Cisco Firepower Discovery Events |
| `fortigate` | FortiGate Firewall (general) |
| `fortigate_54` | FortiGate v5.4 |
| `fortigate_56` | FortiGate v5.6 |
| `fortigate_60` | FortiGate v6.0 |
| `pan_firewall` | Palo Alto Networks Firewall |
| `pan_global_protect` | Palo Alto GlobalProtect |
| `pan_threat_log` | Palo Alto Threat Log |
| `pan_user_id` | Palo Alto User-ID |
| `pfsense_firewall` | pfSense Firewall |
| `sonicwall_firewall` | SonicWall Firewall |
| `sophos_firewall` | Sophos Firewall |
| `barracuda_cloudgen_firewall` | Barracuda CloudGen Firewall |
| `vmware_nsx_firewall` | VMware NSX Firewall |

### IDS/IPS

| Parser | Description |
|--------|-------------|
| `suricata` | Suricata IDS/IPS |
| `sfims` | Cisco Sourcefire IPS |
| `tippingpoint_ips` | TippingPoint IPS |
| `ossec` | OSSEC HIDS |
| `security_onion` | Security Onion |
| `firepower` | Cisco Firepower IPS events |

### Authentication

| Parser | Description |
|--------|-------------|
| `sshd` | OpenSSH daemon |
| `pam` | PAM authentication modules |
| `sudo` | sudo command execution |
| `su` | su command execution |
| `auditd` | Linux Audit daemon |
| `cisco_ise` | Cisco Identity Services Engine |
| `cisco_acs` | Cisco Access Control Server |
| `centrify` | Centrify authentication |
| `okta` | Okta (via signal-client) |
| `microsoft_entra_signin` | Microsoft Entra ID sign-in logs |
| `pulse_secure` | Pulse Secure VPN |
| `beyondtrust` | BeyondTrust PAM |
| `senhasegura_pam` | senhasegura PAM |

### DNS and DHCP

| Parser | Description |
|--------|-------------|
| `bind` | ISC BIND DNS |
| `dnsmasq` | dnsmasq DNS |
| `dnsmasq_dhcp` | dnsmasq DHCP |
| `dhcp` | DHCP server |
| `dhclient` | DHCP client |
| `infoblox` | Infoblox DDI |
| `windows_dhcp_server` | Windows DHCP Server |

### Cloud and SaaS

| Parser | Description |
|--------|-------------|
| `aws_cloudtrail` | AWS CloudTrail |
| `aws_cloudwatch` | AWS CloudWatch |
| `aws_guardduty` | AWS GuardDuty |
| `aws_vpc_flow` | AWS VPC Flow Logs |
| `aws_ssm_agent` | AWS Systems Manager Agent |
| `akamai_json` | Akamai security events |
| `crowdstrike_falcon` | CrowdStrike Falcon |
| `microsoft_defender` | Microsoft Defender |
| `zscaler_nss` | Zscaler NSS |
| `netskope` | Netskope (via signal-client) |

### Endpoint Security

| Parser | Description |
|--------|-------------|
| `sentinelone` | SentinelOne |
| `symantec_sep` | Symantec Endpoint Protection |
| `symantec_dlp` | Symantec DLP |
| `mcafee` | McAfee ePO |
| `mcafee_atd` | McAfee ATD |
| `mcafee_epo` | McAfee ePO |
| `mcafee_nsp` | McAfee NSP |
| `trellix_json` | Trellix (JSON format) |
| `trellix_px` | Trellix PX |
| `carbon_black_analytics_json` | Carbon Black Analytics |
| `bit9` | Carbon Black App Control |
| `deep_instinct` | Deep Instinct (via signal-client) |

### Email Security

| Parser | Description |
|--------|-------------|
| `proofpoint` | Proofpoint email security |
| `barracuda_ess` | Barracuda Email Security Service |
| `cisco_ironport` | Cisco IronPort Email |
| `spamtitan` | SpamTitan |
| `sendmail` | Sendmail MTA |
| `postfix` | Postfix MTA |

### Network Infrastructure

| Parser | Description |
|--------|-------------|
| `cisco_os` | Cisco IOS |
| `cisco_csr` | Cisco CSR |
| `cisco_nci` | Cisco NCI |
| `cisco_prime` | Cisco Prime |
| `cisco_wsa` | Cisco Web Security Appliance |
| `cisco_wireless_lan_controller` | Cisco WLC |
| `juniper_srx` | Juniper SRX (multiple variants) |
| `juniper_mgd` | Juniper MGD |
| `meraki` | Cisco Meraki (multiple variants: AP, firewall, flow, VPN, events) |
| `dell_powerconnect` | Dell PowerConnect |
| `netscaler` | Citrix NetScaler |
| `unifi_ap` | Ubiquiti UniFi AP |
| `unifi_dream_machine` | Ubiquiti UniFi Dream Machine |
| `unifi_security_gateway` | Ubiquiti USG |
| `vmware_esxi` | VMware ESXi |
| `vmware_vcenter` | VMware vCenter |
| `f5_apmd` | F5 BIG-IP APM |
| `f5_asm` | F5 BIG-IP ASM |
| `haproxy` | HAProxy |

### Zeek / Corelight

| Parser | Description |
|--------|-------------|
| `zeek` | Zeek/Corelight (JSON and TSV formats) |
| `bro` | Bro IDS (legacy Zeek) |

### Windows

| Parser | Description |
|--------|-------------|
| `windows_event_log` | Windows Event Log (JSON) |
| `windows_event_log_nxlog` | Windows Event Log via NXLog |
| `windows_security_audit_xml` | Windows Security Audit (XML) |
| `windows_security_audit_csv` | Windows Security Audit (CSV) |
| `winlogbeat` | Elastic Winlogbeat |
| `windows_agent` | WitFoo Windows Agent |

### Linux System

| Parser | Description |
|--------|-------------|
| `kernel` | Linux kernel messages |
| `systemd` | systemd journal |
| `ufw` | Uncomplicated Firewall |
| `crond` | Cron daemon |
| `rsyslogd` | rsyslog daemon |
| `syslog_ng` | syslog-ng |
| `fail2ban_actions` | Fail2ban actions |
| `fail2ban_filter` | Fail2ban filter |
| `linux_audit` | Linux audit subsystem |
| `ntpd` | NTP daemon |

## Parser Naming Convention

Parsers follow a `vendor_product` naming convention using lowercase with underscores. Examples:

- `cisco_asa` — Cisco ASA Firewall
- `pan_firewall` — Palo Alto Networks Firewall
- `aws_cloudtrail` — AWS CloudTrail
- `windows_event_log` — Windows Event Log

## Enabling and Disabling Parsers

Parsers can be toggled on or off through the [Conductor UI Parser Management page](ui/parsers.md) or by directly updating the NATS KV `PARSERS` bucket. Changes take effect within seconds without requiring a container restart.