# Integration Catalog

WitFoo release 1.1.5 includes **312 integrations** that an operator can enable in the Conductor: 256 parsers, 41 pull connectors, 12 exporters and 3 pipeline processors.

An integration is any of four kinds:

- **Parser**: decodes the logs that devices and applications send to the Conductor (syslog and the other push formats).
- **Pull connector**: collects events from a vendor's API.
- **Exporter**: sends WitFoo's artifacts to another system.
- **Pipeline processor**: filters or enriches artifacts on their way through the Conductor.

This catalog is generated from the registries of release 1.1.5 itself and lists what an operator can switch on in the Conductor UI. It is regenerated for every release; a count anywhere else in this documentation follows it.

## Pull connectors (41)

| Connector | What it collects |
| --- | --- |
| 1Password Events | The 1Password Events connector allows you to fetch sign-in attempts, item usage events, and (opt-in) team audit events from 1Password. |
| Abnormal Security | The Abnormal Security connector allows you to fetch threat alerts and account compromise events, with optional Portal Posture Monitoring (portal users, roles, security settings, API-token inventory). |
| Arista AGNI | The Arista AGNI connector allows you to fetch network security alerts from Arista AGNI. |
| Auth0 | The Auth0 connector allows you to fetch authentication and identity management logs. |
| AWS GuardDuty | The AWS GuardDuty connector allows you to fetch threat detection findings from AWS GuardDuty. |
| AWS Security Hub | The AWS Security Hub connector allows you to fetch consolidated security findings from AWS Security Hub. |
| Azure Security | The Azure Security connector allows you to fetch alerts from Azure. |
| Carbon Black | The Carbon Black connector allows you to fetch endpoint security alerts from VMware Carbon Black Cloud. |
| Cisco AMP | The Cisco AMP (Secure Endpoint) connector fetches events from the v1 API and, optionally, devices, vulnerabilities and audit logs from the v3 API. |
| Cisco Duo | The Cisco Duo connector allows you to fetch alerts from Cisco Duo. |
| Cisco Meraki | The Cisco Meraki connector allows you to fetch alerts from Cisco Meraki. |
| Cisco Secure Access | The Cisco Secure Access connector pulls Reporting API activity (DNS, web proxy, firewall, intrusion, ZTNA, decryption) and optionally Alerts from api.sse.cisco.com — the replacement feed for tenants migrating off Cisco Umbrella. |
| Cisco Umbrella | The Cisco Umbrella connector allows you to fetch alerts from Cisco Umbrella. |
| CrowdStrike Falcon | The CrowdStrike Falcon connector allows you to fetch alerts from CrowdStrike Falcon. |
| CyberArk EPM | The CyberArk EPM connector allows you to fetch endpoint privilege management events. |
| Darktrace | The Darktrace connector allows you to fetch AI-driven threat detection alerts from Darktrace. |
| Deep Instinct | The Deep Instinct connector allows you to fetch alerts from Deep Instinct. |
| DNS Zone Transfer | The DNS Zone Transfer connector allows you to transfer DNS zones from a specified DNS server. Ensure that the DNS server supports zone transfers. |
| Druva | The Druva connector pulls Cyber Resilience (Realize) events from Druva, with an optional Threat Watch IOC Sets feed. |
| FortiAnalyzer | The FortiAnalyzer connector allows you to fetch security analytics and log data from Fortinet FortiAnalyzer. |
| Google Cloud SCC | The Google Cloud Security Command Center connector allows you to fetch security findings from Google Cloud. |
| Halcyon | The Halcyon connector allows you to fetch anti-ransomware protection alerts from Halcyon. |
| LevelBlue USM Anywhere | The LevelBlue USM Anywhere connector pulls alarms and events from the USM Anywhere platform API (formerly AT&T Cybersecurity / AlienVault). |
| LimaCharlie | The LimaCharlie connector allows you to fetch alerts from LimaCharlie. |
| Microsoft Sentinel | The Microsoft Sentinel connector allows you to fetch security incidents from a Microsoft Sentinel workspace via the Azure Management API. Workspaces onboarded to the Microsoft Defender portal (retiring the Azure portal experience by 2027-03-31) can also be served by the Azure Security integration, Microsoft |
| Mimecast | The Mimecast connector allows you to fetch alerts from Mimecast. |
| MS Defender Vulnerability Mgmt | Pulls per-device software vulnerabilities (CVEs) from Microsoft Defender Vulnerability Management (MDE API). Same app registration as Azure Security; additionally requires the WindowsDefenderATP |
| Netskope | The Netskope connector allows you to fetch alerts from Netskope. |
| Okta | The Okta connector allows you to fetch alerts from Okta. |
| PAN Cortex | The PAN Cortex connector allows you to fetch alerts from PAN Cortex. |
| Proofpoint CASB | The Proofpoint CASB connector allows you to fetch alerts from Proofpoint CASB. |
| Proofpoint Protect | The Proofpoint Protect connector allows you to fetch alerts from Proofpoint Protect. |
| Qualys | The Qualys connector allows you to fetch vulnerability management and compliance data from Qualys. |
| Rapid7 InsightIDR | The Rapid7 InsightIDR connector allows you to fetch detection and investigation data from Rapid7 InsightIDR. |
| SentinelOne | The SentinelOne connector allows you to fetch endpoint security threats and alerts from SentinelOne. |
| Sophos Central | The Sophos Central connector allows you to fetch security alerts, endpoint inventory, and (opt-in) administrative audit events from Sophos Central. |
| Splunk | The Splunk connector allows you to send data to a Splunk instance. Ensure that the Splunk HTTP Event Collector (HEC) is enabled and configured to accept data. |
| Stealthwatch | The Stealthwatch connector allows you to send data to a Cisco Stealthwatch instance. Ensure that the Stealthwatch API is enabled and accessible. |
| Tenable | The Tenable connector allows you to send data to a Tenable instance. Ensure that the Tenable API is enabled and accessible. |
| Wiz | The Wiz connector allows you to fetch cloud security findings and issues from Wiz. |
| Zscaler ZIA | The Zscaler ZIA connector allows you to fetch web security logs and alerts from Zscaler Internet Access. |

