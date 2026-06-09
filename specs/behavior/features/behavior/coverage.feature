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
