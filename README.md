# WitFoo Analytics Documentation

[![Deploy](https://github.com/witfoo/analytics-docs/actions/workflows/deploy.yml/badge.svg)](https://github.com/witfoo/analytics-docs/actions/workflows/deploy.yml)

User-facing documentation for [WitFoo Analytics](https://github.com/witfoo-dev/analytics), auto-generated and versioned on every release.

**Live site**: [docs.witfoo.com](https://docs.witfoo.com/)

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

## Content-Security-Policy

The site is served with the CSP in [`content-security-policy.txt`](content-security-policy.txt)
(set at the CDN; that file is the copy to paste there). Its `script-src` has no `'unsafe-inline'`,
so a page must not carry inline script: `hooks/csp.py` moves the theme's inline scripts into files
at build time, and the strict build fails on an `onclick=`-style attribute or a `javascript:` URL.
Put behaviour in a `.js` file under `docs/assets/` and list it in `extra_javascript`.

After a Material upgrade, the strict build may report that a content script's hash changed. Add
the new `'sha256-...'` to `script-src` in `content-security-policy.txt` and to the CDN rule before
merging, and remove the old one once the release is live. `hooks/csp.py` explains why those two
scripts stay inline.

## Structure

```text
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
