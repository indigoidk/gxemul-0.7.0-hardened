# det_20261104/table1/VERDICT.md -- erratum (2026-11-05, main loop, from pvr pass 4's F8 and repair 4's report)

CORRECTS line 13's REASON, not its classification: "equivalent: the render loop has no early exit after the reset's old position."
That reason is false -- pvr_render() has a frame-bounds `return` after the reset's old position (see r3_20261105/PRETABLE_3.errata.md,
the second erratum, F8, which corrects the same sentence in PRETABLE_3 and gives the line numbers).  M17 (the reset moved to the end of
pvr_render) stays EQUIVALENT for the reason that erratum states: that return precedes every header of its render, and the field is zero
there -- from DEVINIT, or from the previous render's end, where M17 now resets it.  VERDICT.md itself is a measurement record and is not
rewritten.
