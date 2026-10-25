# Reading task: F2D_PACKET_B (Gemini web; 2026-10-25)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-T19F2DB-a10b` on a line of its own.

# F2d -- THE CLASS-CLOSURE PASS (verify the enumeration), research item T19, ledger row `i8259eoiirr` (#574) -- GXemul hardened fork

Written 2026-10-25 by the main loop.  F2b and F2c each found unobserved cells of the fix's own predicates -- the same class
twice -- so by the repair-chain amendment this revision (v2g) is the CLASS CLOSURE: every predicate the product diff adds was
enumerated from the functions' own inputs with the partition its body induces, each cell got a row or a written disclosure,
every named shape was measured as a mutant against the previous instrument FIRST, and the whole table of record was re-run.
**This pass VERIFIES THE ENUMERATION rather than hunting cells**: is the partition complete, is every cell's row valid by
construction, is every disclosure honest.  The product diff (`dev_8259.c`, `dev_gt.c`, `devices.h`) is unchanged since pass 2
and is not re-litigated; the tree is `GXEMUL-SEC/src/` at HEAD `fa66b70d`; the fix lives only in the scratch clone.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

The stop condition is ZERO floor breaches WITH THE DENOMINATOR: the enumeration in section 2 IS the denominator.  A breach here
is a cell the enumeration MISSES (a predicate the diff adds whose body-tested partition has a cell with neither a row nor a
disclosure), or a rowed cell whose row cannot see its mutant.  A disclosed cell is clause (e), not a breach -- say so if you
disagree with a specific disclosure and why.  **VERDICT LINE FIRST.**

**Self-review disclosed.**  Every seat here named cells that this diff rows: be HARDER on the rows that answer your own
finding.  The adjudicating seat ruled RATIFY WITH CHANGES on F2c naming three holes; all three are rowed here -- check the
rows, not the holes.

**You cannot read files; every fact this pass depends on is inlined -- name any premise you cannot settle rather than guessing.**

**The roster for this pass:** GPT-6 Astra (ADJUDICATES -- its answer is the ruling of record, provisional until the roster
completes), Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: part A = the diff, the enumeration and the measurements,
Q1; part B = the F2c dispositions, Q2/Q3), Gemini 4 Argon (web route, QUEUED behind the single sender).  Fable 5.1 HELD;
kimi, minimax and the Opus seat deliberately not fired; agy quota-walled.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
BREACHES: <a cell the enumeration misses, or a rowed cell whose row cannot see its mutant -- with the mutant shape and the row; or "zero -- denominator: <the enumeration's cells you swept>">
~~~~

---

## 1. What v2g adds, in one paragraph

