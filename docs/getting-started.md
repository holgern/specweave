# Getting Started

## Install

```bash
pip install specweave
```

Optional extras:

```bash
pip install specweave[gherkin]   # official Cucumber Gherkin parser
pip install specweave[dev]       # development tools including docs build
```

## Initialize a project

```bash
specweave init
```

This creates:

- `.specweave.toml` — project configuration
- `specs/behavior/features/` — canonical behavior spec tree
- `specs/behavior/README.md` — managed behavior index
- Empty `tests/` and `reports/behavior/` directories

Run diagnostics at any time:

```bash
specweave doctor
```

## Quick workflow

### New feature spec

```bash
specweave create feature \
  --area auth \
  --title "User login" \
  --scenario "Successful login" \
  --given "a registered user exists" \
  --when "the user submits valid credentials" \
  --then "the user is authenticated"
```

This creates `specs/behavior/features/auth/user-login.feature.md`.

### Generate pytest skeletons

```bash
specweave behavior generate-tests \
  --features specs/behavior/features \
  --tests-dir tests
```

### Run tests and import evidence

```bash
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report \
  reports/behavior/pytest-junit.xml \
  --format junit-xml
```

### Check coverage

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests
```

## Next steps

- {doc}`concepts` — ownership boundaries and design principles
- {doc}`behavior-workflow` — the canonical behavior workflow in detail
- {doc}`configuration` — all configuration options