## Exporters (12)

| Exporter | What it does |
| --- | --- |
| Azure Blob Storage | Export artifacts to Azure Blob Storage. Batches artifacts as compressed NDJSON blobs with time-based partitioning and configurable access tiers. |
| CrowdStrike Falcon Next-Gen SIEM | Export artifacts to CrowdStrike Falcon Next-Gen SIEM through a HEC / HTTP Event Data Connector. Batches events as HEC JSON and authenticates with the data connector API key. |
| Google Cloud Storage | Export artifacts to Google Cloud Storage. Batches artifacts as compressed NDJSON objects with time-based partitioning and configurable storage classes. |
| Local Filesystem | The Local Filesystem exporter allows you to accumulate data into a file up to a size limit and save files to another directory/mount on the same machine. Ensure that the target path is accessible and writable by the application. |
| Microsoft Sentinel | The Microsoft Sentinel exporter allows you to send data to a Microsoft Sentinel workspace via Data Collector API. Ensure that you have the necessary permissions and configurations in your Azure environment. |
| OpenSearch | The OpenSearch exporter allows you to send data to an OpenSearch endpoint. |
| S3 Object Storage | Export artifacts to S3-compatible object storage (AWS S3, MinIO, Cloudflare R2, Backblaze B2, Wasabi, DigitalOcean Spaces). Batches artifacts as compressed NDJSON objects with time-based partitioning. |
| SCP Transfer | The SCP Transfer exporter allows you to accumulate data into a file up to a size limit and securely transfer files over SSH. Ensure that the target server is configured to accept SCP connections. |
| Splunk | The Splunk exporter allows you to send data to a Splunk HEC Event Collector endpoint. |
| UDP Syslog | The UDP Syslog exporter allows you to export data to a UDP syslog server. |
| USM Anywhere | Export artifacts via webhook to LevelBlue USM Anywhere (formerly AlienVault). Sends batched JSON with gzip compression to the webhook API. |
| WitFoo Analytics | Export artifacts to a WitFoo Analytics appliance over a secure WebSocket (TLS) connection. Enter the Analytics host and ingestion port to connect. |

