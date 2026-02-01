https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07

## Prompt: `CREATE_TEST_SUITE_TASK`

You are an AI engineering agent tasked with **creating or extending** a **comprehensive `pytest` test suite** for a specified Python module.

## 0. Inputs you will be given

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

## 2. Read `AGENTS.md`

You must read and operationalize `AGENTS.md` before creating or modifying any files.

---

## 3. Test file naming and placement rules (strict)

### Naming rule

Construct the test module filename as:

```
test_<full_package_spec_with_dots_replaced_by_underscores>_<module_basename>.py
```

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

## 4. Extend-in-place rule

If the target test file already exists:

1. Read it fully.
2. Identify:
    * Defined fixtures.
    * Covered functions/branches/inputs.
    * Missing scenarios (edge cases, error paths, unusual inputs, platform quirks).
    * Redundant tests, unclear naming, missing assertions.
3. **Preserve** existing tests unless they are clearly incorrect or brittle.
4. Add new tests to close coverage gaps.
5. Refactor gently only when it increases clarity and reduces duplication:
    * Prefer parametrization over copy/paste.
    * Keep behavior identical.

---

## 5. Coverage requirements and Coverage Matrix (required, before implementation)

### Coverage Matrix

Before adding or modifying tests, construct a **Coverage Matrix**.

#### Rows

* Each public function, class, and method
* Internal helpers that implement non-trivial logic and affect observable behavior

#### Columns

1. Typical usage paths
2. Boundary conditions implied by the code
3. Error or exceptional behavior implemented in the code
4. Statefulness or repeated invocation effects (if any)
5. Determinism / purity
6. Interaction with external state (filesystem, environment, time, randomness), if applicable

For each cell:

* ✅ covered (cite test)
* ❌ uncovered (describe behavior to be tested)
* N/A with justification

### Requirements

Your suite must include, where applicable:

#### A) Public API coverage

* Every public function/class/method in the module.
* For classes:
    * construction
    * primary methods
    * repr/str if implemented
    * equality/hash if implemented

#### B) Behavior categories

For each callable:

1. **Happy path** (typical valid inputs).
2. **Boundary/edge cases** (empty inputs, minimal inputs, max-like inputs, whitespace, None if allowed).
3. **Invalid inputs and error handling**
    * Verify raised exception types and messages **when stable**.
    * If messages are unstable, assert on exception type only or message substring.
4. **Statefulness** (if any): repeated calls, idempotency, mutation vs immutability.
5. **Platform/path realities** (if file paths involved): Windows vs POSIX separators, newline handling.
6. **Determinism**: outputs should be consistent across runs.

#### C) Negative testing discipline

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
- Assertions
    * Assert observable behavior
    * Do not assert internal implementation details unless part of the contract (as indicated in docstrings or reference docs)
    * For exceptions:
        * assert exception type
        * assert stable message content
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

## 8. Allowed additions

You may add:

* `conftest.py` fixtures **only** if it reduces duplication across multiple tests.
* Small test helpers inside the test module (for existing module, consider reusing any suitable fixtures already defined before creating new ones).

You may **not** change production code unless explicitly instructed. If you find a bug or design flaw, note it in comments or a short section at the end of your response.

---

## 9. Required outputs (order matters)

Return:

1. Repository discovery summary
2. Coverage Matrix
3. Implementation plan mapping matrix gaps to tests
4. Final artifact:
    * exact test file path
    * full test file contents
5. Coverage checklist (functions/classes + key scenarios).

---

## 10. Completion criteria

The task is complete only when:

* All public API behavior is covered
* No Coverage Matrix gap remains unexplained
* Tests pass under the repository’s pytest configuration
* Test file naming and placement rules are satisfied

---

