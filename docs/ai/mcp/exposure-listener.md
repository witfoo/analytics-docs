# Exposure Listener (Port 8444)

The MCP exposure listener is a separate, optional reverse-proxy listener on port 8444 that serves `/mcp` and the app sign-in endpoints and nothing else, so it is the only listener a hosted marketplace client needs to reach.

## Why use it

A hosted marketplace client, such as claude.ai, connects to the appliance from its vendor's servers. The `:443` listener also serves the UI, the API and the WebSockets. The exposure listener lets you publish MCP without publishing those.

For app sign-in, the user's browser must still reach the consent page on the main listener. See [App Sign-in (OAuth 2.1)](oauth.md).

## What it serves

Exactly five paths, for every standard HTTP method, handled the same way as on `:443`:

| Path | What it is |
| --- | --- |
| `/mcp` | The MCP endpoint |
| `/.well-known/oauth-protected-resource` | Protected-resource metadata |
| `/.well-known/oauth-protected-resource/mcp` | Protected-resource metadata |
| `/.well-known/oauth-authorization-server` | Authorization-server metadata |
| `/oauth/token` | The token endpoint for app sign-in |

Every other path answers `404` and reaches no service: the UI, `/api`, `/ws/chat` and the other WebSockets, `/health` and `/metrics`. A near miss such as `/mcp/` or `/MCP` answers `404`, not a redirect, and so does `OPTIONS` on any other path. The consent page and every other sign-in route stay on `:443`.

Where the appliance is not set up for app sign-in, the four sign-in paths answer `404`.

Authentication does not change: `/mcp` needs a personal key or an access token, and the user's `mcp:connect` permission, exactly as on `:443`. A key in the URL is refused with `400`.

## Turn it on (WFA appliance)

Requirements: WFA 2.5.1 or later (install WFA 2.5.3) and analytics 1.2.0 images. An older reverse proxy ignores the setting.

1. **Check that host port 8444 is free.** See [Port conflicts](#port-conflicts).
2. Set both switches in `/witfoo/configs/node.json`:

    ```json
    {
      "mcp_http_enabled": true,
      "mcp_exposure_enabled": true
    }
    ```

3. Restart WFA:

    ```bash
    wfa restart
    ```

WFA then sets `MCP_EXPOSURE_PORT=8444` on the reverse-proxy container, `analytics-reverse-proxy-svc`, and publishes host port **8444** on the host's IPv4 addresses (not on IPv6). The port is fixed; your perimeter may map public 443 to it.

!!! note "Exposure alone does nothing"
    WFA opens the listener only when `mcp_http_enabled` is also `true`. Without the HTTP transport, `/mcp` would answer `404`.

### Verify

1. `docker inspect analytics-reverse-proxy-svc` shows `MCP_EXPOSURE_PORT=8444` and the 8444 binding.
2. `docker logs analytics-reverse-proxy-svc` shows `Starting MCP exposure listener on …`, not an `[ERROR] MCP exposure listener …` line.
3. Send a request. There is no health route, so every path outside the five answers `404`:

    ```bash
    curl -sk -o /dev/null -w '%{http_code}\n' https://<host>:8444/
    ```

    This prints `404` when the listener is serving. Use `http://` on an appliance configured for plain HTTP. A reset, an empty reply or a failed TLS handshake means the listener is not serving. Do not test with a bare TCP connection from the appliance itself: Docker can accept it even when nothing listens.

### Port conflicts

- **A WFA binding already uses 8444** (for example `"reverse_proxy_port": 8444`): WFA does not open the listener, and logs one line in `journalctl -u wfad`: `MCP exposure listener not enabled: its host port is already bound on this node`. The line is not at error priority, so `journalctl -p err` does not show it.
- **A process outside WFA holds 8444** when WFA starts: the reverse-proxy container cannot start, and the UI is down with it. It stays down after the port is freed until WFA restarts. Free the port, or clear `mcp_exposure_enabled`, then run:

    ```bash
    systemctl restart wfad
    ```

## Turn it on (Docker Compose)

Apply the overlay, which sets both switches:

```bash
docker compose -f docker-compose.yml -f docker-compose.mcp-exposure.yml up -d
```

## TLS and load balancers

- **Certificate.** With TLS configured, the listener presents the same certificate as `:443`. By default that is a self-signed certificate (`CN=precinct.local`) that the reverse proxy generates in its container. On a WFA appliance a new one is generated whenever WFA recreates the container, which it does at every WFA start and update.
- **Clients that validate certificates.** A marketplace client that checks the server certificate needs TLS terminated in front of port 8444, by a proxy or load balancer that holds a certificate for the name you publish.
- **Plain HTTP.** When the appliance is configured for plain HTTP (`disable_tls` or `LB_MODE`), the listener is plain HTTP too, and port 8444 carries personal keys, authorization codes and tokens in cleartext. Let only your load balancer reach it.

!!! warning "Declare your load balancer first"
    Declare the proxy or load balancer in front of port 8444 before you point clients at it: `trusted_proxies` in `node.json` on a WFA appliance (WFA 2.5.1 or later), or `WF_TRUSTED_PROXIES` on Docker Compose. List the load balancer's own address, not a private-network range such as `10.0.0.0/8`. Until it is declared that way, every client behind it shares one failed-authentication count on `/mcp`, so 100 failures from one client refuse the others.

    A re-run of `wfa configure` or `wfa fetch` keeps the MCP settings but writes `node.json` without `trusted_proxies`. Add it again after each re-run, then run `wfa restart`.

## Restrict who can reach it

!!! danger "The product restricts no sources"
    The exposure listener has no source-address allow list. Restricting who can reach it is your job:

    - Forward only port 8444 to the marketplace. The listener changes nothing about the appliance's other ports, and does not protect them.
    - Restrict the sources at your perimeter, or on the host in the `DOCKER-USER` chain or an equivalent. A port Docker publishes is not filtered by INPUT-chain rules managed through `ufw` or `firewalld`, so a rule there can look like a restriction and not be one.
    - Prove the restriction with a negative probe: a connection from a source you have not allowed must fail.

For a hosted app, admit the vendor's published address range. See [App Sign-in (OAuth 2.1)](oauth.md).

## Licensing

The exposure listener is not tied to a SKU. The MCP requests it carries are checked against the licence as on `:443`. See [MCP Licensing](licensing.md).

## Related pages

- [Connecting AI Clients & Marketplaces](connect-clients.md)
- [AI-Connector Relay](relay.md): reach the appliance without an inbound port.
