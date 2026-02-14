# TLS

Certificate management for HTTPS configuration.

## Endpoints

| Method | Path | Permission | Description |
| --- | --- | --- | --- |
| GET | `/v1/tls/certificates` | `settings:read` | List certificates |
| POST | `/v1/tls/certificates` | `settings:manage` | Upload certificate |
| DELETE | `/v1/tls/certificates/:id` | `settings:manage` | Delete certificate |
| GET | `/v1/tls/status` | `settings:read` | Current TLS status |

## Certificate Upload

```text
POST /v1/tls/certificates
Content-Type: multipart/form-data

cert: (PEM file)
key: (PEM private key file)
```

Certificates are validated (X.509 format, key pair match) before acceptance. Private keys are encrypted at rest.
