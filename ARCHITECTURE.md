---
title: "Architecture Documentation"
date: "1980-01-01"
generator: "archledger 0.1.1.dev13+g9edca5498"
arc42_template_version: "9.0-EN"
---

# Architecture Documentation

Generated from archledger records. Do not edit this generated file directly.

# Introduction and Goals

## Overview

SpecWeave is a Python CLI and library that translates between canonical Gherkin
behavior specifications, plain pytest enforcement, and normalized BDD execution
evidence. It is not a task ledger, architecture ledger, or CI system.

## Goals

1. **Keep behavior intent readable.** Gherkin `.feature` (Markdown) files
   under `specs/behavior/features/<area>/` serve as the human-readable source of
   truth for what a system should do.
2. **Keep executable validation traceable.** Plain pytest tests under `tests/`
   are the default enforcement path. SpecWeave maps between Gherkin scenarios
   and pytest via stable `@bdd-*` tags, not scenario titles.
3. **Fail closed on incomplete or ambiguous evidence.** A passing command exit
   code alone is never sufficient evidence when a native report is available.
   Skipped, pending, undefined, ambiguous, and missing results block acceptance.
4. **Bridge brownfield pytest into structured behavior specs.** The
   `create gherkin --from-tests` workflow uses AST-based discovery to generate
   draft Gherkin from existing tests without executing them.
5. **Exchange normalized evidence with external tools.** SpecWeave produces
   Taskledger-compatible evidence JSON and Archledger candidate records through
   file-based integrations, without making those tools runtime dependencies.

## Non-goals

- SpecWeave does not own task lifecycle, plan approval, or user gates
  (Taskledger owns those).
- SpecWeave does not own durable architecture records (Archledger owns those).
- SpecWeave does not orchestrate CI pipelines.
- SpecWeave does not require `pytest-bdd`, `behave`, or step-definition modules
  for its canonical workflow.

## Requirements Overview

<!-- archledger: no accepted records for this section yet -->

## Quality Goals

<!-- archledger: no accepted records for this section yet -->

## Stakeholders

<!-- archledger: no accepted records for this section yet -->

# Architecture Constraints

## Technical constraints

- **Python ≥3.10.** The package uses `from __future__ import annotations` and
  union type syntax (`X | Y`) throughout.
- **No required runtime dependencies beyond typer and click.**
  `tomli` is conditionally imported for Python <3.11. `gherkin-official` is
  optional (`pip install specweave[gherkin]`) and only needed for the official
  parser backend. SpecWeave's built-in parser and validation work without it.
  Taskledger and Archledger are never runtime dependencies.
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

<!-- archledger: no accepted records for this section yet -->

# Context and Scope

## System boundary

SpecWeave is a developer CLI tool. It runs in a project checkout directory,
reads and writes local files, and delegates test execution to an external
command (typically `pytest`). It does not listen on ports, run as a daemon, or
expose a network API.

## External actors

```text
┌─────────────┐     reads/writes      ┌───────────────┐
│   Developer  │◄─────────────────────►│   Filesystem  │
│  (CLI user)  │                       │  (.specweave, │
└──────┬───────┘                       │   specs/,     │
       │ invokes                       │   tests/,     │
       ▼                               │   reports/)   │
┌─────────────┐     delegates          └───────────────┘
│  SpecWeave   │──► pytest (external)
│    CLI       │
└──────┬───────┘
       │ file exchange
       ▼
┌──────────────┐  ┌──────────────┐
│  Taskledger   │  │  Archledger  │
│ (task state)  │  │  (arch docs) │
└──────────────┘  └──────────────┘
```

## Interfaces

- **CLI** (`specweave` console script): Typer-based CLI with `--config`,
  `--json` root options. Human and machine-readable output.
- **Filesystem**: canonical layout of `specs/behavior/features/<area>/`,
  `tests/`, `reports/behavior/`, `.specweave/`.
- **Taskledger integration**: file-based JSON exchange
  (`specweave/integrations/taskledger.py`). SpecWeave reads task-BDD JSON and
  writes evidence JSON. It never approves plans or manages task lifecycle.
- **Archledger integration**: candidate markdown rendering
  (`specweave/integrations/archledger.py`). SpecWeave writes candidate files
  when explicitly requested; it never creates accepted records implicitly.



## Business Context

<!-- archledger: no accepted records for this section yet -->

