`@area-integrations` `@feature-taskledger`

# Feature: Taskledger integration

SpecWeave exchanges files with Taskledger for task drafts and behavior

imports. The integration is file-based and does not require Taskledger

as a runtime dependency.

## Rule: Taskledger task draft generation

`@bdd-taskledger-draft`

### Example: create taskledger-task generates a draft JSON

- Given a canonical behavior feature file with @bdd-\* tags
- When specweave runs "create taskledger-task"
- Then a draft JSON file is written
- And the draft has schema_version 1
- And the draft includes scenarios extracted from the feature

`@bdd-taskledger-draft-ac-mapping` `@manual`

### Example: Draft maps @ac-\* tags to acceptance criteria

- Given a feature file with scenarios tagged @ac-0001
- When specweave runs "create taskledger-task"
- Then the draft includes acceptance criteria for @ac-0001

## Rule: Taskledger behavior import

`@bdd-taskledger-import`

### Example: import-taskledger creates a feature from Taskledger export

- Given a Taskledger acceptance export JSON file
- When specweave runs "behavior import-taskledger"
- Then a canonical behavior feature file is written
- And the feature contains scenarios from the export

## Rule: Taskledger evidence generation

`@bdd-taskledger-evidence`

### Example: report normalize generates Taskledger-compatible evidence

- Given a JUnit XML report with scenario results
- When specweave normalizes with --evidence
- Then the output matches the Taskledger evidence JSON shape
- And the output has task_id, criteria, and scenarios arrays
