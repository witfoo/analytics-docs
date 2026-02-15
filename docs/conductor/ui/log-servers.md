# Log Server Configuration

**URL:** `/admin/settings/log-servers`

The Log Server Configuration page manages push-based log ingestion listeners for the Signal Server service. Each listener accepts incoming log data on a specific protocol and port.

## Log Server Connectors

| Connector | Port | Protocol | Description |
|-----------|------|----------|-------------|
| Syslog UDP | 514 | UDP | Standard syslog over UDP. Lightweight, no delivery guarantee. |
| Syslog TCP | 514 | TCP | Standard syslog over TCP. Reliable delivery with connection tracking. |
| Secure Syslog TLS | 6514 | TCP+TLS | Encrypted syslog using TLS certificates. Required for compliance environments. |
| Beats/Logstash | 5044–5045 | TCP | Elastic Beats and Logstash Lumberjack protocol for agent-based collection. |

## Features

### Enable/Disable Toggles

Each log server connector has an independent toggle. Disabled connectors stop listening on their respective ports.

### Masquerading Options

Log server connectors support protocol masquerading, which allows a listener to accept data in one format and tag it as another protocol type. This is useful when:

- Network devices send non-standard syslog formats
- Protocol conversion is needed at the ingestion point
- Legacy devices use unexpected port/protocol combinations

## Configuration

Changes are saved to the NATS KV `SERVERS` bucket and propagate to the Signal Server service within seconds. No container restart is required.

!!! tip
    For most deployments, enable **Syslog UDP** (port 514) for general syslog collection and **Secure Syslog TLS** (port 6514) for devices that support encrypted transport. Use **Beats/Logstash** (ports 5044–5045) for environments with Elastic Beats agents deployed on endpoints.