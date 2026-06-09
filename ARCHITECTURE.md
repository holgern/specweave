# Architecture

## Overview

SpecWeave is a Python CLI and library that translates between canonical classic
Gherkin behavior specifications, plain pytest enforcement, and normalized
execution evidence.

It is not a task ledger, architecture ledger, or CI system.

## Goals

1. keep behavior intent readable
2. keep validation traceable through stable ids
3. fail closed when evidence is incomplete or ambiguous
4. support brownfield pytest-to-Gherkin translation without executing tests
5. exchange files with Taskledger and Archledger without taking ownership of
   their state

## Canonical filesystem model

```text
specweave.toml
specs/behavior/README.md
specs/behavior/manifest.json
specs/behavior/features/<area>/<feature>.feature
specs/behavior/evidence/*.json
specs/behavior/mappings/taskledger/*.json
tests/test_<area>_<feature>.py
reports/behavior/*.xml
reports/behavior/specweave/*.json
```

Compatibility remains for explicit or discovered `.specweave.toml`, but
`specweave.toml` is the default config.

## Key decisions

1. **Classic `.feature` only.** Canonical behavior specs are classic Gherkin.
   Legacy `.feature.md` is rejected with an explicit migration error.
2. **Plain pytest is canonical enforcement.** No `pytest-bdd`, `behave`, or
   step-definition-first workflow is required.
3. **Traceability is tag-based.** Use `@bdd-*` and `@ac-*`; scenario titles are
   display/debug text only.
4. **Durable SpecWeave artifacts stay readable.** Evidence and mappings live
   under `specs/behavior/*`. Generated runner output stays under
   `reports/behavior/*`.
5. **External ledgers stay external.** Taskledger owns task lifecycle.
   Archledger owns accepted architecture records.

## Main layers

- `specweave/config.py` and `specweave/init.py` — config and layout
- `specweave/gherkin/*` — model, parser, writer, lint, validation
- `specweave/translate/*` — pytest/spec translation
- `specweave/behavior/*` — index, coverage, generation, reporting
- `specweave/python_inspect/*` — AST-based pytest inspection
- `specweave/reports/*` — report parsing and normalization
- `specweave/integrations/*` — file-based Taskledger and Archledger exchange
- `specweave/cli.py` — user-facing CLI contract

## External interfaces

- CLI with root `--config` and `--json`
- filesystem-based specs, evidence, and reports
- delegated test execution via external commands
- file-based Taskledger exchange
- candidate-only Archledger output

## Validation rules

- skipped, pending, undefined, ambiguous, errored, failed, missing, and
  unlinked scenarios do not satisfy acceptance criteria
- command exit code alone is not enough evidence when native report data exists
- title-only matching is not valid traceability
