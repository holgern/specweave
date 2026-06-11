"""Lint specification Markdown documents."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

from specweave.specifications.model import Requirement, SpecificationDocument
from specweave.specifications.parser import (
    collect_specification_files,
    parse_specification,
)

_DEFAULT_ALLOWED_PREFIXES = ("REQ", "INV", "IF", "DATA", "NFR", "NGOAL", "RISK", "OPEN")
_NORMATIVE_PREFIXES = {"REQ", "INV", "IF", "DATA", "NFR"}
_NORMATIVE_LANGUAGE_RE = re.compile(r"\b(SHALL|SHOULD|MUST|MAY)\b")
_REQUIREMENT_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9-]*$")


@dataclass(frozen=True)
class LintFinding:
    """A single specifications lint result."""

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


def _resolve_relative_path(path_text: str, reference_path: Path) -> Path:
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


def lint_specification_files(
    paths: tuple[Path, ...] | list[Path] | set[Path],
    *,
    require_verification: bool = True,
    allowed_prefixes: tuple[str, ...] = _DEFAULT_ALLOWED_PREFIXES,
) -> list[LintFinding]:
    """Lint one or more specification files or directories."""
    documents: list[SpecificationDocument] = []
    findings: list[LintFinding] = []

    for path in collect_specification_files(paths):
        document = parse_specification(path)
        documents.append(document)
        display = _display_path(path)
        if not document.spec_id:
            findings.append(
                LintFinding(
                    code="SWSDD001",
                    level="error",
                    path=display,
                    message="Specification document is missing front matter id.",
                    line=1,
                )
            )
        for requirement in document.requirements:
            findings.extend(
                _lint_requirement(
                    document,
                    requirement,
                    require_verification=require_verification,
                    allowed_prefixes=allowed_prefixes,
                )
            )

    findings.extend(_duplicate_document_id_findings(documents))
    findings.extend(_duplicate_requirement_id_findings(documents))
    findings.extend(_missing_link_target_findings(documents))
    if documents and not any(
        document.path.name == "product.spec.md" for document in documents
    ):
        first_path = _display_path(documents[0].path.parent / "product.spec.md")
        findings.append(
            LintFinding(
                code="SWSDD010",
                level="warning",
                path=first_path,
                message=(
                    "Product specification is missing while "
                    "specifications mode is enabled."
                ),
            )
        )
    return findings


def lint_specification_tree(
    root: Path,
    *,
    require_verification: bool = True,
    allowed_prefixes: tuple[str, ...] = _DEFAULT_ALLOWED_PREFIXES,
) -> list[LintFinding]:
    """Lint every `.spec.md` file under *root*."""
    if not root.exists():
        return []
    return lint_specification_files(
        [root],
        require_verification=require_verification,
        allowed_prefixes=allowed_prefixes,
    )


def _lint_requirement(
    document: SpecificationDocument,
    requirement: Requirement,
    *,
    require_verification: bool,
    allowed_prefixes: tuple[str, ...],
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    display = _display_path(document.path)
    if requirement.kind not in allowed_prefixes:
        findings.append(
            LintFinding(
                code="SWSDD004",
                level="error",
                path=display,
                line=requirement.line,
                message=(
                    f"Requirement heading uses unsupported prefix {requirement.kind}."
                ),
            )
        )
    if not requirement.title.strip():
        findings.append(
            LintFinding(
                code="SWSDD006",
                level="error",
                path=display,
                line=requirement.line,
                message="Requirement heading title must be non-empty.",
            )
        )
    if (
        require_verification
        and requirement.status == "active"
        and requirement.kind in {"REQ", "INV"}
        and not requirement.verification_refs
    ):
        findings.append(
            LintFinding(
                code="SWSDD005",
                level="error",
                path=display,
                line=requirement.line,
                message="Active normative requirement has no verification reference.",
            )
        )
    if (
        requirement.status == "active"
        and requirement.kind in _NORMATIVE_PREFIXES
        and requirement.body
        and _NORMATIVE_LANGUAGE_RE.search(requirement.body) is None
    ):
        findings.append(
            LintFinding(
                code="SWSDD007",
                level="warning",
                path=display,
                line=requirement.line,
                message=(
                    "Active requirement uses weak language instead of "
                    "SHALL/SHOULD/MUST/MAY."
                ),
            )
        )
    for ref in requirement.verification_refs:
        if ref.kind != "pytest":
            continue
        pytest_file = _resolve_relative_path(
            ref.target.split("::", 1)[0],
            document.path,
        )
        if not pytest_file.exists():
            findings.append(
                LintFinding(
                    code="SWSDD008",
                    level="error",
                    path=display,
                    line=requirement.line,
                    message=(
                        "Verification reference points to missing pytest "
                        f"test: {ref.target}"
                    ),
                )
            )
    return findings


def _duplicate_document_id_findings(
    documents: list[SpecificationDocument],
) -> list[LintFinding]:
    by_id: dict[str, list[SpecificationDocument]] = defaultdict(list)
    for document in documents:
        if document.spec_id:
            by_id[document.spec_id].append(document)
    findings: list[LintFinding] = []
    for spec_id, duplicates in by_id.items():
        if len(duplicates) < 2:
            continue
        for document in duplicates:
            findings.append(
                LintFinding(
                    code="SWSDD002",
                    level="error",
                    path=_display_path(document.path),
                    line=1,
                    message=f"Duplicate specification document id {spec_id}.",
                )
            )
    return findings


def _duplicate_requirement_id_findings(
    documents: list[SpecificationDocument],
) -> list[LintFinding]:
    by_id: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    for document in documents:
        for requirement in document.requirements:
            by_id[requirement.id].append((document.path, requirement.line))
    findings: list[LintFinding] = []
    for requirement_id, duplicates in by_id.items():
        if len(duplicates) < 2:
            continue
        for path, line in duplicates:
            findings.append(
                LintFinding(
                    code="SWSDD003",
                    level="error",
                    path=_display_path(path),
                    line=line,
                    message=f"Duplicate requirement id {requirement_id}.",
                )
            )
    return findings


def _missing_link_target_findings(
    documents: list[SpecificationDocument],
) -> list[LintFinding]:
    all_ids = {
        requirement.id
        for document in documents
        for requirement in document.requirements
    }
    findings: list[LintFinding] = []
    for document in documents:
        for requirement in document.requirements:
            for link in requirement.links:
                if not _REQUIREMENT_ID_RE.match(link):
                    continue
                if link in all_ids:
                    continue
                findings.append(
                    LintFinding(
                        code="SWSDD009",
                        level="error",
                        path=_display_path(document.path),
                        line=requirement.line,
                        message=f"Linked requirement id does not exist: {link}.",
                    )
                )
    return findings
