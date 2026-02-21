"""
Sigma Rule Validation Test Suite

TDD tests for WitFoo Sigma detection rules. Run before writing rules to
establish the schema contract, then fill in rules until all tests pass.

Usage:
    pytest test_rules.py -v
"""

import glob
import os
import re
import uuid
from pathlib import Path

import pytest
import yaml

from witfoo_fields import VALID_FIELD_NAMES, WITFOO_LOGSOURCE

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
SIGMA_DIR = REPO_ROOT / "docs" / "detection-rules" / "sigma"

# Rule categories and expected subdirectories
RULE_CATEGORIES = [
    "network", "authentication", "malware", "data-loss",
    "cloud", "compliance", "infrastructure", "ids",
]
CORRELATION_DIR = "correlations"
FILTER_DIR = "filters"

# Required Sigma rule fields (SigmaHQ standard + WitFoo additions)
REQUIRED_FIELDS_DETECTION = {
    "title", "id", "custom_id", "status", "level", "description",
    "author", "date", "tags", "logsource", "detection",
}

REQUIRED_FIELDS_CORRELATION = {
    "title", "id", "custom_id", "status", "type", "rules",
}

REQUIRED_FIELDS_FILTER = {
    "title", "id", "custom_id", "status", "logsource", "detection",
}

# Valid Sigma status values
VALID_STATUSES = {"stable", "test", "experimental", "deprecated", "unsupported"}

# Valid Sigma levels
VALID_LEVELS = {"informational", "low", "medium", "high", "critical"}

# Pattern for WitFoo rule IDs
RULE_ID_PATTERN = re.compile(r"^wf-(net|auth|mal|dlp|cloud|comp|infra|ids|corr|filter)-\d{3}$")

# ATT&CK tag pattern
ATTACK_TAG_PATTERN = re.compile(r"^attack\.[a-z_]+$|^attack\.t\d{4}(\.\d{3})?$")


def collect_yaml_files(subdir: str) -> list[Path]:
    """Collect all .yml files from a Sigma subdirectory."""
    d = SIGMA_DIR / subdir
    if not d.exists():
        return []
    return sorted(d.glob("*.yml"))


def collect_all_detection_rules() -> list[Path]:
    """Collect all detection rule YAML files."""
    files = []
    for cat in RULE_CATEGORIES:
        files.extend(collect_yaml_files(cat))
    return files


def collect_all_correlation_rules() -> list[Path]:
    """Collect all correlation rule YAML files."""
    return collect_yaml_files(CORRELATION_DIR)


def collect_all_filter_rules() -> list[Path]:
    """Collect all filter rule YAML files."""
    return collect_yaml_files(FILTER_DIR)


def collect_all_rules() -> list[Path]:
    """Collect every Sigma YAML file."""
    return collect_all_detection_rules() + collect_all_correlation_rules() + collect_all_filter_rules()


def load_rule(path: Path) -> dict:
    """Load and parse a Sigma YAML rule file."""
    with open(path) as f:
        docs = list(yaml.safe_load_all(f))
    assert len(docs) >= 1, f"Empty YAML: {path}"
    return docs[0]


# ---------------------------------------------------------------------------
# Parametrized fixtures
# ---------------------------------------------------------------------------

def pytest_generate_tests(metafunc):
    """Generate test parameters for rule files."""
    if "detection_rule_path" in metafunc.fixturenames:
        rules = collect_all_detection_rules()
        ids = [p.stem for p in rules]
        metafunc.parametrize("detection_rule_path", rules, ids=ids)

    if "correlation_rule_path" in metafunc.fixturenames:
        rules = collect_all_correlation_rules()
        ids = [p.stem for p in rules]
        metafunc.parametrize("correlation_rule_path", rules, ids=ids)

    if "filter_rule_path" in metafunc.fixturenames:
        rules = collect_all_filter_rules()
        ids = [p.stem for p in rules]
        metafunc.parametrize("filter_rule_path", rules, ids=ids)

    if "any_rule_path" in metafunc.fixturenames:
        rules = collect_all_rules()
        ids = [p.stem for p in rules]
        metafunc.parametrize("any_rule_path", rules, ids=ids)


