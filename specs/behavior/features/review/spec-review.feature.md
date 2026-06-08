`@area-review` `@feature-spec-review`

# Feature: Behavior spec review

specweave review specs aggregates lint, coverage, and convention findings

to report on the health of the behavior specification suite.

## Rule: Review reports feature and scenario counts

`@bdd-review-counts`

### Example: Review reports feature and scenario statistics

- Given canonical behavior feature files exist
- When specweave reviews the specs
- Then the summary includes features count
- And the summary includes scenarios count
- And the summary includes bound count

## Rule: Review reports missing bindings

`@bdd-review-missing-bindings`

### Example: Review warns about unbound scenarios

- Given a feature file with an unbound scenario
- When specweave reviews the specs
- Then a finding with code "SWCOV001" is reported
- And the status is "failed"

## Rule: Review reports needs-review tags

`@bdd-review-needs-review`

### Example: Review warns about @needs-review scenarios

- Given a feature file with a scenario tagged @needs-review
- When specweave reviews the specs
- Then a finding with code "SWREV001" is reported

## Rule: Review reports deprecated paths

`@bdd-review-deprecated-paths`

### Example: Review warns about deprecated paths

- Given feature files exist under a deprecated path
- When specweave reviews the specs
- Then a finding with code "SWREV002" is reported

## Rule: Review reports forbidden pytest-bdd usage

`@bdd-review-forbidden-pytest-bdd`

### Example: Review errors on pytest-bdd usage

- Given a test file importing pytest_bdd
- When specweave reviews the specs
- Then a finding with code "SWREV003" is reported
- And the finding level is "error"

## Rule: Review aggregates lint findings

`@bdd-review-lint-findings`

### Example: Review includes lint errors and warnings

- Given a feature file with lint issues
- When specweave reviews the specs
- Then the findings include lint error codes
- And the summary counts include the lint findings
