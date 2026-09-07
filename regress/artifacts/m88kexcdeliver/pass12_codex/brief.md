# PASS 12 -- `m88kexcdeliver` (#502): the CLOSING pass on the v19 L2 repair.  2026-09-06.  ONE diff, ONE table, ONE question.

## WHAT THIS IS
An ordinary correctness review of a CPU model in a hardware simulator for obsolete workstations (GXemul 0.7.0, a
maintained fork): the MC88100 exception-delivery path and its regression detector.  Plain engineering vocabulary;
no security framing is intended or wanted, and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`; the detector is `GXEMUL-SEC/regress/m88k_exc_probe.py`.  Ignore any
other `src/` you find** -- three pristine-2021 upstream copies sit under the project root and are NOT this fork.

**If you cannot read files that is expected -- every fact is inlined.  Name any premise you cannot settle from
this packet rather than guessing; an honest "not checkable from the packet" outranks a confident guess.**
**VERDICT LINE FIRST.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
This chain has now had FIVE consecutive passes find that a repair reproduced, inside itself, the class of defect
it was repairing.  **Pass 11 found it in a filing written from the census built to END that pattern.**  Assume
this repair does it too until you have tested that.

## THE STOP CONDITION THIS PASS IS BEING JUDGED AGAINST
The repair-chain rule closes on the FIRST pass that finds **zero floor breaches** -- but a bare zero does not
close it.  A closing pass must be VALID: the diff delivered (it is, below), the roster's misses named (they are,
at the end), and **the zero carried WITH ITS DENOMINATOR -- which cells, which mutant shapes, were swept.**
So: if you find nothing, say what you looked at.

## SETTLED PREMISES (re-inlined; each was established in an earlier pass of this campaign)
1. Six software-settable MC88100 PSR bits: MODE `0x80000000`, SER `0x20000000`, C `0x10000000`, SFD1 `0x08`,
   IND `0x02`, SFRZ `0x01`.  BO and MXM cannot be set through `m88k_stcr` without stopping the CPU.
2. `m88k_exception()` has: a dispatch `switch` setting `implemented`; a FALLBACK
   `if (vector < USER_TRAPS_START && !implemented)` that stops every CPU; then the SFRZ re-route
   `if (PSR & SFRZ) { if (!is_trap) { vector = ERROR; fatal(...); } update_shadow_regs = false; }`; then a common
   path; then a tail switch.
3. A cell (site, bit) is CLOSED iff two rows reach that site with DIFFERENT values of that bit -- polarity-free,
   because a mutant may condition in either direction.
4. The dispatch-arm space is 7 arms x 6 bits = 42, less 2 MODE-unreachable at BOUNDS/ERROR = **40**, and the
   shipped instrument closes **40 of 40** (`derive_cells.py`, output `CELLCENSUS.out`).
5. `PSR_FRZUSER = 0x00000003` clears **MODE and SFD1** -- both.  This was NOT known when pass 11's predictions
   were written and it is why one of them missed.

## THE REPAIR UNDER REVIEW (v19: 57 -> 59 fault rows.  No product code.)
Pass 11 ruled that `{SFRZ set, is_trap} x {MODE, SFD1}` -- the re-route's TRAP side -- is a FLOOR breach, not
clause-(e) debt, because `PRETABLE12` had already graded the SAME inner `if` as L2 for IND and C, and because the
pass-5/7 mutants `!is_trap || vector == <class>` condition on a field the body does not test either and were
repaired in-round.  Two rows added, both in `trapfrozenind`'s shape:

```python
("trapfrozenuser", [DIVU_R2_R3_R0], {"r3": 0x11, "r5": PSR_FRZUSER}, V_USER0,  0x10004, PSR_RESET,
             [STCR_R5_CR1, TB1_0_R3_128]),   # frozen handler drops to USER mode, then a user trap at 128
