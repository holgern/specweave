# Reports and Evidence

SpecWeave normalizes test execution evidence with fail-closed semantics.

## Supported report formats

| Format          | Source                | Description       |
| --------------- | --------------------- | ----------------- |
| `junit-xml`     | pytest, JUnit runners | XML test reports  |
| `cucumber-json` | Cucumber runners      | JSON test reports |

## Import workflow

```bash
# Run tests with JUnit XML output
pytest --junitxml=reports/behavior/pytest-junit.xml

# Import the report
specweave behavior import-report \
  reports/behavior/pytest-junit.xml \
  --format junit-xml \
  --out .specweave/evidence/pytest-evidence.json
```

## Fail-closed rules

SpecWeave does not mark behavior or acceptance criteria as passed when a
linked result is:

- failed
- errored
- skipped
- pending
- undefined
- ambiguous
- missing
- unlinked
- only implied by process exit code

A passing command exit code alone is not sufficient evidence when a native
report is available.

## Acceptance-criterion coverage

Only scenarios linked by `@bdd-*` and/or `@ac-*` tags count toward
acceptance-criterion evidence. Unlinked scenarios do not satisfy acceptance
criteria. Each required `@ac-*` must have at least one passing linked
scenario.

Rules:

- Missing expected acceptance criteria must fail
- Failed sibling scenarios for the same criterion keep the criterion failed
- Skipped, pending, undefined, and ambiguous states are blocking
- Title-only matching does not satisfy coverage

## Evidence output

Normalized evidence is written as JSON under `.specweave/evidence/`. Each
record preserves:

- Scenario name and status
- Tags and duration (when available)
- Evidence source path
- Acceptance-criterion coverage summary
- Overall status

## Trace and cross-ledger diagnostics

```bash
# Trace a specific scenario across ledgers
specweave trace @bdd-user-login-success --format json

# Cross-ledger consistency check
specweave combi check --json .specweave/reports/combi-check.json
```

Trace output includes task IDs, acceptance criteria, BDD IDs, evidence
references, and source/test references in a `combi.trace.v1` bundle.

## Schema contracts

Shared file contracts for evidence and cross-ledger exchange are documented
as JSON Schema under `specweave/schemas/`:

- `combi.trace.v1.schema.json` — cross-ledger trace bundle
- `specweave.behavior-evidence.v1.schema.json` — normalized evidence
- `specweave.taskledger-bdd-export.v1.schema.json` — Taskledger BDD export
- `specweave.archledger-candidate.v1.schema.json` — Archledger candidate
