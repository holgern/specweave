# Behavior Workflow

The canonical SpecWeave workflow has five stages: lint, index, generate,
run, and import.

## 1. Lint behavior specs

```bash
specweave behavior check
```

Validates feature files for:

- Missing `@bdd-*` IDs (when `require_bdd_ids = true`)
- Missing Given/When/Then steps (when `require_given_when_then = true`)
- Duplicate `@bdd-*` tags across the feature tree
- Structural Gherkin errors

## 2. Generate the behavior index and manifest

```bash
specweave behavior index \
  --features specs/behavior/features \
  --out specs/behavior/README.md \
  --manifest specs/behavior/manifest.json
```

This creates a Markdown index of all features and scenarios, plus a JSON
manifest for machine consumption.

## 3. Generate plain pytest skeletons

Single feature:

```bash
specweave behavior generate-tests \
  specs/behavior/features/auth/user-login.feature.md \
  --out tests/test_auth_user_login.py
```

Whole tree:

```bash
specweave behavior generate-tests \
  --features specs/behavior/features \
  --tests-dir tests
```

Generated test functions include SpecWeave source mapping markers that the
coverage scanner discovers. Existing hand-written tests are preserved unless
`--force` is used.

## 4. Check static behavior coverage

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests \
  --format text
```

Produces a report showing which `@bdd-*` scenarios have linked pytest tests
and which are uncovered.

JSON or Markdown artifacts:

```bash
specweave behavior coverage \
  --features specs/behavior/features \
  --tests tests \
  --json .specweave/reports/behavior-coverage.json
```

List raw explicit mappings:

```bash
specweave behavior mappings --tests tests --format text
```

## 5. Import pytest/JUnit evidence

```bash
pytest tests/test_auth_user_login.py \
  --junitxml=reports/behavior/auth-user-login-junit.xml

specweave behavior import-report \
  reports/behavior/auth-user-login-junit.xml \
  --format junit-xml \
  --out .specweave/evidence/auth-user-login.pytest-evidence.json
```

Evidence is normalized with fail-closed semantics. Only scenarios linked by
`@bdd-*` and `@ac-*` tags count toward acceptance-criterion coverage.

## Brownfield workflow

For existing projects with tests but no specs:

```bash
specweave init
specweave doctor
specweave create gherkin --from-tests tests --out specs/behavior/features
specweave review specs
specweave behavior index
specweave behavior generate-tests \
  --features specs/behavior/features --tests-dir tests
pytest --junitxml=reports/behavior/pytest-junit.xml
specweave behavior import-report \
  reports/behavior/pytest-junit.xml --format junit-xml
```

Specs generated from tests are marked as draft/needs-review and should be
reviewed before committing to canonical status.
