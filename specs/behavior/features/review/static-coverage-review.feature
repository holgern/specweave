@area-review @feature-static-coverage-review
Feature: Review static behavior coverage in both directions

  SpecWeave shows whether every behavior scenario has pytest enforcement and
  whether every pytest test is intentionally connected to behavior.

  Rule: Report feature to pytest coverage

    @bdd-coverage-feature-bound
    Example: Bound scenarios are counted as covered
      Given a feature scenario has exactly one valid pytest mapping
      When I run specweave behavior coverage --view feature
      Then the scenario is shown as bound
      And feature-side coverage counts it as covered

    @bdd-coverage-feature-missing
    Example: Missing scenario bindings are reported
      Given a feature scenario has no pytest mapping
      When I run specweave behavior coverage --view feature
      Then the scenario appears in missing bindings
      And the expected pytest file is shown

    @bdd-coverage-stale-mapping
    Example: Stale mappings are reported
      Given a pytest mapping references a missing feature or scenario id
      When I run specweave behavior coverage
      Then SpecWeave reports a stale mapping with the reason

    @bdd-coverage-duplicate-mapping
    Example: Duplicate mappings are reported
      Given two pytest tests map to the same behavior scenario
      When I run specweave behavior coverage
      Then SpecWeave reports a duplicate binding

  Rule: Report pytest to feature coverage

    @bdd-coverage-test-unmapped
    Example: Unmapped pytest tests are reported in reverse coverage
      Given a pytest test has no SpecWeave mapping
      When I run specweave behavior coverage --view test
      Then the test appears in unmapped_tests
      And pytest-side coverage fails

    @bdd-coverage-test-waived
    Example: Intentional unmapped waivers are honored
      Given intentional-unmapped.json contains the pytest nodeid and reason
      When SpecWeave builds reverse coverage
      Then the pytest test is shown as waived
      And the waived test is not counted as a gap

    @bdd-coverage-both-directions
    Example: Review coverage defaults to both directions
      Given behavior scenarios and pytest tests exist
      When I run specweave review coverage
      Then the report contains Features -> pytest
      And the report contains Pytest -> features

  Rule: Keep failure modes visible

    @bdd-coverage-deprecated-paths
    Example: Deprecated behavior paths fail coverage
      Given feature files exist under deprecated specs/bdd paths
      When SpecWeave builds coverage
      Then deprecated paths are reported as findings

    @bdd-coverage-forbidden-pytest-bdd
    Example: pytest-bdd usage is rejected in the plain pytest workflow
      Given a pytest file imports pytest_bdd
      When SpecWeave builds coverage
      Then the file appears in forbidden_pytest_bdd_usages
