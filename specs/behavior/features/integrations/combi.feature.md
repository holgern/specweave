`@area-integrations` `@feature-combi`

# Feature: Combined cross-tool diagnostics

SpecWeave combi check performs a cross-cutting diagnostic that validates
scenarios have behavior specs, pytest mappings, evidence, and optional
Taskledger/Archledger alignment. It reports gaps and supports strict mode.

## Rule: Combi check identifies missing mappings and evidence

`@bdd-combi-check-gaps`

### Example: Scenario without pytest mapping or evidence reports gaps

- Given a feature with a scenario tagged `@bdd-*` and `@ac-*`
- And no pytest test maps to that scenario
- And no evidence file references that scenario
- When specweave runs combi check
- Then the exit code is zero
- And the output mentions the scenario count
- And the JSON output includes a "missing_pytest_mapping" gap
- And the JSON output includes a "missing_evidence" gap

## Rule: Strict mode fails on missing bdd ids

`@bdd-combi-check-strict`

### Example: Scenario without @bdd-* tag fails in strict mode

- Given a feature with a scenario that has no `@bdd-*` id tag
- When specweave runs combi check with `--strict`
- Then the exit code is non-zero
- And the output includes "missing_bdd_id"
