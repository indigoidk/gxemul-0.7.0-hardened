## 7. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  Test these; do not ratify them:**
  1. at all five sites the fix returns before any TRANSFER data is written, and the `return` is OUTSIDE the latch;
  2. the five new bits `1 << 13` .. `1 << 17` are distinct and collide with no existing `SGIRE_W_*` bit, and the
     demoted BADCOLOR sentence plus the new "next free bit is 1 << 18" sentence are true;
  3. each new message keeps its old key phrase (the witness attributes on those), and S5's new text gains the
     `[ sgi_mte:` prefix the old one lacked;
  4. the kill table is VALID -- base all green, the null medium all red, every log ends with its sentinel -- and each
     mutant in `mutants_564.py` / `mutants_564b.py` is the edit its name says;
  5. the gate block pins every row by name and both denominators by equality, and each `^<name>  .*ok$` pattern can
     match exactly one probe line (names of at most 14 characters in a 16-column field).

**Q2 -- THE SMALLEST EDIT, AND THE FLOOR QUESTION.**  Against the fixed `do_mte_transfer()` and the latch enum: what is
the smallest edit that brings back a guest-visible defect at one of S1-S5 (the process ending, a write the decline
should prevent, an unbounded or missing announcement) while all 53 rows stay green?  Name the row you expect to stay
green.  And the vacuity floor's clause (d), asked of the shipped composite: does a mutant in the DEPENDS-ON enumeration
(PRETABLE section 6 -- the predicates dominating the edits, walked only to the function boundary, plus the latch) sweep
the detector clean?

**Q3 -- ROW VALIDITY.**  Section 5 lists the rows that NO mutant turned red (three controls, and `lin fill a` in table
1 -- table 2 added the growth mutant for it).  Is any other row's channel unable to vary under the mutant PRETABLE
section 4 names for it?  Is any row a survival oracle at a site where the guarded and the unguarded code both survive?

**Q4 -- RECORDS.**  Every ADDED comment sentence in the diff that asserts an observable consequence: true of the code,
and carried by a row or by an explicit no-row sentence (PRETABLE section 2)?  Any claim in sections 1-2 of this brief
that the inlined material does not support?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: CLOSE / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`, then
Q1-Q4.
