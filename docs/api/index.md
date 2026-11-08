# API Reference

WitFoo Analytics exposes a RESTful API for all platform operations. The API follows consistent patterns for authentication, request/response format, pagination, and error handling.

## Base URL

```text
https://<appliance>/api/v1
```

Call the API through the reverse proxy on port 443. The endpoint tables write paths from `/v1`, so `/v1/artifacts` is `https://<appliance>/api/v1/artifacts`.

## Request Flow

```text
Browser/Client → Reverse Proxy (:443) → API (:8080) → Incident Engine (:8082) → Cassandra
```

The API service acts as a gateway adding JWT authentication, permission checks, and request routing. The Incident Engine contains all business logic.

In 1.2.0 the API's own port is not reachable from outside the appliance: a WFA appliance does not publish it, and on Docker Compose it listens on `INTERNAL_LISTEN_IP` (`127.0.0.1` by default). See [Published addresses](../reference/environment-variables.md#published-addresses-docker-compose).

## Sections

- [Authentication](authentication.md) — JWT token management
- [Standards](standards.md) — Request/response conventions
- [Errors](errors.md) — Error codes and handling
- [Endpoints](endpoints/artifacts.md) — Full endpoint reference
