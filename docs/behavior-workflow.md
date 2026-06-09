# Behavior Workflow

The canonical workflow is classic Gherkin under `specs/behavior/features` plus
plain pytest under `tests`.

## 1. Initialize

```bash
specweave init
specweave doctor
```

## 2. Create or infer specs

New feature:

```bash
specweave create feature \
  --area auth \
  --title "Password login" \
  --scenario "Reject invalid password" \
  --given "a registered user exists" \
  --when "the user submits an invalid password" \
  --then "login is rejected"
```

Brownfield from tests:

```bash
specweave create gherkin --from-tests tests --out specs/behavior/features
specweave review specs
```

## 3. Generate index and tests

```bash
specweave behavior index
specweave behavior generate-tests --features specs/behavior/features --tests-dir tests
```

## 4. Check static coverage in both directions

```bash
specweave review coverage --view both --show gaps
```

Use feature-side gaps to add missing `# specweave:` markers or
`@pytest.mark.specweave` mappings. Use pytest-side gaps to decide whether
unmapped tests should be linked to existing scenarios, covered by a new
scenario, or left outside behavior coverage intentionally.

## 5. Import evidence

```bash
pytest --junitxml=specs/behavior/reports/pytest-junit.xml
specweave behavior import-report specs/behavior/reports/pytest-junit.xml --format junit-xml
```

Normalized evidence is written to `specs/behavior/evidence`. Generated runner
artifacts belong under `specs/behavior/reports` and `specs/behavior/reports/specweave`.
