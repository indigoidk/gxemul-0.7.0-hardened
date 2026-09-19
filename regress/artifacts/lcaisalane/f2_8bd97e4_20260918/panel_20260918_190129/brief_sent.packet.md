# `#530` §F2 ADJUDICATION PASS -- every seat's pass-2 findings on 8bd97e4's width row, shared

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

This is the ADJUDICATION pass: you now see what all nine seats said on pass 2, and my disposition on each.
**A disagreement I resolve by writing it up is the failure this pass exists to prevent** -- so where you
were a party to a dispute, adjudicate it yourself, and where my ruling ADOPTS your position, scrutinise it
harder, not softer.  Check the premises, not just the derivations; a seat that re-derives a premise from
something this packet did NOT give it is worth more than one that agrees.

**THE TREE IS `GXEMUL-SEC/src/` AT COMMIT `3c41f01`** (a records commit on top of `8bd97e4`, which shipped
the fix and the row; no product or detector code changed since `8bd97e4`).  Pristine-2021 copies elsewhere
under the project root are NOT this fork.  **If you cannot read files that is expected** -- every fact you
need is inlined; name any premise you cannot settle from this packet.

**Seats that read files: read ONLY these files, nothing else in the tree:** `GXEMUL-SEC/src/devices/dev_lca.c`,
`GXEMUL-SEC/src/core/memory.c`, `GXEMUL-SEC/src/cpus/memory_rw.c`, `GXEMUL-SEC/src/cpus/cpu_alpha_palcode.c`,
`GXEMUL-SEC/regress/lca_widewrite_probe.py`, `GXEMUL-SEC/regress/lca_isalane_probe.py`.  Do not browse the rest
of `regress/`, `regress/artifacts/` or `tools/` -- the measurement you need is inlined in section 3.

**VERDICT LINE FIRST.**

    VERDICT: <for D1: L2-CLASS-CLOSURE | E-DEBT-PLUS-L4 | OTHER> -- <one line with the deciding reason>

## 1. THE SUBJECT, IN FIVE LINES

`DEVICE_ACCESS(lca_isa)` in `src/devices/dev_lca.c` (Alpha `alphabook1`, the 21066 sparse ISA window):
`relative_addr >>= 5` gives the ISA port P (the five discarded bits are k); `if (len == 0) return 0;`;
`ofs = (P & 3) % len`; on a WRITE it forwards `data[ofs]` as ONE byte to port P; on a READ it fetches one byte
and fills `data[0..len)` with that byte at `ofs` and zeros elsewhere.  For every `len >= 4`, `ofs == P & 3`.
The 352-row parent probe drives instruction widths 1/2/4/8 (lanes 0-3, both directions).  The new width row
`regress/lca_widewrite_probe.py` drives ONE PROM GETENV write of 16 bytes (`store_buf`) into the ns16550 scratch
register at port 0x2ff: cell (C=16, k=0, lane 3), and it catches the two variants pass 6 found (`&& len <= 8`
on the write arm; `len == 0 || len > 8` as the guard) -- base 3/3, each variant 2/3.

`store_buf` issues chunks of 1024/256/64/16/4/1 bytes, each only at an address aligned to its size and never
crossing 1 KB, so the wide cells a guest can reach are: C=16 (k in {0,16}, lanes 0-3), C=64 (k=0, lanes 0,2),
C=256 (k=0, lane 0), C=1024 (k=0, lane 0) -- twelve, or EIGHT width/lane cells once the discarded k is collapsed.

## 2. THE RULES IN DISPUTE, inlined

* **Floor clause (d)**: a detector must distinguish the fix from a variant that keeps the guard but nulls its
  effect -- a predicate qualified (`if (X)` -> `if (X && Y)`), a bound relaxed.  Bounded by DEPENDS-ON: the
  predicates dominating the edited lines, and operand swaps from lvalues the guarded body reads.
* **Joint cells (2026-09-04)**: *"DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read
  lvalues EXACTLY WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM ... A value or combination the body never
  tests as a case is DISCLOSED under clause (e)."*
* **Clause (e)**: the probe header names what it is designed to catch; a variant outside the stated contract is
  disclosed debt.  **A breach OF the contract (an in-contract variant undetected) is itself L2.**
* **Pass 6's ruling (flagship, 2026-09-17), verbatim:** *"`&byte, len` diverges WITHIN the probed width set
  (catchable, so a contract line suffices); codex's `len<=8` diverges only OUTSIDE it (uncatchable, so it cannot
  be discharged that way)."* ... *"The probe is instruction-driven and the widest Alpha store, STQ, is 8 bytes --
  no instruction-driven row can ever express len > 8."*
* **Class closure**: two consecutive passes finding breaches of ONE class owe the class closure in ONE diff.
* **Stopping rule**: in-round fixes are for MEASURED FALSE PASSES (floor) and WRONG RECORDS; everything else is
  FILED as coverage debt.

## 3. THE MEASUREMENT (the Opus seat, 102 legs on unmodified alphabook1, every value predicted before it ran)

