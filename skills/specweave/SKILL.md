---
name: specweave
description: Use this skill when working on BDD/Gherkin behavior specifications, Python test translation, step-definition skeleton generation, or BDD runner evidence normalization for the `specweave` package.
license: Apache-2.0
compatibility: opencode
metadata:
  audience: coding-agents
  workflow: task-management
---

# SpecWeave Skill

Use this skill when working on BDD/Gherkin behavior specifications, Python
test translation, step-definition skeleton generation, or BDD runner evidence
normalization for the `specweave` package.

## Purpose

SpecWeave is the project-local BDD bridge. It translates between:

- Python tests;
- plain-English behavior descriptions;
- Gherkin/Cucumber `.feature` files;
- step-definition skeletons;
- normalized BDD execution evidence.

It is not a task lifecycle ledger, architecture ledger, or CI system.

## Ownership boundaries

Use these boundaries when designing changes:

- Taskledger owns task lifecycle, plans, acceptance criteria, validation
  state, and persisted validation evidence.
- SpecWeave owns BDD conversion, Gherkin files, step skeletons, external
  runner delegation, and normalized report/evidence generation.
- Archledger owns durable architecture/spec behavior records after a behavior
  is accepted as architecturally important.

Do not add Taskledger lifecycle commands to SpecWeave. Taskledger exports are input artifacts. SpecWeave normalized evidence is output artifact data, and Taskledger remains responsible for importing it into task state. Do not make SpecWeave write accepted Archledger records by default. Candidate generation is draft-only.

## Canonical file locations

Read `.specweave.toml` or `specweave.toml` first. If no config exists, run:

```bash
specweave init
```

Default canonical locations:

```text
specs/behavior/features/<area>/<feature>.feature.md
specs/behavior/features/<area>/<feature>.feature
tests/test_<area>_<feature>.py
reports/behavior/*.xml
.specweave/reports/*.json
.specweave/evidence/*.json
.specweave/mappings/taskledger/*.json
```

Some projects configure British path spelling:

```text
specs/behaviour/features/<area>/<feature>.feature
reports/behaviour/*.xml
```

Use the configured paths; do not hard-code either spelling.

When `[gherkin].document_format = "markdown"` (the default), agents must
create `.feature.md` files. If a classic `.feature` file is produced, run
`specweave convert <file> --to markdown` or `specweave convert --all --to markdown`
and review the resulting `.feature.md` files before committing.

## Package commands

```bash
specweave init [--spelling behavior|behaviour] [--public-config] [--force] [--dry-run]
specweave --json version
specweave --json doctor
specweave --json review specs
specweave create gherkin --from-tests tests --out specs/behavior/features --mode update
specweave update specs --from-tests tests
specweave create feature --area AREA --title TITLE --scenario SCENARIO --given G --when W --then T
specweave create plan --feature FEATURE --out plan.md
specweave create taskledger-task --feature FEATURE --out .specweave/mappings/taskledger/draft.json
specweave behavior check [--strict]
specweave behavior index --features specs/behavior/features
specweave behavior generate-tests --features specs/behavior/features
specweave behavior coverage --features specs/behavior/features --tests tests [--format json|text|markdown] [--show all|missing|bound|stale|waived]
specweave behavior mappings --tests tests [--format text|json]
specweave behavior import-report REPORT --format junit-xml
specweave behavior import-taskledger SOURCE --out FEATURE
specweave report normalize REPORT --format junit-xml|cucumber-json
specweave convert FEATURE_OR_DIR... [--all] [--out OUT] [--to markdown|classic] [--from auto|markdown|classic] [--force] [--dry-run] [--replace-source] [--validate/--no-validate]
```
specweave trace BDD_ID_OR_FEATURE --format json
specweave combi check --json .specweave/reports/combi-check.json
## Target Gherkin shape

Prefer this generated format:

```gherkin
@area-<area> @feature-<feature>
Feature: <Readable feature title>
  <Short behavior intent, not implementation details.>

  @rule-<rule>
  Rule: <Business rule title>

    @bdd-<stable-id> [@ac-<id>]
    Example: <Observable scenario title>
      Given <initial state/context>
      When <actor/action/event>
      Then <observable outcome>
```

Matching rules:

- match by `@bdd-*` first;
- map to `@ac-*` second;
- use scenario titles only for display/debugging;
- never rely on scenario title as the primary validation key.

## Explicit pytest mapping workflow

Use explicit mapping only. Do not infer behavior coverage from similar test
names or scenario titles.

Preferred loop:

```bash
specweave convert --all --to markdown
specweave behavior coverage --features specs/behavior/features --tests tests --format text --show missing
specweave behavior mappings --tests tests --format text
specweave review specs
```

Map pytest functions with one of:

- `@pytest.mark.specweave(feature=..., scenario=..., rule=...)`
- `# specweave: feature=...` plus `# specweave: scenario=...`
- a docstring that contains the feature path and `@bdd-*` id

Coverage must count only those explicit mappings.

## Harness translation examples

User says:

```text
update @specs from @tests using $specweave
```

Agent should run:

```bash
specweave --json update specs --from-tests @tests --out @specs
specweave --json doctor
specweave --json review specs
```

User says:

```text
$specweave, i want a new feature which is doing this when this happens.
```

Agent should:

1. draft a concrete Gherkin feature from the request;
2. write it using `specweave create feature` if the inputs can be expressed
   as flags;
3. otherwise write the `.feature.md` file (or `.feature` when the config
   uses classic format) directly in the configured feature directory;
4. run `specweave doctor PATH` or `specweave behavior check PATH`;
5. report the created file and scenario IDs.

User says:

```text
$specweave create a plan.md to implement @new_feature.feature
```

Agent should run:

```bash
specweave create plan --feature @new_feature.feature --out plan.md
```

User says:

```text
$specweave create a new $taskledger task to implement new_feature.feature with unit tests.
```

Agent should run the SpecWeave draft first:

```bash
specweave create taskledger-task --feature new_feature.feature --out .specweave/mappings/taskledger/<slug>.task-draft.json
```

Then, only if the project/harness permits Taskledger mutation, use the
external Taskledger workflow to create the task from that draft.

## Validation commands

Use these checks after code changes:

```bash
pytest -q
ruff check .
ruff format --check .
mypy specweave
```

At minimum, run focused tests for changed modules and then the full suite.

## Safety rule

Fail closed. Do not mark acceptance criteria as passed when a linked scenario
is skipped, pending, undefined, ambiguous, errored, or failed. Do not treat
exit code alone as sufficient validation when a native BDD report is available.
