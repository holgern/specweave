@area-config @feature-configuration
Feature: SpecWeave configuration management

  SpecWeave loads project configuration from TOML files, discovers config

  by walking parent directories, and renders deterministic defaults.

  Rule: Config discovery walks parent directories

    @bdd-config-discovery-finds-public
    Example: Discovery finds specweave.toml in current directory
      Given a file "specweave.toml" exists in the working directory
      When specweave discovers the config
      Then the config path is "specweave.toml"

    @bdd-config-discovery-finds-dotfile
    Example: Discovery still finds .specweave.toml when it is the only config
      Given a file ".specweave.toml" exists in the working directory
      When specweave discovers the config
      Then the config path is ".specweave.toml"

    @bdd-config-discovery-prefers-public
    Example: Discovery prefers specweave.toml over .specweave.toml
      Given both ".specweave.toml" and "specweave.toml" exist in the same directory
      When specweave discovers the config
      Then the config path is "specweave.toml"

    @bdd-config-discovery-walks-parents
    Example: Discovery walks parent directories when not found locally
      Given a file "specweave.toml" exists in a parent directory
      When specweave discovers the config from a subdirectory
      Then the config path points to the parent directory file

    @bdd-config-discovery-returns-none
    Example: Discovery returns None when no config exists
      Given no specweave config file exists in any parent directory
      When specweave discovers the config
      Then the config path is None

  Rule: Config loading returns defaults when no file exists

    @bdd-config-load-defaults
    Example: Loading with no file returns default config
      Given no config file path is provided
      When specweave loads the config
      Then the config has schema_version 1
      And the spelling is "behavior"
      And the features_dir is "specs/behavior/features"
      And the evidence_dir is "specs/behavior/evidence"

    @bdd-config-load-from-file
    Example: Loading reads values from a valid TOML file
      Given a config file with spelling "behaviour"
      When specweave loads the config
      Then the spelling is "behaviour"
      And the features_dir is "specs/behaviour/features"

  Rule: Config rejects unsupported schema versions

    @bdd-config-rejects-unsupported-schema
    Example: Loading fails for schema_version 2
      Given a config file with schema_version 2
      When specweave loads the config
      Then a ValueError is raised with "Unsupported specweave config schema_version"

  Rule: Default config rendering is deterministic

    @bdd-config-render-behavior
    Example: Default config renders behavior spelling
      Given the default config rendering function
      When specweave renders the default config with spelling "behavior"
      Then the output contains 'spelling = "behavior"'
      And the output contains 'features_dir = "specs/behavior/features"'
      And the output contains 'evidence_dir = "specs/behavior/evidence"'
      And the output does not contain 'document_format'

    @bdd-config-render-behaviour
    Example: Default config renders behaviour spelling
      Given the default config rendering function
      When specweave renders the default config with spelling "behaviour"
      Then the output contains 'spelling = "behaviour"'
      And the output contains 'features_dir = "specs/behaviour/features"'
      And the output contains 'reports_state_dir = "reports/behaviour/specweave"'
