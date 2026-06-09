[![PyPI - Version](https://img.shields.io/pypi/v/specweave)](https://pypi.org/project/specweave/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/specweave)
![PyPI - Downloads](https://img.shields.io/pypi/dm/specweave)
[![codecov](https://codecov.io/gh/holgern/specweave/graph/badge.svg?token=CjRFwWvyYm)](https://codecov.io/gh/holgern/specweave)

# specweave

SpecWeave translates between canonical Gherkin behavior specs, plain pytest
enforcement, and normalized execution evidence.

It is not a task ledger, architecture ledger, or CI system.

## Canonical layout

```text
specweave.toml
specs/behavior/README.md
specs/behavior/manifest.json
specs/behavior/features/<area>/<feature>.feature
specs/behavior/evidence/*.json
specs/behavior/mappings/taskledger/*.json
tests/test_<area>_<feature>.py
reports/behavior/*.xml
reports/behavior/specweave/*.json
```

Hidden `.specweave.toml` is still discovered for existing projects, but
`specweave.toml` is the default config file and classic `.feature` is the only
canonical feature format.

## Behavior workflow

```bash
specweave init
specweave doctor
specweave create gherkin --from-tests tests --out specs/behavior/features
specweave review specs
specweave review coverage --view both --show gaps
specweave behavior index
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report reports/behavior/pytest-junit.xml --format junit-xml
```

## Classic Gherkin only

Canonical specs use classic Gherkin:

```gherkin
@area-auth @feature-password-login
Feature: Password login
  Users authenticate with a password.

  @rule-invalid-password
  Rule: Invalid passwords are rejected

    @bdd-password-login-invalid-password @ac-0001
    Example: Reject invalid password
      Given a registered user exists
      When the user submits an invalid password
      Then login is rejected
      And no authenticated session is created
```

Legacy `.feature.md` files are no longer supported as canonical specs.

## Evidence and mappings

- normalized evidence: `specs/behavior/evidence`
- Taskledger mapping artifacts: `specs/behavior/mappings/taskledger`
- generated runner output: `reports/behavior`
- SpecWeave runner summaries: `reports/behavior/specweave`

Import pytest/JUnit evidence with:

```bash
specweave behavior import-report \
  reports/behavior/pytest-junit.xml \
  --format junit-xml \
  --out specs/behavior/evidence/pytest-evidence.json
```

## Optional Taskledger integration

Taskledger exchange is file-based:

```bash
specweave behavior import-taskledger \
  specs/behavior/mappings/taskledger/task-0123.json \
  --out specs/behavior/features/task-management/plan-gates.feature

specweave create taskledger-task \
  --feature specs/behavior/features/task-management/plan-gates.feature \
  --out specs/behavior/mappings/taskledger/draft.json
```

Trace and cross-ledger diagnostics remain read-only:

```bash
specweave trace @bdd-login-success --format json
specweave combi check --json reports/behavior/specweave/combi-check.json
```

## Installation

```bash
pip install specweave
pip install specweave[gherkin]   # optional official Cucumber parser
pip install -e ".[dev]"          # development tools
```

## Development

```bash
pytest -q
ruff check .
ruff format --check .
mypy specweave
```

## License

Apache 2.0
