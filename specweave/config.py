"""SpecWeave configuration: dataclasses, discovery, loading, and rendering."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SpecWeavePaths:
    """Resolved directory and file paths for a SpecWeave project."""

    specs_root: Path = Path("specs/behavior")
    features_dir: Path = Path("specs/behavior/features")
    behavior_readme: Path = Path("specs/behavior/README.md")
    manifest: Path = Path("specs/behavior/manifest.json")
    tests_dir: Path = Path("tests")
    reports_dir: Path = Path("reports/behavior")
    state_dir: Path = Path(".specweave")
    evidence_dir: Path = Path(".specweave/evidence")
    reports_state_dir: Path = Path(".specweave/reports")
    mapping_dir: Path = Path(".specweave/mappings")


@dataclass(frozen=True)
class SpecWeavePytest:
    """Pytest discovery configuration."""

    test_globs: tuple[str, ...] = ("tests/test_*.py", "tests/**/*_test.py")
    ignore_globs: tuple[str, ...] = (".venv/**", "build/**", "dist/**")


@dataclass(frozen=True)
class SpecWeaveGherkin:
    """Gherkin generation configuration."""

    dialect: str = "en"
    document_format: str = "markdown"  # markdown | classic
    feature_extension: str = ".feature.md"
    feature_extensions: tuple[str, ...] = (".feature.md", ".feature")
    official_parser: bool = True
    markdown_parser: str = "specweave"  # specweave | cucumber-js | off
    compile_pickles: bool = False
    default_scenario_keyword: str = "Example"
    require_given_when_then: bool = True
    require_bdd_ids: bool = True
    id_style: str = "slug"
    include_generated_tag: bool = True
    include_needs_review_tag: bool = True
    canonical_task_tags: bool = False

    def __post_init__(self) -> None:
        if self.document_format not in ("markdown", "classic"):
            raise ValueError(
                f"Unsupported document_format: {self.document_format}; "
                "expected 'markdown' or 'classic'"
            )
        if self.markdown_parser not in ("specweave", "cucumber-js", "off"):
            raise ValueError(
                f"Unsupported markdown_parser: {self.markdown_parser}; "
                "expected 'specweave', 'cucumber-js', or 'off'"
            )


@dataclass(frozen=True)
class SpecWeaveGeneration:
    """Code/spec generation configuration."""

    group_by: str = "file"
    mode: str = "create"
    preserve_manual_edits: bool = True
    mark_generated_from_tests: bool = True


@dataclass(frozen=True)
class SpecWeaveConfig:
    """Full SpecWeave project configuration."""

    schema_version: int = 1
    project_root: Path = Path(".")
    spelling: str = "behavior"
    gitkeep: bool = True
    paths: SpecWeavePaths = field(default_factory=SpecWeavePaths)
    pytest: SpecWeavePytest = field(default_factory=SpecWeavePytest)
    gherkin: SpecWeaveGherkin = field(default_factory=SpecWeaveGherkin)
    generation: SpecWeaveGeneration = field(default_factory=SpecWeaveGeneration)
    test_command: str = "pytest --junitxml=reports/behavior/pytest-junit.xml"
    agent_json_default: bool = False

    def __post_init__(self) -> None:
        if self.spelling != "behavior" and self.paths == SpecWeavePaths():
            s = self.spelling
            spec_segment = f"specs/{s}"
            report_segment = f"reports/{s}"
            object.__setattr__(
                self,
                "paths",
                SpecWeavePaths(
                    specs_root=Path(spec_segment),
                    features_dir=Path(f"{spec_segment}/features"),
                    behavior_readme=Path(f"{spec_segment}/README.md"),
                    manifest=Path(f"{spec_segment}/manifest.json"),
                    reports_dir=Path(report_segment),
                ),
            )
            object.__setattr__(
                self, "test_command", f"pytest --junitxml=reports/{s}/pytest-junit.xml"
            )


_CONFIG_NAMES = (".specweave.toml", "specweave.toml")


def find_config(start: Path | None = None) -> Path | None:
    """Walk up from *start* looking for a SpecWeave config file.

    If *start* is already a file, return it directly.
    """
    if start is None:
        start = Path.cwd()
    if start.is_file():
        return start
    for directory in (start, *start.parents):
        for name in _CONFIG_NAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate
    return None


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------


def _toml_load(text: str) -> dict:
    if sys.version_info >= (3, 11):
        import tomllib

        return tomllib.loads(text)
    import tomli

    return tomli.loads(text)


def load_config(config_path: Path | None = None) -> SpecWeaveConfig:
    """Load configuration from *config_path* or discovered config.

    Returns default config when no file is found.
    """
    if config_path is None:
        config_path = find_config()

    if config_path is None:
        return SpecWeaveConfig()

    if not config_path.exists():
        return SpecWeaveConfig()

    raw = _toml_load(config_path.read_text(encoding="utf-8"))

    if raw.get("schema_version", 1) != 1:
        raise ValueError(
            f"Unsupported specweave config schema_version: {raw.get('schema_version')}"
        )

    spelling = raw.get("spelling", "behavior")
    paths_data = raw.get("paths", {})
    pytest_data = raw.get("pytest", {})
    gherkin_data = raw.get("gherkin", {})
    generation_data = raw.get("generation", {})
    commands_data = raw.get("commands", {})
    agent_data = raw.get("agent", {})

    paths = _build_paths(spelling, paths_data)
    pytest_cfg = _build_pytest(pytest_data)
    gherkin_cfg = _build_gherkin(gherkin_data)
    generation_cfg = _build_generation(generation_data)

    return SpecWeaveConfig(
        schema_version=raw.get("schema_version", 1),
        project_root=Path(raw.get("project_root", ".")),
        spelling=spelling,
        gitkeep=raw.get("gitkeep", True),
        paths=paths,
        pytest=pytest_cfg,
        gherkin=gherkin_cfg,
        generation=generation_cfg,
        test_command=commands_data.get(
            "test", "pytest --junitxml=reports/behavior/pytest-junit.xml"
        ),
        agent_json_default=agent_data.get("json_default", False),
    )


def _build_paths(spelling: str, data: dict) -> SpecWeavePaths:
    spec_segment = f"specs/{spelling}"
    report_segment = f"reports/{spelling}"

    return SpecWeavePaths(
        specs_root=Path(data.get("specs_root", f"{spec_segment}")),
        features_dir=Path(data.get("features_dir", f"{spec_segment}/features")),
        behavior_readme=Path(data.get("behavior_readme", f"{spec_segment}/README.md")),
        manifest=Path(data.get("manifest", f"{spec_segment}/manifest.json")),
        tests_dir=Path(data.get("tests_dir", "tests")),
        reports_dir=Path(data.get("reports_dir", f"{report_segment}")),
        state_dir=Path(data.get("state_dir", ".specweave")),
        evidence_dir=Path(data.get("evidence_dir", ".specweave/evidence")),
        reports_state_dir=Path(data.get("reports_state_dir", ".specweave/reports")),
        mapping_dir=Path(data.get("mapping_dir", ".specweave/mappings")),
    )


def _build_pytest(data: dict) -> SpecWeavePytest:
    return SpecWeavePytest(
        test_globs=tuple(data.get("test_globs", SpecWeavePytest().test_globs)),
        ignore_globs=tuple(data.get("ignore_globs", SpecWeavePytest().ignore_globs)),
    )


def _build_gherkin(data: dict) -> SpecWeaveGherkin:
    defaults = SpecWeaveGherkin()
    return SpecWeaveGherkin(
        dialect=data.get("dialect", defaults.dialect),
        document_format=data.get("document_format", defaults.document_format),
        feature_extension=data.get("feature_extension", defaults.feature_extension),
        feature_extensions=tuple(
            data.get("feature_extensions", list(defaults.feature_extensions))
        ),
        official_parser=data.get("official_parser", defaults.official_parser),
        markdown_parser=data.get("markdown_parser", defaults.markdown_parser),
        compile_pickles=data.get("compile_pickles", defaults.compile_pickles),
        default_scenario_keyword=data.get(
            "default_scenario_keyword", defaults.default_scenario_keyword
        ),
        require_given_when_then=data.get(
            "require_given_when_then", defaults.require_given_when_then
        ),
        require_bdd_ids=data.get("require_bdd_ids", defaults.require_bdd_ids),
        id_style=data.get("id_style", defaults.id_style),
        include_generated_tag=data.get(
            "include_generated_tag", defaults.include_generated_tag
        ),
        include_needs_review_tag=data.get(
            "include_needs_review_tag", defaults.include_needs_review_tag
        ),
        canonical_task_tags=data.get(
            "canonical_task_tags", defaults.canonical_task_tags
        ),
    )


def _build_generation(data: dict) -> SpecWeaveGeneration:
    defaults = SpecWeaveGeneration()
    return SpecWeaveGeneration(
        group_by=data.get("group_by", defaults.group_by),
        mode=data.get("mode", defaults.mode),
        preserve_manual_edits=data.get(
            "preserve_manual_edits", defaults.preserve_manual_edits
        ),
        mark_generated_from_tests=data.get(
            "mark_generated_from_tests", defaults.mark_generated_from_tests
        ),
    )


# ---------------------------------------------------------------------------
# Default config rendering
# ---------------------------------------------------------------------------


def render_default_config(*, spelling: str = "behavior") -> str:
    """Render the default TOML config as a deterministic string."""
    s = spelling
    spec_segment = f"specs/{s}"
    report_segment = f"reports/{s}"

    return (
        f"schema_version = 1\n"
        f'project_root = "."\n'
        f'spelling = "{s}"\n'
        f"\n"
        f"[paths]\n"
        f'specs_root = "{spec_segment}"\n'
        f'features_dir = "{spec_segment}/features"\n'
        f'behavior_readme = "{spec_segment}/README.md"\n'
        f'manifest = "{spec_segment}/manifest.json"\n'
        f'tests_dir = "tests"\n'
        f'reports_dir = "{report_segment}"\n'
        f'state_dir = ".specweave"\n'
        f'evidence_dir = ".specweave/evidence"\n'
        f'reports_state_dir = ".specweave/reports"\n'
        f'mapping_dir = ".specweave/mappings"\n'
        f"\n"
        f"gitkeep = true\n"
        f"\n"
        f"[pytest]\n"
        f'test_globs = ["tests/test_*.py", "tests/**/*_test.py"]\n'
        f'ignore_globs = [".venv/**", "build/**", "dist/**"]\n'
        f"\n"
        f"[gherkin]\n"
        f'dialect = "en"\n'
        f'document_format = "markdown"\n'
        f'feature_extension = ".feature.md"\n'
        f'feature_extensions = [".feature.md", ".feature"]\n'
        f"official_parser = true\n"
        f'markdown_parser = "specweave"\n'
        f"compile_pickles = false\n"
        f'default_scenario_keyword = "Example"\n'
        f"require_given_when_then = true\n"
        f"require_bdd_ids = true\n"
        f'id_style = "slug"\n'
        f"include_generated_tag = true\n"
        f"include_needs_review_tag = true\n"
        f"canonical_task_tags = false\n"
        f"\n"
        f"[generation]\n"
        f'group_by = "file"\n'
        f'mode = "create"\n'
        f"preserve_manual_edits = true\n"
        f"mark_generated_from_tests = true\n"
        f"\n"
        f"[commands]\n"
        f'test = "pytest --junitxml=reports/{s}/pytest-junit.xml"\n'
        f"\n"
        f"[agent]\n"
        f"json_default = false\n"
    )


# ---------------------------------------------------------------------------
# Backward-compatible constants (existing code uses these)
# ---------------------------------------------------------------------------

REPORT_DIR = Path(".specweave/reports")
"""Default directory for runner summary reports."""

BEHAVIOR_FEATURES_DIR = Path("specs/behavior/features")
BEHAVIOR_INDEX_PATH = Path("specs/behavior/README.md")
BEHAVIOR_MANIFEST_PATH = Path("specs/behavior/manifest.json")
PYTEST_TESTS_DIR = Path("tests")
BEHAVIOR_REPORTS_DIR = Path("reports/behavior")
SPECWEAVE_REPORTS_DIR = REPORT_DIR
SPECWEAVE_EVIDENCE_DIR = Path(".specweave/evidence")
SPECWEAVE_MAPPING_DIR = Path(".specweave/mappings")

# Compatibility aliases retained for older code paths.
FEATURES_DIR = BEHAVIOR_FEATURES_DIR
BDD_INDEX_PATH = BEHAVIOR_INDEX_PATH
BDD_MANIFEST_PATH = BEHAVIOR_MANIFEST_PATH
BDD_TESTS_DIR = PYTEST_TESTS_DIR
BDD_REPORTS_DIR = BEHAVIOR_REPORTS_DIR
