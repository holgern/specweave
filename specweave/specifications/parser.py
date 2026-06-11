"""Parser for specification Markdown documents."""

from __future__ import annotations

import re
from pathlib import Path

from specweave.specifications.model import (
    Requirement,
    SpecificationDocument,
    VerificationRef,
)

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_REQUIREMENT_RE = re.compile(
    r"^(?P<id>[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9-]*)(?:\s*(?:—|-)\s*(?P<title>.*))?$"
)
_VERIFICATION_RE = re.compile(r"^-\s*(?P<kind>[a-z][a-z0-9_-]*)\s*:\s*(?P<target>.+)$")
_LINK_RE = re.compile(r"^-\s*(?P<link>.+)$")


def collect_specification_files(
    paths: tuple[Path, ...] | list[Path] | set[Path],
) -> list[Path]:
    """Collect `.spec.md` files from one or more files or directories."""
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.name.endswith(".spec.md"):
            files.append(path)
            continue
        if path.is_dir():
            files.extend(sorted(candidate for candidate in path.rglob("*.spec.md")))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def parse_specification(path: Path) -> SpecificationDocument:
    """Parse a specification document from *path*."""
    return parse_specification_text(path.read_text(encoding="utf-8"), source_path=path)


def parse_specification_text(
    text: str,
    *,
    source_path: Path,
) -> SpecificationDocument:
    """Parse *text* into a `SpecificationDocument`."""
    lines = text.splitlines()
    front_matter, body_start = _parse_front_matter(lines)
    title = str(
        front_matter.get("title")
        or _first_heading(lines[body_start:])
        or source_path.stem
    )
    spec_id = str(front_matter.get("id", ""))
    kind = str(front_matter.get("kind", "specification"))
    status = str(front_matter.get("status", "active"))
    requirements = _parse_requirements(
        lines,
        body_start=body_start,
        default_status=status,
    )
    return SpecificationDocument(
        path=source_path,
        spec_id=spec_id,
        title=title,
        kind=kind,
        status=status,
        requirements=tuple(requirements),
    )


def _parse_front_matter(lines: list[str]) -> tuple[dict[str, object], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    front_matter: dict[str, object] = {}
    index = 1
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped == "---":
            return front_matter, index + 1
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            front_matter[key.strip()] = _parse_scalar(value.strip())
        index += 1
    raise ValueError("Unterminated front matter.")


def _parse_scalar(value: str) -> object:
    if value.isdigit():
        return int(value)
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    return value


def _first_heading(lines: list[str]) -> str | None:
    for line in lines:
        match = _HEADING_RE.match(line.strip())
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return None


def _parse_requirements(
    lines: list[str],
    *,
    body_start: int,
    default_status: str,
) -> list[Requirement]:
    headings: list[tuple[int, int, str]] = []
    for index in range(body_start, len(lines)):
        match = _HEADING_RE.match(lines[index].strip())
        if match is None:
            continue
        headings.append((index, len(match.group(1)), match.group(2).strip()))

    requirements: list[Requirement] = []
    for position, (index, level, heading_text) in enumerate(headings):
        if level != 3:
            continue
        match = _REQUIREMENT_RE.match(heading_text)
        if match is None:
            continue
        end = len(lines)
        for later_index, later_level, _ in headings[position + 1 :]:
            if later_level <= 3:
                end = later_index
                break
        requirement_id = match.group("id")
        requirement_title = (match.group("title") or "").strip()
        requirements.append(
            _parse_requirement_block(
                requirement_id=requirement_id,
                requirement_title=requirement_title,
                default_status=default_status,
                lines=lines[index + 1 : end],
                line=index + 1,
            )
        )
    return requirements


def _parse_requirement_block(
    *,
    requirement_id: str,
    requirement_title: str,
    default_status: str,
    lines: list[str],
    line: int,
) -> Requirement:
    body_lines: list[str] = []
    rationale_lines: list[str] = []
    verification_refs: list[VerificationRef] = []
    links: list[str] = []
    status = default_status

    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("Rationale:"):
            inline = stripped.partition(":")[2].strip()
            block, index = _collect_section(lines, index + 1)
            rationale_lines = [inline] if inline else []
            rationale_lines.extend(block)
            continue
        if stripped.startswith("Verification:"):
            inline = stripped.partition(":")[2].strip()
            block, index = _collect_section(lines, index + 1)
            verification_refs.extend(
                _parse_verification_block(([inline] if inline else []) + block)
            )
            continue
        if stripped.startswith("Links:"):
            inline = stripped.partition(":")[2].strip()
            block, index = _collect_section(lines, index + 1)
            links.extend(_parse_links_block(([inline] if inline else []) + block))
            continue
        if stripped.startswith("Status:"):
            value = stripped.partition(":")[2].strip()
            if value:
                status = value
            index += 1
            continue
        body_lines.append(lines[index])
        index += 1

    kind = requirement_id.split("-", 1)[0]
    return Requirement(
        id=requirement_id,
        title=requirement_title,
        kind=kind,
        status=status,
        body=_normalize_block(body_lines),
        rationale=_normalize_block(rationale_lines),
        verification_refs=tuple(verification_refs),
        links=tuple(links),
        line=line,
    )


def _collect_section(lines: list[str], start: int) -> tuple[list[str], int]:
    collected: list[str] = []
    index = start
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith(("Rationale:", "Verification:", "Links:", "Status:")):
            break
        collected.append(lines[index])
        index += 1
    return collected, index


def _parse_verification_block(lines: list[str]) -> list[VerificationRef]:
    refs: list[VerificationRef] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        match = _VERIFICATION_RE.match(stripped)
        if match is None:
            continue
        refs.append(
            VerificationRef(
                kind=match.group("kind"),
                target=match.group("target").strip(),
            )
        )
    return refs


def _parse_links_block(lines: list[str]) -> list[str]:
    links: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        match = _LINK_RE.match(stripped)
        if match is not None:
            links.append(match.group("link").strip())
    return links


def _normalize_block(lines: list[str]) -> str:
    stripped_lines = [line.rstrip() for line in lines]
    while stripped_lines and not stripped_lines[0].strip():
        stripped_lines.pop(0)
    while stripped_lines and not stripped_lines[-1].strip():
        stripped_lines.pop()
    return "\n".join(stripped_lines).strip()
