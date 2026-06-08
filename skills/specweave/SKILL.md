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

Use this skill when working on BDD/Gherkin behavior specifications, Python test translation, step-definition skeleton generation, or BDD runner evidence normalization for the `specweave` package.

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

- Taskledger owns task lifecycle, plans, acceptance criteria, validation state, and persisted validation evidence.
- SpecWeave owns BDD conversion, Gherkin files, step skeletons, external runner delegation, and normalized report/evidence generation.
- Archledger owns durable architecture/spec behavior records after a behavior is accepted as architecturally important.

Do not add Taskledger lifecycle commands to SpecWeave. Do not make SpecWeave write accepted Archledger records by default. Candidate generation is acceptable.

## Preferred file locations

Store executable BDD assets in the project repository:

```text
tests/bdd/features/<task-id>-<slug>.feature
tests/bdd/steps/<slug>_steps.py
reports/bdd/<task-id>-cucumber.json
.specweave/reports/summary.json
.specweave/evidence/<task-id>.bdd-evidence.json
```

Do not store executable `.feature` files only inside Taskledger state or Archledger records. Taskledger and Archledger should store metadata, evidence references, and durable summaries.

## Current package commands

Existing CLI commands:

```bash
specweave explain PATH...
specweave draft --from-json task.json --out tests/bdd/features/task.feature
specweave bind tests/bdd/features/task.feature --backend behave --out tests/bdd/steps
specweave run --runner behave -- behave tests/bdd/features --format json -o reports/bdd/task.json
specweave version
```

Current backend support for `bind` is `behave` only.

## Current implementation gaps

Before claiming full Taskledger/Archledger workflow support, verify these are implemented:

- `Rule:` support in Gherkin model/parser/writer;
- multiple tags on a single tag line;
- canonical tags: `@task-*`, `@rule-*`, `@bdd-*`, `@ac-*`;
- task-BDD model with rules and examples;
- stable BDD example IDs;
- Cucumber JSON normalization;
- JUnit XML normalization;
- scenario-to-acceptance-criterion mapping by tags;
- fail-closed treatment for skipped, pending, undefined, ambiguous, and failed scenarios;
- Taskledger-compatible evidence JSON output;
- Archledger candidate markdown generation.

## Target Gherkin shape

Prefer this generated format:

```gherkin
@task-0123
Feature: Task lifecycle gates

  @rule-0001
  Rule: Implementation requires an accepted plan

    @bdd-0001 @task-0123 @rule-0001 @ac-0001
    Scenario: Agent cannot start implementation without an accepted plan
      Given a task has a proposed plan
      When the agent starts implementation
      Then taskledger rejects the transition
```

Matching rules:

- match by `@bdd-*` first;
- map to `@ac-*` second;
- use scenario titles only for display/debugging;
- never rely on scenario title as the primary validation key.

## Recommended implementation order

1. Add `Rule` model plus parser/writer support.
2. Add multi-tag-line parsing/writing.
3. Add task-BDD JSON model and Feature conversion.
4. Add Cucumber JSON and JUnit XML report normalizers.
5. Add acceptance-criterion coverage/mapping.
6. Add Taskledger-compatible evidence JSON output.
7. Add Archledger candidate markdown rendering.
8. Expand step backend support after the core evidence flow is reliable.

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

Fail closed. Do not mark acceptance criteria as passed when a linked scenario is skipped, pending, undefined, ambiguous, errored, or failed. Do not treat exit code alone as sufficient validation when a native BDD report is available.
