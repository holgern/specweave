# Getting Started

## Initialize a project

```bash
specweave init --mode both
specweave doctor
```

This creates `specweave.toml`, `specs/behaviour/features`, and, when requested,
`specs/specifications`.

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
specweave behaviour generate-tests --features specs/behaviour/features --tests-dir tests
pytest --junitxml=specs/behaviour/reports/pytest-junit.xml
specweave behaviour import-report specs/behaviour/reports/pytest-junit.xml --format junit-xml
specweave specifications index
specweave specifications coverage --view both --show gaps
```
