# AGENTS.md

This file defines how coding agents should work in the `specweave` repository.

`specweave` is a Python CLI and library for weaving together canonical Gherkin behavior specifications, plain pytest enforcement, generated skeletons, and normalized BDD/test execution evidence. Its core contract is: keep behavior intent readable, keep executable validation traceable, and fail closed when evidence is incomplete or ambiguous.

SpecWeave is not Taskledger, Archledger, or CI. It may exchange files with those tools, but it must not become their durable state owner.

## 1. Communication

- Assume the user is technically strong.
- Be direct, concrete, and brief.
- Do not explain obvious Python, Typer, TOML, dataclass, pytest, ruff, mypy, packaging, or Gherkin basics.
- Do not narrate trivial edits.
- Push back when a request would weaken traceability, fail-closed evidence behavior, stable IDs, JSON contracts, config semantics, or public APIs.
- Ask a clarifying question only when ambiguity is likely to cause the wrong behavior or an irreversible contract change.
- Otherwise, proceed with the smallest correct change.
- Report results as: changed, verified, not verified, risks.

## 2. Operating Principles

### 2.1 Prefer the smallest correct change

Priorities:

1. behavior/spec traceability is correct
2. validation evidence fails closed
3. canonical layout is preserved
4. behavior is verified with focused tests
5. intent is obvious in code
6. changes stay in the owning layer
7. CLI and public API contracts stay stable unless explicitly changed

Avoid:

- speculative abstractions
- broad rewrites during feature work
- unrelated formatting or cleanup
- casual command, flag, status, field, path, tag, or JSON shape changes
- weakening `@bdd-*`, `@ac-*`, `@task-*`, or `@rule-*` mapping semantics
- treating scenario titles as durable validation keys
- reintroducing legacy canonical layouts
- adding Taskledger or Archledger as runtime dependencies
- adding migration code unless requested
- creating commits

### 2.2 Treat behavior specs and evidence as product data

Preserve these invariants:

- `specs/behavior/features/` is the default canonical behavior spec tree.
- `specs/behaviour/features/` is supported through spelling configuration and must not drift.
- One `.feature` file should represent one behavior feature.
- Feature files should be grouped by area.
- Scenario/example identity is tag-based, primarily `@bdd-*`.
- Acceptance-criterion linkage is tag-based, primarily `@ac-*`.
- Scenario titles are display/debug text only.
- Plain pytest under `tests/` is the default executable enforcement path.
- JUnit/Cucumber/runner outputs are evidence inputs, not durable truth by themselves.
- `.specweave/` stores generated state, reports, evidence, and mappings; do not treat it as the canonical behavior source.
- `specs/behavior/manifest.json` and `specs/behavior/README.md` are generated/index outputs and should be reproducible.
- Manual feature edits must be preserved unless the user explicitly requests overwrite/force.

### 2.3 Work as a verifiable loop

For each task:

1. identify the owned layer
2. make the smallest coherent change
3. add or update focused tests
4. run the narrowest useful verification
5. widen verification only when the change crosses layers

Examples:

- Gherkin grammar bug -> `specweave/gherkin/parser.py`, `specweave/gherkin/writer.py`, or `specweave/gherkin/model.py` plus parser/writer tests
- behavior index bug -> `specweave/behavior/index.py` plus CLI/index tests
- static coverage bug -> `specweave/behavior/coverage.py` plus coverage tests
- report import bug -> `specweave/behavior/reporting.py`, `specweave/reports/*.py`, and report tests
- pytest discovery/mapping bug -> `specweave/python_inspect/ast_reader.py` plus Python inspection tests
- pytest-to-Gherkin bug -> `specweave/translate/pytest_to_gherkin.py` plus translation tests
- feature-to-test skeleton bug -> `specweave/behavior/generate.py` or `specweave/translate/spec_to_code.py` plus generation tests
- config/init bug -> `specweave/config.py`, `specweave/init.py`, `specweave/doctor.py` plus config/init/doctor tests
- CLI contract bug -> `specweave/cli.py`, `specweave/cli_context.py`, or `specweave/launcher.py` plus CLI and CLI JSON tests
- Taskledger exchange bug -> `specweave/integrations/taskledger.py` plus integration/task draft tests
- Archledger candidate bug -> `specweave/integrations/archledger.py` plus Archledger candidate tests
- docs or skill drift -> `README.md`, `skills/specweave/SKILL.md`, `specs/*/README.md`, and command example tests where present