Three sessions and two rows close the cells F2c named.  `maskrem`: both UARTs pending, line 4 masked, the poll acknowledges 3 --
`maskrem ip2` reads CP0 Cause bit 10 right after it: FIX 0 (only a MASKED request remains, the recompute drops the line), HEAD 1,
`D_recompute_raw` 1; `maskrem irr after` 0x10 (FIX) / 0x18 (HEAD).  `ack ip2` and `pit ip2`: Cause bit 10 right after the poll
that acknowledges the ONLY pending line (the UART; the 8253's event): FIX 0 / HEAD 1; `D_recompute_true` and `D_recompute_none`
leave 1.  `isrother`: line 3 acknowledged, line 4 pending and NOT acknowledged, EOI 0x64 -- `isrother irr4` 0 in both columns
(the legacy branch consumes; `D_eoi_anyisr` leaves 1) and `isrother isr` FIX 0x08 / HEAD 0x00.  `gtmask`: the UART (4) and the
RTC (8) pending with the master's cascade line 2 MASKED, the GT read -- `gtmask iack` 4 in both columns and `gtmask isr8` 0
(`D_gt_nocasc2` returns 8 and sets slave ISR bit 0); `gtmask isr` FIX 0x10 / HEAD 0x00.  `D_scan_high` (the scan picks the
highest line) measures the priority order the two-line rows pin.  123 rows in 17 sessions, 32 symptom rows; the
contract carries the enumeration and the OUTSIDE list (`pic1 == NULL` / `pic2 == NULL` unobservable on a one-machine instrument;
`n2 < 0` unreachable while bus_isa re-folds bit 2; the retire guard's two conjuncts filed with the band-row construction; the
two-slave stall owed as `i8259cascline`).

## 2. THE ENUMERATION (from `killtable_20261025/PRETABLE.out`, the v2g block -- written before the table of record)

```
v2g BLOCK, 2026-10-25 13:42:29 (after the repair's own pass F2c -- six RATIFY-class answers, one NOT RATIFY refuted by argument -- and BEFORE the
v2g table of record).  F2c found cells of the SAME CLASS F2b found (unobserved cells of the fix's own predicates), so this
revision is the CLASS CLOSURE the repair-chain amendment requires: the enumeration below is what the closing pass verifies.

1. THE F2c CELLS, measured against the UNCHANGED v2f instrument first (run_extra2_19.sh -> table_v2f_extra/SCORES.txt):
   D_recompute_raw   the recompute's mask term dropped (`if (d->irr)`)                        ESCAPED 101/101
   D_recompute_true  the recompute replaced by an unconditional ASSERT                        KILLED 99/101
   D_recompute_none  the recompute deleted                                                    KILLED 99/101
   D_eoi_anyisr      `if (d->isr & bit)` -> `if (d->isr)`                                     ESCAPED 101/101
   D_gt_nocasc2      `if (n == 2 && p->pic2 != NULL)` -> `if (p->pic2 != NULL)`               ESCAPED 101/101
   D_scan_high       the scan picks the highest pending line                                  KILLED 94/101

2. THE ENUMERATION -- every predicate the product diff adds, the partition its own body induces, one row or one disclosure per cell:
   pic8259_acknowledge():
     `pending == 0` (pending = irr & ~ier)   empty -> -1: quiet iack, poll masked, poll once | non-empty: every acknowledge row
                                             mutant D_scan_raw (`irr` for `irr & ~ier`): masked irr4, poll masked, poll once
     the scan (lowest set bit first)         one line: every ack row | two lines on one PIC: poll first 0x83, gtboth iack 8
                                             mutant D_scan_high: measured above
     ISR set / IRR cleared                   M_noack_isr (poll isr, poll3 isr, isr both, casc isr2/isr8, gt isr ...), M_noack_irr
     the retire guard (pic1 && n == 0 &&     (pic1, line 0, count > 0): pit poll irr0 + rate storm (D_noretire) | (pic1, other
       ptr && *ptr > 0)                      line): D_retire_anyline DISCLOSED | (pic2, line 0): D_retire_anypic DISCLOSED --
                                             both observable only with a pending count >= 2, which only host time produces;
                                             filed pit8253retireguard with the band-row construction | ptr NULL: no 8253 on the
                                             machine (not malta) DISCLOSED | count == 0 with line 0 asserted: unreachable (the
                                             tick asserts only while count > 0) DISCLOSED
     the recompute `d->irr & ~d->ier`        unmasked request remains -> ASSERT: nonspec ip2 (D_deassert) | nothing remains ->
                                             DEASSERT: ack ip2, pit ip2 (D_recompute_true, D_recompute_none) | only a MASKED
                                             request remains -> DEASSERT: maskrem ip2 (D_recompute_raw)
   the poll read arm (case 0x0c):
     `i < 0 ? 0x00 : 0x80 | i`               nothing: quiet poll, poll masked | a line: every poll byte row
     the one-shot `current_command = 0x0a`   after a successful poll: poll once2 (D_latch_cond, M_sticky) | after an
                                             unsuccessful poll: poll once (M_sticky) | the revert TARGET (IRR, not the last
                                             RR/RIS selection): filed i8259ocw3revert DISCLOSED
   the specific-EOI arm `if (d->isr & bit)`  (in service, unmasked): eoi acked, eoi acked3 (B_eoi, D_eoi_n4, D_eoi_n3,
                                             D_eoi_ier) | (in service, masked): maskeoi isr (D_eoi_maskcond) | (not in service,
                                             nothing in service): eoi noack | (not in service, ANOTHER in service): isrother irr4
                                             + isrother isr (D_eoi_anyisr) | (masked, not in service): masked eoi
     the body `d->isr &= ~bit`               exactly its bit: spec eoi one (B_spec_isr0)
     the legacy branch's recalc              HEAD's unchanged lines -- not a cell of the diff
   the non-specific arm (lowest ISR bit)     nonspec lowest, nonspec twice (B_nonspec); highest-instead: by construction (0x10
                                             vs 0x08) -- not built, DISCLOSED as by-construction
   dev_gt.c GT_PCI0_INTR_ACK:
     `writeflag == MEM_READ`                 write: gt write isr (D_gt_write) | read: every gt row
     `pic1 != NULL`                          NULL (MVME5500): UNOBSERVABLE on a one-machine instrument DISCLOSED
     `n == 2 && pic2 != NULL`                cascade with slave work: gtcasc, gtboth (D_gt_nocasc, B_gt) | non-cascade with
                                             slave work pending: gtmask iack, gtmask isr8 (D_gt_nocasc2) | pic2 NULL:
                                             UNOBSERVABLE DISCLOSED
     `n2 >= 0`                               >= 0: gtcasc iack 8, gtboth iack 8 | < 0 (spurious cascade): unreachable while
                                             bus_isa re-folds bit 2 on every ISA event DISCLOSED (named in the contract)
     `n >= 0`                                >= 0: gt iack, gtboth iack (D_gt_noassign) | < 0: quiet iack (D_gt_always)
   OUTSIDE the enumeration, disclosed: D_fold (the two-SLAVE-request stall: a CPU-line observable with two pic2 sources; owed
   as i8259cascline; nonspec ip2 and the v2g Cause rows see only the master-side recompute).

```
**THIS FIRING ANSWERS QUESTIONS 2 AND 3 ONLY** (the F2c dispositions C1-C9; the denominator).  The enumeration is in section 2; the measurements are summarised in section 4 below; treat the rows as given.  Keep hidden reasoning short; VERDICT line first.


## 4. (measurements, summary)

* `witness_20261025f/` -- v2g on the UNMODIFIED HEAD clone, HEAD column: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=123/123 (before any v2g fix measurement).
* `pass2_20261025/fixlegs_132736/` -- v2g, BOTH legs: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=123/123 I8259EOI_CONTROL_fix=OK I8259EOI_RESULT_fix=123/123; rate: rate storm 0x1c84 head 5000..inf fix 1..1000 [HEAD] ok; rate storm 0x03 head 5000..inf fix 1..1000 [FIX] ok;
* `pass2_20261025/legs_133457/` -- L0 (the pre-fix build in GATE mode vs the FIX column): I8259EOI_CONTROL=OK I8259EOI_RESULT=91/123, exactly the 32 symptom rows red; L3 (`/bin/false`): I8259EOI_CONTROL=FAIL I8259EOI_RESULT=0/123, sentinel present.
* History: v2f = `witness_20261025e/` 101/101, `fixlegs_114055/` 101/101 both legs, `legs_114659/` L0 75/101 (26 symptom rows), L3 0/101; its table of record `SCORES_v2f.txt` / `table_v2f/`: 23 mutants, 20 killed, 3 escaped (the disclosed three).

**29 mutants, 26 KILLED, 3 ESCAPED (D_fold, D_retire_anypic, D_retire_anyline)** -- `killtable_20261025/SCORES.txt`, every mutant re-run from the frozen v2g copy.

## 5. THE F2c DISPOSITIONS (from `pass2_20261025/f2c_20261025/F2C_RULINGS.md`) -- adjudicate them

## Dispositions on the F2c answers
C1  DeepSeek A (NOT RATIFY: "three escaped mutants remain"): REJECTED by argument -- the three escapes are the DISCLOSED cells
    (`D_fold`: the two-slave stall, owed as `i8259cascline`; the two retire-guard conjuncts: filed `pit8253retireguard` with the
    band-row construction), named in PRETABLE.out before the table ran and in the contract; Astra, Grok, GLM A, GLM B and DeepSeek B
    all read them as disclosed.  "Zero breaches with the denominator" counts undisclosed escapes; a disclosed cell is clause (e).
C2  The recompute's partition (Grok BREACH; GLM B BREACH; Astra hole 2; GLM A's `pit ip2`): ACCEPTED as clause-(d) floor cells --
    the predicate the fix ADDS, with its body-tested partition {unmasked request remains -> ASSERT; nothing remains -> DEASSERT;
    only masked remains -> DEASSERT}; v2f rows only the first.  v2g rows all three: `maskrem ip2` (both UARTs pending, line 4
    masked, the poll acknowledges 3; Cause bit 10: FIX 0 / HEAD 1 -- symptom), `ack ip2` (the poll acknowledges the only pending
    line; FIX 0 / HEAD 1 -- symptom) and `pit ip2` (the poll retires the only 8253 event; FIX 0 / HEAD 1 -- symptom).  Mutants
    MEASURED first against v2f: `D_recompute_raw`, `D_recompute_true`, `D_recompute_none`.
