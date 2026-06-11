@area-authoring @feature-canonical-feature-authoring
Feature: Author canonical behavior features

  SpecWeave treats classic .feature files under specs/behavior/features as the
  readable behavior source of truth.

  Rule: Create features from structured inputs

    @bdd-create-feature-from-options
    Example: Create a feature from command options
      Given I provide an area, feature title, scenario title, and Given When Then steps
      When I run specweave create feature
      Then SpecWeave writes a .feature file under specs/behavior/features/<area>
      And the feature has area and feature tags
      And the scenario has a stable @bdd-* tag

    @bdd-create-feature-from-json-draft
    Example: Create a feature from a JSON draft
      Given a JSON draft contains feature tags, rules, scenarios, and steps
      When I run specweave create feature --from-json draft.json
      Then SpecWeave writes a canonical .feature file
      And the written feature preserves the draft scenario identifiers

    @bdd-create-feature-refuses-overwrite
    Example: Existing feature files are protected by default
      Given the target feature file already exists
      When I run specweave create feature without --force
      Then SpecWeave refuses to overwrite the file
      And the command exits with failure

    @bdd-create-feature-dry-run
    Example: Dry run reports the target without writing
      Given I provide valid feature creation inputs
      When I run specweave create feature --dry-run
      Then SpecWeave reports the feature path and scenario ids
      And no feature file is written

  Rule: Lint features as product-facing specifications

    @bdd-check-valid-feature
    Example: Valid canonical features pass behavior check
      Given a feature file uses Feature, Rule, Example, and Given When Then
      And each scenario has a stable @bdd-* tag
      When I run specweave behavior check
      Then no behavior lint findings are reported

    @bdd-check-missing-bdd-id
    Example: Scenarios without identifiers are reported
      Given a feature scenario has no @bdd-* tag
      When I run specweave behavior check
      Then SpecWeave reports the missing scenario id

    @bdd-check-missing-given-when-then
    Example: Incomplete scenarios are reported
      Given a scenario is missing one of Given, When, or Then
      When I run specweave behavior check
      Then SpecWeave reports a lint finding for the scenario

    @bdd-check-markdown-feature-rejected
    Example: Legacy markdown feature files are rejected
      Given a behavior file path ends with .feature.md
      When SpecWeave parses or checks the file
      Then SpecWeave reports that markdown feature files are unsupported
