@area-gherkin @feature-writer
Feature: Gherkin feature file writing

  The Gherkin writer serializes Feature dataclass instances back to

  canonical Gherkin text. It preserves tags, rules, scenarios, and steps.

  Rule: Writer produces canonical Gherkin output

    @bdd-writer-basic-feature
    Example: Writer serializes a feature with scenarios
      Given a Feature with one Scenario and steps
      When specweave writes the feature
      Then the output contains "Feature:" with the title
      And the output contains "Scenario:" or "Example:" with the title
      And the output contains Given, When, Then steps

    @bdd-writer-rules
    Example: Writer serializes Rule blocks
      Given a Feature with a Rule containing scenarios
      When specweave writes the feature
      Then the output contains "Rule:" with the rule title
      And the scenarios are indented under the rule

    @bdd-writer-tags
    Example: Writer preserves tags at all levels
      Given a Feature with tags on feature, rule, and scenario
      When specweave writes the feature
      Then the output contains feature-level tags before "Feature:"
      And the output contains rule-level tags before "Rule:"
      And the output contains scenario-level tags before the scenario

    @bdd-writer-descriptions
    Example: Writer preserves descriptions
      Given a Feature with descriptions on feature and scenario
      When specweave writes the feature
      Then the feature description appears after "Feature:"
      And the scenario description appears after the scenario header

    @bdd-writer-roundtrip
    Example: Parsing then writing produces equivalent output
      Given a canonical Gherkin feature text
      When specweave parses and then writes the feature
      Then the output is semantically equivalent to the input
