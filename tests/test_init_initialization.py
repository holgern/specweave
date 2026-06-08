"""Tests for specweave init."""

from __future__ import annotations

from pathlib import Path

from specweave.init import _readme_is_specweave_managed, init_result_to_dict, run_init

FEATURE = "specs/behavior/features/init/initialization.feature.md"


class TestInitDefault:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-dotfile
    def test_creates_default_config_and_layout(self, tmp_path: Path) -> None:
        """Init creates .specweave.toml by default."""
        result = run_init(
            config_path=tmp_path / ".specweave.toml", project_root=tmp_path
        )
        assert result.config_path == tmp_path / ".specweave.toml"
        assert (tmp_path / ".specweave.toml").exists()
        assert (tmp_path / ".specweave").is_dir()
        assert (tmp_path / ".specweave" / "reports").is_dir()
        assert (tmp_path / ".specweave" / "evidence").is_dir()
        assert (tmp_path / ".specweave" / "mappings").is_dir()
        assert (tmp_path / "specs" / "behavior" / "README.md").exists()
        assert (tmp_path / "specs" / "behavior" / "features" / ".gitkeep").exists()
        assert (tmp_path / "reports" / "behavior").is_dir()

    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-gitkeep
    def test_creates_behavior_paths(self, tmp_path: Path) -> None:
        """Init creates .gitkeep in features directory."""
        result = run_init(
            config_path=tmp_path / ".specweave.toml", project_root=tmp_path
        )
        created_names = [str(p) for p in result.created]
        assert any("specs" in n and "behavior" in n for n in created_names)


class TestInitBritishSpelling:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-british-spelling
    def test_creates_behaviour_layout(self, tmp_path: Path) -> None:
        """Init creates behaviour layout with --spelling behaviour."""
        run_init(
            config_path=tmp_path / ".specweave.toml",
            spelling="behaviour",
            project_root=tmp_path,
        )
        assert (tmp_path / "specs" / "behaviour" / "README.md").exists()
        assert (tmp_path / "specs" / "behaviour" / "features" / ".gitkeep").exists()
        assert (tmp_path / "reports" / "behaviour").is_dir()


class TestInitPublicConfig:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-public-config
    def test_writes_specweave_toml(self, tmp_path: Path) -> None:
        """Init creates specweave.toml with --public-config."""
        run_init(config_path=tmp_path / "specweave.toml", project_root=tmp_path)
        assert (tmp_path / "specweave.toml").exists()
        assert not (tmp_path / ".specweave.toml").exists()


class TestInitIdempotency:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-idempotent
    def test_does_not_overwrite_existing_config(self, tmp_path: Path) -> None:
        """Running init twice does not fail."""
        config_path = tmp_path / ".specweave.toml"
        config_path.write_text("schema_version = 1\ncustom = true\n")
        original = config_path.read_text()

        result = run_init(config_path=config_path, project_root=tmp_path)
        assert config_path.read_text() == original
        assert any("already exists" in w for w in result.warnings)

    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-refuses-overwrite-readme
    def test_does_not_overwrite_non_specweave_readme(self, tmp_path: Path) -> None:
        """Init skips non-SpecWeave README."""
        readme = tmp_path / "specs" / "behavior" / "README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("# My custom project\n")

        result = run_init(
            config_path=tmp_path / ".specweave.toml", project_root=tmp_path
        )
        assert readme.read_text() == "# My custom project\n"
        assert readme in result.skipped

    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-warns-existing-config
    def test_reports_existing_directories(self, tmp_path: Path) -> None:
        """Init warns when config already exists."""
        (tmp_path / ".specweave").mkdir()
        result = run_init(
            config_path=tmp_path / ".specweave.toml", project_root=tmp_path
        )
        assert tmp_path / ".specweave" in result.existing


class TestInitForce:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-force-overwrites-readme
    def test_force_overwrites_generated_config_only(self, tmp_path: Path) -> None:
        """Init overwrites managed README with --force."""
        config_path = tmp_path / ".specweave.toml"
        config_path.write_text("schema_version = 1\nold = true\n")

        result = run_init(config_path=config_path, force=True, project_root=tmp_path)
        new_content = config_path.read_text()
        assert "old = true" not in new_content
        assert config_path in result.existing


class TestInitDryRun:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-dry-run
    def test_writes_nothing(self, tmp_path: Path) -> None:
        """Dry-run reports paths without writing."""
        result = run_init(
            config_path=tmp_path / ".specweave.toml",
            dry_run=True,
            project_root=tmp_path,
        )
        assert not (tmp_path / ".specweave.toml").exists()
        assert not (tmp_path / ".specweave").exists()
        assert len(result.created) > 0


class TestInitJsonShape:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-dotfile
    def test_json_shape(self, tmp_path: Path) -> None:
        """Init creates .specweave.toml by default (JSON shape)."""
        result = run_init(
            config_path=tmp_path / ".specweave.toml", project_root=tmp_path
        )
        data = init_result_to_dict(result)
        assert data["schema_version"] == 1
        assert data["command"] == "init"
        assert data["status"] == "ok"
        assert "created" in data
        assert "existing" in data
        assert "skipped" in data
        assert "warnings" in data
        # All paths are strings
        for p in data["created"]:
            assert isinstance(p, str)


class TestReadmeIsSpecweaveManaged:
    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-readme
    def test_nonexistent(self) -> None:
        """Init creates a managed README in specs root."""
        assert _readme_is_specweave_managed(Path("/fake")) is False

    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-readme
    def test_non_managed_content(self, tmp_path: Path) -> None:
        """Init creates a managed README in specs root."""
        readme = tmp_path / "README.md"
        readme.write_text("# Custom")
        assert _readme_is_specweave_managed(readme) is False

    # specweave: feature=specs/behavior/features/init/initialization.feature.md
    # specweave: scenario=@bdd-init-creates-readme
    def test_managed_content(self, tmp_path: Path) -> None:
        """Init creates a managed README in specs root."""
        readme = tmp_path / "README.md"
        readme.write_text("# Specs\nThis directory is managed by SpecWeave.\n")
        assert _readme_is_specweave_managed(readme) is True
