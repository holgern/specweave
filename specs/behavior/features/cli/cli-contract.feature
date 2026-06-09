@area-cli @feature-cli-contract
Feature: SpecWeave CLI contract

  The SpecWeave CLI provides commands for behavior-driven development

  workflows. It supports root options for config path and JSON output,

  and preserves stable exit codes.

  Rule: Root options work across all commands

    @bdd-cli-config-option
    Example: --config selects an explicit config path
      Given a config file at a custom path
      When specweave runs with --config pointing to that file
      Then the custom config is loaded

    @bdd-cli-json-output
    Example: --json produces machine-readable output
      Given specweave is installed
      When specweave runs "version" with --json
      When specweave runs "version" with --json
      Then the output is valid JSON
      And the JSON has schema_version 1
      And the JSON has status "ok"

    @bdd-cli-json-init
    Example: init --json produces machine-readable output
      Given an empty project directory
      When specweave runs "init --json"
      When specweave runs "init --json"
      Then the output is valid JSON
      And the JSON has command "init"
      And the JSON has created and existing arrays

  Rule: Behavior subcommands work correctly

    @bdd-cli-behavior-check
    Example: behavior check lints feature files
      Given canonical behavior feature files exist
      When specweave runs "behavior check"
      Then the command completes successfully

    @bdd-cli-behavior-index
    Example: behavior index generates index and manifest
      Given canonical behavior feature files exist
      When specweave runs "behavior index"
      Then the behavior index file is written
      And the manifest file is written

    @bdd-cli-behavior-generate-tests
    Example: behavior generate-tests creates pytest skeletons
      Given a canonical behavior feature file
      When specweave runs "behavior generate-tests"
      Then a pytest skeleton file is created

    @bdd-cli-behavior-coverage
    Example: behavior coverage checks spec-to-test mapping
      Given canonical behavior feature files and tests exist
      When specweave runs "behavior coverage"
      Then the coverage JSON is output

    @bdd-cli-behavior-import-report
    Example: behavior import-report imports JUnit XML
      Given a JUnit XML report and mapped test files
      When specweave runs "behavior import-report"
      Then evidence JSON is written

  Rule: BDD compatibility aliases work

    @bdd-cli-bdd-check-alias
    Example: bdd check is an alias for behavior check
      Given canonical behavior feature files exist
      When specweave runs "bdd check"
      Then the command behaves identically to "behavior check"

    @bdd-cli-bdd-index-alias
    Example: bdd index is an alias for behavior index
      Given canonical behavior feature files exist
      When specweave runs "bdd index"
      Then the command behaves identically to "behavior index"

  Rule: Create subcommands work correctly

    @bdd-cli-create-feature
    Example: create feature writes a new Gherkin feature file
      Given an empty project directory
      When specweave runs "create feature" with area, title, scenario, given, when, then
      When specweave runs "create feature" with area, title, scenario, given, when, then
      Then a feature file is created
      And the file contains the specified scenario

    @bdd-cli-create-gherkin
    Example: create gherkin generates features from tests
      Given existing pytest test files
      When specweave runs "create gherkin --from-tests tests"
      Then feature files are generated

    @bdd-cli-create-plan
    Example: create plan generates an implementation plan
      Given a canonical behavior feature file
      When specweave runs "create plan"
      Then a plan Markdown file is written

  Rule: Exit codes reflect result status

    @bdd-cli-exit-doctor-failed
    Example: doctor exits non-zero when errors found
      Given a project with config errors
      When specweave runs "doctor"
      Then the exit code is 1

    @bdd-cli-exit-check-errors
    Example: behavior check exits non-zero on lint errors
      Given a feature file with lint errors
      When specweave runs "behavior check"
      Then the exit code is 1

    @bdd-cli-exit-normalize-failed
    Example: report normalize exits non-zero when report failed
      Given a JUnit XML report with failures
      When specweave runs "report normalize"
      Then the exit code is 1