## 3. Project Shape

### 3.1 What SpecWeave is

SpecWeave provides:

- `specweave init` project initialization
- config discovery/loading from `.specweave.toml` or `specweave.toml`
- canonical behavior specs under `specs/behavior/features/`
- optional British spelling layout under `specs/behaviour/features/`
- Gherkin model/parser/writer/linter support
- translation from existing pytest tests to draft Gherkin features
- generation of plain pytest skeletons from Gherkin features
- behavior index and manifest generation
- static behavior coverage checks
- pytest/JUnit evidence import
- Cucumber JSON and JUnit XML normalization
- fail-closed mapping from scenario results to acceptance criteria
- optional Taskledger file exchange
- Archledger candidate markdown generation
- legacy bridge commands for older BDD experiments

It does not provide:

- task lifecycle state
- user approval gates
- architecture-record persistence
- CI orchestration
- JavaScript/Java Cucumber skeleton generation
- a requirement to use `pytest-bdd`, `behave`, or step-definition modules for the canonical workflow

### 3.2 Canonical layout

Preserve the default layout:

```text
.specweave.toml
specs/behavior/README.md
specs/behavior/features/<area>/<feature>.feature
specs/behavior/manifest.json
tests/test_<area>_<feature>.py
reports/behavior/*.xml
.specweave/reports/*.json
.specweave/evidence/*.json
.specweave/mappings/taskledger/*.json
```

Also preserve the public-config variant:

```text
specweave.toml
```

Also preserve the British spelling variant:

```text
specs/behaviour/README.md
specs/behaviour/features/<area>/<feature>.feature
specs/behaviour/manifest.json
reports/behaviour/*.xml
```

Do not steer canonical docs or examples toward these legacy/bridge-only layouts:

```text
tests/bdd/features/
specs/bdd/features/
tests/behavior/
tests/behaviour/
pytest-bdd step-module-first layouts
```

Step-definition modules may still exist for `bind`/backend compatibility, examples, or legacy bridge tests. They are not the canonical behavior workflow.

### 3.3 Brownfield workflow

The intended brownfield flow is:

```bash
specweave init
specweave doctor
specweave create gherkin --from-tests tests --out specs/behavior/features
specweave review specs
specweave behavior index
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report reports/behavior/pytest-junit.xml --format junit-xml
```

When generating specs from existing tests:

- group by file unless the user explicitly changes grouping
- put area subdirectories under `specs/behavior/features/<area>/`
- create one `.feature` per inferred feature
- include generated/needs-review tags as configured
- preserve existing manual feature files by default
- require stable `@bdd-*` IDs for validation traceability
- mark generated specs as draft/needs-review when the source is inferred from tests

### 3.4 New behavior workflow

For a new feature request, prefer:

```bash
specweave create feature \
  --area <area> \
  --title "<Feature title>" \
  --scenario "<Scenario title>" \
  --given "<precondition>" \
  --when "<action>" \
  --then "<observable outcome>"
```

Then generate implementation planning artifacts only after the feature exists:

```bash
specweave create plan --feature specs/behavior/features/<area>/<feature>.feature --out plan.md
specweave create taskledger-task --feature specs/behavior/features/<area>/<feature>.feature
```

Do not make SpecWeave approve a Taskledger plan, validate a Taskledger task, or persist an Archledger architecture record. It may generate drafts/candidates for those tools.

## 4. Important Code Surfaces

Use the owning layer before editing.

