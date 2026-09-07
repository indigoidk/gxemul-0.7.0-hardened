# DESIGN SCOPING (read-only) — two register-assignment defects in one Alpha PALcode handler

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees. **A recent panel had seven of nine seats confirm a premise stated wrongly.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. THE TWO DEFECTS — both verified by reading, both one token

`PAL_OSF1_swpctx` in `src/cpus/cpu_alpha_palcode.c` swaps process context. Two register
assignments in it look wrong, and in both cases a comment states the intent the code misses.

**(A) The return register.**

    /*  Return old context in v0.  */
    cpu->cd.alpha.r[ALPHA_A0] = cpu->cd.alpha.ctx;

The comment says `v0`; the store is to `ALPHA_A0`. `ALPHA_V0` exists and is used correctly
elsewhere in the same file. The ABI wrapper `alpha_pal_swpctx` in
`src/include/thirdparty/alpha_cpu.h` declares its return register `__asm("$0")` and ends
`return (v0);`.

**(B) The page-table base.**

    // Update all variables in the pcb simultaneously:
    cpu->cd.alpha.pcb.apcb_ptbr   = new_ptbr;      <- correct
    ...
    cpu->cd.alpha.pcb.apcb_ptbr   = new_flags;     <- should this be apcb_flags?

`apcb_ptbr` is assigned twice; `apcb_flags` appears never to be assigned at all. If that reading is
right, then after any `swpctx` the page-table base holds the flags word — and
`alpha_translate_v2p()` opens with `base = cpu->cd.alpha.pcb.apcb_ptbr << ALPHA_PAGESHIFT`.

## 2. THE QUESTIONS

**Q1 — are both readings right?** In particular for (B): is `apcb_flags` genuinely never written
anywhere, and is `new_flags` genuinely otherwise dead? **If either is used somewhere I have not
looked, (B) is not a defect and I want to know before writing a fix.**

**Q2 — are the two fixes right, and are they ONE change or TWO?** This project's reopening rule
lets a round take a second site only if one fix design covers both and one test covers both with no
new observation. Same function, same class, same file — but say so explicitly if you disagree, and
say why.

**Q3 — what else is wrong in this handler?** Both defects are of the same species: an assignment to
the wrong member of a struct or register file, next to a comment asserting the right one. **A third
instance is more likely than not.** Please read the whole handler, including the context-SAVE half
above the load, and the surrounding PALcode cases.

**Q4 — REMOVED.**  This brief originally asked for the smallest guest program that would witness each
defect.  That question got the whole run refused by a content filter at 145 KB, and the measured
discriminator across six runs is that asking a seat to BUILD SOMETHING THAT TRIGGERS A DEFECT is
refused while asking WHAT IS TRUE is not.  So the witness construction goes elsewhere and this brief
asks only about the readings and the scope.

**Q5 — the accept side, stated as a property rather than as a program.**  If these are fixed, what
PROPERTY must a regression test assert so that a later edit cannot silently undo them?  Note a test
that only checks `v0` after a `swpctx` would still pass if someone assigned BOTH `a0` and `v0`, so
the property is not simply *the right register holds the right value*.  **Name the property; do not
write the test.**

## 3. WHAT I AM NOT ASKING

Do not write the diff. Do not write the probe. I want the readings checked, the round's scope
settled, and the witness shape named.

**If, while verifying a claim, you found something ELSE — say so.** Four of tonight's findings
arrived that way, including (B) itself, which came out of a brief that asked only whether Alpha
machines can run anything.