Variants, each ONE edit to the committed function:
`va` write arm `&& len <= 16` | `vb` guard `|| len > 16` | `vc` write arm `&& (len <= 8 || (P & 3) == 3)` |
`vd` `% (len > 8 ? 8 : len)` | `ve` guard `|| (len > 8 && P < 0x200)` | `vf` `data[len > 8 ? 0 : ofs]` |
`vg` before the shift: `if (len > 8 && (relative_addr & 0x10)) return 0;` | `vh` read loop `i < len && i < 8` |
`vt1` "aligned only": `len > 8 && (relative_addr & 0x1f)` refused | `vt2` refuse a wide chunk that continues the
previous access | `vw64`, `vw256`: write arm `&& len <= 64` / `<= 256`.

Cells (the same GETENV instrument, one session each): `frozen` = the shipped row (16, k0, lane 3, SCR 0x2ff);
`k16` SCR at k=16; `l0w16`/`l0w64` MCR 0x2fc lane 0 at C=16/64; `l2w64` MSR 0x2fe lane 2 at C=64; `low16` 8259 IMR
0x21 lane 1; `mc2` one 32-byte GETENV = two 16-byte chunks (0x2fe k16 lane 2, then 0x2ff k0 lane 3);
`kbc16/256/1024` the 8042 command byte via port 0x60 at C=16/256/1024.  Score = rows green / rows; `-` = not run.

    cell     base  va    vb    vc    vd    ve    vf    vg    vh    vt1   vt2   vw64  vw256
    frozen   3/3   3/3   3/3   3/3   3/3   3/3   2/3   3/3   3/3   3/3   3/3   3/3   3/3
    k16      3/3   3/3   3/3   3/3   3/3   3/3   2/3   2/3   3/3   2/3   3/3   3/3   3/3
    l0w16    3/3   3/3   -     2/3   -     3/3   -     3/3   -     3/3   3/3   -     -
    l0w64    3/3   2/3   2/3   2/3   3/3   3/3   3/3   3/3   3/3   3/3   3/3   3/3   3/3
    l2w64    3/3   2/3   -     2/3   -     3/3   -     3/3   -     3/3   3/3   3/3   3/3
    low16    3/3   3/3   -     2/3   -     2/3   -     3/3   -     3/3   3/3   -     -
    mc2      5/5   5/5   5/5   4/5   5/5   5/5   3/5   4/5   5/5   4/5   4/5   -     -
    kbc16    3/3   3/3   -     2/3   -     2/3   -     3/3   -     3/3   3/3   -     -
    kbc256   3/3   2/3   -     2/3   -     2/3   -     3/3   -     3/3   3/3   2/3   3/3
    kbc1024  3/3   2/3   2/3   2/3   3/3   2/3   3/3   3/3   3/3   3/3   3/3   2/3   2/3

**Read it this way:** the shipped row (`frozen`) detects only `vf`; `vd`, `vh` are equivalent everywhere; every
other variant is detected at some OTHER reachable cell by the same instrument.  The pair {mc2, kbc1024} detects
all nine escapes plus `vf`.  The parent's 352 rows score every variant 352/352 by construction (each added
predicate is gated on `len > 8`; the parent never drives a GETENV).

## 4. FINDINGS, with my disposition on each

F1  [all nine] every Q1 prediction held; now MEASURED (section 3).  ACCEPTED.
F2  [codex, all] the twelve-cell count is exact for store_buf; eight width/lane cells once k collapses (codex walked
    all 174,080 start-address/width pairs).  ACCEPTED.
F3  [all nine] L4: the parent header's *"The width cell is therefore COVERED, not merely disclosed"* -- one cell of
    twelve is rowed.  ACCEPTED -> corrected in place.
F4  [all nine] L4: the contract's clause (iii), *"the others share the same `len > 8' predicate"* -- refuted by va,
    vb and the ladder.  ACCEPTED -> corrected in place.
F5  [grok, glm, deepseek, minimax, codex, opus5] the contract's *"DESIGNED TO CATCH: any guard that declines a
    len > 8 WRITE ... in either the guard form or the write-arm-conjunct form"* is falsified by va, vb, vc, ve, vg,
    vt1, vt2 -- each such a guard, each undetected.  ACCEPTED as a contract breach -> the contract is narrowed to
    what the rows measure, and every measured escape is named with the cell that detects it.
F6  [five seats; glm dissents] `wide alive` is survive-only: a reinstated process-ending call at len > 8 leaves t4
    unprinted, so `wide getenv` reds with it.  ACCEPTED (mechanical); glm's dissent REJECTED.
F7  [codex, grok, agy; opus5 and kimi disagree] `wide live` is not a DEVICE signature -- the scratch register is a
    plain stored byte.  REFINED: it is a valid round-trip control (no RAM is mapped in this window), and the label
    should say "round-trip control"; `wide getenv`'s 0x44 is the RAM discriminator.  L4-minor, corrected in place.
F8  [grok; agy was wrong] the earlier Opus GETENV replica (port 0x3ff, a3=64) issued 16-byte chunks, not 64
    (0x7fe0 is not 64-aligned).  ACCEPTED.
