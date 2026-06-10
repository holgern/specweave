"""Tests for generated-id behavior autolinking."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from specweave.behavior.autolink import autolink_generated_ids, autolink_result_to_dict
from specweave.cli import app

runner = CliRunner()


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _feature(root: Path, area: str, name: str, bdd_id: str) -> Path:
    return _write(
        root / area / f"{name}.feature",
        f"""@area-{area}
Feature: {name}

  @{bdd_id}
  Example: Observable behavior
    Given x
    When y
    Then z
""",
    )


def test_autolink_generated_id_top_level_function(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-does_the_thing")
    _write(tests / "test_autolink.py", "def test_does_the_thing() -> None:\n    pass\n")

    result = autolink_generated_ids(features=features, tests=tests)

    assert result.summary["planned"] == 1
    assert result.items[0].nodeid == "tests/test_autolink.py::test_does_the_thing"


def test_autolink_dry_run_does_not_write(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-does_the_thing")
    test_file = _write(
        tests / "test_autolink.py", "def test_does_the_thing() -> None:\n    pass\n"
    )

    before = test_file.read_text(encoding="utf-8")
    autolink_generated_ids(features=features, tests=tests)

    assert test_file.read_text(encoding="utf-8") == before


def test_autolink_apply_writes_mapping_comments(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-does_the_thing")
    test_file = _write(
        tests / "test_autolink.py", "def test_does_the_thing() -> None:\n    pass\n"
    )

    result = autolink_generated_ids(features=features, tests=tests, apply=True)

    content = test_file.read_text(encoding="utf-8")
    assert result.summary["written"] == 1
    assert "import pytest" in content
    assert "@pytest.mark.specweave" in content
    assert "@bdd-behavior-does_the_thing" in content


def test_autolink_preserves_decorators(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-decorated")
    test_file = _write(
        tests / "test_autolink.py",
        "import pytest\n\n\n"
        "@pytest.mark.slow\n"
        "def test_decorated() -> None:\n"
        "    pass\n",
    )

    autolink_generated_ids(features=features, tests=tests, apply=True)

    content = test_file.read_text(encoding="utf-8")
    assert content.index("@pytest.mark.specweave") < content.index("@pytest.mark.slow")


def test_autolink_class_method_uses_method_indentation(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-class_method")
    test_file = _write(
        tests / "test_autolink.py",
        "class TestBehavior:\n    def test_class_method(self) -> None:\n        pass\n",
    )

    autolink_generated_ids(features=features, tests=tests, apply=True)

    assert "    @pytest.mark.specweave" in test_file.read_text(encoding="utf-8")


def test_autolink_skips_existing_mapping(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-existing")
    _write(
        tests / "test_autolink.py",
        "# sw: f=specs/behavior/features/behavior/autolink.feature\n"
        "# sw: s=@bdd-behavior-existing\n"
        "def test_existing() -> None:\n    pass\n",
    )

    result = autolink_generated_ids(features=features, tests=tests)

    assert result.summary["planned"] == 0
    assert result.summary["skipped_existing"] == 1


def test_autolink_reports_ambiguous_equal_score(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-duplicate")
    _write(tests / "test_one.py", "def test_duplicate() -> None:\n    pass\n")
    _write(tests / "test_two.py", "def test_duplicate() -> None:\n    pass\n")

    result = autolink_generated_ids(features=features, tests=tests)

    assert result.summary["ambiguous"] == 1
    assert result.summary["planned"] == 0


def test_autolink_rewrites_duplicate_occurrences_only_when_enabled(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-duplicate")
    _write(tests / "test_one.py", "def test_duplicate() -> None:\n    pass\n")
    _write(tests / "test_two.py", "def test_duplicate() -> None:\n    pass\n")

    result = autolink_generated_ids(
        features=features, tests=tests, rewrite_duplicates=True
    )

    assert result.summary["planned"] == 1
    assert result.items[0].confidence == "nth-duplicate"


def test_autolink_json_shape(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    features = tmp_path / "specs" / "behavior" / "features"
    tests = tmp_path / "tests"
    _feature(features, "behavior", "autolink", "bdd-behavior-json_shape")
    _write(tests / "test_autolink.py", "def test_json_shape() -> None:\n    pass\n")

    payload = autolink_result_to_dict(
        autolink_generated_ids(features=features, tests=tests)
    )

    assert payload["schema_version"] == 1
    assert payload["command"] == "behavior autolink"
    assert set(payload) == {
        "schema_version",
        "command",
        "strategy",
        "apply",
        "summary",
        "items",
        "ambiguous",
        "unmatched",
    }


def test_autolink_uses_config_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write(
        tmp_path / ".specweave.toml",
        """schema_version = 1
project_root = "."
spelling = "behavior"
[paths]
features_dir = "features"
tests_dir = "checks"
reports_state_dir = "reports/specweave"
behavior_readme = "README.behavior.md"
manifest = "manifest.json"
evidence_dir = "evidence"
reports_dir = "reports"
mapping_dir = "mappings"
""",
    )
    _feature(tmp_path / "features", "behavior", "autolink", "bdd-behavior-config_path")
    _write(
        tmp_path / "checks" / "test_autolink.py",
        "def test_config_path() -> None:\n    pass\n",
    )

    result = runner.invoke(app, ["behavior", "autolink", "--format", "json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["summary"]["planned"] == 1
