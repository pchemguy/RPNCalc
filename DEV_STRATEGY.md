## Core Principles

* **Layered design**: parsing, evaluation engine, and user interface are strictly decoupled.
* **Feasibility probes first**: early components may be intentionally minimal or "dumb" to validate integration paths and contracts.
* **Explicit contracts**: each module exposes a narrow, well-defined interface.
* **Test-driven evolution**: behavior is locked in with tests before refinement.
* **No speculative behavior**: undefined or ambiguous behavior is deferred, not guessed.
* **Incremental evolution**: treat all code and assumptions as tentative, prioritize clarity and reversibility