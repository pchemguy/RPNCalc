https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07

## RUN_TEST_SUITE_AND_FIX_TASK

You are tasked with **running the repository test suite** (or a targeted subset) using `pytest`, diagnosing failures, and applying the **minimum safe changes** needed to reach a clean pass, while strictly following repository rules.

---
## 1. Core objective

Run the repo test suite and fix all issues until `pytest -v` from the repository root passes.

---

## 2. Read `AGENTS.md`

You must read and operationalize root `AGENTS.md` and any files it requires you to read.

---

## 3. Failure triage workflow (strict, expanded)

When tests fail, you must perform **systematic triage** before making any code changes.

### 3.1 Classify failures by root cause

Group failures by **underlying cause**, not by test name or traceback surface.

At minimum, classify each failure as one of:

* **Import / resolution failure**
* **Test logic failure**
* **Production logic failure**
* **Environment or configuration failure**

Do not proceed to fixes until all failures are classified.

---

### 3.2 Import and resolution failure analysis (mandatory, first)

If any failure involves `ImportError`, `ModuleNotFoundError`, or unresolved symbols:

#### 3.2.1 Determine import type

For each failing import, determine whether it is:

1. **Standard library dependency import (missing `import` statements)**
    * Example: `import os`, `from number import Real`
2. **External dependency import**
    * Example: `import numpy`, `from rich.console import Console`
3. **Local project import**
    * Example: `from rpncalc.engine import Calculator`
    * Example: `from .parser import tokenize`

Proceed according to the corresponding branch below.
Important: if the issue cannot be fixed and the task must be aborted, you must
- complete full analysis of all failed tests,
- make best effort to determine which failures can likely be fixed automatically.
- provide detailed report about all fixable issues and issues requiring human's intervention.

---

#### 3.2.3 Standard library dependency imports

1. Determine whether the dependency can be **unambiguously identified**:
    * The import name clearly maps to a known package name, or
    * The dependency is already referenced elsewhere in the repo (docs, comments, pyproject.toml extras).
2. If **unambiguous**:
    - Add missing `import` statements.
    * Continue the task.
3. If **ambiguous** (unclear package name, multiple possible distributions, unclear versioning):
    * Produce a **detailed dependency analysis**:
         * failing import statement
         * candidate packages (if any)
         * why ambiguity cannot be resolved locally
    * **Abort the task** without making speculative changes.

#### 3.2.3 External dependency imports

For missing **external dependencies**:

1. Determine whether the dependency can be **unambiguously identified**:
    * The import name clearly maps to a known package name, or
    * The dependency is already referenced elsewhere in the repo (docs, comments, pyproject.toml extras).
2. If **unambiguous**:
    * Add the dependency to `pyproject.toml` in the appropriate section:
         * `[project].dependencies` or
         * `[project.optional-dependencies]` (e.g. `dev`)
       * Use the most flexible constraint:
           * ideally, unconstrained specification,
           * **minimum version constraint** consistent with existing deps, if unconstrained specification cannot be used.
           * add missing `import` statements, if applicable.
       * Continue the task.
3. If **ambiguous** (unclear package name, multiple possible distributions, unclear versioning):
    * Produce a **detailed dependency analysis**:
        * failing import statement
        * candidate packages (if any)
        * why ambiguity cannot be resolved locally
    * **Abort the task** without making speculative changes.
4. If the agent **does not have Internet access** and dependency identity cannot be confirmed locally:
    * Produce a **detailed import error analysis**.
    * **Abort the task**.
5. If the agent **has Internet access** and can unambiguously identify and install all missing dependencies:
    * Install dependencies.
    * Continue the task.

---

#### 3.2.4 Local project imports

For missing or failing **local imports**, the agent must **not** immediately patch source code.

Instead, perform the following analysis:

##### A) File-level resolution

* Verify whether the imported module file exists in the current source tree.
* If the file does not exist:
    * Examine recent commit history (several most recent commits) to determine whether:
        * the file was renamed,
        * the file was moved,
        * the file was removed intentionally.

##### B) Identifier-level resolution

* If the module exists but the imported identifier does not:
    * Examine recent commits affecting that module to determine whether:
        * the identifier was renamed,
        * functionality was split or merged,
        * the identifier was intentionally removed.

##### C) Documentation and policy alignment

Consult:

* `AGENTS.md`
* Files referenced by `AGENTS.md`
* Module docstrings
* Naming or refactoring guidelines documented in the repo

Use these sources to infer **intended naming or refactoring schemes**.

##### D) Fix selection rule

* If a **likely refactor or rename** can be determined with high confidence:
    * **Update the test code** to match the new structure.
    * Do **not** add compatibility aliases or dummy exports source code.
* If intent is unclear or conflicting:
    * Produce a **detailed ambiguity report**.
    * **Abort the task**.

---

### 3.3 Non-import failures

For failures not related to imports:

1. Determine whether the failure is due to:
    * incorrect test assumptions,
    * outdated tests after refactor,
    * incorrect production behavior,
    * misconfiguration.
2. Apply the **minimum change** that resolves the root cause and is consistent with:
    * current implementation,
    * documented contracts,
    * `DEV_STRATEGY.md`.

---

### 3.4 Global constraints on fixes

Across all failure types:

* Prefer updating **tests** when failures are caused by refactors or contract changes.
* Prefer updating **source code** only when tests correctly encode current documented behavior.
* Never apply "compatibility hacks" (dummy imports, alias re-exports, blanket try/excepts) to silence failures.

If a correct fix cannot be determined confidently, **abort and report**.

---

## 4. Fixing constraints

### 4.1 Allowed modifications

You may modify:

* failing test files
* the production module(s) under test
* shared test utilities (`conftest.py`, helpers) only if it reduces duplication or fixes a systematic issue
* configuration only if the failure is clearly caused by misconfiguration and the intended config is evident from repo docs

### 4.2 Prohibited modifications

You must not:

* delete tests to make the suite pass
* weaken assertions without replacing them with equally meaningful assertions
* introduce speculative behavior not evidenced by code/docs
* silence failures by catching broad exceptions or suppressing warnings unless repo docs require it
* change unrelated files

### 4.3 Working tree safety

Assume the working tree may be dirty:

* Do not discard unrelated changes.
* Touch the smallest set of files needed.
* If you detect unexpected changes that affect your ability to reason safely, stop and report.

---

## 5. Iteration loop

Use this loop until clean:

1. Run (targeted if applicable, e.g. `pytest -v <test_file.py>`)
2. Fix minimum set of issues
3. Re-run the same scope
4. Once green, run `pytest -v` full suite
5. Stop only when full suite passes

Avoid large "batch changes" without rerunning tests.

---

## 6. Output requirements (order matters)

Return:

1. **Repo discovery summary**
    * how tests are configured (testpaths/addopts)
    * what command(s) you ran
2. **Test run results summary**
    * pass/fail counts (or a concise failure list)
3. **Root-cause grouping**
    * each root cause and the associated failures
4. **Changes made**
    * files changed and why (brief, factual)
5. **Verification**
    * confirmation that `pytest -v` from repo root passes

---

### Notes

* Prefer correctness and minimal diffs over refactoring.
* Keep fixes aligned with `DEV_STRATEGY.md` and other repo guidance surfaced via `AGENTS.md`.
