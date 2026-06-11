# Reports and Evidence

SpecWeave normalizes execution evidence with fail-closed semantics.

## Supported imports

- `junit-xml`
- `cucumber-json`

## Default locations

- behaviour runner reports: `specs/behaviour/reports`
- behaviour runner summaries: `specs/behaviour/reports/specweave`
- behaviour evidence: `specs/behaviour/evidence`
- specifications evidence: `specs/specifications/evidence`
- Taskledger mapping artifacts: `specs/behaviour/mappings/taskledger`

## Import example

```bash
pytest --junitxml=specs/behaviour/reports/pytest-junit.xml

specweave behaviour import-report \
  specs/behaviour/reports/pytest-junit.xml \
  --format junit-xml \
  --out specs/behaviour/evidence/pytest-evidence.json

specweave specifications import-report \
  build/reports/junit.xml \
  --format junit-xml \
  --out specs/specifications/evidence/junit.pytest-evidence.json
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
specweave combi check --json specs/behaviour/reports/specweave/combi-check.json
```