# ---------------------------------------------------------------------------
# Tests: Rule counts
# ---------------------------------------------------------------------------

class TestRuleCounts:
    """Verify minimum rule counts per category."""

    def test_total_detection_rules(self):
        rules = collect_all_detection_rules()
        assert len(rules) >= 55, f"Expected ≥55 detection rules, got {len(rules)}"

    def test_total_correlation_rules(self):
        rules = collect_all_correlation_rules()
        assert len(rules) >= 8, f"Expected ≥8 correlation rules, got {len(rules)}"

    def test_total_filter_rules(self):
        rules = collect_all_filter_rules()
        assert len(rules) >= 5, f"Expected ≥5 filter rules, got {len(rules)}"

    @pytest.mark.parametrize("category,min_count", [
        ("network", 12),
        ("authentication", 8),
        ("malware", 8),
        ("data-loss", 6),
        ("cloud", 6),
        ("compliance", 5),
        ("infrastructure", 5),
        ("ids", 5),
    ])
    def test_category_counts(self, category, min_count):
        rules = collect_yaml_files(category)
        assert len(rules) >= min_count, f"Category '{category}': expected ≥{min_count} rules, got {len(rules)}"


# ---------------------------------------------------------------------------
# Tests: Detection rule schema
# ---------------------------------------------------------------------------