## Technical Context

<!-- archledger: no accepted records for this section yet -->

# Solution Strategy

## Key decisions

1. **Tag-based traceability, not title-based.** Scenario identity is anchored
   on `@bdd-*` tags. Acceptance criteria are anchored on `@ac-*` tags. Scenario
   titles are display/debug text only. This makes validation deterministic and
   rename-safe.

2. **Plain pytest as the canonical enforcement path.** SpecWeave generates
   standard `test_*.py` files with `@specweave` markers and source-mapping
   comments. No `pytest-bdd` step definitions, no `behave` step modules, no
   `tests/bdd/` directory are required.

3. **Fail-closed evidence.** Report normalization treats every non-passed
   scenario status (failed, skipped, pending, undefined, ambiguous, missing,
   unlinked) as blocking. A clean command exit code is never sufficient
   evidence.

4. **Frozen dataclass models throughout.** `Feature`, `Rule`, `Scenario`,
   `Step`, `ScenarioResult`, `NormalizedBddReport`, `TaskBddSpec`, and
   configuration classes are all immutable frozen dataclasses. This prevents
   accidental mutation during pipeline transforms.

5. **Dual Gherkin format.** SpecWeave supports both classic `.feature` and
   Markdown `.feature` files. The default is `.feature`. A `convert`
   command bridges between formats.

6. **Layered architecture.** The code is organized into Gherkin model/parser/
   writer, behavior workflow, translation, report normalization, Python AST
   inspection, integrations, and CLI. Each layer owns its domain; cross-layer
   calls go through well-defined module boundaries.

7. **AST-based discovery, not test execution.** The brownfield workflow
   (`create gherkin --from-tests`) reads Python AST to infer behavior from
   test names, docstrings, markers, and assertions. Tests are never executed
   during discovery.

## Strategy Items

<!-- archledger: no accepted records for this section yet -->

# Building Block View

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
- `specweave/gherkin/markdown.py` — Markdown `.feature` parser/writer.
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



## Whitebox Overall System

## Motivation

SpecWeave decomposes into seven primary black boxes, each owning a clear
domain. The decomposition keeps Gherkin parsing separate from behavior
workflow logic, separate from report normalization, and separate from
external integrations.

## Contained building blocks

- **CLI Layer** (al_block_0014) — Typer command dispatch, context, and output formatting
- **Gherkin Layer** (al_block_0015) — Model, parser, writer, linter, and format conversion
- **Behavior Workflow** (al_block_0016) — Index, coverage, test generation, report import
- **Report Normalization** (al_block_0017) — Native report parsing, normalization, evidence assembly
- **Translation Layer** (al_block_0018) — pytest-to-Gherkin, spec-to-code, code-to-spec
- **Python AST Inspection** (al_block_0019) — Static test discovery and mapping extraction
- **Integrations** (al_block_0020) — Taskledger exchange, Archledger candidates, combi check

## Important interfaces

- CLI → all other layers via lazy imports in command handlers
- Behavior Workflow → Gherkin Layer for parsing and linting
- Report Normalization → Gherkin Layer for tag-based mapping
- Translation → Gherkin Layer for writing, AST Inspection for reading
- Integrations → Behavior Workflow, Reports, and Gherkin models

### Level 2

#### CLI Layer

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Root Typer application with sub-apps for `behavior`, `bdd`, `report`,
`create`, `review`, and `combi` command groups. Handles root `--config`
(explicit config path) and `--json` (machine-readable output) options.
Constructs `CliContext` with loaded config and JSON-output flag.

## Key files

- `specweave/cli.py` (1321 lines) — all command declarations
- `specweave/cli_context.py` — `CliContext` and `build_cli_context()`
- `specweave/launcher.py` — `main()` entry point
- `specweave/__main__.py` — `python -m specweave` support

## Interfaces

- **Inbound:** Developer invokes `specweave` console script
- **Outbound:** Lazy imports to all other layers from command handlers
- **Output:** Human text to stdout, JSON to stdout when `--json` is set

#### Gherkin Layer

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Owns the Gherkin data model, parsing, writing, linting, format conversion, and
validation. Supports both classic `.feature` and Markdown `.feature` formats.
The built-in parser and subset validator work without external dependencies.
The optional `gherkin-official` backend (`pip install specweave[gherkin]`)
provides full Cucumber Gherkin compatibility.

