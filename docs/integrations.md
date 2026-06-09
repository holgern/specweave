# Integrations

SpecWeave integrates with Taskledger and Archledger through file-based
exchange only. It does not make either a runtime dependency.

## Taskledger integration

Taskledger owns task lifecycle, plans, acceptance criteria, user approval,
and durable task evidence. SpecWeave owns behavior feature files and
normalized evidence.

### Import Taskledger acceptance data

```bash
specweave behavior import-taskledger \
  .specweave/mappings/taskledger/task-0123.json \
  --out specs/behavior/features/task-management/plan-gates.feature.md
```

This creates a canonical behavior feature from a Taskledger export. The
Taskledger export is an input artifact; SpecWeave remains the owner of the
resulting feature file.

### Create a Taskledger task draft

```bash
specweave create taskledger-task \
  --feature specs/behavior/features/auth/user-login.feature.md
```

This generates a JSON task draft that can be imported into Taskledger.

### Boundaries

- SpecWeave does not add Taskledger lifecycle commands
- SpecWeave does not approve plans or waive validation
- SpecWeave does not require Taskledger as a Python dependency
- Exchange is file-based and explicit

## Archledger integration

Archledger owns durable architecture and specification records. SpecWeave
may render candidate markdown from a feature and `@bdd-*` tags.

### Generate an Archledger candidate

```bash
specweave archledger \
  --feature specs/behavior/features/auth/user-login.feature.md \
  --scenario @bdd-user-login-success
```

### Boundaries

- SpecWeave does not create accepted Archledger records by default
- SpecWeave does not mutate Archledger state implicitly
- Candidate output must be explicitly accepted through Archledger

## Combi trace

The `combi.trace.v1` bundle provides read-only cross-ledger traceability:

```bash
specweave trace @bdd-user-login-success --format json
```

This exposes task IDs, accepted AC IDs, BDD IDs, evidence references,
source/test references, and Archledger provenance. Missing BDD mappings or
evidence remain visible gaps.
