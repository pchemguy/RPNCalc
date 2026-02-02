https://chatgpt.com/c/69746329-5974-832f-b661-88ceaf5c57cc

# AGENTS.md

## Dev Environment and Tools

### Python Dependencies

- Setup environment with `pip install -e .[dev]`

### Testing

- Run full test suite - `pytest -v` from the repository root 
* Use standard pytest options for selective runs or debugging (e.g., `pytest -v <test_file.py>`).
* Triage and resolve all test failures according to `TEST_FAILURE_TRIAGE.md`
* Resolve all failures before considering the task complete.

### Formatting

```
ruff format "{path/to/dir}"
ruff check "{path/to/dir}"
ruff check --fix "{path/to/dir}"
```

## Sample Repo Structure

```
<package_name>/
  src/<package_name>/
    __init__.py
    exceptions.py
    engine.py
    engine_fp.py
    parser.py
    parser_fp.py
    cli.py
  tests/
    test_engine.py
    test_engine_fp.py
    test_parser.py
    test_parser_fp.py
    test_cli_smoke.py
pyproject.toml
AGENTS.md
DEV_STRATEGY.md
PROJECT.md
TEST_FAILURE_TRIAGE.md
README.md 
```

## Mandatory Repo Discovery Steps

Before writing or modifying any files, you must:

1. Read and operationalize
    - root `AGENTS.md` (this file)
    - any existing files at repo root:
        - README.md
        - DESIGN.md
        - ARCHITECTURE.md
        - DEV_STRATEGY.md
        - PLAN.md
        - PROJECT.md
        - TEST_FAILURE_TRIAGE.md
    - additional referenced files.
2. Locate and read `pyproject.toml`  at the repo root.
3. Determine package name (`<package_name>`)
    * `[project]`
    * `name`
4. Determine pytest configuration:
    * `[tool.pytest.ini_options]`
    * `testpaths`, markers, plugins
5. Confirm `testpaths` resolves to an **existing directory** relative to repo root.
6. Determine source layout (one of):
    - `<package_name>`
    - `src/<package_name>`
    - `<package_name>/src/<package_name>`
7. Check if this value from `pyproject.toml`, if present, is consistent with determined source layout: 
    - `[tool.hatch.build.targets.wheel]`
    - `packages`
8. Locate existing testing infrastructure:
    * `pytest.ini`, `conftest.py`
    * shared fixtures or helpers
9. Determine how tests are intended to be executed in this repository.

**If required files are inaccessible** → agent must stop further task processing, output “BLOCKED” + list missing artifacts.
**If files exist but are ambiguous** → agent must proceed with the *repo's dominant convention* and explicitly state assumptions.

## Editing Constraints

### Character Set

Prefer ASCII when editing or creating files:

* Use English names for units and symbols (for example, `deg`, `alpha`).
* Use ASCII quotes and dashes exclusively.
* Strictly applies to code, comments, and docstrings within code modules.
* Only use non-ASCII in Markdown, when there is no a common ASCII equivalent and using non-ASCII is justified (e.g., when using border chars for schematics).
* Do not globally normalize existing files unless explicitly instructed.
* When editing a block containing non-ASCII characters, replace them with ASCII equivalents where reasonable.

### Comments and Documentation

* Add comments where logic or intent is non-obvious.
* Prefer short explanatory comments preceding complex logic.
* Comments should explain why, not what.
* Comments must remain accurate after code changes.
* Avoid trivial comments.

### Code Quality

* Code should be:
    * readable,
    * explicit,
    * and unsurprising.
* Repeated literal values should be factored into constants where it improves clarity.
* Avoid unnecessary abstraction.
* Avoid premature optimization.

### Documentation Quality

* Docstrings and Markdown should:
    * accurately describe behavior and intent,
    * align with the current implementation,
    * avoid stale or misleading statements.
* Scan for:
    * typos,
    * broken links,
    * inconsistent formatting,
    * incorrect references.

### Math Notation

* Inline MathJAX: `$N$`
* Block MathJAX:

```
$$
N
$$
```

## Git and Working Tree Safety

Assume the working tree may be dirty.

* Never revert or discard changes you did not make unless explicitly instructed.
* Do not amend commits unless explicitly requested.
* If unrelated changes exist:
    * Ignore unrelated files.
    * Carefully integrate with existing changes in files you touch.
* If you encounter unexpected changes you cannot safely reason about:
    * **Stop immediately** and ask the user how to proceed.
* Unless explicitly requested or approved, **never** use destructive git commands such as:
    * `git reset --hard`
    * `git checkout --`

## Language-Specific Rules

* **Python**: Follow `PythonStyleGuidelines.md`.

---
