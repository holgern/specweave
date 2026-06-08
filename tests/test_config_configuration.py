"""Tests for SpecWeave config discovery, loading, and rendering."""

from __future__ import annotations

from pathlib import Path

import pytest

from specweave.config import (
    SpecWeaveConfig,
    SpecWeaveGherkin,
    SpecWeavePaths,
    find_config,
    load_config,
    render_default_config,
)

FEATURE = "specs/behavior/features/config/configuration.feature.md"


class TestFindConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-discovery-finds-dotfile
    def test_prefers_explicit(self, tmp_path: Path) -> None:
        """Discovery finds .specweave.toml in current directory."""
        config_file = tmp_path / "my-config.toml"
        config_file.write_text("schema_version = 1\n")
        assert find_config(config_file) == config_file

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-discovery-prefers-dotfile
    def test_prefers_dotfile_over_public(self, tmp_path: Path) -> None:
        """Discovery prefers .specweave.toml over specweave.toml."""
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        (tmp_path / "specweave.toml").write_text("schema_version = 1\n")
        found = find_config(tmp_path)
        assert found is not None
        assert found.name == ".specweave.toml"

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-discovery-returns-none
    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        """Discovery returns None when no config exists."""
        assert find_config(tmp_path) is None

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-discovery-walks-parents
    def test_walks_up_directories(self, tmp_path: Path) -> None:
        """Discovery walks parent directories when not found locally."""
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        child = tmp_path / "sub" / "deep"
        child.mkdir(parents=True)
        found = find_config(child)
        assert found is not None
        assert found.name == ".specweave.toml"


class TestLoadConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_defaults_when_missing(self) -> None:
        """Loading with no file returns default config."""
        config = load_config(Path("/nonexistent"))
        assert config.schema_version == 1
        assert config.spelling == "behavior"
        assert config.paths.features_dir == Path("specs/behavior/features")

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-rejects-unsupported-schema
    def test_rejects_unsupported_schema(self, tmp_path: Path) -> None:
        """Loading fails for schema_version 2."""
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text("schema_version = 99\n")
        with pytest.raises(ValueError, match="Unsupported"):
            load_config(config_file)

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-from-file
    def test_normalizes_paths(self, tmp_path: Path) -> None:
        """Loading reads values from a valid TOML file."""
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(
            'schema_version = 1\nspelling = "behaviour"\n'
            '[paths]\nfeatures_dir = "specs/behaviour/features"\n'
        )
        config = load_config(config_file)
        assert config.spelling == "behaviour"
        assert config.paths.features_dir == Path("specs/behaviour/features")

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-from-file
    def test_loads_all_sections(self, tmp_path: Path) -> None:
        """Loading reads values from a valid TOML file (all sections)."""
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

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-from-file
    def test_gherkin_new_fields_preserved(self, tmp_path: Path) -> None:
        """Loading reads values from a valid TOML file (gherkin fields)."""
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(
            "schema_version = 1\n"
            "[gherkin]\n"
            'document_format = "classic"\n'
            'feature_extension = ".feature"\n'
            'feature_extensions = [".feature"]\n'
            "official_parser = false\n"
            'markdown_parser = "off"\n'
            "compile_pickles = true\n"
        )
        config = load_config(config_file)
        assert config.gherkin.document_format == "classic"
        assert config.gherkin.feature_extension == ".feature"
        assert config.gherkin.feature_extensions == (".feature",)
        assert config.gherkin.official_parser is False
        assert config.gherkin.markdown_parser == "off"
        assert config.gherkin.compile_pickles is True


class TestRenderDefaultConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-render-behavior
    def test_renders_behavior(self) -> None:
        """Default config renders behavior spelling."""
        text = render_default_config(spelling="behavior")
        assert 'spelling = "behavior"' in text
        assert "specs/behavior" in text

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-render-behaviour
    def test_renders_behaviour(self) -> None:
        """Default config renders behaviour spelling."""
        text = render_default_config(spelling="behaviour")
        assert 'spelling = "behaviour"' in text
        assert "specs/behaviour" in text

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-render-behavior
    def test_is_valid_toml(self) -> None:
        """Default config renders behavior spelling (valid TOML)."""
        import sys

        text = render_default_config()
        if sys.version_info >= (3, 11):
            import tomllib

            parsed = tomllib.loads(text)
        else:
            import tomli

            parsed = tomli.loads(text)
        assert parsed["schema_version"] == 1

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-render-behavior
    def test_roundtrip(self, tmp_path: Path) -> None:
        """Default config renders behavior spelling (roundtrip)."""
        text = render_default_config()
        config_file = tmp_path / ".specweave.toml"
        config_file.write_text(text)
        config = load_config(config_file)
        assert config.schema_version == 1
        assert config.spelling == "behavior"

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-render-behavior
    def test_renders_new_gherkin_defaults(self) -> None:
        """Default config renders behavior spelling (gherkin defaults)."""
        text = render_default_config()
        assert 'document_format = "markdown"' in text
        assert 'feature_extension = ".feature.md"' in text
        assert 'feature_extensions = [".feature.md", ".feature"]' in text
        assert "official_parser = true" in text
        assert 'markdown_parser = "specweave"' in text
        assert "compile_pickles = false" in text


class TestSpecWeavePaths:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_defaults(self) -> None:
        """Loading with no file returns default config (paths)."""
        paths = SpecWeavePaths()
        assert paths.features_dir == Path("specs/behavior/features")
        assert paths.tests_dir == Path("tests")

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_frozen(self) -> None:
        """Loading with no file returns default config (frozen)."""
        paths = SpecWeavePaths()
        with pytest.raises(AttributeError):
            paths.features_dir = Path("other")  # type: ignore[misc]


class TestSpecWeaveConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_defaults(self) -> None:
        """Loading with no file returns default config."""
        config = SpecWeaveConfig()
        assert config.schema_version == 1
        assert config.spelling == "behavior"

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_frozen(self) -> None:
        """Loading with no file returns default config (frozen)."""
        config = SpecWeaveConfig()
        with pytest.raises(AttributeError):
            config.spelling = "other"  # type: ignore[misc]


class TestSpecWeaveGherkin:
    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_default_document_format(self) -> None:
        """Loading with no file returns default config (document_format)."""
        g = SpecWeaveGherkin()
        assert g.document_format == "markdown"

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_default_feature_extension(self) -> None:
        """Loading with no file returns default config (feature_extension)."""
        g = SpecWeaveGherkin()
        assert g.feature_extension == ".feature.md"

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_invalid_document_format_raises(self) -> None:
        """Loading with no file returns default config (invalid format)."""
        with pytest.raises(ValueError, match="document_format"):
            SpecWeaveGherkin(document_format="invalid")

    # specweave: feature=specs/behavior/features/config/configuration.feature.md
    # specweave: scenario=@bdd-config-load-defaults
    def test_invalid_markdown_parser_raises(self) -> None:
        """Loading with no file returns default config (invalid parser)."""
        with pytest.raises(ValueError, match="markdown_parser"):
            SpecWeaveGherkin(markdown_parser="bogus")
