# Concepts

## Canonical behavior source

SpecWeave treats classic Gherkin `.feature` files under
`specs/behavior/features` as the source of truth for behavior intent.

## Executable enforcement

Plain pytest under `tests/` is the default enforcement path. Coverage and trace
matching use explicit mappings plus stable `@bdd-*` and `@ac-*` tags.

## Evidence

Normalized evidence is durable, readable JSON under `specs/behavior/evidence`.
Generated runner output remains under `specs/behavior/reports`.

## Boundaries

- Taskledger owns task lifecycle and validation state.
- SpecWeave owns behavior specs, translation, and normalized evidence.
- Archledger owns durable architecture records.
