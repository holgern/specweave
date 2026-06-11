@area-integrations @feature-combi-audit
Feature: Audit cross-tool links without mutation

  SpecWeave can read behavior specs, pytest mappings, evidence, Taskledger mappings,
  and Archledger state to report gaps without mutating external tools.

  Rule: Report cross-tool gaps

    @bdd-combi-reports-missing-pytest-mapping
    Example: Missing pytest mapping appears as a combi gap
      Given a behavior scenario has no pytest mapping
      When I run specweave combi check
      Then SpecWeave reports a gap for missing executable validation

    @bdd-combi-reports-missing-evidence
    Example: Missing evidence appears as a combi gap
      Given a behavior scenario has a pytest mapping but no evidence
      When I run specweave combi check
      Then SpecWeave reports a gap for missing validation evidence

    @bdd-combi-strict-fails-missing-bdd-id
    Example: Strict mode fails on missing scenario identifiers
      Given a scenario has no @bdd-* id
      When I run specweave combi check --strict
      Then SpecWeave reports an error
      And the command exits with failure

    @bdd-combi-json-output
    Example: Combi check can write a JSON report
      Given cross-tool gaps exist
      When I run specweave combi check --json reports/combi.json
      Then SpecWeave writes the structured gap report
      And the human summary is still printed
