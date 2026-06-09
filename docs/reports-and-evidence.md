# Reports and Evidence

SpecWeave normalizes execution evidence with fail-closed semantics.

## Supported imports

- `junit-xml`
- `cucumber-json`

## Default locations

- runner reports: `reports/behavior`
- SpecWeave runner summaries: `reports/behavior/specweave`
- normalized evidence: `specs/behavior/evidence`
- Taskledger mapping artifacts: `specs/behavior/mappings/taskledger`

## Import example

```bash
pytest --junitxml=reports/behavior/pytest-junit.xml

specweave behavior import-report \
  reports/behavior/pytest-junit.xml \
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
specweave trace @bdd-user-login-success --format json
specweave combi check --json reports/behavior/specweave/combi-check.json
```
