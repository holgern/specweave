@area-behavior @feature-autolink
Feature: Behavior autolink
  SpecWeave can convert high-confidence generated scenario ids into explicit pytest mappings.

  @rule-generated-id-autolink
  Rule: Generated id autolinking

    @bdd-autolink-generated-id-dry-run @ac-0001 @ac-0005
    Example: Dry-run reports generated id mappings without writing files
      Given generated Gherkin scenarios from pytest tests
      And plain pytest tests without SpecWeave mapping metadata
      When the agent runs behavior autolink without apply
      Then SpecWeave reports planned mapping metadata
      And no pytest file is changed

    @bdd-autolink-generated-id-apply @ac-0002 @ac-0003
    Example: Apply writes explicit mapping metadata
      Given a generated scenario id matching a pytest function name
      When the agent runs behavior autolink with apply
      Then SpecWeave writes explicit mapping metadata above the pytest test
      And decorators and class indentation remain valid

    @bdd-autolink-ambiguous-candidate @ac-0004
    Example: Ambiguous matches are reported instead of guessed
      Given two generated scenarios that can map to the same pytest function name
      When the agent runs behavior autolink
      Then SpecWeave reports the match as ambiguous
      And no mapping metadata is written for that test

    @bdd-autolink-refresh-wrapper @ac-0006
    Example: Refresh regenerates common behavior artifacts
      Given a configured SpecWeave project
      When the agent runs behavior refresh with coverage mappings and index enabled
      Then SpecWeave regenerates the configured coverage report mapping inventory and behavior index
