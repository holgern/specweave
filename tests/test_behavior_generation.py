"""Tests for pytest skeleton generation from behavior features."""

from __future__ import annotations

from pathlib import Path

from specweave.behavior.generate import generate_from_paths, generate_pytest_skeleton
from specweave.gherkin.model import Feature, Rule, Scenario, Step

FEATURE = "specs/behavior/features/behavior/generation.feature"


def _write_feature(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _simple_feature() -> Feature:
    return Feature(
        title="Login",
        rules=(
            Rule(
                title="Auth rule",
                tags=("rule-auth",),
                scenarios=(
                    Scenario(
                        title="Valid login",
                        keyword="Example",
                        tags=("bdd-login-valid",),
                        steps=(
                            Step(keyword="Given", text="a registered user"),
                            Step(keyword="When", text="the user logs in"),
                            Step(keyword="Then", text="login succeeds"),
                        ),
                    ),
                ),
            ),
        ),
    )


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-single-feature
def test_generate_single_feature(tmp_path: Path) -> None:
    """Generation creates a test file for a feature."""
    features_dir = tmp_path / "features"
    feature_path = _write_feature(
        features_dir / "auth" / "login.feature",
        (
            "Feature: Login\n"
            "  Rule: Auth\n"
            "    @bdd-login-valid\n"
            "    Example: Valid\n"
            "      Given x\n"
        ),
    )
    tests_dir = tmp_path / "tests"
    result = generate_from_paths(
        feature_path=feature_path,
        tests_dir=tests_dir,
    )
    assert len(result) >= 1
    assert result[0].exists()


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-scenario-function
def test_generate_scenario_function() -> None:
    """Each scenario becomes a test function."""
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert "def test_" in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-specweave-markers
def test_generate_specweave_markers() -> None:
    """Test functions have correct specweave markers."""
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert "@pytest.mark.specweave" in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-docstring
def test_generate_docstring() -> None:
    """Test functions have docstrings with scenario details."""
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert '"""' in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-step-comments
def test_generate_step_comments() -> None:
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert "# Arrange" in code or "Given" in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-canonical-path
def test_generate_canonical_path() -> None:
    """Test path is derived from feature path."""
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert "specs/behavior/features/auth/login.feature" in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-rules
def test_generate_rules() -> None:
    """Scenarios in rules get rule markers."""
    feature = _simple_feature()
    code = generate_pytest_skeleton(
        feature, Path("specs/behavior/features/auth/login.feature")
    )
    assert 'rule="Auth rule"' in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-long-mapping-lines
def test_generate_avoids_long_specweave_mapping_lines() -> None:
    feature = Feature(
        title="Long paths",
        rules=(
            Rule(
                title="A rule title that is deliberately long but still readable",
                scenarios=(
                    Scenario(
                        title="Long mapping",
                        keyword="Example",
                        tags=(
                            "bdd-cli-command-contract-commands-do-not-register-"
                            "local-json-options-and-remain-ruff-clean",
                        ),
                        steps=(Step(keyword="Given", text="x"),),
                    ),
                ),
            ),
        ),
    )
    code = generate_pytest_skeleton(
        feature,
        Path(
            "specs/behavior/features/cli_command_contract/"
            "cli-command-contract.feature"
        ),
    )

    assert max(len(line) for line in code.splitlines()) <= 88
    assert "cli_command_contract/" in code
    assert "local-json-options-" in code
    assert "remain-ruff-clean" in code


# specweave: feature=specs/behavior/features/behavior/generation.feature
# specweave: scenario=@bdd-generate-batch
def test_generate_batch(tmp_path: Path) -> None:
    """Generation processes all features in a directory."""
    features_dir = tmp_path / "features"
    area = features_dir / "auth"
    f1 = _write_feature(
        area / "login.feature",
        (
            "Feature: Login\n"
            "  @bdd-login\n"
            "  Example: Login\n"
            "    Given x\n"
            "    When y\n"
            "    Then z\n"
        ),
    )
    f2 = _write_feature(
        area / "logout.feature",
        (
            "Feature: Logout\n"
            "  @bdd-logout\n"
            "  Example: Logout\n"
            "    Given x\n"
            "    When y\n"
            "    Then z\n"
        ),
    )
    tests_dir = tmp_path / "tests"
    r1 = generate_from_paths(feature_path=f1, tests_dir=tests_dir)
    r2 = generate_from_paths(feature_path=f2, tests_dir=tests_dir)
    assert len(r1) == 1
    assert len(r2) == 1
