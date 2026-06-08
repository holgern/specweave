`@area-gherkin` `@feature-official`

# Feature: Official Cucumber Gherkin parser adapter

SpecWeave wraps the official `gherkin-official` parser to validate classic
Gherkin syntax and to produce the internal Feature/Rule/Scenario/Step
dataclass model. It accepts raw text and optional source path metadata.

## Rule: Parse classic Gherkin with the official parser

`@bdd-official-parse-simple`

### Example: Official parser extracts feature title, tags, and description

- Given classic Gherkin text with `@feature-tag`, a title, and a description
- When the official parser is used
- Then the Feature title is "Hello"
- And the Feature tags include "feature-tag"
- And the Feature description is "Some description."
- And the Feature has one Scenario
- And the Scenario title is "A simple test"
- And the Scenario keyword is "Scenario"
- And the Scenario tags include "scenario-tag"
- And the Scenario has three steps: Given, When, Then

`@bdd-official-parse-rules`

### Example: Official parser extracts Rule blocks with tags

- Given classic Gherkin text with a Rule containing a Scenario
- When the official parser is used
- Then the Feature title is "With rules"
- And the Feature contains one Rule
- And the Rule title is "Rule A"
- And the Rule has its rule-level tags
- And the Rule Scenario has its scenario-level tags

`@bdd-official-parse-no-tags`

### Example: Official parser handles features without tags

- Given classic Gherkin text with no tags
- When the official parser is used
- Then the Feature tags are empty

`@bdd-official-source-path`

### Example: Official parser stores the source path when provided

- Given classic Gherkin text
- When the official parser is used with a source_path argument
- Then the Feature source_path is set to that path

`@bdd-official-compile-pickles`

### Example: Official parser supports pickle compilation mode

- Given classic Gherkin text
- When the official parser is used with compile_pickles=True
- Then the Feature is still parsed correctly
- And the title is preserved

## Rule: Validate classic Gherkin syntax

`@bdd-official-validate-valid`

### Example: Validation succeeds for valid Gherkin

- Given syntactically valid classic Gherkin text
- When the official parser validates it
- Then no error is raised

`@bdd-official-validate-invalid`

### Example: Validation fails for invalid Gherkin

- Given text that is not valid Gherkin
- When the official parser validates it
- Then a ParseError is raised

## Rule: Reject invalid Gherkin on parse

`@bdd-official-reject-invalid`

### Example: Parser raises ParseError for invalid input

- Given text that is not valid Gherkin
- When the official parser is used
- Then a ParseError is raised

`@bdd-official-preserve-description`

### Example: Parser preserves multi-line descriptions through official parser

- Given classic Gherkin text with a description
- When the official parser is used
- Then the description text is preserved in the Feature
