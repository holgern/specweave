# AGENTS.md

This file defines how coding agents should work in the `specweave` repository.

## Core contract

SpecWeave keeps behavior intent readable, executable validation traceable, and
evidence fail-closed when data is incomplete or ambiguous.

It is not Taskledger, Archledger, or CI.

## Working rules

- prefer the smallest correct change
- preserve tag-based traceability (`@bdd-*`, `@ac-*`)
- preserve fail-closed evidence semantics
- preserve manual feature and test edits unless overwrite is explicit
- keep changes in the owning layer
- add focused tests for non-trivial behavior changes
- do not create commits

- when using the SpecWeave skill, read `skills/specweave/SKILL.md` from this repository before any globally installed SpecWeave skill and state the loaded skill path

## Canonical layout

```text
specweave.toml
specs/behavior/README.md
specs/behavior/manifest.json
specs/behavior/features/<area>/<feature>.feature
specs/behavior/evidence/*.json
specs/behavior/mappings/taskledger/*.json
tests/test_<area>_<feature>.py
specs/behavior/reports/*.xml
specs/behavior/reports/specweave/*.json
```

Compatibility:

- `.specweave.toml` is still discovered for existing projects
- `specs/behaviour/...` remains supported through spelling configuration

Do not reintroduce `.feature.md` as a canonical format.

## Ownership boundaries

SpecWeave owns:

- canonical behavior feature files
- pytest-to-Gherkin translation
- plain pytest skeleton generation
- behavior index and manifest generation
- report normalization and evidence JSON
- file-based Taskledger and Archledger exchange

Taskledger owns:

- task lifecycle
- plan approval
- validation state
- waivers

Archledger owns:

- durable architecture records

## Gherkin rules

- canonical behavior specs are classic `.feature`
- one feature per file
- group features by area
- scenario identity is tag-based, primarily `@bdd-*`
- acceptance linkage is tag-based, primarily `@ac-*`
- scenario titles are display/debug text only
- plain pytest under `tests/` is the default enforcement path

Do not match validation by scenario title.

- start coverage linking work with `specweave review coverage --view both --show gaps` before broad source or test greps
- do not treat bare `@bdd-*` docstring text as a pytest mapping unless the same mapping also includes the feature path
- end SpecWeave task summaries with Summary, Files changed, Validation, Coverage result, and Remaining work sections

## Config and init rules

- default config file: `specweave.toml`
- hidden `.specweave.toml` remains supported for discovery and explicit paths
- default evidence path: `specs/behavior/evidence`
- default mapping path: `specs/behavior/mappings`
- default runner summary path: `specs/behavior/reports/specweave`
- `specweave init` must not create `.specweave/`

## Important code surfaces

- `specweave/config.py`
- `specweave/init.py`
- `specweave/cli.py`
- `specweave/gherkin/parser.py`
- `specweave/gherkin/writer.py`
- `specweave/gherkin/lint.py`
- `specweave/behavior/index.py`
- `specweave/behavior/coverage.py`
- `specweave/behavior/reporting.py`
- `specweave/behavior/generate.py`
- `specweave/translate/pytest_to_gherkin.py`
- `specweave/python_inspect/ast_reader.py`
- `specweave/integrations/taskledger.py`
- `specweave/integrations/archledger.py`
- `specweave/trace.py`

## Testing expectations

Prefer focused tests first:

```bash
pytest tests/test_config_configuration.py
pytest tests/test_init_initialization.py
pytest tests/test_gherkin_parser.py
pytest tests/test_gherkin_writer.py
pytest tests/test_gherkin_lint.py
pytest tests/test_translation_pytest_to_gherkin.py
pytest tests/test_create_feature_json.py
pytest tests/test_cli_json.py
pytest tests/test_cli_cli_contract.py
pytest tests/test_behavior_index.py
pytest tests/test_behavior_coverage.py
pytest tests/test_behavior_reporting.py
pytest tests/test_trace.py
pytest tests/test_combi_check.py
pytest tests/test_integrations_taskledger.py
pytest tests/test_review_spec_review.py
pytest tests/test_doctor_diagnostics.py
```

Widen when needed:

```bash
pytest -q
ruff check .
ruff format --check .
mypy specweave
```

## Documentation sync

When commands, workflow, or layout change, update:

- `README.md`
- `docs/`
- `skills/specweave/SKILL.md`
- `ARCHITECTURE.md`
- relevant behavior specs under `specs/behavior/features/`

## Avoid

- reintroducing Markdown `.feature.md` support
- storing durable SpecWeave artifacts under `.specweave/`
- changing JSON shapes casually
- matching by scenario title
- treating skipped or missing evidence as passing
- making Taskledger or Archledger runtime dependencies
