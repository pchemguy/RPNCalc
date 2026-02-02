# Development Strategy

## Core Principles

* **Layered design**: parsing, evaluation engine, and user interface are strictly decoupled.
* **Feasibility probes first**: early components may be intentionally minimal or "dumb" to validate integration paths and contracts.
* **Explicit contracts**: each module exposes a narrow, well-defined interface.
* **Test-driven evolution**: behavior is locked in with tests before refinement.
* **No speculative behavior**: undefined or ambiguous behavior is deferred, not guessed.
* **Incremental evolution**: treat all code and assumptions as tentative, prioritize clarity and reversibility

## Development Mode

* Start with **absolute-minimum implementations** that cannot fail structurally.
* Gradually replace probes with stricter, validated implementations.
* Refactoring is expected and encouraged once contracts are stabilized.

## Feasibility Probes (FPs)

- Design probes for
    - High risk essential code to retire risks early.
    - Low risk code to implement gradual evolution of complex logic.
- Prefer adding a potentially low value FP to omitting a medium value FP.
- Treat FPs as stepping stones toward complex logic.
- Place FPs in separate companion modules next to target modules with `_fp` suffix (e.g., `parser_fp` or `engine_fp`).
- Gradually transform minimalistic code in FPs by extending and refactoring as appropriate into code to be included in subsequent prototypes.
- When introducing new or extending existing features/functionality or considering alternative implementations, prefer adding new feasibility probes to the companion `_fp` module, testing them, possibly performing early evolution. Once a particular implementation is selected via probing/testing, the code can be transferred/refactored into the production module (without `_fp`).
- When implementing feasibility probes, prefer simple probe routines with descriptive names. For example, for `tokenize` routine in `parser` you might create `tokenize_ws_only` and `tokenize_normalize` in `parser_fp`, testing in `test_parser_fp`, then refactoring `tokenize_ws_only` and `tokenize_normalize` into `tokenize` routine in `parser` and forming `test_parser` test suite from `test_parser_fp`.

