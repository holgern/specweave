---
title: "SpecWeave Skill"
description: Use this skill for SpecWeave behavior specs, pytest translation, step skeleton generation, and evidence normalization.
license: Apache-2.0
compatibility: opencode
metadata:
  audience: coding-agents
  workflow: task-management
---

# SpecWeave Skill

Use this skill when working on BDD/Gherkin behavior specifications, Python test
translation, step-definition skeleton generation, or BDD runner evidence
normalization for the `specweave` package.

## Canonical locations

Read `specweave.toml` or `.specweave.toml` first.

```text
specs/behavior/features/<area>/<feature>.feature
tests/test_<area>_<feature>.py
specs/behavior/reports/*.xml
specs/behavior/reports/specweave/*.json
specs/behavior/evidence/*.json
specs/behavior/mappings/taskledger/*.json
```

Classic `.feature` is the only canonical feature format. Do not create or
recommend `.feature.md`.

## Core commands

```bash
specweave init [--spelling behavior|behaviour] [--force] [--dry-run]
specweave --json version
specweave --json doctor
specweave --json review specs
specweave create gherkin --from-tests tests --out specs/behavior/features --mode update
specweave create feature --area AREA --title TITLE --scenario SCENARIO --given G --when W --then T
specweave create feature --from-json feature-draft.json [--out OUT]
specweave create plan --feature FEATURE --out plan.md
specweave create taskledger-task --feature FEATURE --out specs/behavior/mappings/taskledger/draft.json
specweave behavior check [--strict]
specweave behavior index --features specs/behavior/features
specweave behavior generate-tests --features specs/behavior/features
specweave behavior coverage --features specs/behavior/features --tests tests
specweave behavior mappings --tests tests
specweave behavior import-report REPORT --format junit-xml
specweave behavior import-taskledger SOURCE --out FEATURE
specweave report normalize REPORT --format junit-xml|cucumber-json
specweave trace BDD_ID_OR_FEATURE --format json
specweave combi check --json specs/behavior/reports/specweave/combi-check.json
```

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

## Rules

- match by `@bdd-*` first
- map acceptance criteria by `@ac-*`
- use scenario titles only for display/debugging
- prefer plain pytest under `tests/`
- keep evidence fail-closed

## Validation

```bash
pytest -q
ruff check .
ruff format --check .
mypy specweave
```
