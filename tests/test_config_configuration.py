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

FEATURE = "specs/behavior/features/config/configuration.feature"


class TestFindConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-discovery-finds-dotfile
    def test_prefers_explicit(self, tmp_path: Path) -> None:
        config_file = tmp_path / "my-config.toml"
        config_file.write_text("schema_version = 1\n")
        assert find_config(config_file) == config_file

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-discovery-prefers-public
    def test_prefers_public_over_dotfile(self, tmp_path: Path) -> None:
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        (tmp_path / "specweave.toml").write_text("schema_version = 1\n")
        found = find_config(tmp_path)
        assert found is not None
        assert found.name == "specweave.toml"

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-discovery-returns-none
    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        assert find_config(tmp_path) is None

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-discovery-finds-hidden
    def test_finds_hidden_config(self, tmp_path: Path) -> None:
        (tmp_path / ".specweave.toml").write_text("schema_version = 1\n")
        found = find_config(tmp_path)
        assert found is not None
        assert found.name == ".specweave.toml"

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-discovery-walks-parents
    def test_walks_up_directories(self, tmp_path: Path) -> None:
        (tmp_path / "specweave.toml").write_text("schema_version = 1\n")
        child = tmp_path / "sub" / "deep"
        child.mkdir(parents=True)
        found = find_config(child)
        assert found is not None
        assert found.name == "specweave.toml"


class TestLoadConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-load-defaults
    def test_defaults_when_missing(self) -> None:
        config = load_config(Path("/nonexistent"))
        assert config.schema_version == 1
        assert config.spelling == "behavior"
        assert config.paths.features_dir == Path("specs/behavior/features")
        assert config.paths.evidence_dir == Path("specs/behavior/evidence")

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-rejects-unsupported-schema
    def test_rejects_unsupported_schema(self, tmp_path: Path) -> None:
        config_file = tmp_path / "specweave.toml"
        config_file.write_text("schema_version = 99\n")
        with pytest.raises(ValueError, match="Unsupported"):
            load_config(config_file)

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-load-from-file
    def test_normalizes_paths(self, tmp_path: Path) -> None:
        config_file = tmp_path / "specweave.toml"
        config_file.write_text(
            'schema_version = 1\nspelling = "behaviour"\n'
            '[paths]\nfeatures_dir = "specs/behaviour/features"\n'
        )
        config = load_config(config_file)
        assert config.spelling == "behaviour"
        assert config.paths.features_dir == tmp_path / "specs/behaviour/features"

    def test_loads_all_sections(self, tmp_path: Path) -> None:
        config_file = tmp_path / "specweave.toml"
        config_file.write_text(
            "schema_version = 1\n"
            'spelling = "behavior"\n'
            "[paths]\n"
            'reports_state_dir = "specs/behavior/reports/specweave"\n'
            "[pytest]\n"
            'test_globs = ["tests/test_*.py"]\n'
            "[gherkin]\n"
            'id_style = "sequence"\n'
            "[generation]\n"
            'group_by = "file"\n'
        )
        config = load_config(config_file)
        assert config.pytest.test_globs == ("tests/test_*.py",)
        assert config.gherkin.id_style == "sequence"
        assert config.generation.group_by == "file"
        assert config.paths.reports_state_dir == (
            tmp_path / "specs/behavior/reports/specweave"
        )

    def test_resolves_paths_from_config_project_root(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "specweave.toml"
        config_file.write_text(
            'schema_version = 1\nproject_root = "../project"\n'
            '[paths]\nfeatures_dir = "features"\n',
            encoding="utf-8",
        )

        config = load_config(config_file)

        assert config.project_root == (tmp_path / "project").resolve()
        assert config.paths.features_dir == (tmp_path / "project/features").resolve()

    def test_rejects_unsupported_group_by(self, tmp_path: Path) -> None:
        config_file = tmp_path / "specweave.toml"
        config_file.write_text(
            'schema_version = 1\n[generation]\ngroup_by = "area"\n',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="group_by"):
            load_config(config_file)

    def test_gherkin_fields_preserved(self, tmp_path: Path) -> None:
        config_file = tmp_path / "specweave.toml"
        config_file.write_text(
            "schema_version = 1\n"
            "[gherkin]\n"
            "official_parser = true\n"
            "compile_pickles = true\n"
            'default_scenario_keyword = "Scenario"\n'
        )
        config = load_config(config_file)
        assert config.gherkin.official_parser is True
        assert config.gherkin.compile_pickles is True
        assert config.gherkin.default_scenario_keyword == "Scenario"


class TestRenderDefaultConfig:
    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-render-behavior
    def test_renders_behavior(self) -> None:
        text = render_default_config(spelling="behavior")
        assert 'spelling = "behavior"' in text
        assert 'evidence_dir = "specs/behavior/evidence"' in text
        assert 'reports_state_dir = "specs/behavior/reports/specweave"' in text

    # specweave: feature=specs/behavior/features/config/configuration.feature
    # specweave: scenario=@bdd-config-render-behaviour
    def test_renders_behaviour(self) -> None:
        text = render_default_config(spelling="behaviour")
        assert 'spelling = "behaviour"' in text
        assert 'evidence_dir = "specs/behaviour/evidence"' in text
        assert 'reports_state_dir = "specs/behaviour/reports/specweave"' in text

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
        config_file = tmp_path / "specweave.toml"
        config_file.write_text(text)
        config = load_config(config_file)
        assert config.schema_version == 1
        assert config.spelling == "behavior"

    def test_renders_classic_only_defaults(self) -> None:
        text = render_default_config()
        assert "official_parser = false" in text
        assert "compile_pickles = false" in text
        assert 'default_scenario_keyword = "Example"' in text
        assert "document_format" not in text
        assert "feature_extension" not in text
        assert "feature_extensions" not in text
        assert "markdown_parser" not in text
        assert "\nstate_dir =" not in text


class TestSpecWeavePaths:
    def test_defaults(self) -> None:
        paths = SpecWeavePaths()
        assert paths.features_dir == Path("specs/behavior/features")
        assert paths.tests_dir == Path("tests")
        assert paths.evidence_dir == Path("specs/behavior/evidence")
        assert paths.mapping_dir == Path("specs/behavior/mappings")

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


class TestSpecWeaveGherkin:
    def test_default_official_parser_is_false(self) -> None:
        g = SpecWeaveGherkin()
        assert g.official_parser is False

    def test_default_keyword_is_example(self) -> None:
        g = SpecWeaveGherkin()
        assert g.default_scenario_keyword == "Example"

    def test_compile_pickles_without_official_raises(self) -> None:
        with pytest.raises(ValueError, match="compile_pickles"):
            SpecWeaveGherkin(compile_pickles=True, official_parser=False)

    def test_compile_pickles_with_official_ok(self) -> None:
        g = SpecWeaveGherkin(compile_pickles=True, official_parser=True)
        assert g.compile_pickles is True