C3  Astra hole 1 (`d->isr & bit` -> `d->isr != 0`): ACCEPTED as a clause-(d) cell (the added predicate weakened to a coarser test
    of the same lvalue).  v2g session `isrother`: line 3 acknowledged, line 4 pending and NOT acknowledged, EOI 0x64 -- the legacy
    branch must consume IRR bit 4 (`isrother irr4` 0 both; the mutant leaves 1) and ISR must keep bit 3 (`isrother isr` FIX 0x08 /
    HEAD 0x00).  Mutant `D_eoi_anyisr`, measured first.
C4  Astra hole 3 (GT `n == 2` dropped): ACCEPTED as a clause-(d) cell of the GT guard's partition {n == 2 with slave work; n != 2
    with slave work; n != 2 without}.  v2g session `gtmask`: UART 4 and RTC 8 pending, master line 2 MASKED (OCW1 0x04), the GT
    read: the master acknowledges 4, the slave is left alone -- `gtmask iack` 4 both, `gtmask isr8` 0 both (the mutant returns 8
    and sets slave ISR bit 0), `gtmask isr` FIX 0x10 / HEAD 0x00.  Mutant `D_gt_nocasc2`, measured first.
C5  GLM B disclosure gaps: `pic1 != NULL` false and `pic2 == NULL` are UNOBSERVABLE on a one-machine instrument (no session can
    remove a PIC) -- DISCLOSED in the contract's OUTSIDE list; `n2 >= 0` false (the spurious cascade) is unreachable while the fold
    invariant holds (PRETABLE G4) -- named explicitly in the contract and in the `i8259cascline` filing's note.  GLM B's open
    question (a bare command read after an OCW3 ISR selection): the fix's one-shot touches only the 0x0c poll; the 0x0a/0x0b
    selections are HEAD's unchanged lines -- not a cell of the fix's predicates; recorded, not rowed.
