"""Autolink generated behavior scenarios to plain pytest tests."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

from specweave.behavior.common import (
    display_path,
    iter_feature_scenarios,
    scenario_identifier,
    slugify,
)
from specweave.behavior.generate import _keyword_string_arg_lines
from specweave.gherkin.lint import collect_feature_files
from specweave.gherkin.parser import parse_feature
from specweave.python_inspect.ast_reader import (
    PytestTestItem,
    collect_pytest_tests,
    collect_specweave_tests,
)


@dataclass(frozen=True)
class AutolinkItem:
    feature: str
    scenario: str
    test_file: str
    nodeid: str
    function_name: str
    line: int
    status: str
    reason: str
    confidence: str


@dataclass(frozen=True)
class AutolinkResult:
    schema_version: int
    command: str
    strategy: str
    apply: bool
    summary: dict[str, int]
    items: tuple[AutolinkItem, ...]
    ambiguous: tuple[AutolinkItem, ...]
    unmatched: tuple[AutolinkItem, ...]


def autolink_result_to_dict(result: AutolinkResult) -> dict[str, object]:
    return {
        "schema_version": result.schema_version,
        "command": result.command,
        "strategy": result.strategy,
        "apply": result.apply,
        "summary": result.summary,
        "items": [asdict(item) for item in result.items],
        "ambiguous": [asdict(item) for item in result.ambiguous],
        "unmatched": [asdict(item) for item in result.unmatched],
    }


def autolink_generated_ids(
    *,
    features: Path,
    tests: Path,
    apply: bool = False,
    allow_non_generated: bool = False,
    rewrite_duplicates: bool = False,
) -> AutolinkResult:
    plan = build_autolink_plan(
        features=features,
        tests=tests,
        allow_non_generated=allow_non_generated,
        rewrite_duplicates=rewrite_duplicates,
    )
    if not apply:
        return plan
    written, files_changed = apply_autolink_plan(plan, tests=tests)
    summary = dict(plan.summary)
    summary["written"] = written
    summary["files_changed"] = files_changed
    return AutolinkResult(
        schema_version=plan.schema_version,
        command=plan.command,
        strategy=plan.strategy,
        apply=True,
        summary=summary,
        items=plan.items,
        ambiguous=plan.ambiguous,
        unmatched=plan.unmatched,
    )


def build_autolink_plan(
    *,
    features: Path,
    tests: Path,
    allow_non_generated: bool = False,
    rewrite_duplicates: bool = False,
) -> AutolinkResult:
    feature_paths = (
        collect_feature_files((features,)) if features.is_dir() else [features]
    )
    test_paths = sorted(tests.rglob("test_*.py")) if tests.is_dir() else [tests]
    pytest_items = collect_pytest_tests(test_paths)
    existing = {
        (mapping.test_file, mapping.nodeid, mapping.function_name)
        for mapping in collect_specweave_tests(test_paths)
    }
    existing_by_function = {
        (mapping.test_file, mapping.function_name)
        for mapping in collect_specweave_tests(test_paths)
    }

    scenarios = _generated_scenarios(feature_paths, features, allow_non_generated)
    tests_by_name: dict[str, list[PytestTestItem]] = defaultdict(list)
    for item in pytest_items:
        tests_by_name[item.function_name].append(item)

    planned: list[AutolinkItem] = []
    ambiguous: list[AutolinkItem] = []
    unmatched: list[AutolinkItem] = []
    skipped_existing = 0

    for scenario in scenarios:
        function_name = scenario["function_name"]
        candidates = tests_by_name.get(function_name, [])
        if not candidates:
            unmatched.append(
                _item_from_scenario(
                    scenario,
                    None,
                    "unmatched",
                    "No pytest test function matched generated id.",
                    "no-candidate",
                )
            )
            continue
        available = [
            candidate
            for candidate in candidates
            if (candidate.test_file, candidate.nodeid, candidate.function_name)
            not in existing
            and (candidate.test_file, candidate.function_name)
            not in existing_by_function
        ]
        if not available:
            skipped_existing += 1
            continue
        scored = sorted(
            (
                (_score_candidate(scenario, candidate), candidate)
                for candidate in available
            ),
            key=lambda value: value[0],
            reverse=True,
        )
        if len(scored) == 1:
            planned.append(
                _item_from_scenario(
                    scenario,
                    scored[0][1],
                    "planned",
                    "Unique pytest function name match.",
                    "exact-function-name",
                )
            )
            continue
        if scored[0][0] > scored[1][0]:
            planned.append(
                _item_from_scenario(
                    scenario,
                    scored[0][1],
                    "planned",
                    "Unique highest-scored file match.",
                    "scored-unique-file",
                )
            )
            continue
        if rewrite_duplicates:
            ordered = sorted(available, key=lambda item: (item.test_file, item.line))
            planned.append(
                _item_from_scenario(
                    scenario,
                    ordered[0],
                    "planned",
                    "Duplicate occurrence rewrite enabled.",
                    "nth-duplicate",
                )
            )
            continue
        ambiguous.append(
            _item_from_scenario(
                scenario,
                scored[0][1],
                "ambiguous",
                "Multiple pytest candidates have equal score.",
                "ambiguous",
            )
        )

    summary = {
        "planned": len(planned),
        "written": 0,
        "skipped_existing": skipped_existing,
        "ambiguous": len(ambiguous),
        "unmatched": len(unmatched),
        "files_changed": 0,
    }
    return AutolinkResult(
        schema_version=1,
        command="behavior autolink",
        strategy="generated-id",
        apply=False,
        summary=summary,
        items=tuple(planned),
        ambiguous=tuple(ambiguous),
        unmatched=tuple(unmatched),
    )


def apply_autolink_plan(result: AutolinkResult, *, tests: Path) -> tuple[int, int]:
    writable = [item for item in result.items if item.status == "planned"]
    by_file: dict[str, list[AutolinkItem]] = defaultdict(list)
    for item in writable:
        by_file[item.test_file].append(item)

    files_changed = 0
    written = 0
    for test_file, items in by_file.items():
        path = Path(test_file)
        if not path.exists() and tests.is_dir():
            path = tests / Path(test_file).name
        source = path.read_text(encoding="utf-8")
        test_items = {item.nodeid: item for item in collect_pytest_tests((path,))}
        lines = source.splitlines()
        for item in sorted(
            items,
            key=lambda current: test_items[current.nodeid].insert_line,
            reverse=True,
        ):
            test_item = test_items[item.nodeid]
            insert_at = test_item.insert_line - 1
            mapping_lines = _decorator_lines(
                item.feature, item.scenario, test_item.indent
            )
            lines[insert_at:insert_at] = mapping_lines
            written += 1
        new_source = "\n".join(lines).rstrip() + "\n"
        new_source = _ensure_pytest_import(new_source)
        if new_source != source:
            path.write_text(new_source, encoding="utf-8")
            files_changed += 1
    return written, files_changed


def render_autolink_text(result: AutolinkResult) -> str:
    mode = "apply" if result.apply else "dry-run"
    summary = result.summary
    lines = [
        f"SpecWeave behavior autolink: {mode}",
        "planned: {planned}, written: {written}, existing: {skipped_existing}, "
        "ambiguous: {ambiguous}, unmatched: {unmatched}".format(**summary),
    ]
    for item in result.items[:20]:
        lines.append(f"+ {item.nodeid}")
        lines.append(f"  -> {item.feature} {item.scenario}")
    if len(result.items) > 20:
        lines.append(f"... {len(result.items) - 20} more planned mappings")
    return "\n".join(lines)


def _generated_scenarios(
    feature_paths: Iterable[Path], features_root: Path, allow_non_generated: bool
) -> list[dict[str, str]]:
    scenarios: list[dict[str, str]] = []
    for feature_path in feature_paths:
        feature = parse_feature(
            feature_path.read_text(encoding="utf-8"), source_path=feature_path
        )
        feature_ref = display_path(feature_path)
        area = _feature_area(feature_path, features_root)
        for _, scenario in iter_feature_scenarios(feature):
            scenario_ref = scenario_identifier(scenario)
            function_name = _function_name_from_generated_id(scenario_ref, area)
            if function_name is None:
                if not allow_non_generated:
                    continue
                function_name = (
                    f"test_{scenario_ref.removeprefix('@bdd-').replace('-', '_')}"
                )
            scenarios.append(
                {
                    "feature": feature_ref,
                    "scenario": scenario_ref,
                    "function_name": function_name,
                    "feature_stem": feature_path.stem.replace("-", "_"),
                    "area": area,
                }
            )
    return scenarios


def _feature_area(feature_path: Path, features_root: Path) -> str:
    try:
        relative = feature_path.relative_to(features_root)
    except ValueError:
        return slugify(feature_path.parent.name)
    if relative.parent == Path("."):
        return "behavior"
    return slugify(relative.parent.parts[0])


def _function_name_from_generated_id(scenario_ref: str, area: str) -> str | None:
    if not scenario_ref.startswith("@bdd-"):
        return None
    value = scenario_ref.removeprefix("@bdd-")
    prefix = f"{area}-"
    if not value.startswith(prefix):
        return None
    return f"test_{value.removeprefix(prefix).replace('-', '_')}"


def _score_candidate(scenario: dict[str, str], candidate: PytestTestItem) -> int:
    stem = Path(candidate.test_file).stem.replace("-", "_")
    score = 0
    if scenario["area"].replace("-", "_") in stem:
        score += 2
    if scenario["feature_stem"] in stem:
        score += 3
    return score


def _item_from_scenario(
    scenario: dict[str, str],
    candidate: PytestTestItem | None,
    status: str,
    reason: str,
    confidence: str,
) -> AutolinkItem:
    return AutolinkItem(
        feature=scenario["feature"],
        scenario=scenario["scenario"],
        test_file=candidate.test_file if candidate else "",
        nodeid=candidate.nodeid if candidate else "",
        function_name=scenario["function_name"],
        line=candidate.line if candidate else 0,
        status=status,
        reason=reason,
        confidence=confidence,
    )


def _decorator_lines(feature: str, scenario: str, indent: str) -> list[str]:
    return [
        f"{indent}@pytest.mark.specweave(",
        *_keyword_string_arg_lines("feature", feature, indent=f"{indent}    "),
        *_keyword_string_arg_lines("scenario", scenario, indent=f"{indent}    "),
        f"{indent})",
    ]


def _ensure_pytest_import(source: str) -> str:
    if "import pytest" in source:
        return source
    lines = source.splitlines()
    insert_at = 0
    while insert_at < len(lines) and (
        lines[insert_at].startswith('"""')
        or lines[insert_at].startswith("from __future__")
        or not lines[insert_at].strip()
    ):
        insert_at += 1
    lines[insert_at:insert_at] = ["import pytest", ""]
    return "\n".join(lines).rstrip() + "\n"
