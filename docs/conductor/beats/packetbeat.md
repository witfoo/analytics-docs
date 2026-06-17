---
tags:
  - conductor
  - integration
  - beats
---

# Packetbeat (OSS)

Packetbeat captures **network metadata** off the wire — DNS queries, HTTP
transactions, TLS handshakes, and connection flows — and ships it to Conductor
over the Lumberjack protocol. It is a passive sensor: deploy it on a host that
sees the traffic you care about (a server, or a box receiving a SPAN/mirror
port).

| | |
|---|---|
| **Category** | Push Ingestion (Log Shipper) |
| **Protocol** | Lumberjack (Beats *Logstash* output) |
| **Conductor Port** | TCP 5044 / 5045 |
| **Distribution** | OSS — Apache License 2.0 (`packetbeat-oss`) |
| **OSS Release Line** | 7.17.x (final OSS line; examples use `7.17.29`) |
| **Platforms** | Linux (libpcap), Windows (Npcap) |
| **Vendor Docs** | [Packetbeat Reference 7.17](https://www.elastic.co/guide/en/beats/packetbeat/7.17/index.html) |

!!! warning "OSS only"
    Install `packetbeat-oss` (Apache 2.0). There is **no** `-oss` build for
    8.x/9.x — use the **7.17.x** line. See the [overview](index.md).

## Prerequisites

- [ ] The **Beats/Logstash** listener is enabled in Conductor
      ([Log Servers](../ui/log-servers.md))
- [ ] The sensor host can reach the Conductor host on TCP **5044/5045**
- [ ] Packet-capture support: **libpcap** on Linux (pulled in by the package),
      **[Npcap](https://npcap.com/)** on Windows
- [ ] Root (Linux) / Administrator (Windows) — raw packet capture is privileged

## Step 1 — Install the OSS build

=== "Debian / Ubuntu"

    Using the OSS repository (see [overview Step 2](index.md#step-2-install-the-oss-build)):

    ```bash
    sudo apt-get install packetbeat-oss
    ```

    Or install a standalone artifact:

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-7.17.29-amd64.deb
    sudo dpkg -i packetbeat-oss-7.17.29-amd64.deb
    ```

=== "RHEL / CentOS"

    Using the OSS repository:

    ```bash
    sudo yum install packetbeat-oss
    ```

    Or install a standalone artifact:

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-7.17.29-x86_64.rpm
    sudo rpm -vi packetbeat-oss-7.17.29-x86_64.rpm
    ```

=== "Linux tar.gz"

    ```bash
    curl -L -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-7.17.29-linux-x86_64.tar.gz
    tar xzvf packetbeat-oss-7.17.29-linux-x86_64.tar.gz
    cd packetbeat-oss-7.17.29-linux-x86_64
    ```

=== "Windows"

    Install [Npcap](https://npcap.com/) first (WinPcap-compatible mode), then:

    ```powershell
    # Run as Administrator
    Invoke-WebRequest -Uri https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-oss-7.17.29-windows-x86_64.zip -OutFile packetbeat-oss.zip
    Expand-Archive .\packetbeat-oss.zip -DestinationPath 'C:\Program Files\'
    Rename-Item 'C:\Program Files\packetbeat-oss-7.17.29-windows-x86_64' 'Packetbeat'
    cd 'C:\Program Files\Packetbeat'
    .\install-service-packetbeat.ps1
    ```

Confirm the OSS build:

```bash
packetbeat version
# packetbeat version 7.17.29 (amd64), libbeat 7.17.29 ...
```

## Step 2 — Configure `packetbeat.yml`

Edit `/etc/packetbeat/packetbeat.yml` (Linux) or
`C:\Program Files\Packetbeat\packetbeat.yml` (Windows):

```yaml
# ============================================================
# packetbeat.yml — OSS build, ships to WitFoo Conductor
# ============================================================

# --------------------------- Capture ------------------------
# "any" captures on all interfaces (Linux). On Windows, set the device
# index from: packetbeat devices
packetbeat.interfaces.device: any

# --------------------------- Flows --------------------------
packetbeat.flows:
  timeout: 30s
  period: 10s

# ------------------------- Protocols ------------------------
packetbeat.protocols:
  - type: dns
    ports: [53]
    include_authorities: true
    include_additionals: true

  - type: http
    ports: [80, 8080, 8000, 5000]

  - type: tls
    ports: [443, 8443]

  - type: dhcpv4
    ports: [67, 68]

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
#   # ssl.certificate_authorities: ["/etc/packetbeat/conductor-ca.crt"]

# Not shipping to Elasticsearch/Kibana — disable their setup paths.
setup.template.enabled: false
setup.ilm.enabled: false
setup.dashboards.enabled: false

# ---------------------------- Logging -----------------------
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/packetbeat
  name: packetbeat
  keepfiles: 7
```

!!! tip "DNS and TLS are the high-value protocols"
    For security telemetry, **DNS**, **TLS** (SNI/cert metadata), and **flows**
    deliver the most value at the lowest volume. Add `http` only where you have
    plaintext HTTP worth inspecting. Packetbeat records metadata, not payloads.

## Step 3 — Validate and start

```bash
# Validate configuration and connectivity (capture needs root)
sudo packetbeat test config -e
sudo packetbeat test output -e        # should reach <conductor-host>:5044

# List capture devices if "any" is not suitable
sudo packetbeat devices

# Start the service
sudo systemctl enable --now packetbeat        # Linux (package install)
# Start-Service packetbeat                     # Windows
```

Then confirm delivery on the Conductor host:

```bash
docker logs signal-server-svc --tail=50
```

Open **WitFoo Analytics → Signals → Search** and look for flow/DNS/TLS
artifacts from the sensor host. Packetbeat events arrive as Beats JSON.

## Troubleshooting

### No events / "no devices found"

Run `sudo packetbeat devices` and set `packetbeat.interfaces.device` to a real
interface. On Windows, install **Npcap** in WinPcap-compatible mode before
starting the service.

### Permission denied opening interface

Packet capture is privileged. Run under `sudo`/Administrator, or grant the Linux
binary capture capability:

```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which packetbeat)
```

### `test output` fails with connection refused

Enable the **Beats/Logstash** connector in
[Log Servers](../ui/log-servers.md) and confirm firewall access to TCP
5044/5045.

### TLS handshake / EOF on connect

The node has TLS enabled but the output is plain (or vice versa). Add the
`ssl.*` block above (self-signed → `ssl.verification_mode: none`), or disable
TLS on the node. See the [TLS note](index.md#step-3-point-the-output-at-conductor).

---

*See also: [Log Shippers overview](index.md) ·
[Filebeat (OSS)](filebeat.md) ·
[Winlogbeat (OSS)](winlogbeat.md)*
