"""
WitFoo Artifact Field Registry

Exhaustive registry of all camelCase field names from the artifact.Artifact struct
(conductor_suite/common/domain/artifact/artifact.go). These are the exact field names
sent to all SIEM platforms (Splunk, OpenSearch, Sentinel) by the artifact-exporter.

Used by:
  - Sigma rule validation (ensure rules reference real fields)
  - pySigma processing pipelines (field mapping)
  - Dashboard query validation
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FieldType(Enum):
    STRING = "string"
    INT = "int"
    INT_ARRAY = "[]int"
    STRING_ARRAY = "[]string"
    UUID = "uuid"
    TIMESTAMP = "timestamp"


@dataclass(frozen=True)
class ArtifactField:
    """Represents a single field from artifact.Artifact."""
    name: str
    field_type: FieldType
    category: str
    description: str
    example: Optional[str] = None


# Complete field registry — matches artifact.Artifact struct JSON tags exactly
ARTIFACT_FIELDS: dict[str, ArtifactField] = {f.name: f for f in [
    # Meta / Identity
    ArtifactField("id", FieldType.UUID, "Meta", "Artifact ID (timeuuid)"),
    ArtifactField("hash", FieldType.STRING, "Meta", "XXH64 dedup hash"),
    ArtifactField("org_id", FieldType.STRING, "Meta", "Organization ID", "witfoo"),
    ArtifactField("appliance_id", FieldType.UUID, "Meta", "Source appliance UUID"),

    # Network — Source
    ArtifactField("clientIP", FieldType.STRING, "Network", "Source IP address", "192.168.1.100"),
    ArtifactField("clientPort", FieldType.STRING, "Network", "Source port", "54321"),
    ArtifactField("clientHostname", FieldType.STRING, "Network", "Source hostname", "workstation-01"),
    ArtifactField("clientMAC", FieldType.STRING, "Network", "Source MAC address", "00:11:22:33:44:55"),
    ArtifactField("clientBytes", FieldType.STRING, "Network", "Bytes sent by client", "1024"),
    ArtifactField("clientPackets", FieldType.STRING, "Network", "Packets sent by client", "10"),

    # Network — Destination
    ArtifactField("serverIP", FieldType.STRING, "Network", "Destination IP address", "10.0.0.1"),
    ArtifactField("serverPort", FieldType.STRING, "Network", "Destination port", "443"),
    ArtifactField("serverHostname", FieldType.STRING, "Network", "Destination hostname", "db-server-01"),
    ArtifactField("serverMAC", FieldType.STRING, "Network", "Destination MAC address"),
    ArtifactField("serverBytes", FieldType.STRING, "Network", "Bytes sent by server", "4096"),
    ArtifactField("serverPackets", FieldType.STRING, "Network", "Packets received", "8"),

    # Network — Aggregate
    ArtifactField("protocol", FieldType.STRING, "Network", "Network protocol", "TCP"),
    ArtifactField("totalBytes", FieldType.STRING, "Network", "Total bytes transferred", "5120"),
    ArtifactField("fqdn", FieldType.STRING, "Network", "Fully qualified domain name", "evil.example.com"),

    # Identity
    ArtifactField("userName", FieldType.STRING, "Identity", "User name", "jdoe"),
    ArtifactField("emailFrom", FieldType.STRING, "Identity", "Email sender", "user@example.com"),
    ArtifactField("emailTo", FieldType.STRING, "Identity", "Email recipient", "admin@corp.com"),
    ArtifactField("emailSubject", FieldType.STRING, "Identity", "Email subject line"),
    ArtifactField("emailClient", FieldType.STRING, "Identity", "Email client application"),
    ArtifactField("emailSendingServer", FieldType.STRING, "Identity", "Sending mail server"),

    # File
    ArtifactField("fileName", FieldType.STRING, "File", "File name", "malware.exe"),
    ArtifactField("fileHash", FieldType.STRING, "File", "File hash (SHA256/MD5)", "a1b2c3d4..."),
    ArtifactField("filePath", FieldType.STRING, "File", "File path", "/tmp/payload.bin"),

    # Classification
    ArtifactField("streamName", FieldType.STRING, "Classification", "Log source stream", "ids_suricata"),
    ArtifactField("messageType", FieldType.STRING, "Classification", "Event classification", "auth_failure"),
    ArtifactField("action", FieldType.STRING, "Classification", "Action taken", "block"),
    ArtifactField("tags", FieldType.STRING_ARRAY, "Classification", "Event tags"),

    # Severity
    ArtifactField("severityCode", FieldType.STRING, "Severity", "Numeric severity (1=critical, 5=info)", "2"),
    ArtifactField("severityLabel", FieldType.STRING, "Severity", "Severity label", "high"),

    # Detection
    ArtifactField("ruleName", FieldType.STRING, "Detection", "IDS/IPS rule name", "ET TROJAN"),
    ArtifactField("ruleCategory", FieldType.STRING, "Detection", "IDS/IPS rule category", "trojan-activity"),
    ArtifactField("cve", FieldType.STRING, "Detection", "CVE identifier", "CVE-2024-1234"),
    ArtifactField("cveDescription", FieldType.STRING, "Detection", "CVE description text"),
    ArtifactField("matchedLeadRules", FieldType.INT_ARRAY, "Detection", "WitFoo lead rule IDs", "[2, 10]"),
    ArtifactField("attackTechniqueIds", FieldType.STRING_ARRAY, "Detection", "MITRE ATT&CK technique IDs", '["T1110", "T1078"]'),
    ArtifactField("stixIndicatorIds", FieldType.STRING_ARRAY, "Detection", "STIX indicator IDs"),
    ArtifactField("matchedPredicateRules", FieldType.INT_ARRAY, "Detection", "Predicate rule IDs"),

    # Context
    ArtifactField("senderHost", FieldType.STRING, "Context", "Original sender host"),
    ArtifactField("sourceInfo", FieldType.STRING, "Context", "Source metadata"),
    ArtifactField("program", FieldType.STRING, "Context", "Program name", "sshd"),
    ArtifactField("pid", FieldType.STRING, "Context", "Process ID", "12345"),
    ArtifactField("application", FieldType.STRING, "Context", "Application name", "apache2"),
    ArtifactField("vendorCode", FieldType.STRING, "Context", "Vendor-specific code"),
    ArtifactField("uri", FieldType.STRING, "Context", "Request URI", "/api/v1/login"),

    # Syslog
    ArtifactField("facilityCode", FieldType.STRING, "Syslog", "Syslog facility code", "4"),
    ArtifactField("facilityLabel", FieldType.STRING, "Syslog", "Syslog facility label", "auth"),
    ArtifactField("priority", FieldType.STRING, "Syslog", "Syslog priority", "34"),

    # GeoIP
    ArtifactField("geoRegion", FieldType.STRING, "GeoIP", "Geographic region", "US-East"),

    # Time
    ArtifactField("startTimeUTC", FieldType.STRING, "Time", "Event start time (UTC)"),
    ArtifactField("endTimeUTC", FieldType.STRING, "Time", "Event end time (UTC)"),

    # Raw
    ArtifactField("message", FieldType.STRING, "Raw", "Raw log message"),

    # Enrichment (set IDs from behavioral sets)
    ArtifactField("productIds", FieldType.INT_ARRAY, "Enrichment", "Product IDs"),
    ArtifactField("clientSetIds", FieldType.INT_ARRAY, "Enrichment", "Client behavioral set IDs"),
    ArtifactField("serverSetIds", FieldType.INT_ARRAY, "Enrichment", "Server behavioral set IDs"),
    ArtifactField("fileSetIds", FieldType.INT_ARRAY, "Enrichment", "File behavioral set IDs"),
    ArtifactField("userSetIds", FieldType.INT_ARRAY, "Enrichment", "User behavioral set IDs"),
]}


# Convenience sets for validation
VALID_FIELD_NAMES: frozenset[str] = frozenset(ARTIFACT_FIELDS.keys())

NETWORK_FIELDS: frozenset[str] = frozenset(
    f.name for f in ARTIFACT_FIELDS.values() if f.category == "Network"
)

DETECTION_FIELDS: frozenset[str] = frozenset(
    f.name for f in ARTIFACT_FIELDS.values() if f.category == "Detection"
)

IDENTITY_FIELDS: frozenset[str] = frozenset(
    f.name for f in ARTIFACT_FIELDS.values() if f.category == "Identity"
)

# Valid logsource values for WitFoo Sigma rules
WITFOO_LOGSOURCE = {
    "product": "witfoo",
    "service": "artifact-exporter",
}

# Valid messageType values (from lead rules and artifact classification)
VALID_MESSAGE_TYPES: frozenset[str] = frozenset([
    "auth_failure", "blocked", "botnet_connection", "credential_access",
    "data_destruction", "data_exfiltration", "data_staging",
    "defense_evasion", "exploit_attempt", "malicious_behavior",
    "malicious_session", "phishing_click", "phishing_email",
    "policy_violation", "privilege_escalation", "service_discovery",
    "service_disruption", "anomalous_behavior", "degraded_hardware",
    "degraded_service", "financial_anomaly", "ids_event", "ids_action",
    "content_filter", "ioc_match", "iom_match", "blacklisted_process",
    "threat_event", "endpoint_protection", "infrastructure_exploit",
    "malicious_software", "ransomware_download", "ransomware_encryption",
    "config_change",
])