- `specweave/cli.py` — root Typer app, command groups, root `--config`, root `--json`, command output behavior
- `specweave/cli_context.py` — CLI context construction and JSON-output flag handling
- `specweave/config.py` — config dataclasses, discovery, defaults, TOML loading, default config rendering
- `specweave/init.py` — `specweave init`, managed README detection, layout creation, dry-run/force behavior
- `specweave/doctor.py` — project/config/layout diagnostics and `--fix`
- `specweave/review.py` — spec review findings for missing bindings and needs-review state
- `specweave/gherkin/model.py` — Feature/Rule/Scenario/Step data contracts
- `specweave/gherkin/parser.py` — Gherkin parsing
- `specweave/gherkin/writer.py` — Gherkin serialization
- `specweave/gherkin/tags.py` — tag parsing/filtering helpers
- `specweave/gherkin/lint.py` — feature collection, canonical path checks, scenario linting, duplicate ID checks
- `specweave/behavior/common.py` — shared behavior paths, slugs, feature identity, scenario IDs, generated test names
- `specweave/behavior/generate.py` — plain pytest skeleton generation from canonical features
- `specweave/behavior/index.py` — behavior README and manifest generation
- `specweave/behavior/coverage.py` — static mapping/coverage checks
- `specweave/behavior/reporting.py` — pytest/JUnit report import and evidence mapping through the manifest
- `specweave/python_inspect/ast_reader.py` — pytest scenario extraction and SpecWeave binding discovery
- `specweave/python_inspect/assertions.py` — assertion-to-plain-English rendering
- `specweave/translate/pytest_to_gherkin.py` — brownfield pytest-to-Gherkin generation
- `specweave/translate/spec_to_code.py` — feature drafting and step/backend binding helpers
- `specweave/translate/code_to_spec.py` — test explanation helpers
- `specweave/backends/*.py` — behave and pytest-bdd skeleton generation
- `specweave/bdd/*.py` — Task-BDD JSON model, store, and feature conversion
- `specweave/reports/cucumber_json.py` — Cucumber JSON parsing
- `specweave/reports/junit_xml.py` — JUnit XML parsing
- `specweave/reports/mapping.py` — tag-based trace extraction and acceptance coverage summarization
- `specweave/reports/normalize.py` — normalized report and Taskledger-compatible evidence JSON
- `specweave/reports/model.py` — report/result dataclasses and status values
- `specweave/runners/command.py` — subprocess runner delegation
- `specweave/runners/reports.py` — runner summary writing
- `specweave/integrations/taskledger.py` — file-based Taskledger exchange
- `specweave/integrations/archledger.py` — Archledger candidate markdown rendering
- `specweave/errors.py` — public exception taxonomy
- `specweave/__main__.py`, `specweave/launcher.py` — entrypoints
- `specweave/py.typed` — typed package marker
- `skills/specweave/SKILL.md` — external agent skill protocol
- `README.md` — canonical user-facing workflow
- `pyproject.toml` — package metadata, dependencies, test/mypy config
- `.ruff.toml` — lint/format config
- `tests/` — focused behavior and contract tests

## 5. CLI Contract

### 5.1 Current command families

Preserve the registered command families:

```text
specweave init
specweave doctor
specweave version
specweave explain PATH...
specweave behavior check
specweave behavior index
specweave behavior generate-tests
specweave behavior coverage
specweave behavior import-report
specweave behavior import-taskledger
specweave bdd check
specweave bdd index
specweave bdd generate-tests
specweave bdd coverage
specweave bdd export
specweave bdd import-feature
specweave report normalize
specweave report inspect
specweave review specs
specweave create gherkin
specweave create feature
specweave create plan
specweave create taskledger-task
specweave update
specweave archledger
specweave draft
specweave bind
specweave run
```

`behavior` is the canonical command family. `bdd check`, `bdd index`, `bdd generate-tests`, and `bdd coverage` are compatibility aliases for the behavior workflow.

`draft`, `bind`, `run`, `bdd export`, `bdd import-feature`, `report normalize`, and `archledger` are bridge/legacy/support commands. Keep them working unless explicitly removed, but do not make them the recommended canonical workflow without updating README, skill docs, tests, and examples together.

### 5.2 Root options

Preserve root options:

```text
--config PATH
--json
```

Rules:

- `--config` must select an explicit config path.
- Config discovery must continue to prefer `.specweave.toml` over `specweave.toml` when both exist at the same level.
- Config discovery must continue walking parent directories.
- `--json` must remain a root-level machine-readable output contract.
- Do not force machine consumers to parse human text.
- Test JSON payload shape and exit code together.

### 5.3 Human output

Human output should stay concise and stable. Do not casually change line order, labels, status words, or wording that tests or agents may rely on.

### 5.4 Exit behavior

Preserve failure semantics:

- lint/check failures should exit non-zero when findings are errors
- coverage failures should exit non-zero when required mappings/evidence are missing
- report normalization should exit non-zero for failed/fail-closed reports
- unsupported backends should produce clear errors
- missing files/configured paths should produce clear diagnostics

## 6. Config and Initialization Contracts

### 6.1 Config files

Supported config files:

```text
.specweave.toml
specweave.toml
```

Preserve default rendered config shape:

