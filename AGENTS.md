https://chatgpt.com/c/69746329-5974-832f-b661-88ceaf5c57cc

# AGENTS.md

## Dev Environment and Tools

### Python Dependencies

- Setup environment with `pip install -e .[dev]`

### Testing

- Run `pytest -v` from the repository root 
* Use standard pytest options for selective runs or debugging.
* Resolve all failures before considering the task complete.

### Formatting

```
ruff format "{path/to/dir}"
ruff check "{path/to/dir}"
ruff check --fix "{path/to/dir}"
```

## Mandatory Repo Discovery Steps

Before writing or modifying any files, you must:

1. Read and operationalize `AGENTS.md` (this file), and any additional referenced files (follow any local references).
2. Locate and read `pyproject.toml`  at repo root.
3. Determine package name (`<package_name>`)
    * `[project]`
    * `name`
4. Determine pytest configuration:
    * `[tool.pytest.ini_options]`
    * `testpaths`, markers, plugins
5. Confirm pytest `tests` directory path (as determined from `pyproject.toml`) relative to repo root matches one of the the patterns:
    * `tests`
    * `<package_name>/tests`
6. Confirm pytest `tests` directory path (as determined from `pyproject.toml`) already exists (it must exist).
7. Determine source layout (one of):
    - `<package_name>`
    - `src/<package_name>`
    - `<package_name>/src/<package_name>`
8. Check if this value from `pyproject.toml`, if present, is consistent with determined source layout: 
    - `[tool.hatch.build.targets.wheel]`
    - `packages`
9. Locate existing testing infrastructure:
    * `pytest.ini`, `conftest.py`
    * shared fixtures or helpers
10. Determine how tests are intended to be executed in this repository.

If any of the above cannot be determined, stop and report what is missing.


## Editing Constraints

### Character Set

**ASCII only**: When editing or creating files:

* Use English names for units and symbols (for example, `deg`, `alpha`).
* Use ASCII quotes and dashes exclusively.
* Applies to code, comments, docstrings, and Markdown.
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
