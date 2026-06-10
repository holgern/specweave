# Commands

## Root options

```text
--config PATH
--json
```

## Core

```bash
specweave init
specweave doctor
specweave version
specweave explain PATH...
```

## Behavior

```bash
specweave behavior check [FEATURE_OR_DIR]
specweave behavior index --features specs/behavior/features --out specs/behavior/README.md --manifest specs/behavior/manifest.json --tests-dir tests
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
specweave behavior coverage --features specs/behavior/features --tests tests --view both --show gaps --format markdown --out specs/behavior/reports/specweave/coverage.md
specweave behavior mappings --tests tests --format json
specweave behavior import-report REPORT --format junit-xml
specweave behavior import-taskledger SOURCE --out FEATURE
```

## Review

```bash
specweave review specs
specweave review coverage --view both --show gaps --format markdown --out specs/behavior/reports/specweave/coverage-gaps.md
specweave review coverage --view feature --show missing
specweave review coverage --view test --show unmapped
```

`review specs` is the concise health gate. `review coverage` is the detailed
two-way browser for feature-to-pytest and pytest-to-feature traceability.

## Create

```bash
specweave create gherkin --from-tests tests --out specs/behavior/features
specweave create feature --area AREA --title TITLE --scenario SCENARIO --given G --when W --then T
specweave create feature --from-json feature-draft.json [--out OUT]
specweave create plan --feature FEATURE --out plan.md
specweave create taskledger-task --feature FEATURE --out specs/behavior/mappings/taskledger/draft.json
```

## Diagnostics

```bash
specweave trace BDD_ID_OR_FEATURE --format json
specweave combi check --json specs/behavior/reports/specweave/combi-check.json
```

## Compatibility and bridge commands

These remain available but are not the canonical workflow:

- `bdd check/index/generate-tests/coverage`
- `bdd export`
- `bdd import-feature`
- `draft`
- `bind`
- `run`
- `report normalize`
- `report inspect`
- `archledger`
- `update`

There is no longer a canonical `convert` command for Markdown feature files.
