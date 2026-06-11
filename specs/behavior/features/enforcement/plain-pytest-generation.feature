@area-enforcement @feature-plain-pytest-generation
Feature: Generate plain pytest enforcement from behavior specs

  SpecWeave uses plain pytest as the default enforcement path and records explicit
  mappings from tests back to behavior scenarios.

  Rule: Create pytest skeletons from feature files

    @bdd-generate-tests-single-feature
    Example: Generate a pytest skeleton for one feature
      Given a canonical behavior feature with two scenarios
      When I run specweave behavior generate-tests path/to/feature.feature
      Then SpecWeave writes a pytest test file for the feature
      And the file contains one test function per scenario

    @bdd-generate-tests-batch
    Example: Generate pytest skeletons for all features
      Given multiple feature files exist under specs/behavior/features
      When I run specweave behavior generate-tests --features specs/behavior/features
      Then SpecWeave writes one pytest file per feature

    @bdd-generate-tests-stable-mapping-markers
    Example: Generated tests contain explicit SpecWeave mappings
      Given a behavior scenario has a stable @bdd-* tag
      When SpecWeave generates the pytest skeleton
      Then the test function contains mapping metadata for the feature path
      And the test function contains mapping metadata for the scenario id

    @bdd-generate-tests-docstrings-and-steps
    Example: Generated tests preserve scenario intent for developers
      Given a behavior scenario has a title and Given When Then steps
      When SpecWeave generates the pytest skeleton
      Then the test function docstring includes the scenario title
      And the function body contains comments for each scenario step

    @bdd-generate-tests-avoids-long-lines
    Example: Mapping metadata does not force excessive source lines
      Given a feature path and scenario id are long
      When SpecWeave generates the pytest skeleton
      Then the mapping metadata remains readable by the Python linter
