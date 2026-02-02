https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07

## RUN_TEST_SUITE_AND_FIX_TASK

You are tasked with running the repository test suite per root `AGENTS.md`, diagnosing failures, and applying the minimum safe changes needed to reach a clean pass, while strictly following repository rules, particularly `TEST_FAILURE_TRIAGE.md`.

---
## 1. Core objective

- Run the repo test suite and fix all issues until all tests pass.
- You must read and operationalize root `AGENTS.md` and any files it requires you to read.

---

## 2. Iteration loop

Use this loop until clean:

1. Start by running the full test suite from the repository root per root `AGENTS.md`:
    - If the full suite passes, the task is complete.
2. Select a single issue or a focused group of closely related issues.
3. Run only the failing scope associated with the selected issue:
    - Prefer path-based selection using failing test file(s) reported by the selected testing framework.
4. Complete triage per `TEST_FAILURE_TRIAGE.md`.
5. Create and implement a fixing plan:
    - The plan must address only the selected root cause.
    - Changes must be minimal and consistent with repo docs and contracts.
6. Re-run the same focused scope as in Step 3:
    - If any selected tests still fail, return to Step 4.
    - If all selected tests pass, return to Step 1.

---

## 4. Output requirements (order matters)

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
