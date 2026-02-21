#!/bin/bash
# Validates integration guide structure for PR140
# Usage: ./scripts/validate-integration-guides.sh
set -e

DOCS_DIR="docs/conductor/integrations"
REQUIRED_SECTIONS=("## Prerequisites" "## Step 1:" "## Step 2:" "## Step 3:" "## Troubleshooting")
ERRORS=0

echo "=== PR140 Integration Guide Validation ==="
echo ""

# Check directory exists
if [ ! -d "$DOCS_DIR" ]; then
  echo "FAIL: $DOCS_DIR directory not found"
  exit 1
fi

# Count guide files (excluding index and common-troubleshooting)
GUIDE_COUNT=$(find "$DOCS_DIR" -name "*.md" ! -name "index.md" ! -name "common-troubleshooting.md" | wc -l)
echo "Found $GUIDE_COUNT guide files"

# Check all nav-referenced files exist
echo ""
echo "--- Checking nav references ---"
for f in $(grep -oP 'conductor/integrations/\S+\.md' mkdocs.yml 2>/dev/null); do
  if [ ! -f "docs/$f" ]; then
    echo "MISSING: docs/$f (referenced in mkdocs.yml)"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check required sections in each guide
echo ""
echo "--- Checking required sections ---"
for f in "$DOCS_DIR"/*.md; do
  [ "$(basename "$f")" = "index.md" ] && continue
  [ "$(basename "$f")" = "common-troubleshooting.md" ] && continue

  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$f"; then
      echo "MISSING SECTION: '$section' in $(basename "$f")"
      ERRORS=$((ERRORS + 1))
    fi
  done

  # Check frontmatter tags
  if ! head -10 "$f" | grep -q "integration"; then
    echo "MISSING TAG: 'integration' in frontmatter of $(basename "$f")"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check for orphaned files
echo ""
echo "--- Checking for orphaned files ---"
for f in "$DOCS_DIR"/*.md; do
  rel="${f#docs/}"
  if ! grep -q "$rel" mkdocs.yml 2>/dev/null; then
    echo "ORPHANED: $(basename "$f") not in mkdocs.yml nav"
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [ $ERRORS -gt 0 ]; then
  echo "FAILED: $ERRORS errors found"
  exit 1
fi

echo "PASSED: All integration guides validated ($GUIDE_COUNT guides)"
