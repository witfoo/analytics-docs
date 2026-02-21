# Troubleshooting

This guide covers common issues, diagnostic procedures, and resolution steps for WitFoo Conductor deployments.

## Diagnostic Tools

### WFA Diagnostics

Run `wfa diag` to verify connectivity and system health:

```bash
sudo wfa diag
```

This checks:

- **Grafana Cloud** — metrics endpoint connectivity
- **WitFoo Intel** — support and remote jobs
- **WitFoo Library** — support pack upload
- **WitFoo Licensing** — license validation
- **Docker Registry** — container image access
- **Cassandra Seeds** — database connectivity (port 9042)
- **Disk Usage** — warns if any partition exceeds 80%

### Support Bundle

Generate a comprehensive support bundle with `wfa support`:

```bash
sudo wfa support
```

Collects 19 diagnostic categories including Docker state, system logs, Cassandra diagnostics, NATS stream info, network configuration, and extended service logs. Automatically uploads to WitFoo support if a license is configured.

## Common Issues

### Services Not Starting

```bash
# Check service status
sudo wfa status

# Check container state
docker ps -a

# Check service logs
docker logs <container-name> --tail=100
```

### NATS Connectivity

If services cannot connect to the broker:

```bash
# Verify broker-edge is running
docker ps | grep broker-edge

# Check NATS streams
docker exec broker-edge-svc nats stream ls

# Check NATS server info
docker exec broker-edge-svc nats server info
```

### Parser Errors

If messages are not being parsed:

1. Check the unknown stream for unparsed messages
2. Verify parsers are enabled in the Conductor UI (`/admin/settings/processors`)
3. Check signal-parser logs: `docker logs signal-parser-svc --tail=200`

### Memory Issues

On constrained nodes (8 GB RAM), containers may experience OOM kills:

```bash
# Check container memory usage
docker stats --no-stream

# Check system memory
free -h
```

!!! tip
    For nodes with limited memory, consider reducing the number of enabled parsers and integrations.

## Integration-Specific Troubleshooting

For issues related to specific data source integrations (authentication errors,
rate limiting, missing data), see the per-vendor troubleshooting sections in the
[Integration Enablement Guides](integrations/index.md), or the shared
[Common Integration Troubleshooting](integrations/common-troubleshooting.md)
page covering connection, authentication, rate limiting, and data flow diagnostics.

## Log Locations

| Source | Location |
|--------|----------|
| WFA daemon | `journalctl -u wfad` |
| Container logs | `docker logs <container-name>` |
| Container log files | `/logs/<service-name>/` |
| NATS logs | `docker logs broker-edge-svc` |
