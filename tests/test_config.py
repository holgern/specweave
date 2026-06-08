"""Tests for SpecWeave config discovery, loading, and rendering."""

from __future__ import annotations

from pathlib import Path

import pytest

from specweave.config import (
    SpecWeaveConfig,
    SpecWeavePaths,
    find_config,
    load_config,
    render_default_config,
)


class TestFindConfig:
    def test_prefers_explicit(self, tmp_path: Path) -> None:
        config_file = tmp_path / "my-config.toml"
        config_file.write_text("schema_version = 1\n")
        assert find_config(config_file) == config_file

    def test_prefers_dotfile_over_public(self, tmp_path: Path) -> None:
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        (tmp_path / "specweave.toml").write_text("schema_version = 1\n")
        found = find_config(tmp_path)
        assert found is not None
        assert found.name == ".specweave.toml"

    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        assert find_config(tmp_path) is None

    def test_walks_up_directories(self, tmp_path: Path) -> None:
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        child = tmp_path / "sub" / "deep"
        child.mkdir(parents=True)
        found = find_config(child)
        assert found is not None
        assert found.name == ".specweave.toml"


class TestLoadConfig:
    def test_defaults_when_missing(self) -> None:
        config = load_config(Path("/nonexistent"))
        assert config.schema_version == 1
        assert config.spelling == "behavior"
        assert config.paths.features_dir == Path("specs/behavior/features")

    def test_rejects_unsupported_schema(self, tmp_path: Path) -> None:
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text("schema_version = 99\n")
        with pytest.raises(ValueError, match="Unsupported"):
            load_config(config_file)

    def test_normalizes_paths(self, tmp_path: Path) -> None:
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(
            'schema_version = 1\nspelling = "behaviour"\n'
            '[paths]\nfeatures_dir = "specs/behaviour/features"\n'
        )
        config = load_config(config_file)
        assert config.spelling == "behaviour"
        assert config.paths.features_dir == Path("specs/behaviour/features")

    def test_loads_all_sections(self, tmp_path: Path) -> None:
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(
            "schema_version = 1\n"
            'spelling = "behavior"\n'
            "[pytest]\n"
            'test_globs = ["tests/test_*.py"]\n'
            "[gherkin]\n"
            'id_style = "sequence"\n'
            "[generation]\n"
            'group_by = "area"\n'
        )
        config = load_config(config_file)
        assert config.pytest.test_globs == ("tests/test_*.py",)
        assert config.gherkin.id_style == "sequence"
        assert config.generation.group_by == "area"


class TestRenderDefaultConfig:
    def test_renders_behavior(self) -> None:
        text = render_default_config(spelling="behavior")
        assert 'spelling = "behavior"' in text
        assert "specs/behavior" in text

    def test_renders_behaviour(self) -> None:
        text = render_default_config(spelling="behaviour")
        assert 'spelling = "behaviour"' in text
        assert "specs/behaviour" in text

    def test_is_valid_toml(self) -> None:
        import sys

        text = render_default_config()
        if sys.version_info >= (3, 11):
            import tomllib

            parsed = tomllib.loads(text)
        else:
            import tomli

            parsed = tomli.loads(text)
        assert parsed["schema_version"] == 1

    def test_roundtrip(self, tmp_path: Path) -> None:
        text = render_default_config()
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(text)
        config = load_config(config_file)
        assert config.schema_version == 1
        assert config.spelling == "behavior"


class TestSpecWeavePaths:
    def test_defaults(self) -> None:
        paths = SpecWeavePaths()
        assert paths.features_dir == Path("specs/behavior/features")
        assert paths.tests_dir == Path("tests")

    def test_frozen(self) -> None:
        paths = SpecWeavePaths()
        with pytest.raises(AttributeError):
            paths.features_dir = Path("other")  # type: ignore[misc]


class TestSpecWeaveConfig:
    def test_defaults(self) -> None:
        config = SpecWeaveConfig()
        assert config.schema_version == 1
        assert config.spelling == "behavior"

    def test_frozen(self) -> None:
        config = SpecWeaveConfig()
        with pytest.raises(AttributeError):
            config.spelling = "other"  # type: ignore[misc]
