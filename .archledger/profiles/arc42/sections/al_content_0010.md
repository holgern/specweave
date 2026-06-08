---
schema_version: 2
id: al_content_0010
type: section
section: quality_requirements
title: Quality Requirements
order: 100
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
---

## Correctness

- **Fail-closed by default.** Evidence normalization must never mark a scenario
  or acceptance criterion as passed when the source data is failed, errored,
  skipped, pending, undefined, ambiguous, missing, or unlinked.
- **Tag-based validation.** Lint checks enforce `@bdd-*` IDs and
  Given/When/Then steps when configured. Duplicate `@bdd-*` IDs across
  features are errors.
- **Deterministic output.** Config rendering, JSON output, and generated
  files must be reproducible from the same inputs.

## Maintainability

- **Layered architecture.** Each module owns its domain (Gherkin parsing,
  behavior workflow, report normalization, etc.). Cross-layer calls use
  well-defined module boundaries.
- **Frozen dataclasses.** Immutable models prevent accidental mutation.
- **Type-checked.** `mypy` with `strict` settings runs on `specweave/`.
  All public functions have type hints.
- **31 focused test files** covering config, init, doctor, CLI, parser,
  writer, coverage, reporting, integrations, and more.

## Usability

- **CLI-first.** All features are accessible through `specweave` CLI commands.
- **`--json` root option** provides machine-readable output for all commands.
- **`doctor` command** diagnoses setup and convention problems.
- **Idempotent init.** Running `specweave init` twice does not overwrite
  existing config or features without `--force`.

## Performance

- **AST-based discovery.** No test execution during spec generation.
- **File-based only.** No network calls, database queries, or daemon
  processes.
- **Minimal dependencies.** Only typer, click, and gherkin-official at runtime.
