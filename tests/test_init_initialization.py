"""Tests for specweave init."""

from __future__ import annotations

from pathlib import Path

from specweave.init import _readme_is_specweave_managed, init_result_to_dict, run_init

FEATURE = "specs/behavior/features/init/initialization.feature"


class TestInitDefault:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-creates-public-config
    def test_creates_default_config_and_layout(self, tmp_path: Path) -> None:
        result = run_init(
            config_path=tmp_path / "specweave.toml",
            project_root=tmp_path,
        )
        assert result.config_path == tmp_path / "specweave.toml"
        assert (tmp_path / "specweave.toml").exists()
        assert (tmp_path / "specs" / "behavior" / "evidence").is_dir()
        assert (tmp_path / "specs" / "behavior" / "mappings").is_dir()
        assert (tmp_path / "specs" / "behavior" / "reports" / "specweave").is_dir()
        assert (tmp_path / "specs" / "behavior" / "README.md").exists()
        assert (tmp_path / "specs" / "behavior" / "features" / ".gitkeep").exists()
        assert (tmp_path / "specs" / "behavior" / "evidence" / ".gitkeep").exists()
        assert (tmp_path / "specs" / "behavior" / "mappings" / ".gitkeep").exists()
        assert (
            tmp_path / "specs" / "behavior" / "reports" / "specweave" / ".gitkeep"
        ).exists()
        assert (tmp_path / "specs" / "behavior" / "reports").is_dir()
        assert not (tmp_path / ".specweave").exists()

    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-creates-gitkeep
    def test_creates_behavior_paths(self, tmp_path: Path) -> None:
        result = run_init(
            config_path=tmp_path / "specweave.toml",
            project_root=tmp_path,
        )
        created_names = [str(p) for p in result.created]
        assert any("specs" in n and "behavior" in n for n in created_names)


class TestInitBritishSpelling:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-british-spelling
    def test_creates_behaviour_layout(self, tmp_path: Path) -> None:
        run_init(
            config_path=tmp_path / "specweave.toml",
            spelling="behaviour",
            project_root=tmp_path,
        )
        assert (tmp_path / "specs" / "behaviour" / "README.md").exists()
        assert (tmp_path / "specs" / "behaviour" / "features" / ".gitkeep").exists()
        assert (tmp_path / "specs" / "behaviour" / "evidence" / ".gitkeep").exists()
        assert (tmp_path / "specs" / "behaviour" / "mappings" / ".gitkeep").exists()
        assert (
            tmp_path / "specs" / "behaviour" / "reports" / "specweave" / ".gitkeep"
        ).exists()
        assert (tmp_path / "specs" / "behaviour" / "evidence").is_dir()
        assert (tmp_path / "specs" / "behaviour" / "mappings").is_dir()
        assert (tmp_path / "specs" / "behaviour" / "reports" / "specweave").is_dir()


class TestInitCompatibility:
    def test_hidden_config_path_still_works_when_explicit(self, tmp_path: Path) -> None:
        run_init(config_path=tmp_path / ".specweave.toml", project_root=tmp_path)
        assert (tmp_path / ".specweave.toml").exists()


class TestInitIdempotency:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-idempotent
    def test_does_not_overwrite_existing_config(self, tmp_path: Path) -> None:
        config_path = tmp_path / "specweave.toml"
        config_path.write_text("schema_version = 1\ncustom = true\n")
        original = config_path.read_text()

        result = run_init(config_path=config_path, project_root=tmp_path)
        assert config_path.read_text() == original
        assert any("already exists" in w for w in result.warnings)

    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-refuses-overwrite-readme
    def test_does_not_overwrite_non_specweave_readme(self, tmp_path: Path) -> None:
        readme = tmp_path / "specs" / "behavior" / "README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("# My custom project\n")

        result = run_init(
            config_path=tmp_path / "specweave.toml",
            project_root=tmp_path,
        )
        assert readme.read_text() == "# My custom project\n"
        assert readme in result.skipped

    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-warns-existing-config
    def test_reports_existing_directories(self, tmp_path: Path) -> None:
        (tmp_path / "specs" / "behavior" / "evidence").mkdir(parents=True)
        result = run_init(
            config_path=tmp_path / "specweave.toml",
            project_root=tmp_path,
        )
        assert tmp_path / "specs" / "behavior" / "evidence" in result.existing


class TestInitForce:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-force-overwrites-readme
    def test_force_overwrites_generated_config_only(self, tmp_path: Path) -> None:
        config_path = tmp_path / "specweave.toml"
        config_path.write_text("schema_version = 1\nold = true\n")

        result = run_init(config_path=config_path, force=True, project_root=tmp_path)
        new_content = config_path.read_text()
        assert "old = true" not in new_content
        assert config_path in result.existing


class TestInitDryRun:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-dry-run
    def test_writes_nothing(self, tmp_path: Path) -> None:
        result = run_init(
            config_path=tmp_path / "specweave.toml",
            dry_run=True,
            project_root=tmp_path,
        )
        assert not (tmp_path / "specweave.toml").exists()
        assert not (tmp_path / "specs" / "behavior" / "reports" / "specweave").exists()
        assert not (tmp_path / "specs" / "behavior" / "evidence").exists()
        assert len(result.created) > 0


class TestInitJsonShape:
    def test_json_shape(self, tmp_path: Path) -> None:
        result = run_init(
            config_path=tmp_path / "specweave.toml",
            project_root=tmp_path,
        )
        data = init_result_to_dict(result)
        assert data["schema_version"] == 1
        assert data["command"] == "init"
        assert data["status"] == "ok"
        assert "created" in data
        assert "existing" in data
        assert "skipped" in data
        assert "warnings" in data
        for p in data["created"]:
            assert isinstance(p, str)


class TestReadmeIsSpecweaveManaged:
    # specweave: feature=specs/behavior/features/init/initialization.feature
    # specweave: scenario=@bdd-init-creates-readme
    def test_nonexistent(self) -> None:
        assert _readme_is_specweave_managed(Path("/fake")) is False

    def test_non_managed_content(self, tmp_path: Path) -> None:
        readme = tmp_path / "README.md"
        readme.write_text("# Custom")
        assert _readme_is_specweave_managed(readme) is False

    def test_managed_content(self, tmp_path: Path) -> None:
        readme = tmp_path / "README.md"
        readme.write_text("# Specs\nThis directory is managed by SpecWeave.\n")
        assert _readme_is_specweave_managed(readme) is True
