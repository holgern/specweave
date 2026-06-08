`@area-bdd` `@feature-convert`

# Feature: Task-BDD JSON to Gherkin conversion

SpecWeave converts between its internal Task-BDD JSON model and canonical
Gherkin Feature files. Round-trips preserve task, rule, bdd, and acceptance
criterion IDs. Top-level examples become top-level scenarios, and And/But
step grouping is preserved.

## Rule: Export Task-BDD spec to classic Gherkin

`@bdd-bridge-export-to-gherkin`

### Example: Task-BDD spec renders as target Gherkin with all tags

- Given a Task-BDD spec with task_id, feature title, rules, and examples
- When specweave exports it to a Gherkin Feature
- Then the output includes `@task-<task_id>`
- And the output includes `Feature: <title>`
- And the output includes `@rule-<id>` for each rule
- And the output includes `@bdd-<id>`, `@task-<id>`, `@rule-<id>`, `@ac-<id>` on scenarios
- And the output includes Scenario title
- And the output includes Given, When, Then steps

## Rule: Round-trip preserves all IDs and content

`@bdd-bridge-roundtrip-ids`

### Example: Export then import preserves task, rule, bdd, and ac ids

- Given a Task-BDD spec with known ids
- When the spec is exported to Gherkin and re-imported
- Then the re-imported task_id matches the original
- Then the re-imported feature title matches
- Then the re-imported rule id and title match
- Then the re-imported example id, rule_id, and acceptance criteria match
- Then Given, When, and Then steps match

`@bdd-bridge-multiple-ac`

### Example: Multiple acceptance criteria and custom tags survive round-trip

- Given a Task-BDD spec with multiple `@ac-*` ids and a custom tag
- When the spec is exported to Gherkin and re-imported
- Then both acceptance criteria ids are preserved
- And the custom tag is preserved
- And the bdd id is unchanged

## Rule: Top-level examples become top-level scenarios

`@bdd-bridge-top-level`

### Example: Example without rule_id renders as top-level scenario

- Given a Task-BDD spec with an example that has no rule_id
- When the spec is exported to Gherkin
- Then the Feature has no rules
- And the Feature has one top-level Scenario
- And the Scenario title matches the example title

## Rule: And/But steps group correctly

`@bdd-bridge-and-but-steps`

### Example: Multiple Given/When/Then entries render as And/But steps

- Given a Task-BDD spec where examples have multiple Given, When, and Then entries
- When the spec is exported to Gherkin and re-imported
- Then the re-imported example has all Given entries preserved
- Then the re-imported example has all When entries preserved
- Then the re-imported example has all Then entries preserved

## Rule: JSON store read/write

`@bdd-bridge-json-roundtrip`

### Example: save then load is idempotent

- Given a Task-BDD spec
- When it is saved to a JSON file and loaded back
- Then the loaded spec equals the original
- And the JSON file contains the task_id
- And the acceptance_criteria field is an array

`@bdd-bridge-json-to-feature-to-json`

### Example: JSON to feature to JSON preserves all ids

- Given a Task-BDD JSON payload with task, rules, and examples
- When the JSON is loaded, converted to Gherkin, converted back, and saved
- Then the final JSON task_id matches the original
- And the final JSON rule id matches
- And the final JSON example id matches
- And the final JSON acceptance criteria array matches