## Key files

- `specweave/gherkin/model.py` — `Feature`, `Rule`, `Scenario`, `Step` frozen dataclasses
- `specweave/gherkin/parser.py` (257 lines) — Gherkin text → `Feature` model
- `specweave/gherkin/writer.py` — `Feature` model → Gherkin text
- `specweave/gherkin/lint.py` (410 lines) — linting, duplicate ID detection, path checks
- `specweave/gherkin/convert.py` (378 lines) — classic ↔ Markdown conversion
- `specweave/gherkin/markdown.py` (463 lines) — Markdown `.feature` parser/writer
- `specweave/gherkin/tags.py` — tag parsing/filtering helpers
- `specweave/gherkin/draft.py` — feature draft loading from JSON
- `specweave/gherkin/official.py` — adapter for optional `gherkin-official` parser
- `specweave/gherkin/validation.py` — SpecWeave subset validator (no external deps)

## Interfaces

- **Inbound:** Called by CLI, Behavior Workflow, Translation, and Integrations
- **Outbound:** Pure data transformations; optional `gherkin-official` backend
  (lazy-imported, only when installed)

#### Behavior Workflow

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Orchestrates the canonical behavior workflow: lint specs, generate index and
manifest, generate plain pytest skeletons, check static coverage, and import
pytest/JUnit reports into evidence JSON.

## Key files

- `specweave/behavior/common.py` — shared paths, slugs, feature identity, scenario IDs
- `specweave/behavior/index.py` (246 lines) — README and manifest generation
- `specweave/behavior/generate.py` — plain pytest skeleton generation
- `specweave/behavior/coverage.py` (538 lines) — static mapping and coverage checks
- `specweave/behavior/reporting.py` (180 lines) — report import and evidence mapping

## Interfaces

- **Inbound:** CLI `behavior` subcommands
- **Outbound:** Gherkin Layer (parsing, linting), Python AST Inspection (coverage), Reports (evidence)

#### Report Normalization

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Parses native runner reports (Cucumber JSON, JUnit XML), normalizes them into a
unified `NormalizedBddReport` model, maps scenario results to `@bdd-*` and
`@ac-*` tags, and assembles fail-closed evidence JSON.

## Key files

- `specweave/reports/model.py` — `ScenarioResult`, `CriterionResult`, `NormalizedBddReport`, status constants
- `specweave/reports/normalize.py` (233 lines) — report normalization pipeline
- `specweave/reports/cucumber_json.py` — Cucumber JSON parser
- `specweave/reports/junit_xml.py` — JUnit XML parser
- `specweave/reports/mapping.py` — tag-based trace extraction, AC coverage summarization

## Interfaces

- **Inbound:** CLI `report` subcommands, Behavior Workflow `import-report`
- **Outbound:** Writes normalized JSON and Taskledger evidence JSON to filesystem

#### Translation Layer

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Bidirectional translation between Python tests and Gherkin behavior specs:

- **pytest → Gherkin:** Brownfield workflow. Uses AST Inspection to discover
  tests, then generates draft `.feature` files.
- **Gherkin → pytest:** New-feature workflow. Generates plain pytest skeletons
  from canonical feature files.
- **Code → Spec explanation:** Explains Python test files as candidate behavior
  specs.

Also handles step/backend binding for legacy `behave` and `pytest-bdd`
workflows via `specweave/backends/`.

## Key files

- `specweave/translate/pytest_to_gherkin.py` (273 lines) — brownfield generation
- `specweave/translate/spec_to_code.py` — feature drafting and binding
- `specweave/translate/code_to_spec.py` — test explanation
- `specweave/translate/naming.py` — naming conventions
- `specweave/backends/behave.py` — behave step skeleton generation
- `specweave/backends/pytest_bdd.py` — pytest-bdd step skeleton generation

## Interfaces

- **Inbound:** CLI `create gherkin`, `create feature`, `bind`, `explain`
- **Outbound:** Gherkin Layer (writing), Python AST Inspection (reading), backends

#### Python AST Inspection

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

Static analysis of Python test files using the `ast` module. Discovers test
functions, extracts `@specweave` markers and source-mapping comments, and
converts assert statements into candidate `Then` clauses.

## Key files

- `specweave/python_inspect/ast_reader.py` (303 lines) — `extract_test_scenarios()`,
  `collect_specweave_tests()`, `SpecweaveTestMapping` dataclass
