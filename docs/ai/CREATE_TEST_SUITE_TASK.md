## Prompt: `CREATE_TEST_SUITE_TASK`

You are an AI engineering agent tasked with **creating or extending** a **comprehensive `pytest` test suite** for a specified Python module.

### 0. Inputs you will be given

You will be provided:

* **Target module path** (one of):
    * a local file path (e.g., `rpncalc/src/rpncalc/parser.py`), or
    * a GitHub repo path reference using the same repository-relative format.
* Optionally, a short note describing intended behavior.

You must infer everything else by reading the repository files.

---

## 1. Core objective

Produce a **high-quality, comprehensive pytest test module** for the target module that:

* Maximizes **functional coverage** (happy paths + edge cases + failure modes).
* Encodes **current behavior** (don’t "correct" behavior unless explicitly required).
* Is **stable** (no flaky timing assumptions, no dependence on external network/services).
* Is **readable and maintainable** (tests explain intent clearly).

---

## 2. Mandatory repo discovery steps (do these first)

1. **Locate `pyproject.toml`** at repo root.
2. Determine where tests must live by inspecting `pyproject.toml` and repo conventions:
    * Look for pytest configuration: `[tool.pytest.ini_options]` (especially `testpaths`).
    * If `testpaths` exists, place the test file under one of those directories.
    * Otherwise, follow repo convention (commonly `tests/` at repo root).
3. Identify package layout:
    * Confirm whether source is under `src/` (e.g., `src/<package>/...`).
4. Scan for existing testing utilities and fixtures:
    * `conftest.py`, `tests/helpers.py`, existing fixtures, factories, etc.
5. Determine how tests are run in this project (from README, `pytest.ini`, `pyproject.toml`).

**Do not** guess test locations without checking `pyproject.toml`.

---

## 3. Test file naming and placement rules (strict)

### Naming rule

Construct the test module filename as:

* `"test_" + <full_package_spec_with_dots_replaced_by_underscores> + "_" + <module_basename> + ".py"`

Where:

* **full package spec** is the import path **excluding the module name**.
* **module basename** is the module filename without `.py`.

Example:

* Target: `rpncalc/src/rpncalc/parser.py`
* Import path: `rpncalc.parser`
* Full package spec: `rpncalc`
* Module basename: `parser`
* Test file: `test_rpncalc_parser.py`

If the import path includes subpackages, include them:

* `pkg.subpkg.parser` → `test_pkg_subpkg_parser.py`

### Placement rule

Place this file in the test directory determined in section (2), consistent with `pyproject.toml` pytest config.

---

## 4. "Extend instead of overwrite" rule

If the target test file already exists:

1. Read it fully.
2. Identify:
    * Available fixtures.
    * Covered functions/branches/inputs.
    * Missing scenarios (edge cases, error paths, unusual inputs, platform quirks).
    * Redundant tests, unclear naming, missing assertions.
3. **Preserve** existing tests unless they are clearly incorrect or brittle.
4. Add new tests to close coverage gaps.
5. Refactor gently only when it increases clarity and reduces duplication:
    * Prefer parametrization over copy/paste.
    * Keep behavior identical.

---

## 5. Coverage requirements

Your suite must include, where applicable:

### A) Public API coverage

* Every public function/class/method in the module.
* For classes:
    * construction
    * primary methods
    * repr/str if implemented
    * equality/hash if implemented

### B) Behavior categories

For each callable:

1. **Happy path** (typical valid inputs).
2. **Boundary/edge cases** (empty inputs, minimal inputs, max-like inputs, whitespace, None if allowed).
3. **Invalid inputs and error handling**
    * Verify raised exception types and messages **when stable**.
    * If messages are unstable, assert on exception type only or message substring.
4. **Statefulness** (if any): repeated calls, idempotency, mutation vs immutability.
5. **Platform/path realities** (if file paths involved): Windows vs POSIX separators, newline handling.
6. **Determinism**: outputs should be consistent across runs.

### C) Negative testing discipline

* Do not add "fantasy behavior" tests. Only test:
    * behavior implemented now, or
    * behavior clearly specified in module docstrings or project docs.

If behavior is ambiguous, write tests that document current behavior and add a comment noting ambiguity.

---

## 6. Test design standards (strict)

* Use `pytest` idioms:
    * `pytest.mark.parametrize`
    * `pytest.raises`
    * fixtures for shared setup
* Prefer **pure unit tests**.
* Avoid external network and system dependencies.
* Avoid random unless seeded and asserted appropriately.
* Do not rely on test execution order.
* Keep tests fast; avoid large loops or large data unless necessary.
* Use **descriptive test names**: `test_<unit>_<condition>_<expected>()`.

---

## 7. Quality bar for assertions

Each test must have:

* A clear "arrange / act / assert" structure (can be implicit, but readable).
* Assertions that check **meaningful outcomes** (not just "it runs").
* When comparing complex structures, assert structure and key properties, not only stringified output.

---

## 8. Optional improvements (allowed, but constrained)

You may add:

* `conftest.py` fixtures **only** if it reduces duplication across multiple tests (if the module exists, read it and update as necessary).
* Small test helpers inside the test module (for existing module, consider reusing any suitable fixtures already defined before creating new ones).

You may **not** change production code unless explicitly instructed. If you find a bug or design flaw, note it in comments or a short section at the end of your response.

---

## 9. Output format (what you must produce)

Return:

1. The **exact path** where the test file must be placed (repo-relative).
2. The complete contents of the test file.
3. A short checklist of what is covered (functions/classes + key scenarios).

---

