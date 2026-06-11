@area-setup @feature-project-initialization
Feature: Initialize a SpecWeave project

  SpecWeave prepares a Python repository for behavior-first traceability without
  taking ownership of the project test runner, task system, or architecture records.

  Rule: Create the canonical behavior layout

    @bdd-init-default-layout
    Example: Initialize a new project with default behavior paths
      Given a Python project without SpecWeave configuration
      When I run specweave init
      Then SpecWeave creates specweave.toml
      And SpecWeave creates specs/behavior/features
      And SpecWeave creates specs/behavior/README.md
      And SpecWeave does not create a hidden runtime state directory

    @bdd-init-explicit-hidden-config
    Example: Initialize with an explicitly requested hidden config file
      Given a Python project without SpecWeave configuration
      When I run specweave --config .specweave.toml init
      Then SpecWeave creates .specweave.toml
      And the configured paths still point into specs/behavior

    @bdd-init-british-spelling
    Example: Initialize with British spelling when requested
      Given a Python project without SpecWeave configuration
      When I run specweave init --spelling behaviour
      Then SpecWeave creates specs/behaviour/features
      And the generated test command writes reports under specs/behaviour/reports

  Rule: Preserve project-owned files

    @bdd-init-idempotent
    Example: Re-running init reports existing files instead of failing
      Given a project already initialized by SpecWeave
      When I run specweave init again
      Then SpecWeave reports existing generated paths
      And the command exits successfully

    @bdd-init-preserves-non-managed-readme
    Example: Init does not overwrite a project-owned README
      Given specs/behavior/README.md exists without the SpecWeave managed marker
      When I run specweave init
      Then SpecWeave leaves the README content unchanged
      And SpecWeave reports the README as skipped

    @bdd-init-force-overwrites-managed-config
    Example: Force rewrites only SpecWeave-managed generated files
      Given a project contains a generated SpecWeave config
      When I run specweave init --force
      Then SpecWeave rewrites the generated config
      And SpecWeave does not overwrite non-managed behavior documentation
