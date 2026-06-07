"""Core dataclass models for Gherkin structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Step:
    """A single Gherkin step (Given, When, Then, And, But)."""

    keyword: str  # Given, When, Then, And, But
    text: str


@dataclass(frozen=True)
class Scenario:
    """A Gherkin scenario with optional tags."""

    title: str
    steps: tuple[Step, ...]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class Feature:
    """A Gherkin feature containing scenarios."""

    title: str
    scenarios: tuple[Scenario, ...]
    tags: tuple[str, ...] = ()
    description: str = ""
    source_path: Path | None = None


@dataclass(frozen=True)
class AcceptanceCriterion:
    """A single acceptance criterion from a task."""

    task_id: str
    criterion_id: str
    text: str


@dataclass(frozen=True)
class RunnerSummary:
    """Normalized output from a delegated BDD runner."""

    schema_version: int
    runner: str
    command: tuple[str, ...]
    exit_code: int
    status: str  # passed, failed, error
    scenarios: int = 0
    failed: int = 0
    evidence: tuple[str, ...] = field(default_factory=tuple)
