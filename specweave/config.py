"""SpecWeave configuration: dataclasses, discovery, loading, and rendering."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path


def _default_behaviour_paths(
    *,
    specs_root: Path = Path("specs"),
    spelling: str = "behaviour",
) -> SpecWeaveBehaviourPaths:
    root = specs_root / spelling
    reports_dir = root / "reports"
    return SpecWeaveBehaviourPaths(
        root=root,
        features_dir=root / "features",
        readme=root / "README.md",
        manifest=root / "manifest.json",
        mappings_dir=root / "mappings",
        evidence_dir=root / "evidence",
        reports_dir=reports_dir,
        reports_state_dir=reports_dir / "specweave",
    )


def _default_specification_paths(
    *,
    specs_root: Path = Path("specs"),
) -> SpecWeaveSpecificationPaths:
    root = specs_root / "specifications"
    reports_dir = root / "reports"
    return SpecWeaveSpecificationPaths(
        root=root,
        product_spec=root / "product.spec.md",
        readme=root / "README.md",
        manifest=root / "manifest.json",
        capabilities_dir=root / "capabilities",
        interfaces_dir=root / "interfaces",
        integrations_dir=root / "integrations",
        mappings_dir=root / "mappings",
        evidence_dir=root / "evidence",
        reports_dir=reports_dir,
        reports_state_dir=reports_dir / "specweave",
    )


@dataclass(frozen=True)
class SpecWeaveBehaviourPaths:
    """Resolved behaviour-mode directory and file paths."""

    root: Path = Path("specs/behaviour")
    features_dir: Path = Path("specs/behaviour/features")
    readme: Path = Path("specs/behaviour/README.md")
    manifest: Path = Path("specs/behaviour/manifest.json")
    mappings_dir: Path = Path("specs/behaviour/mappings")
    evidence_dir: Path = Path("specs/behaviour/evidence")
    reports_dir: Path = Path("specs/behaviour/reports")
    reports_state_dir: Path = Path("specs/behaviour/reports/specweave")


@dataclass(frozen=True)
class SpecWeaveSpecificationPaths:
    """Resolved specifications-mode directory and file paths."""

    root: Path = Path("specs/specifications")
    product_spec: Path = Path("specs/specifications/product.spec.md")
    readme: Path = Path("specs/specifications/README.md")
    manifest: Path = Path("specs/specifications/manifest.json")
    capabilities_dir: Path = Path("specs/specifications/capabilities")
    interfaces_dir: Path = Path("specs/specifications/interfaces")
    integrations_dir: Path = Path("specs/specifications/integrations")
    mappings_dir: Path = Path("specs/specifications/mappings")
    evidence_dir: Path = Path("specs/specifications/evidence")
    reports_dir: Path = Path("specs/specifications/reports")
    reports_state_dir: Path = Path("specs/specifications/reports/specweave")


@dataclass(frozen=True, init=False)
class SpecWeavePaths:
    """Resolved directory and file paths for a SpecWeave project."""

    specs_root: Path
    tests_dir: Path
    behaviour: SpecWeaveBehaviourPaths
    specifications: SpecWeaveSpecificationPaths | None

    def __init__(
        self,
        *,
        specs_root: Path = Path("specs"),
        tests_dir: Path = Path("tests"),
        behaviour: SpecWeaveBehaviourPaths | None = None,
        specifications: SpecWeaveSpecificationPaths | None = None,
        features_dir: Path | None = None,
        behavior_readme: Path | None = None,
        manifest: Path | None = None,
        reports_dir: Path | None = None,
        evidence_dir: Path | None = None,
        reports_state_dir: Path | None = None,
        mapping_dir: Path | None = None,
    ) -> None:
        normalized_specs_root = specs_root
        if behaviour is None and _has_legacy_behaviour_overrides(
            features_dir=features_dir,
            behavior_readme=behavior_readme,
            manifest=manifest,
            reports_dir=reports_dir,
            evidence_dir=evidence_dir,
            reports_state_dir=reports_state_dir,
            mapping_dir=mapping_dir,
        ):
            behaviour = _build_behaviour_from_legacy(
                specs_root=specs_root,
                features_dir=features_dir,
                behavior_readme=behavior_readme,
                manifest=manifest,
                reports_dir=reports_dir,
                evidence_dir=evidence_dir,
                reports_state_dir=reports_state_dir,
                mapping_dir=mapping_dir,
            )
            normalized_specs_root = behaviour.root.parent
        elif behaviour is None and specs_root.name in {"behavior", "behaviour"}:
            normalized_specs_root = specs_root.parent
            behaviour = _default_behaviour_paths(
                specs_root=normalized_specs_root,
                spelling=specs_root.name,
            )
        elif behaviour is None:
            behaviour = _default_behaviour_paths(specs_root=specs_root)

        object.__setattr__(self, "specs_root", normalized_specs_root)
        object.__setattr__(self, "tests_dir", tests_dir)
        object.__setattr__(self, "behaviour", behaviour)
        object.__setattr__(self, "specifications", specifications)

    @property
    def features_dir(self) -> Path:
        return self.behaviour.features_dir

    @property
    def behavior_readme(self) -> Path:
        return self.behaviour.readme

    @property
    def manifest(self) -> Path:
        return self.behaviour.manifest

    @property
    def reports_dir(self) -> Path:
        return self.behaviour.reports_dir

    @property
    def evidence_dir(self) -> Path:
        return self.behaviour.evidence_dir

    @property
    def reports_state_dir(self) -> Path:
        return self.behaviour.reports_state_dir

    @property
    def mapping_dir(self) -> Path:
        return self.behaviour.mappings_dir


def _has_legacy_behaviour_overrides(
    *,
    features_dir: Path | None,
    behavior_readme: Path | None,
    manifest: Path | None,
    reports_dir: Path | None,
    evidence_dir: Path | None,
    reports_state_dir: Path | None,
    mapping_dir: Path | None,
) -> bool:
    return any(
        value is not None
        for value in (
            features_dir,
            behavior_readme,
            manifest,
            reports_dir,
            evidence_dir,
            reports_state_dir,
            mapping_dir,
        )
    )


def _build_behaviour_from_legacy(
    *,
    specs_root: Path,
    features_dir: Path | None,
    behavior_readme: Path | None,
    manifest: Path | None,
    reports_dir: Path | None,
    evidence_dir: Path | None,
    reports_state_dir: Path | None,
    mapping_dir: Path | None,
) -> SpecWeaveBehaviourPaths:
    root = _derive_legacy_behaviour_root(
        specs_root=specs_root,
        features_dir=features_dir,
        behavior_readme=behavior_readme,
        manifest=manifest,
        reports_dir=reports_dir,
        evidence_dir=evidence_dir,
        reports_state_dir=reports_state_dir,
        mapping_dir=mapping_dir,
    )
    default_reports_dir = root / "reports"
    return SpecWeaveBehaviourPaths(
        root=root,
        features_dir=features_dir or (root / "features"),
        readme=behavior_readme or (root / "README.md"),
        manifest=manifest or (root / "manifest.json"),
        mappings_dir=mapping_dir or (root / "mappings"),
        evidence_dir=evidence_dir or (root / "evidence"),
        reports_dir=reports_dir or default_reports_dir,
        reports_state_dir=reports_state_dir or (default_reports_dir / "specweave"),
    )


def _derive_legacy_behaviour_root(
    *,
    specs_root: Path,
    features_dir: Path | None,
    behavior_readme: Path | None,
    manifest: Path | None,
    reports_dir: Path | None,
    evidence_dir: Path | None,
    reports_state_dir: Path | None,
    mapping_dir: Path | None,
) -> Path:
    candidates = (
        (features_dir, 0),
        (behavior_readme, 0),
        (manifest, 0),
        (reports_dir, 0),
        (evidence_dir, 0),
        (reports_state_dir, 1),
        (mapping_dir, 0),
    )
    for candidate, parents_up in candidates:
        if candidate is not None:
            root = candidate
            for _ in range(parents_up + 1):
                root = root.parent
            return root
    if specs_root.name in {"behavior", "behaviour"}:
        return specs_root
    return specs_root / "behaviour"


@dataclass(frozen=True)
class SpecWeavePytest:
    """Pytest discovery configuration."""

    test_globs: tuple[str, ...] = ("tests/test_*.py", "tests/**/*_test.py")
    ignore_globs: tuple[str, ...] = (".venv/**", "build/**", "dist/**")


@dataclass(frozen=True)
class SpecWeaveGherkin:
    """Gherkin generation configuration."""

    dialect: str = "en"
    official_parser: bool = False
    compile_pickles: bool = False
    default_scenario_keyword: str = "Example"
    require_given_when_then: bool = True
    require_bdd_ids: bool = True
    id_style: str = "slug"
    include_generated_tag: bool = True
    include_needs_review_tag: bool = True
    canonical_task_tags: bool = False

    def __post_init__(self) -> None:
        if self.compile_pickles and not self.official_parser:
            raise ValueError(
                "compile_pickles requires official_parser to be enabled; "
                "install specweave[gherkin] and set official_parser = true."
            )


@dataclass(frozen=True)
class SpecWeaveBehaviour:
    """Behaviour-mode configuration."""

    require_bdd_ids: bool = True
    default_scenario_keyword: str = "Example"
    generated_tag: str = "generated"
    needs_review_tag: str = "needs-review"


@dataclass(frozen=True)
class SpecWeaveSpecifications:
    """Specifications-mode configuration."""

    require_requirement_ids: bool = True
    allowed_requirement_prefixes: tuple[str, ...] = (
        "REQ",
        "INV",
        "IF",
        "DATA",
        "NFR",
        "NGOAL",
        "RISK",
        "OPEN",
    )
    require_verification: bool = True
    require_rationale: bool = False


@dataclass(frozen=True)
class SpecWeaveGeneration:
    """Code/spec generation configuration."""

    group_by: str = "file"
    mode: str = "create"
    preserve_manual_edits: bool = True
    mark_generated_from_tests: bool = True

    def __post_init__(self) -> None:
        if self.group_by != "file":
            raise ValueError(
                f"Unsupported generation group_by: {self.group_by}; expected 'file'"
            )


@dataclass(frozen=True)
class SpecWeaveConfig:
    """Full SpecWeave project configuration."""

    schema_version: int = 1
    project_root: Path = Path(".")
    spelling: str = "behaviour"
    gitkeep: bool = True
    paths: SpecWeavePaths = field(default_factory=SpecWeavePaths)
    pytest: SpecWeavePytest = field(default_factory=SpecWeavePytest)
    gherkin: SpecWeaveGherkin = field(default_factory=SpecWeaveGherkin)
    behaviour: SpecWeaveBehaviour = field(default_factory=SpecWeaveBehaviour)
    specifications: SpecWeaveSpecifications | None = None
    generation: SpecWeaveGeneration = field(default_factory=SpecWeaveGeneration)
    test_command: str = "pytest --junitxml=specs/behaviour/reports/pytest-junit.xml"
    agent_json_default: bool = False

    def __post_init__(self) -> None:
        if self.spelling != "behaviour" and self.paths == SpecWeavePaths():
            object.__setattr__(
                self,
                "paths",
                SpecWeavePaths(
                    specs_root=Path("specs"),
                    tests_dir=Path("tests"),
                    behaviour=_default_behaviour_paths(
                        specs_root=Path("specs"),
                        spelling=self.spelling,
                    ),
                ),
            )
            default_command = _default_test_command(
                "behaviour",
                include_behaviour=True,
            )
            if self.test_command == default_command:
                object.__setattr__(
                    self,
                    "test_command",
                    _default_test_command(self.spelling, include_behaviour=True),
                )


_CONFIG_NAMES = ("specweave.toml", ".specweave.toml")


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


def _toml_load(text: str) -> dict:
    if sys.version_info >= (3, 11):
        import tomllib

        return tomllib.loads(text)
    import tomli

    return tomli.loads(text)


def load_config(config_path: Path | None = None) -> SpecWeaveConfig:
    """Load configuration from *config_path* or discovered config."""
    resolved_config_path = config_path or find_config()
    if resolved_config_path is None:
        return _default_project_config(Path.cwd())
    if not resolved_config_path.exists():
        return _default_project_config(resolved_config_path.parent)

    raw = _toml_load(resolved_config_path.read_text(encoding="utf-8"))

    if raw.get("schema_version", 1) != 1:
        raise ValueError(
            f"Unsupported specweave config schema_version: {raw.get('schema_version')}"
        )

    spelling = raw.get("spelling", "behaviour")
    paths_data = raw.get("paths", {})
    pytest_data = raw.get("pytest", {})
    gherkin_data = raw.get("gherkin", {})
    behaviour_data = raw.get("behaviour", {})
    specifications_data = raw.get("specifications")
    generation_data = raw.get("generation", {})
    commands_data = raw.get("commands", {})
    agent_data = raw.get("agent", {})

    project_root = Path(raw.get("project_root", "."))
    if not project_root.is_absolute():
        project_root = resolved_config_path.parent / project_root
    project_root = project_root.resolve()

    specifications_enabled = bool(specifications_data) or bool(
        paths_data.get("specifications")
    )
    paths = _resolve_paths(
        _build_paths(
            spelling,
            paths_data,
            enable_specifications=specifications_enabled,
        ),
        project_root,
    )
    pytest_cfg = _build_pytest(pytest_data)
    gherkin_cfg = _build_gherkin(gherkin_data)
    behaviour_cfg = _build_behaviour(behaviour_data, gherkin_cfg)
    specifications_cfg = (
        _build_specifications(specifications_data)
        if specifications_enabled or specifications_data is not None
        else None
    )
    generation_cfg = _build_generation(generation_data)

    include_behaviour = True
    return SpecWeaveConfig(
        schema_version=raw.get("schema_version", 1),
        project_root=project_root,
        spelling=spelling,
        gitkeep=raw.get("gitkeep", True),
        paths=paths,
        pytest=pytest_cfg,
        gherkin=gherkin_cfg,
        behaviour=behaviour_cfg,
        specifications=specifications_cfg,
        generation=generation_cfg,
        test_command=commands_data.get(
            "test",
            _default_test_command(
                spelling,
                include_behaviour=include_behaviour,
                include_specifications=paths.specifications is not None,
            ),
        ),
        agent_json_default=agent_data.get("json_default", False),
    )


def _default_project_config(project_root: Path) -> SpecWeaveConfig:
    specs_root = project_root / "specs"
    canonical_behaviour_root = specs_root / "behaviour"
    compatibility_behavior_root = specs_root / "behavior"
    spelling = "behaviour"
    if not canonical_behaviour_root.exists() and compatibility_behavior_root.exists():
        spelling = "behavior"
    specifications_enabled = (specs_root / "specifications").exists()
    return SpecWeaveConfig(
        project_root=project_root,
        spelling=spelling,
        paths=SpecWeavePaths(
            specs_root=Path("specs"),
            tests_dir=Path("tests"),
            behaviour=_default_behaviour_paths(
                specs_root=Path("specs"),
                spelling=spelling,
            ),
            specifications=(
                _default_specification_paths(specs_root=Path("specs"))
                if specifications_enabled
                else None
            ),
        ),
        specifications=SpecWeaveSpecifications() if specifications_enabled else None,
        test_command=_default_test_command(
            spelling,
            include_behaviour=True,
            include_specifications=specifications_enabled,
        ),
    )


def _resolve_paths(paths: SpecWeavePaths, project_root: Path) -> SpecWeavePaths:
    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else (project_root / path).resolve()

    behaviour = SpecWeaveBehaviourPaths(
        root=resolve(paths.behaviour.root),
        features_dir=resolve(paths.behaviour.features_dir),
        readme=resolve(paths.behaviour.readme),
        manifest=resolve(paths.behaviour.manifest),
        mappings_dir=resolve(paths.behaviour.mappings_dir),
        evidence_dir=resolve(paths.behaviour.evidence_dir),
        reports_dir=resolve(paths.behaviour.reports_dir),
        reports_state_dir=resolve(paths.behaviour.reports_state_dir),
    )
    specifications = None
    if paths.specifications is not None:
        specifications = SpecWeaveSpecificationPaths(
            root=resolve(paths.specifications.root),
            product_spec=resolve(paths.specifications.product_spec),
            readme=resolve(paths.specifications.readme),
            manifest=resolve(paths.specifications.manifest),
            capabilities_dir=resolve(paths.specifications.capabilities_dir),
            interfaces_dir=resolve(paths.specifications.interfaces_dir),
            integrations_dir=resolve(paths.specifications.integrations_dir),
            mappings_dir=resolve(paths.specifications.mappings_dir),
            evidence_dir=resolve(paths.specifications.evidence_dir),
            reports_dir=resolve(paths.specifications.reports_dir),
            reports_state_dir=resolve(paths.specifications.reports_state_dir),
        )
    return SpecWeavePaths(
        specs_root=resolve(paths.specs_root),
        tests_dir=resolve(paths.tests_dir),
        behaviour=behaviour,
        specifications=specifications,
    )


def _build_paths(
    spelling: str,
    data: dict,
    *,
    enable_specifications: bool = False,
) -> SpecWeavePaths:
    raw_specs_root = Path(data.get("specs_root", "specs"))
    legacy_behaviour_root = (
        raw_specs_root if raw_specs_root.name in {"behavior", "behaviour"} else None
    )
    specs_root = (
        legacy_behaviour_root.parent if legacy_behaviour_root else raw_specs_root
    )

    behaviour_data = data.get("behaviour")
    if isinstance(behaviour_data, dict):
        root = Path(
            behaviour_data.get(
                "root",
                _default_behaviour_paths(specs_root=specs_root, spelling=spelling).root,
            )
        )
        default_reports_dir = root / "reports"
        behaviour = SpecWeaveBehaviourPaths(
            root=root,
            features_dir=Path(behaviour_data.get("features_dir", root / "features")),
            readme=Path(behaviour_data.get("readme", root / "README.md")),
            manifest=Path(behaviour_data.get("manifest", root / "manifest.json")),
            mappings_dir=Path(behaviour_data.get("mappings_dir", root / "mappings")),
            evidence_dir=Path(behaviour_data.get("evidence_dir", root / "evidence")),
            reports_dir=Path(behaviour_data.get("reports_dir", default_reports_dir)),
            reports_state_dir=Path(
                behaviour_data.get(
                    "reports_state_dir",
                    default_reports_dir / "specweave",
                )
            ),
        )
    else:
        behaviour = _build_behaviour_from_legacy(
            specs_root=legacy_behaviour_root or specs_root,
            features_dir=_optional_path(data.get("features_dir")),
            behavior_readme=_optional_path(data.get("behavior_readme")),
            manifest=_optional_path(data.get("manifest")),
            reports_dir=_optional_path(data.get("reports_dir")),
            evidence_dir=_optional_path(data.get("evidence_dir")),
            reports_state_dir=_optional_path(data.get("reports_state_dir")),
            mapping_dir=_optional_path(data.get("mapping_dir")),
        )

    specifications = None
    specifications_data = data.get("specifications")
    if enable_specifications or isinstance(specifications_data, dict):
        specs_data = (
            specifications_data if isinstance(specifications_data, dict) else {}
        )
        root = Path(
            specs_data.get(
                "root", _default_specification_paths(specs_root=specs_root).root
            )
        )
        reports_dir = root / "reports"
        specifications = SpecWeaveSpecificationPaths(
            root=root,
            product_spec=Path(specs_data.get("product_spec", root / "product.spec.md")),
            readme=Path(specs_data.get("readme", root / "README.md")),
            manifest=Path(specs_data.get("manifest", root / "manifest.json")),
            capabilities_dir=Path(
                specs_data.get("capabilities_dir", root / "capabilities")
            ),
            interfaces_dir=Path(specs_data.get("interfaces_dir", root / "interfaces")),
            integrations_dir=Path(
                specs_data.get("integrations_dir", root / "integrations")
            ),
            mappings_dir=Path(specs_data.get("mappings_dir", root / "mappings")),
            evidence_dir=Path(specs_data.get("evidence_dir", root / "evidence")),
            reports_dir=Path(specs_data.get("reports_dir", reports_dir)),
            reports_state_dir=Path(
                specs_data.get(
                    "reports_state_dir",
                    reports_dir / "specweave",
                )
            ),
        )

    return SpecWeavePaths(
        specs_root=specs_root,
        tests_dir=Path(data.get("tests_dir", "tests")),
        behaviour=behaviour,
        specifications=specifications,
    )


def _optional_path(value: object) -> Path | None:
    if isinstance(value, str):
        return Path(value)
    return None


def _build_pytest(data: dict) -> SpecWeavePytest:
    return SpecWeavePytest(
        test_globs=tuple(data.get("test_globs", SpecWeavePytest().test_globs)),
        ignore_globs=tuple(data.get("ignore_globs", SpecWeavePytest().ignore_globs)),
    )


def _build_gherkin(data: dict) -> SpecWeaveGherkin:
    defaults = SpecWeaveGherkin()
    return SpecWeaveGherkin(
        dialect=data.get("dialect", defaults.dialect),
        official_parser=data.get("official_parser", defaults.official_parser),
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


def _build_behaviour(data: dict, gherkin: SpecWeaveGherkin) -> SpecWeaveBehaviour:
    return SpecWeaveBehaviour(
        require_bdd_ids=data.get("require_bdd_ids", gherkin.require_bdd_ids),
        default_scenario_keyword=data.get(
            "default_scenario_keyword",
            gherkin.default_scenario_keyword,
        ),
        generated_tag=data.get("generated_tag", "generated"),
        needs_review_tag=data.get("needs_review_tag", "needs-review"),
    )


def _build_specifications(data: dict | None) -> SpecWeaveSpecifications:
    payload = data or {}
    defaults = SpecWeaveSpecifications()
    return SpecWeaveSpecifications(
        require_requirement_ids=payload.get(
            "require_requirement_ids",
            defaults.require_requirement_ids,
        ),
        allowed_requirement_prefixes=tuple(
            payload.get(
                "allowed_requirement_prefixes",
                defaults.allowed_requirement_prefixes,
            )
        ),
        require_verification=payload.get(
            "require_verification",
            defaults.require_verification,
        ),
        require_rationale=payload.get(
            "require_rationale",
            defaults.require_rationale,
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


def _default_test_command(
    spelling: str,
    *,
    include_behaviour: bool,
    include_specifications: bool = False,
) -> str:
    if include_behaviour:
        return f"pytest --junitxml=specs/{spelling}/reports/pytest-junit.xml"
    if include_specifications:
        return "pytest --junitxml=specs/specifications/reports/pytest-junit.xml"
    return "pytest --junitxml=reports/pytest-junit.xml"


def render_default_config(
    *, spelling: str = "behaviour", mode: str = "behaviour"
) -> str:
    """Render the default TOML config as a deterministic string."""
    normalized_mode = {"behavior": "behaviour"}.get(mode, mode)
    include_behaviour = normalized_mode in {"behaviour", "both"}
    include_specifications = normalized_mode in {"specifications", "both"}
    behaviour_root = f"specs/{spelling}"
    default_test_command = _default_test_command(
        spelling,
        include_behaviour=include_behaviour,
        include_specifications=include_specifications,
    )

    sections = [
        "schema_version = 1",
        'project_root = "."',
        f'spelling = "{spelling}"',
        "",
        "[paths]",
        'specs_root = "specs"',
        'tests_dir = "tests"',
    ]
    if include_behaviour:
        sections.extend(
            [
                "",
                "[paths.behaviour]",
                f'root = "{behaviour_root}"',
                f'features_dir = "{behaviour_root}/features"',
                f'readme = "{behaviour_root}/README.md"',
                f'manifest = "{behaviour_root}/manifest.json"',
                f'mappings_dir = "{behaviour_root}/mappings"',
                f'evidence_dir = "{behaviour_root}/evidence"',
                f'reports_dir = "{behaviour_root}/reports"',
                f'reports_state_dir = "{behaviour_root}/reports/specweave"',
                "",
                "[behaviour]",
                "require_bdd_ids = true",
                'default_scenario_keyword = "Example"',
                'generated_tag = "generated"',
                'needs_review_tag = "needs-review"',
            ]
        )
    if include_specifications:
        sections.extend(
            [
                "",
                "[paths.specifications]",
                'root = "specs/specifications"',
                'product_spec = "specs/specifications/product.spec.md"',
                'readme = "specs/specifications/README.md"',
                'manifest = "specs/specifications/manifest.json"',
                'capabilities_dir = "specs/specifications/capabilities"',
                'interfaces_dir = "specs/specifications/interfaces"',
                'integrations_dir = "specs/specifications/integrations"',
                'mappings_dir = "specs/specifications/mappings"',
                'evidence_dir = "specs/specifications/evidence"',
                'reports_dir = "specs/specifications/reports"',
                'reports_state_dir = "specs/specifications/reports/specweave"',
                "",
                "[specifications]",
                "require_requirement_ids = true",
                "allowed_requirement_prefixes = ["
                '"REQ", "INV", "IF", "DATA", "NFR", '
                '"NGOAL", "RISK", "OPEN"]',
                "require_verification = true",
                "require_rationale = false",
            ]
        )

    sections.extend(
        [
            "",
            "gitkeep = true",
            "",
            "[pytest]",
            'test_globs = ["tests/test_*.py", "tests/**/*_test.py"]',
            'ignore_globs = [".venv/**", "build/**", "dist/**"]',
            "",
            "[gherkin]",
            'dialect = "en"',
            "official_parser = false",
            "compile_pickles = false",
            'default_scenario_keyword = "Example"',
            "require_given_when_then = true",
            "require_bdd_ids = true",
            'id_style = "slug"',
            "include_generated_tag = true",
            "include_needs_review_tag = true",
            "canonical_task_tags = false",
            "",
            "[generation]",
            'group_by = "file"',
            'mode = "create"',
            "preserve_manual_edits = true",
            "mark_generated_from_tests = true",
            "",
            "[commands]",
            f'test = "{default_test_command}"',
            "",
            "[agent]",
            "json_default = false",
            "",
        ]
    )
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Backward-compatible constants (existing code uses these)
# ---------------------------------------------------------------------------

REPORT_DIR = Path("specs/behaviour/reports/specweave")
# Default directory for runner summary reports.

BEHAVIOR_FEATURES_DIR = Path("specs/behaviour/features")
BEHAVIOR_INDEX_PATH = Path("specs/behaviour/README.md")
BEHAVIOR_MANIFEST_PATH = Path("specs/behaviour/manifest.json")
PYTEST_TESTS_DIR = Path("tests")
BEHAVIOR_REPORTS_DIR = Path("specs/behaviour/reports")
SPECWEAVE_REPORTS_DIR = REPORT_DIR
SPECWEAVE_EVIDENCE_DIR = Path("specs/behaviour/evidence")
SPECWEAVE_MAPPING_DIR = Path("specs/behaviour/mappings")

# Compatibility aliases retained for older code paths.
FEATURES_DIR = BEHAVIOR_FEATURES_DIR
BDD_INDEX_PATH = BEHAVIOR_INDEX_PATH
BDD_MANIFEST_PATH = BEHAVIOR_MANIFEST_PATH
BDD_TESTS_DIR = PYTEST_TESTS_DIR
BDD_REPORTS_DIR = BEHAVIOR_REPORTS_DIR