F9  [agy, grok, opus5 by census; packet seats could not settle] GETENV/store_buf is the only len > 8 producer into
    this window on alphabook1: no PHYSICAL producer (pccmos only, 1 byte), no bus master, no wide read.  ACCEPTED.
F10 [opus5] CONSTRUCTION GAP: nothing asserts the GETENV length exceeds 8 -- `load_const(A3, 16)` edited to 4 makes
    a len-4 row that base and both pass-6 variants pass silently.  ACCEPTED -> owed with the row's next edit (a
    two-chunk cell such as `mc2` pins the width by construction).
F11 [codex] a single session sweeping several cells is unsound: a variant that falls into the read arm writes
    zeros into store_buf's SOURCE (the emulator's boot string), so later GETENVs see a shorter string.  REFINED:
    sound only with an ORDER in which any clobbering variant is already detected (opus5: {mc2 then kbc1024}).
F12 [codex] the probe exits 0 on FAIL (a runner must parse WIDEWRITE_RESULT); contract (i) conflates byte
    SELECTION with DELIVERY of the other bytes.  ACCEPTED as records.
F13 [kimi] a GETENV to a misaligned a2 is issued as sixteen 1-byte writes, all forwarded -> lcawidefold's "15 of 16
    dropped" is alignment-dependent.  ACCEPTED, recorded on that row.
F14 [grok] the nested forward has no PHYSICAL flag and works only because ptbr==0 identity-maps it -- the open row
    lcaisaphys.  ACCEPTED, recorded on that row.
F15 [glm] option: a direct-call unit harness covering every cell; [kimi] a static lint tripwire; [opus5] fold the
    closure into lcawidefold's eventual fix.  FILED as options, not adopted here.

## 5. DISAGREEMENTS -- please adjudicate your OWN side

**D1 -- are va/vb/vc/ve/vg/vt1/vt2 floor breaches (L2, class closure owed now) or clause-(e) debt?**
* L2 -- **codex**: *"I treat pass 6 as a specific exception establishing coverage obligations for the reachable
  width class, rather than an exception for the literal constant 8. Under that interpretation, moving the cutoff to
  16 cannot discharge the obligation."*  **glm**: pass 6 governs, bounded to dimensions "whose producible values
  are all witnessable"; the letter read literally "would empty clause (d) of its own named example".  **kimi**:
  "distinguishes" means OBSERVABLE behaviour varies -- lane selects the forwarded byte, port the destination -- so
  vc/ve are L2 on either rule.  **deepseek, minimax**: all five are inside the contract's own "any", reachable, and
  undetected.
* DEBT -- **opus5** (measured): *"pass 6's 'uncatchable' is a condition on clause (e): a contract line can only
  discharge a variant that some shipped instrument can reach ... It is now met, measured: every escape is killed
  by the GETENV instrument at another cell."*  **agy**: the constants 16/64/0x200/0x10 introduce partitions the
  body never induces; pass 6 read literally "would create an infinite regress".  **grok**: the letter governs ROW
  demand; one reachable len > 8 WRITE row discharged pass 6's cell; "(c) is the closest call for a real L2 row."

**MY RULING (provisional -- fable5 rules LAST): E-DEBT-PLUS-L4, and I adopt the measuring seat's reading.**
Warrant: pass 6's own reason is about CAPABILITY -- *"no instruction-driven row can ever express len > 8"*.  The
body tests `len` only against 0 and `% len` separates {1},{2},{3},{>=4}, so every width >= 4 is one body class,
already driven at lanes 0-3 by the parent at len 4 and 8.  The shipped GETENV instrument now reaches every wide
cell (section 3), so each escape is dischargeable by a contract line naming the cell that detects it.  That
reading is bounded; codex's is too (by the producer's eight cells), and **I am least sure of this ruling on vc**,
where lane is a partition the body does distinguish.  **Consequences:** correct F3/F4/F5/F7/F12 in place; FILE the
two-cell strengthening {mc2, kbc1024} (measured to detect every escape, and it also closes F10) as coverage debt
for its own round -- or, if you rule L2, it is the class closure's minimal form and I want your cell set.

**D2** `wide alive` alone-red: glm (yes, on the crash class) vs five seats (no).  Ruled: no (F6).
**D3** `wide live` a device signature: opus5/kimi/minimax (yes, in context) vs codex/grok/agy (no).  Ruled: F7.

## 6. OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* I wrote the row, its contract, the parent's COVERED sentence and this ruling.  A ruling that lets my own row
  stand with corrections instead of new rows is the ruling I am least likely to test -- test it.
* The strengthening is FILED, not shipped, under my ruling; if that is a floor breach being filed, say so.
* D1's crux may be vc alone: lane x (width > 8).  If vc is L2 and the rest are debt, the closure is the four C=16
  lanes (plus the F10 pin), not all eight cells.

## 7. QUESTIONS

1. Adjudicate F1..F15 and D1..D3 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or refined fourteen of fifteen findings and ruled
   against five seats on D1.  That is a suspicious shape; agreement is not evidence.
3. **WHAT DID ALL NINE OF US MISS?**  You now have the whole panel's output.

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
