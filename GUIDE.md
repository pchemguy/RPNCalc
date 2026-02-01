## 🛠 Project Blueprint: The Robust RPN Engine

### 1. Learning Goals

Beyond basic state management, this project is designed to teach you:

* **Decoupling Logic:** Separating the "Engine" (math/logic) from the "Interface" (CLI/User input).
* **Dispatch Patterns:** Using dictionaries instead of long `if/elif` chains to map operators to functions.
* **Testing Suites:** Writing `pytest` or `unittest` cases that cover both "Happy Paths" and "Edge Case Minefields."
* **Graceful Recovery:** Ensuring the program doesn't crash when it hits an error, but instead provides a helpful message and stays ready for the next command.

### 2. Architecture (Modular Design)

To practice real-world development, don't put everything in one file. Structure it like this:

* `exceptions.py`: Define your custom errors (e.g., `RPNError`, `InsufficientOperandsError`).
* `engine.py`: The `Calculator` class that manages the stack.
* `parser.py`: Logic to clean and validate input strings.
* `main.py`: The loop that interacts with the user.

---

### 3. Edge Cases

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

### 4. Implementation Strategy

**Step 1: The Core Engine**

Create a `Calculator` class. Instead of `if char == '+':`, use a mapping:

```python
self.operators = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}

```

**Step 2: Custom Exceptions**

Don't just use `print("Error")`. Create a hierarchy so your UI can catch them specifically:

```python
class RPNError(Exception): pass
class StackUnderflowError(RPNError): pass
class CalculatorDivisionError(RPNError): pass

```

**Step 3: The Testing Phase (TDD)**

Before you write the logic for the `*` operator, write a test for it.

* **Test Case A:** `evaluate("3 4 *") == 12`
* **Test Case B:** `evaluate("3 *")` raises `StackUnderflowError`.

---

### 5. Advanced Features

Once the basics are solid, try adding these to test your design's flexibility:

1. **Undo Command:** Add a `z` or `undo` token that reverts the stack to the previous state.
2. **Variable Support:** Allow users to store values (e.g., `10 STO x`, then `x 5 +` results in `15`).
3. **Advanced Math:** Integrate the `math` module for `sin`, `cos`, and `sqrt`.

> **Pro Tip:** When handling division, remember that in RPN `10 2 /` means $10 \div 2$. Because stacks are **Last-In, First-Out (LIFO)**, the first number you pop is actually your divisor (the 2), and the second number popped is your dividend (the 10).

---


