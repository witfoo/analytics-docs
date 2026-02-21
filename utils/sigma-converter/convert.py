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
from pathlib import Path

import yaml
from sigma.collection import SigmaCollection
from sigma.backends.splunk import SplunkBackend
from sigma.backends.opensearch import OpensearchLuceneBackend
from sigma.backends.microsoft365defender import KustoBackend

from witfoo_pipeline import (
    witfoo_splunk_pipeline,
    witfoo_opensearch_pipeline,
    witfoo_sentinel_pipeline,
)


SIGMA_DIR = Path(__file__).parent.parent.parent / "docs" / "detection-rules" / "sigma"

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
        required=True,
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
    args = parser.parse_args()

    targets = (
        ["splunk", "opensearch", "sentinel"] if args.target == "all" else [args.target]
    )

    all_ok = True

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
