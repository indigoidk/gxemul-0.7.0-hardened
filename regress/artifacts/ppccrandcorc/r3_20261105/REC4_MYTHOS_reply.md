MYTHOSRECR575

VERDICT: all five false records corrected (F1, F4, F5 in dated errata; F2, F3 in the probe in place); the probe edit is proved text-only by AST comparison against table 3's frozen instrument.

- F1: errata withdraws "a mask with bits above 4 is the fix" (CLOSURE3.md:736-737). Field masks are closed over m = 0..30 by enumeration only; masks above bit 4 act on raw shifted words (`cpu_ppc_instr.c:2730-2731`) and import neighbouring fields, which `v575c.py:94` cannot model. They are outside the denominator and disclosed, not proved.
- F2: the `64 crorc baread` note (`ppc_crlogic_probe.py:386`) now reads "a=0 at the fix; a!=0 is red". It no longer says "every mask", since read mask 0 keeps a = 0 and is caught elsewhere.
- F3: the docstring (lines 54-58) now splits DELIBERATELY UNCOVERED into "EQUIVALENT, proved" and "DISCLOSED, NOT equivalent: the crandc toggle of (5)", with the crandc 31,0,1 over CR 0 counterexample.
- F4: errata withdraws "red on every result-1 row" (CLOSURE3.md:732). crorc C = 2 lets `64 crorc 10` and `32 crorc 10` pass. The setbits rows close every C != 1 directly.
- F5: errata withdraws the "would cost more rows" claim (CLOSURE3.md:714-715). One whole-CR session (seed 0x2; crandc 31,30,31; crorc 30,30,0; want 0x3) catches both set-literal families, so three rows suffice. Four is the single-instruction minimum. The four measured rows stay.
- No copy of F1, F4 or F5 exists in the probe. The lines checked are listed in RECORDS4_NOTE.md.

Text-only proof: with the module docstring dropped and every string constant replaced by a placeholder, `ast.dump` of the in-tree probe equals that of `table3/probe70_frozen.py` (True, 53679 = 53679). The raw diff shows exactly the two text hunks. Max line width stays at 143. The in-tree probe now differs from the frozen instrument in printed text only.

Files touched: edited `regress/ppc_crlogic_probe.py`; wrote `r3_20261105/ppc_crlogic_probe.py.pre_rec4` (md5 matches the frozen probe), `CLOSURE3.errata.md`, `RECORDS4_NOTE.md`. CLOSURE3.md, PRETABLE_3.out and table3/ are untouched. One disclosure: the py_compile check briefly created `regress/__pycache__`, which I removed. The Gemini second reading called for by DISPOSITION.md is still owed.
