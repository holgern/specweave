# Commands

## Root options

```text
--config PATH
--json
```

## Core

```bash
specweave init --mode behaviour|specifications|both
specweave doctor
specweave version
specweave explain PATH...
```

## Behaviour

```bash
specweave behaviour check [FEATURE_OR_DIR]
specweave behaviour index --features specs/behaviour/features --out specs/behaviour/README.md --manifest specs/behaviour/manifest.json --tests-dir tests
specweave behaviour generate-tests --features specs/behaviour/features --tests-dir tests
specweave behaviour autolink --features specs/behaviour/features --tests tests --strategy generated-id
specweave behaviour autolink --features specs/behaviour/features --tests tests --strategy generated-id --apply
specweave behaviour refresh --coverage --mappings --index
specweave behaviour coverage --features specs/behaviour/features --tests tests --view both --show gaps --format markdown --out specs/behaviour/reports/specweave/coverage.md
specweave behaviour mappings --tests tests --format json
specweave behaviour import-report REPORT --format junit-xml
specweave behaviour import-taskledger SOURCE --out FEATURE
```

`behavior` remains available as a compatibility alias. `bdd` remains available as
an older compatibility group.

## Specifications

```bash
specweave specifications check [SPEC_OR_DIR]
specweave specifications index --root specs/specifications
specweave specifications coverage --root specs/specifications --tests tests --view both --show gaps
specweave specifications import-report REPORT --format junit-xml
```

`sdd` is the short alias for the same command group.

## Review

```bash
specweave review specs
specweave review behaviour
specweave review specifications
specweave review coverage --view both --show gaps --format markdown --out specs/behaviour/reports/specweave/coverage-gaps.md
specweave review coverage --view feature --show missing
specweave review coverage --view test --show unmapped
```

`review specs` is the concise health gate. `review coverage` is the detailed
two-way browser for feature-to-pytest and pytest-to-feature traceability.

Do not chain diagnostic gap commands with `&&`. Some gap commands correctly exit non-zero when gaps remain. Use labeled semicolon-separated commands or inspect each command separately.

## Create

```bash
specweave create gherkin --from-tests tests --out specs/behaviour/features
specweave create feature --area AREA --title TITLE --scenario SCENARIO --given G --when W --then T
specweave create feature --from-json feature-draft.json [--out OUT]
specweave create plan --feature FEATURE --out plan.md
specweave create taskledger-task --feature FEATURE --out specs/behaviour/mappings/taskledger/draft.json
```

## Diagnostics

```bash
specweave trace BDD_ID_OR_FEATURE --format json
specweave combi check --json specs/behaviour/reports/specweave/combi-check.json
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
