# API Reference

WitFoo Analytics exposes a RESTful API for all platform operations. The API follows consistent patterns for authentication, request/response format, pagination, and error handling.

## Base URL

```text
http://localhost:8080/api/v1
```

## Request Flow

```text
Browser/Client → Reverse Proxy (:8080) → API Gateway (:8090) → Incident Engine (:8082) → Cassandra
```

The API service acts as a gateway adding JWT authentication, permission checks, and request routing. The Incident Engine contains all business logic.

## Sections

- [Authentication](authentication.md) — JWT token management
- [Standards](standards.md) — Request/response conventions
- [Errors](errors.md) — Error codes and handling
- [Endpoints](endpoints/artifacts.md) — Full endpoint reference
