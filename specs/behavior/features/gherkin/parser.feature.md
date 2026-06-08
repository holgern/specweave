`@area-gherkin` `@feature-parser`
# Feature: Gherkin feature file parsing

The Gherkin parser reads feature text and produces Feature/Rule/Scenario/Step

dataclass instances. It supports classic .feature and markdown .feature.md

formats.

## Rule: Classic Gherkin parsing extracts structure

`@bdd-parser-classic-feature`
### Example: Parser extracts feature title and scenarios
* Given a classic Gherkin feature with one scenario
* When specweave parses the feature
* Then the Feature has the correct title
* And the Feature contains one Scenario
* And the Scenario has Given, When, and Then steps

`@bdd-parser-classic-rules`
### Example: Parser extracts Rule blocks
* Given a classic Gherkin feature with a Rule containing two scenarios
* When specweave parses the feature
* Then the Feature has one Rule
* And the Rule contains two Scenarios

`@bdd-parser-classic-tags`
### Example: Parser preserves tags on features, rules, and scenarios
* Given a classic Gherkin feature with tags at each level
* When specweave parses the feature
* Then the Feature tags include the feature-level tags
* And the Rule tags include the rule-level tags
* And the Scenario tags include the scenario-level tags

`@bdd-parser-classic-description`
### Example: Parser preserves feature and scenario descriptions
* Given a classic Gherkin feature with descriptions
* When specweave parses the feature
* Then the Feature description is preserved
* And the Scenario description is preserved

`@bdd-parser-classic-top-level-scenarios`
### Example: Parser handles top-level scenarios outside rules
* Given a classic Gherkin feature with top-level scenarios
* When specweave parses the feature
* Then the Feature has top-level scenarios
* And the Feature has no rules

## Rule: Markdown Gherkin parsing

`@bdd-parser-markdown-feature`
### Example: Parser extracts structure from markdown format
* Given a markdown Gherkin feature file
* When specweave parses the feature
* Then the Feature has the correct title
* And the Scenario steps are extracted

## Rule: Parser dispatches by format

`@bdd-parser-dispatch-by-suffix`
### Example: Parser selects markdown parser for .feature.md files
* Given a feature source with ".feature.md" suffix
* When specweave parses the feature
* Then the markdown parser is used

`@bdd-parser-dispatch-classic`
### Example: Parser selects classic parser for .feature files
* Given a feature source with ".feature" suffix
* When specweave parses the feature
* Then the classic parser is used

## Rule: Parser requires Feature line

`@bdd-parser-requires-feature-line`
### Example: Parser raises ValueError without Feature line
* Given text that does not contain "Feature:"
* When specweave parses the feature
* Then a ValueError is raised with "Expected 'Feature:' line"
