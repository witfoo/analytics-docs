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

## Internal TLS

Inter-service communication within the Docker network uses plaintext by default. For enhanced security, configure TLS between services using the certificate management API.