- `specweave/python_inspect/assertions.py` — `describe_assert()` for
  assertion-to-English rendering

## Interfaces

- **Inbound:** Called by Translation Layer and Behavior Coverage
- **Outbound:** Returns `Scenario` and `SpecweaveTestMapping` objects; no filesystem writes

#### Integrations

**Parent:** al_block_0013
**Interfaces:** 
**Location:** 

## Responsibility

File-based exchange with Taskledger and Archledger, plus cross-ledger
integration auditing. SpecWeave never calls Taskledger or Archledger APIs;
all exchange is through local JSON and Markdown files.

## Key files

- `specweave/integrations/taskledger.py` (184 lines) — task-BDD JSON import,
  evidence JSON export, `task_id_from_report()`
- `specweave/integrations/archledger.py` — candidate markdown rendering from
  feature + `@bdd-*`
- `specweave/integrations/combi.py` — `run_combi_check()` cross-ledger audit

## Interfaces

- **Inbound:** CLI `archledger`, `behavior import-taskledger`, `combi check`, `trace`
- **Outbound:** Writes JSON (Taskledger) and Markdown (Archledger) to filesystem
- **Boundary:** Never imports Taskledger or Archledger as Python packages

# Runtime View

## Brownfield workflow (tests → specs → evidence)

```text
Developer          SpecWeave CLI              Filesystem
   │                     │                        │
   │ specweave init      │                        │
   │────────────────────►│ create .specweave.toml │
   │                     │───────────────────────►│
   │                     │                        │
   │ specweave create    │                        │
   │   gherkin           │                        │
   │   --from-tests      │ AST-read tests/*.py    │
   │────────────────────►│───────────────────────►│
   │                     │ generate .feature   │
   │                     │───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   check             │ lint .feature files │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   index             │ write README + manifest│
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   generate-tests    │ write test_*.py files  │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ pytest              │                        │
   │─────────────────────────────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   import-report     │ read JUnit XML         │
   │────────────────────►│───────────────────────►│
   │                     │ write evidence JSON    │
   │                     │───────────────────────►│
```

## New-feature workflow (spec-first)

```text
Developer          SpecWeave CLI              Filesystem
   │                     │                        │
   │ specweave create    │                        │
   │   feature           │                        │
   │   --area --title    │ generate .feature   │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ specweave behavior  │                        │
   │   generate-tests    │ write test_*.py        │
   │────────────────────►│───────────────────────►│
   │                     │                        │
   │ (implement tests)   │                        │
   │─────────────────────────────────────────────►│
```

## Report normalization flow

1. External runner (pytest with `--junitxml`) writes native XML to
   `reports/behavior/`.
2. `specweave report normalize` parses the XML via
   `specweave/reports/junit_xml.py`, maps scenario results to `@bdd-*` tags,
   rolls up acceptance criteria via `@ac-*`.
3. Non-passed scenarios fail the report. Missing expected `@ac-*` coverage
   fails the report.
4. Output: normalized JSON or Taskledger evidence JSON to
   `specs/behavior/evidence/`.



<!-- archledger: no accepted records for this section yet -->

# Deployment View

## Deployment model

SpecWeave is a single Python package deployed to a developer's environment via
`pip install specweave`. It has no server component.

```text
┌──────────────────────────────────────────┐
│          Developer Workstation            │
│                                          │
│  ┌──────────────┐   ┌────────────────┐  │
│  │ specweave CLI │   │ Python ≥3.10   │  │
│  │ (pip install) │   │ (venv/system)  │  │
│  └──────┬───────┘   └────────────────┘  │
│         │ invokes                        │
│  ┌──────▼───────┐                        │
│  │    pytest     │ (external, already     │
│  │              │  installed in venv)     │
│  └──────────────┘                        │
│                                          │
│  Project checkout:                       │
│    .specweave.toml                       │
│    specs/behavior/features/              │
│    tests/                                │
│    reports/behavior/                     │
│    .specweave/                           │
└──────────────────────────────────────────┘
```

## Artifact layout

