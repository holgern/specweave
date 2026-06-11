@area-integrations @feature-archledger-trace
Feature: Produce Archledger candidates and trace bundles

  SpecWeave can prepare behavior evidence for architecture review without writing
  accepted architecture records itself.

  Rule: Create Archledger candidate records

    @bdd-archledger-candidate
    Example: Render a candidate behavior record for one scenario
      Given a feature contains a scenario with a @bdd-* id
      When I run specweave archledger --feature feature.feature --bdd bdd-id
      Then SpecWeave writes candidate markdown
      And the candidate includes the feature title, scenario title, tags, and steps

    @bdd-archledger-unknown-bdd
    Example: Unknown scenario ids fail clearly
      Given a feature does not contain the requested @bdd-* id
      When I run specweave archledger with that id
      Then SpecWeave reports the missing scenario id
      And no accepted architecture record is written

  Rule: Extract behavior-centered traces

    @bdd-trace-by-bdd-id
    Example: Trace a behavior scenario by id
      Given behavior features, pytest mappings, evidence, and task mappings exist
      When I run specweave trace bdd-login-success
      Then SpecWeave emits a JSON trace bundle
      And the bundle includes feature, scenario, acceptance criteria, pytest references, evidence references, and gaps

    @bdd-trace-rejects-markdown-feature-path
    Example: Trace rejects legacy markdown feature paths
      Given the trace target is a .feature.md path
      When I run specweave trace with that target
      Then SpecWeave reports a migration gap
