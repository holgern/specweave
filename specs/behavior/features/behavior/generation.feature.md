`@area-behavior` `@feature-generation`

# Feature: Plain pytest skeleton generation

specweave behavior generate-tests creates plain pytest test skeletons

from canonical behavior feature files. Each scenario becomes a test

function with specweave markers and a NotImplementedError stub.

## Rule: Generation creates pytest skeletons

`@bdd-generate-single-feature` `@manual`

### Example: Generation creates a test file for a feature

- Given a canonical behavior feature file
- When specweave generates pytest skeletons
- Then a test file is created at the canonical test path
- And the test file contains "import pytest"
- And the test file contains a SPECWEAVE_FEATURE constant

`@bdd-generate-scenario-function` `@manual`

### Example: Each scenario becomes a test function

- Given a feature file with two scenarios
- When specweave generates pytest skeletons
- Then the test file contains two test functions
- And each function has a @pytest.mark.specweave decorator
- And each function raises NotImplementedError

`@bdd-generate-specweave-markers` `@manual`

### Example: Test functions have correct specweave markers

- Given a feature file with a scenario tagged @bdd-example
- When specweave generates pytest skeletons
- Then the test function has @pytest.mark.specweave with feature and scenario
- And the scenario marker references @bdd-example

`@bdd-generate-docstring` `@manual`

### Example: Test functions have docstrings with scenario details

- Given a feature file with a scenario and steps
- When specweave generates pytest skeletons
- Then the test function docstring contains the scenario title
- And the docstring contains the Given, When, Then steps

`@bdd-generate-step-comments` `@manual`

### Example: Test functions have step comments

- Given a feature file with Given, When, Then steps
- When specweave generates pytest skeletons
- Then the test function contains "# Arrange:" comment
- And the test function contains "# Act:" comment
- And the test function contains "# Assert:" comment

## Rule: Generation derives canonical test paths

`@bdd-generate-canonical-path` `@manual`

### Example: Test path is derived from feature path

- Given a feature at "specs/behavior/features/auth/login.feature"
- When specweave generates pytest skeletons
- Then the test file is at "tests/test_auth_login.py"

## Rule: Generation handles rules

`@bdd-generate-rules` `@manual`

### Example: Scenarios in rules get rule markers

- Given a feature file with a Rule containing a scenario
- When specweave generates pytest skeletons
- Then the test function marker includes the rule title

## Rule: Generation supports batch mode

`@bdd-generate-batch` `@manual`

### Example: Generation processes all features in a directory

- Given multiple feature files in the features directory
- When specweave generates pytest skeletons with --features
- Then a test file is created for each feature