```text
.specweave.toml              # config (hidden, preferred)
specweave.toml               # config (public alternative)
specs/behavior/
  README.md                  # generated index
  features/<area>/*.feature
  manifest.json              # generated manifest
tests/test_<area>_<feature>.py
reports/behavior/*.xml       # native runner output
.specweave/
  evidence/*.json            # normalized evidence
  reports/*.json             # report state
  mappings/taskledger/*.json # Taskledger exchange
skills/specweave/SKILL.md    # agent skill (not packaged)
```

## CI integration

SpecWeave runs in CI as a CLI step after `pytest --junitxml=...`:

```bash
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report reports/behavior/pytest-junit.xml --format junit-xml
```

No special CI plugin, Docker image, or hosted service is required.



<!-- archledger: no accepted records for this section yet -->

# Cross-cutting Concepts

## Tag-based traceability

All scenario identity and acceptance-criteria linkage is tag-based:

| Tag prefix   | Purpose                   | Used by              |
| ------------ | ------------------------- | -------------------- |
| `@bdd-*`     | Stable scenario identity  | validation, evidence |
| `@ac-*`      | Acceptance criterion link | coverage, reporting  |
| `@task-*`    | Task exchange metadata    | Taskledger exchange  |
| `@rule-*`    | Rule exchange metadata    | Taskledger exchange  |
| `@area-*`    | Feature area grouping     | index, coverage      |
| `@feature-*` | Feature identity tag      | index, lint          |

Scenario titles are display/debug text only. Title matching is never used for
validation — only as a review hint with explicit uncertainty.

## Fail-closed evidence

Report normalization (`specweave/reports/normalize.py`) treats every non-passed
scenario status as blocking:

- `failed`, `undefined`, `pending`, `ambiguous` → always fail the report
- `skipped` → fails unless `--allow-skipped` is explicitly set
- Missing expected `@ac-*` → fails
- Unlinked scenarios → do not count toward acceptance criteria
- Clean command exit code alone → never sufficient evidence

## Frozen dataclass models

All public models are frozen dataclasses (`frozen=True`):

- Gherkin: `Feature`, `Rule`, `Scenario`, `Step`
- Reports: `ScenarioResult`, `CriterionResult`, `NormalizedBddReport`
- BDD: `TaskBddSpec`, `BddRule`, `BddExample`
- Config: `SpecWeaveConfig`, `SpecWeavePaths`, `SpecWeaveGherkin`, etc.

## Deterministic output

- TOML config rendering is deterministic (`specweave/config.py`).
- JSON output is sorted and indented consistently (`json.dumps(sort_keys=True)`).
- Feature files are written deterministically from models.
- Test names are derived deterministically from scenario titles via slugification.

## Dual Gherkin format

SpecWeave supports both `.feature` (classic Gherkin) and `.feature`
(Markdown-embedded Gherkin, the default). The `convert` command bridges
between formats. The Markdown parser is in `specweave/gherkin/markdown.py`.



<!-- archledger: no accepted records for this section yet -->

# Architecture Decisions

## AD-1: Tag-based identity, not title-based

**Context:** Scenario titles change frequently during editing. Using them as
validation keys would cause false negatives.

**Decision:** Anchor all validation on `@bdd-*` tags. Use `@ac-*` for
acceptance-criteria linkage. Titles are display-only.

**Consequences:** Stable validation across renames. Requires discipline to
maintain tags, but this is enforced by `require_bdd_ids = true` in config.

## AD-2: Plain pytest as the canonical enforcement path

**Context:** Existing BDD tools in Python (pytest-bdd, behave) couple tests to
step-definition modules and require framework-specific boilerplate.

**Decision:** Generate standard `test_*.py` files with `@specweave` markers and
source-mapping comments. No step definitions required.

**Consequences:** Lower barrier to adoption. Tests are runnable without
SpecWeave installed. But SpecWeave-specific markers are needed for static
coverage checks.

## AD-3: AST-based test discovery, not execution

**Context:** Inferring behavior from existing tests could be done by running
them and inspecting results, or by static analysis.

**Decision:** Use Python AST parsing (`specweave/python_inspect/ast_reader.py`)
to discover tests. Never execute tests during discovery.

**Consequences:** Fast, deterministic, safe. But inferred Gherkin may miss
runtime-only behavior.

## AD-4: Fail-closed report normalization

**Context:** BDD evidence must be reliable for acceptance decisions.

**Decision:** Every non-passed status blocks. Missing scenarios block. Missing
acceptance criteria block. Exit code alone is insufficient.

