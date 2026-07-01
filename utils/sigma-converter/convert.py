#!/usr/bin/env python3
"""
WitFoo Sigma Rule Conversion Pipeline

Converts WitFoo Sigma detection rules to platform-specific query languages
using pySigma backends. Supports Splunk SPL, OpenSearch DQL, and Microsoft
Sentinel KQL output.

Usage:
    python convert.py --target splunk --output ../../docs/detection-rules/splunk/
    python convert.py --target opensearch --output ../../docs/detection-rules/opensearch/
    python convert.py --target sentinel --output ../../docs/detection-rules/sentinel/
    python convert.py --target all --validate-only
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path

import yaml

# NOTE: the pySigma collection/backends and the witfoo_pipeline module (which
# also imports pySigma) are imported lazily inside convert_rules(). They are only
# needed for the platform conversions — keeping them out of module scope lets the
# stdlib-only bundle path (generate_sigma_bundle) and the load_* helpers run
# without the heavy SIEM backend dependencies installed.


SIGMA_DIR = Path(__file__).parent.parent.parent / "docs" / "detection-rules" / "sigma"

# Default destination for the aggregate one-click Sigma download bundle.
SIGMA_BUNDLE_PATH = SIGMA_DIR.parent / "sigma_rules.zip"

DETECTION_CATEGORIES = [
    "network",
    "authentication",
    "malware",
    "data-loss",
    "cloud",
    "compliance",
    "infrastructure",
    "ids",
]


def load_detection_rules() -> list[Path]:
    """Discover all detection rule YAML files (excludes correlations and filters)."""
    rules = []
    for category in DETECTION_CATEGORIES:
        cat_dir = SIGMA_DIR / category
        if cat_dir.is_dir():
            rules.extend(sorted(cat_dir.glob("*.yml")))
    return rules


def load_all_rules() -> list[Path]:
    """Discover all rule YAML files including correlations and filters."""
    rules = load_detection_rules()
    for subdir in ["correlations", "filters"]:
        d = SIGMA_DIR / subdir
        if d.is_dir():
            rules.extend(sorted(d.glob("*.yml")))
    return rules


def is_detection_rule(rule_path: Path) -> bool:
    """Check if a YAML file is a standard detection rule (not correlation/filter)."""
    with open(rule_path) as f:
        data = yaml.safe_load(f)
    return data.get("type") not in ("correlation", "filter")


def generate_sigma_bundle(output_path: Path | None = None) -> int:
    """
    Package every Sigma source rule into a single, deterministic zip archive for
    one-click download from the docs site.

    Every ``*.yml`` under ``docs/detection-rules/sigma/<category>/`` is included —
    all categories, including correlations and filters — under arcnames
    ``sigma/<category>/<file>.yml``.

    The archive is byte-for-byte reproducible so the committed binary only changes
    when a rule's *content* changes (never from build-time mtime or zlib-version
    drift):
      * categories and files are iterated in sorted order;
      * every entry uses a fixed ``date_time`` of 1980-01-01 (the zip epoch);
      * entries are stored uncompressed (``ZIP_STORED``) with pinned
        ``create_system``/``external_attr`` — independent of the host OS and any
        deflate implementation.

    Args:
        output_path: Destination zip path. Defaults to
            ``docs/detection-rules/sigma_rules.zip`` (``SIGMA_BUNDLE_PATH``).

    Returns:
        Number of rule entries written to the archive.
    """
    if output_path is None:
        output_path = SIGMA_BUNDLE_PATH

    # Collect (arcname, source) for every rule, sorted for a stable entry order.
    entries: list[tuple[str, Path]] = []
    for category in sorted(p.name for p in SIGMA_DIR.iterdir() if p.is_dir()):
        cat_dir = SIGMA_DIR / category
        for rule_path in sorted(cat_dir.glob("*.yml")):
            arcname = f"sigma/{category}/{rule_path.name}"
            entries.append((arcname, rule_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for arcname, rule_path in entries:
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3  # Unix — pin for cross-platform reproducibility
            info.external_attr = 0o644 << 16  # regular file, rw-r--r--
            zf.writestr(info, rule_path.read_bytes())

    print(f"Wrote Sigma bundle: {output_path} ({len(entries)} rules)")
    return len(entries)


def convert_rules(target: str, output_dir: Path | None, validate_only: bool) -> bool:
    """
    Convert Sigma rules to the specified platform target.

    Args:
        target: One of 'splunk', 'opensearch', 'sentinel'
        output_dir: Directory to write converted rules (None if validate_only)
        validate_only: If True, only check that conversion succeeds

    Returns:
        True if conversion succeeded, False otherwise
    """
    # Lazy import (see module-level note): only the platform conversions need the
    # pySigma backends, so importing here keeps the module usable without them.
    from sigma.collection import SigmaCollection
    from sigma.backends.splunk import SplunkBackend
    from sigma.backends.opensearch import OpensearchLuceneBackend
    from sigma.backends.microsoft365defender import KustoBackend

    from witfoo_pipeline import (
        witfoo_splunk_pipeline,
        witfoo_opensearch_pipeline,
        witfoo_sentinel_pipeline,
    )

    detection_rules = load_detection_rules()
    if not detection_rules:
        print(f"ERROR: No detection rules found in {SIGMA_DIR}")
        return False

    print(f"\n{'='*60}")
    print(f"Converting {len(detection_rules)} detection rules to {target}")
    print(f"{'='*60}")

    # Build SigmaCollection from detection rules only
    # (correlation/filter rules are validated separately)
    sigma_collection = SigmaCollection.load_ruleset(
        [str(p) for p in detection_rules]
    )

    if target == "splunk":
        backend = SplunkBackend(processing_pipeline=witfoo_splunk_pipeline())
        ext = ".spl"
    elif target == "opensearch":
        backend = OpensearchLuceneBackend(processing_pipeline=witfoo_opensearch_pipeline())
        ext = ".dql"
    elif target == "sentinel":
        backend = KustoBackend(processing_pipeline=witfoo_sentinel_pipeline())
        ext = ".kql"
    else:
        print(f"ERROR: Unknown target '{target}'")
        return False

    success_count = 0
    error_count = 0
    results = {}

    for rule in sigma_collection:
        rule_id = rule.id if rule.id else "unknown"
        rule_title = rule.title if rule.title else "Untitled"
        try:
            converted = backend.convert_rule(rule)
            if converted:
                query = converted[0] if isinstance(converted, list) else converted
                results[rule_id] = {
                    "title": rule_title,
                    "query": query,
                }
                success_count += 1
            else:
                print(f"  WARNING: Empty output for {rule_id} ({rule_title})")
                error_count += 1
        except Exception as e:
            print(f"  ERROR converting {rule_id} ({rule_title}): {e}")
            error_count += 1

    print(f"\nResults: {success_count} succeeded, {error_count} failed")

    if validate_only:
        return error_count == 0

    # Write output files
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        rules_dir = output_dir / "rules"
        rules_dir.mkdir(exist_ok=True)

        for rule_id, data in results.items():
            # Sanitize filename from rule ID
            filename = str(rule_id).replace("-", "_") + ext
            out_path = rules_dir / filename
            with open(out_path, "w") as f:
                f.write(f"# Rule: {data['title']}\n")
                f.write(f"# ID: {rule_id}\n")
                f.write(f"# Generated by WitFoo Sigma Converter\n\n")
                f.write(str(data["query"]) + "\n")
            print(f"  Wrote {out_path}")

        # Write index file with all queries
        index_path = output_dir / f"all_rules{ext}"
        with open(index_path, "w") as f:
            f.write(f"# WitFoo Sigma Rules — {target.title()} Queries\n")
            f.write(f"# Generated by WitFoo Sigma Converter\n")
            f.write(f"# Total rules: {len(results)}\n\n")
            for rule_id, data in results.items():
                f.write(f"\n# --- {data['title']} ({rule_id}) ---\n")
                f.write(str(data["query"]) + "\n")
        print(f"  Wrote combined index: {index_path}")

    return error_count == 0


def validate_correlation_rules() -> bool:
    """Validate correlation rules parse as valid YAML with required fields."""
    corr_dir = SIGMA_DIR / "correlations"
    if not corr_dir.is_dir():
        print("No correlation rules directory found")
        return True

    valid_types = {"event_count", "value_count", "temporal", "temporal_ordered"}
    rules = sorted(corr_dir.glob("*.yml"))
    print(f"\nValidating {len(rules)} correlation rules...")

    ok = True
    for rule_path in rules:
        with open(rule_path) as f:
            data = yaml.safe_load(f)
        rule_type = data.get("type", "")
        if rule_type not in valid_types:
            print(f"  ERROR: {rule_path.name} has invalid type: '{rule_type}' (expected one of {valid_types})")
            ok = False
        elif not data.get("rules"):
            print(f"  ERROR: {rule_path.name} missing 'rules' field")
            ok = False
        else:
            print(f"  OK: {rule_path.name} ({data.get('title', 'untitled')})")
    return ok


def validate_filter_rules() -> bool:
    """Validate filter rules parse as valid YAML with required fields."""
    filt_dir = SIGMA_DIR / "filters"
    if not filt_dir.is_dir():
        print("No filter rules directory found")
        return True

    rules = sorted(filt_dir.glob("*.yml"))
    print(f"\nValidating {len(rules)} filter rules...")

    ok = True
    for rule_path in rules:
        with open(rule_path) as f:
            data = yaml.safe_load(f)
        if not data.get("detection"):
            print(f"  ERROR: {rule_path.name} missing 'detection' field")
            ok = False
        elif not data.get("logsource"):
            print(f"  ERROR: {rule_path.name} missing 'logsource' field")
            ok = False
        else:
            print(f"  OK: {rule_path.name} ({data.get('title', 'untitled')})")
    return ok


def main():
    parser = argparse.ArgumentParser(
        description="WitFoo Sigma Rule Conversion Pipeline"
    )
    parser.add_argument(
        "--target",
        choices=["splunk", "opensearch", "sentinel", "all"],
        help="Target SIEM platform",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for converted rules",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate conversion succeeds (no file output)",
    )
    parser.add_argument(
        "--bundle",
        action="store_true",
        help="Generate the aggregate Sigma rules zip (all source rules)",
    )
    parser.add_argument(
        "--bundle-output",
        type=Path,
        help="Destination for --bundle (default: docs/detection-rules/sigma_rules.zip)",
    )
    args = parser.parse_args()

    if not args.target and not args.bundle:
        parser.error("one of --target or --bundle is required")

    all_ok = True

    if args.target:
        targets = (
            ["splunk", "opensearch", "sentinel"]
            if args.target == "all"
            else [args.target]
        )
        for target in targets:
            output = args.output if args.target != "all" else None
            ok = convert_rules(target, output, args.validate_only or args.target == "all")
            if not ok:
                all_ok = False

        # Always validate correlation and filter rules
        if not validate_correlation_rules():
            all_ok = False
        if not validate_filter_rules():
            all_ok = False

    if args.bundle:
        generate_sigma_bundle(args.bundle_output)

    if all_ok:
        print(f"\n{'='*60}")
        print("ALL VALIDATIONS PASSED")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("SOME VALIDATIONS FAILED")
        print(f"{'='*60}")
        sys.exit(1)


if __name__ == "__main__":
    main()
