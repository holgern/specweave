# Getting Started

## Initialize a project

```bash
specweave init
specweave doctor
```

This creates `specweave.toml`, `specs/behavior/features`, and the default
evidence/report directories.

## Create a feature

```bash
specweave create feature \
  --area auth \
  --title "Password login" \
  --scenario "Reject invalid password" \
  --given "a registered user exists" \
  --when "the user submits an invalid password" \
  --then "login is rejected"
```

## Generate tests and import evidence

```bash
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report reports/behavior/pytest-junit.xml --format junit-xml
```
