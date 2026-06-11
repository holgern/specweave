@area-navigation @feature-behavior-index-and-manifest
Feature: Generate the behavior index and manifest

  SpecWeave produces readable and machine-readable summaries of the behavior spec
  corpus so humans and tools can navigate the same source of truth.

  Rule: Build a readable behavior index

    @bdd-index-readable-feature-list
    Example: Markdown index lists behavior features
      Given multiple canonical feature files exist
      When I run specweave behavior index
      Then SpecWeave writes specs/behavior/README.md
      And the README lists each feature path and title

    @bdd-index-rules-and-scenarios
    Example: Markdown index includes rules and scenarios
      Given a feature contains rules and scenarios
      When SpecWeave builds the behavior index
      Then the README lists the rules
      And the README lists scenario ids and titles

    @bdd-index-evidence-status
    Example: Markdown index includes latest evidence when available
      Given behavior evidence exists for mapped scenarios
      When SpecWeave builds the behavior index
      Then the README includes the latest evidence status for each scenario

  Rule: Build a machine-readable manifest

    @bdd-manifest-scenario-mappings
    Example: Manifest records scenario mappings
      Given pytest tests contain explicit SpecWeave mappings
      When I run specweave behavior index
      Then SpecWeave writes specs/behavior/manifest.json
      And the manifest links feature scenario ids to pytest nodeids

    @bdd-manifest-unbound-scenario
    Example: Manifest marks unbound scenarios as missing
      Given a behavior scenario has no pytest mapping
      When SpecWeave builds the manifest
      Then the scenario automation status is missing

    @bdd-manifest-fails-on-lint-errors
    Example: Index generation refuses invalid feature files
      Given a feature file has a lint error
      When I run specweave behavior index
      Then SpecWeave reports the lint error
      And no successful manifest is claimed