C6  The scan direction (main loop, from the enumeration): the two-line rows pin lowest-first by construction (`poll first` 0x83,
    `gtboth iack` 8); mutant `D_scan_high` added so the pin is MEASURED, not inferred.
C7  Records (GLM A, GLM B, Astra A12/A7): the F2c packet's "two sessions and six rows" undercounted -- v2f added THIRTEEN explicit
    rows (seven answering cells, six companions) plus four liveness rows (two sessions x ram/stable) = 17, 84 -> 101; the packet's
    diff caption said v2d -> v2e for a v2d -> v2f diff; the 20/3 table is of v2f (its SCORES header names the fixlegs_114055 copy);
    the rate artifact lives at `pass1_20261025/rate_explore_20261025/` (the drafts cited it without the pass-1 prefix: corrected);
    the A7 gloss "a run of about a second" is UNMEASURED -- the rate session's wall time is not recorded; the FIX count 3 is a band
    guard, the cadence is filed with `pit8253retireguard`.  All L4, corrected in the drafts and here.
C8  Astra A1 (the Linux ICW2 extract is relayed, not version-pinned): ACCEPTED as the honest state -- the warrant is Grok's
    re-fetch, recorded as such; a version-pinned extract is owed to `i8259isrnever`'s neighbourhood, not to this landing.
C9  Astra on `D_eoi_n3`/`D_eoi_n4` also red on `spec eoi one`/`spec eoi both` (coherent over-catch) and on `spec isr both` being the
    precondition witness, not a second kill: ACCEPTED as wording for the contract.


## 6. The three questions

1. THE ENUMERATION AND THE NEW ROWS.  Is the partition in section 2 the one the fix's bodies induce -- for each predicate the
   diff adds (`pending == 0`, the scan, the retire guard, the recompute, the poll's one-shot, `d->isr & bit` and its body, the
   non-specific arm, the five GT guards) name any cell it misses.  For each new row (`ack ip2`, `pit ip2`, `maskrem ip2`,
   `maskrem irr after`, `isrother irr4`, `isrother isr`, `gtmask iack`, `gtmask isr8`, `gtmask isr`): is it valid by
   construction -- does the named mutant change the named observable, and can the row read green on a build where the cell is
   wrong?  Do the inserted `mfc0` reads in `ack` and `pit` change any old row (the packet says no: `mfc0` touches no device)?
2. WHICH OF MY NINE F2c DISPOSITIONS (C1-C9) IS WRONG?  I rejected one answer's verdict (C1), accepted every named cell as a floor
   cell (C2-C4), disclosed two unobservable cells and one unreachable one (C5), and corrected the records (C7).  Name the count
   you overturn.
3. ZERO BREACHES, WITH THE DENOMINATOR.  The table of record swept 123 rows against 29 mutants; escapes beyond the three
   disclosed: none.  Is there a cell of the enumeration with neither a row nor an honest disclosure?  Is any
   disclosure wrong (a disclosed cell that IS constructible deterministically on this machine)?  Name it, or state the
   denominator you swept and found closed.

## 7. Answer format

~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
BREACHES: <...>
~~~~
Then Q1, Q2, Q3 in order; mark claims READ / DERIVED / NOT CHECKABLE, with the single file or fact that would settle anything
you cannot.  Keep hidden reasoning short; put the answer in the response.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`T19F2DB: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
