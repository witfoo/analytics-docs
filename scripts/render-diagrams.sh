#!/usr/bin/env bash
# Pre-render the Mermaid diagrams into diagrams/svg/ (see hooks/mermaid_static.py).
#
# Run it after adding or editing a ```mermaid block, or after changing a pin in
# diagrams/renderer.json or the mkdocs-material pin in requirements.txt, then commit
# diagrams/svg/. `mkdocs build --strict` fails until the renders match the sources.
#
# Needs: the docs' Python environment (requirements.txt), Node.js 18+ and npm, and the
# Chromium that the pinned Playwright drives. All three pins (Mermaid, Playwright, Chromium)
# are in diagrams/renderer.json and the renderer refuses any other version, so every author
# gets the same bytes. Only the person editing a diagram needs Node and Chromium: the site
# build itself (CI and the docs server) uses the committed renders and stays Python only.
#
# Network: none beyond the site build's own (the privacy plugin's downloads, which it
# caches in .cache/). Mermaid is the copy that build downloads, checked against the pinned
# sha256. Playwright is installed with `npm ci` from scripts/diagrams/package-lock.json,
# which uses the npm cache first. Chromium is installed only on request:
#   PLAYWRIGHT_INSTALL=1            run `playwright install chromium` first (downloads it)
#   PLAYWRIGHT_MODULE=/path/to/node_modules/playwright   use an existing install (same pin)
#   MERMAID_JS=/path/to/mermaid.min.js   use this copy of the pinned Mermaid instead
#   MERMAID_FETCH=1                 download the pinned Mermaid from unpkg instead
#   MKDOCS=/path/to/mkdocs          pick the mkdocs binary
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo"
mkdocs="${MKDOCS:-mkdocs}"
tool="$repo/scripts/diagrams"

if [ -z "${PLAYWRIGHT_MODULE:-}" ]; then
  npm --prefix "$tool" ci --prefer-offline --no-audit --no-fund >/dev/null
  if [ "${PLAYWRIGHT_INSTALL:-}" = "1" ]; then
    (cd "$tool" && npx --no-install playwright install chromium)
  fi
fi

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

echo "Building the site with the diagrams left to the theme..."
DOCS_MERMAID_CAPTURE=1 "$mkdocs" build --quiet --site-dir "$work/site"

site_url="$(sed -n 's/^site_url:[[:space:]]*//p' mkdocs.yml | head -n 1)"
echo "Rendering..."
node "$tool/render.cjs" "$work/site" "$repo/diagrams/svg" "$repo/diagrams/renderer.json" "$site_url"

echo "Checking with a strict build..."
# Not with --quiet: it hides the warnings, and then --strict does not fail.
"$mkdocs" build --strict --site-dir "$work/check"
echo "Done. Commit diagrams/svg/."
