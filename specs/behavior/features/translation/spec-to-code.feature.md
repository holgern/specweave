`@area-translation` `@feature-spec-to-code`

# Feature: Gherkin-to-test skeleton generation

SpecWeave generates test skeletons from Gherkin features. It produces step
function names deterministically, binds features to backend-specific step
files, drafts feature files from structured JSON input, and fails clearly
for unsupported backends.

## Rule: Generate deterministic step function names

`@bdd-spec-to-code-step-name`

### Example: Step function name derives from keyword and text

- Given a step "Given a registered user exists"
- When specweave generates the step function name
- Then the name is "step_given_a_registered_user_exists"
- And a When step produces a name starting with "step_when"

`@bdd-spec-to-code-dedup`

### Example: Duplicate step texts get unique suffixes

- Given two steps with the same "Given a step" text
- When specweave generates the second function name with existing names
- Then the two names are different
- And the second name ends with "_2"

## Rule: Draft feature from JSON input

`@bdd-spec-to-code-draft`

### Example: draft_feature creates a valid feature file from JSON

- Given a JSON input with task_id, title, and acceptance criteria
- When specweave drafts a feature file
- Then the output file exists
- And the content includes the taskledger id reference
- And the content includes the Feature title
- And the content includes the acceptance criterion id
- And the content includes a Given step

## Rule: Bind feature to a backend step skeleton

`@bdd-spec-to-code-bind-behave`

### Example: bind_feature creates a behave step skeleton

- Given a classic Gherkin feature with scenarios and steps
- When specweave binds the feature to the "behave" backend
- Then a step file is created in the output directory
- And the file imports behave decorators
- And the file contains @given, @when, @then decorators with step text
- And each step function raises NotImplementedError

`@bdd-spec-to-code-bind-pytest-bdd`

### Example: bind_feature creates a pytest-bdd step skeleton

- Given a classic Gherkin feature with scenarios and steps
- When specweave binds the feature to the "pytest-bdd" backend
- Then a step file is created in the output directory
- And the file imports pytest_bdd
- And the file contains @when with parsers.parse

`@bdd-spec-to-code-bind-unsupported`

### Example: Unsupported backend raises clear error

- Given a classic Gherkin feature
- When specweave binds the feature to an unknown backend name
- Then a ValueError is raised with "Unsupported backend"