```toml
schema_version = 1
project_root = "."
spelling = "behavior"

[paths]
specs_root = "specs/behavior"
features_dir = "specs/behavior/features"
behavior_readme = "specs/behavior/README.md"
manifest = "specs/behavior/manifest.json"
tests_dir = "tests"
reports_dir = "reports/behavior"
state_dir = ".specweave"
evidence_dir = ".specweave/evidence"
reports_state_dir = ".specweave/reports"
mapping_dir = ".specweave/mappings"

[pytest]
test_globs = ["tests/test_*.py", "tests/**/*_test.py"]
ignore_globs = [".venv/**", "build/**", "dist/**"]

[gherkin]
dialect = "en"
default_scenario_keyword = "Example"
require_given_when_then = true
require_bdd_ids = true
id_style = "slug"
include_generated_tag = true
include_needs_review_tag = true
canonical_task_tags = false

[generation]
group_by = "file"
mode = "create"
preserve_manual_edits = true
mark_generated_from_tests = true

[commands]
test = "pytest --junitxml=reports/behavior/pytest-junit.xml"

[agent]
json_default = false
```

Rules:

- keep paths relative by default
- reject unsupported schema versions
- normalize path values consistently
- do not silently change the default spelling
- do not silently change generated output directories
- update `tests/test_config.py` and `tests/test_init.py` for any config/init change

### 6.2 Init behavior

`specweave init` should:

- create `.specweave.toml` by default
- create `specweave.toml` with `--public-config`
- create the configured behavior specs root
- create a managed `README.md` in the behavior specs root
- support `--spelling behavior`
- support `--spelling behaviour`
- be idempotent
- refuse to overwrite non-managed README content
- overwrite generated config/readme only with explicit `--force`
- support `--dry-run` without writing files
- report created/existing/skipped paths clearly
- support JSON output through root `--json`

Do not make `init` import tests, generate feature files, run pytest, or contact Taskledger/Archledger. Initialization only prepares SpecWeave configuration and layout.

## 7. Gherkin and Behavior Contracts

### 7.1 Canonical Gherkin shape

Prefer this shape:

```gherkin
@feature-slug
Feature: Feature title

  Rule: Optional business rule

    @bdd-feature-scenario @ac-0001
    Example: Scenario title
      Given an explicit precondition
      When a user-visible action happens
      Then an observable outcome is true
```

Rules:

- use `Feature`, optional `Rule`, and `Scenario`/`Example`
- keep one feature per file
- group features by area
- preserve descriptions when parsing and writing
- preserve tags when parsing and writing
- parse and write multiple tags on one line
- parse and write `Rule:` blocks
- preserve top-level scenarios outside rules
- preserve `Given`, `When`, `Then`, `And`, and `But`
- require Given/When/Then when configured
- require stable `@bdd-*` IDs when configured

### 7.2 Tags and matching

Trace matching rules:

1. match by `@bdd-*` first
2. map acceptance criteria by `@ac-*`
3. use `@task-*` only as task exchange metadata
4. use `@rule-*` only as rule exchange metadata
5. use titles only for display/debugging

Do not implement title-only matching for validation. Title matching may be used only as a review hint with explicit uncertainty.

### 7.3 Generated specs from tests

When converting pytest to Gherkin:

- use AST-based discovery; do not execute tests to infer behavior
- derive feature/area names deterministically from file paths
- generate deterministic slug-style scenario IDs
- mark generated specs as generated/needs-review when configured
- include meaningful Given/When/Then text from test names, docstrings, comments, markers, or assertions when available
- preserve existing generated IDs when updating
- preserve manual files unless `--force` is explicitly used
- do not overwrite hand-written feature files by default

### 7.4 Generated tests from specs

When generating plain pytest skeletons:

- keep executable enforcement under `tests/`
- include SpecWeave source mapping markers or metadata that static coverage can discover
- derive canonical test paths from feature paths
- produce focused test functions with stable, readable names
- preserve existing hand-written tests unless explicitly requested
- avoid forcing `pytest-bdd` or `behave` into the canonical path

## 8. Report and Evidence Contracts

### 8.1 Fail closed

Fail closed. Do not mark behavior or acceptance criteria as passed when a linked native result is:

- failed
- errored
- skipped
- pending
- undefined
- ambiguous
- missing
- unlinked
- only implied by process exit code

A passing command exit code is not sufficient evidence when a native report is available or expected.

### 8.2 Native report normalization

Preserve support for:

```text
cucumber-json
junit-xml
```

Normalized reports should preserve:

- scenario name
- status
- tags
- duration when available
- evidence/source path when available
- command source when supplied
- acceptance-criterion coverage summary
- overall status

