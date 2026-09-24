# #545 closing pass -- does the class closure (repair 2) hold, and which of my dispositions of the first repair's pass-2 findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  This repair touches `regress/diff_footbridge.c` and
`regress/gate_offline.sh` only; `src/devices/dev_footbridge.c` is unchanged by it.  File-reading seats:
read the FROZEN copies in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2c\frozen\` (md5 prefixes:
dev_footbridge.c 783c0c7f, diff_footbridge.c 4d7bdcc3 = the 707-row instrument under review,
diff_footbridge.491.c ff8f87b6 = the previous 491-row one, gate_offline.sh 45d2b495), not the working files.
There are THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`); they are NOT this fork.  If your line numbers disagree with mine by
hundreds you are reading one of them -- say so.

**If you cannot read files that is expected** -- every fact you need is inlined below (the handler, the
diff, the measurements).  Name any premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a count, a set, a membership -- ENUMERATE it rather than
reasoning about it**, and enumerate the right domain: ask what the PRODUCER of a value can emit.

**VERDICT LINE FIRST**, so your answer survives truncation: `VERDICT: SHIP` or
`VERDICT: DO NOT SHIP -- <reason>`.

**THIS IS A CLOSING PASS, SO A ZERO NEEDS A DENOMINATOR.**  If you find no breach, say WHICH cells and
WHICH edit shapes you swept.  "Nothing found" and "nothing looked for" must not read the same.

## What #545 is (plain engineering language)

#545 changed five register arms of the DC21285 "footbridge" device model.  Before it, a guest WRITE to any of
four read-only status registers (IRQ_STATUS +0x180, IRQ_RAW_STATUS +0x184, FIQ_STATUS +0x280, FIQ_RAW_STATUS
+0x284) or a guest READ of the write-only IRQEnableClear (+0x18c) ended the emulator process.  After it, each
such access is DECLINED -- no register changes, a declined read returns 0 -- and ANNOUNCED ONCE per site
through a per-site warn-once latch (`warned_*`).  The detector is `regress/diff_footbridge.c` (an offline
differential that `#include`s the real `dev_footbridge.c` and calls its access function directly) plus
`regress/footbridge_sites_probe.py` (a 37-row guest probe, unchanged by this repair).

## The chain so far (every step measured; artifacts under `regress/artifacts/fbd5/`)

1. pass 1, pass 2, the §F2 findings-sharing pass, and the flagship seat's regress/adjudication pass.
2. The flagship seat PREDICTED, by reading, that five one-condition edits to the DIRECTION test (Q1..Q5, e.g.
   `if (writeflag == MEM_READ && d->irq_enable)` at IRQ_STATUS) would pass every row.  Measured TRUE:
   333/333 offline and 37/37 guest for each (`q2_20260923/Q2.log`).  -> REPAIR 1 (X9 = legal x latches clear,
   plus a "wide" seed state), 491 rows.
3. Repair 1's own pass 2 (panel `panel_20260923_143458` + the Opus measuring seat + a dedicated codex job):
   codex, grok, glm and the kimi substitute DO NOT SHIP; agy, deepseek and minimax SHIP.  The Opus seat built
   434 one-line variants of the five arms and the head predicates: **153 passed all 491 rows**.
4. That was the THIRD consecutive pass to find cells of ONE space, so the carrier's class-closure amendment
   governed: REPAIR 2 enumerates the whole space from the handler's own inputs, closes it in ONE diff
   (X10, X11, X12 and a fourth "ones" state), and rewrites the CONTRACT to name what is covered and what is
   not.  **THIS PASS VERIFIES THAT ENUMERATION -- it is not asked to hunt new cells one at a time.**

## Measured after repair 2 (all offline, frozen instruments, scratch trees restored and `cmp`-verified)

* **FIX: 707 rows, 0 failures** (`q2_20260923/repair2/Q2R2.log`, instrument md5 4d7bdcc3).
* **The Opus seat's 434 variants re-scored on the 707 rows** (`repair2/OPUS_RESCORE.txt`): **57 green, exactly
  the 57 predicted in `PRETABLE_Q2b.out`** (written 15:10, before the 15:13 table; corrections, if any, go to a
  separate `.corrections` file -- the mtime shows the order, it cannot prove the file was never touched):

      family     built  green@491  green@707        family     built  green@491  green@707
      a_neg        20       0         0            dom          4       4         2
      a_pos        20       0         0            e_ctl        3       0         0
      b_neg        25      10         0            e_dir       20      20        20
      b_pos        25       0         0            e_flag      20      20        20
      bit_dir_b1   20      20         0            fl_neg      20      10         0
      bit_dir_b3   20      10         0            fl_pos      20       0         0
      bit_flag_b1  20      20         0            idata        2       2         1
      c_dir        15       3         0            lane        10      10         0
      c_flag       10       0         0            or_F        40       0         0
      case          5       5         5            or_L        25      14         4
      d_neg        20       0         0            swap_body   20       0         0
      d_pos        20       0         0            swap_flag   20       0         0
      dir_eq       10       5         5            TOTAL      434     153        57

  The 57 still green, by family: e_dir 20 + e_flag 20 (`dir && d->F != 0x10`, `flag && d->F != 0x10` -- a
  condition on one EXACT field value), case 5 (`case 0x1a0: case IRQ_STATUS:` and its four mirrors -- a new
  offset aliased onto an arm), dom 2 (the timer fold widened to start at IRQ_STATUS / 0x100), dir_eq 5
  (`writeflag != MEM_WRITE` -- writeflag has two values), or_L 4 (`dir || d->own_latch` at the four STATUS
  arms: a latched bad write then runs the read branch, whose only effect is `odata`, which the tail returns only
  for a read -- the fifth, at +0x18c, is RED, because there the write branch drives the interrupt output), idata 1
  (`writeflag == MEM_WRITE && idata != 0x20` at +0x18c -- one exact data value).
