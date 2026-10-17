# Signal Server (Push Ingestion)

Signal Server handles push-based log ingestion from network sources. It listens on multiple protocols and ports, buffering incoming data before publishing to the NATS `artifacts.raw` stream for downstream processing.

## Listeners

| Protocol | Port | Description |
|----------|------|-------------|
| Syslog UDP | 514 | Standard syslog over UDP (RFC3164/RFC5424) |
| Syslog TCP | 514 | Standard syslog over TCP |
| Beats/Logstash | 5044–5045 | Elastic Beats and Logstash Lumberjack protocol. 5044 uses TLS when TLS is enabled on the Conductor node; 5045 never uses TLS |
| Secure Syslog TLS | 6514 | Syslog over TLS when TLS is enabled on the Conductor node (the configuration wizard's default); plain TCP otherwise |
| TCP | 7514 | Syslog with RFC 6587 octet counting: each message is sent as its length in bytes, a space, then the message, with nothing between messages. Uses TLS when TLS is enabled on the node, as 6514 does. |

Each listener runs as an independent connector following the **Source → Flow → Sink** pattern:

1. **Source** — Network listener accepting connections on the configured port
2. **Buffer** — Internal event buffer (5000 event capacity) for backpressure management
3. **Flow** — Transforms raw network data into `ArtifactRaw` format
4. **Sink** — Publishes to NATS JetStream on the `artifacts.raw` subject

## Configuration

Signal Server is configured via the NATS KV `SERVERS` bucket. Each listener can be independently enabled or disabled through the [Conductor UI Log Server page](ui/log-servers.md).

### Masquerading

Signal Server supports protocol masquerading, which allows a listener to accept data in one format and tag it as another. This is useful when network devices send non-standard syslog formats or when protocol conversion is needed at the ingestion point.

## Performance

- **TCP timeout**: 60 seconds (industry standard for log collectors)
- **Lumberjack protocol**: Payload validation with 10 MB compressed limit and 4096 events per window
- **Non-blocking sends**: All framers use non-blocking channel sends to prevent connection hangs
- **Buffer capacity**: 5000 events per listener with backpressure management

!!! tip
    When configuring network devices to send syslog to Conductor, use TCP (port 514) or Secure Syslog TLS (port 6514) for reliable delivery. UDP syslog may drop messages under high load since UDP provides no delivery guarantee.
