`@area-gherkin` `@feature-markdown`

# Feature: Markdown-with-Gherkin parser and writer

SpecWeave parses and writes `.feature.md` files using a Markdown-with-Gherkin
format. Tags are backticked, headings use markdown levels, and steps are
markdown bullets. The parser ignores non-Gherkin prose around the feature
structure.

## Rule: Parse markdown feature structure

`@bdd-md-parse-feature`

### Example: Parser extracts feature title and tags from markdown

- Given a valid markdown feature with backticked area and feature tags
- When specweave parses the markdown feature
- Then the Feature title is "Password login"
- And the Feature tags include "area-auth", "feature-password-login", and "generated"

`@bdd-md-parse-rule-scenario`

### Example: Parser extracts Rule and Scenario with tags

- Given a markdown feature with a rule and a scenario
- When specweave parses the markdown feature
- Then the Feature contains one Rule
- And the Rule title is preserved
- And the Rule tags include the rule-level tag
- And the Rule contains one Scenario
- And the Scenario title is preserved
- And the Scenario keyword is "Example"
- And the Scenario tags include its bdd-id and needs-review

`@bdd-md-parse-steps`

### Example: Parser extracts Given, When, Then steps from bullets

- Given a markdown feature with bullet steps
- When specweave parses the markdown feature
- Then the Scenario has three steps
- And the first step keyword is "Given"
- And the second step keyword is "When"
- And the third step keyword is "Then"
- And each step has its text extracted

`@bdd-md-parse-top-level`

### Example: Parser extracts top-level scenarios outside rules

- Given a markdown feature with a scenario outside any rule
- When specweave parses the markdown feature
- Then the Feature has a top-level Scenario
- And the Scenario keyword is "Scenario"
- And the Scenario has its bdd-id tag

`@bdd-md-parse-description`

### Example: Parser preserves feature description text

- Given a markdown feature with descriptive prose after the heading
- When specweave parses the markdown feature
- Then the Feature description includes that prose text

`@bdd-md-parse-ignores-prose`

### Example: Parser ignores non-Gherkin markdown around the feature

- Given markdown text with random prose before the feature heading
- When specweave parses the text
- Then the Feature title is still extracted correctly
- And the random prose is not treated as tags or steps

`@bdd-md-parse-requires-backticked-tags`

### Example: Classic @tags without backticks are not parsed as tags

- Given markdown text with bare "@tag" instead of backticked `@tag`
- When specweave parses the markdown
- Then the Feature has no tags

`@bdd-md-parse-empty-feature`

### Example: Parser handles a feature with no rules or scenarios

- Given markdown containing only a "# Feature: Empty" heading
- When specweave parses the markdown
- Then the Feature title is "Empty"
- And the Feature has no scenarios
- And the Feature has no rules

## Rule: Write markdown feature output

`@bdd-md-write-feature`

### Example: Writer produces properly formatted markdown

- Given a Feature object parsed from a markdown feature
- When specweave writes it as markdown
- Then the output contains backticked area and feature tags
- Then the output contains "# Feature: …" heading
- Then the output contains "## Rule: …" for each rule
- Then the output contains "### Example: …" for each scenario
- Then the output contains bullet steps with Given, When, Then keywords

`@bdd-md-write-roundtrip`

### Example: Parse-write-parse round-trip preserves model

- Given a Feature object parsed from a markdown feature
- When the feature is written to markdown and re-parsed
- Then the re-parsed Feature has the same title
- Then the re-parsed Feature has the same tags
- Then the re-parsed Feature has the same number of rules
- Then the re-parsed Feature has the same number of top-level scenarios
- Then each rule has the same title, tags, and scenario count
- Then each scenario has the same title, keyword, and step count

## Rule: Convert markdown to classic

`@bdd-md-to-classic`

### Example: Markdown feature converts to classic Gherkin

- Given a valid markdown feature with rules and scenarios
- When specweave converts it to classic Gherkin
- Then the output contains "Feature: Password login"
- Then the output contains "Scenario: Top level test"
- Then the output contains Given/When/Then step keywords

`@bdd-md-to-classic-validates`

### Example: Converted classic text validates with official parser

- Given a valid markdown feature
- When specweave converts it to classic and validates with the official parser
- Then the validation succeeds
- And the parsed Feature title matches the original

## Rule: Tag helper utilities

`@bdd-md-has-backticked-tags`

### Example: Detect backticked tags on a line

- Given text containing "`@tag1` `@tag2`"
- When specweave checks for backticked tags
- Then the result is true
- And plain text without backticked tags returns false
- And a markdown heading line returns false

`@bdd-md-parse-backticked-tags`

### Example: Extract tag names from backticked tag text

- Given text "`@tag1` `@tag2`"
- When specweave parses the backticked tags
- Then the result includes "tag1" and "tag2"
- And a single backticked tag is also extracted correctly
