`@area-behavior` `@feature-reporting`

# Feature: Behavior evidence import from pytest reports

specweave behavior import-report imports pytest/JUnit XML reports into

behavior evidence JSON. It maps test results to scenarios using specweave

markers and the manifest.

## Rule: Import maps test results to scenarios

`@bdd-import-maps-by-nodeid` `@manual`

### Example: Import maps results by normalized nodeid

- Given a JUnit XML report with a passing test
- And a test file with a specweave marker matching the nodeid
- When specweave imports the report
- Then the evidence contains a result for the mapped scenario
- And the result status is "passed"

`@bdd-import-maps-by-function-name` `@manual`

### Example: Import falls back to function name matching

- Given a JUnit XML report with a test result
- And a test file with a specweave marker matching the function name
- When specweave imports the report
- Then the evidence contains a result for the mapped scenario

`@bdd-import-maps-by-manifest` `@manual`

### Example: Import uses manifest mappings when available

- Given a JUnit XML report with a test result
- And a manifest file with the test mapping
- When specweave imports the report
- Then the evidence contains a result using the manifest mapping

## Rule: Import reports unmapped tests

`@bdd-import-unmapped-tests` `@manual`

### Example: Import reports tests without specweave markers

- Given a JUnit XML report with a test that has no specweave marker
- When specweave imports the report
- Then the evidence contains an unmapped entry
- And the unmapped entry has the test nodeid and status

## Rule: Import writes evidence JSON

`@bdd-import-writes-evidence` `@manual`

### Example: Import writes evidence to the target path

- Given a JUnit XML report
- When specweave imports the report to a target path
- Then the evidence JSON file is written
- And the file has schema_version 1
- And the file has backend "pytest"
