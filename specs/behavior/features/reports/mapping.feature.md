`@area-reports` `@feature-mapping`
# Feature: Report tag mapping and acceptance coverage

The reports.mapping module extracts BDD and acceptance criterion IDs

from scenario tags and summarizes acceptance criterion coverage from

normalized scenario results.

## Rule: Tag extraction identifies BDD and AC IDs

`@bdd-tag-extraction-bdd`
### Example: Extraction finds @bdd-* tags
* Given scenario tags include "@bdd-login-success @area-auth"
* When specweave extracts IDs from tags
* Then bdd_ids includes "bdd-login-success"

`@bdd-tag-extraction-ac`
### Example: Extraction finds @ac-* tags
* Given scenario tags include "@bdd-login @ac-0001 @ac-0002"
* When specweave extracts IDs from tags
* Then ac_ids includes "ac-0001" and "ac-0002"

`@bdd-tag-extraction-empty`
### Example: Extraction returns empty lists when no matching tags
* Given scenario tags include "@area-auth @feature-login"
* When specweave extracts IDs from tags
* Then bdd_ids is empty
* And ac_ids is empty

## Rule: Criteria summarization groups by AC ID

`@bdd-criteria-summary`
### Example: Summarization groups scenarios by acceptance criterion
* Given scenario results with @ac-0001 tags
* When specweave summarizes criteria
* Then a criterion entry exists for "ac-0001"
* And the entry has the correct status

`@bdd-criteria-fail-closed`
### Example: Failed scenarios fail the linked criterion
* Given a scenario tagged @ac-0001 with status "failed"
* When specweave summarizes criteria
* Then the criterion "ac-0001" status is "failed"

`@bdd-criteria-missing-coverage`
### Example: Expected AC with no scenarios fails coverage
* Given no scenarios linked to @ac-0001
* When specweave requires expected coverage for @ac-0001
* Then the coverage status is "failed"