### 8.3 Acceptance coverage

Rules:

- only scenarios linked by `@bdd-*` and/or `@ac-*` should count toward criterion evidence
- unlinked scenarios do not satisfy acceptance criteria
- each required `@ac-*` must have at least one passing linked scenario
- missing expected acceptance criteria must fail
- failed sibling scenarios for the same criterion must keep the criterion failed unless explicitly supported otherwise
- skipped/pending/undefined/ambiguous/error states are blocking unless `allow_skipped` or an equivalent explicit option applies where already supported and tested

### 8.4 Evidence files

Generated evidence belongs under:

```text
.specweave/evidence/
.specweave/reports/
reports/behavior/
```

Do not make `.feature` files or pytest source files depend on evidence files to parse. Evidence should be importable and regenerable.

## 9. Integration Boundaries

### 9.1 Taskledger

Taskledger owns:

- task lifecycle
- plans
- acceptance criteria as task state
- user approval/waiver decisions
- validation state
- durable task evidence records

SpecWeave owns:

- behavior feature files
- conversion between task-BDD JSON and Gherkin
- normalized BDD/test evidence JSON
- file-based imports/exports for Taskledger
- draft Taskledger task payloads from features

Rules:

- do not add Taskledger lifecycle commands to SpecWeave
- do not require Taskledger as a Python dependency
- do not store canonical behavior only inside Taskledger state
- do not let SpecWeave approve plans or waive validation
- keep Taskledger exchange file-based and explicit
- preserve Taskledger-compatible evidence shape when changing report models
- update `tests/test_integration_taskledger.py` and `tests/test_taskledger_draft.py` for changes

### 9.2 Archledger

Archledger owns durable architecture/spec records.

SpecWeave may:

- render candidate markdown from a feature and `@bdd-*`
- include behavior lines, tags, and source references
- write candidate files when explicitly requested

SpecWeave must not:

- create accepted Archledger records by default
- mutate Archledger state implicitly
- turn every behavior spec into an architecture record
- hide missing `@bdd-*` or unknown scenario errors

Update `tests/test_archledger_candidate.py` for changes.

### 9.3 Cucumber and external runners

SpecWeave delegates execution. It may run commands and collect outputs, but it is not a Cucumber implementation or CI runner.

Rules:

- keep `specweave run` as external command delegation
- capture stdout/stderr/summary paths predictably
- do not infer pass/fail solely from stdout prose
- prefer native reports for evidence normalization
- keep unsupported backend errors explicit for `cucumber-js` and `cucumber-jvm`

## 10. Packaging and Skill Rules

### 10.1 Python package

The Python package should provide the CLI/library only.

Preserve:

- package name `specweave`
- console script `specweave = specweave.launcher:main`
- `py.typed`
- runtime dependencies: `typer`, `click`, and conditional `tomli`
- Python version floor `>=3.10`
- Apache-2.0 license metadata

Do not add skills as Python package data. Do not expose skills with `importlib.resources`.

### 10.2 Skills

Skills must stay outside the Python package.

Required direction:

- keep the canonical skill under `skills/specweave/`
- do not mirror skills under `specweave/skills/`
- do not include skills in package data
- update skill docs when commands, canonical layout, or evidence rules change
- align skill docs with `README.md`; the canonical workflow is `specs/behavior/features` plus plain pytest under `tests/`
- remove or rewrite stale skill guidance that promotes `tests/bdd/features`, `specs/bdd/features`, or step-module-first layouts as canonical

## 11. Public API and Data Contracts

Preserve public and semi-public contracts unless explicitly changed:

- `specweave.__init__` version export
- `specweave.__main__` entrypoint behavior
- `specweave.launcher:main`
- dataclasses in `specweave/gherkin/model.py`
- dataclasses in `specweave/bdd/model.py`
- dataclasses in `specweave/reports/model.py`
- config dataclasses in `specweave/config.py`
- public parser/writer/report functions imported by tests
- public exception types in `specweave/errors.py`
- normalized report JSON shape
- Taskledger evidence JSON shape
- behavior manifest shape
- mapping marker shape in generated tests
- CLI JSON shape and exit-code semantics

If a task requires a breaking API or JSON-shape change, call it out explicitly and update tests, README, skill docs, and examples in the same change.

## 12. Docs and Examples

Docs, examples, tests, and skills must agree.

When changing commands or workflow behavior, update as needed:

