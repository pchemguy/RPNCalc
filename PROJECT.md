# PROJECT.md

## RPN Calculator (Feasibility- and Test-Driven Development)

This project is a **learning and practice vehicle** for AI-assisted Python development of a small but non-trivial system, emphasizing **incremental prototypes, feasibility probes, and test-driven refinement** toward a clean MVP.

The concrete artifact is a **Reverse Polish Notation (RPN) calculator**, but correctness alone is not the primary goal. The primary objective is to practice **systematic development workflows**: isolating risk, validating assumptions early, enforcing clean layering, and evolving prototypes without premature over-engineering.

### Architecture (Target, but evolves incrementally)

* `parser`: transforms raw input into token lists (initially minimal, total, non-validating).
* `engine`: pure stack-based evaluation logic with operator dispatch.
* `exceptions`: explicit error taxonomy (introduced only when behavior is defined).
* `cli`: interactive loop with graceful recovery and persistent state.

---

## Tentative Design/Development Plan

**IMPORTANT**: This is an initial plan. Treat every aspect as tentative and assume that everything may change during prototyping phase.

### Target architecture (minimal but real)

```
rpncalc/
  src/rpncalc/
    __init__.py
    exceptions.py
    engine.py
    engine_fp.py
    parser.py
    parser_fp.py
    cli.py
  tests/
    test_engine.py
    test_engine_fp.py
    test_parser.py
    test_parser_fp.py
    test_cli_smoke.py
pyproject.toml
AGENTS.md
PROJECT.md
README.md 
```

**Layering**

* **engine**: pure logic (stack, operators, evaluation). No printing.
* **parser**: tokenization + numeric conversion + normalization rules.
* **cli**: REPL loop, error presentation, "graceful recovery".
* **exceptions**: one place for your error taxonomy.

This lets you practice: isolated unit tests (engine/parser) + higher-level tests (cli).

---

### Edge Cases

| Scenario                     | Description                                                   | Expected Behavior                                                                             |
| ---------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Stack Underflow**          | Input: `+` when the stack is empty (or has only one number).  | Raise `StackUnderflowError` and show detailed error message.                                  |
| **Division by Zero**         | Input: `5 0 /`.                                               | Handle the standard division exception and show detailed error message.                       |
| **Unknown Token**            | Input: `3 4 $`.                                               | TBD                                                                                           |
| **Type Chaos**               | Input: `3 four +`.                                            | TBD                                                                                           |
| **Whitespace variations**    | Input: `3   4 +` vs `3 4+`.                                   | TBD                                                                                           |
| **Trailing Data**            | Input: `5 5 + 10`                                             | The stack should result in `[10, 10]`. Does your UI notify the user there is "leftover" data? |
| **Floating Point Precision** | Input: `0.1 0.2 +`                                            | Results in `0.30000000000000004`. Should you round to a specific precision?                   |
| **Unary Operators**          | Input: `-5 abs`                                               | Handling operators that only require *one* number instead of two.                             |
| **Memory Persistence**       | User enters `5`, then `10`, then `+` in three separate lines. | The stack must persist across multiple input calls.                                           |
| **Large Numbers**            | Input: `10**1000`                                             | Handling potential `OverflowError` in Python for extreme calculations.                        |

---

### Define "semantics" now (resolves your TBDs)

#### Tokens & parsing

* Split by whitespace **only**. That means `3 4+` is invalid (token `4+` is not a number/operator).
* Accept:
    * integers: `42`, `-5`
    * floats: `3.14`, `-0.5`, `.5`, `5.`
    * scientific: `1e3`, `-2.5e-2`
* Reject:
    * `10**1000` as a *literal* (it’s an expression, not a number token). If you want big numbers, input the full integer directly or add a `pow` operator.

#### Unknown token

Raise `UnknownTokenError(token=...)`.

#### Type chaos (`"four"`)

Also `UnknownTokenError` (or a distinct `NumberParseError`; both are fine—pick one). I’d separate them to keep UX precise.

#### Underflow

Raise `StackUnderflowError(op='+', needed=2, have=1)`.

#### Trailing data

**Allowed.** RPN calculators commonly leave remaining items on the stack.

* `5 5 + 10` ends with stack `[10, 10]`.
* UI: after each line, print top-of-stack (optional), but do not warn by default.

#### Floating point precision

**Do not round in the engine.** Return Python floats as-is.

* UI can offer optional formatting (e.g., `--precision 10`) later.
  This cleanly separates "math correctness" from "display policy".

#### Unary operators

Support both unary and binary operators by storing `arity` with each op.

#### Memory persistence across lines

The CLI owns one `Calculator` instance and reuses it for the entire session.

#### Large numbers

Python `int` is arbitrary precision; `10**1000` isn’t a literal token, but very large integer literals *are* fine.
For floats, you can hit `OverflowError` or `inf`. Decide:

* Engine: allow `inf` to exist (it’s a float), but raise `NumericError` on `OverflowError` from `math` functions if you add them.

---

### Exceptions taxonomy (small but expressive)

* `RPNError(Exception)`
    * `ParseError(RPNError)`
        * `UnknownTokenError(ParseError)`
        * `NumberParseError(ParseError)`
    * `EvaluationError(RPNError)`
        * `StackUnderflowError(EvaluationError)`
        * `DivisionByZeroError(EvaluationError)`
        * `DomainError(EvaluationError)` (later: `sqrt(-1)`, etc.)

You want **one catch** in CLI: `except RPNError as e:` print friendly message; continue.

---

### Engine design (what to build first)

#### Core object

`Calculator` with:

* `stack: list[Number]` (start with `float | int`, but simplest is `float` everywhere at first)
* `evaluate_tokens(tokens: list[str]) -> None` (mutates stack)
* `evaluate_line(line: str) -> None` (calls parser → tokens → eval)

#### Operator registry

Avoid `lambda` for anything non-trivial; use named functions so:

* tracebacks are readable
* you can unit-test operator functions directly if you want

Represent ops as:

* `Operator(name, arity, func)`

This also makes it trivial to add `undo`, `sqrt`, etc.

---

### Prototype-driven workflow (what to practice)

#### Prototype 0 — skeleton + "red tests"

**Deliverables**

* packaging layout (`src/…`)
* empty modules
* failing tests that encode the semantics above

**Tests**

* `test_eval_add_basic`
* `test_underflow_binary_op`
* `test_unknown_token`
* `test_parser_rejects_concat_token` (`"4+"`)
* `test_trailing_data_kept`

#### Prototype 1 — parser + engine for numbers and `+ - * /`

**Goal**

* Make tests pass.
* Keep engine pure and deterministic.

**Edge tests**

* division by zero
* multiple spaces
* negative numbers
* scientific notation

#### Prototype 2 — CLI REPL + recovery

**Goal**

* you can type multiple lines and the stack persists
* errors don’t terminate session
* optional commands: `p` (print stack), `c` (clear), `q` (quit)

**Tests**

* "smoke" test using `subprocess` (or keep it minimal and test the REPL loop via dependency injection of input/output streams).

#### Prototype 3 — extendability exercise

Add **one** feature that stresses architecture:

* unary op (`abs`)
* and/or `undo` (which forces state snapshotting)

This is where you practice refactoring without breaking tests.

---

### Concrete operator semantics (recommended defaults)

* `/` uses true division (float). If both operands are ints, you *still* return float.
* If divisor is exactly zero:
    * raise `DivisionByZeroError(dividend=..., divisor=...)`
* For `-` and `/`, remember order:
    * pop `b` then `a`, compute `a - b`, `a / b`

---
