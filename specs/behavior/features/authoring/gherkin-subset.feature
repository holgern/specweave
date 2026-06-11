@area-authoring @feature-gherkin-subset
Feature: Enforce the supported Gherkin subset

  SpecWeave keeps the accepted Gherkin language small so feature files remain
  stable, reviewable, and directly mappable to plain pytest tests.

  Rule: Accept readable scenario structure

    @bdd-gherkin-accepts-rules-and-examples
    Example: Rules and examples are preserved
      Given a feature contains tags, a description, a Rule, and Examples
      When SpecWeave parses and writes the feature
      Then the feature title, description, tags, rules, scenarios, and steps are preserved

    @bdd-gherkin-accepts-and-but
    Example: And and But steps remain attached to the scenario
      Given a scenario uses Given, And, When, But, and Then
      When SpecWeave parses the feature
      Then the steps remain in their original order

    @bdd-gherkin-official-parser-optional
    Example: Official parser validation can be enabled
      Given the optional official Gherkin dependency is installed
      When SpecWeave validates a classic .feature file with official_parser enabled
      Then invalid Gherkin is rejected by the official parser

  Rule: Reject unsupported executable constructs

    @bdd-gherkin-rejects-background
    Example: Background is outside the supported subset
      Given a feature file contains a Background block
      When SpecWeave validates the feature
      Then SpecWeave reports an unsupported keyword error

    @bdd-gherkin-rejects-scenario-outline
    Example: Scenario Outline is outside the supported subset
      Given a feature file contains a Scenario Outline and Examples table
      When SpecWeave validates the feature
      Then SpecWeave reports an unsupported keyword error

    @bdd-gherkin-rejects-data-table
    Example: Data tables are outside the supported subset
      Given a scenario step contains a data table
      When SpecWeave validates the feature
      Then SpecWeave reports an unsupported construct error

    @bdd-gherkin-rejects-doc-string
    Example: Doc strings are outside the supported subset
      Given a scenario step contains a doc string
      When SpecWeave validates the feature
      Then SpecWeave reports an unsupported construct error