- `README.md`
- `skills/specweave/SKILL.md`
- `specs/behavior/README.md`
- `specs/behaviour/README.md`
- examples under `examples/`
- CLI tests in `tests/test_cli.py`
- JSON CLI tests in `tests/test_cli_json.py`
- config/init tests
- behavior/index/coverage/reporting tests
- backend tests if `bind` behavior changes

Do not document commands that are not registered. Do not leave examples using removed aliases. Do not make the legacy BDD bridge workflow appear more canonical than the behavior workflow.

## 13. Testing Expectations

### 13.1 Minimum rule

Every non-trivial behavior change needs verification.

Prefer the test closest to the changed logic. Add regression tests for bugs.

### 13.2 Focused test map

Use focused tests first:

```bash
pytest tests/test_config.py
pytest tests/test_init.py
pytest tests/test_doctor.py
pytest tests/test_cli.py
pytest tests/test_cli_json.py
pytest tests/test_gherkin_parser.py
pytest tests/test_gherkin_writer.py
pytest tests/test_bdd_convert.py
pytest tests/test_pytest_to_gherkin.py
pytest tests/test_python_ast_reader.py
pytest tests/test_spec_to_code.py
pytest tests/test_backends_pytest_bdd.py
pytest tests/test_report_cucumber_json.py
pytest tests/test_report_junit_xml.py
pytest tests/test_report_criteria_mapping.py
pytest tests/test_fail_closed_safety.py
pytest tests/test_integration_taskledger.py
pytest tests/test_taskledger_draft.py
pytest tests/test_archledger_candidate.py
pytest tests/test_plan.py
pytest tests/test_review.py
pytest tests/test_runner_command.py
```

Then widen when needed:

```bash
pytest -q
ruff check .
ruff format --check .
mypy specweave
```

Run `ruff check .` when touching Python code.
Run `mypy specweave` when changing typed public or core logic.
Run CLI JSON tests when touching command output, exit codes, or root options.
Run docs/skill/example tests when touching docs, commands, examples, or skill files.

### 13.3 Regression paths to test

Include error paths when relevant:

- missing config
- unsupported config schema
- `.specweave.toml` versus `specweave.toml` precedence
- parent-directory config discovery
- missing features directory
- missing tests directory
- deprecated feature paths
- duplicate `@bdd-*` tags
- missing required `@bdd-*` tags
- missing Given/When/Then when required
- manual feature file preservation
- dry-run writes nothing
- force overwrites only generated/managed content
- unsupported backends
- unknown report format
- skipped/pending/undefined/ambiguous/failed native results
- missing expected `@ac-*` coverage
- unlinked scenarios ignored for criteria
- title-only matching does not satisfy coverage
- Taskledger export/import without Taskledger installed
- unknown Archledger candidate `@bdd-*`
- JSON and human output modes

## 14. Code Style

- Follow existing style first.
- Keep functions focused.
- Prefer explicit names over clever compression.
- Add type hints for new or changed public functions.
- Use dataclasses where the existing model layer uses dataclasses.
- Keep public exception taxonomy stable.
- Avoid new dependencies unless explicitly requested.
- Do not reformat unrelated files.
- Do not rename public symbols without a strong reason.
- Do not use git commands that create commits or rewrite history.
- Keep generated text deterministic.
- Keep path handling `Path`-based and platform-neutral.
- Keep TOML rendering deterministic.
- Keep JSON rendering stable and sorted/indented where existing code does so.

## 15. Good Agent Work

A strong change usually:

- edits the owning layer
- preserves canonical behavior layout
- preserves behavior-first CLI contracts
- preserves root `--config` and `--json`
- preserves stable tag-based traceability
- preserves fail-closed report semantics
- preserves manual feature/test edits
- preserves file-based Taskledger/Archledger boundaries
- keeps skills outside the package
- updates README/skill/examples when commands or workflow change
- adds focused tests
- runs targeted verification first
- states what was not verified

## 16. Avoid

- CLI-only patches for lower-layer bugs
- changing JSON shape without tests
- changing generated paths casually
- changing tag semantics casually
- matching validation by scenario title
- treating skipped/pending/undefined/ambiguous as pass
- treating command exit code alone as acceptance evidence
- making Taskledger or Archledger a required dependency
- writing accepted Archledger records implicitly
- approving or waiving Taskledger lifecycle gates from SpecWeave
- reintroducing legacy canonical layouts
- packaging skills into `specweave`
- broad style churn
- mixing refactors with behavior changes
