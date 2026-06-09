"""Lint canonical SpecWeave behavior feature files."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

from specweave.config import BEHAVIOR_FEATURES_DIR
from specweave.gherkin.model import Feature, Scenario
from specweave.gherkin.parser import parse_feature

_UNSUPPORTED_PREFIXES = (
    "Background:",
    "Scenario Outline:",
    "Scenario Template:",
    "Examples:",
)
_DEPRECATED_PATH_SEGMENTS = (
    "specs/bdd/features",
    "tests/bdd/features",
    "tests/behavior/features",
)


@dataclass(frozen=True)
class LintFinding:
    """A single behavior lint result."""

    code: str
    level: str
    path: str
    message: str
    line: int | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _feature_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        return []
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file() and candidate.suffix == ".feature"
    )


def collect_feature_files(paths: Iterable[Path]) -> list[Path]:
    """Collect feature files from one or more files/directories."""

    files: list[Path] = []
    for path in paths:
        files.extend(_feature_files(path))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def default_feature_files() -> list[Path]:
    """Return canonical feature files under the default features directory."""

    return collect_feature_files((BEHAVIOR_FEATURES_DIR,))


def _feature_display_path(path: Path) -> str:
    return _display_path(path).replace("\\", "/")


def _canonical_root(path: Path) -> bool:
    return _feature_display_path(path).startswith("specs/behavior/features/")


def _is_deprecated_path(path: Path) -> bool:
    display = _feature_display_path(path)
    return any(segment in display for segment in _DEPRECATED_PATH_SEGMENTS)


def _feature_path_findings(path: Path) -> list[LintFinding]:
    display = _feature_display_path(path)
    findings: list[LintFinding] = []
    if "specs/bdd/features" in display:
        findings.append(
            LintFinding(
                code="SWBEH015",
                level="warning",
                path=display,
                message=(
                    "Deprecated feature path under specs/bdd/features; "
                    "use specs/behavior/features instead."
                ),
            )
        )
        return findings
    if any(
        segment in display
        for segment in ("tests/bdd/features", "tests/behavior/features")
    ):
        findings.append(
            LintFinding(
                code="SWBEH012",
                level="warning",
                path=display,
                message=(
                    "Deprecated feature path under tests/bdd/features or "
                    "tests/behavior/features."
                ),
            )
        )
        return findings
    if not _canonical_root(path):
        findings.append(
            LintFinding(
                code="SWBEH009",
                level="error",
                path=display,
                message=(
                    "Canonical behavior feature must live under "
                    "specs/behavior/features."
                ),
            )
        )
        return findings

    relative = Path(display).relative_to(BEHAVIOR_FEATURES_DIR)
    if len(relative.parts) != 2:
        findings.append(
            LintFinding(
                code="SWBEH010",
                level="warning",
                path=display,
                message=(
                    "Canonical feature path should match "
                    "specs/behavior/features/<area>/<feature>.feature."
                ),
            )
        )
    if path.stem.startswith("task-"):
        findings.append(
            LintFinding(
                code="SWBEH011",
                level="warning",
                path=display,
                message="Canonical feature filename should not start with task-.",
            )
        )
    return findings


def _unsupported_findings(path: Path, text: str, *, strict: bool) -> list[LintFinding]:
    if not strict:
        return []
    findings: list[LintFinding] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if (
            stripped.startswith(_UNSUPPORTED_PREFIXES)
            or stripped.startswith("|")
            or stripped.startswith('"""')
        ):
            findings.append(
                LintFinding(
                    code="SWBEH008",
                    level="error",
                    path=_feature_display_path(path),
                    line=line_no,
                    message=f"Unsupported construct ignored by parser: {stripped}",
                )
            )
    return findings


def _first_meaningful_line(text: str) -> tuple[int, str] | None:
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped:
            return line_no, stripped
    return None


def _unsupported_markdown_findings(path: Path) -> list[LintFinding]:
    if not str(path).endswith(".feature.md"):
        return []
    return [
        LintFinding(
            code="SWBEH016",
            level="error",
            path=_feature_display_path(path),
            message=(
                "Markdown .feature.md files are no longer supported; "
                "convert to classic .feature."
            ),
        )
    ]


