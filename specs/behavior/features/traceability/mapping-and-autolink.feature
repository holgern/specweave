@area-traceability @feature-mapping-and-autolink
Feature: Map behavior scenarios to pytest tests

  SpecWeave uses stable tags and explicit metadata, not scenario titles, to connect
  behavior intent to executable pytest tests.

  Rule: Discover explicit mappings

    @bdd-mappings-from-comments
    Example: Mapping comments link a pytest test to a behavior scenario
      Given a pytest test contains SpecWeave feature and scenario comments
      When I run specweave behavior mappings
      Then the test appears in the mapping inventory
      And the inventory includes the feature path, scenario id, nodeid, and source

    @bdd-mappings-from-docstring
    Example: Docstring metadata is accepted as an explicit mapping
      Given a pytest test docstring contains SpecWeave mapping metadata
      When SpecWeave discovers pytest mappings
      Then the mapping is included in coverage

    @bdd-mappings-title-never-binds
    Example: Similar titles are only suggestions
      Given a scenario title matches a pytest test name
      And the pytest test has no SpecWeave mapping
      When SpecWeave builds coverage
      Then the scenario is not counted as bound
      And any matching test is shown only as a candidate hint

  Rule: Autolink generated specs safely

    @bdd-autolink-dry-run
    Example: Dry-run proposes generated scenario mappings
      Given a generated feature and generated pytest tests share generated ids
      When I run specweave behavior autolink
      Then SpecWeave reports planned mappings
      And no test file is modified

    @bdd-autolink-apply
    Example: Apply writes explicit mapping comments
      Given autolink finds an unambiguous generated scenario to test match
      When I run specweave behavior autolink --apply
      Then SpecWeave writes explicit mapping metadata into the pytest test

    @bdd-autolink-ambiguous-match
    Example: Ambiguous autolink candidates fail safe
      Given two pytest tests match the same generated scenario id
      When I run specweave behavior autolink
      Then SpecWeave reports the ambiguity
      And no mapping is guessed

    @bdd-autolink-check-mode
    Example: Check mode fails when mappings would be created
      Given autolink finds planned mappings
      When I run specweave behavior autolink --check
      Then the command exits with failure