class TestDetectionRuleSchema:
    """Validate individual detection rule YAML structure."""

    def test_yaml_parses(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        assert isinstance(rule, dict)

    def test_required_fields(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        missing = REQUIRED_FIELDS_DETECTION - set(rule.keys())
        assert not missing, f"Missing required fields: {missing}"

    def test_valid_status(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        assert rule.get("status") in VALID_STATUSES, f"Invalid status: {rule.get('status')}"

    def test_valid_level(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        assert rule.get("level") in VALID_LEVELS, f"Invalid level: {rule.get('level')}"

    def test_rule_id_is_uuid(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        rule_id = rule.get("id", "")
        try:
            uuid.UUID(str(rule_id))
        except ValueError:
            pytest.fail(f"Rule id '{rule_id}' is not a valid UUID")

    def test_custom_id_format(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        custom_id = rule.get("custom_id", "")
        assert RULE_ID_PATTERN.match(custom_id), f"custom_id '{custom_id}' doesn't match pattern wf-{{category}}-NNN"

    def test_logsource_product(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        logsource = rule.get("logsource", {})
        assert logsource.get("product") == WITFOO_LOGSOURCE["product"], \
            f"logsource.product must be 'witfoo', got '{logsource.get('product')}'"

    def test_has_attack_tags(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        tags = rule.get("tags", [])
        attack_tags = [t for t in tags if t.startswith("attack.")]
        assert len(attack_tags) >= 1, "Rule must have at least one attack.* tag"

    def test_attack_tags_format(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        tags = rule.get("tags", [])
        for tag in tags:
            if tag.startswith("attack."):
                assert ATTACK_TAG_PATTERN.match(tag), f"Invalid ATT&CK tag format: {tag}"

    def test_detection_has_condition(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        detection = rule.get("detection", {})
        assert "condition" in detection, "Detection block must have a 'condition'"

    def test_field_names_valid(self, detection_rule_path):
        """Ensure all field names in detection blocks reference real artifact fields."""
        rule = load_rule(detection_rule_path)
        detection = rule.get("detection", {})
        invalid_fields = set()

        for key, value in detection.items():
            if key == "condition":
                continue
            if isinstance(value, dict):
                for field_name in value.keys():
                    # Strip Sigma modifiers (|contains, |endswith, |re, etc.)
                    base_field = field_name.split("|")[0]
                    if base_field and base_field not in VALID_FIELD_NAMES:
                        invalid_fields.add(base_field)

        assert not invalid_fields, f"Unknown artifact fields: {invalid_fields}"

    def test_has_falsepositives(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        assert "falsepositives" in rule, "Rule must document false positives"

    def test_has_author(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        assert rule.get("author") == "WitFoo", f"Author should be 'WitFoo', got '{rule.get('author')}'"

    def test_filename_matches_custom_id(self, detection_rule_path):
        rule = load_rule(detection_rule_path)
        custom_id = rule.get("custom_id", "")
        expected_stem = custom_id.replace("-", "_")
        actual_stem = detection_rule_path.stem
        assert actual_stem == expected_stem, \
            f"Filename '{actual_stem}.yml' doesn't match custom_id '{custom_id}' (expected '{expected_stem}.yml')"


# ---------------------------------------------------------------------------
# Tests: Correlation rule schema
# ---------------------------------------------------------------------------

class TestCorrelationRuleSchema:
    """Validate correlation rule YAML structure."""

    def test_yaml_parses(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        assert isinstance(rule, dict)

    def test_required_fields(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        missing = REQUIRED_FIELDS_CORRELATION - set(rule.keys())
        assert not missing, f"Missing required fields: {missing}"

    def test_type_is_correlation(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        assert rule.get("type") in ("event_count", "value_count", "temporal", "temporal_ordered"), \
            f"Correlation type must be event_count, value_count, temporal, or temporal_ordered"

    def test_has_group_by(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        assert "group-by" in rule, "Correlation rule must have group-by"

    def test_has_timespan(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        assert "timespan" in rule, "Correlation rule must have timespan"

    def test_rule_id_is_uuid(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        rule_id = rule.get("id", "")
        try:
            uuid.UUID(str(rule_id))
        except ValueError:
            pytest.fail(f"Correlation rule id '{rule_id}' is not a valid UUID")

    def test_custom_id_format(self, correlation_rule_path):
        rule = load_rule(correlation_rule_path)
        custom_id = rule.get("custom_id", "")
        assert RULE_ID_PATTERN.match(custom_id), f"custom_id '{custom_id}' doesn't match pattern"


# ---------------------------------------------------------------------------
# Tests: Filter rule schema
# ---------------------------------------------------------------------------

class TestFilterRuleSchema:
    """Validate filter rule YAML structure."""

    def test_yaml_parses(self, filter_rule_path):
        rule = load_rule(filter_rule_path)
        assert isinstance(rule, dict)

    def test_required_fields(self, filter_rule_path):
        rule = load_rule(filter_rule_path)
        missing = REQUIRED_FIELDS_FILTER - set(rule.keys())
        assert not missing, f"Missing required fields: {missing}"

    def test_rule_id_is_uuid(self, filter_rule_path):
        rule = load_rule(filter_rule_path)
        rule_id = rule.get("id", "")
        try:
            uuid.UUID(str(rule_id))
        except ValueError:
            pytest.fail(f"Filter rule id '{rule_id}' is not a valid UUID")

    def test_custom_id_format(self, filter_rule_path):
        rule = load_rule(filter_rule_path)
        custom_id = rule.get("custom_id", "")
        assert RULE_ID_PATTERN.match(custom_id), f"custom_id '{custom_id}' doesn't match pattern"


# ---------------------------------------------------------------------------
# Tests: Global uniqueness
# ---------------------------------------------------------------------------

class TestGlobalUniqueness:
    """Cross-rule validation."""

    def test_no_duplicate_rule_ids(self):
        all_rules = collect_all_rules()
        ids = []
        for path in all_rules:
            rule = load_rule(path)
            ids.append(rule.get("id"))
        duplicates = [rid for rid in ids if ids.count(rid) > 1]
        assert not duplicates, f"Duplicate rule IDs: {set(duplicates)}"

    def test_no_duplicate_custom_ids(self):
        all_rules = collect_all_rules()
        ids = []
        for path in all_rules:
            rule = load_rule(path)
            ids.append(rule.get("custom_id"))
        duplicates = [rid for rid in ids if ids.count(rid) > 1]
        assert not duplicates, f"Duplicate custom IDs: {set(duplicates)}"

    def test_no_duplicate_titles(self):
        all_rules = collect_all_rules()
        titles = []
        for path in all_rules:
            rule = load_rule(path)
            titles.append(rule.get("title"))
        duplicates = [t for t in titles if titles.count(t) > 1]
        assert not duplicates, f"Duplicate titles: {set(duplicates)}"
