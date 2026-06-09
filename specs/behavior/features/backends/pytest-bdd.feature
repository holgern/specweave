@area-backends @feature-pytest-bdd
Feature: pytest-bdd step-skeleton backend

  SpecWeave provides a legacy/bridge backend that generates pytest-bdd step
  definition skeletons from parsed Gherkin features. It deduplicates repeated
  steps, collects scenarios from Rule blocks, and uses source-path filenames
  when available.

  Rule: Backend registry

    @bdd-backend-registry
    Example: Supported backends include behave and pytest-bdd
      Given specweave is initialized
      When the backend registry is queried
      Then "behave" is a supported backend
      And "pytest-bdd" is a supported backend
      And the pytest-bdd backend resolves to its generator function

    @bdd-backend-unsupported
    Example: Unsupported Cucumber backends report clear messages
      Given specweave is initialized
      When the backend registry is queried for unsupported names
      Then "cucumber-js" is listed as unsupported
      And "cucumber-jvm" is listed as unsupported
      And requesting either raises a ValueError with "not yet supported"

  Rule: Generate pytest-bdd skeleton

    @bdd-backend-pytest-bdd-skeleton
    Example: Skeleton includes pytest-bdd imports, scenarios, and step decorators
      Given a Feature with a Scenario containing Given, When, Then steps
      When specweave generates the pytest-bdd skeleton
      Then the skeleton imports from pytest_bdd
      And the skeleton includes "scenarios(" referencing the feature file
      And the skeleton has @given with parsers.parse and target_fixture
      And the skeleton has @when with parsers.parse
      And the skeleton has @then with parsers.parse
      And each step function raises NotImplementedError

    @bdd-backend-pytest-bdd-dedup
    Example: Repeated steps appear only once in the skeleton
      Given a Feature where the same step text appears as Given and And
      When specweave generates the pytest-bdd skeleton
      Then the step text appears only once in parsers.parse calls

    @bdd-backend-pytest-bdd-rule-scenarios
    Example: Steps inside Rule blocks are included
      Given a Feature with a Rule containing a Scenario with Given, When, Then
      When specweave generates the pytest-bdd skeleton
      Then steps from the Rule Scenario are included
      And step text from Given, When, Then inside the Rule appears in parsers.parse calls

    @bdd-backend-pytest-bdd-source-path
    Example: Skeleton uses the source feature filename when available
      Given a Feature with source_path set to a specific filename
      When specweave generates the pytest-bdd skeleton
      Then the scenarios() call references that filename
