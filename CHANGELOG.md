# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-09

### Changed

- Made `gherkin-official` an optional dependency (`pip install specweave[gherkin]`). The default parser no longer requires it. SpecWeave validates supported Gherkin subsets strictly without the official parser.
- Removed Markdown-with-Gherkin (`.feature.md`) support. The canonical format is now classic `.feature` only. Legacy `.feature.md` paths fail with explicit migration errors.
- Switched config defaults to public `specweave.toml` and readable artifact paths (`specs/behavior/evidence`, `specs/behavior/mappings`, `reports/behavior/specweave`).

### Added

- Strict SpecWeave subset validator that rejects unsupported Gherkin constructs (Background, Scenario Outline, tables, doc strings, `*` steps).
- Two-way coverage review command (`specweave review coverage`) that reports both feature-to-pytest and pytest-to-feature coverage gaps with actionable reasons (`missing_test_file`, `unmapped_candidate_tests`).
- Reverse pytest inventory: behavior coverage now tracks mapped, unmapped, and stale pytest tests with `schema_version 2` JSON output.
- `specweave behavior coverage` extended with `--view`, `--test-file`, and `--suggestions` options.
- Sphinx documentation baseline: 10 content pages covering getting started, concepts, behavior workflow, Gherkin formats, commands, configuration, reports and evidence, integrations, development, and API.
- `docs` extra in `pyproject.toml` (`myst-parser`, `sphinx`, `sphinx-rtd-theme`).
- Updated `ARCHITECTURE.md` and `AGENTS.md` to reflect optional `gherkin-official` and classic-only format.

### Fixed

- Lint now reports unsupported Gherkin constructs as errors instead of warnings.
- Writer rejects `Scenario Outline`/`Template` keywords explicitly.
- Markdown parser restricts Scenario headings to `Scenario`/`Example` only.
- Removed stray badge markup from `README.md`.
- Synced `.specweave.toml` with current `render_default_config()` output.

## [0.1.0] - 2026-06-08

### Added

- Initial SpecWeave MVP: package skeleton, CLI (`explain`, `draft`, `bind`, `run`, `version`), Gherkin model/writer/parser, AST inspection, spec-to-code generation, and delegated test runner.
- Gherkin `Rule:` support, multi-tag lines, and top-level scenario backward compatibility.
- Task-BDD model with JSON store, round-trip ID preservation, and `And`/`But` grouping.
- Report normalization for `cucumber-json` and `junit-xml` with fail-closed status semantics.
- Tag-based acceptance criterion mapping (`@bdd-*`, `@ac-*`) with `require_expected_coverage`.
- File-based Taskledger adapter (rich + legacy shapes, no hard import dependency).
- Archledger candidate markdown renderer (candidate-only, no Archledger dependency).
- Step skeleton backends: `behave` (verbatim) and `pytest-bdd` with backend registry.
- CLI subcommands: `report normalize`, `report inspect`, `bdd export`, `bdd import-feature`, `archledger candidate`.
- Behavior-first plain pytest workflow: `behavior check`, `behavior index`, `behavior generate-tests`, `behavior coverage`, `behavior report import`.
- Config system with `SpecWeavePaths` and `SpecWeaveConfig` dataclasses, `find_config()`, `load_config()`.
- `specweave init` command with dry-run, force, public config, and `behaviour` spelling support.
- `specweave doctor` diagnostics (12 checks) with `--fix` for missing directories.
- `specweave review specs` for lint, coverage, evidence, and needs-review aggregation.
- `specweave create feature` with `--from-json` structured rendering and `--dry-run`.
- `specweave create plan` and `specweave create taskledger-task` for planning workflows.
- Root `--json` callback for machine-readable output on all top-level commands.
- Pytest-to-Gherkin translation with `@bdd-*` tags, `@generated`, and `@needs-review` markers.
- Brownfield Gherkin workflow: `extract_module_docstring()`, `extract_class_rules()`.
- Markdown-with-Gherkin parser and writer with backticked tags and heading-depth-aware nesting (now removed in 0.2.0).
- Official `gherkin-official` parser adapter with AST conversion (now optional in 0.2.0).
- Bulk feature conversion with summary reporting and safe replace-source handling.
- Explicit pytest coverage mapping via `.feature` docstring references.
- Cross-ledger trace contract: `specweave trace` and `specweave combi check` with versioned JSON Schema files.
- Behavior manifest and Markdown index generation.
- Versioned JSON Schema contracts for trace, behavior evidence, and Taskledger BDD exchange.
- Apache-2.0 license.