## Pipeline processors (3)

| Processor | What it does |
| --- | --- |
| ProtoGraph Processor | ProtoGraph filtering samples against a ten-tuple of values to reduce noise and ensure high-quality analytic sampling. |
| Redaction Processor | Tokenizes PII (credit cards, SSNs, emails, custom regex) before artifacts are exported. Optionally maintains an exportable alias map of the original ↔ redacted values. |
| STIX Threat Intelligence | Enriches artifacts with threat intelligence from STIX/TAXII feeds. Matched artifacts are tagged with indicator IDs and ATT&CK technique references. |

## Parsers (256)

| Parser | Identifier | Description |
| --- | --- | --- |
| AD Audit Plus | `ad_audit_plus` | AD Audit Plus logs |
| Agetty | `agetty` | Agetty logs |
| Akamai | `akamai` | Akamai logs |
| Anacron | `anacron` | Anacron logs |
| Apache | `apache` | Apache HTTP Server logs |
| Apache Access Log | `apacheaccesslog` | Apache Access logs |
| Apache Authz | `apacheauthz` | Apache Authorization logs |
| Apache SSL | `apachessl` | Apache SSL logs |
| Arista WIPS Sensor | `arista_wips_sensor` | Arista WIPS sensor / AP device logs: sensord cloud uplink, CLI audit, and client Wi-Fi session events (AirTight SpectraGuard / Mojo lineage) |
| Arista Wireless | `arista_wireless` | Arista Wireless logs |
| Aristaflowcontrol | `aristaflowcontrol` | Aristaflowcontrol logs |
| Attaris Gateway | `attarrisgateway` | Attaris Gateway logs |
| AudioCodes Mediant | `audiocodesmediant` | AudioCodes Mediant logs |
| Auditd | `auditd` | Linux Auditd logs |
| Auditd Log | `auditdlog` | Auditd Log logs |
| AWS CloudTrail | `aws_cloud_trail` | AWS CloudTrail logs |
| AWS CloudWatch | `aws_cloudwatch` | AWS CloudWatch logs |
| AWS GuardDuty | `awsguardduty` | AWS GuardDuty logs |
| AWS SSM | `aws_ssm` | AWS SSM logs |
| AWS VPC Flow | `aws_vpc_flow` | AWS VPC Flow logs |
| Barracuda CloudGen | `barracuda_cloudgen` | Barracuda CloudGen logs |
| Barracuda ESS | `barracuda_ess` | Barracuda Email Security Service logs |
| Barracuda WAF | `barracudawaf` | Barracuda Web Application Firewall logs |
| Barracuda WAF RFC Logs | `barracuda_waf_rfc` | Barracuda Web Application Firewall logs (RFC format) |
| Beyond Trust | `beyond_trust` | Beyond Trust logs |
| Beyond Trust LWSMD | `beyond_trust_lwsmd` | Beyond Trust LWSMD logs |
| BIND | `bind` | BIND DNS server logs |
| Bit9 | `bit9` | Bit9 logs |
| Broadcom Driver | `broadcomdriver` | Broadcom Driver logs |
| Caprica | `caprica` | Caprica logs |
| CarbonBlack | `carbonblack` | CarbonBlack logs |
| CAS | `cas` | Central Authentication Service (CAS) logs |
| Cellular AP | `cellular_ap` | Cellular Access Point logs |
| Centrify | `centrify` | Centrify logs |
| Checkpoint Firewall | `checkpoint_firewall` | Checkpoint Firewall logs |
| Checkpoint Firewall 2 | `checkpointfirewall2` | Checkpoint Firewall 2 logs |
| Checkpoint Firewall 3 | `checkpoint_firewall_3` | Checkpoint Firewall 3 logs |
| Checkpoint Firewall 4 | `checkpointfirewall4` | Checkpoint Firewall 4 logs |
| Checkpoint Firewall AppControl | `checkpoint_firewall_appcontrol` | Checkpoint Firewall AppControl logs |
| Checkpoint Firewall HTTPS Inspection | `checkpoint_firewall_https_inspection` | Checkpoint Firewall HTTPS Inspection logs |
| Checkpoint Firewall Identity Awareness | `checkpoint_firewall_identity_awareness` | Checkpoint Firewall Identity Awareness logs |
| Checkpoint Firewall URL Filtering | `checkpoint_firewall_url_filtering` | Checkpoint Firewall URL Filtering logs |
| Checkpoint Harmony Email | `checkpoint_harmony_email` | Checkpoint Harmony Email logs |
| Checkpoint Smart1 | `checkpoint_smart1` | Checkpoint Smart1 logs |
| ChronyD | `chronyd` | ChronyD logs |
| Cisco ACE | `cisco_ace` | Cisco Application Control Engine logs |
| Cisco ACS | `cisco_acs` | Cisco Access Control Server logs |
| Cisco AP Watchdog | `ciscoapwatchdog` | Cisco access-point watchdog stats and restart-reason telemetry |
| Cisco ASA | `cisco_asa` | Cisco Adaptive Security Appliance logs |
| Cisco CSR | `cisco_csr` | Cisco Cloud Services Router logs |
| Cisco Firepower | `ciscofirepower` | Cisco Firepower logs |
| Cisco Firepower Discovery | `cisco_firepower_discovery` | Cisco Firepower Discovery logs |
| Cisco IronPort | `cisco_ironport` | Cisco IronPort logs |
| Cisco ISE | `ciscoise` | Cisco Identity Services Engine logs |
| Cisco NCI | `cisconci` | Cisco Network Control Interface logs |
| Cisco NetFlow | `cisco_netflow` | Cisco NetFlow logs |
| Cisco OS | `cisco_os` | Cisco OS logs |
| Cisco PIX | `cisco_pix` | Cisco PIX Firewall logs |
| Cisco Prime | `cisco_prime` | Cisco Prime logs |
| Cisco Stealthwatch | `stealth_watch` | Cisco Stealthwatch logs |
| Cisco VCS | `cisco_vcs` | Cisco VCS logs |
| Cisco WLAN Controller | `cisco_wireless_lan_controller` | Cisco Wireless LAN Controller logs |
| Cisco WSA | `cisco_wsa` | Cisco Web Security Appliance logs |
| CloudInit | `cloud_init` | CloudInit logs |
| CMAEventD | `cmaeventd` | CMAEventD logs |
| Connection ID | `connectionid` | Connection ID logs |
| Containerd | `containerd` | Containerd logs |
| Crond | `crond` | Crond logs |
| CrowdStrike Falcon | `crowdstrikefalcon` | CrowdStrike Falcon logs |
| Cups LPD | `cupslpd` | Cups LPD logs |
| Custom Artifact | `custom_artifact` | Custom Artifact logs |
| Datto Network Manager Audit | `datto_network_manager_audit` | Datto Network Manager Audit logs |
| DBus | `dbusdaemon` | DBus logs |
| Dell PowerConnect | `dellpowerconnect` | Dell PowerConnect logs |
| Device Unreachable | `device_unreachable` | Device Unreachable logs |
| DHClient | `dhclient` | DHClient logs |
| DHCP | `dhcp` | DHCP logs |
| Dnsmasq | `dnsmasq` | Dnsmasq logs |
| Dnsmasq DHCP | `dnsmasqdhcp` | Dnsmasq DHCP server logs (DHCPREQUEST, DHCPACK, DHCPDISCOVER, etc.) |
| Docker Compose | `docker-compose` | Docker Compose logs |
| Dockerd | `dockerd` | Dockerd logs |
| DPKG | `dpkg` | Debian Package logs |
| Drupal | `drupal` | Drupal logs |
| Ericsson Security Manager | `ericssonsecuritymanager` | Ericsson Security Manager logs |
| F5 APMD | `f5apmd` | F5 APMD logs |
| F5 ASM | `f5asm` | F5 Application Security Manager logs |
| F5 GTMD | `f5gtmd` | F5 GTMD logs |
| F5 HTTPD | `f5httpd` | F5 HTTPD logs |
| F5 HTTPD Auth Cache | `f5httpdauthcache` | F5 HTTPD Auth Cache logs |
| F5 Logger | `f5logger` | F5 Logger logs |
| F5 MCPD | `f5mcpd` | F5 MCPD logs |
| F5 PAM Audit | `f5pamaudit` | F5 PAM Audit logs |
| F5 TMM | `f5tmm` | F5 TMM logs |
| Fail2Ban Actions | `fail2banactions` | Fail2Ban Actions logs |
| Fail2Ban Filter | `fail2banfilter` | Fail2Ban Filter logs |
| FortiGate | `fortigate` | FortiGate firewall logs |
| General | `general` | General log formats |
| General Info | `general_info` | General informational logs |
| Generic Log | `generic_log` | Generic Log logs |
| Getty | `getty` | Getty logs |
| GIN Access Log | `ginaccesslog` | GIN Access logs |
| HAProxy | `haproxy` | HAProxy logs |
| Hostapd | `hostapd` | Hostapd logs |
| HPE Nimble | `hpe_nimble` | HPE Nimble Storage logs |
| HTTP Access Log | `httpaccesslog` | HTTP Access logs |
| HTTPD | `httpd` | HTTPD logs |
| Imperva SecureSphere | `imperva_secure_sphere` | Imperva SecureSphere logs |
| Infoblox | `infoblox` | Infoblox logs |
| Java | `java` | Java logs |
| Java Exception | `javaexception` | Java Exception logs |
| Java Stack Trace | `javastacktrace` | Java Stack Trace logs |
| Juniper MGD | `juniper_mgd` | Juniper MGD logs |
| Juniper SRX | `juniper_srx` | Juniper SRX firewall logs |
| Kernel | `kernel` | Linux kernel logs |
| Lantronix Local Manager | `lantronix_local_manager` | Lantronix (Uplogix) Local Manager out-of-band console manager reachability reports |
| LevelBlue USM Anywhere | `usm_anywhere` | LevelBlue (AlienVault) USM Anywhere alarms and events (API pull records) |
| Linux Audit | `linux_audit` | Linux Audit logs |
| McAfee | `mcafee` | McAfee logs |
| McAfee EPO | `mcafeeepo` | McAfee EPO logs |
| McAfeeATD | `mcafeeatd` | McAfeeATD logs |
| McAfeeNSP | `mcafeensp` | McAfeeNSP logs |
| Meraki | `meraki` | Meraki logs |
| Meraki Firewall | `merakifirewall` | Meraki Firewall logs |
| Meraki L7 Firewall | `merakil7firewall` | Meraki L7 Firewall logs |
| Message Repeats | `messagerepeats` | Message Repeats logs |
| Microsoft Defender Incident | `microsoft_defender_incident` | Microsoft 365 Defender security incidents (Graph security/incidents) |
| Microsoft Entra Directory Audit | `microsoft_directory_audit` | Microsoft Entra ID directory audit logs (Graph directoryAudits) |
| Microsoft Entra Inventory | `microsoft_entra_inventory` | Microsoft Entra ID user & registered-device inventory |
| Microsoft Entra Sign-In | `microsoft_entra_signin` | Microsoft Entra ID Sign-In logs |
| Microsoft Intune | `microsoft_intune` | Microsoft Intune managed-device & detected-app inventory (CSC8 2/4) |
| Microsoft Secure Score | `microsoftsecurescore` | Microsoft Graph security secureScores posture snapshots |
| MS Defender Office365 | `microsoft_defender_office365` | Microsoft Defender Office365 logs |
| MS Defender Vuln Mgmt | `microsoft_defender_vuln` | Microsoft Defender Vulnerability Management per-device CVE assessment rows (CSC8 control 7) |
| Multipart Message | `multipartmessage` | Multipart Message logs |
| Multipathd | `multipathd` | Multipathd logs |
| Netfilter | `netfilter` | Netfilter logs |
| Netscaler | `netscaler` | Netscaler logs |
| NetworkManager | `networkmanager` | NetworkManager logs |
| NTPD | `ntpd` | Network Time Protocol Daemon logs |
| Okta | `okta` | Okta System Log identity events and user-directory records (API pull / raw JSON) |
| OpenSSH SFTP | `opensshsftp` | OpenSSH sftp-server subsystem file-transfer and session logs |
| OpenVPN | `openvpn` | OpenVPN logs |
| OPNsense Firewall | `opnsense_firewall` | OPNsense Firewall logs |
| OPNsense Firewall Status | `opnsense_firewall_status` | OPNsense Firewall Status logs |
| OSSEC | `ossec` | OSSEC logs |
| Paessler PRTG | `paessler_prtg` | Paessler PRTG logs |
| Palo Alto Cortex XDR | `cortex_xdr` | Palo Alto Cortex XDR endpoint detection alerts (pulled via the Cortex XDR API) |
| Palo Alto Firewall | `panfirewall` | Palo Alto Networks firewall logs |
| Palo Alto GlobalProtect | `panglobalprotect` | Palo Alto Networks GlobalProtect logs |
| Palo Alto Threat Log | `panthreatlog` | Palo Alto Networks Threat logs |
| PAM | `pam` | Pluggable Authentication Module (PAM) logs |
| PanUserID | `panuserid` | PanUserID logs |
| PFSense Firewall | `pfsensefirewall` | PFSense Firewall logs |
| PHP Log | `phplog` | PHP application logs |
| Ping Identity | `ping_identity` | Ping Identity PingFederate security audit log (pipe-delimited audit.log) |
| Pluribus Netvisor ONE | `netvisor_one` | Pluribus Netvisor ONE logs |
| Postfix | `postfix` | Postfix mail server logs |
| PostgreSQL | `postgres` | PostgreSQL database logs |
| Precinct | `precinct` | Precinct logs |
| Proofpoint | `proofpoint` | Proofpoint logs |
| Pulse Secure | `pulse_secure` | Pulse Secure logs |
| Qualcomm WLAN AP | `qualcommwlanap` | Qualcomm-based WiFi Access Point logs (Netgear Insight, band steering, configd, nddmp, cloudAgent) |
| Radware WAF | `radware_waf` | Radware WAF logs |
| Roqos | `roqos` | Roqos logs |
| RPC Mountd | `rpc_mountd` | RPC Mountd logs |
| Rsyslogd | `rsyslogd` | Rsyslogd logs |
| Ruby | `ruby` | Ruby stdlib Logger output (Rails, Sidekiq, OCI unified-monitoring-agent, etc.) |
| SAP SMP | `sap_smp` | SAP SMP logs |
| SecureCircle | `securecircle` | SecureCircle logs |
| Security Onion | `security_onion` | Security Onion logs |
| Senhasegura | `senhasegura` | Senhasegura logs |
| SentinelOne | `sentinelone` | SentinelOne logs |
| SFIMS | `sfims` | Sourcefire/Intrusion Management System logs |
| Silverfort | `silverfort` | Silverfort identity-protection authentication (CEF) |
| SNMPD | `snmpd` | SNMPD logs |
| SonicWall Firewall | `sonicwallfirewall` | SonicWall Firewall logs |
| Sophos Firewall | `sophosfirewall` | Sophos Firewall logs |
| SpamTitan | `spam_titan` | SpamTitan logs |
| Splunk Network Traffic | `splunknetworktraffic` | Splunk Network Traffic logs |
| Splunk Search | `splunksearch` | Splunk Search logs |
| Splunk Send Mod Action | `splunksendmodaction` | Splunk Send Mod Action logs |
| Squid | `squid` | Squid proxy server logs |
| SSHD | `sshd` | Secure Shell Daemon (SSH) logs |
| SSMTP | `ssmtp` | SSMTP logs |
| Stealthbitsactivitymonitor | `stealthbitsactivitymonitor` | Stealthbitsactivitymonitor logs |
| SU | `su` | Switch User (su) logs |
| Sudo | `sudo` | Sudo command logs |
| Suricata | `suricata` | Suricata network intrusion detection logs |
| SVN | `svn` | Subversion (SVN) logs |
| Symantec DLP | `symantecdlp` | Symantec DLP logs |
| Symantec ProxySG | `symantecproxysg` | Symantec ProxySG logs |
| Symantec SEP | `symantecsep` | Symantec SEP logs |
| Syslog Mark | `syslogmark` | Syslog Mark logs |
| Syslog-NG | `syslogng` | Syslog-NG logs |
| Systemd | `systemd` | Systemd logs |
| Tanium Detect RFC | `tanium_detect_rfc` | Tanium Detect RFC logs |
| Tanium Signals | `tanium_signals` | Tanium Signals logs |
| Tenable AD | `tenable_ad` | Tenable AD logs |
| Tenable.io | `tenable_io` | Tenable.io asset inventory via REST API |
| Timesyncd | `timesyncd` | Time Synchronization Daemon logs |
| TippingPoint IPS | `tippingpointips` | TippingPoint IPS logs |
| TippingPoint IPS 2 | `tippingpointips2` | TippingPoint IPS 2 logs |
| Trellix JSON | `trellix_json` | Trellix JSON logs |
| Trellix PX | `trellix_px` | Trellix PX logs |
| Tufin | `tufin` | Tufin logs |
| Tufin Policy | `tufinstpolicy` | Tufin Policy logs |
| UFW | `ufw` | Uncomplicated Firewall (UFW) logs |
| Unifi Security Gateway | `unifi_security_gateway` | Unifi Security Gateway logs |
| Unifi System | `unifi_system` | Unifi System logs |
| VDSM | `vdsm` | Virtual Desktop and Server Manager (VDSM) logs |
| VMware ESXi | `vmware_esxi` | VMware ESXi logs |
| VMware ESXi addvob | `vmwareaddvob` | VMware ESXi addvob (VMkernel Observation injector) host logs |
| VMware ESXi Update | `vmware_esxupdate` | VMware ESXi Update logs |
| VMware NSX Config Agent | `vmwarensxcfgagent` | VMware NSX config agent (cfgAgent) logs |
| VMware NSX Exporter | `vmwarensxexporter` | VMware NSX host aggregation/fabric exporter (nsx-exporter) logs |
| VMware NSX Firewall | `vmwarensxfirewall` | VMware NSX Firewall logs |
| VMware NSX Manager | `vmwarensx` | VMware NSX manager/CCP (NSX app-name) logs |
| VMware NSX Manager (TLS/Trust) | `vmwarensxmanager` | VMware NSX Manager certificate/TLS-trust stack traces (NsxTrustManager, tcp_newline) |
| VMware NSX NestDB | `vmwarensxnestdb` | VMware NSX NestDB host config-store logs (ESXi transport nodes) |
| VMware NSX Netopa | `vmwarensxnetopa` | VMware NSX network operations agent (netopa) keepalive and framework telemetry from ESXi transport nodes |
| VMware NSX Ops Agent | `nsxopsagent` | VMware NSX operations agent (nsx-opsagent) logs |
| VMware NSX Proxy | `vmwarensxproxy` | VMware NSX proxy (nsx-proxy) logs |
| VMware NSX SFHC | `vmwarensxsfhc` | VMware NSX Service Fabric Host Component lifecycle logs |
| VMware NSX SHA | `vmwarensxsha` | VMware NSX system health agent (nsx-sha) logs |
| VMware NSX SHA Python | `vmwarensxshapython` | VMware NSX system health agent python plugins (nsx-sha-python) logs |
| VMware NSX-T MP Service | `vmwarensxmpservice` | VMware NSX-T Manager RPC/aggregation service logs |
| VMware Reverse HTTP Proxy | `rhttpproxy` | VMware Reverse HTTP Proxy (rhttpproxy) logs |
| VMware Tools | `vmware_tools` | VMware Tools logs |
| VMware vCenter Appliance Management | `vmwareapplmgmt` | VMware vCenter Server Appliance Management Service (applmgmt_vmonsvc) logs |
| VMware vCenter Lookup Service | `vmwarevclookupsvc` | VMware vCenter Lookup Service (lookupsvc-lookupserver) logs |
| VMware vCenter Server | `vmwarevcenter` | VMware vCenter Server daemon logs |
| VMware vCenter SSO STS Service | `vmwareidentitysts` | VMware vCenter Single Sign-On Security Token Service (STS) service logs |
| VMware VGAUTH | `vmware_vgauth` | VMware VGAUTH logs |
| VMware Vpxa (ESXi Agent) | `vcenter` | VMware Vpxa ESXi host agent logs |
| VMware VPXD | `vmwarevpxd` | VMware vCenter Server VPXD daemon logs |
| VMware vSphere SSO | `vmware_vsphere_sso` | VMware vCenter Single Sign-On (STS) authentication |
| VMware vSphere SSO Tomcat Access | `vmwaressotomcat` | VMware vCenter Single Sign-On Tomcat localhost access logs (STS / sso-adminserver HTTP requests) |
| Vmwarensxavim | `vmwarensxavim` | Vmwarensxavim logs |
| Vmwarevsanclusteragent | `vmwarevsanclusteragent` | Vmwarevsanclusteragent logs |
| Vmwarevsanepd | `vmwarevsanepd` | VMware vSAN entry persistence daemon (epd) logs |
| Websense | `websense` | Websense logs |
| Whoopsie | `whoopsie` | Whoopsie crash reporting logs |
| Windows Agent | `windowsagent` | Windows Agent logs |
| Windows DHCP Server | `windows_dhcp_server` | Windows DHCP Server logs |
| Windows Event Log | `windowseventlog` | Windows Event logs |
| Windows Event Log NXLog | `windowseventlognxlog` | Windows Event Log NXLog logs |
| Windows Security Audit CSV | `windowssecurityauditcsv` | Windows Security Audit CSV logs |
| Windows Security Audit Equals Newline KV | `windows_security_audit_equalsnewlinekv` | Windows Security Audit Equals Newline KV logs |
| Windows Security Audit XML | `windowssecurityauditxml` | Windows Security Audit XML logs |
| Winlogbeat | `winlogbeat` | Winlogbeat logs |
| Winlogbeat ECS | `winlogbeat_ecs` | Elastic winlogbeat ECS JSON (Windows Event Log) |
| WitFoo Console | `witfooconsole` | WitFoo Console appliance internal service chatter (Echo access logs, housekeeping) — diagnostic drain |
| WordPress | `wordpress` | WordPress logs |
| Xinetd | `xinetd` | Xinetd logs |
| Zeek | `zeek` | Zeek network monitoring logs |
| Zscaler NSS | `zscaler_nss` | Zscaler NSS logs |
