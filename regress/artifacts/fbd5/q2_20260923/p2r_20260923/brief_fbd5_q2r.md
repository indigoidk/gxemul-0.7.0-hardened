# #545 repair pass 2 -- rows added to the footbridge offline differential after the flagship seat's reading was measured true

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** -- this repair touches `regress/diff_footbridge.c` and
`regress/gate_offline.sh` only; `src/devices/dev_footbridge.c` is unchanged by it.  File-reading seats:
read the FROZEN copies in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2r\frozen\` (md5: dev_footbridge.c
783c0c7f, diff_footbridge.c ff8f87b6, diff_footbridge.prerepair.c 116083d0, gate_offline.sh 03cea4dc), not
the working files, which other work may touch.  There are THREE pristine-2021-upstream copies of GXemul
under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this
fork.  If your line numbers disagree with mine by hundreds you are reading one of them — say so.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a set, a membership — ENUMERATE it
rather than reasoning about it.**  And ENUMERATE THE RIGHT DOMAIN — ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation: `VERDICT: SHIP` or
`VERDICT: DO NOT SHIP -- <reason>`.

## What #545 is, and what this repair is (plain engineering language)

#545 changed five register arms of the DC21285 "footbridge" device model.  Before it, a guest WRITE to
any of four read-only status registers (IRQ_STATUS +0x180, IRQ_RAW_STATUS +0x184, FIQ_STATUS +0x280,
FIQ_RAW_STATUS +0x284) or a guest READ of the write-only IRQEnableClear (+0x18c) ended the emulator process.
After it, each such access is DECLINED -- no register changes, a declined read returns 0 -- and ANNOUNCED
ONCE per site through a per-site warn-once latch (`warned_*`).  The detector is two instruments:
`regress/diff_footbridge.c`, an offline differential that `#include`s the real `dev_footbridge.c` and calls
its access function directly, and `regress/footbridge_sites_probe.py`, a 37-row guest probe.

The round has had pass 1, pass 2, an adjudication pass (§F2) and a regress/adjudication pass by the
flagship seat.  That last pass predicted, BY READING, that five one-condition edits to the DIRECTION test
of the edited arms would leave every row green:

    Q1  IRQ_STATUS        `if (writeflag == MEM_READ)`  ->  `if (writeflag == MEM_READ && d->irq_enable)`
    Q2  IRQ_RAW_STATUS    `if (writeflag == MEM_READ)`  ->  `if (writeflag == MEM_READ && d->irq_status)`
    Q3  FIQ_STATUS        `if (writeflag == MEM_READ)`  ->  `if (writeflag == MEM_READ && d->fiq_enable)`
    Q4  FIQ_RAW_STATUS    `if (writeflag == MEM_READ)`  ->  `if (writeflag == MEM_READ && d->fiq_status)`
    Q5  IRQ_ENABLE_CLEAR  `if (writeflag == MEM_WRITE) {`  ->  `if (writeflag == MEM_WRITE && d->irq_enable) {`

In the RESET state (every field 0, every latch clear) each sends a LEGAL access into the decline branch,
which announces a complaint that did not happen, consumes that site's latch (so the next real bad access
is silent) and -- for the reads -- returns 0, which is also the right value in that state.  The existing
rows could not see it: the latch-clear legal rows (X2, X5, X8) all run in a SEEDED state where the added
condition is true, and X7, which does run the all-zero state, latches every site before its legal access.

**MEASURED BEFORE THE REPAIR** (`regress/artifacts/fbd5/q2_20260923/Q2.log`, scratch trees, restored and
`cmp`-verified): FIX 333/333 offline + 37/37 guest; **Q1..Q5 each 333/333 and 37/37** -- all five confirmed.

**THE REPAIR (rows only; product code unchanged):**
* **X9**, 69 rows: every LEGAL access with the latches still CLEAR -- the five readable registers
  (IRQ_STATUS, IRQ_RAW_STATUS, FIQ_STATUS, FIQ_RAW_STATUS, and IRQEnable at +0x188) at widths 1, 2 and 4,
  plus the eight enable writes (Set/Clear x IRQ/FIQ x data 0 / 0x70) -- from three states: seeded
  (0x18/0x30/0x60/0xc0), all-zero, and wide (0x80010018/0x00010030/0x40020060/0x000200c0).  Each cell is ONE
  row on a fresh instance: returns 1, announces nothing, reads its value over the width (or writes the
  targeted enable as written, leaves the other three fields, and for IRQ Set/Clear drives the interrupt
  output exactly once by `irq_status & new_enable`, for FIQ not at all); then the five declines must
  announce EXACTLY 5, because no latch was consumed.
