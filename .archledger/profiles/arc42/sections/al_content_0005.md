---
schema_version: 2
id: al_content_0005
type: section
section: building_block_view
title: Building Block View
order: 50
status: accepted
date: "2026-06-08"
body_format: markdown
created_at: "2026-06-08T12:58:35Z"
updated_at: "2026-06-08T18:30:00Z"
source_refs:
  - specweave/
---

## Level 1: Overall system

```text
┌─────────────────────────────────────────────────────┐
│                    SpecWeave CLI                      │
│  (specweave/cli.py, specweave/cli_context.py)        │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │  Config   │  │  Gherkin │  │    Behavior      │   │
│  │  Layer    │  │  Layer   │  │    Workflow      │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Translate│  │  Reports │  │  Python Inspect  │   │
│  │  Layer   │  │  Layer   │  │                  │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
│                                                       │
│  ┌──────────────────────────────────────────────┐    │
│  │         Integrations (Taskledger, Archledger)│    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## Level 2: Key building blocks

### CLI & Entry Points

- `specweave/cli.py` — Typer app, command groups (behavior, bdd, report,
  create, review, combi), root `--config`/`--json` options.
- `specweave/cli_context.py` — `CliContext` construction, JSON-output flag.
- `specweave/launcher.py` — console script entry `main()`.
- `specweave/__main__.py` — `python -m specweave` entry.

### Configuration & Init

- `specweave/config.py` — `SpecWeaveConfig` dataclass hierarchy, TOML loading,
  config discovery (`.specweave.toml` preferred over `specweave.toml`,
  parent-walking), default config rendering.
- `specweave/init.py` — `specweave init`, directory layout creation, managed
  README detection, dry-run/force.
- `specweave/doctor.py` — project diagnostics and `--fix`.

### Gherkin Layer

- `specweave/gherkin/model.py` — `Feature`, `Rule`, `Scenario`, `Step`,
  `AcceptanceCriterion`, `RunnerSummary` dataclasses.
- `specweave/gherkin/parser.py` — Gherkin text → `Feature` model.
- `specweave/gherkin/writer.py` — `Feature` model → Gherkin text.
- `specweave/gherkin/lint.py` — feature collection, canonical path checks,
  scenario linting, duplicate `@bdd-*` detection.
- `specweave/gherkin/tags.py` — tag parsing/filtering helpers.
- `specweave/gherkin/convert.py` — classic ↔ Markdown format conversion.
- `specweave/gherkin/markdown.py` — Markdown `.feature.md` parser/writer.
- `specweave/gherkin/draft.py` — feature draft loading from JSON.

### Behavior Workflow

- `specweave/behavior/common.py` — shared paths, slugs, feature identity,
  scenario IDs, canonical test path derivation.
- `specweave/behavior/index.py` — behavior README and manifest generation.
- `specweave/behavior/generate.py` — plain pytest skeleton generation from
  canonical features.
- `specweave/behavior/coverage.py` — static mapping/coverage checks between
  specs and tests.
- `specweave/behavior/reporting.py` — pytest/JUnit report import and evidence
  mapping.

### Python Inspection

- `specweave/python_inspect/ast_reader.py` — AST-based test discovery,
  `SpecweaveTestMapping` extraction, `@specweave` marker and comment parsing.
- `specweave/python_inspect/assertions.py` — assertion-to-plain-English
  rendering.

### Translation

- `specweave/translate/pytest_to_gherkin.py` — brownfield pytest-to-Gherkin
  generation.
- `specweave/translate/spec_to_code.py` — feature drafting, step/backend
  binding helpers.
- `specweave/translate/code_to_spec.py` — test explanation helpers.
- `specweave/translate/naming.py` — naming convention utilities.

### Reports

- `specweave/reports/model.py` — `ScenarioResult`, `CriterionResult`,
  `NormalizedBddReport` dataclasses, status constants.
- `specweave/reports/cucumber_json.py` — Cucumber JSON parser.
- `specweave/reports/junit_xml.py` — JUnit XML parser.
- `specweave/reports/mapping.py` — tag-based trace extraction and acceptance
  coverage summarization.
- `specweave/reports/normalize.py` — report normalization and evidence JSON
  assembly.

### BDD Bridge

- `specweave/bdd/model.py` — `TaskBddSpec`, `BddRule`, `BddExample`
  dataclasses.
- `specweave/bdd/convert.py` — bidirectional conversion between Gherkin
  model and task-BDD JSON model.
- `specweave/bdd/store.py` — task-BDD JSON load/save.

### Backends (bridge/legacy)

- `specweave/backends/behave.py` — behave step-definition skeleton generation.
- `specweave/backends/pytest_bdd.py` — pytest-bdd skeleton generation.

### Integrations

- `specweave/integrations/taskledger.py` — file-based Taskledger exchange.
- `specweave/integrations/archledger.py` — Archledger candidate markdown
  rendering.
- `specweave/integrations/combi.py` — cross-ledger integration diagnostics.

### Cross-cutting

- `specweave/trace.py` — behavior-centered trace bundle extraction.
- `specweave/review.py` — spec review findings.
- `specweave/planning.py` — plan generation from features.
- `specweave/runners/command.py` — subprocess runner delegation.
- `specweave/runners/reports.py` — runner summary writing.
- `specweave/errors.py` — `SpecWeaveError`, `ParseError`, `BackendError`,
  `RunnerError`.
