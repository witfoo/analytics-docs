# WitFoo Analytics Documentation

[![Deploy](https://github.com/witfoo/analytics-docs/actions/workflows/deploy.yml/badge.svg)](https://github.com/witfoo/analytics-docs/actions/workflows/deploy.yml)

User-facing documentation for [WitFoo Analytics](https://github.com/witfoo-dev/analytics), auto-generated and versioned on every release.

**Live site**: [witfoo.github.io/analytics-docs](https://witfoo.github.io/analytics-docs/)

## Local Development

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Serve locally (hot-reload)
mkdocs serve

# Build (strict mode — catches broken links/refs)
mkdocs build --strict
```

Visit [http://localhost:8000](http://localhost:8000) after running `mkdocs serve`.

## Versioning

Documentation is deployed via [mike](https://github.com/jimporter/mike) with version-locked releases:

- Each analytics release (e.g., `1.0.0`) generates and deploys its own documentation version
- The `latest` alias always points to the most recent release
- Previous versions remain accessible via the version selector dropdown

## Contributing

1. Edit markdown files in `docs/`
2. Test locally with `mkdocs serve`
3. Submit a PR — CI validates with `mkdocs build --strict`, markdownlint, and lychee link checking
4. Merge to main triggers automatic deployment

## Structure

```
docs/
  getting-started/    # Installation, first login, architecture
  user-guide/         # Signals, Graph, Observer, Reporter, CyberGrid, Health
  admin-guide/        # Users, roles, permissions, settings
  api/                # Authentication, standards, 23 endpoint groups
  ai/                 # AI assistant, MCP server
  deployment/         # Docker, WFA, TLS, monitoring
  reference/          # Permissions matrix, roles, env vars, schema
```

## Technology

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) v9.7.0
- [mike](https://github.com/jimporter/mike) for multi-version deployment
- GitHub Pages for hosting
- GitHub Actions for CI/CD
