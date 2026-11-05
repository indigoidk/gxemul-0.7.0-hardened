# PROBE_IDENTITY.md -- the staged regress/ppc_crlogic_probe.py differs from the working copy in its docstring only

Built by build_staged_575.py.  Working copy 25529 bytes md5 141591f8a2de70bfbd9ad4038bcd40d8; staged 25571 bytes md5 75b5510dc724167345a639df60cf6aad; table 3's frozen instrument (regress/artifacts/ppccrandcorc/r3_20261105/table3/probe70_frozen.py) md5 772576e7f1795ff8006c5884148e0fa8.

* `ast.dump` with the module docstring dropped, every string kept: staged == working copy: **True**.
* `ast.dump` with the module docstring dropped and every string constant replaced by `<STR>` (RECORDS4_NOTE.md's method): staged == table3/probe70_frozen.py: **True** (so every row name, seed, instruction, want and order, every function body and every non-string constant is the measured instrument's; the row notes differ only where RECORDS4_NOTE.md says).
* `py_compile`: run by the pretest.  Longest line: 143 characters (the working copy's: 143).

Why: precommit section U (`tools/pipeline/check_score_claims.py`) reads every `N/M` in a gated probe's docstring as a score claim against the gate pin (70).  The seven are historical scores of the 62- and 66-row instruments and an opcode/extended-opcode pair; each is now in words.  Hunks:

```
@@ line 35
- t2).  The pre-fix build scores 52/62 (the ten DISC rows); /bin/true 5/62 and /bin/false 1/62 score CONTROL=FAIL, and an
+ t2).  The pre-fix build scores 52 of 62 (the ten DISC rows); /bin/true 5 of 62 and /bin/false 1 of 62 score CONTROL=FAIL, and an
@@ line 46
-   pre-fix build scores 56/66 (the ten DISC rows); /bin/true 5/66 and /bin/false 1/66 score CONTROL=FAIL.
+   pre-fix build scores 56 of 66 (the ten DISC rows); /bin/true 5 of 66 and /bin/false 1 of 66 score CONTROL=FAIL.
@@ line 60
-   (1) crnand (19/225) is not decoded at HEAD and stops the CPU; it is filed separately as
+   (1) crnand (opcode 19, extended opcode 225) is not decoded at HEAD and stops the CPU; it is filed separately as
```
