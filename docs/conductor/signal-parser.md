# Signal Parser Architecture

The Signal Parser transforms raw log messages into structured security artifacts. It consumes from the `artifacts.raw` NATS stream, runs each message through a serial pipeline of 200+ parsers, and publishes results to either `artifacts.parsed` (successful) or `artifacts.unknown` (unmatched).

## Serial Parser Pipeline

The parser uses a five-service internal architecture:

1. **InputPipeline** — Consumes from NATS, performs format detection (RFC3164, RFC5424, CEF, LEEF, JSON, Zeek), and broadcasts to the parser stage
2. **SerialParserPipeline** — Processes messages through parsers serially with early exit optimization. When a parser's fingerprint matches, parsing executes immediately and no further parsers are tested.
3. **OutputPipeline** — Routes parsed artifacts to `artifacts.parsed` and unmatched messages to `artifacts.unknown`
4. **SvcWatcher** — Orchestrates startup: waits for all parsers to initialize before allowing the InputPipeline to consume messages
5. **249 Connector Services** — Configuration watchers that enable/disable individual parsers based on NATS KV state

## Parser Registry and Fingerprinting

Each parser implements the `Parsable` interface:

```go
type Parsable interface {
    Fingerprint(draft *artifact.Draft) bool  // Can this parser handle the message?
    Parse(draft *artifact.Draft) error       // Extract structured fields
    LogSamples() []string                    // Test samples for validation
}
```

**Fingerprinting** is the key optimization. Each parser defines a fast check (typically a string match or regex on the program name or message prefix) that determines whether it can handle a given message. The serial pipeline tests fingerprints in sequence and stops at the first match, avoiding unnecessary work.

!!! info "Early Exit Optimization"
    With 200+ parsers, the serial pipeline with early exit achieves ~99.6% reduction in processing operations compared to running all parsers on every message. Most messages match within the first few fingerprint tests.

## Worker Pool Configuration

The SerialParserPipeline uses configurable worker pools for parallel processing:

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `SERIAL_PARSER_WORKERS` | 10 | Number of serial parser workers |
| `FORMAT_MAX_WORKERS` | 30 | Format detection workers |
| `OUTPUT_ARTIFACT_MAX_WORKERS` | 10 | Output transformation workers |

## Performance

- **Throughput**: >2000 messages/second with 200+ active parsers
- **Per-message latency**: <2ms for optimized parsers
- **Success rate**: 100% deterministic processing (zero message loss)
- **Buffer sizes**: 20K event buffers for stable throughput

## Unknown Message Handling

Messages that no parser can match are published to the `artifacts.unknown` subject. These messages are available for monitoring and analysis to identify new log formats that need parser development.

```bash
# Check unknown message volume
docker exec broker-edge-svc nats stream info DATA | grep unknown
```

## Configuration

Parser enable/disable state is managed via the NATS KV `PARSERS` bucket. Parsers can be toggled through the [Conductor UI Parser Management page](ui/parsers.md).

!!! warning
    Parser connectors require valid configuration from the NATS KV bucket to function. If the broker is unavailable during startup, parsers will wait for configuration delivery before processing any messages.