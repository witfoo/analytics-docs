---
tags:
  - conductor
  - integration
  - beats
---

# Winlogbeat (OSS)

Winlogbeat ships **Windows Event Logs** — Security, System, Application, and
Sysmon channels — to Conductor over the Lumberjack protocol. It is a
Windows-only agent.

| | |
|---|---|
| **Category** | Push Ingestion (Log Shipper) |
| **Protocol** | Lumberjack (Beats *Logstash* output) |
| **Conductor Port** | TCP 5044 / 5045 |
| **Distribution** | OSS — Apache License 2.0 (`winlogbeat-oss`) |
| **OSS Release Line** | 7.17.x (final OSS line; examples use `7.17.29`) |
| **Platforms** | Windows |
| **Vendor Docs** | [Winlogbeat Reference 7.17](https://www.elastic.co/guide/en/beats/winlogbeat/7.17/index.html) |

!!! warning "OSS only"
    Install the **`winlogbeat-oss`** ZIP (Apache 2.0). There is **no** `-oss`
    build for 8.x/9.x — use the **7.17.x** line. See the [overview](index.md).

## Prerequisites

- [ ] The **Beats/Logstash** listener is enabled in Conductor
      ([Log Servers](../ui/log-servers.md))
- [ ] The Windows host can reach the Conductor host on TCP **5044/5045**
- [ ] Administrator PowerShell on the Windows host
- [ ] *(Optional)* [Sysmon](https://learn.microsoft.com/sysinternals/downloads/sysmon)
      installed for richer endpoint telemetry

## Step 1 — Install the OSS build

Winlogbeat is distributed only as a Windows `.zip`. Run an **elevated**
PowerShell:

```powershell
# Download the OSS build (7.17.x — final OSS line)
Invoke-WebRequest `
  -Uri https://artifacts.elastic.co/downloads/beats/winlogbeat/winlogbeat-oss-7.17.29-windows-x86_64.zip `
  -OutFile winlogbeat-oss.zip

# Extract and place under Program Files
Expand-Archive .\winlogbeat-oss.zip -DestinationPath 'C:\Program Files\'
Rename-Item 'C:\Program Files\winlogbeat-oss-7.17.29-windows-x86_64' 'Winlogbeat'
cd 'C:\Program Files\Winlogbeat'

# Install the Windows service (does not start it yet)
.\install-service-winlogbeat.ps1
```

Confirm the OSS build:

```powershell
.\winlogbeat.exe version
# winlogbeat version 7.17.29 (amd64), libbeat 7.17.29 ...
```

## Step 2 — Configure `winlogbeat.yml`

Edit `C:\Program Files\Winlogbeat\winlogbeat.yml`:

```yaml
# ============================================================
# winlogbeat.yml — OSS build, ships to WitFoo Conductor
# ============================================================

# --------------------------- Event Logs ---------------------
winlogbeat.event_logs:
  - name: Security
  - name: System
  - name: Application
    ignore_older: 72h

  # Sysmon — include only if Sysmon is installed
  - name: Microsoft-Windows-Sysmon/Operational

  # PowerShell script-block logging (very useful for detection)
  - name: Microsoft-Windows-PowerShell/Operational
    event_id: 4103, 4104

# ---------------------------- Output ------------------------
# Conductor's Signal Server speaks the Lumberjack protocol used by the
# Beats Logstash output. Point output.logstash at the Conductor host.
output.logstash:
  hosts: ["<conductor-host>:5044"]
  # Spread across both listeners (optional):
  # hosts: ["<conductor-host>:5044", "<conductor-host>:5045"]
  # loadbalance: true

# If your Conductor node runs with TLS enabled, uncomment:
# output.logstash:
#   hosts: ["<conductor-host>:5044"]
#   ssl.enabled: true
#   ssl.verification_mode: none   # appliance uses a self-signed certificate
#   # ssl.certificate_authorities: ["C:\\Program Files\\Winlogbeat\\conductor-ca.crt"]

# Not shipping to Elasticsearch/Kibana — disable their setup paths.
setup.template.enabled: false
setup.ilm.enabled: false
setup.dashboards.enabled: false

# ---------------------------- Logging -----------------------
logging.level: info
logging.to_files: true
logging.files:
  path: C:\ProgramData\winlogbeat\Logs
  name: winlogbeat
  keepfiles: 7
```

!!! tip "Pick channels deliberately"
    `Security` is high-volume. For most deployments **Security + System +
    Sysmon + PowerShell/Operational** give strong detection coverage without
    flooding the pipeline. Use `event_id` and `ignore_older` to scope each
    channel.

## Step 3 — Validate and start

```powershell
# From C:\Program Files\Winlogbeat (elevated)
.\winlogbeat.exe test config -c .\winlogbeat.yml -e
.\winlogbeat.exe test output -c .\winlogbeat.yml -e   # reach <conductor-host>:5044

# Start the service
Start-Service winlogbeat
```

Then confirm delivery on the Conductor host:

```bash
docker logs signal-server-svc --tail=50
```

Open **WitFoo Analytics → Signals → Search** and filter for the Windows
hostname. Winlogbeat events are auto-detected as the `winlogbeat` log format by
the pipeline.

## Troubleshooting

### `test output` fails with connection refused

Enable the **Beats/Logstash** connector in
[Log Servers](../ui/log-servers.md) and confirm the Windows firewall permits
outbound TCP 5044/5045.

### TLS handshake / EOF on connect

The node has TLS enabled but the output is plain (or vice versa). Add the
`ssl.*` block above — for a self-signed appliance certificate set
`ssl.verification_mode: none` or pin the CA. See the
[TLS note](index.md#step-3-point-the-output-at-conductor).

### Sysmon channel not found

Winlogbeat logs `failed to open ... Microsoft-Windows-Sysmon/Operational`.
Install Sysmon, or remove that entry from `winlogbeat.event_logs`.

---

*See also: [Log Shippers overview](index.md) ·
[Filebeat (OSS)](filebeat.md) ·
[Packetbeat (OSS)](packetbeat.md)*
