[![PyPI - Version](https://img.shields.io/pypi/v/specweave)](https://pypi.org/project/specweave/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/specweave)
![PyPI - Downloads](https://img.shields.io/pypi/dm/specweave)
[![codecov](https://codecov.io/gh/holgern/specweave/graph/badge.svg?token=CjRFwWvyYm)](https://codecov.io/gh/holgern/specweave)

# specweave

SpecWeave translates between canonical Gherkin behaviour specs, Markdown
specification requirements, plain pytest enforcement, and normalized execution
evidence.

It is not a task ledger, architecture ledger, or CI system.

## Canonical layout

```text
specweave.toml
specs/behaviour/README.md
specs/behaviour/manifest.json
specs/behaviour/features/<area>/<feature>.feature
specs/behaviour/evidence/*.json
specs/behaviour/mappings/taskledger/*.json
specs/specifications/README.md
specs/specifications/manifest.json
specs/specifications/product.spec.md
specs/specifications/capabilities/*.spec.md
specs/specifications/interfaces/*.spec.md
specs/specifications/integrations/*.spec.md
specs/specifications/evidence/*.json
tests/test_<area>_<feature>.py
specs/behaviour/reports/*.xml
specs/behaviour/reports/specweave/*.json
```

Hidden `.specweave.toml` is still discovered for existing projects, but
`specweave.toml` is the default config file and classic `.feature` is the only
canonical feature format.

Existing `specs/behavior/...` projects still work as deprecated compatibility
layouts. New projects should use `specs/behaviour/...`.

## Behaviour and specifications workflow

Use the golden review as the default coding-agent entry point:

```bash
specweave review golden
```

It aggregates doctor, behavior check, bidirectional coverage, mapping inventory,
and spec review. It writes review artifacts under
`specs/behaviour/reports/specweave` (or the configured behavior spelling).

The default enforcement workflow is bidirectional and plain-pytest based:

```bash
specweave init --mode both
specweave doctor
specweave create gherkin --from-tests tests --out specs/behaviour/features
specweave review coverage --view both --show gaps
specweave behaviour mappings --tests tests --format json
specweave review specs
specweave behaviour autolink --strategy generated-id
specweave behaviour autolink --strategy generated-id --apply
specweave behaviour refresh --coverage --mappings --index
specweave behaviour generate-tests --features specs/behaviour/features --tests-dir tests
pytest --junitxml=specs/behaviour/reports/pytest-junit.xml
specweave behaviour import-report specs/behaviour/reports/pytest-junit.xml --format junit-xml
specweave specifications coverage --view both --show gaps
```

pytest-bdd and behave skeletons are optional adapters. They are not required for
the default enforcement path.

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

- behaviour evidence: `specs/behaviour/evidence`
- behaviour Taskledger mappings: `specs/behaviour/mappings/taskledger`
- specifications evidence: `specs/specifications/evidence`
- generated runner output: `specs/behaviour/reports`
- SpecWeave runner summaries: `specs/behaviour/reports/specweave`

Import pytest/JUnit evidence with:

```bash
specweave behaviour import-report \
  specs/behaviour/reports/pytest-junit.xml \
  --format junit-xml \
  --out specs/behaviour/evidence/pytest-evidence.json
```

For new pytest mappings, prefer `@pytest.mark.specweave(...)` over long comment headers. Long feature paths and scenario ids can be split as adjacent Python string literals, which keeps generated tests Ruff-compatible while preserving exact mapping values.

## Optional Taskledger integration

Taskledger exchange is file-based:

```bash
specweave behaviour import-taskledger \
  specs/behaviour/mappings/taskledger/task-0123.json \
  --out specs/behaviour/features/task-management/plan-gates.feature

specweave create taskledger-task \
  --feature specs/behaviour/features/task-management/plan-gates.feature \
  --out specs/behaviour/mappings/taskledger/draft.json
```

Trace and cross-ledger diagnostics remain read-only:

```bash
specweave trace @bdd-login-success --format json
specweave combi check --json specs/behaviour/reports/specweave/combi-check.json
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
