`@area-translation` `@feature-pytest-to-gherkin`

# Feature: Brownfield pytest-to-Gherkin generation

specweave create gherkin generates draft Gherkin feature files from

existing pytest test files. It uses AST-based discovery and groups

features by file.

## Rule: Generation discovers tests via AST

`@bdd-translate-discovers-tests`

### Example: Generation finds test functions in pytest files

- Given a pytest file with test functions
- When specweave generates Gherkin from the tests
- Then feature files are generated
- And each test function becomes a scenario

`@bdd-translate-group-by-file`

### Example: Generation groups scenarios by test file

- Given multiple pytest test files
- When specweave generates Gherkin with group_by "file"
- Then one feature file is created per test file
- And each feature file contains scenarios from that test

## Rule: Generation preserves existing features

`@bdd-translate-preserve-manual`

### Example: Generation does not overwrite manual feature files

- Given a manual feature file exists
- When specweave generates Gherkin in "update" mode
- Then the manual file is preserved
- And only draft features are updated

`@bdd-translate-force-overwrite`

### Example: Generation overwrites with --force

- Given a generated feature file exists
- When specweave generates Gherkin with --force
- Then the feature file is overwritten

## Rule: Generation marks drafts appropriately

`@bdd-translate-marks-generated`

### Example: Generated features have @generated tag

- Given pytest test files
- When specweave generates Gherkin
- Then the generated features have @generated tag
- And the generated features have @needs-review tag

## Rule: Generation supports dry-run mode

`@bdd-translate-dry-run`

### Example: Dry-run reports without writing files

- Given pytest test files
- When specweave generates Gherkin with --dry-run
- Then no feature files are written
- And the result reports what would be generated
