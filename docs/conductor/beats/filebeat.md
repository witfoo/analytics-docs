---
tags:
  - conductor
  - integration
  - beats
---

# Filebeat (OSS)

Filebeat is a lightweight shipper for **log files** — syslog, authentication
logs, web/application logs, and structured (NDJSON) logs. The OSS edition
streams those events to Conductor over the Lumberjack protocol.

| | |
|---|---|
| **Category** | Push Ingestion (Log Shipper) |
| **Protocol** | Lumberjack (Beats *Logstash* output) |
| **Conductor Port** | TCP 5044 / 5045 |
| **Distribution** | OSS — Apache License 2.0 (`filebeat-oss`) |
| **OSS Release Line** | 7.17.x (final OSS line; examples use `7.17.29`) |
| **Platforms** | Linux, Windows |
| **Vendor Docs** | [Filebeat Reference 7.17](https://www.elastic.co/guide/en/beats/filebeat/7.17/index.html) |

!!! warning "OSS only"
    Install `filebeat-oss` (Apache 2.0). There is **no** `-oss` build for 8.x/9.x
    — use the **7.17.x** line. See the [overview](index.md) for the full
    rationale.

## Prerequisites

- [ ] The **Beats/Logstash** listener is enabled in Conductor
      ([Log Servers](../ui/log-servers.md))
- [ ] The agent host can reach the Conductor host on TCP **5044/5045**
- [ ] Root/Administrator on the host where Filebeat runs

## Step 1 — Install the OSS build

=== "Debian / Ubuntu"

    Using the OSS repository (see [overview Step 2](index.md#step-2-install-the-oss-build)):

    ```bash
    sudo apt-get install filebeat-oss
    ```

    Or install a standalone artifact:

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.17.29-amd64.deb
    sudo dpkg -i filebeat-oss-7.17.29-amd64.deb
    ```

=== "RHEL / CentOS"

    Using the OSS repository:

    ```bash
    sudo yum install filebeat-oss
    ```

    Or install a standalone artifact:

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.17.29-x86_64.rpm
    sudo rpm -vi filebeat-oss-7.17.29-x86_64.rpm
    ```

=== "Linux tar.gz"

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.17.29-linux-x86_64.tar.gz
    tar xzvf filebeat-oss-7.17.29-linux-x86_64.tar.gz
    cd filebeat-oss-7.17.29-linux-x86_64
    ```

=== "Windows"

    ```powershell
    # Run as Administrator
    Invoke-WebRequest -Uri https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.17.29-windows-x86_64.zip -OutFile filebeat-oss.zip
    Expand-Archive .\filebeat-oss.zip -DestinationPath 'C:\Program Files\'
    Rename-Item 'C:\Program Files\filebeat-oss-7.17.29-windows-x86_64' 'Filebeat'
    cd 'C:\Program Files\Filebeat'
    .\install-service-filebeat.ps1
    ```

Confirm the OSS build installed:

```bash
filebeat version
# filebeat version 7.17.29 (amd64), libbeat 7.17.29 ...
```

## Step 2 — Configure `filebeat.yml`

Replace the package default at `/etc/filebeat/filebeat.yml`
(Linux) or `C:\Program Files\Filebeat\filebeat.yml` (Windows) with a
Conductor-focused configuration:

```yaml
# ============================================================
# filebeat.yml — OSS build, ships to WitFoo Conductor
# ============================================================

# ----------------------------- Inputs -----------------------
filebeat.inputs:
  - type: filestream
    id: system-logs
    enabled: true
    paths:
      - /var/log/syslog
      - /var/log/auth.log
      - /var/log/messages
      - /var/log/secure

  # Example: a structured (NDJSON) application log
  - type: filestream
    id: app-json
    enabled: false
    paths:
      - /var/log/myapp/*.json
    parsers:
      - ndjson:
          target: ""
          add_error_key: true

# ----------------------------- Output -----------------------
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
#   # ssl.certificate_authorities: ["/etc/filebeat/conductor-ca.crt"]

# Not shipping to Elasticsearch/Kibana — disable their setup paths.
setup.template.enabled: false
setup.ilm.enabled: false
setup.dashboards.enabled: false

# ----------------------------- Logging ----------------------
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0640
```

!!! tip "Modules are available in the OSS build"
    OSS Filebeat still ships the bundled modules (e.g. `system`, `nginx`,
    `iptables`). Enable them with `filebeat modules enable system` and add
    `filebeat.config.modules` — they ship through the same `output.logstash`
    block. Only X-Pack features are removed from the OSS distribution.

## Step 3 — Validate and start

```bash
# Validate configuration and connectivity
sudo filebeat test config -e
sudo filebeat test output -e        # should reach <conductor-host>:5044

# Start the service
sudo systemctl enable --now filebeat        # Linux (package install)
# Start-Service filebeat                     # Windows
```

Then confirm delivery:

```bash
# On the Conductor host
docker logs signal-server-svc --tail=50
```

Open **WitFoo Analytics → Signals → Search** and filter for the agent's
hostname. Filebeat events are auto-detected as the `filebeat` log format by the
pipeline.

## Troubleshooting

### `test output` fails with connection refused

The Beats listener is disabled or unreachable. Enable **Beats/Logstash** in
[Log Servers](../ui/log-servers.md) and confirm firewall access to TCP 5044/5045.

### TLS handshake / EOF on connect

The node has TLS enabled but the output is plain (or vice versa). Add the
`ssl.*` block shown above (self-signed → `ssl.verification_mode: none`), or
disable TLS on the node. See the [TLS note](index.md#step-3-point-the-output-at-conductor).

### Events collected but not searchable in Analytics

Check that the input `paths` match real files and that Filebeat has read
permission. `filebeat -e` in the foreground prints harvester activity per file.

---

*See also: [Log Shippers overview](index.md) ·
[Winlogbeat (OSS)](winlogbeat.md) ·
[Packetbeat (OSS)](packetbeat.md)*
