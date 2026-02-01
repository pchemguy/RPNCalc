## Prompt: `CREATE_TEST_SUITE_TASK`

### (Coverage Matrix First — Final, Clean)

You are an AI engineering agent tasked with **creating or extending** a **comprehensive `pytest` test suite** for a specified Python module.

---

## 0) Inputs you will be given

You will be provided:

* **Target module path** (one of):

  * a local file path (e.g., `rpncalc/src/rpncalc/parser.py`), or
  * a GitHub repo path reference using the same repository-relative format.
* Optionally, a short note describing intended behavior.

You must infer everything else from repository contents.

---

## 1) Core objective

Produce a **high-quality, comprehensive pytest test module** that:

* Maximizes **behavioral coverage** of the existing implementation
* Reflects **current semantics**
* Is **deterministic, stable, and fast**
* Is **readable and maintainable**

---

## 2) Mandatory repository discovery

Before writing or modifying tests, you must:

1. Locate and read `pyproject.toml`
2. Determine pytest configuration:

   * `[tool.pytest.ini_options]`
   * `testpaths`, markers, plugins
3. Determine source layout (`src/` vs flat)
4. Locate existing testing infrastructure:

   * `pytest.ini`, `conftest.py`
   * shared fixtures or helpers
5. Determine how tests are intended to be executed in this repository

If any of the above cannot be determined, stop and report what is missing.

---

## 3) Test module naming and placement (strict)

### Naming rule

The test filename **must** be:

```
test_<full_package_spec_with_dots_replaced_by_underscores>_<module_basename>.py
```

Examples:

* `rpncalc/src/rpncalc/parser.py`
  → import `rpncalc.parser`
  → `test_rpncalc_parser.py`

* `src/pkg/subpkg/core.py`
  → import `pkg.subpkg.core`
  → `test_pkg_subpkg_core.py`

### Placement rule

Place the test file under a directory specified by pytest configuration (`testpaths`), or follow established repository convention if configuration is absent.

---

## 4) Extend-in-place rule

If the target test file already exists:

1. Read it fully
2. Preserve existing tests unless clearly incorrect or brittle
3. Identify uncovered behavior
4. Extend coverage to close gaps
5. Refactor only when it clearly reduces duplication or improves clarity

---

## 5) Coverage Matrix (required, before implementation)

Before adding or modifying tests, construct a **Coverage Matrix**.

### Rows

* Each public function, class, and method
* Internal helpers that implement non-trivial logic and affect observable behavior

### Columns

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

---

## 6) Test design standards

* Use idiomatic `pytest`
* Prefer parametrization over duplication
* Avoid external dependencies and network access
* No reliance on test execution order
* Keep tests fast and deterministic

### Assertions

* Assert observable behavior
* Do not assert internal implementation details unless part of the contract
* For exceptions:

  * assert exception type
  * assert message content only when stable

---

## 7) Allowed additions

You may add:

* Test helpers inside the test module
* Shared fixtures only if they materially reduce duplication

You may not modify production code unless explicitly instructed.

---

## 8) Required outputs (order matters)

Return:

1. Repository discovery summary
2. Coverage Matrix
3. Implementation plan mapping matrix gaps to tests
4. Final artifact:

   * exact test file path
   * full test file contents
5. Coverage checklist

---

## 9) Completion criteria

The task is complete only when:

* All public API behavior is covered
* No Coverage Matrix gap remains unexplained
* Tests pass under the repository’s pytest configuration
* Test file naming and placement rules are satisfied

---

### Bottom line

You were absolutely correct to object.

**Any list of “don’ts”, “best practices”, or “folklore warnings” is already a failure** in a task-oriented agent prompt.
The constraints must be enforced **structurally**, not rhetorically.

This version does exactly that.

If you want next:

* a **REVIEW_TEST_SUITE_TASK** prompt that audits tests for speculative cases, or
* a **MINIMAL_FEASIBILITY_TEST_TASK** tuned for your RPNCalc bootstrap phase,

say the word.
