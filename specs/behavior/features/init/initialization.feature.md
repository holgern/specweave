`@area-init` `@feature-initialization`
# Feature: SpecWeave project initialization

specweave init creates the config file and directory layout for a new

SpecWeave project. It is idempotent and supports dry-run mode.

## Rule: Init creates config and directories

`@bdd-init-creates-dotfile`
### Example: Init creates .specweave.toml by default
* Given an empty project directory
* When specweave init runs
* Then ".specweave.toml" is created
* And the specs/behavior/features directory exists
* And the .specweave directory exists
* And the reports/behavior directory exists

`@bdd-init-creates-public-config`
### Example: Init creates specweave.toml with --public-config
* Given an empty project directory
* When specweave init runs with --public-config
* Then "specweave.toml" is created
* And ".specweave.toml" is not created

`@bdd-init-creates-readme`
### Example: Init creates a managed README in specs root
* Given an empty project directory
* When specweave init runs
* Then "specs/behavior/README.md" is created
* And the README contains "This directory is managed by SpecWeave."

`@bdd-init-creates-gitkeep`
### Example: Init creates .gitkeep in features directory
* Given an empty project directory
* When specweave init runs
* Then "specs/behavior/features/.gitkeep" is created

## Rule: Init is idempotent

`@bdd-init-idempotent`
### Example: Running init twice does not fail
* Given an empty project directory
* When specweave init runs twice
* Then no errors occur
* And all paths are reported as existing on the second run

## Rule: Init supports British spelling

`@bdd-init-british-spelling`
### Example: Init creates behaviour layout with --spelling behaviour
* Given an empty project directory
* When specweave init runs with --spelling behaviour
* Then "specs/behaviour/features" directory exists
* And "reports/behaviour" directory exists
* And the config contains 'spelling = "behaviour"'

## Rule: Init supports dry-run mode

`@bdd-init-dry-run`
### Example: Dry-run reports paths without writing
* Given an empty project directory
* When specweave init runs with --dry-run
* Then no files or directories are created
* And the result reports paths that would be created

## Rule: Init refuses to overwrite non-managed README

`@bdd-init-refuses-overwrite-readme`
### Example: Init skips non-SpecWeave README
* Given a README with custom content in specs/behavior
* When specweave init runs without --force
* Then the README is skipped
* And a warning mentions non-SpecWeave content

`@bdd-init-force-overwrites-readme`
### Example: Init overwrites managed README with --force
* Given a SpecWeave-managed README in specs/behavior
* When specweave init runs with --force
* Then the README is overwritten

## Rule: Init warns about existing config

`@bdd-init-warns-existing-config`
### Example: Init warns when config already exists
* Given a ".specweave.toml" already exists
* When specweave init runs without --force
* Then a warning mentions the config already exists
