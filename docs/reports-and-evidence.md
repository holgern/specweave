# Reports and Evidence

SpecWeave normalizes execution evidence with fail-closed semantics.

## Supported imports

- `junit-xml`
- `cucumber-json`

## Default locations

- runner reports: `specs/behavior/reports`
- SpecWeave runner summaries: `specs/behavior/reports/specweave`
- normalized evidence: `specs/behavior/evidence`
- Taskledger mapping artifacts: `specs/behavior/mappings/taskledger`

## Import example

```bash
pytest --junitxml=specs/behavior/reports/pytest-junit.xml

specweave behavior import-report \
  specs/behavior/reports/pytest-junit.xml \
  --format junit-xml \
  --out specs/behavior/evidence/pytest-evidence.json
```

## Fail-closed rules

Passing evidence must not be inferred from:

- skipped, pending, undefined, ambiguous, errored, failed, or missing scenarios
- title-only matching
- process exit code alone when a native report exists

## Trace and cross-ledger diagnostics

```bash
specweave review coverage --view both --show gaps
specweave trace @bdd-user-login-success --format json
specweave combi check --json specs/behavior/reports/specweave/combi-check.json
```
