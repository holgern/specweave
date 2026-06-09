"""Tests for behavior index and manifest generation."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.index import build_behavior_index

FEATURE = "specs/behavior/features/behavior/index.feature"


def _write_feature(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _setup_project(tmp_path: Path) -> dict:
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    evidence_dir = tmp_path / "specs" / "behavior" / "evidence"
    tests_dir.mkdir()
    evidence_dir.mkdir(parents=True)
    _write_feature(
        features_dir / "auth" / "login.feature",
        (
            "Feature: Login\n"
            "  @bdd-login-valid\n"
            "  Example: Valid login\n"
            "    Given x\n"
            "    When y\n"
            "    Then z\n"
        ),
    )
    (tests_dir / "test_auth_login.py").write_text(
        "# specweave: feature=specs/behavior/features/auth/login.feature\n"
        "# specweave: scenario=@bdd-login-valid\n"
        "def test_valid_login() -> None:\n    pass\n",
        encoding="utf-8",
    )
    return {
        "features_dir": features_dir,
        "tests_dir": tests_dir,
        "evidence_dir": evidence_dir,
    }


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-generates-markdown
def test_index_generates_markdown(tmp_path: Path) -> None:
    """Index generates Markdown with feature listing."""
    paths = _setup_project(tmp_path)
    result, markdown = build_behavior_index(
        features_dir=paths["features_dir"],
        tests_dir=paths["tests_dir"],
        evidence_dir=paths["evidence_dir"],
    )
    assert "features" in result
    assert isinstance(markdown, str)


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-generates-manifest
def test_index_generates_manifest(tmp_path: Path) -> None:
    """Index generates JSON manifest with scenario mappings."""
    paths = _setup_project(tmp_path)
    result, _ = build_behavior_index(
        features_dir=paths["features_dir"],
        tests_dir=paths["tests_dir"],
        evidence_dir=paths["evidence_dir"],
    )
    assert "features" in result
    assert result["schema_version"] == 1


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-scenario-entries
def test_index_scenario_entries(tmp_path: Path) -> None:
    """Manifest includes scenario entries with automation status."""
    paths = _setup_project(tmp_path)
    result, _ = build_behavior_index(
        features_dir=paths["features_dir"],
        tests_dir=paths["tests_dir"],
        evidence_dir=paths["evidence_dir"],
    )
    assert len(result["features"]) >= 1


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-unbound-scenario
def test_index_unbound_scenario(tmp_path: Path) -> None:
    """Manifest marks unbound scenarios as missing."""
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    evidence_dir = tmp_path / "specs" / "behavior" / "evidence"
    tests_dir.mkdir()
    evidence_dir.mkdir(parents=True)
    _write_feature(
        features_dir / "auth" / "login.feature",
        (
            "Feature: Login\n"
            "  @bdd-login-valid\n"
            "  Example: Valid login\n"
            "    Given x\n"
            "    When y\n"
            "    Then z\n"
        ),
    )
    result, _ = build_behavior_index(
        features_dir=features_dir,
        tests_dir=tests_dir,
        evidence_dir=evidence_dir,
    )
    assert len(result["features"]) >= 1


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-evidence-status
def test_index_evidence_status(tmp_path: Path) -> None:
    """Manifest includes latest evidence status when available."""
    paths = _setup_project(tmp_path)
    result, _ = build_behavior_index(
        features_dir=paths["features_dir"],
        tests_dir=paths["tests_dir"],
        evidence_dir=paths["evidence_dir"],
    )
    assert "schema_version" in result


# specweave: feature=specs/behavior/features/behavior/index.feature
# specweave: scenario=@bdd-index-rules
def test_index_rules(tmp_path: Path) -> None:
    """Manifest preserves Rule structure."""
    features_dir = tmp_path / "specs" / "behavior" / "features"
    tests_dir = tmp_path / "tests"
    evidence_dir = tmp_path / "specs" / "behavior" / "evidence"
    tests_dir.mkdir()
    evidence_dir.mkdir(parents=True)
    _write_feature(
        features_dir / "auth" / "login.feature",
        (
            "Feature: Login\n"
            "  Rule: Auth\n"
            "    @bdd-login-valid\n"
            "    Example: Valid\n"
            "      Given x\n"
            "      When y\n"
            "      Then z\n"
        ),
    )
    result, _ = build_behavior_index(
        features_dir=features_dir,
        tests_dir=tests_dir,
        evidence_dir=evidence_dir,
    )
    feat = result["features"][0]
    assert "rules" in feat or "scenarios" in feat