**Consequences:** High confidence in "passed" evidence. May require teams to
explicitly allow skipped tests or address flaky suites.

## AD-5: File-based Taskledger/Archledger integration

**Context:** SpecWeave needs to exchange data with Taskledger and Archledger but
must not become coupled to their internals.

**Decision:** JSON file exchange. SpecWeave reads task-BDD JSON and writes
evidence JSON. No runtime dependency on either tool.

**Consequences:** Clean boundaries. SpecWeave can run without Taskledger or
Archledger installed. Exchange format changes require coordination.

## AD-6: Markdown .feature as default format

**Context:** Classic `.feature` files have no native Markdown support, making
them harder to read in GitHub, IDEs, and agent contexts.

**Decision:** Default to `.feature` with embedded Gherkin inside Markdown
code fences. Support classic `.feature` as a first-class alternative.

**Consequences:** Better readability in modern tooling. Requires a Markdown
parser alongside the standard Gherkin parser. The `convert` command bridges
formats.

## AD-7: Optional gherkin-official dependency

**Context:** `gherkin-official` (the Cucumber reference parser) was previously
listed as a required runtime dependency. However, SpecWeave's built-in parser
and subset validator (`specweave/gherkin/validation.py`) cover the canonical
subset without external help. Only users needing full Cucumber Gherkin
compatibility require the official parser.

**Decision:** Move `gherkin-official` to an optional extra
(`pip install specweave[gherkin]`). The adapter in
`specweave/gherkin/official.py` lazy-imports the library and raises a clear
error when it is not installed. The core SpecWeave workflow (parse, lint,
generate, convert, validate) works without it.

**Consequences:** Smaller default install footprint. Users who need full
Cucumber compatibility opt in explicitly. The built-in subset validator
catches unsupported constructs (Background, Scenario Outline, tables, doc
strings) without any external dependency.


## Tag-based scenario identity

**Status:** proposed
**Date:** 2026-06-08
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

Scenario titles change frequently during editing. Using them as validation
keys would cause false negatives in evidence mapping and coverage checks.
Teams need stable identifiers that survive renames, restructuring, and
translation between formats.

## Decision

Anchor all validation on `@bdd-*` tags. Use `@ac-*` for acceptance-criteria
linkage. Scenario titles are display/debug text only.

Enforced by `require_bdd_ids = true` in config and by lint checks in
`specweave/gherkin/lint.py`.

## Consequences

- **Positive:** Deterministic, rename-safe validation. Evidence mapping works
  across format conversions and language changes.
- **Negative:** Teams must maintain tags manually. Missing or duplicate tags
  are lint errors.

## Alternatives considered

- Title-based matching: rejected — fragile, causes false negatives on renames.
- UUID-based IDs: rejected — less human-readable in Gherkin source.


## Classic `.feature` is the canonical behavior format

**Status:** accepted
**Date:** 2026-06-09
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

SpecWeave previously supported both classic Gherkin `.feature` and Markdown-embedded `.feature.md` as behavior spec formats. Maintaining two parser and writer paths adds complexity for humans, tools, and coding agents.

## Decision

Use classic Gherkin `.feature` files as the only canonical behavior-spec format in SpecWeave.

Durable SpecWeave-owned JSON artifacts live under `specs/behavior/`:

- `specs/behavior/evidence`
- `specs/behavior/mappings`

Generated runner output lives under:

- `reports/behavior`
- `reports/behavior/specweave`

## Alternatives considered

- Continue supporting `.feature.md` alongside `.feature`: rejected — two parser and writer paths add maintenance burden without sufficient benefit.
- Migrate `.feature.md` to a separate plugin: rejected — not enough usage to justify the indirection.
## Consequences

- legacy `.feature.md` files are not canonical and are rejected
- `specweave.toml` is the default config file
- `.specweave.toml` remains a compatibility discovery path for existing
  projects


## Plain pytest as canonical enforcement

**Status:** proposed
**Date:** 2026-06-08
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

Existing Python BDD tools (pytest-bdd, behave) couple tests to
step-definition modules and require framework-specific boilerplate. This
creates a barrier to adoption and makes tests dependent on BDD infrastructure.

## Decision

Generate standard `test_*.py` files with `@specweave` markers and
source-mapping comments (`# specweave: scenario=...`). No step definitions
required. Tests are runnable without SpecWeave installed.

## Consequences

