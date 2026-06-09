# Commands

SpecWeave commands are organized into families. Use `--help` on any command
for details.

## Root options

```
--config PATH    Use an explicit config file path
--json           Machine-readable JSON output
```

## Core commands

### init

Initialize a SpecWeave project configuration and directory layout.

```bash
specweave init
specweave init --public-config        # use specweave.toml instead of .specweave.toml
specweave init --spelling behaviour   # British spelling variant
specweave init --dry-run
specweave init --force
```

### doctor

Diagnose SpecWeave setup and convention problems.

```bash
specweave doctor
specweave doctor --fix
```

### version

Print the specweave version.

```bash
specweave version
```

### explain

Explain Python test files as candidate behavior specs.

```bash
specweave explain tests/test_auth.py
```

## Behavior commands

The `behavior` family is the canonical command group.

### behavior check

Lint behavior feature files.

```bash
specweave behavior check
```

### behavior index

Generate the behavior Markdown index and manifest.

```bash
specweave behavior index \
  --features specs/behavior/features \
  --out specs/behavior/README.md \
  --manifest specs/behavior/manifest.json
```

### behavior generate-tests

Generate plain pytest skeletons from feature files.

```bash
specweave behavior generate-tests \
  --features specs/behavior/features \
  --tests-dir tests
```

### behavior coverage

Check static coverage between specs and tests.

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests
```

### behavior mappings

List explicit SpecWeave pytest mappings discovered from tests.

```bash
specweave behavior mappings --tests tests --format text
```

### behavior import-report

Import a pytest/JUnit report into behavior evidence JSON.

```bash
specweave behavior import-report \
  reports/behavior/pytest-junit.xml \
  --format junit-xml
```

### behavior import-taskledger

Create a canonical behavior feature from a Taskledger export.

```bash
specweave behavior import-taskledger \
  .specweave/mappings/taskledger/task-0123.json
```

## Create commands

### create feature

Create a new Gherkin feature file from structured inputs.

```bash
specweave create feature \
  --area auth \
  --title "User login" \
  --scenario "Successful login" \
  --given "a registered user exists" \
  --when "the user submits valid credentials" \
  --then "the user is authenticated"
```

### create gherkin

Create or update `.feature` files from existing pytest tests.

```bash
specweave create gherkin --from-tests tests --out specs/behavior/features
```

### create plan

Create a deterministic implementation plan from a feature file.

```bash
specweave create plan \
  --feature specs/behavior/features/auth/user-login.feature.md \
  --out plan.md
```

### create taskledger-task

Create a Taskledger task draft JSON from a feature file.

```bash
specweave create taskledger-task \
  --feature specs/behavior/features/auth/user-login.feature.md
```

## Review commands

### review specs

Review and diagnose SpecWeave projects.

```bash
specweave review specs
```

## Conversion commands

### convert

Convert between classic `.feature` and Markdown `.feature.md` formats.

```bash
specweave convert specs/behavior/features/auth/login.feature --to markdown
specweave convert --all --to markdown
specweave convert login.feature.md --to classic
```

## Diagnostics commands

### trace

Emit a normalized behavior-centered trace bundle.

```bash
specweave trace @bdd-user-login-success --format json
```

### combi check

Read-only cross-ledger integration diagnostics.

```bash
specweave combi check --json .specweave/reports/combi-check.json
```

## Bridge and legacy commands

These commands remain available for compatibility but are not the canonical
workflow:

- `draft` — Draft a feature file from acceptance criteria
- `bind` — Create missing step-definition skeletons
- `run` — Run a delegated BDD command
- `report normalize` — Normalize runner reports
- `archledger` — Render an Archledger candidate record
- `bdd check/index/generate-tests/coverage` — Aliases for behavior commands
- `bdd export` / `bdd import-feature` — Task-BDD JSON exchange
- `update` — Alias for `create gherkin --mode update`
