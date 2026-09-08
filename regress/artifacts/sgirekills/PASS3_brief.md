# #513 pass 3 -- reviewing the REPAIR that pass 2 produced

**VERDICT LINE FIRST.**

This is the repair-chain rule in operation: *a repair made in response to a pass 2 owes its own
pass 2*, because the obligation follows the MATERIAL, not the narrative.  Pass 2 found one floor
breach and three wrong records; all four are repaired; **this pass reviews the repair.**

**The stop condition is a pass that finds ZERO floor breaches** -- but a bare zero does not close
the chain.  If you find nothing, say what you SWEPT: which cells, which mutant shapes.  *"Zero
found"* and *"zero looked for"* must not render the same.

**Please do not simply ratify.**  Three seats said DO NOT SHIP last pass and two were right.  If
this repair is wrong, or incomplete in the same way the thing it repairs was, say so.

Tree: `GXEMUL-SEC/src/`.  Ignore the pristine 2021 `src/` at the project root.

## 1. WHAT PASS 2 FOUND, and what was done about each

**(a) L2 -- clause-(d) floor breach.**  `tex xbit` fires the six WIDTH latches only, sweeping bits
0-5, so giving the TEX read decline an already-used NON-LEN bit escapes:

    SGIRE_W_TEX_RD = 1 << 11  ->  1 << 8  (= SGIRE_W_UNMAP_RD)

predicted 44/44, because the detector's four TEX-read scenarios and its unmapped-read scenario
never share an emulator instance.  **REPAIRED** with two same-instance rows, both orderings.

**(b) L4 -- the enum comment** said *"the next free bit is 1 << 11; the enum ends HERE"* and this
diff took `1 << 11`.  **CORRECTED**: demoted in place, live claim moved to the last enumerator,
matching the repair the same file already applied to `SGIRE_W_PRIM_OP`.

**(c) L4 -- my LINEAR comment** said the `len == 8` guard "keeps tlbi even".  Width does not imply
alignment.  **CORRECTED** at both linear arms.

**(d) L4 -- the probe's contract header** still described six live read kills and deleted row
names.  **CORRECTED** in place beside the original.

**And one claim of mine was WITHDRAWN**: I had said `M8_texaccept` measures the store-first TEX
design.  It does not isolate it -- M8 also removes the announce, so both channels red.

## 2. THE MEASUREMENT -- the repair's own numbers, from its log

```
# #513 pass-2 L2 verification  (scratch clone /tmp/gx513b, frozen instrument)

BASE_pass2        46/46   repaired detector, CLEAN
M13_latchcollide  44/46   KILLED   SGIRE_W_TEX_RD 1<<11 -> 1<<8 (= SGIRE_W_UNMAP_RD)

# The panel PREDICTED this mutant at 44/44 against the PRE-REPAIR 44-row detector.
# That prediction is not re-measured here -- the 44-row form no longer exists.  What is
# measured is that the REPAIRED detector kills it.
L2VERIFY_DONE
```

`46 - 44 = exactly two red rows`, precisely the two the repair added, with **no existing row's
score perturbed**.

## 3. THE REPAIR ITSELF -- the two new rows, verbatim from the probe

```python
#  *** L2 -- A FLOOR BREACH FOUND BY THE PASS-2 PANEL, REPAIRED IN-ROUND. ***
#
#  Clause (d)'s DEPENDS-ON closure includes `d->warned', and `tex xbit' sweeps the six
#  *_LEN bits only.  The panel named the escape and predicted its score: give the TEX
#  read decline an ALREADY-USED NON-LEN bit --
#
#      SGIRE_W_TEX_RD = 1 << 11   ->   1 << 8   (= SGIRE_W_UNMAP_RD)
#
#  -- and the 44-row detector scores a CLEAN SWEEP, because its four TEX-read scenarios
#  and its unmapped-read scenario NEVER SHARE AN EMULATOR INSTANCE.  `tex xbit' sets bits
#  0-5, so bit 8 is clear in every session that reads TEX.  M10 established detection of a
#  WIDTH-bit collision, not of every existing-bit collision.
#
#  The repair is a SAME-INSTANCE sequence in BOTH orderings: whichever announce fires
#  first must not suppress the other.  One ordering alone would leave the mirror open --
#  the `#499' shape, where a repair closes the cell the mutant used and leaves its twin.
DECL_R = "unimplemented read from address 0x1800 -- declined.  (once) ]"

for nm, first, second in (("tex/unmap", TEX_BASE, OUTSIDE),
                          ("unmap/tex", OUTSIDE, TEX_BASE)):
    A = Addr(CODE)
    t, alive, how = session(load(A, first, OP_LD_V0_AT) + load(A, second, OP_LD_V0_AT))
    got = "%i/%i" % (t.count(TEX_RD_DECL), t.count(DECL_R)) if alive else "died"
    row(nm, got, "1/1",
        "LATCH INDEPENDENCE: both announces fire in ONE instance, either order")
```

The other three repairs are comment corrections; they change no executable line.  **Say if you want
them inlined too** -- I have kept them out to keep this pass scoped to the material that can fail.

## 4. QUESTIONS

**Q1. THE FLOOR QUESTION, asked of the SHIPPED COMPOSITE (not just this diff).**  Is there a
clause-(d) mutant that sweeps the **46-row** detector clean?  The DEPENDS-ON closure is the
predicates dominating the edited lines walked to the enclosing function, plus operand swaps from
fields the guarded body reads: `writeflag`, `len`, `relative_addr`, the five arrays, `d->warned`,
and -- **added this pass, after three seats found it missing** -- `odata`.

**Q2. IS THE REPAIR ITSELF DEFECTIVE IN THE WAY THE ORIGINAL WAS?**  This is the sharpest question
and the reason the repair-chain rule exists: `#499` reproduced its own breach inside its repair --
it closed the cell the mutant used and left the symmetric one.  I rowed BOTH orderings for exactly
that reason.  **Is there a third cell?**  Concretely: `d->warned` has bits 0-11 in use; `tex xbit`
sweeps 0-5; the new rows exercise bit 8 against bit 11.  **Bits 6, 7, 9, 10 are swept by nothing.**
Is that a breach, or is it coverage debt outside the floor?  Argue it -- and note that a rule which
demands a row per bit pair is the `#392` shape.

**Q3. ARE THE NEW ROWS THEMSELVES VACUOUS UNDER ANY MUTANT?**  Each asserts `1/1` -- both decline
literals present exactly once in one instance.  **Name the smallest edit that keeps a guard and
makes these two rows green while the latch behaviour is wrong.**

**Q4. DID THE COMMENT CORRECTIONS INTRODUCE NEW WRONG RECORDS?**  A correction carries more
authority than the error, so it earns a second reading, not less of one.  This project has three
recorded instances of a correction repeating the error it corrects -- and this round has already
produced one (my LINEAR wording was *worse* than the older comment it sat beside).

**Q5. IS THE CHAIN CLOSED?**  If you find zero floor breaches, say so **with your denominator**:
what did you enumerate?  If you find one, it is L2 and gets repaired in-round however late.
