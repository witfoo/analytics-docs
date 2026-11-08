# Configuration

A Docker Compose or standalone WitFoo Analytics stack is configured through environment variables in the `.env` file at the root of the checkout. `docker/.env` is a link to it. A value exported in the shell you run `docker compose` from wins over the file.

On a WFA-managed appliance, WFA builds every container's environment, and you configure the appliance through `node.json` and `wfa configure` instead. See [WFA deployment](wfa.md).

The full list of variables is in the [Environment Variables](../reference/environment-variables.md) reference.

## Required Variables

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | The secret the session key is derived from. Identical on the reverse proxy, api, incident-engine and dispatcher |
| `AUTH_CONFIG_ENCRYPTION_KEY` | The key that seals the secrets stored in the database. 32 random bytes, base64: `openssl rand -base64 32`. **Required from 1.2.0**, with no default |
| `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS` | Optional. The key or keys `AUTH_CONFIG_ENCRYPTION_KEY` replaced, comma-separated, so data sealed under them stays readable |

!!! warning "Set the encryption key before you upgrade a Compose stack to 1.2.0"
    The compose files no longer carry a default for `AUTH_CONFIG_ENCRYPTION_KEY`. Every `docker compose` command refuses to run until it is set, and the services refuse a value that is not 32 bytes of base64, or the value earlier compose files shipped. The launch scripts generate a key for you when none is set.

    A stack started from an earlier compose file that never set a key of its own must also list the old shipped value as `AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS`. Follow [Upgrading to 1.2.0](../reference/upgrade-1.2.0.md) before you start 1.2.0.

    On more than one node, every node that runs the api or incident-engine against the same Cassandra cluster needs the same two values. Back the key up with the database, and store the two apart.

## Core Variables

| Variable | Default | Description |
| --- | --- | --- |
| `CASSANDRA_HOSTS` | `cassandra:9042` | Cassandra contact points |
| `NATS_URL` | `nats://nats:4222` | NATS connection URL |
| `ORG_ID` | `development` | Organization identifier used in metric labels |

## Published Addresses

The compose files publish fixed ports. Two variables choose the host address they are published on:

| Variable | Default | Services |
| --- | --- | --- |
| `LISTEN_IP` | `0.0.0.0` in the compose files (the example `.env` sets `127.0.0.1`) | Reverse proxy (443, 8081), artifact receiver (8090, 8443), Cassandra (9042) |
| `INTERNAL_LISTEN_IP` | `127.0.0.1` | api (8080), incident-engine (8082), dispatcher (8003), UI (3000), NATS (4222, 8222), Conductor broker edge (4223, 8223), Prometheus (9090), Grafana (3001) |

!!! warning "Firewall Cassandra"
    `LISTEN_IP` still publishes Cassandra's client port. Restrict it at the host firewall to the nodes that need it.

Before 1.2.0 every service was published on `LISTEN_IP`. From 1.2.0 the api, incident-engine, NATS, Prometheus and Grafana are reachable from the host only, unless you set `INTERNAL_LISTEN_IP`. The full port list of each compose file is in the [Docker Compose Reference](docker-compose.md).

## Load Balancers and Trusted Proxies

`WF_TRUSTED_PROXIES` names the load balancers whose `X-Forwarded-For` the reverse proxy believes. Set it on the reverse proxy service, as the commented line in `docker-compose.lb.yml` shows:

```yaml
reverse-proxy:
  environment:
    - WF_TRUSTED_PROXIES=192.0.2.10   # the load balancer's address
```

- With it unset, a TLS edge believes no forwarder: every client is keyed on its own TCP address.
- An edge without TLS, or in LB mode (`LB_MODE=true`), still trusts the private ranges for one more release, with a startup WARN. Set the list to end the WARN and trust only your load balancer.
- A load balancer that sends only `X-Real-IP` is keyed on its own address.
- Behind a load balancer, set the list before you enable the MCP exposure listener. Otherwise every client behind it shares one failed-authentication count on `/mcp`.

## Security Variables

| Variable | Description |
| --- | --- |
| `JWT_SECRET` | Session key secret |
| `AUTH_CONFIG_ENCRYPTION_KEY` | XChaCha20-Poly1305 master key for stored secrets (base64, 32 bytes) |
| `ANALYTICS_SECRET` | HMAC-SHA256 shared secret for Conductor auth |
| `WF_JWT_SECRET` | Conductor single sign-on secret (AIO plus Conductor) |
| `SECRET_KEY` | Conductor UI and Console UI session key. Leave it unset, or set 64 hexadecimal characters (`openssl rand -hex 32`). Values from earlier releases or example files are refused |

## Feature Flags

| Variable | Default | Description |
| --- | --- | --- |
| `WF_LICENSE` | (empty) | Appliance license key, for framework sync |
| `VITE_UI_MODULES` | `all` | UI module visibility: `all`, `search_only`, `search_observer` |
| `WF_MCP_HTTP_ENABLED` | `false` | Serves the HTTP MCP transport at `/mcp`. See [MCP Configuration](../ai/mcp/configuration.md) |
| `GRAFANA_REMOTE_WRITE_URL` | (empty) | Enable Prometheus remote write to Grafana Cloud |

## Cassandra Tuning

| Variable | Default | Description |
| --- | --- | --- |
| `JVM_EXTRA_OPTS` | (unset) | JVM options the Cassandra image appends last; set the heap here, for example `-Xms4G -Xmx4G`. `CASSANDRA_HEAP` does not change the heap |
| `DATA_NODE_HOSTS` | `cassandra:9042` | External Cassandra hosts for processing nodes |

## Example .env

```bash
JWT_SECRET=<output of: openssl rand -hex 32>
AUTH_CONFIG_ENCRYPTION_KEY=<output of: openssl rand -base64 32>
# Only when replacing a key, or moving a stack that never set one:
# AUTH_CONFIG_ENCRYPTION_KEY_PREVIOUS=<the key it replaces>
LISTEN_IP=127.0.0.1
# INTERNAL_LISTEN_IP=127.0.0.1
```
