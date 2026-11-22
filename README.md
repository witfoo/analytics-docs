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
(set at the CDN; that file is the copy to paste there). Neither its `script-src` nor its
`style-src` has `'unsafe-inline'`, so a page must not carry inline script or inline style:

- `hooks/csp.py` moves the theme's inline scripts and its `<style>` into files at build time.
  The strict build fails on an `onclick=`-style attribute, a `javascript:` URL, a `style=""`
  attribute or a `<style>` element in a page. Put behaviour in a `.js` file under `docs/assets/`
  and list it in `extra_javascript`; put styling in `docs/assets/stylesheets/extra.css`.
- `hooks/mermaid_static.py` serves the Mermaid diagrams pre-rendered (see [Diagrams](#diagrams)).

After a Material upgrade, the strict build may report that a content script's hash changed. Add
the new `'sha256-...'` to `script-src` in `content-security-policy.txt` and to the CDN rule before
merging, and remove the old one once the release is live. `hooks/csp.py` explains why those two
scripts stay inline.

## Diagrams

Write diagrams as ` ```mermaid ` blocks, as before. They are not drawn in the reader's browser:
Mermaid styles what it draws with inline styles, which the CSP blocks. Instead each diagram is
rendered ahead of time and committed under `diagrams/svg/`, and `hooks/mermaid_static.py` puts the
render in the page.

After you add or edit a diagram (or change a pin in `diagrams/renderer.json`, or the
`mkdocs-material` pin in `requirements.txt`), run:

```bash
./scripts/render-diagrams.sh
```

and commit `diagrams/svg/`. Until the renders match the diagrams, `mkdocs build --strict` (the PR
check) fails and names the diagram, and it also fails on a render that no page uses.

The script builds the site, opens each diagram page in headless Chromium with every request
answered from that build, lets the theme draw the diagrams with its own Mermaid configuration and
fonts, and saves the result. It needs Node.js 18+ and npm as well as the Python environment.
Mermaid, Playwright and Chromium are pinned in `diagrams/renderer.json` and the script refuses any
other version, so the same sources give the same files on every machine; a second run writes
nothing. It reaches no network the site build does not already use: Mermaid is the copy the
privacy plugin downloads for the build (checked against the pinned sha256), and Playwright comes
from `npm ci` with `scripts/diagrams/package-lock.json`. Run it once with `PLAYWRIGHT_INSTALL=1`
to download the pinned Chromium; the script's header lists the other options.

The site build itself (CI and the docs server) stays Python only: it reads the committed renders
and runs no browser and no Node.

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
