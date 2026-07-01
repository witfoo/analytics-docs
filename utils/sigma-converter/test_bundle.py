"""
Sigma Bundle Tests

Validates the aggregate `sigma_rules.zip` download bundle produced by
`generate_sigma_bundle()`:
  - contains every Sigma source rule (all 68, all categories incl. correlations/filters)
  - arcnames are `sigma/<category>/<file>.yml`
  - archived bytes match the on-disk source rules exactly (independent oracle)
  - the archive is byte-for-byte deterministic (fixed mtime + stored) so the
    committed binary only churns when a rule's content changes

These tests use only the stdlib `zipfile` + the pure `generate_sigma_bundle`
helper, so they run without the heavy pySigma SIEM backends installed.
"""

import zipfile
from pathlib import Path

import pytest

from convert import generate_sigma_bundle, SIGMA_DIR


def _source_rule_arcnames() -> set[str]:
    """The `sigma/<category>/<file>.yml` arcname for every source rule on disk."""
    names = set()
    for cat_dir in SIGMA_DIR.iterdir():
        if cat_dir.is_dir():
            for rule in cat_dir.glob("*.yml"):
                names.add(f"sigma/{cat_dir.name}/{rule.name}")
    return names


@pytest.fixture
def bundle_path(tmp_path) -> Path:
    out = tmp_path / "sigma_rules.zip"
    generate_sigma_bundle(out)
    return out


class TestSigmaBundle:
    """Contract for the aggregate one-click Sigma download bundle."""

    def test_bundle_created(self, bundle_path):
        assert bundle_path.is_file()

    def test_bundle_contains_every_source_rule(self, bundle_path):
        with zipfile.ZipFile(bundle_path) as zf:
            names = set(zf.namelist())
        assert names == _source_rule_arcnames()

    def test_bundle_has_68_entries(self, bundle_path):
        with zipfile.ZipFile(bundle_path) as zf:
            names = zf.namelist()
        assert len(names) == 68, f"expected 68 rule entries, got {len(names)}"
        assert all(
            n.startswith("sigma/") and n.endswith(".yml") for n in names
        ), "every arcname must be sigma/<category>/<file>.yml"

    def test_return_value_is_entry_count(self, tmp_path):
        out = tmp_path / "b.zip"
        count = generate_sigma_bundle(out)
        with zipfile.ZipFile(out) as zf:
            assert count == len(zf.namelist())

    def test_arcnames_sorted(self, bundle_path):
        with zipfile.ZipFile(bundle_path) as zf:
            names = zf.namelist()
        assert names == sorted(names), "entries must be written in sorted order"

    def test_archived_bytes_match_source(self, bundle_path):
        """Each archived entry is byte-identical to its on-disk source rule."""
        with zipfile.ZipFile(bundle_path) as zf:
            for name in zf.namelist():
                rel = name[len("sigma/"):]  # name == sigma/<category>/<file>.yml
                src = SIGMA_DIR / rel
                assert zf.read(name) == src.read_bytes(), f"content drift for {name}"

    def test_entries_have_fixed_timestamp(self, bundle_path):
        """Fixed 1980-01-01 mtime — guards against zipfile's default now() mtime."""
        with zipfile.ZipFile(bundle_path) as zf:
            for info in zf.infolist():
                assert info.date_time == (1980, 1, 1, 0, 0, 0), (
                    f"{info.filename} has non-fixed mtime {info.date_time}"
                )

    def test_entries_are_stored_not_deflated(self, bundle_path):
        """Stored (uncompressed) → byte-identical regardless of zlib version."""
        with zipfile.ZipFile(bundle_path) as zf:
            for info in zf.infolist():
                assert info.compress_type == zipfile.ZIP_STORED, (
                    f"{info.filename} is compressed ({info.compress_type})"
                )

    def test_bundle_is_byte_deterministic(self, tmp_path):
        """Two independent generations produce byte-identical archives."""
        a = tmp_path / "a.zip"
        b = tmp_path / "b.zip"
        generate_sigma_bundle(a)
        generate_sigma_bundle(b)
        assert a.read_bytes() == b.read_bytes()

    def test_default_output_path(self):
        """Default destination is docs/detection-rules/sigma_rules.zip."""
        import inspect

        # Exercised without writing: confirm the documented default target.
        expected = SIGMA_DIR.parent / "sigma_rules.zip"
        assert expected.name == "sigma_rules.zip"
        assert expected.parent.name == "detection-rules"
        # generate_sigma_bundle accepts an optional output_path (default None).
        sig = inspect.signature(generate_sigma_bundle)
        assert sig.parameters["output_path"].default is None
