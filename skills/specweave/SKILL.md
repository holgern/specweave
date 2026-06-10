---
title: "SpecWeave Skill"
description: Deterministic workflow for SpecWeave behavior specs, pytest mappings, coverage review, and evidence normalization.
license: Apache-2.0
compatibility: opencode
metadata:
  audience: coding-agents
  workflow: behavior-specification
---

# SpecWeave Skill

Use this skill for SpecWeave behavior specifications, Gherkin feature files, plain-pytest mappings, coverage review, and normalized BDD evidence.

## Non-negotiables

1. Read `specweave.toml` or `.specweave.toml` before running commands. Use `--config <path>` when the project uses a non-default or hidden config.
2. Classic `.feature` files are canonical. Do not create `.feature.md`.
3. Treat scenario identity as `@bdd-*`, not the scenario title.
4. Do not treat a bare `@bdd-*` string in a test docstring as a mapping. A mapping must include both the feature path and the scenario id.
5. Use SpecWeave reports before grepping. Grep is only a fallback after the commands below fail to answer the question.
6. Commands that report gaps may exit non-zero. Read their output; do not assume the command crashed.

## Canonical locations

Resolve these from config first. Defaults are:

```text
specs/behavior/features/<area>/<feature>.feature
tests/test_<area>_<feature>.py
specs/behavior/reports/*.xml
specs/behavior/reports/specweave/*.json
specs/behavior/evidence/*.json
specs/behavior/mappings/taskledger/*.json
```

## First diagnostic workflow

Run this sequence before editing files:

```bash
specweave --config .specweave.toml --json doctor
specweave --config .specweave.toml review specs
specweave --config .specweave.toml review coverage --view both --show gaps --format markdown --out specs/behavior/reports/specweave/coverage-gaps.md
specweave --config .specweave.toml behavior mappings --tests tests --format json
```

If the project uses `specweave.toml`, drop `--config .specweave.toml`.

## When asked to complete feature coverage and link tests

1. Fix Gherkin lint errors first. Use `specweave behavior check` and edit only the reported feature files.
2. Generate or refresh the two-way coverage report with `review coverage --view both --show gaps`.
3. If features were generated from pytest and coverage shows many candidate tests, run `specweave behavior autolink --strategy generated-id` first. Review the dry-run. Only then run again with `--apply`.
4. For each remaining missing feature-side binding, add a mapping to the most relevant plain-pytest test or create a skeleton with `behavior generate-tests`.
5. For each unmapped pytest-side test, decide one of: link it to an existing scenario, create a new scenario, or leave it unmapped intentionally and mention why.
6. Regenerate standard artifacts with `behavior refresh --coverage --mappings --index` or regenerate the behavior index directly with `behavior index --features specs/behavior/features --tests-dir tests`.
7. Finish with a compact summary: changed files, command results, remaining gaps, and next commands.

Do not chain diagnostic gap commands with `&&`. Some gap commands correctly exit non-zero. Use labeled semicolon-separated commands or inspect each command separately.

## Mapping plain pytest to Gherkin

Preferred mapping for new or generated pytest tests is the decorator form:

```python
@pytest.mark.specweave(
    feature=(
        "specs/behavior/features/<area>/"
        "<feature>.feature"
    ),
    scenario=(
        "@bdd-<stable-id-part-1>"
        "<stable-id-part-2>"
    ),
)
def test_observable_behavior() -> None:
    ...
```

Short comments are valid for manual mappings when each line stays under Ruff's limit:

```python
# sw: f=specs/behavior/features/<area>/<feature>.feature
# sw: s=@bdd-<stable-id>
def test_observable_behavior() -> None:
    ...
```

Legacy `# specweave: feature=...` and `# specweave: scenario=...` comments remain valid for compatibility. Do not add file-level `# ruff: noqa: E501` only because of SpecWeave mapping metadata. Docstring mapping is valid only when it contains both `specs/behavior/features/...feature` and `@bdd-*`.

## Command matrix

```bash
specweave init [--public-config] [--spelling behavior|behaviour] [--force] [--dry-run]
specweave --json version
specweave --json doctor
specweave doctor --fix
specweave review specs
specweave review coverage --view both --show gaps --format markdown --out specs/behavior/reports/specweave/coverage-gaps.md
specweave create gherkin --from-tests tests --out specs/behavior/features --mode update
specweave create feature --area AREA --title TITLE --scenario SCENARIO --given G --when W --then T
specweave create feature --from-json feature-draft.json [--out OUT]
specweave create plan --feature FEATURE --out plan.md
specweave create taskledger-task --feature FEATURE --out specs/behavior/mappings/taskledger/draft.json
specweave behavior check [FEATURE_OR_DIR] [--strict]
specweave behavior index --features specs/behavior/features --out specs/behavior/README.md --manifest specs/behavior/manifest.json --tests-dir tests
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
specweave behavior coverage --features specs/behavior/features --tests tests --view both --show gaps --format markdown --out specs/behavior/reports/specweave/coverage.md
specweave behavior mappings --tests tests --format json
specweave behavior autolink --features specs/behavior/features --tests tests --strategy generated-id [--apply]
specweave behavior refresh --coverage --mappings --index
specweave behavior import-report specs/behavior/reports/pytest-junit.xml --format junit-xml --out specs/behavior/evidence/pytest-evidence.json
specweave behavior import-taskledger SOURCE --out FEATURE
specweave report normalize REPORT --format junit-xml|cucumber-json
specweave trace BDD_ID_OR_FEATURE --format json
specweave combi check --json specs/behavior/reports/specweave/combi-check.json
```

Note: `behavior index` uses `--tests-dir`, not `--tests`, unless the CLI has added a compatibility alias.

## Target Gherkin shape

```gherkin
@area-<area> @feature-<feature>
Feature: <Readable feature title>
  <Short behavior intent>

  @rule-<rule>
  Rule: <Business rule title>

    @bdd-<stable-id> @ac-<id>
    Example: <Observable scenario title>
      Given <initial state/context>
      When <actor/action/event>
      Then <observable outcome>
```

## Output contract for coding agents

End every SpecWeave task with this structure:

```markdown
## Summary

- ...

## Files changed

- `path`: why

## Validation

- `command`: passed/failed, relevant counts

## Coverage result

- features/scenarios/bound/missing/unmapped/stale
- link to generated report path if created

## Remaining work

- exact files or `@bdd-*` ids still requiring attention
```
