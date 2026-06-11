"""Tests for Gherkin feature file linting."""

from __future__ import annotations

from pathlib import Path

from specweave.gherkin.lint import lint_feature_files

FEATURE = "specs/behavior/features/gherkin/lint.feature"


def _write_feature(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _canonical_dir(tmp_path: Path) -> Path:
    d = tmp_path / "specs" / "behavior" / "features" / "area"
    d.mkdir(parents=True, exist_ok=True)
    return d


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-single-feature
def test_lint_multiple_feature_lines(tmp_path: Path) -> None:
    """Lint errors on multiple Feature lines."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: One\nFeature: Two\n  Scenario: S\n    Given x\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH002" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-empty-feature-title
def test_lint_empty_feature_title(tmp_path: Path) -> None:
    """Lint errors on empty feature title."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature:\n  Scenario: S\n    Given x\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH003" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-empty-scenario-title
def test_lint_empty_scenario_title(tmp_path: Path) -> None:
    """Lint errors on empty scenario title."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example:\n    Given x\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH004" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-missing-given-when-then
def test_lint_missing_given_when_then(tmp_path: Path) -> None:
    """Lint errors when Given/When/Then are missing."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example: E\n    Something happens\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH005" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-empty-rule
def test_lint_empty_rule(tmp_path: Path) -> None:
    """Lint errors on Rule without scenarios."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Rule: R\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH006" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-duplicate-bdd-tags
def test_lint_duplicate_bdd_tags(tmp_path: Path) -> None:
    """Lint errors on duplicate @bdd-* tags."""
    d = _canonical_dir(tmp_path)
    content = (
        "Feature: F\n"
        "  @bdd-dup\n  Example: A\n    Given x\n    When y\n    Then z\n"
        "  @bdd-dup\n  Example: B\n    Given x\n    When y\n    Then z\n"
    )
    _write_feature(d / "test.feature", content)
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH007" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-missing-bdd-tag
def test_lint_missing_bdd_tag(tmp_path: Path) -> None:
    """Lint warns when scenario lacks @bdd-* tag."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example: E\n    Given x\n    When y\n    Then z\n",
    )
    findings = lint_feature_files([d / "test.feature"], require_scenario_ids=True)
    assert any(f.code == "SWBEH014" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-task-tags-discouraged
def test_lint_task_tags_discouraged(tmp_path: Path) -> None:
    """Lint warns on task-specific tags in features."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        (
            "Feature: F\n"
            "  @bdd-s1 @task-001\n"
            "  Example: E\n"
            "    Given x\n"
            "    When y\n"
            "    Then z\n"
        ),
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH013" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-canonical-path
def test_lint_canonical_path(tmp_path: Path) -> None:
    """Lint errors on features outside canonical path."""
    d = tmp_path / "other" / "features"
    d.mkdir(parents=True)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example: E\n    Given x\n    When y\n    Then z\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH009" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-area-subdirectory
def test_lint_area_subdirectory(tmp_path: Path) -> None:
    """Lint warns when feature is not in area subdirectory."""
    d = tmp_path / "specs" / "behavior" / "features"
    d.mkdir(parents=True)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example: E\n    Given x\n    When y\n    Then z\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH009" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-deprecated-path
def test_lint_deprecated_path(tmp_path: Path) -> None:
    """Lint warns on deprecated feature paths."""
    d = tmp_path / "specs" / "bdd" / "features"
    d.mkdir(parents=True)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Example: E\n    Given x\n    When y\n    Then z\n",
    )
    findings = lint_feature_files([d / "test.feature"])
    assert any(f.code == "SWBEH015" for f in findings)


# sw: f=specs/behavior/features/gherkin/lint.feature
# sw: s=@bdd-lint-strict-unsupported
def test_lint_strict_unsupported(tmp_path: Path) -> None:
    """Strict mode errors on Scenario Outline."""
    d = _canonical_dir(tmp_path)
    _write_feature(
        d / "test.feature",
        "Feature: F\n  Scenario Outline: SO\n    Given x\n    When y\n    Then z\n",
    )
    findings = lint_feature_files([d / "test.feature"], strict=True)
    assert any(f.code == "SWBEH008" and f.level == "error" for f in findings)


# sw: f=specs/behavior/features/gherkin/markdown.feature
# sw: s=@bdd-lint-rejects-markdown-file
def test_lint_rejects_markdown_feature_file(tmp_path: Path) -> None:
    d = _canonical_dir(tmp_path)
    path = _write_feature(d / "test.feature.md", "# Feature: F\n")
    findings = lint_feature_files([path])
    assert any(f.code == "SWBEH016" and f.level == "error" for f in findings)
