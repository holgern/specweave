"""Static coverage checks between specification requirements and plain pytest tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from specweave.behavior.common import display_path
from specweave.python_inspect.ast_reader import (
    PytestTestItem,
    SpecweaveTestMapping,
    collect_pytest_tests,
    collect_specweave_tests,
    is_specification_mapping,
)
from specweave.specifications.parser import (
    collect_specification_files,
    parse_specification,
)

_VIEW_VALUES = frozenset({"requirement", "test", "both"})
_SHOW_VALUES = frozenset(
    {"all", "gaps", "bound", "missing", "unmapped", "stale", "waived", "duplicate"}
)


def _test_files(tests_dir: Path) -> list[Path]:
    return sorted(
        candidate for candidate in tests_dir.rglob("*.py") if candidate.is_file()
    )


def _resolve_project_relative(path_text: str, reference_path: Path) -> Path:
    candidate = Path(path_text)
    if candidate.exists():
        return candidate
    if candidate.is_absolute():
        return candidate
    for ancestor in (reference_path.parent, *reference_path.parents):
        resolved = ancestor / candidate
        if resolved.exists():
            return resolved
    return candidate


def _normalize_nodeid(nodeid: str) -> str:
    if "::" not in nodeid:
        return nodeid
    file_part, remainder = nodeid.split("::", 1)
    return f"{display_path(Path(file_part))}::{remainder}"


def _mapping_sort_key(mapping: SpecweaveTestMapping) -> tuple[str, str, str, int]:
    return (
        mapping.spec or "",
        mapping.requirement or "",
        mapping.test_file,
        mapping.line,
    )


def _mapping_lookup(
    mappings: list[SpecweaveTestMapping],
) -> tuple[
    dict[tuple[str, str], list[SpecweaveTestMapping]],
    dict[str, list[SpecweaveTestMapping]],
]:
    by_key: dict[tuple[str, str], list[SpecweaveTestMapping]] = {}
    by_nodeid: dict[str, list[SpecweaveTestMapping]] = {}
    for mapping in mappings:
        if mapping.spec is None or mapping.requirement is None:
            continue
        by_key.setdefault((mapping.spec, mapping.requirement), []).append(mapping)
        by_nodeid.setdefault(_normalize_nodeid(mapping.nodeid), []).append(mapping)
    return by_key, by_nodeid


def _declared_requirement_mappings(root: Path) -> list[SpecweaveTestMapping]:
    mappings: list[SpecweaveTestMapping] = []
    for path in collect_specification_files([root]):
        document = parse_specification(path)
        spec_ref = display_path(path)
        for requirement in document.requirements:
            for ref in requirement.verification_refs:
                if ref.kind != "pytest":
                    continue
                nodeid = ref.target.strip()
                if not nodeid:
                    continue
                file_part, _, remainder = nodeid.partition("::")
                resolved_file = _resolve_project_relative(file_part, path)
                normalized_nodeid = (
                    f"{display_path(resolved_file)}::{remainder}"
                    if remainder
                    else display_path(resolved_file)
                )
                mappings.append(
                    SpecweaveTestMapping(
                        function_name=remainder or nodeid.split("::")[-1],
                        test_file=display_path(resolved_file),
                        nodeid=normalized_nodeid,
                        line=requirement.line,
                        source="specification",
                        spec=spec_ref,
                        requirement=requirement.id,
                    )
                )
    return mappings


def _intentional_unmapped_path(root: Path, mapping_dir: Path | None) -> Path:
    if mapping_dir is not None:
        return mapping_dir / "intentional-unmapped.json"
    return root / "mappings" / "intentional-unmapped.json"


def _load_intentional_unmapped(
    path: Path,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    if not path.exists():
        return {}, {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    tests_raw = raw.get("tests", []) if isinstance(raw, dict) else []
    requirements_raw = raw.get("requirements", []) if isinstance(raw, dict) else []
    test_waivers: dict[str, dict[str, str]] = {}
    requirement_waivers: dict[str, dict[str, str]] = {}
    for item in tests_raw:
        if not isinstance(item, dict):
            continue
        nodeid = str(item.get("nodeid") or "").strip()
        if not nodeid:
            continue
        test_waivers[_normalize_nodeid(nodeid)] = {
            "reason": str(item.get("reason") or "intentional-unmapped").strip()
            or "intentional-unmapped",
            "source": display_path(path),
        }
    for item in requirements_raw:
        if not isinstance(item, dict):
            continue
        requirement_id = str(item.get("id") or "").strip()
        if not requirement_id:
            continue
        requirement_waivers[requirement_id] = {
            "reason": str(item.get("reason") or "intentional-unmapped").strip()
            or "intentional-unmapped",
            "source": display_path(path),
        }
    return test_waivers, requirement_waivers


def _mapping_item(mapping: SpecweaveTestMapping) -> dict[str, Any]:
    return {
        "test_file": mapping.test_file,
        "nodeid": _normalize_nodeid(mapping.nodeid),
        "function_name": mapping.function_name,
        "line": mapping.line,
        "source": mapping.source,
    }


def _mapping_target(mapping: SpecweaveTestMapping) -> dict[str, Any]:
    return {
        "spec": mapping.spec,
        "requirement": mapping.requirement,
        "source": mapping.source,
    }


def _mapping_valid(
    mapping: SpecweaveTestMapping,
    expected_requirements: dict[tuple[str, str], dict[str, Any]],
) -> bool:
    if mapping.spec is None or mapping.requirement is None:
        return False
    return (mapping.spec, mapping.requirement) in expected_requirements


def _test_inventory(
    test_items: list[PytestTestItem],
    mappings: list[SpecweaveTestMapping],
    expected_requirements: dict[tuple[str, str], dict[str, Any]],
    intentional_unmapped: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    _, mappings_by_nodeid = _mapping_lookup(mappings)
    grouped: dict[str, list[dict[str, Any]]] = {}
    unmapped_tests: list[dict[str, Any]] = []

    for test_item in test_items:
        nodeid = _normalize_nodeid(test_item.nodeid)
        linked = sorted(mappings_by_nodeid.get(nodeid, []), key=_mapping_sort_key)
        valid = [
            mapping
            for mapping in linked
            if _mapping_valid(mapping, expected_requirements)
        ]
        primary_mapping = valid[0] if valid else (linked[0] if linked else None)
        waiver = (
            {
                "reason": test_item.unmapped_reason,
                "source": test_item.unmapped_source or "comment",
            }
            if test_item.unmapped_reason
            else intentional_unmapped.get(nodeid)
        )
        if not linked and waiver:
            status = "waived"
        elif not linked:
            status = "unmapped"
        elif valid:
            status = "mapped"
        else:
            status = "stale"

        entry = {
            "nodeid": nodeid,
            "function_name": test_item.function_name,
            "line": test_item.line,
            "status": status,
            "mapping": (
                None if primary_mapping is None else _mapping_target(primary_mapping)
            ),
            "waiver": waiver,
            "test_file": test_item.test_file,
        }
        grouped.setdefault(test_item.test_file, []).append(entry)
        if status == "unmapped":
            unmapped_tests.append(entry.copy())

    tests: list[dict[str, Any]] = []
    for test_file, items in sorted(grouped.items()):
        mapped = sum(1 for item in items if item["status"] == "mapped")
        unmapped = sum(1 for item in items if item["status"] == "unmapped")
        stale = sum(1 for item in items if item["status"] == "stale")
        waived = sum(1 for item in items if item["status"] == "waived")
        if mapped == len(items):
            status = "mapped"
        elif unmapped == len(items):
            status = "unmapped"
        elif stale == len(items):
            status = "stale"
        elif waived == len(items):
            status = "waived"
        else:
            status = "mixed"
        tests.append(
            {
                "test_file": test_file,
                "status": status,
                "tests_total": len(items),
                "mapped": mapped,
                "unmapped": unmapped,
                "stale": stale,
                "waived": waived,
                "items": items,
            }
        )
    return tests, sorted(
        unmapped_tests, key=lambda item: (item["test_file"], item["line"])
    )


def build_specification_coverage(
    *,
    root: Path,
    tests_dir: Path,
    mapping_dir: Path | None = None,
) -> dict[str, Any]:
    """Build the coverage report for specifications and pytest tests."""
    spec_files = collect_specification_files([root])
    discovered_mappings = [
        mapping
        for mapping in collect_specweave_tests(_test_files(tests_dir))
        if is_specification_mapping(mapping)
    ]
    deduped: dict[tuple[str, str, str], SpecweaveTestMapping] = {}
    for mapping in discovered_mappings + _declared_requirement_mappings(root):
        key = (
            mapping.spec or "",
            mapping.requirement or "",
            _normalize_nodeid(mapping.nodeid),
        )
        deduped.setdefault(key, mapping)
    mappings = sorted(deduped.values(), key=_mapping_sort_key)

    expected_requirements: dict[tuple[str, str], dict[str, Any]] = {}
    documents: list[dict[str, Any]] = []
    requirements_total = 0
    for spec_path in spec_files:
        document = parse_specification(spec_path)
        spec_ref = display_path(spec_path)
        requirement_entries: list[dict[str, Any]] = []
        for requirement in document.requirements:
            requirements_total += 1
            expected_requirements[(spec_ref, requirement.id)] = {
                "spec": spec_ref,
                "title": requirement.title,
                "line": requirement.line,
                "status": requirement.status,
                "kind": requirement.kind,
            }
            requirement_entries.append(
                {
                    "id": requirement.id,
                    "title": requirement.title,
                    "line": requirement.line,
                    "status": requirement.status,
                    "kind": requirement.kind,
                }
            )
        documents.append(
            {
                "path": spec_ref,
                "title": document.title,
                "requirements": requirement_entries,
            }
        )

    mapping_by_key, _ = _mapping_lookup(mappings)
    test_items = collect_pytest_tests(_test_files(tests_dir))
    intentional_unmapped_path = _intentional_unmapped_path(root, mapping_dir)
    test_waivers, requirement_waivers = _load_intentional_unmapped(
        intentional_unmapped_path
    )
    tests, unmapped_tests = _test_inventory(
        test_items,
        mappings,
        expected_requirements,
        test_waivers,
    )

    missing_bindings: list[dict[str, Any]] = []
    stale_bindings: list[dict[str, Any]] = []
    duplicate_bindings: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    requirements_bound = 0
    requirements_waived = 0

    for document in documents:
        for requirement in document["requirements"]:
            key = (document["path"], requirement["id"])
            linked = sorted(mapping_by_key.get(key, []), key=_mapping_sort_key)
            mappings_data = [_mapping_item(mapping) for mapping in linked]
            waived = requirement["id"] in requirement_waivers
            if linked:
                status = "duplicate" if len(linked) > 1 else "bound"
                requirements_bound += 1
                if status == "duplicate":
                    duplicate_bindings.append(
                        {
                            "spec": document["path"],
                            "requirement": requirement["id"],
                            "title": requirement["title"],
                            "count": len(linked),
                            "mappings": mappings_data,
                        }
                    )
            elif waived or requirement["kind"] in {"NGOAL", "RISK", "OPEN"}:
                status = "waived"
                requirements_waived += 1
            else:
                status = "missing"
                missing_bindings.append(
                    {
                        "spec": document["path"],
                        "requirement": requirement["id"],
                        "title": requirement["title"],
                        "line": requirement["line"],
                        "reason": "missing_requirement_binding",
                    }
                )

            requirements.append(
                {
                    "spec": document["path"],
                    "requirement": requirement["id"],
                    "title": requirement["title"],
                    "line": requirement["line"],
                    "status": status,
                    "mappings": mappings_data,
                    "waiver": requirement_waivers.get(requirement["id"]),
                }
            )

    for mapping in mappings:
        if _mapping_valid(mapping, expected_requirements):
            continue
        stale_bindings.append(
            {
                "spec": mapping.spec,
                "requirement": mapping.requirement,
                "test_file": mapping.test_file,
                "nodeid": _normalize_nodeid(mapping.nodeid),
                "function_name": mapping.function_name,
                "line": mapping.line,
                "source": mapping.source,
                "reason": (
                    "missing_spec"
                    if mapping.spec not in {document["path"] for document in documents}
                    else "missing_requirement"
                ),
            }
        )

    pytest_tests_total = len(test_items)
    pytest_tests_mapped = sum(
        1 for group in tests for item in group["items"] if item["status"] == "mapped"
    )
    pytest_tests_unmapped = len(unmapped_tests)
    pytest_tests_waived = sum(
        1 for group in tests for item in group["items"] if item["status"] == "waived"
    )
    pytest_mappings_stale = sum(
        1 for group in tests for item in group["items"] if item["status"] == "stale"
    )
    coverage_percent = (
        round((requirements_bound / requirements_total) * 100.0, 1)
        if requirements_total
        else 0.0
    )
    pytest_coverage_percent = (
        round(
            ((pytest_tests_mapped + pytest_tests_waived) / pytest_tests_total) * 100.0,
            1,
        )
        if pytest_tests_total
        else 0.0
    )
    status = (
        "failed"
        if any((missing_bindings, stale_bindings, duplicate_bindings, unmapped_tests))
        else "passed"
    )
    return {
        "schema_version": 1,
        "mode": "specifications",
        "status": status,
        "documents_total": len(documents),
        "requirements_total": requirements_total,
        "requirements_bound": requirements_bound,
        "requirements_waived": requirements_waived,
        "coverage_percent": coverage_percent,
        "pytest_tests_total": pytest_tests_total,
        "pytest_tests_mapped": pytest_tests_mapped,
        "pytest_tests_unmapped": pytest_tests_unmapped,
        "pytest_tests_waived": pytest_tests_waived,
        "pytest_mappings_stale": pytest_mappings_stale,
        "pytest_coverage_percent": pytest_coverage_percent,
        "documents": documents,
        "requirements": requirements,
        "tests": tests,
        "missing_bindings": missing_bindings,
        "stale_bindings": stale_bindings,
        "duplicate_bindings": duplicate_bindings,
        "unmapped_tests": unmapped_tests,
        "intentional_unmapped_path": display_path(intentional_unmapped_path),
    }


def _validate_view(view: str) -> None:
    if view not in _VIEW_VALUES:
        expected = ", ".join(sorted(_VIEW_VALUES))
        raise ValueError(
            f"Unsupported view filter: {view}; expected one of: {expected}"
        )


def _validate_show(show: str) -> None:
    if show not in _SHOW_VALUES:
        expected = ", ".join(sorted(_SHOW_VALUES))
        raise ValueError(
            f"Unsupported show filter: {show}; expected one of: {expected}"
        )


def render_specification_coverage_text(
    data: dict[str, Any],
    *,
    view: str = "requirement",
    show: str = "all",
) -> str:
    """Render human-readable specifications coverage text."""
    _validate_view(view)
    _validate_show(show)
    lines = [
        f"Specifications coverage: {data['status']}",
        (
            f"documents: {data['documents_total']}, "
            f"requirements: {data['requirements_total']}, "
            f"bound: {data['requirements_bound']}, "
            f"missing bindings: {len(data['missing_bindings'])}"
        ),
        (
            f"pytest tests: {data['pytest_tests_total']}, "
            f"mapped: {data['pytest_tests_mapped']}, "
            f"unmapped: {data['pytest_tests_unmapped']}, "
            f"waived: {data['pytest_tests_waived']}, "
            f"stale mappings: {data['pytest_mappings_stale']}"
        ),
        "",
    ]
    if view in {"requirement", "both"}:
        lines.extend(["Requirements -> pytest", ""])
        if data["missing_bindings"]:
            for binding in data["missing_bindings"]:
                lines.append(
                    f"- {binding['spec']} {binding['requirement']} "
                    f"{binding['title']} [missing]"
                )
        elif show in {"all", "bound"}:
            for requirement in data["requirements"]:
                if requirement["status"] == "bound":
                    lines.append(
                        f"- {requirement['spec']} "
                        f"{requirement['requirement']} "
                        f"{requirement['title']} [bound]"
                    )
        else:
            lines.append("No requirement-side items for current filters.")
        lines.append("")
    if view in {"test", "both"}:
        lines.extend(["Pytest -> requirements", ""])
        if data["unmapped_tests"]:
            for item in data["unmapped_tests"]:
                lines.append(f"- {item['nodeid']} [unmapped]")
        elif show in {"all", "bound"}:
            for group in data["tests"]:
                for item in group["items"]:
                    if item["status"] == "mapped":
                        mapping = item["mapping"] or {}
                        lines.append(
                            f"- {item['nodeid']} -> "
                            f"{mapping.get('spec', '')} "
                            f"{mapping.get('requirement', '')}"
                        )
        else:
            lines.append("No pytest-side items for current filters.")
    return "\n".join(lines).rstrip()


def render_specification_coverage_markdown(
    data: dict[str, Any],
    *,
    view: str = "requirement",
    show: str = "all",
) -> str:
    """Render specifications coverage as Markdown."""
    _validate_view(view)
    _validate_show(show)
    lines = [
        "# Specifications coverage",
        "",
        f"**Status:** {data['status']}",
        "",
        (
            f"**Requirement coverage:** "
            f"{data['requirements_bound']}/{data['requirements_total']} "
            f"bound ({data['coverage_percent']:.1f}%), "
            f"{len(data['missing_bindings'])} missing"
        ),
        (
            f"**Pytest coverage:** "
            f"{data['pytest_tests_mapped'] + data['pytest_tests_waived']}/"
            f"{data['pytest_tests_total']} accepted "
            f"({data['pytest_coverage_percent']:.1f}%), "
            f"{data['pytest_tests_unmapped']} unmapped"
        ),
        "",
    ]
    if view in {"requirement", "both"}:
        lines.extend(["## Requirements -> pytest", ""])
        if data["missing_bindings"]:
            for binding in data["missing_bindings"]:
                lines.append(
                    f"- `{binding['spec']}` `{binding['requirement']}` — "
                    f"{binding['title']}"
                )
            lines.append("")
    if view in {"test", "both"}:
        lines.extend(["## Pytest -> requirements", ""])
        if data["unmapped_tests"]:
            for item in data["unmapped_tests"]:
                lines.append(f"- `{item['nodeid']}`")
            lines.append("")
    return "\n".join(lines).rstrip()


def write_specification_coverage_json(data: dict[str, Any], path: str | Path) -> None:
    """Write specifications coverage *data* to *path*."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
