@area-behavior @feature-coverage
Feature: Static behavior coverage checks

  specweave behavior coverage checks the mapping between behavior feature

  files and plain pytest test files. It reports missing bindings, stale

  bindings, deprecated paths, and forbidden pytest-bdd usage.

  Rule: Coverage identifies bound and unbound scenarios

    @bdd-coverage-bound-scenario
    Example: Coverage marks bound scenarios
      Given a feature file with a scenario mapped to a pytest test
      When specweave builds the behavior coverage
      Then the scenario appears in scenarios_bound count
      And the scenario is not in missing_bindings

    @bdd-coverage-unbound-scenario
    Example: Coverage reports missing bindings
      Given a feature file with a scenario not mapped to any test
      When specweave builds the behavior coverage
      Then the scenario appears in missing_bindings
      And the reason is "missing_scenario_binding"

    @bdd-coverage-missing-test-file
    Example: Coverage reports missing test files
      Given a feature file with no corresponding test file
      When specweave builds the behavior coverage
      Then a missing_binding entry has reason "missing_test_file"

  Rule: Coverage detects stale bindings

    @bdd-coverage-stale-binding
    Example: Coverage reports bindings to non-existent features
      Given a test file with a specweave marker referencing a missing feature
      When specweave builds the behavior coverage
      Then a stale_binding entry appears
      And the reason is "missing_feature"

    @bdd-coverage-stale-scenario
    Example: Coverage reports bindings to non-existent scenarios
      Given a test file with a specweave marker referencing a missing scenario
      When specweave builds the behavior coverage
      Then a stale_binding entry has reason "missing_scenario"

  Rule: Coverage detects deprecated paths

    @bdd-coverage-deprecated-paths
    Example: Coverage reports deprecated feature paths
      Given feature files exist under "specs/bdd/features"
      When specweave builds the behavior coverage
      Then deprecated_paths contains the path

  Rule: Coverage detects forbidden pytest-bdd usage

    @bdd-coverage-forbidden-pytest-bdd
    Example: Coverage reports pytest-bdd imports in test files
      Given a test file importing pytest_bdd
      When specweave builds the behavior coverage
      Then forbidden_pytest_bdd_usages contains the test file

  Rule: Coverage skips manual and waived scenarios

    @bdd-coverage-manual-scenario
    Example: Coverage skips scenarios tagged @manual
      Given a feature file with a scenario tagged @manual
      When specweave builds the behavior coverage
      Then the scenario is not in missing_bindings

  Rule: Coverage can be viewed from pytest back to features

    @bdd-coverage-class-method-mapping
    Example: Coverage matches mappings on pytest class methods
      Given a mapped pytest method belongs to a test class
      When specweave builds the behavior coverage
      Then the class-qualified pytest test is counted as mapped
      And the pytest test is not counted as unmapped

    @bdd-coverage-pytest-unmapped
    Example: Coverage reports unmapped pytest tests
      Given a pytest test function without a SpecWeave mapping
      When specweave builds the behavior coverage
      Then the pytest test appears in unmapped_tests
      And the pytest-side summary counts it as unmapped

    @bdd-coverage-pytest-stale
    Example: Coverage reports stale pytest mappings in the pytest view
      Given a pytest test function mapped to a missing scenario id
      When specweave builds the behavior coverage
      Then the pytest test appears with status "stale"
      And the stale binding includes the missing scenario id

    @bdd-coverage-both-directions-render
    Example: Coverage renders feature and pytest directions together
      Given feature scenarios and pytest tests with mixed mapping states
      When specweave renders coverage with view "both"
      Then the output includes "Features -> pytest"
      And the output includes "Pytest -> features"

  Rule: Coverage reasons are actionable

    @bdd-coverage-missing-test-file-reason
    Example: Coverage distinguishes a missing expected test file
      Given a feature scenario whose expected pytest file does not exist
      When specweave builds the behavior coverage
      Then the missing binding reason is "missing_test_file"

    @bdd-coverage-candidate-tests
    Example: Coverage suggests candidate tests without binding by title
      Given an unmapped pytest test resembles a missing scenario
      When specweave builds the behavior coverage
      Then the scenario remains missing
      And candidate_tests contains the pytest test as a hint