("trapfrozensfd1", [DIVU_R2_R3_R0], {"r3": 0x11, "r5": PSR_FRZSUP},  V_BOUNDS, 0x10004, PSR_RESET,
             [STCR_R5_CR1, TB1_0_R3_7]),     # frozen, SFD1 CLEAR, same trap as trapfrozenind
```

`r3 = 0x11` because bit 0 must be SET or the `tb1` does not trap and the row is silently inert.  Vector 128 is
`>= USER_TRAPS_START` so the fallback does not claim it, and `X(tb1)` checks privilege only for `vector < 128`.

## TABLE 15, MEASURED (pre-table block written 20:45:25, first build 20:46)
Every score re-derived by DIFFING each result against `BASE.out`, not from the driver's echo -- table 13's driver
read a stale file and table 14's echo attributed rows to the wrong mutant.

| mutant | on v19 (shipped) | on frozen v17 (pre-repair) | rows red on v19 |
|---|---|---|---|
| `!is_trap \|\| !(PSR & MODE)` | 58/59 | **57/57 -- CLEAN SWEEP** | `trapfrozenuser` |
| `!is_trap \|\| !(PSR & SFD1)` | 57/59 | **57/57 -- CLEAN SWEEP** | `trapfrozenuser`, `trapfrozensfd1` |
| `!is_trap \|\| (PSR & MODE)` (CONTROL) | 44/59 | -- | 15 rows: every MODE-set trap row |

BASE 59/59 opening and closing; scratch clone, clean against SEC, no sentinel left.

## THE ONE DISCLOSED DEFECT IN MY OWN PREDICTIONS, so you need not find it
I predicted the SFD1 mutant would red `trapfrozensfd1` ALONE (58/59).  It reddened `trapfrozenuser` too, because
of premise 5.  So **`trapfrozenuser` is a JOINT row varying two bits**, not the single-axis MODE row I described.
The control proves MODE is still uniquely closed by it (15 MODE-set rows red, `trapfrozenuser` spared).

**AND THE HONEST COST: `trapfrozensfd1` has ZERO measured delta against its own mutant** -- delete it and the SFD1
mutant is still caught at 58/58.  Its stated warrant is single-axis attribution, since a row varying two bits
cannot say which one fired.

## THE QUESTIONS
1. **Is that warrant good enough under the ADDITION LICENCE?**  The licence says additions are justified by a
   MEASURED DELTA or a TRANSFERRED WARRANT, never by "it cannot hurt".  `trapfrozensfd1`'s delta is zero.  I claim
   attribution is a transferred warrant (the anchor rule's principle one level down).  **Is that right, or is this
   row exactly the "cannot hurt" addition the licence exists to refuse?**
2. **Does the repair reproduce the defect it repairs?**  The trap side now varies MODE, SFD1, IND, C and SER;
   SFRZ is invariant by construction.  **Is there a site or a bit this repair closes at one cell while the
   contract claims the axis?**  That is what passes 9 and 11 each found.
3. **Is `trapfrozenuser` load-bearing for anything ELSE that would silently break?**  It is now the sole carrier
   of the MODE cell AND a second carrier of SFD1.  A future edit to `PSR_FRZUSER` moves both.

## THE SECOND QUESTION, with the count named
Of this repair's dispositions -- (i) FLOOR not debt; (ii) two rows rather than one; (iii) keeping the
zero-delta row; (iv) the joint row left joint rather than re-cut single-axis; (v) v20 recorded as comment-only;
(vi) the contract sentence claiming the trap side is closed on all five varying bits -- **WHICH IS WRONG?**

VERDICT LINE FIRST (`CLOSE THE CHAIN` / `ONE MORE REPAIR: <which>` / `DO NOT SHIP`), then your answer with its
DENOMINATOR -- which cells and which mutant shapes you swept -- then anything else.  Under a page.

*Roster note for the closing-pass validity condition: agy is DELIBERATELY NOT FIRED (measurement reservation);
opus5 and fable5 are HELD for the 9th; glm has burned its budget on hidden reasoning twice on this row.*
