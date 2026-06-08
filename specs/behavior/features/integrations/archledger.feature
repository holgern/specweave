@area-integrations @feature-archledger
Feature: Archledger integration
  SpecWeave generates Archledger candidate markdown for scenarios that are
  architecturally important. Candidates are written only when explicitly
  requested.

  Rule: Archledger candidate generation

    @bdd-archledger-candidate
    Example: archledger command renders candidate markdown
      Given a canonical behavior feature file with @bdd-* tags
      When specweave runs "archledger" with a valid @bdd-* id
      Then a candidate Markdown file is written
      And the file contains the scenario behavior lines
      And the file references the source feature

    @bdd-archledger-unknown-bdd
    Example: archledger errors on unknown @bdd-* id
      Given a canonical behavior feature file
      When specweave runs "archledger" with an unknown @bdd-* id
      Then a ValueError is raised
      And the error mentions the unknown scenario

  Rule: Archledger does not write accepted records by default

    @bdd-archledger-candidate-only
    Example: archledger produces candidates, not accepted records
      Given a canonical behavior feature file
      When specweave runs "archledger"
      Then the output is a candidate record
      And the record is not marked as accepted
