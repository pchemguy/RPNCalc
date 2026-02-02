## 3. Failure triage workflow (strict, expanded)

When tests fail, you must perform **systematic triage** before making any code or configuration changes. No fixes may be applied until all failures have been classified and analyzed according to the rules below.

---

### 3.1 Classify failures by root cause

Group failures by **underlying cause**, not by test name or traceback surface.

At minimum, classify each failure as one of:

- **Import / resolution failure**
- **Test logic failure**
- **Source code logic failure**
- **Environment or configuration failure**

Do not proceed to fixes until all failures are classified.

---

### 3.2 Import and resolution failure analysis (mandatory, first)

If any failure involves `ImportError`, `ModuleNotFoundError`, `NameError` related to imports, or unresolved symbols, this section **must be applied first**.

---

#### 3.2.1 Determine import type

For each failing import or unresolved symbol, determine whether it is:

1. **Missing standard-library import**
    - Example: `os.path.exists(...)` used without `import os`
2. **External dependency import**
    - Example: `import numpy`, `from rich.console import Console`
3. **Local project import**
    - Example: `from rpncalc.engine import Calculator`
    - Example: `from .parser import tokenize`

Proceed according to the corresponding branch below.

Important: if the task must be aborted, you must still:

- complete analysis of **all failed tests**,
- identify which failures are likely fixable automatically,
- and produce a detailed report covering all findings.

---

#### 3.2.2 Missing standard-library imports

This category applies **only** when a failure is caused by a missing `import` statement for a Python standard-library module that is referenced by the code.

Procedure:

1. Confirm that the referenced module is part of the Python standard library:
    - Verify by inspecting the failing source code and existing imports.
    - Do not assume stdlib status based on name similarity alone.
2. If confirmed:
    - Add the minimal missing `import` statement(s) to the appropriate source file(s).
    - Follow existing import style in the file (module-level imports, ordering, etc.).
3. Re-run the failing scope to confirm the issue is resolved.

Reclassification rule: If the referenced module is **not** part of the standard library, reclassify the failure as an **external dependency import** and proceed to 3.2.3.  
Abort rule: If stdlib status cannot be determined unambiguously using repository contents, produce a detailed analysis and abort the task.

Abort report must include:

- the failing import or symbol
- file and line numbers where it is referenced
- why stdlib status could not be confirmed locally

---

#### 3.2.3 External dependency imports

For failures caused by missing **external dependencies**:

1. Determine whether the dependency can be **unambiguously identified** using repository contents:
    - clear mapping from import name to package name, or
    - explicit references in documentation, comments, or `pyproject.toml`.
2. If unambiguous:
    - Add the dependency to `pyproject.toml` in the appropriate section:
        - `[project].dependencies` for runtime dependencies, or
        - `[project.optional-dependencies].dev` for test-only dependencies.
    - Prefer the most flexible constraint:
        1) unconstrained,
        2) minimum version consistent with existing dependencies,
        3) other appropriate specification.
    - Add missing `import` statements if applicable.
    - Continue the task.
3. If ambiguous:
    - Produce a detailed dependency analysis:
        - failing import statement
        - candidate packages (if any)
        - reason ambiguity cannot be resolved locally
    - Abort the task without making speculative changes.

Internet access rules:

- If the agent **does not have Internet access** and dependency identity cannot be confirmed locally:
    - Produce a detailed analysis and abort the task.
- If the agent **has Internet access** and all missing dependencies can be unambiguously identified:
    - Add them to `pyproject.toml`.
    - Continue the task.
- If ambiguity remains after best effort:
    - Abort and report.

---

#### 3.2.4 Local project imports

For missing or failing **local project imports**, the agent must **not** immediately modify source code to silence the failure. Instead, perform the following analysis:

##### A) File-level resolution

- Verify whether the imported module file exists in the current source tree.
- If the file does not exist:
    - Examine a limited, recent commit window to determine whether the file was:
        - renamed,
        - moved,
        - intentionally removed.

##### B) Identifier-level resolution

- If the module exists but the imported identifier does not:
    - Examine recent commits affecting that module to determine whether:
        - the identifier was renamed,
        - functionality was split or merged,
        - the identifier was intentionally removed.

##### C) Documentation and policy alignment

Consult:

- `AGENTS.md`
- files referenced by `AGENTS.md`
- module docstrings
- documented naming or refactoring guidelines

Use these sources to infer **intended naming or refactoring schemes**.

##### D) Fix selection rule

- If a likely refactor or rename can be determined with **high confidence**:
    - Update the **test code** to match the new structure.
    - Do **not** add compatibility aliases, dummy exports, or shim imports to source code.
- If intent is unclear, conflicting, or cannot be determined within a bounded analysis effort:
    - Produce a detailed ambiguity report.
    - Abort the task.

---

### 3.3 Non-import failures

For failures not related to imports:

1. Determine whether the failure is due to:
    - incorrect test assumptions,
    - outdated tests after refactor,
    - incorrect source code behavior,
    - misconfiguration.
2. Apply the **minimum change** that resolves the root cause and is consistent with:
    - current implementation,
    - documented contracts,
    - `DEV_STRATEGY.md`.

---

### 3.4 Global constraints on fixes

Across all failure types:

- Prefer updating **tests** when failures are caused by refactors or contract changes.
- Prefer updating **source code** only when tests correctly encode documented behavior.
- Never apply compatibility hacks (dummy imports, alias re-exports, blanket `try/except`) to silence failures.

If a correct fix cannot be determined confidently, **abort and report**.

Abort mode:

- Do not modify code or configuration.
- Produce analysis only.

---
