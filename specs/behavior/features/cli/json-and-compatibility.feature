@area-cli @feature-json-and-compatibility
Feature: Provide scriptable CLI output and compatibility aliases

  SpecWeave commands are usable by humans and by coding agents that need stable
  machine-readable output.

  Rule: Return JSON for automation

    @bdd-cli-global-json-version
    Example: Version supports global JSON output
      Given SpecWeave is installed
      When I run specweave --json version
      Then SpecWeave prints a JSON object with schema_version, command, status, and version

    @bdd-cli-create-feature-json
    Example: Create feature reports machine-readable ids
      Given I create a feature with --json
      When the command succeeds
      Then the JSON output includes the feature path and scenario ids

    @bdd-cli-review-specs-json
    Example: Review specs supports JSON output
      Given a project has behavior specs and pytest tests
      When I run specweave --json review specs
      Then the output contains status, summary, and findings

  Rule: Keep compatibility commands routed to the behavior workflow

    @bdd-cli-bdd-check-alias
    Example: bdd check aliases behavior check
      Given behavior feature files exist
      When I run specweave bdd check
      Then SpecWeave performs the same linting as specweave behavior check

    @bdd-cli-bdd-coverage-alias
    Example: bdd coverage aliases behavior coverage
      Given behavior feature files and pytest tests exist
      When I run specweave bdd coverage
      Then SpecWeave performs the same static coverage check as specweave behavior coverage

    @bdd-cli-update-alias
    Example: update aliases create gherkin update mode
      Given pytest tests exist
      When I run specweave update --from-tests tests
      Then SpecWeave updates generated Gherkin using file grouping
