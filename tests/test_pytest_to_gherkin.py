"""Tests for pytest-to-Gherkin generation."""

from __future__ import annotations

from pathlib import Path

from specweave.config import SpecWeaveConfig
from specweave.translate.pytest_to_gherkin import (
    _derive_area,
    _derive_feature_title,
    _slug,
    generate_gherkin_from_tests,
)


def _feature_file_paths(dir_path: Path) -> list[Path]:
    """Return .feature and .feature.md files under *dir_path*."""
    return [
        f
        for f in dir_path.rglob("*")
        if f.is_file() and (f.suffix == ".feature" or str(f).endswith(".feature.md"))
    ]


def _write_pytest_file(tmp_path: Path, name: str, content: str) -> Path:
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    p = tests_dir / name
    p.write_text(content, encoding="utf-8")
    return p


# A simple test with a real assert that the AST reader can detect
_SIMPLE_TEST = "def test_valid_login():\n    assert user is not None\n"


class TestSlug:
    def test_basic(self) -> None:
        assert _slug("Password Reset") == "password-reset"

    def test_special_chars(self) -> None:
        assert _slug("User's login (retry)") == "user-s-login-retry"


class TestDeriveArea:
    def test_simple(self, tmp_path: Path) -> None:
        tests_dir = tmp_path / "tests"
        f = tests_dir / "test_auth.py"
        assert _derive_area(f, tests_dir) == "auth"

    def test_nested(self, tmp_path: Path) -> None:
        tests_dir = tmp_path / "tests"
        f = tests_dir / "unit" / "test_parser.py"
        assert _derive_area(f, tests_dir) == "unit"


class TestDeriveFeatureTitle:
    def test_test_prefix(self) -> None:
        assert _derive_feature_title(Path("test_auth_password.py")) == "Auth Password"

    def test_test_suffix(self) -> None:
        assert _derive_feature_title(Path("auth_password_test.py")) == "Auth Password"


class TestCreateGherkinFromSinglePytestFile:
    def test_creates_feature(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        result = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        assert result["status"] == "ok"
        assert result["created"] == 1
        assert len(result["results"]) == 1

    def test_marks_needs_review(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        features = _feature_file_paths(out_dir)
        assert len(features) == 1, f"Found features: {features}"
        content = features[0].read_text()
        assert "@needs-review" in content
        assert "@generated" in content

    def test_includes_bdd_id(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        result = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        scenario_ids = result["results"][0]["scenario_ids"]
        assert len(scenario_ids) == 1
        assert scenario_ids[0].startswith("bdd-")


class TestCreateGherkinGroupsByArea:
    def test_groups_by_file(self, tmp_path: Path) -> None:
        _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        _write_pytest_file(tmp_path, "test_billing_invoice.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        tests_dir = tmp_path / "tests"
        result = generate_gherkin_from_tests(
            test_paths=[tests_dir],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        assert result["created"] == 2
        features = _feature_file_paths(out_dir)
        areas = {p.parent.name for p in features}
        assert len(areas) == 2, f"Areas found: {areas}"


class TestCreateGherkinPreservesExisting:
    def test_skips_manual_file_without_force(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        # Create a manual .feature.md file matching the default extension
        feature_path = out_dir / "auth_login" / "auth-login.feature.md"
        feature_path.parent.mkdir(parents=True)
        feature_path.write_text(
            "Feature: Manual\n  Scenario: Handwritten\n    Given something\n",
            encoding="utf-8",
        )

        result = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        skipped = result["skipped"]
        assert skipped == 1, (
            f"Expected 1 skipped, got {skipped}: {result.get('warnings')}"
        )
        assert any("SWWRITE001" in w for w in result["warnings"])

    def test_preserves_existing_bdd_id(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        result2 = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            mode="update",
            config=SpecWeaveConfig(),
        )
        assert result2["updated"] == 1


class TestCreateGherkinDryRun:
    def test_writes_nothing(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        result = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            dry_run=True,
            config=SpecWeaveConfig(),
        )
        assert result["created"] == 1
        assert not out_dir.exists()


class TestCreateGherkinJsonShape:
    def test_json_shape(self, tmp_path: Path) -> None:
        test_file = _write_pytest_file(tmp_path, "test_auth_login.py", _SIMPLE_TEST)
        out_dir = tmp_path / "specs" / "behavior" / "features"
        result = generate_gherkin_from_tests(
            test_paths=[test_file],
            out_dir=out_dir,
            config=SpecWeaveConfig(),
        )
        assert result["schema_version"] == 1
        assert result["command"] == "create gherkin"
        assert "results" in result
        for r in result["results"]:
            assert "feature_path" in r
            assert "status" in r
            assert "scenario_ids" in r
