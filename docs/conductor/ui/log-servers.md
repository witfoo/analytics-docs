# Log Server Configuration

**URL:** `/admin/settings/log-servers`

The Log Server Configuration page manages push-based log ingestion listeners for the Signal Server service. Each listener accepts incoming log data on a specific protocol and port.

## Log Server Connectors

| Connector | Port | Protocol | Description |
|-----------|------|----------|-------------|
| UDP/514 (Syslog) | 514 | UDP | Standard syslog over UDP, in RFC 3164 or RFC 5424 format, one message per datagram. Each datagram is read whole. No delivery guarantee. |
| TCP/514 (Syslog) | 514 | TCP | Standard syslog over TCP, in RFC 3164 or RFC 5424 format, newline terminated. Reliable delivery with connection tracking. |
| TCP/6514 (Syslog over TLS) | 6514 | TCP or TLS | Syslog over TLS when TLS is enabled on the Conductor node (the configuration wizard's default); plain TCP otherwise. Required for compliance environments. |
| TCP/7514 (Syslog RFC6587) | 7514 | TCP or TLS | Syslog with RFC 6587 octet counting: each message is sent as its length in bytes, a space, then the message, with no line ending between messages. Uses TLS when TLS is enabled on the node, as 6514 does. |
| TCP/5044 (Beats with TLS), TCP/5045 (Beats No TLS) | 5044–5045 | TCP or TLS | Elastic Beats and Logstash Lumberjack protocol for agent-based collection. Port 5044 uses TLS when TLS is enabled on the Conductor node; port 5045 never uses TLS. |
| UDP/2055 (NetFlow / IPFIX) | 2055 | UDP | Binary flow records (NetFlow v5, v7, v9 and IPFIX) from routers, switches and firewalls. **Off until you enable it.** |
| HTTP/8008 (Artifact Receiver) | 8008 | HTTP | A WebSocket endpoint that receives artifacts from another Conductor. **Off until you enable it.** |

!!! info "Help text corrected in 1.2.0"
    The help text of the TCP/7514 listener now says it reads octet-counted frames. Earlier releases said its logs must be newline terminated, which was wrong. The UDP/514 help text no longer says logs must be newline terminated: each datagram is read whole.

## NetFlow and IPFIX Collector

The **UDP/2055 (NetFlow / IPFIX)** listener receives binary NetFlow v5, v7, v9 and IPFIX records. It decodes them, removes duplicates seen by several exporters, and summarizes them into one conversation artifact per client and server pair for every 60-second window. It is separate from the `cisco_netflow` and `netflow_optimizer` parsers, which read flow data sent as text over syslog.

To start collecting flows:

1. Open **Log Servers** in the Conductor UI and enable **UDP/2055 (NetFlow / IPFIX)**.
2. Point your flow exporters at the appliance's UDP port 2055.

Things to know:

- **It is off by default.** A new node leaves UDP/2055 and HTTP/8008 off. A node upgraded from 1.1.x has no NetFlow record, so UDP/2055 stays off until you switch it on.
- **No TLS or authentication.** NetFlow over UDP is unauthenticated by protocol, the same trust posture as syslog on UDP/514. Restrict who can reach the port at your firewall.
- **Reachability on WFA appliances.** WFA 2.5.1 and later publish 2055/udp on Conductor and AIO + Conductor appliances and open it in the host firewall. Under WFA 2.4.x the port is not published: upgrade WFA to 2.5.3, or publish it by hand.
- **Docker Compose.** The compose files do not publish 2055/udp. Add `2055:2055/udp` to the signal server's ports.
- **After a NATS data clear**, the NetFlow listener is not restored. Enable it again under Log Servers.
- **Enable it after the node has started.** If the NetFlow listener is the only enabled server when the node first starts, the classic syslog and Beats servers are not set up.
- **After a restart with a full flow-state store**, the collector can read stale flow baselines.

!!! note "HTTP/8008 on upgraded nodes"
    Releases before 1.2.0 turned HTTP/8008 on automatically, so a node upgraded from 1.1.x keeps it listening. The signal server logs `opt-in module is enabled by its KV record` at every start for such a listener. Switch HTTP/8008 off under Log Servers if nobody uses it.

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
    For most deployments, enable **UDP/514 (Syslog)** for general syslog collection and **TCP/6514 (Syslog over TLS)** for devices that support encrypted transport. Port 6514 uses TLS when TLS is enabled on the Conductor node (the configuration wizard's default); plain TCP otherwise. Use the Beats listeners (ports 5044–5045) for environments with Elastic Beats agents deployed on endpoints.

## Sending from Elastic Beats

To stream data from the OSS editions of **Filebeat**, **Winlogbeat**, or
**Packetbeat** into the Beats/Logstash listener, see the
[Log Shippers (Beats)](../beats/index.md) guides. They cover installing the OSS
(Apache 2.0) builds and the example `output.logstash` configuration for each
agent.

## Sending Syslog Out

The syslog exporter (**UDP Syslog** on the Exporters page) sends over UDP only in 1.2.0. See [Exporter Configuration](exporters.md).
