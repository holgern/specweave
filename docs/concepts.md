# Concepts

## What SpecWeave is

SpecWeave provides:

- Gherkin model, parser, writer, and linter
- Translation from existing pytest tests to draft Gherkin features
- Generation of plain pytest skeletons from Gherkin features
- Behavior index and manifest generation
- Static behavior coverage checks
- JUnit XML evidence import and normalization
- Fail-closed mapping from scenario results to acceptance criteria
- Optional Taskledger file exchange and Archledger candidate generation

## What SpecWeave is not

SpecWeave is not:

- A task ledger — it does not own task lifecycle state
- An architecture ledger — it does not persist architecture records
- A CI system — it delegates test execution to pytest
- A test runner — it normalizes evidence from external reports
- A Cucumber implementation — it does not execute Gherkin directly

## Ownership boundaries

| Asset                            | Owner                                       |
| -------------------------------- | ------------------------------------------- |
| `.feature.md` / `.feature` files | SpecWeave                                   |
| Plain pytest test files          | SpecWeave (generated skeletons) and user    |
| Behavior manifest and index      | SpecWeave (generated)                       |
| Evidence JSON                    | SpecWeave (generated from imported reports) |
| Task lifecycle, plans, approvals | Taskledger                                  |
| Architecture records             | Archledger                                  |

SpecWeave exchanges files with Taskledger and Archledger through explicit
import/export but never becomes their durable state owner.

## Key design principles

### Tag-based traceability

Scenario identity is tag-based, primarily `@bdd-*`. Acceptance-criterion
linkage is tag-based, primarily `@ac-*`. Scenario titles are display and
debug text only. Title-based matching is not used for validation.

### Fail-closed evidence

SpecWeave fails closed. It does not mark behavior or acceptance criteria as
passed when a linked result is failed, errored, skipped, pending, undefined,
ambiguous, missing, or unlinked. A passing command exit code alone is not
sufficient evidence.

### Plain pytest first

SpecWeave generates plain pytest test skeletons. It does not require
`pytest-bdd`, `behave`, step-definition modules, or Cucumber runtimes for
the canonical workflow.

### Markdown Gherkin first

When `[gherkin].document_format = "markdown"` (the default), SpecWeave
uses `.feature.md` files. Classic `.feature` files are supported through
configuration and conversion.