def _scenario_findings(
    path: Path, feature: Feature, *, require_scenario_ids: bool
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for scenario in iter_feature_scenarios(feature):
        if not scenario.title.strip():
            findings.append(
                LintFinding(
                    code="SWBEH004",
                    level="error",
                    path=_feature_display_path(path),
                    line=scenario.line,
                    message="Scenario/Example title must be non-empty.",
                )
            )
        keywords = {step.keyword for step in scenario.steps}
        if not {"Given", "When", "Then"}.issubset(keywords):
            findings.append(
                LintFinding(
                    code="SWBEH005",
                    level="error",
                    path=_feature_display_path(path),
                    line=scenario.line,
                    message=(
                        "Scenario/Example should contain at least one Given, "
                        "one When, and one Then."
                    ),
                )
            )
        if require_scenario_ids and not any(
            tag.startswith("bdd-") for tag in scenario.tags
        ):
            findings.append(
                LintFinding(
                    code="SWBEH014",
                    level="warning",
                    path=_feature_display_path(path),
                    line=scenario.line,
                    message="Scenario lacks a stable @bdd-* tag for coverage/indexing.",
                )
            )
        for tag in scenario.tags:
            if tag.startswith("task-") or tag.startswith("taskledger:"):
                findings.append(
                    LintFinding(
                        code="SWBEH013",
                        level="warning",
                        path=_feature_display_path(path),
                        line=scenario.line,
                        message=(
                            "Task-specific tags are discouraged in canonical "
                            "behavior specs."
                        ),
                    )
                )
                break
    return findings


def iter_feature_scenarios(feature: Feature) -> Iterable[Scenario]:
    """Yield all scenarios/examples in *feature*."""

    yield from feature.scenarios
    for rule in feature.rules:
        yield from rule.scenarios


def lint_feature_files(
    paths: Iterable[Path], *, strict: bool = False, require_scenario_ids: bool = False
) -> list[LintFinding]:
    """Lint one or more feature paths."""

    findings: list[LintFinding] = []
    parsed: dict[Path, Feature] = {}
    bdd_tags: dict[str, list[tuple[Path, int | None]]] = defaultdict(list)

    for path in collect_feature_files(paths):
        display = _feature_display_path(path)
        findings.extend(_unsupported_markdown_findings(path))
        if str(path).endswith(".feature.md"):
            continue
        text = path.read_text(encoding="utf-8")
        findings.extend(_feature_path_findings(path))
        feature_count = sum(
            1
            for line in text.splitlines()
            if line.strip().startswith("Feature:")
            or line.strip().startswith("# Feature:")
        )
        if feature_count != 1:
            findings.append(
                LintFinding(
                    code="SWBEH002",
                    level="error",
                    path=display,
                    message="Feature file must contain exactly one Feature.",
                )
            )
        findings.extend(_unsupported_findings(path, text, strict=strict))
        try:
            feature = parse_feature(text, source_path=path)
        except ValueError as exc:
            findings.append(
                LintFinding(
                    code="SWBEH001",
                    level="error",
                    path=display,
                    message=str(exc),
                )
            )
            continue
        parsed[path] = feature
        if not feature.title.strip():
            findings.append(
                LintFinding(
                    code="SWBEH003",
                    level="error",
                    path=display,
                    line=feature.line,
                    message="Feature title must be non-empty.",
                )
            )
        for rule in feature.rules:
            if not rule.scenarios:
                findings.append(
                    LintFinding(
                        code="SWBEH006",
                        level="error",
                        path=display,
                        line=rule.line,
                        message="Rule should contain at least one scenario/example.",
                    )
                )
            for tag in rule.tags:
                if tag.startswith("task-") or tag.startswith("taskledger:"):
                    findings.append(
                        LintFinding(
                            code="SWBEH013",
                            level="warning",
                            path=display,
                            line=rule.line,
                            message=(
                                "Task-specific tags are discouraged in canonical "
                                "behavior specs."
                            ),
                        )
                    )
                    break
        for tag in feature.tags:
            if tag.startswith("task-") or tag.startswith("taskledger:"):
                findings.append(
                    LintFinding(
                        code="SWBEH013",
                        level="warning",
                        path=display,
                        line=feature.line,
                        message=(
                            "Task-specific tags are discouraged in canonical "
                            "behavior specs."
                        ),
                    )
                )
                break
        findings.extend(
            _scenario_findings(path, feature, require_scenario_ids=require_scenario_ids)
        )
        for scenario in iter_feature_scenarios(feature):
            for tag in scenario.tags:
                if tag.startswith("bdd-"):
                    bdd_tags[tag].append((path, scenario.line))

    for tag, locations in sorted(bdd_tags.items()):
        if len(locations) < 2:
            continue
        for path, line in locations:
            findings.append(
                LintFinding(
                    code="SWBEH007",
                    level="error",
                    path=_feature_display_path(path),
                    line=line,
                    message=f"Duplicate scenario tag @{tag} within repository.",
                )
            )

    return sorted(findings, key=lambda item: (item.path, item.line or 0, item.code))