* **Carried kills** (`repair2/CARRIED_KILLS_491_to_707.txt`): FIX + the 49 earlier table-4 mutants + the nine
  newer cases {Q1..Q5, W1, W2, T1, T2} = 59 entries; every row red on the 491-row instrument is red on the 707
  one (no row was renamed between them): **lost = 0**.  M1 and M1b..M1e are the verbatim `exit(1)`
  reinstatements and are recorded as PROCESS DEATH (no row summary), on both instruments.
* **The dedicated codex job's ten variants V1..V10** (its own reading was of the 491 rows; it answered after
  repair 2 had been built), measured on BOTH instruments (`q2_20260923/codexV_20260923/CV.log`, predictions
  written first):

      variant (one line changed)                                                     491 rows   707 rows
      V1  IRQ_STATUS        if (writeflag == MEM_READ && !d->warned_irq_raw_w)           1 red     10 red
      V2  IRQ_RAW_STATUS    if (writeflag == MEM_READ && len == 4)                       9 red     17 red
      V3  IRQ_STATUS        if (writeflag == MEM_READ && d->irq_enable != 0x10)          GREEN     GREEN
      V4  FIQ_ENABLE_CLEAR  if (writeflag == MEM_WRITE && d->fiq_enable)                 GREEN     GREEN
      V5  IRQ_ENABLE_SET    if (writeflag == MEM_WRITE && d->irq_status) {               2 red      2 red
      V6  IRQ_STATUS        else if (!d->warned_irq_status_w && d->irq_enable) {        30 red     42 red
      V7  IRQ_ENABLE_CLEAR  } else if (!d->warned_irq_clear_r && len == 4) {             8 red     10 red
      V8  IRQ_STATUS        odata = d->irq_status & d->irq_enable & 0xffff;              2 red      5 red
      V9  IRQ_ENABLE_CLEAR  d->irq_enable &= ~(idata & 0xff);                            GREEN      3 red
      V10 IRQ_ENABLE_CLEAR  if (d->irq_status & idata)  [in place of & d->irq_enable]    3 red     12 red

  codex's static reading matched the 491 column exactly (10 of 10).  V9's three reds on 707 are
  `X12 IRQ Clear write all-ones len 2 (ones, ...)`, `... len 4 (ones, ...)`, `... len 4 (wide, ...)`.
  V3 is the exact-value class; V4 is equivalent (with fiq_enable 0, skipping `fiq_enable &= ~idata` changes
  nothing, and the arm has no else).

## §C — SETTLED PREMISES (recorded resolutions; do not re-derive, but say if the diff or the handler contradicts one)

1. **The product change is settled** -- decline + once-latched announce at the five sites, 0 for the declined
   read.  Pass 1, pass 2, §F2 and the adjudication all ruled on it; neither repair touches it.
2. **The floor these rows answer to** (the carrier's DEPENDS-ON rule, bounded): the predicates DOMINATING each
   edited decline, walked to the function boundary, crossed with the body-read lvalues' BODY-TESTED partitions
   where they are jointly reachable; a value or combination the bodies never test as a case is DISCLOSED
   (clause e), not rowed.
3. **Insertion-class edits in OTHER cases** (a writer added at +0x188, the FIQ enable pair, TIMER_1_VALUE) are
   outside that closure (adjudication Q1).  Their existing rows stay, ungraded as floor.
4. **No guest reset-state reads are added**: every seat that answered repair 1's Q5 agreed the offline rows carry
   the floor; codex added that guest reads would buy integration coverage, not floor coverage.
5. **`fiq_status` has NO writer in the product** (grok, Opus): every FIQ status value these rows seed is synthetic.
   `irq_status` is written ONLY by `footbridge_interrupt_assert` / `_deassert` (`d->irq_status |= interrupt->line`,
   `d->irq_status &= ~interrupt->line`), which the offline harness stubs.

## The handler -- `DEVICE_ACCESS(footbridge)`, the parts this closure is about (verbatim, frozen copy)

NOT SHOWN: the PCI-config, UART and timer arms between `switch (relative_addr) {` and `case IRQ_STATUS:`, and the
timer arms after `case FIQ_ENABLE_CLEAR:`.  They read and write no field the five arms read, EXCEPT that a timer
tick reaches `irq_status` through the interrupt callbacks (see §C.5).

```c
DEVICE_ACCESS(footbridge)
{
	struct footbridge_data *d = (struct footbridge_data *) extra;
	uint64_t idata = 0, odata = 0;
	int timer_nr = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
		relative_addr &= ~0x060;
	}

	switch (relative_addr) {
	/* ... NOT SHOWN: VENDOR_ID, DEVICE_ID, PCI config, UART ... */

	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
		else if (!d->warned_irq_status_w) {
			d->warned_irq_status_w = 1;
			fatal("[ WARNING: footbridge write to irq status? "
			    "(once) ]\n");
		}
		break;

	case IRQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status;
		else if (!d->warned_irq_raw_w) {
			d->warned_irq_raw_w = 1;
			fatal("[ footbridge write to irq_raw_status (once) ]\n");
		}
		break;

	case IRQ_ENABLE_SET:
		if (writeflag == MEM_WRITE) {
			d->irq_enable |= idata;
			if (d->irq_status & d->irq_enable)
				INTERRUPT_ASSERT(d->irq);
			else
				INTERRUPT_DEASSERT(d->irq);
		} else {
			odata = d->irq_enable;
		}
		break;

	case IRQ_ENABLE_CLEAR:
		if (writeflag == MEM_WRITE) {
			d->irq_enable &= ~idata;
			if (d->irq_status & d->irq_enable)
				INTERRUPT_ASSERT(d->irq);
			else
				INTERRUPT_DEASSERT(d->irq);
		} else if (!d->warned_irq_clear_r) {
			d->warned_irq_clear_r = 1;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? (once) ]\n");
		}
		break;

	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
		else if (!d->warned_fiq_status_w) {
			d->warned_fiq_status_w = 1;
			fatal("[ WARNING: footbridge write to fiq status? "
			    "(once) ]\n");
		}
		break;

	case FIQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status;
		else if (!d->warned_fiq_raw_w) {
			d->warned_fiq_raw_w = 1;
			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
		}
		break;

	case FIQ_ENABLE_SET:
		if (writeflag == MEM_WRITE)
			d->fiq_enable |= idata;
		break;

	case FIQ_ENABLE_CLEAR:
		if (writeflag == MEM_WRITE)
			d->fiq_enable &= ~idata;
		break;

	/* ... NOT SHOWN: the timer arms ... */

	default:if (writeflag == MEM_READ) {
			fatal("[ footbridge: read from 0x%x ]\n",
			    (int)relative_addr);
		} else {
			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
			    (int)relative_addr, (long long)idata);
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```
(The `#545:` and `#539:` comments inside the arms are omitted here; nothing else is.)  Offsets: IRQ_STATUS 0x180,
IRQ_RAW_STATUS 0x184, IRQ_ENABLE_SET 0x188, IRQ_ENABLE_CLEAR 0x18c, FIQ_STATUS 0x280, FIQ_RAW_STATUS 0x284,
FIQ_ENABLE_SET 0x288, FIQ_ENABLE_CLEAR 0x28c; the timer range is TIMER_1_LOAD 0x300 .. TIMER_4_CLEAR 0x36c.

## §F2 — the first repair's pass-2 findings, with MY disposition of each

*(Self-review is disclosed: I wrote both repairs and every disposition below.  Seats whose finding I ADOPTED:
scrutinise the adoption harder, not softer -- check that the ROWS I added answer your finding, not merely that
your finding was right.)*

**F1 -- legal access with the latches SET, the VALUE channel** (grok, codex seat, Opus b_neg; kimi-substitute on
the latch vector).  `writeflag == MEM_READ && !d->warned_irq_raw_w` made every +0x184 read after one declined write
return 0; X7 checked only the announce count.  **ACCEPTED -> X10**: every latch SET, then each legal read returns its
value over its width, and a legal IRQ Clear write still clears and drives (5 registers x 3 widths + 1 write, x 4
states = 64 rows).  Measured: b_neg 10 green -> 0.
**F2 -- the cross-site latch ORDER** (Opus fl_neg / or_L on a later latch; kimi-substitute).  Every multi-site
sequence declined the sites in one fixed order, so a site's first decline was never made with a LATER site
already latched.  **ACCEPTED -> X11**: each ordered pair (j latched, then i's first decline announces exactly once,
keeps every field and the output) -- 20 rows, seeded.  Measured: fl_neg 10 -> 0; or_L 14 -> 4 (the 4 left are the
equivalent own-latch forms).
**F3 -- the legal Clear write's WIDTH** (codex seat Q3, Opus c_dir).  Every legal write was len 4.  **ACCEPTED ->
X12** (Clear write 0x70 at len 1 and 2).  c_dir 3 -> 0.
**F4 -- the legal Clear write's DATA** (Opus `!(idata >> 8)`; codex-dedicated V9 `~(idata & 0xff)`).  Clear data was
only 0 / 0x70.  **ACCEPTED -> X12** (all-ones data at len 1, 2 and 4).  V9: green -> 3 red.
**F5 -- a condition keyed on a field BIT no state sets** (grok `irq_enable & 0x100`, agy `irq_status & 1`, kimi-
substitute `irq_enable & 1`, glm `fiq_enable & 0x100`, Opus bit_*).  **ACCEPTED -> a fourth state, ONES**
(0xffffffff in all four fields) in X6, X7, X9, X10 and X12: with all-zero, every single-bit condition on one field
diverts in one of the two.  bit_* 50 -> 0.
**F6 -- byte-lane masks on a read value or a decline-body store** (Opus lane_*).  **ACCEPTED -> ONES** as above.
lane 10 -> 0.
**F7 -- the two HEAD predicates dominate every decline and were missing from my §C.2 list** (codex-dedicated T2/T3,
Opus Q1(a)): the write-data fetch `if (writeflag == MEM_WRITE) idata = ...` and the timer-fold range test.
**REFINED, not rowed separately**: (i) the fetch feeds only `idata`, which NO decline reads; on the legal side its
`&& len == 4` / `&& len != 1` forms are now RED (X12's narrow Clear writes), and a single-field zero/nonzero
condition on it is held by X9/X12's writes from the all-zero and ones states; (ii) the fold clears only bits 5-6,
and all five offsets (0x180, 0x184, 0x18c, 0x280, 0x284) have bits 5-6 clear, so a WIDENED fold (Opus dom 2) is
EQUIVALENT at the five and only aliases OTHER offsets onto the arms (the address axis, disclosed); a NARROWED fold
(codex's nine timer-range x field pairs) changes only timer registers (other registers' semantics, disclosed).
**F8 -- conditions on one EXACT field value** (Opus e_dir/e_flag 40; codex-dedicated V3; glm on repair 1's
contract).  **DISCLOSED (clause e)**: the bodies test no values, and no finite set of states holds every value.
The contract now names it.
**F9 -- "bits 8-31 are exercised" and the X8 row names "(all 32 bits)" overclaim** (glm, codex seat, Opus Q1(c)).
**ACCEPTED for the comments** (gate comment rewritten; the X8 comment now says the wide seeds set bytes 0, 2 and 3
and the ONES state exercises byte 1).  **Row NAMES kept**: renaming breaks the carried-kills row identity; "(all 32
bits)" means the len-4 read is compared over all 32 bits of its result.
**F10 -- X9's header said "every legal access"** (codex seat Q4, codex-dedicated T3, kimi-substitute, Opus Q4).
**ACCEPTED**: the header now lists exactly the reads at 1/2/4 and the eight enable writes at len 4, and points at
X12 for the Clear write's other widths and data.
**F11 -- stale sentences in repair 1** ("every seed above fits in ONE byte" in X8 once wide seeds landed; X9's
"returned 0" should say READ DATA 0; the brief's "59 variants against TABLE4" was really 59 ENTRIES: FIX + 49 +
nine new; "never amended" cannot be proved by a snapshot) (codex seat Q4).  **ACCEPTED**, all corrected (the brief
above uses the corrected forms).
**F12 -- the gate pins distinct-name COUNTS per family, not identities** (codex-dedicated T4): a required row
replaced by another uniquely-named passing row keeps every count.  **FILED** as a new LOW item (`fbgateidentity`):
it concerns edits to the DETECTOR, not to the product, so it is not a floor question for this round.
**F13 -- the CPU irq line can stick high** (Opus: `line10+` while disabled, then `W188=0x400`, then `line10-`
leaves the line at 1 while IRQ_STATUS reads 0 -- the enable arms call `INTERRUPT_ASSERT` without setting
`irq_asserted`, and `footbridge_interrupt_deassert` deasserts only `if (... && d->irq_asserted)`).  **FILED MED
(`fbirqstuck`)**: a real product defect in two arms #545 did not edit; its own round.
**F14 -- no guest reset-state reads** -- settled (§C.4).

**D1 -- SHIP vs DO NOT SHIP on repair 1** (agy, deepseek, minimax SHIP; codex, grok, glm, kimi-substitute DO NOT
SHIP).  **Settled by MEASUREMENT**: the Opus seat's 153 greens were real; the DO NOT SHIP side was right.

**WHAT IS STILL OWED**: the gate run at 707 (`gate_offline.sh`), the flagship seat's second look, and the records.
**WHERE I MIGHT BE FOOLING MYSELF**: I have accepted or refined ELEVEN of fourteen findings.  That is a suspicious
number, and agreement is not evidence.  And the contract's "THE SPACE" is MY enumeration; F7 shows my previous one
was incomplete.

## The repair-2 diff (INLINED IN FULL -- `diff -u` of the 491-row instrument against the 707-row one)

`git diff --numstat`-style for this repair's files:
    regress/diff_footbridge.c   INLINED (the whole repair-2 diff, below)
    regress/gate_offline.sh     INLINED (its whole repair-2 diff, below)
    src/devices/dev_footbridge.c  NOT SHOWN as a diff -- unchanged by both repairs (md5 783c0c7f); its
                                  relevant function is inlined above
    regress/footbridge_sites_probe.py and the other #545 files -- unchanged by both repairs

### regress/diff_footbridge.c (491 rows, ff8f87b6 -> 707 rows, 4d7bdcc3)

```diff
--- a/regress/diff_footbridge.c
+++ b/regress/diff_footbridge.c
@@ -829,31 +829,42 @@
 	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).
 	 *
 	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4) x data (zero, nonzero; writes only) x state
-	 *      (seeded, all-zero, wide) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
+	 *      (seeded, all-zero, wide, ones) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
 	 *      returns 1; the announce count moves by exactly 1 on the first access and 0 on the repeat; all four
 	 *      register fields are unchanged; the interrupt output is untouched (no assert, no deassert); and a
 	 *      declined read returns 0 over its whole width.
 	 *  X7: EVERY LEGAL ACCESS RE-ARMS NO LATCH -- with all five sites latched: each enable write (Set/Clear,
 	 *      IRQ/FIQ) with zero and nonzero data, and each legal read of the readable registers plus VENDOR_ID
-	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded, all-zero and wide states (so a read that
-	 *      returns 0 is covered, and so is a field bit above byte 0).  After each, re-declining all five sites
-	 *      must announce nothing.
-	 *  X9 (below X8) is the other half of the legal side: every legal access with the latches still CLEAR.
+	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded, all-zero, wide and ones states (so a read
+	 *      that returns 0 is covered, and so is every bit of every field).  After each, re-declining all five
+	 *      sites must announce nothing.  X7 observes the ANNOUNCE channel only; the value channel of a legal
+	 *      access with the latches set is X10's.
+	 *  X9-X12 (below X8) are the rest of the legal side: X9 with the latches still CLEAR, X10 with every latch
+	 *  SET (value and effect), X11 the cross-site latch ORDER, X12 the legal Clear write's width and data.
 	 *
-	 *  CONTRACT (clause e): the class is ACCESS (declined, legal) x STATE (seeded, all-zero, wide) x LATCH
-	 *  (clear, set) at these five sites -- declined x both latches in X6, legal x set in X7, legal x clear in
-	 *  X9.  *** THIS SAID "the cells above are the whole class" UNTIL THE ADJUDICATION PASS OF 2026-09-23, AND
-	 *  IT WAS MEASURED FALSE: X7 latched every site BEFORE its legal access, so LEGAL x ALL-ZERO x LATCH-CLEAR
-	 *  -- the reset state -- had no row, and five one-conjunct edits to the DIRECTION test (`writeflag ==
-	 *  MEM_READ && d->irq_enable` and its mirrors) passed all 333 rows here and all 37 guest rows
-	 *  (regress/artifacts/fbd5/q2_20260923/Q2.log). ***  The DEPENDS-ON bound these rows use: the predicates
-	 *  dominating each edited decline (case label, direction test, latch), and the lvalues read by BOTH
-	 *  branches under the direction test -- the four interrupt fields and the five latches.  Not in the
-	 *  class: the interrupt output after a LEGAL access except where X9 pins it, any other register's
-	 *  semantics, WIDE DATA on a declined write (data stays 0 / 0x70), joint conjuncts over two fields
-	 *  beyond the three states, and a latch guard conditioned on a field neither branch reads (measured F1:
-	 *  `&& !timer_control[0]` passes every row here; the guest sites probe catches it only because its
-	 *  prologue arms timer 1; table4_20260919).
+	 *  CONTRACT (clause e).  THE SPACE, enumerated from the handler: the case label (the timer fold maps no
+	 *  address onto these five), the direction test, the width, idata (read by the legal Clear write), the four
+	 *  interrupt fields (read by the legal branches) and the five latches (each read by its own decline).  The
+	 *  bodies TEST only the direction, their own latch, and (irq_status & the new enable) in the Clear write;
+	 *  every other input is a value they compute with.  COVERED: declined x width x data {0, 0x70} x state x
+	 *  first/repeat (X6); legal x width x state x own latch clear (X9) and every latch set (X7 announce, X10
+	 *  value and effect); each ordered pair of sites for the first decline (X11); the legal Clear write at every
+	 *  width and with all-ones data (X9, X12).  STATES: seeded, all-zero, wide and ONES -- with all-zero, the
+	 *  ones state makes every single-bit condition on one field divert in one of the two.
+	 *  *** THIS SAID "the cells above are the whole class" and was measured false TWICE on 2026-09-23: first the
+	 *  reset state (legal x all-zero x latches clear -- five one-conjunct edits to the DIRECTION test passed all
+	 *  333 rows and all 37 guest rows, q2_20260923/Q2.log), then, after X9 closed that, the value channel with
+	 *  the latches set, the cross-site order, the narrow Clear write and any field bit no state set (the Opus
+	 *  seat's 434 variants, _scratchpad/fbd5/q2r/opus/; a row set it built and measured is X10-X12). ***
+	 *  NOT COVERED, stated so a later escape is "outside the contract", not a surprise: a condition on one EXACT
+	 *  field value (`d->irq_enable != 0x10`) -- the bodies test no values and no finite set of states holds them
+	 *  all; the ADDRESS axis -- a case label added for another offset, or a widened timer fold, aliasing an
+	 *  address onto an arm; joint conditions over two fields beyond the four states, or over two latches beyond
+	 *  X11's pairs; WIDE DATA on a declined write (data stays 0 / 0x70); the interrupt output after a legal
+	 *  access except where X9/X10/X12 pin it; any other register's semantics; and a latch guard conditioned on
+	 *  a field neither branch reads (measured F1: `&& !timer_control[0]` passes every row here; the guest sites
+	 *  probe catches it only because its prologue arms timer 1; table4_20260919).  fiq_status has NO writer in
+	 *  the product, so every FIQ status value these rows seed is synthetic.
 	 */
 	{
 		static const struct { uint64_t addr; int wf; const char *nm; } S5[] = {
@@ -861,10 +872,14 @@
 			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
 			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
 		/*  #545 adjudication (Fable 5.1, Q2 (e) cell): the byte seeds left bits 8-31 of every field unexercised,
-		    so a decline store or a latch clearer keyed on them passed every row.  "wide" is X8's seeds.  */
-		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[3] = {
+		    so a decline store or a latch clearer keyed on them passed every row.  "wide" is X8's seeds -- and it
+		    still left byte 1 of every field, bit 0, bits 18-29 and byte 3 of the enables at 0, so a condition keyed
+		    on one of those bits passed every row (repair pass 2, five seats; Opus measured 30 such edits green).
+		    "ones" sets every bit of every field: with all-zero, a single-bit condition diverts in one of the two.  */
+		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[4] = {
 			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
-			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
+			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" },
+			{ 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, "ones" } };
 		static const int W[3] = { 1, 2, 4 };
 		static const struct { uint64_t addr; int wf; uint64_t data; const char *nm; } LW[8] = {
 			{ IRQ_ENABLE_SET, MEM_WRITE, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, MEM_WRITE, 0x70, "IRQ Set write 0x70" },
@@ -884,7 +899,7 @@
 #define XSAME(x, s) ((x)->irq_status == ST[s].is && (x)->irq_enable == ST[s].ie && (x)->fiq_status == ST[s].fs \
 		&& (x)->fiq_enable == ST[s].fe)
 		for (si = 0; si < 5; si++)
-			for (st = 0; st < 3; st++)
+			for (st = 0; st < 4; st++)
 				for (wi = 0; wi < 3; wi++)
 					for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {
 						x = calloc(1, sizeof(*x)); XSET(x, st);
@@ -905,7 +920,7 @@
 						}
 						free(x);
 					}
-		for (st = 0; st < 3; st++)
+		for (st = 0; st < 4; st++)
 			for (k = 0; k < 8 + 9 * 3; k++) {
 				x = calloc(1, sizeof(*x)); XSET(x, st);
 				for (si = 0; si < 5; si++) {
@@ -934,10 +949,10 @@
 #undef XSET
 		fatal_calls = 0;
 	}
-	/*  X8 (adjudication pass, G11): every seed above fits in ONE byte, so a legal read truncated to 8 bits
-	    passed every row.  Wide seeds, bits in every byte lane that matters: each legal word read returns its
-	    full 32-bit value (the masked reads: 0x80010018 & 0x00010030 = 0x00010010, 0x40020060 & 0x000200c0 =
-	    0x00020040).  */
+	/*  X8 (adjudication pass, G11): every seed in the P-rows and X1-X5 fits in ONE byte, so a legal read
+	    truncated to 8 bits passed every row.  Wide seeds: each legal word read returns its full 32-bit value
+	    (the masked reads: 0x80010018 & 0x00010030 = 0x00010010, 0x40020060 & 0x000200c0 = 0x00020040).  These
+	    seeds set bits in bytes 0, 2 and 3 only; the ONES state in X6/X7/X9-X12 is what exercises byte 1.  */
 	{
 		struct footbridge_data *x = calloc(1, sizeof(*x));
 		unsigned char b[8];
@@ -962,21 +977,25 @@
 		free(x);
 		fatal_calls = 0;
 	}
-	/*  X9 (adjudication pass, 2026-09-23 -- Fable 5.1's Q2, MEASURED before this block existed): EVERY LEGAL
-	    ACCESS WITH THE LATCHES STILL CLEAR, from each state.  X7 latched all five sites before its legal access,
+	/*  X9 (adjudication pass, 2026-09-23 -- Fable 5.1's Q2, MEASURED before this block existed): the legal
+	    accesses of the five sites -- reads of the four status registers and of IRQEnable (+0x188) at widths 1, 2
+	    and 4, and the eight enable writes at len 4 (X12 has the Clear write's other widths and data) -- WITH THE
+	    LATCHES STILL CLEAR, from each state.  X7 latched all five sites before its legal access,
 	    so a direction test conjoined with a field that is 0 in the RESET state (`writeflag == MEM_READ &&
 	    d->irq_enable` at IRQ_STATUS, its three read mirrors, `writeflag == MEM_WRITE && d->irq_enable` at
 	    IRQEnableClear) sent the legal access into the decline, which announced a phantom complaint, consumed the
-	    latch and returned 0 -- the right value in that state -- and every row stayed green
+	    latch and -- for the reads -- returned read data 0, the right value in that state; the diverted Clear WRITE
+	    cleared nothing, which in that state is also the right result -- and every row stayed green
 	    (regress/artifacts/fbd5/q2_20260923/Q2.log: 333/333 and 37/37 for all five).  Each cell is ONE row on a
 	    fresh instance: the access returns 1 and announces nothing; a read returns its value over the width and
 	    changes no field; a write sets the enable it targets as written and leaves the other three alone, and IRQ
 	    Set/Clear drive the interrupt output exactly once by (irq_status & the new enable) while FIQ Set/Clear do
 	    not touch it; then the five declines announce EXACTLY 5, because no latch was consumed.  */
 	{
-		static const struct { uint32_t is, ie, fs, fe; const char *nm; } S9[3] = {
+		static const struct { uint32_t is, ie, fs, fe; const char *nm; } S9[4] = {
 			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
-			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
+			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" },
+			{ 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, "ones" } };
 		static const struct { uint64_t addr; int wf; } D5[5] = {
 			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
 			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
@@ -993,7 +1012,7 @@
 		char xn[200];
 		int st, k, si, a0, d0, rv, ok;
 		struct footbridge_data *x;
-		for (st = 0; st < 3; st++)
+		for (st = 0; st < 4; st++)
 			for (k = 0; k < 5 * 3 + 8; k++) {
 				uint32_t is = S9[st].is, ie = S9[st].ie, fs = S9[st].fs, fe = S9[st].fe;
 				x = calloc(1, sizeof(*x));
@@ -1039,12 +1058,132 @@
 			}
 		fatal_calls = 0;
 	}
-	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (78 P-rows + 222 X-rows); the adjudication
-	    pass, 2026-09-23: 333 -> 491 (X6 +54 and X7 +35 for the wide state, X9 69).  */
+	/*  X10-X12 (the first repair's own pass 2, 2026-09-23).  The Opus measuring seat built 434 one-line variants of the
+	    five arms against the 491-row instrument; 153 passed, and the in-bound ones fell into three cells no row had:
+	    the VALUE of a legal access with the latches SET (X7 counts announces only: `writeflag == MEM_READ &&
+	    !d->warned_irq_raw_w` made every +0x184 read after one declined write return 0, guest-visible), the ORDER of
+	    two sites' latches (every multi-site sequence declined the sites in one fixed order, so a site's first decline
+	    was never made with a LATER site already latched), and the legal Clear write's WIDTH and DATA (every legal
+	    write was len 4 with data 0 or 0x70).  The seat measured this row set in scratch -- it reddened every in-bound
+	    variant that passed -- and it is adopted here with the fourth state added and all-ones Clear data.
+	    X10: every latch SET, then each legal read returns its value over its width, and a legal IRQ Clear write still
+	         clears and drives the output (5 registers x 3 widths + 1 write, x 4 states).
+	    X11: each ordered pair of sites: latch j, then i's FIRST decline announces exactly once and keeps every field
+	         and the interrupt output (20 pairs, seeded).
+	    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear
+	         (x 4 states): it clears (ne = ie & ~idata, idata the low bytes the width carries), drives the output once by
+	         (irq_status & ne), announces nothing, and the five declines that follow announce exactly 5.  */
+	{
+		static const struct { uint32_t is, ie, fs, fe; const char *nm; } SY[4] = {
+			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
+			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" },
+			{ 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, "ones" } };
+		static const struct { uint64_t addr; int wf; const char *nm; } DY[5] = {
+			{ IRQ_STATUS, MEM_WRITE, "write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "write IRQ_RAW_STATUS" },
+			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
+			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
+		static const struct { uint64_t addr; const char *nm; } RY[5] = {
+			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
+			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQEnable" } };
+		static const struct { int w; uint64_t data; const char *nm; } CY[5] = {
+			{ 1, 0x70, "0x70 len 1" }, { 2, 0x70, "0x70 len 2" }, { 1, 0xffffffffULL, "all-ones len 1" },
+			{ 2, 0xffffffffULL, "all-ones len 2" }, { 4, 0xffffffffULL, "all-ones len 4" } };
+		static const int WY[3] = { 1, 2, 4 };
+		unsigned char b[8];
+		char yn[200];
+		int i, j, st, r, w, c, si, a0, d0, f0, ok;
+		struct footbridge_data *x;
+#define YNEW(s) do { x = calloc(1, sizeof(*x)); arm_irqs(x); x->irq.interrupt_assert = noop_assert; \
+		x->irq.interrupt_deassert = noop_deassert; x->irq_status = SY[s].is; x->irq_enable = SY[s].ie; \
+		x->fiq_status = SY[s].fs; x->fiq_enable = SY[s].fe; } while (0)
+#define YSAME(s) (x->irq_status == SY[s].is && x->irq_enable == SY[s].ie && x->fiq_status == SY[s].fs \
+		&& x->fiq_enable == SY[s].fe)
+#define YDECLINE_ALL() do { for (si = 0; si < 5; si++) { memory_writemax64(cpu, b, 4, 0x70); \
+		dev_footbridge_access(cpu, NULL, DY[si].addr, b, 4, DY[si].wf, x); } } while (0)
+		/*  X10  */
+		for (st = 0; st < 4; st++) {
+			for (r = 0; r < 5; r++)
+				for (w = 0; w < 3; w++) {
+					uint32_t is = SY[st].is, ie = SY[st].ie, fs = SY[st].fs, fe = SY[st].fe;
+					uint64_t want = r == 0 ? (uint64_t) (is & ie) : r == 1 ? (uint64_t) is
+					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
+					want &= WY[w] == 4 ? 0xffffffffULL : WY[w] == 2 ? 0xffffULL : 0xffULL;
+					YNEW(st);
+					YDECLINE_ALL();
+					f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+					memset(b, 0xa5, sizeof(b));
+					dev_footbridge_access(cpu, NULL, RY[r].addr, b, WY[w], MEM_READ, x);
+					ok = fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)
+					    && irq_asserts == a0 && irq_deasserts == d0;
+					snprintf(yn, sizeof(yn), "X10 legal len %d read of %s (%s, latches SET) returns its value",
+					    WY[w], RY[r].nm, SY[st].nm);
+					check_u(yn, ok, 1);
+					free(x);
+				}
+			{
+				uint32_t is = SY[st].is, ne = SY[st].ie & ~0x70u;
+				YNEW(st);
+				YDECLINE_ALL();
+				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+				memory_writemax64(cpu, b, 4, 0x70);
+				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
+				ok = fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
+				    && x->fiq_status == SY[st].fs && x->fiq_enable == SY[st].fe
+				    && ((is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
+				                  : (irq_asserts == a0 && irq_deasserts == d0 + 1));
+				snprintf(yn, sizeof(yn), "X10 IRQ Clear write 0x70 (%s, latches SET) clears and drives", SY[st].nm);
+				check_u(yn, ok, 1);
+				free(x);
+			}
+		}
+		/*  X11  */
+		for (j = 0; j < 5; j++)
+			for (i = 0; i < 5; i++) {
+				if (i == j)
+					continue;
+				YNEW(0);
+				memory_writemax64(cpu, b, 4, 0x70);
+				dev_footbridge_access(cpu, NULL, DY[j].addr, b, 4, DY[j].wf, x);
+				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+				memory_writemax64(cpu, b, 4, 0x70);
+				dev_footbridge_access(cpu, NULL, DY[i].addr, b, 4, DY[i].wf, x);
+				ok = fatal_calls - f0 == 1 && YSAME(0) && irq_asserts == a0 && irq_deasserts == d0;
+				snprintf(yn, sizeof(yn), "X11 first %s after %s latched: announced once", DY[i].nm, DY[j].nm);
+				check_u(yn, ok, 1);
+				free(x);
+			}
+		/*  X12  */
+		for (st = 0; st < 4; st++)
+			for (c = 0; c < 5; c++) {
+				uint64_t mask = CY[c].w == 4 ? 0xffffffffULL : CY[c].w == 2 ? 0xffffULL : 0xffULL;
+				uint32_t is = SY[st].is, ne = SY[st].ie & ~(uint32_t) (CY[c].data & mask);
+				YNEW(st);
+				fatal_calls = 0; a0 = irq_asserts; d0 = irq_deasserts;
+				memory_writemax64(cpu, b, CY[c].w, CY[c].data);
+				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
+				ok = fatal_calls == 0 && x->irq_enable == ne && x->irq_status == is
+				    && x->fiq_status == SY[st].fs && x->fiq_enable == SY[st].fe
+				    && ((is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
+				                  : (irq_asserts == a0 && irq_deasserts == d0 + 1));
+				YDECLINE_ALL();
+				ok = ok && fatal_calls == 5;
+				snprintf(yn, sizeof(yn), "X12 IRQ Clear write %s (%s, latches clear)", CY[c].nm, SY[st].nm);
+				check_u(yn, ok, 1);
+				free(x);
+			}
+#undef YDECLINE_ALL
+#undef YSAME
+#undef YNEW
+		fatal_calls = 0;
+	}
+	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (the 33 are the 32 timer rows and this one;
+	    then 78 P-rows + 222 X-rows); the adjudication pass, 2026-09-23: 333 -> 491 (X6 +54 and X7 +35 for the wide
+	    state, X9 69); its repair's own pass 2: 491 -> 707 (the ones state: X6 +54, X7 +35, X9 +23; X10 64, X11 20,
+	    X12 20).  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "491");
+		check("IDENTITY row count -- guards against a stale copy", buf, "707");
 	}
 
 	printf("\n%d rows, %d failures\n", rows, fails);
```

### regress/gate_offline.sh (03cea4dc... -> 45d2b495)

```diff
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -585,7 +585,7 @@
     check     "footbridge: row failures" \
               "$(grep -oE '[0-9]+ failures' "$FBLOG" | grep -oE '^[0-9]+')" "0"
     check_min "footbridge: rows actually run" \
-              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 491
+              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 707
     check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
     #  #545: the five declined sites.  P0-P9 pin preservation under a NONZERO seeded status, the read
     #  expressions, the latch per site and byte-first at IRQ_STATUS; X1-X3 (the pass-2 L2 repair) pin
@@ -593,21 +593,29 @@
     #  X4/X5 pin ZERO data / a zero enable as the first access, and a legal zero Clear write.  X6/X7 are
     #  the CLASS CLOSURE (two consecutive passes found cells of one space): every declined access --
     #  site x width x data x state x first/repeat -- keeps every field and the interrupt output and reads
-    #  0; every legal access, from seeded, all-zero and wide state, re-arms no latch.  X8: wide (multi-byte)
-    #  seeds, so a legal read truncated to 8 bits reds.  X9 (the adjudication pass, 2026-09-23): every LEGAL access
-    #  with the latches still CLEAR, from the seeded, all-zero and wide states -- X7 latched every site first, so
-    #  five one-conjunct edits to the direction test (`writeflag == MEM_READ && d->irq_enable` and mirrors) passed
-    #  every row (q2_20260923/Q2.log); and a WIDE third state in X6/X7, so bits 8-31 of a field are exercised.
-    #  Kill tables: regress/artifacts/fbd5/{killtable,xtable,table3,table4}_20260919/ and q2_20260923/repair/.
+    #  0; every legal access with every latch set re-arms no latch.  X8: wide (multi-byte) seeds, so a legal read
+    #  truncated to 8 bits reds.  X9 (the adjudication pass, 2026-09-23): the legal accesses with the latches still
+    #  CLEAR -- X7 latched every site first, so five one-conjunct edits to the direction test (`writeflag ==
+    #  MEM_READ && d->irq_enable` and mirrors) passed every row (q2_20260923/Q2.log).  X10-X12 (that repair's own
+    #  pass 2, where the Opus seat's 434 variants found three more cells open): X10 the VALUE of a legal access
+    #  with every latch set, X11 each ordered pair of sites' latches, X12 the legal Clear write's width and data.
+    #  STATES in X6/X7/X9/X10/X12: seeded, all-zero, wide and ONES -- the ones state sets every bit of every field,
+    #  so with all-zero a condition keyed on any single bit diverts in one of the two.  Not covered, and said so in
+    #  diff_footbridge.c's contract: a condition on one exact field value, and the address axis.
+    #  Kill tables: regress/artifacts/fbd5/{killtable,xtable,table3,table4}_20260919/ and
+    #  regress/artifacts/fbd5/q2_20260923/{repair,repair2}/.
     #  COUNTED AS DISTINCT GREEN ROW NAMES, not green lines (adjudication pass, G10): a duplicated green
     #  line cannot stand in for a missing row.  Every row name in the file is unique on the fix.
     fb_distinct() { grep -E "^  ok    $1 " "$FBLOG" | sed -E 's/^  ok    //; s/[[:space:]]+[0-9]+$//' | sort -u | wc -l | tr -d ' '; }
     check "footbridge: #545 P-rows green (P0-P9), distinct names" "$(fb_distinct 'P[0-9]')" "78"
-    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "311"
-    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "162"
-    check "footbridge: #545 X7 every legal access re-arms no latch" "$(fb_distinct 'X7')" "105"
+    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "400"
+    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "216"
+    check "footbridge: #545 X7 every legal access re-arms no latch" "$(fb_distinct 'X7')" "140"
     check "footbridge: #545 X8 wide legal reads keep all 32 bits" "$(fb_distinct 'X8')" "6"
-    check "footbridge: #545 X9 legal access, latches clear, all states" "$(fb_distinct 'X9')" "69"
+    check "footbridge: #545 X9 legal access, latches clear, all states" "$(fb_distinct 'X9')" "92"
+    check "footbridge: #545 X10 legal access, latches SET, value kept" "$(fb_distinct 'X10')" "64"
+    check "footbridge: #545 X11 every ordered pair of site latches" "$(fb_distinct 'X11')" "20"
+    check "footbridge: #545 X12 legal Clear write, every width and data" "$(fb_distinct 'X12')" "20"
     #  Name each row that is the SOLE detector of something.
     check "footbridge: the zero-load row is present" \
           "$(grep -c 'load 0 becomes the full 24-bit span' "$FBLOG")" "1"
```

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1(c) and Q3 first)

**Q1 -- verify the enumeration (the closing pass's job).**  The rewritten CONTRACT (in the diff above, the comment
above the X6 rows) states THE SPACE, what is COVERED and what is NOT COVERED.  Against the inlined handler:
 (a) is every input and every partition the five bodies TEST named in THE SPACE?  Name any that is missing;
 (b) for each COVERED class, name the row family that holds it (X6, X7, X9, X10, X11, X12) and say whether those
     rows observe a channel that actually DIFFERS under a one-condition edit in that class -- a row whose observable
     cannot vary under the edit it is for does not hold it;
 (c) is every NOT COVERED item genuinely outside the floor of §C.2, or is one of them a floor cell that is owed a
     row?  Check F7's two premises in particular rather than accepting them: that no decline reads `idata`, and that
     the timer fold changes none of the five offsets (ENUMERATE `offset & ~0x060` for 0x180, 0x184, 0x18c, 0x280,
     0x284).
**Q2 -- the smallest edit that the 707 rows cannot see and the contract does not disclose.**  Name one change to the
five arms or the two head predicates that re-opens what the declines protect -- a legal access treated as a bad
one, a bad one not announced, a field changed, a latch consumed or re-armed, the interrupt output driven -- while
every one of the 707 rows stays green, and that is NOT in the NOT COVERED list.  Name the row you expect to stay
green.  If you find none, give your denominator: which edit shapes, at which arms.
**Q3 -- adjudicate the §F2 list.**  F1..F14 and D1: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a
reason.  Then: **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or refined eleven of fourteen findings.
In particular: is keeping the X8 row NAMES (F9) right; is F7's "refined, not rowed" right; is FILING F12 and F13,
rather than fixing them in this round, right?
**Q4 -- records.**  Is any sentence in the added or rewritten comments (the X8, X9 and X10-X12 headers, the CONTRACT,
the IDENTITY comment, the gate_offline.sh comment) false as of today, or stale the moment it lands?  ENUMERATE the
IDENTITY arithmetic -- 707 = 33 + 78 + 38 + 216 + 140 + 6 + 92 + 64 + 20 + 20 -- against the loops in the diff, and
the gate pins (X[1-8] 400, X6 216, X7 140, X8 6, X9 92, X10 64, X11 20, X12 20) against the same loops.
**Q5 -- option-set completeness.**  For F12 and F13 I chose FILE.  Is there a disposition I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
