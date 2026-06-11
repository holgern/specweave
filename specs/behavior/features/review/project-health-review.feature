@area-review @feature-project-health-review
Feature: Review project health for release readiness

  SpecWeave combines lint, coverage, mapping, and evidence status into review
  commands that are suitable for local use and CI gates.

  Rule: Diagnose project setup

    @bdd-doctor-passes-initialized-project
    Example: Doctor passes for a complete configured project
      Given the configured behavior directories exist
      And feature files contain unique @bdd-* scenario ids
      When I run specweave doctor
      Then SpecWeave reports passed

    @bdd-doctor-fix-creates-missing-directories
    Example: Doctor fix creates missing configured directories
      Given the config exists but behavior directories are missing
      When I run specweave doctor --fix
      Then SpecWeave creates the missing configured directories
      And remaining diagnostics are reported

    @bdd-doctor-duplicate-bdd-tags
    Example: Doctor reports duplicate scenario identifiers
      Given two scenarios use the same @bdd-* tag
      When I run specweave doctor
      Then SpecWeave reports a duplicate scenario id finding
      And the command exits with failure

  Rule: Review behavior specs

    @bdd-review-specs-summary
    Example: Review specs reports feature and pytest coverage summary
      Given behavior features and pytest tests exist
      When I run specweave review specs
      Then SpecWeave reports feature, scenario, bound, and missing binding counts
      And SpecWeave reports pytest mapped, unmapped, and stale mapping counts

    @bdd-review-specs-needs-review
    Example: Review flags generated scenarios that still need review
      Given a scenario is tagged @needs-review
      When I run specweave review specs
      Then SpecWeave reports a needs-review finding

    @bdd-refresh-common-artifacts
    Example: Refresh rewrites index, mappings, and coverage reports
      Given a configured SpecWeave project
      When I run specweave behavior refresh
      Then SpecWeave writes the behavior README
      And SpecWeave writes the behavior manifest
      And SpecWeave writes coverage and mapping reports under reports/specweave

    @bdd-review-golden-command
    Example: Golden review aggregates coding-agent health checks
      Given a configured SpecWeave project
      When I run specweave review golden
      Then SpecWeave runs doctor, behavior check, coverage, mappings, and spec review
      And SpecWeave writes coverage, mapping, and review artifacts
      And the command exit code reflects release-blocking findings
