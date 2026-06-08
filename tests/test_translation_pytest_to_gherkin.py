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

FEATURE = "specs/behavior/features/translation/pytest-to-gherkin.feature.md"


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
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_basic(self) -> None:
        """Generation finds test functions in pytest files."""
        assert _slug("Password Reset") == "password-reset"

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_special_chars(self) -> None:
        """Generation finds test functions in pytest files (special chars)."""
        assert _slug("User's login (retry)") == "user-s-login-retry"


class TestDeriveArea:
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-group-by-file
    def test_simple(self, tmp_path: Path) -> None:
        """Generation groups scenarios by test file."""
        tests_dir = tmp_path / "tests"
        f = tests_dir / "test_auth.py"
        assert _derive_area(f, tests_dir) == "auth"

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-group-by-file
    def test_nested(self, tmp_path: Path) -> None:
        """Generation groups scenarios by test file (nested)."""
        tests_dir = tmp_path / "tests"
        f = tests_dir / "unit" / "test_parser.py"
        assert _derive_area(f, tests_dir) == "unit"


class TestDeriveFeatureTitle:
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_test_prefix(self) -> None:
        """Generation finds test functions in pytest files (test prefix)."""
        assert _derive_feature_title(Path("test_auth_password.py")) == "Auth Password"

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_test_suffix(self) -> None:
        """Generation finds test functions in pytest files (test suffix)."""
        assert _derive_feature_title(Path("auth_password_test.py")) == "Auth Password"


class TestCreateGherkinFromSinglePytestFile:
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_creates_feature(self, tmp_path: Path) -> None:
        """Generation finds test functions in pytest files."""
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

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-marks-generated
    def test_marks_needs_review(self, tmp_path: Path) -> None:
        """Generated features have @generated tag."""
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

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_includes_bdd_id(self, tmp_path: Path) -> None:
        """Generation finds test functions in pytest files (bdd id)."""
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
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-group-by-file
    def test_groups_by_file(self, tmp_path: Path) -> None:
        """Generation groups scenarios by test file."""
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
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-preserve-manual
    def test_skips_manual_file_without_force(self, tmp_path: Path) -> None:
        """Generation does not overwrite manual feature files."""
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

    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-preserve-manual
    def test_preserves_existing_bdd_id(self, tmp_path: Path) -> None:
        """Generation does not overwrite manual feature files (preserve bdd id)."""
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
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-dry-run
    def test_writes_nothing(self, tmp_path: Path) -> None:
        """Dry-run reports without writing files."""
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
    # specweave:feature=specs/behavior/features/translation/pytest-to-gherkin.feature.md
    # specweave: scenario=@bdd-translate-discovers-tests
    def test_json_shape(self, tmp_path: Path) -> None:
        """Generation finds test functions in pytest files (JSON shape)."""
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
