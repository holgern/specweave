`@area-gherkin` `@feature-convert`

# Feature: Gherkin document format conversion

SpecWeave converts between classic `.feature` and Markdown `.feature.md`
formats while preserving tags, rules, scenarios, steps, and descriptions.
Conversion supports single files, directory batches, content-based format
detection, and dry-run previews.

## Rule: Infer format from file suffix

`@bdd-convert-infer-format`

### Example: Suffix `.feature` infers classic format

- Given a source path ending with ".feature"
- When specweave infers the document format
- Then the format is "classic"

`@bdd-convert-infer-markdown`

### Example: Suffix `.feature.md` infers markdown format

- Given a source path ending with ".feature.md"
- When specweave infers the document format
- Then the format is "markdown"

## Rule: Convert classic to markdown

`@bdd-convert-classic-to-markdown`

### Example: Classic feature becomes markdown without losing structure

- Given a classic `.feature` file with tags, a Feature, a Rule, and a Scenario
- When specweave converts it to markdown
- Then the output file has ".feature.md" suffix
- And the Feature title is preserved as a heading
- And rule tags are backticked
- And the Rule title is preserved as a heading
- And scenario tags are backticked
- And the Scenario has Given, When, and Then steps
- And the output status is "created"

`@bdd-convert-default-output-path`

### Example: Default output path derives from source

- Given a source path "login.feature" and target format "markdown"
- When specweave computes the default output path
- Then the output path is "login.feature.md"

## Rule: Protect existing output

`@bdd-convert-refuses-overwrite`

### Example: Conversion refuses to overwrite existing output

- Given a `.feature.md` file already exists at the target path
- When specweave converts without `--force`
- Then a ValueError is raised
- And the error message says to use `--force`

## Rule: Batch directory conversion

`@bdd-convert-directory`

### Example: Convert all classic features in a directory tree

- Given a directory containing classic `.feature` files
- When specweave converts the directory to markdown
- Then every classic feature produces a markdown output
- And the overall status is "passed"
- And the summary reports the count of created files

`@bdd-convert-keeps-source`

### Example: Batch conversion keeps source files by default

- Given a directory containing classic `.feature` files
- When specweave converts the directory to markdown
- Then the original classic files remain on disk
- And new markdown files exist alongside them

`@bdd-convert-replace-source`

### Example: Replace source removes classic files after success

- Given a directory containing classic `.feature` files
- When specweave converts the directory to markdown with `--replace-source`
- Then the original classic files are deleted
- And the summary reports deleted source count
- And the output status is "passed"

`@bdd-convert-dry-run`

### Example: Dry-run reports without writing files

- Given a directory containing classic `.feature` files
- When specweave converts with `--dry-run` and `--replace-source`
- Then no files are created or deleted
- And the output status is "dry-run"
- And each item indicates whether the source would be deleted

`@bdd-convert-collision`

### Example: Batch conversion reports collision as error

- Given a directory containing a classic `.feature` file
- And a markdown `.feature.md` file already exists at the output path
- When specweave converts the directory without `--force`
- Then the overall status is "failed"
- And the summary includes an error count
- And the colliding item has status "error"

## Rule: Content-based format detection

`@bdd-convert-from-content-classic`

### Example: Detect classic content in a `.feature.md` file

- Given a `.feature.md` file containing classic Gherkin syntax
- When specweave converts with `--from content --to markdown --force`
- Then the source format is detected as "classic"
- And the output status is "updated"
- And the file contains markdown headings after conversion

`@bdd-convert-from-content-markdown`

### Example: Detect markdown content already in markdown format

- Given a `.feature.md` file already containing markdown Gherkin syntax
- When specweave converts with `--from content --to markdown`
- Then the source format is detected as "markdown"
- And the output status is "unchanged"

## Rule: CLI JSON output contract

`@bdd-convert-cli-json`

### Example: Single-file conversion reports JSON with format info

- Given a classic `.feature` file
- When specweave is invoked with `--json convert <file> --no-validate`
- Then the exit code is zero
- And the JSON output includes `command: "convert"`
- And the JSON output includes `source_format: "classic"`
- And the JSON output includes `target_format: "markdown"`
- And the output path ends with ".feature.md"

`@bdd-convert-cli-batch-json`

### Example: Batch conversion with --all reports JSON summary

- Given multiple classic `.feature` files in the features directory
- When specweave is invoked with `--json convert --all --to markdown --no-validate`
- Then the exit code is zero
- And the JSON output includes `mode: "batch"`
- And the summary includes created and error counts
- And every source file appears in the items array