- **Positive:** Lower barrier to adoption. Tests work with standard pytest.
  SpecWeave is a development tool, not a test framework dependency.
- **Negative:** Static coverage checks require SpecWeave-specific markers.
  Teams using pytest-bdd or behave need the bridge/legacy path.

## Alternatives considered

- pytest-bdd as canonical: rejected — adds runtime dependency and step-module coupling.
- behave as canonical: rejected — different test runner, more coupling.


## AST-based test discovery

**Status:** proposed
**Date:** 2026-06-08
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

Brownfield projects have existing pytest tests that describe behavior
implicitly. SpecWeave needs to infer Gherkin specs from these tests without
requiring manual rewriting.

## Decision

Use Python `ast` module to parse test files statically. Extract test function
names, docstrings, markers, and assert statements. Never execute tests during
discovery.

## Consequences

- **Positive:** Fast, deterministic, safe. Works on any Python file without
  imports or execution. No side effects.
- **Negative:** Cannot capture runtime-only behavior. Inferred Gherkin may be
  low quality for poorly named tests. Marked with `@generated` and
  `@needs-review` tags.

## Alternatives considered

- Runtime introspection: rejected — slow, side effects, non-deterministic.
- Manual spec writing only: rejected — defeats the brownfield workflow purpose.


## Fail-closed evidence normalization

**Status:** proposed
**Date:** 2026-06-08
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

BDD evidence is used for acceptance decisions. If the normalization layer
is lenient, teams may accept incomplete or misleading evidence.

## Decision

Every non-passed scenario status (failed, skipped, pending, undefined,
ambiguous, missing, unlinked) blocks the report. Missing expected `@ac-*`
coverage blocks. A clean command exit code alone is never sufficient evidence.

## Consequences

- **Positive:** High confidence in "passed" evidence. No false positives in
  acceptance decisions.
- **Negative:** May require teams to explicitly address skipped tests or
  flaky suites before evidence passes.

## Alternatives considered

- Fail-open (only hard failures block): rejected — undermines evidence trust.
- Configurable per-status defaults: rejected — too easy to weaken by accident.


## File-based Taskledger and Archledger integration

**Status:** proposed
**Date:** 2026-06-08
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

SpecWeave needs to exchange data with Taskledger (task lifecycle, plans,
acceptance criteria) and Archledger (architecture records) but must not
become coupled to their internals or require their installation.

## Decision

All integration is file-based JSON and Markdown exchange. SpecWeave reads
task-BDD JSON and writes evidence JSON for Taskledger. It renders candidate
Markdown for Archledger. Neither tool is a Python dependency.

## Consequences

- **Positive:** Clean boundaries. SpecWeave runs independently. No version
  coupling with external tools.
- **Negative:** Format changes in Taskledger or Archledger require coordinated
  updates. No runtime validation against external tool schemas.

## Alternatives considered

- Direct API integration: rejected — tight coupling, version fragility.
- Shared database: rejected — violates the "no database" constraint.


## Make gherkin-official an optional dependency

**Status:** proposed
**Date:** 2026-06-09
**Deciders:** 
**Supersedes:** 
**Related:** 

## Context

SpecWeave bundles a built-in Gherkin parser (`specweave/gherkin/parser.py`) that
covers the SpecWeave canonical subset: Feature, Rule, Scenario/Example, and
Given/When/Then/And/But steps. A subset validator
(`specweave/gherkin/validation.py`) rejects unsupported constructs (Background,
Scenario Outline, data tables, doc strings, wildcard `*` steps) without any
external dependency.

The Cucumber reference parser `gherkin-official` provides full Gherkin
compatibility but is not needed for SpecWeave's canonical workflow. Requiring it
as a runtime dependency increases the install footprint for all users.

## Decision

Move `gherkin-official` to an optional extra (`pip install specweave[gherkin]`).
The adapter in `specweave/gherkin/official.py` lazy-imports the library and
raises a clear `ParseError` when it is not installed. The core SpecWeave
workflow (parse, lint, generate, convert, validate) works without it.

## Consequences

- **Positive:** Smaller default install. Only two required runtime dependencies
  (typer, click). Users needing full Cucumber compatibility opt in explicitly.
- **Positive:** The subset validator catches unsupported constructs without
  external dependencies, giving deterministic error messages.
- **Negative:** Users who relied on `gherkin-official` being installed
  automatically must now install `specweave[gherkin]` explicitly.

