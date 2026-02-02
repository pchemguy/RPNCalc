# Development Strategy (DEV_STRATEGY.md)

## Core Principles

- **Layered design**  
    Parsing, evaluation engine, and user interface are strictly decoupled. Each layer owns a single responsibility and communicates only through explicit contracts.
- **Feasibility probes first**  
    Early components may be intentionally minimal, incomplete, or "dumb" in order to validate integration paths, contracts, and evolution strategies before committing to complexity.
- **Explicit contracts**  
    Every module exposes a narrow, well-defined interface. Contracts are stabilized before internal sophistication is increased.
- **Test-driven evolution**  
    Behavior is locked in with tests before refinement or extension. Tests define what is known and intentionally leave undefined behavior unspecified.
- **No speculative behavior**  
    Undefined, ambiguous, or controversial behavior is deferred. The system must not guess, infer intent, or silently enforce "best practices" not explicitly encoded.
- **Incremental evolution**  
    Treat all code and assumptions as tentative. Prioritize clarity, reversibility, and refactorability over completeness or elegance.

---

## Development Mode

- Start with **absolute-minimum implementations** that cannot fail structurally.
- Prefer total, side-effect-free routines in early stages.
- Gradually replace probes with stricter, validated implementations as contracts stabilize.
- Refactoring is expected and encouraged once behavior is fixed by tests.

---

## Feasibility Probes (FPs)

Feasibility probes are a **primary development tool**, not a temporary crutch.

### Purpose

Design feasibility probes to:

- Retire **high-risk, essential uncertainties** as early as possible.
- Enable **gradual, low-risk evolution** of code that is expected to become complex over time.

Prefer adding a potentially low-value FP over omitting a medium-value FP.

---

### Structural Rules

- Feasibility probes live in **companion modules** collocated with their target modules and suffixed with `_fp` (e.g. `parser_fp.py`, `engine_fp.py`).
- Production modules (`parser.py`, `engine.py`, ...) must not import from `_fp` modules.
- Probes may be incomplete, permissive, or redundant by design.

---

### Evolution Workflow

- When introducing new functionality, extending existing behavior, or considering alternative implementations:
    - Prefer adding **new probe routines** to the corresponding `_fp` module.
    - Write focused tests for probe behavior (e.g. `test_parser_fp.py`).
    - Use probes to explore contracts, boundaries, and failure modes.
- Once an implementation strategy is selected:
    - Transfer or refactor the chosen probe logic into the production module.
    - Derive the production test suite from the probe tests.
    - Retain unused probes for historical context unless explicitly retired.

---

### Probe Design Guidelines

- Prefer **small, single-purpose probe routines** with descriptive names.
- Avoid embedding policy or interpretation unless explicitly being probed.
- Keep probes side-effect free whenever possible.

**Example (parser evolution):**

- Implement `tokenize_ws_only` and `tokenize_normalize` in `parser_fp.py`.
- Test them in `test_parser_fp.py`.
- Promote the selected behavior into `parser.tokenize`.
- Form `test_parser.py` by refining the corresponding probe tests.

---
