`@area-reports` `@feature-normalization`
# Feature: Report normalization and evidence generation

specweave report normalize parses runner-native reports (JUnit XML,

Cucumber JSON) and produces a normalized JSON report. It enforces

fail-closed semantics for acceptance criteria.

## Rule: Normalization parses supported formats

`@bdd-normalize-junit-xml`
### Example: Normalization parses JUnit XML reports
* Given a JUnit XML report with passing and failing scenarios
* When specweave normalizes the report
* Then the normalized report has scenario results
* And each result has feature, scenario, status, and tags

`@bdd-normalize-cucumber-json`
### Example: Normalization parses Cucumber JSON reports
* Given a Cucumber JSON report with scenario results
* When specweave normalizes the report
* Then the normalized report has scenario results
* And each result has the correct status

`@bdd-normalize-unsupported-format`
### Example: Normalization rejects unsupported formats
* Given a report file
* When specweave normalizes with format "unknown"
* Then a ValueError is raised with "Unsupported format"

## Rule: Normalization computes overall status

`@bdd-normalize-all-passed`
### Example: Report status is passed when all scenarios pass
* Given a report where all scenarios passed
* When specweave normalizes the report
* Then the overall status is "passed"
* And the passed count equals the scenario count

`@bdd-normalize-any-failed`
### Example: Report status is failed when any scenario fails
* Given a report with one failing scenario
* When specweave normalizes the report
* Then the overall status is "failed"
* And the failed count is 1

`@bdd-normalize-skipped-fails-by-default`
### Example: Skipped scenarios fail the report by default
* Given a report with one skipped scenario
* When specweave normalizes the report
* Then the overall status is "failed"

`@bdd-normalize-allow-skipped`
### Example: Skipped scenarios pass with --allow-skipped
* Given a report with one skipped scenario
* When specweave normalizes the report with allow_skipped
* Then the overall status is "passed"

## Rule: Normalization enforces acceptance criteria coverage

`@bdd-normalize-missing-ac-coverage`
### Example: Report fails when expected AC has no passing scenario
* Given a report with no scenarios linked to @ac-0001
* When specweave normalizes with --expect-ac @ac-0001
* Then the overall status is "failed"

`@bdd-normalize-ac-covered`
### Example: Report passes when expected AC has a passing scenario
* Given a report with a passing scenario tagged @ac-0001
* When specweave normalizes with --expect-ac @ac-0001
* Then the overall status is "passed"

## Rule: Normalization generates evidence JSON

`@bdd-normalize-evidence-json`
### Example: Normalization writes Taskledger evidence JSON
* Given a JUnit XML report
* When specweave normalizes with --evidence
* Then the output is Taskledger evidence JSON
* And the JSON has task_id, criteria, and scenarios
