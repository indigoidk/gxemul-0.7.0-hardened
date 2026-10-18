## 7. Questions

**Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py` (and `regress/gate_arm.sh`).**  Do not read
`regress/artifacts/` or `tools/pipeline/ledger.json` -- everything this brief takes from them is inlined above.  This is
an ordinary code review of error handling in an emulated graphics transfer engine and of the regression test for it.

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  Test these; do not ratify them:**
  1. at all five sites the change returns before any TRANSFER data is written, and the `return` is OUTSIDE the
     announce-once condition;
  2. the five new bits `1 << 13` .. `1 << 17` are distinct and collide with no existing `SGIRE_W_*` bit, and the
     demoted BADCOLOR sentence plus the new "next free bit is 1 << 18" sentence are true;
  3. each new message keeps its old key phrase, and S5's new text gains the `[ sgi_mte:` prefix the old one lacked;
  4. the measurement tables in sections 2 and 5 are internally consistent (a baseline all green, a non-emulator binary
     all red, every mutant scored below the row count) -- as a records check of what is inlined;
  5. the gate block pins every row by name and both denominators by equality, and each `^<name>  .*ok$` pattern can
     match exactly one test line (names of at most 14 characters in a 16-column field).

**Q2 is not asked of this seat.**

**Q3 -- TEST VALIDITY.**  Is any row's observable unable to differ between the correct code and the defect PRETABLE
section 4 names for it?  Is any row a survival-only check at a site where the correct code and the defect both
survive?  Section 5 lists the rows no table turned red.

**Q4 -- RECORDS.**  Every ADDED comment sentence in the diff that asserts an observable consequence: true of the code,
and carried by a row or by an explicit no-row sentence (PRETABLE section 2)?  Any claim in sections 1-2 of this brief
that the inlined material does not support?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: CLOSE / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`, then
Q1, Q3, Q4.
