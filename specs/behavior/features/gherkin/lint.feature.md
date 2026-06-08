`@area-gherkin` `@feature-lint`

# Feature: Gherkin feature file linting

The linter checks canonical behavior feature files for structural problems,

missing tags, deprecated paths, and duplicate identifiers.

## Rule: Lint checks feature structure

`@bdd-lint-single-feature` `@manual`

### Example: Lint errors on multiple Feature lines

- Given a feature file with two "Feature:" lines
- When specweave lints the feature
- Then a finding with code "SWBEH002" is reported
- And the finding level is "error"

`@bdd-lint-empty-feature-title` `@manual`

### Example: Lint errors on empty feature title

- Given a feature file with an empty feature title
- When specweave lints the feature
- Then a finding with code "SWBEH003" is reported

`@bdd-lint-empty-scenario-title` `@manual`

### Example: Lint errors on empty scenario title

- Given a feature file with an empty scenario title
- When specweave lints the feature
- Then a finding with code "SWBEH004" is reported

`@bdd-lint-missing-given-when-then` `@manual`

### Example: Lint errors when Given/When/Then are missing

- Given a feature file with a scenario missing Then step
- When specweave lints the feature
- Then a finding with code "SWBEH005" is reported

`@bdd-lint-empty-rule` `@manual`

### Example: Lint errors on Rule without scenarios

- Given a feature file with a Rule containing no scenarios
- When specweave lints the feature
- Then a finding with code "SWBEH006" is reported

## Rule: Lint checks tag conventions

`@bdd-lint-duplicate-bdd-tags` `@manual`

### Example: Lint errors on duplicate @bdd-\* tags

- Given two scenarios sharing the same @bdd-\* tag
- When specweave lints the features
- Then a finding with code "SWBEH007" is reported for each location

`@bdd-lint-missing-bdd-tag` `@manual`

### Example: Lint warns when scenario lacks @bdd-\* tag

- Given a scenario without any @bdd-\* tag
- When specweave lints with require_scenario_ids
- Then a finding with code "SWBEH014" is reported

`@bdd-lint-task-tags-discouraged` `@manual`

### Example: Lint warns on task-specific tags in features

- Given a feature file with a @task-\* tag on a scenario
- When specweave lints the feature
- Then a finding with code "SWBEH013" is reported

## Rule: Lint checks file paths

`@bdd-lint-canonical-path` `@manual`

### Example: Lint errors on features outside canonical path

- Given a feature file not under "specs/behavior/features"
- When specweave lints the feature
- Then a finding with code "SWBEH009" is reported

`@bdd-lint-area-subdirectory` `@manual`

### Example: Lint warns when feature is not in area subdirectory

- Given a feature file directly under "specs/behavior/features"
- When specweave lints the feature
- Then a finding with code "SWBEH010" is reported

`@bdd-lint-deprecated-path` `@manual`

### Example: Lint warns on deprecated feature paths

- Given a feature file under "specs/bdd/features"
- When specweave lints the feature
- Then a finding with code "SWBEH015" is reported

## Rule: Strict mode reports unsupported constructs

`@bdd-lint-strict-unsupported` `@manual`

### Example: Strict mode warns on Scenario Outline

- Given a feature file with "Scenario Outline:"
- When specweave lints the feature with strict mode
- Then a finding with code "SWBEH008" is reported
