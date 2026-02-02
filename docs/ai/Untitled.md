## 3. Test file naming and placement rules (strict)

### Naming rule

Construct the test module filename as:

```
test_<subpackage_chain_with_underscores>_<module_basename>.py
```

Where:

* **subpackage chain** is the import path **between the top-level package and the module**, with `.` replaced by `_`.
* The **top-level package name is always omitted**.
* **module basename** is the module filename without `.py`.
* If the module is located directly under the top-level package (i.e. no subpackages), the filename is simply:

```
test_<module_basename>.py
```

(no extra underscore).

---

### Formal definition

Given import path:

```
<top_pkg>.<subpkg1>.<subpkg2>....<module>
```

The test filename is:

```
test_<subpkg1>_<subpkg2>_..._<module>.py
```

If there are no `<subpkg*>` segments:

```
test_<module>.py
```

---

### Examples

| Target file path                           | Import path                 | Test filename               |
| ------------------------------------------ | --------------------------- | --------------------------- |
| `rpncalc/src/rpncalc/parser.py`            | `rpncalc.parser`            | `test_parser.py`            |
| `rpncalc/src/rpncalc/io/serializer.py`     | `rpncalc.io.serializer`     | `test_io_serializer.py`     |
| `rpncalc/src/rpncalc/ui/cli/formatting.py` | `rpncalc.ui.cli.formatting` | `test_ui_cli_formatting.py` |
| `src/pkg/subpkg/parser.py`                 | `pkg.subpkg.parser`         | `test_subpkg_parser.py`     |
| `src/pkg/a/b/c/mod.py`                     | `pkg.a.b.c.mod`             | `test_a_b_c_mod.py`         |

---

### Invariants (non-negotiable)

* Never include the top-level package name in test filenames.
* Always include the module name.
* Never emit empty segments or double underscores.
* The filename must be derivable **mechanically** from the import path.

---

