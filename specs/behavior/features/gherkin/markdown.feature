@area-gherkin @feature-markdown-rejection
Feature: Legacy Markdown feature files are rejected

  SpecWeave uses classic `.feature` files as the only canonical behavior-spec
  format. Legacy `.feature.md` inputs are rejected with an explicit migration
  message instead of being parsed, written, or linted as canonical specs.

  Rule: Parser rejects markdown feature files

    @bdd-markdown-parser-rejects-path
    Example: Parser rejects a .feature.md source path
      Given a file path ending with ".feature.md"
      When specweave parses the file as a canonical feature
      Then parsing fails
      And the error says markdown feature files are no longer supported

  Rule: Lint reports unsupported markdown files

    @bdd-lint-rejects-markdown-file
    Example: Lint returns an explicit unsupported-format finding
      Given a canonical feature input path ending with ".feature.md"
      When specweave lints that path
      Then the finding code is "SWBEH016"
      And the finding explains that classic ".feature" is required

  Rule: Validation rejects markdown feature syntax

    @bdd-validation-rejects-markdown
    Example: Markdown validation fails closed
      Given markdown-shaped Gherkin text
      When specweave validates the text as a legacy markdown feature
      Then validation fails
      And the error says markdown feature files are no longer supported
