# TLS Configuration

Configure HTTPS for WitFoo Analytics.

## Quick Setup

### Self-Signed (Development)

WitFoo Analytics generates a self-signed certificate on first boot. This is suitable for development but will show browser warnings.

### Custom Certificate

Upload a trusted certificate through the web UI or API:

1. Navigate to **Admin** > **Settings** > **Certificates**
2. Upload your certificate (PEM) and private key
3. The reverse proxy hot-reloads the new certificate

### Let's Encrypt

Use an external reverse proxy (nginx, Caddy, Traefik) with Let's Encrypt in front of WitFoo Analytics.

## Hot-Reload

The reverse proxy supports zero-downtime certificate rotation using the `tls.Config.GetCertificate` callback. When a certificate is uploaded via the API, it takes effect immediately.

## Load Balancers and Trusted Proxies

When a load balancer or another proxy terminates TLS in front of WitFoo Analytics, declare it to the reverse proxy so that the reverse proxy can read the real client address from `X-Forwarded-For`:

| Deployment | Setting |
| --- | --- |
| Docker Compose or a standalone stack | `WF_TRUSTED_PROXIES`, a comma-separated list of addresses or CIDRs |
| WFA appliance (WFA 2.5.1 or later) | `trusted_proxies` in `/witfoo/configs/node.json`, for example `"trusted_proxies": ["192.0.2.10"]` |

With the list unset, what the reverse proxy trusts depends on how it serves:

| Edge | Trusted forwarders when the list is unset |
| --- | --- |
| TLS edge (TLS enabled, not in `LB_MODE`). This is the default on the compose files and on a WFA appliance in HTTPS mode | None. Every client is keyed on its own connection address, and no client can assert an address |
| Behind a load balancer (`LB_MODE`, or TLS not enabled) | For this release only, any peer in `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` and `127.0.0.1`, with a startup WARN. This compatibility list is removed in a later release |

Other rules:

- The reverse proxy reads the client address from `X-Forwarded-For` only. A load balancer that sends only `X-Real-IP` is keyed on its own address.
- Set the list to the load balancer's own address. Until it is declared, every client behind the load balancer shares one failed-authentication count on the MCP endpoint (`/mcp`).

!!! warning "Re-running `wfa configure` or `wfa fetch` drops `trusted_proxies`"
    A re-run of `wfa configure` or `wfa fetch` (including `wfa configure --license-file`) writes `node.json` without `trusted_proxies`. Add it again after each re-run, then run `sudo wfa restart`.

## MCP Exposure Listener (Port 8444)

The optional MCP exposure listener on port 8444 serves the MCP endpoint and the app sign-in endpoints for marketplace AI clients. It uses the same certificate as port 443, and serves plain HTTP when the appliance is configured for plain HTTP (`disable_tls` or `LB_MODE`).

The default certificate is self-signed, so a client that checks the server certificate needs TLS terminated in front of port 8444 by a proxy or load balancer that holds a certificate for the name you publish. Declare that proxy or load balancer as a trusted proxy (above) before you point clients at it. See [MCP Exposure Listener](../ai/mcp/exposure-listener.md).

## Internal TLS

Inter-service communication within the Docker network uses plaintext by default. For enhanced security, configure TLS between services using the certificate management API.
