# Certificates

Manage TLS certificates for HTTPS access and internal service communication.

## Certificate Management

### Upload Certificate

1. Navigate to **Admin** > **Settings** > **Certificates**
2. Click **Upload Certificate**
3. Provide the certificate file (PEM format) and private key
4. Click **Save**

### Certificate Validation

Uploaded certificates are validated before acceptance:

- X.509 format verification
- Key pair matching (certificate + private key)
- Expiration date check

### Hot-Reload

The reverse proxy supports certificate hot-reload. When a new certificate is uploaded, it takes effect immediately without restarting services. This uses the `tls.Config.GetCertificate` callback pattern.

## Self-Signed Certificates

For development and testing, WitFoo Analytics generates a self-signed certificate on first boot. Replace it with a trusted certificate for production use.

## Certificate Storage

- Certificates are stored in Cassandra
- Private keys are encrypted at rest using AES-256-GCM
- File permissions: private keys 0600, certificates 0644