## Alternatives considered

- Keep `gherkin-official` required: rejected — inflates the dependency tree for
  users who only need the canonical subset.
- Bundle a vendored copy: rejected — maintenance burden, version drift.
- Bundle a vendored copy: rejected — maintenance burden, version drift.

# Quality Requirements

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
- **Minimal dependencies.** Only typer and click at runtime. `gherkin-official`
  is optional (`specweave[gherkin]`) and only needed for the official parser
  backend.



## Quality Requirements Overview

<!-- archledger: no accepted records for this section yet -->

## Quality Scenarios

<!-- archledger: no accepted records for this section yet -->

# Risks and Technical Debt

## Risks

1. **Tag discipline required.** If teams neglect `@bdd-*` tags, static
   coverage and evidence mapping break. Mitigated by `require_bdd_ids = true`
   and lint enforcement.

2. **Dual format complexity.** Supporting both `.feature` and `.feature`
   doubles the parser surface. The `convert` command and `gherkin/markdown.py`
   must stay in sync with the classic parser.

3. **Brownfield inference quality.** AST-based test discovery may produce
   low-quality Gherkin from poorly named tests. Marked with `@generated` and
   `@needs-review` tags to flag human review.

4. **Cross-tool format drift.** Taskledger and Archledger JSON shapes may
   evolve independently. SpecWeave must track compatible shapes without
   coupling to their internals.

5. **Report format coverage.** Only `junit-xml` and `cucumber-json` report
   formats are supported. Projects using other runners (e.g., `pytest-cucumber`)
   may need adapter work.

## Technical debt

1. **Bridge/legacy commands.** `bdd export`, `bdd import-feature`,
   `report normalize`, `archledger`, `draft`, `bind`, and `run` are legacy or
   bridge commands. They must stay working but should not grow new features.

2. **Compatibility aliases.** `bdd check`, `bdd index`, `bdd generate-tests`,
   and `bdd coverage` are aliases for `behavior` commands. They add CLI
   surface area without new functionality.

3. **Backends module.** `specweave/backends/behave.py` and
   `specweave/backends/pytest_bdd.py` generate step-definition skeletons for
   non-canonical workflows. These may lag behind the canonical path.

4. **Config backward compatibility.** Constants like `FEATURES_DIR`,
   `BDD_INDEX_PATH`, `BDD_MANIFEST_PATH` in `specweave/config.py` are
   compatibility aliases that older code paths rely on.

## Risk Overview

<!-- archledger: no accepted records for this section yet -->

# Glossary

| Term                 | Definition                                                                  |
| -------------------- | --------------------------------------------------------------------------- |
| Behavior spec        | A Gherkin `.feature` or `.feature` file describing expected behavior        |
| Canonical layout     | The default directory structure: `specs/behavior/features/`, `tests/`, etc. |
| Brownfield workflow  | Generating specs from existing pytest tests (tests → specs)                 |
| New-feature workflow | Writing specs first, then generating test skeletons (spec → tests)          |
| `@bdd-*` tag         | Stable scenario identity tag used for validation traceability               |
| `@ac-*` tag          | Acceptance criterion linkage tag                                            |
| `@task-*` tag        | Task exchange metadata tag (Taskledger)                                     |
| `@rule-*` tag        | Rule exchange metadata tag (Taskledger)                                     |
| Fail-closed          | Evidence normalization that treats every non-passed status as blocking      |
| Plain pytest         | Standard `test_*.py` files without pytest-bdd or behave dependencies        |
| Manifest             | `specs/behavior/manifest.json` — generated index of all features/scenarios  |
| Evidence JSON        | Normalized test execution evidence in `specs/behavior/evidence/`            |
| Task-BDD JSON        | Portable BDD representation used for Taskledger exchange                    |
| Feature Markdown     | `.feature` format — Gherkin embedded in Markdown code fences                |
| Source mapping       | `@specweave` markers and comments in generated tests linking to scenarios   |
| Building block       | A top-level architectural module or subsystem within SpecWeave              |
| Archledger           | External tool that owns durable architecture and specification records      |
| Taskledger           | External tool that owns task lifecycle, plans, and acceptance criteria      |
| Combi check          | Cross-ledger integration audit without mutating external ledgers            |

<!-- archledger: no accepted records for this section yet -->