* **A WIDE third state in X6 and X7** (+54, +35 rows): every earlier seed fit in one byte, so an edit
  keyed on bits 8-31 of a field passed every row (the flagship seat's "(e) cell").
* IDENTITY 333 -> 491; `gate_offline.sh` pins moved to 491 / 311 / 162 / 105 / 6 / 69 (distinct green names).

**PRETABLE_Q2.out** was written at 14:19:25 and never amended; the repair table started 14:22:42.

**MEASURED AFTER THE REPAIR** (`q2_20260923/repair/Q2R.log`, one frozen instrument, md5 ff8f87b6):

    FIX  491 rows, 0 failures
    Q1   3 red: X9 legal len 1/2/4 read of IRQ_STATUS (all-zero, latches clear)
    Q2   3 red: X9 ... IRQ_RAW_STATUS (all-zero)      Q3  3 red: X9 ... FIQ_STATUS (all-zero)
    Q4   3 red: X9 ... FIQ_RAW_STATUS (all-zero)      Q5  2 red: X9 IRQ Clear write 0 / 0x70 (all-zero)
    W1   12 red, all "X6 write IRQ_STATUS ... wide first/repeat"   (control: decline body also does
         `d->irq_status &= 0xffff;` -- invisible at byte seeds)
    W2   3 red, all "X7 legal len 1/2/4 read of IRQ_STATUS (wide) re-arms NO latch"   (control: the
         IRQ_STATUS read branch also clears its latch when `d->irq_status >> 16`)
    T1, T2 (the earlier width controls)  2 red each
    59 variants compared row-by-row against the 327-row TABLE4 (`q2_20260923/repair/CARRIED_KILLS.txt`):
    0 lost; one historic ROW RENAME is mapped, not counted (the 333-row instrument renamed an X3 row).
    Every prediction in PRETABLE_Q2.out matched exactly.  Guest-only variants (M9, Z9 announce TEXT; F1
    `&& !timer_control[0]`) are 0 offline before and after, by design.

## §C — SETTLED PREMISES (recorded resolutions; do not re-derive, but say if the diff contradicts one)

1. **The product change is settled** -- decline + once-latched announce at the five sites, the value 0 for
   the declined read; pass 1, pass 2, §F2 and the adjudication all ruled on it; this repair does not touch it.
2. **The DEPENDS-ON bound these rows answer to** (adjudication pass, Q1/D1): the predicates DOMINATING each
   edited decline, walked to the function boundary -- the case label, the direction test, the latch -- and
   the lvalues read by BOTH branches under the direction test: `irq_status`, `irq_enable`, `fiq_status`,
   `fiq_enable` and the five latches.
3. **Insertion-class edits in OTHER cases** (a writer added at +0x188, the FIQ enable pair, TIMER_1_VALUE)
   are outside that closure (adjudication Q1 narrowed them); their existing rows stay, ungraded as floor.
4. **The guest reset-state reads the flagship seat RECOMMENDED** (+0x180/+0x184/+0x280/+0x284 at the head of
   the probe's arm S, scored on a buffer mark) are NOT added -- the floor is carried offline by X9, and arm
   S keeps its disclosed "order, not emitter" limit.  Q5 below asks whether that is right.

## THE HANDLER ARMS (dev_footbridge.c, unchanged by this repair; lines 566-660 of the frozen copy)

```c
	case UART_FLAGS:
		odata = UART_TX_EMPTY;
		break;

	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
		else if (!d->warned_irq_status_w) {
			/*  #545: read-only register (7.3.29); the write is
			    declined -- no register changes, only this site's
			    warn-once latch is set -- and announced once.  */
			d->warned_irq_status_w = 1;
			fatal("[ WARNING: footbridge write to irq status? "
			    "(once) ]\n");
		}
		break;

	case IRQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status;
		else if (!d->warned_irq_raw_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
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
			/*  #539: a read of 188h is documented -- IRQEnable is
			    "read-only ... can only be changed by writing to
			    the EnableSet and EnableClear registers", reset 0
			    (DC21285 Table 7-10, 7.3.31).  The value below was
			    always right; the exit(1) that followed it is gone.  */
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
			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
			    7-10 names no register at 18Ch for reads, so the read
			    is declined with 0 -- the IRQEnable value that used to
			    be computed here is 188h's answer, not 18Ch's.  */
			d->warned_irq_clear_r = 1;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? (once) ]\n");
		}
		break;

	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
		else if (!d->warned_fiq_status_w) {
			/*  #545: read-only (7.3.29); declined, announced once.  */
			d->warned_fiq_status_w = 1;
			fatal("[ WARNING: footbridge write to fiq status? "
			    "(once) ]\n");
		}
		break;

	case FIQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status;
		else if (!d->warned_fiq_raw_w) {
			/*  #545: read-only (7.3.30); declined, announced once.  */
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

	case TIMER_1_LOAD:
		if (writeflag == MEM_READ)
```

## THE REPAIR DIFF -- regress/diff_footbridge.c (pre-repair md5 116083d0 -> ff8f87b6)

```diff
--- a/regress/diff_footbridge.c
+++ b/regress/diff_footbridge.c
@@ -829,28 +829,42 @@
 	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).
 	 *
 	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4) x data (zero, nonzero; writes only) x state
-	 *      (seeded, all-zero) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
+	 *      (seeded, all-zero, wide) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
 	 *      returns 1; the announce count moves by exactly 1 on the first access and 0 on the repeat; all four
 	 *      register fields are unchanged; the interrupt output is untouched (no assert, no deassert); and a
 	 *      declined read returns 0 over its whole width.
 	 *  X7: EVERY LEGAL ACCESS RE-ARMS NO LATCH -- with all five sites latched: each enable write (Set/Clear,
 	 *      IRQ/FIQ) with zero and nonzero data, and each legal read of the readable registers plus VENDOR_ID
-	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded state and from the all-zero state (so a
-	 *      read that returns 0 is covered).  After each, re-declining all five sites must announce nothing.
+	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded, all-zero and wide states (so a read that
+	 *      returns 0 is covered, and so is a field bit above byte 0).  After each, re-declining all five sites
+	 *      must announce nothing.
+	 *  X9 (below X8) is the other half of the legal side: every legal access with the latches still CLEAR.
 	 *
-	 *  CONTRACT (clause e): the cells above are the whole class for these five sites.  Not in it: the
-	 *  interrupt output after a LEGAL access (the #539 rows), any other register's semantics, and a latch
-	 *  guard conditioned on a device field the decline body never reads (measured F1: `&& !timer_control[0]`
-	 *  passes every row here -- it is outside the DEPENDS-ON bound, and the guest sites probe catches it
-	 *  only because its prologue arms timer 1; table4_20260919).
+	 *  CONTRACT (clause e): the class is ACCESS (declined, legal) x STATE (seeded, all-zero, wide) x LATCH
+	 *  (clear, set) at these five sites -- declined x both latches in X6, legal x set in X7, legal x clear in
+	 *  X9.  *** THIS SAID "the cells above are the whole class" UNTIL THE ADJUDICATION PASS OF 2026-09-23, AND
+	 *  IT WAS MEASURED FALSE: X7 latched every site BEFORE its legal access, so LEGAL x ALL-ZERO x LATCH-CLEAR
+	 *  -- the reset state -- had no row, and five one-conjunct edits to the DIRECTION test (`writeflag ==
+	 *  MEM_READ && d->irq_enable` and its mirrors) passed all 333 rows here and all 37 guest rows
+	 *  (regress/artifacts/fbd5/q2_20260923/Q2.log). ***  The DEPENDS-ON bound these rows use: the predicates
+	 *  dominating each edited decline (case label, direction test, latch), and the lvalues read by BOTH
+	 *  branches under the direction test -- the four interrupt fields and the five latches.  Not in the
+	 *  class: the interrupt output after a LEGAL access except where X9 pins it, any other register's
+	 *  semantics, WIDE DATA on a declined write (data stays 0 / 0x70), joint conjuncts over two fields
+	 *  beyond the three states, and a latch guard conditioned on a field neither branch reads (measured F1:
+	 *  `&& !timer_control[0]` passes every row here; the guest sites probe catches it only because its
+	 *  prologue arms timer 1; table4_20260919).
 	 */
 	{
 		static const struct { uint64_t addr; int wf; const char *nm; } S5[] = {
 			{ IRQ_STATUS, MEM_WRITE, "write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "write IRQ_RAW_STATUS" },
 			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
 			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
-		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[2] = {
-			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" } };
+		/*  #545 adjudication (Fable 5.1, Q2 (e) cell): the byte seeds left bits 8-31 of every field unexercised,
+		    so a decline store or a latch clearer keyed on them passed every row.  "wide" is X8's seeds.  */
+		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[3] = {
+			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
+			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
 		static const int W[3] = { 1, 2, 4 };
 		static const struct { uint64_t addr; int wf; uint64_t data; const char *nm; } LW[8] = {
 			{ IRQ_ENABLE_SET, MEM_WRITE, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, MEM_WRITE, 0x70, "IRQ Set write 0x70" },
@@ -870,7 +884,7 @@
 #define XSAME(x, s) ((x)->irq_status == ST[s].is && (x)->irq_enable == ST[s].ie && (x)->fiq_status == ST[s].fs \
 		&& (x)->fiq_enable == ST[s].fe)
 		for (si = 0; si < 5; si++)
-			for (st = 0; st < 2; st++)
+			for (st = 0; st < 3; st++)
 				for (wi = 0; wi < 3; wi++)
 					for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {
 						x = calloc(1, sizeof(*x)); XSET(x, st);
@@ -891,7 +905,7 @@
 						}
 						free(x);
 					}
-		for (st = 0; st < 2; st++)
+		for (st = 0; st < 3; st++)
 			for (k = 0; k < 8 + 9 * 3; k++) {
 				x = calloc(1, sizeof(*x)); XSET(x, st);
 				for (si = 0; si < 5; si++) {
@@ -948,11 +962,89 @@
 		free(x);
 		fatal_calls = 0;
 	}
-	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (78 P-rows + 222 X-rows).  */
+	/*  X9 (adjudication pass, 2026-09-23 -- Fable 5.1's Q2, MEASURED before this block existed): EVERY LEGAL
+	    ACCESS WITH THE LATCHES STILL CLEAR, from each state.  X7 latched all five sites before its legal access,
+	    so a direction test conjoined with a field that is 0 in the RESET state (`writeflag == MEM_READ &&
+	    d->irq_enable` at IRQ_STATUS, its three read mirrors, `writeflag == MEM_WRITE && d->irq_enable` at
+	    IRQEnableClear) sent the legal access into the decline, which announced a phantom complaint, consumed the
+	    latch and returned 0 -- the right value in that state -- and every row stayed green
+	    (regress/artifacts/fbd5/q2_20260923/Q2.log: 333/333 and 37/37 for all five).  Each cell is ONE row on a
+	    fresh instance: the access returns 1 and announces nothing; a read returns its value over the width and
+	    changes no field; a write sets the enable it targets as written and leaves the other three alone, and IRQ
+	    Set/Clear drive the interrupt output exactly once by (irq_status & the new enable) while FIQ Set/Clear do
+	    not touch it; then the five declines announce EXACTLY 5, because no latch was consumed.  */
+	{
+		static const struct { uint32_t is, ie, fs, fe; const char *nm; } S9[3] = {
+			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
+			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
+		static const struct { uint64_t addr; int wf; } D5[5] = {
+			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
+			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
+		static const struct { uint64_t addr; const char *nm; } R5[5] = {
+			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
+			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQEnable" } };
+		static const struct { uint64_t addr; int fiq, set; uint32_t data; const char *nm; } W8[8] = {
+			{ IRQ_ENABLE_SET, 0, 1, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, 0, 1, 0x70, "IRQ Set write 0x70" },
+			{ IRQ_ENABLE_CLEAR, 0, 0, 0, "IRQ Clear write 0" }, { IRQ_ENABLE_CLEAR, 0, 0, 0x70, "IRQ Clear write 0x70" },
+			{ FIQ_ENABLE_SET, 1, 1, 0, "FIQ Set write 0" }, { FIQ_ENABLE_SET, 1, 1, 0x70, "FIQ Set write 0x70" },
+			{ FIQ_ENABLE_CLEAR, 1, 0, 0, "FIQ Clear write 0" }, { FIQ_ENABLE_CLEAR, 1, 0, 0x70, "FIQ Clear write 0x70" } };
+		static const int W9[3] = { 1, 2, 4 };
+		unsigned char b[8];
+		char xn[200];
+		int st, k, si, a0, d0, rv, ok;
+		struct footbridge_data *x;
+		for (st = 0; st < 3; st++)
+			for (k = 0; k < 5 * 3 + 8; k++) {
+				uint32_t is = S9[st].is, ie = S9[st].ie, fs = S9[st].fs, fe = S9[st].fe;
+				x = calloc(1, sizeof(*x));
+				arm_irqs(x);
+				x->irq.interrupt_assert = noop_assert;
+				x->irq.interrupt_deassert = noop_deassert;
+				x->irq_status = is;  x->irq_enable = ie;  x->fiq_status = fs;  x->fiq_enable = fe;
+				fatal_calls = 0;
+				a0 = irq_asserts;  d0 = irq_deasserts;
+				if (k < 15) {
+					int r = k / 3, w = W9[k % 3];
+					uint64_t want = r == 0 ? (uint64_t) (is & ie) : r == 1 ? (uint64_t) is
+					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
+					want &= w == 4 ? 0xffffffffULL : w == 2 ? 0xffffULL : 0xffULL;
+					memset(b, 0xa5, sizeof(b));
+					rv = dev_footbridge_access(cpu, NULL, R5[r].addr, b, w, MEM_READ, x);
+					ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want
+					    && x->irq_status == is && x->irq_enable == ie && x->fiq_status == fs
+					    && x->fiq_enable == fe && irq_asserts == a0 && irq_deasserts == d0;
+					snprintf(xn, sizeof(xn), "X9 legal len %d read of %s (%s, latches clear)",
+					    w, R5[r].nm, S9[st].nm);
+				} else {
+					int j = k - 15;
+					uint32_t old = W8[j].fiq ? fe : ie;
+					uint32_t ne = W8[j].set ? (old | W8[j].data) : (old & ~W8[j].data);
+					memory_writemax64(cpu, b, 4, W8[j].data);
+					rv = dev_footbridge_access(cpu, NULL, W8[j].addr, b, 4, MEM_WRITE, x);
+					ok = rv == 1 && fatal_calls == 0 && x->irq_status == is && x->fiq_status == fs
+					    && (W8[j].fiq ? (x->fiq_enable == ne && x->irq_enable == ie)
+					                  : (x->irq_enable == ne && x->fiq_enable == fe))
+					    && (W8[j].fiq ? (irq_asserts == a0 && irq_deasserts == d0)
+					        : (is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
+					                    : (irq_asserts == a0 && irq_deasserts == d0 + 1));
+					snprintf(xn, sizeof(xn), "X9 %s (%s, latches clear)", W8[j].nm, S9[st].nm);
+				}
+				for (si = 0; si < 5; si++) {
+					memory_writemax64(cpu, b, 4, 0x70);
+					dev_footbridge_access(cpu, NULL, D5[si].addr, b, 4, D5[si].wf, x);
+				}
+				ok = ok && fatal_calls == 5;
+				check_u(xn, ok, 1);
+				free(x);
+			}
+		fatal_calls = 0;
+	}
+	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (78 P-rows + 222 X-rows); the adjudication
+	    pass, 2026-09-23: 333 -> 491 (X6 +54 and X7 +35 for the wide state, X9 69).  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "333");
+		check("IDENTITY row count -- guards against a stale copy", buf, "491");
 	}
 
 	printf("\n%d rows, %d failures\n", rows, fails);
```

## THE REPAIR DIFF -- regress/gate_offline.sh

```diff
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -585,7 +585,7 @@
     check     "footbridge: row failures" \
               "$(grep -oE '[0-9]+ failures' "$FBLOG" | grep -oE '^[0-9]+')" "0"
     check_min "footbridge: rows actually run" \
-              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 333
+              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 491
     check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
     #  #545: the five declined sites.  P0-P9 pin preservation under a NONZERO seeded status, the read
     #  expressions, the latch per site and byte-first at IRQ_STATUS; X1-X3 (the pass-2 L2 repair) pin
@@ -593,17 +593,21 @@
     #  X4/X5 pin ZERO data / a zero enable as the first access, and a legal zero Clear write.  X6/X7 are
     #  the CLASS CLOSURE (two consecutive passes found cells of one space): every declined access --
     #  site x width x data x state x first/repeat -- keeps every field and the interrupt output and reads
-    #  0; every legal access, from seeded and all-zero state, re-arms no latch.  X8: wide (multi-byte)
-    #  seeds, so a legal read truncated to 8 bits reds.
-    #  Kill tables: regress/artifacts/fbd5/{killtable,xtable,table3,table4}_20260919/.
+    #  0; every legal access, from seeded, all-zero and wide state, re-arms no latch.  X8: wide (multi-byte)
+    #  seeds, so a legal read truncated to 8 bits reds.  X9 (the adjudication pass, 2026-09-23): every LEGAL access
+    #  with the latches still CLEAR, from the seeded, all-zero and wide states -- X7 latched every site first, so
+    #  five one-conjunct edits to the direction test (`writeflag == MEM_READ && d->irq_enable` and mirrors) passed
+    #  every row (q2_20260923/Q2.log); and a WIDE third state in X6/X7, so bits 8-31 of a field are exercised.
+    #  Kill tables: regress/artifacts/fbd5/{killtable,xtable,table3,table4}_20260919/ and q2_20260923/repair/.
     #  COUNTED AS DISTINCT GREEN ROW NAMES, not green lines (adjudication pass, G10): a duplicated green
     #  line cannot stand in for a missing row.  Every row name in the file is unique on the fix.
     fb_distinct() { grep -E "^  ok    $1 " "$FBLOG" | sed -E 's/^  ok    //; s/[[:space:]]+[0-9]+$//' | sort -u | wc -l | tr -d ' '; }
     check "footbridge: #545 P-rows green (P0-P9), distinct names" "$(fb_distinct 'P[0-9]')" "78"
-    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "222"
-    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "108"
-    check "footbridge: #545 X7 every legal access re-arms no latch" "$(fb_distinct 'X7')" "70"
+    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "311"
+    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "162"
+    check "footbridge: #545 X7 every legal access re-arms no latch" "$(fb_distinct 'X7')" "105"
     check "footbridge: #545 X8 wide legal reads keep all 32 bits" "$(fb_distinct 'X8')" "6"
+    check "footbridge: #545 X9 legal access, latches clear, all states" "$(fb_distinct 'X9')" "69"
     #  Name each row that is the SOLE detector of something.
     check "footbridge: the zero-load row is present" \
           "$(grep -c 'load 0 becomes the full 24-bit span' "$FBLOG")" "1"
```

## §E -- QUESTIONS (answer each, numbered)

**Q1 -- premise audit.**  I state these as facts; check each rather than agreeing:
 (a) ACCESS {declined, legal} x STATE {seeded, all-zero, wide} x LATCH {clear, set} at the five sites is
     the whole class under the §C.2 bound, and X6 (declined x both latches), X7 (legal x set) and X9
     (legal x clear) cover it -- walk the predicates that dominate each edited decline in the inlined
     handler and say whether any is missing;
 (b) X9's expectations match the handler: for each of the eight enable writes, work out the resulting
     enable field and whether the handler calls ASSERT or DEASSERT (or neither), from the inlined code, in
     all three states, and compare with the rule the X9 row asserts;
 (c) the wide seeds exercise bits above byte 0 in every one of the four fields, and the masked reads
     (IRQ_STATUS = irq_status & irq_enable; FIQ_STATUS = fiq_status & fiq_enable) are non-zero above byte
     0 in the wide state -- ENUMERATE the four products;
 (d) no pre-repair row changed its meaning (row names are unchanged; X6/X7 only gain cells).
**Q2 -- the smallest change that the 491 rows cannot see.**  Name one change to the five handler arms (or to
the detector) that re-opens what the declines protect -- a legal access treated as a bad one, a bad one
not announced, a field changed, a latch consumed or re-armed -- while every one of the 491 rows stays green,
and name the row you expect to stay green.  (Examples of the SHAPE, not claims: a condition keyed on one
exact field value, on a field bit no state sets, or on a latch belonging to a different site.)
**Q3 -- class or instance.**  Two consecutive passes (§F2, then the adjudication) found cells of one space.
The carrier's rule then owes the CLASS in one diff, with the contract naming what is covered and what is
not.  Does this repair close the class or only the five instances?  Name any cell of site x direction x
width x data x state x latch that is NOT rowed, and say whether it is inside the §C.2 bound.
**Q4 -- records.**  Is any sentence in the added comments (the X9 header, the rewritten X6/X7 CONTRACT, the
gate_offline.sh comment) false as of today, or stale the moment it lands?
**Q5 -- the guest row.**  Is leaving the guest reset-state reads out (§C.4) right, given the offline rows
carry the floor -- or does the guest instrument owe them for a reason the offline rows cannot cover?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
