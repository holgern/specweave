# Gherkin Formats

SpecWeave supports two Gherkin storage formats: Markdown (`.feature.md`,
the default) and classic (`.feature`).

## Markdown format (default)

When `[gherkin].document_format = "markdown"`, SpecWeave uses `.feature.md`
files. Feature content is embedded in fenced code blocks:

```markdown
@user-login
Feature: User login

Rule: Valid credentials grant access

    @bdd-user-login-success @ac-0001
    Example: Successful login
      Given a registered user exists
      When the user submits valid credentials
      Then the user is authenticated
```

The Markdown wrapper enables rich surrounding documentation, linking, and
navigation in editors, code review, and static site generators.

## Classic format

The traditional Gherkin `.feature` format is fully supported:

```gherkin
@user-login
Feature: User login

  Rule: Valid credentials grant access

    @bdd-user-login-success @ac-0001
    Example: Successful login
      Given a registered user exists
      When the user submits valid credentials
      Then the user is authenticated
```

## Converting between formats

```bash
specweave convert specs/behavior/features/auth/login.feature
specweave convert specs/behavior/features --to markdown
specweave convert --all --to markdown
specweave convert login.feature.md --to classic
specweave convert login.feature --dry-run
specweave convert specs/behavior/features --to markdown --replace-source
```

Source files are kept by default. Use `--replace-source` to delete classic
sources after conversion. After bulk conversion, run `specweave behavior coverage` to catch stale mappings.

## Gherkin configuration

| Setting                    | Default                       | Description                      |
| -------------------------- | ----------------------------- | -------------------------------- |
| `document_format`          | `"markdown"`                  | Storage format for feature files |
| `feature_extension`        | `".feature.md"`               | Primary file extension           |
| `feature_extensions`       | `[".feature.md", ".feature"]` | Recognized extensions            |
| `dialect`                  | `"en"`                        | Gherkin language dialect         |
| `default_scenario_keyword` | `"Example"`                   | Default scenario keyword         |
| `require_given_when_then`  | `true`                        | Require Given/When/Then steps    |
| `require_bdd_ids`          | `true`                        | Require `@bdd-*` tags            |
| `id_style`                 | `"slug"`                      | ID generation style              |
| `official_parser`          | `false`                       | Use gherkin-official parser      |
| `markdown_parser`          | `"specweave"`                 | Markdown parser backend          |

## Official parser (optional)

Install `specweave[gherkin]` for full Cucumber Gherkin compatibility via
the official reference parser. The built-in parser covers the canonical
subset and is sufficient for most workflows.
