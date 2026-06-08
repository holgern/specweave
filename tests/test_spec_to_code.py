"""Tests for the spec-to-code generation (bind command)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from specweave.translate.naming import step_function_name
from specweave.translate.spec_to_code import bind_feature, draft_feature


def test_step_function_name_basic() -> None:
    """step_function_name generates predictable names."""
    name = step_function_name("Given a registered user exists")
    assert name == "step_given_a_registered_user_exists"

    name = step_function_name("When the user submits an invalid password")
    assert name == "step_when_the_user_submits_an_invalid_password"


def test_step_function_name_dedup() -> None:
    """Duplicate step texts get unique suffixes."""
    name1 = step_function_name("Given a step", existing=frozenset())
    name2 = step_function_name("Given a step", existing=frozenset({name1}))
    assert name1 != name2
    assert name2.endswith("_2")


def test_draft_feature_creates_file() -> None:
    """draft_feature creates a valid .feature file from JSON."""
    json_data = json.dumps(
        {
            "task_id": "TL-0042",
            "title": "Password login",
            "acceptance_criteria": [
                {"id": "AC-001", "text": "Reject invalid password"}
            ],
        }
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / "task.json"
        json_path.write_text(json_data, encoding="utf-8")

        out_path = Path(tmpdir) / "output.feature"
        draft_feature(json_path, out_path)

        assert out_path.exists()
        content = out_path.read_text(encoding="utf-8")
        assert "@taskledger:TL-0042" in content
        assert "Feature: Password login" in content
        assert "@ac:AC-001" in content
        assert "Given the system is ready" in content


def test_bind_feature_creates_skeleton() -> None:
    """bind_feature creates a Python step skeleton file."""
    feature_text = """@taskledger:TL-0042
Feature: Password login

  @ac:AC-001
  Scenario: Reject invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then login is rejected
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        feature_path = Path(tmpdir) / "test.feature"
        feature_path.write_text(feature_text, encoding="utf-8")

        out_dir = Path(tmpdir) / "steps"
        bind_feature(feature_path, "behave", out_dir)

        step_file = out_dir / "test_steps.py"
        assert step_file.exists()
        content = step_file.read_text(encoding="utf-8")
        assert "from behave import given, then, when" in content
        assert '@given("a registered user exists")' in content
        assert '@when("the user submits an invalid password")' in content
        assert '@then("login is rejected")' in content
        assert "raise NotImplementedError" in content


def test_bind_unsupported_backend_raises() -> None:
    """Unknown backends raise ValueError."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        feature_path = Path(tmpdir) / "test.feature"
        feature_path.write_text(
            "Feature: X\n  Scenario: Y\n    Given z\n",
        )
        import pytest

        with pytest.raises(ValueError, match="Unsupported backend"):
            bind_feature(feature_path, "totally-unknown", Path(tmpdir) / "out")
