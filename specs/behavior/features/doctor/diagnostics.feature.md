`@area-doctor` `@feature-diagnostics`

# Feature: SpecWeave project diagnostics

specweave doctor checks the project setup, config, paths, and feature

files for problems. It can optionally fix missing directories.

## Rule: Doctor checks config presence and schema

`@bdd-doctor-missing-config`

### Example: Doctor warns when no config file exists

- Given no specweave config file exists
- When specweave doctor runs
- Then the result contains a warning with code "SWDOC001"
- And the status is "passed"

`@bdd-doctor-unsupported-schema`

### Example: Doctor errors on unsupported schema version

- Given a config file with schema_version 2
- When specweave doctor runs
- Then the result contains an error with code "SWDOC002"
- And the status is "failed"

## Rule: Doctor checks directory existence

`@bdd-doctor-missing-directories`

### Example: Doctor warns about missing directories

- Given a valid config but missing features directory
- When specweave doctor runs
- Then the result contains warnings for missing directories
- And the warnings include codes "SWDOC006" through "SWDOC010"

`@bdd-doctor-fix-creates-directories`

### Example: Doctor --fix creates missing directories

- Given a valid config but missing features directory
- When specweave doctor runs with --fix
- Then the missing directories are created
- And warnings mention the created paths

## Rule: Doctor checks for deprecated paths

`@bdd-doctor-deprecated-paths`

### Example: Doctor warns about deprecated feature paths

- Given feature files exist under "specs/bdd/features"
- When specweave doctor runs
- Then the result contains a warning with code "SWDOC004"

## Rule: Doctor checks for duplicate bdd tags

`@bdd-doctor-duplicate-bdd-tags`

### Example: Doctor errors on duplicate @bdd-\* tags

- Given two feature files share the same @bdd-\* tag
- When specweave doctor runs
- Then the result contains errors with code "SWDOC005"
- And the status is "failed"

## Rule: Doctor validates feature files

`@bdd-doctor-validates-features`

### Example: Doctor reports feature lint errors

- Given a feature file missing Given/When/Then steps
- When specweave doctor runs
- Then the result contains an error for the lint finding
