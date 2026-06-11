"""Models for specification documents and requirement traceability."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VerificationRef:
    """A declared verification reference for a requirement."""

    kind: str
    target: str
    status: str = "declared"


@dataclass(frozen=True)
class Requirement:
    """A parsed normative or informational requirement block."""

    id: str
    title: str
    kind: str
    status: str
    body: str
    rationale: str
    verification_refs: tuple[VerificationRef, ...]
    links: tuple[str, ...]
    line: int


@dataclass(frozen=True)
class SpecificationDocument:
    """A parsed `.spec.md` document."""

    path: Path
    spec_id: str
    title: str
    kind: str
    status: str
    requirements: tuple[Requirement, ...]
