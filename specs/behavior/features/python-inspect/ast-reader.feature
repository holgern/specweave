@area-python-inspect @feature-ast-reader
Feature: AST-based Python test inspection

  SpecWeave inspects Python test files via AST (abstract syntax tree) without
  importing or executing the module. It discovers test functions, extracts
  SpecWeave mapping markers, and converts assertion expressions into candidate
  behavior descriptions.

  Rule: Discover test functions via AST

    @bdd-ast-extract-test-functions
    Example: AST reader finds test\_\* functions in a Python file
      Given a Python file containing a `test_rejects_invalid_password` function with assertions
      When specweave extracts test scenarios from the file
      Then one scenario is discovered
      And the scenario title is derived from the function name
      And the scenario has at least two steps (When and Then)

    @bdd-ast-ignores-non-test
    Example: AST reader ignores helper functions and non-test functions
      Given a Python file containing a `helper` function without `test_` prefix
      When specweave extracts test scenarios from the file
      Then zero scenarios are discovered

  Rule: Convert assertions to plain English

    @bdd-ast-assert-equals
    Example: Equality assertion becomes "x equals 42"
      Given a Python `assert x == 42` statement
      When specweave describes the assertion
      Then the description includes "x"
      And the description includes "equals"
      And the description includes "42"

    @bdd-ast-assert-is-none
    Example: Identity assertion becomes "session is None"
      Given a Python `assert session is None` statement
      When specweave describes the assertion
      Then the description includes "session"
      And the description includes "is None"

    @bdd-ast-assert-truthy
    Example: Truthiness assertion becomes "user is truthy"
      Given a bare Python `assert user` statement
      When specweave describes the assertion
      Then the description is "user is truthy"

    @bdd-ast-assert-call
    Example: Call assertion becomes "func_name succeeds"
      Given a Python `assert validate_token(token)` statement
      When specweave describes the assertion
      Then the description includes "succeeds"

  Rule: Discover SpecWeave pytest marker mappings

    @bdd-ast-discover-marker
    Example: AST reader extracts @pytest.mark.specweave mappings
      Given a Python file with `@pytest.mark.specweave(feature=…, scenario=…)` decorator
      When specweave discovers mappings in the file
      Then one mapping is discovered
      And the mapping feature path ends with the expected feature file name
      And the mapping scenario is the `@bdd-*` id
      And the mapping source is "marker"

    @bdd-ast-discover-comment
    Example: AST reader extracts # specweave: comment mappings
      Given a Python file with `# specweave: feature=…` and `# specweave: scenario=…` comments
      When specweave discovers mappings in the file
      Then one mapping is discovered
      And the mapping feature path ends with the expected feature file name
      And the mapping scenario is the `@bdd-*` id
      And the mapping source is "comment"

    @bdd-ast-discover-docstring
    Example: AST reader extracts docstring-based SpecWeave mappings
      Given a Python file with a docstring containing a feature path and `@bdd-*` id
      And a matching `.feature` file exists
      When specweave discovers mappings in the file
      Then one mapping is discovered
      And the mapping feature path matches the canonical feature path
      And the mapping scenario matches the bdd-id
      And the mapping source is "docstring"
