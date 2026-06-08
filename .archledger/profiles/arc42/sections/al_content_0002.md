---
schema_version: 2
id: al_content_0002
type: section
section: architecture_constraints
title: Architecture Constraints
order: 20
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Technical constraints

- **Python ≥3.10.** The package uses `from __future__ import annotations` and
  union type syntax (`X | Y`) throughout.
- **No required runtime dependencies beyond typer, click, and gherkin-official.**
  `tomli` is conditionally imported for Python <3.11. Taskledger and Archledger
  are never runtime dependencies.
- **No test runner dependency for the canonical workflow.** SpecWeave generates
  plain pytest functions; it does not require `pytest-bdd`, `behave`, or
  step-definition modules.
- **File-based configuration.** `.specweave.toml` (hidden, preferred) or
  `specweave.toml` (public). TOML only; no YAML or JSON config.
- **Frozen dataclasses for all public models.** Gherkin models
  (`specweave/gherkin/model.py`), report models (`specweave/reports/model.py`),
  and BDD models (`specweave/bdd/model.py`) are immutable dataclasses.
- **No database or external service.** SpecWeave reads and writes files only.
  All state is filesystem-based under `.specweave/`, `specs/`, `tests/`, and
  `reports/`.

## Organizational constraints

- Skills live under `skills/specweave/` outside the Python package. They are not
  shipped as package data or exposed via `importlib.resources`.
- The package name on PyPI is `specweave`. The console script is
  `specweave = specweave.launcher:main`.
- License: Apache-2.0.
