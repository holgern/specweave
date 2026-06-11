# Behavior Workflow

The canonical workflow is classic Gherkin under `specs/behaviour/features` plus
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
specweave create gherkin --from-tests tests --out specs/behaviour/features
specweave review specs
```

## 3. Review coverage before manual scanning

Start traceability work with SpecWeave's review commands instead of broad source greps:

```bash
specweave review specs
specweave review coverage --view both --show gaps --format markdown --out specs/behaviour/reports/specweave/coverage-gaps.md
specweave behaviour mappings --tests tests --format json
```

If features were generated from pytest and coverage shows many candidate tests, run a dry-run autolink first:

```bash
specweave behaviour autolink --features specs/behaviour/features --tests tests --strategy generated-id
specweave behaviour autolink --features specs/behaviour/features --tests tests --strategy generated-id --apply
```

Review the dry-run before using `--apply`. Autolink creates traceability metadata only. It does not validate behavior evidence.

## 4. Generate index and tests

```bash
specweave behaviour generate-tests --features specs/behaviour/features --tests-dir tests
specweave behaviour index --features specs/behaviour/features --out specs/behaviour/README.md --manifest specs/behaviour/manifest.json --tests-dir tests
```

## 5. Check static coverage in both directions

```bash
specweave review coverage --view both --show gaps
```

Use feature-side gaps to add missing `@pytest.mark.specweave` mappings or short `# sw:` comments. Prefer decorators for new or generated tests because Python string literals can be split to satisfy Ruff line length. Do not add file-level `# ruff: noqa: E501` only because of SpecWeave mapping metadata. Use pytest-side gaps to decide whether unmapped tests should be linked to existing scenarios, covered by a new scenario, or left outside behavior coverage intentionally.

## 5. Import evidence

```bash
pytest --junitxml=specs/behaviour/reports/pytest-junit.xml
specweave behaviour import-report specs/behaviour/reports/pytest-junit.xml --format junit-xml
```

Normalized evidence is written to `specs/behaviour/evidence`. Generated runner
artifacts belong under `specs/behaviour/reports` and `specs/behaviour/reports/specweave`.

## Refresh common artifacts

Use the wrapper when you need the standard coverage, mapping inventory, and index artifacts from config paths:

```bash
specweave behaviour refresh --coverage --mappings --index
```

This avoids repeated shell redirection and keeps output paths consistent.
