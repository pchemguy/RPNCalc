https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07

## RUN_TEST_SUITE_TASK

You are tasked with **running the repository test suite** (or a targeted subset) using `pytest`, diagnosing failures, and applying the **minimum safe changes** needed to reach a clean pass, while strictly following repository rules.

---
## 1. Core objective

Run the repo test suite and fix all issues.

---

## 2. Read `AGENTS.md`

You must read and operationalize root `AGENTS.md` and any files it requires you to read.

---

## 3. Failure triage workflow (strict)

When tests fail:

1. **Group failures by root cause**, not by test name.
2. For each root cause, identify whether it is:
    * a test bug (incorrect assumption, brittle assertion, wrong import path, order dependence)
    * a production bug (actual incorrect behavior)
    * an environment/config issue (missing dependency, path misconfig, wrong test discovery)
3. Apply the **minimum change** that resolves the root cause and is consistent with repository docs.

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

1. Run (targeted if applicable)
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

If you are blocked (missing files, cannot run tests), explicitly state what is missing and what you could not verify.

---

### Notes

* Prefer correctness and minimal diffs over refactoring.
* Keep fixes aligned with `DEV_STRATEGY.md` and other repo guidance surfaced via `AGENTS.md`.
