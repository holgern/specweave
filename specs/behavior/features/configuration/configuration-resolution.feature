@area-configuration @feature-configuration-resolution
Feature: Resolve SpecWeave configuration

  SpecWeave loads stable local configuration so the same commands work for humans,
  automation, and coding agents.

  Rule: Discover configuration predictably

    @bdd-config-prefers-public-config
    Example: Public config is preferred over hidden config
      Given specweave.toml and .specweave.toml both exist in the project root
      When SpecWeave resolves configuration
      Then SpecWeave loads specweave.toml

    @bdd-config-finds-hidden-config
    Example: Hidden config remains supported for existing projects
      Given only .specweave.toml exists in the project root
      When SpecWeave resolves configuration
      Then SpecWeave loads .specweave.toml

    @bdd-config-walks-parent-directories
    Example: Commands run from subdirectories still find the project config
      Given specweave.toml exists in a parent directory
      When I run a SpecWeave command from a nested directory
      Then SpecWeave uses the parent configuration

    @bdd-config-explicit-path
    Example: An explicit config path overrides discovery
      Given a project has multiple possible config files
      When I run specweave --config custom/specweave.toml doctor
      Then SpecWeave loads custom/specweave.toml

  Rule: Reject invalid configuration early

    @bdd-config-unsupported-schema-version
    Example: Unsupported schema versions fail clearly
      Given the config file contains an unsupported schema_version
      When SpecWeave loads configuration
      Then SpecWeave reports the unsupported schema version
      And the command exits with failure

    @bdd-config-unsupported-generation-grouping
    Example: Unsupported pytest-to-Gherkin grouping fails closed
      Given the config sets generation.group_by to an unsupported value
      When SpecWeave loads configuration
      Then SpecWeave reports that only file grouping is supported

    @bdd-config-pickles-require-official-parser
    Example: Pickle compilation requires the official parser
      Given the config enables compile_pickles
      And the config does not enable official_parser
      When SpecWeave loads configuration
      Then SpecWeave reports that compile_pickles requires official_parser
