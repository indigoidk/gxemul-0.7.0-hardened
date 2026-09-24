# #545 (fbdeclinefive) -- THE ADJUDICATION PASS (the panel shares its findings) + THE REPAIR'S OWN PASS 2

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
Check the premises, not just the derivations.  This round's own records were wrong NINE times after pass 2 (listed below),
so a sentence here being confident is not evidence.  **THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**
at HEAD f685d75 plus the uncommitted #545 working set; ignore any other `src/` under the project root.  If you cannot read
files, that is expected: the repair diff and every result are inlined.  Name any premise you cannot settle from the packet.
Ordinary engineering language: declines, latches, detector rows.  **VERDICT LINE FIRST.**

## 1. WHAT HAPPENED SINCE YOU LAST SAW THIS ROUND
Pass 2 (nine seats; Fable HELD by the owner, recorded as held, not failed) reviewed a fix that changes five footbridge
register accesses from ending the process to a declined, once-announced access, plus its detector.  **No seat found a
defect in the product change.**  Two seats found the DETECTOR below the floor:
* the Opus measuring seat MEASURED nine one-edit mutants passing every row (`len == 4` on four of five decline guards; a
  legal read re-arming a latch; a guard widened to swallow a legal narrow read);
* a dedicated codex reading found, against the already-repaired detector: `&& idata` on any latch guard (a zero-data first
  write never announces), `writeflag` rewritten as `!idata`/`idata`, a SEED COLLISION (0x18&0x30 == 0x50&0x30 == 0x10, so
  swapping `irq_status` for `fiq_status` in the IRQ_STATUS read passed), N rows that count texts over the whole arm (two
  sites exchanging texts stayed green), and gate count pins a duplicated green line could satisfy.
The main loop repaired all of it in ONE diff (section 3) and re-measured it (section 4).

## 2. EVERY FINDING AND MY DISPOSITION (full text: P2_FINDINGS.md F1-F50/D1-D10, CODEX_DED_TRIAGE.md R1-R6/W1-W6/D1-D4;
## both are inlined only in summary here -- file-reading seats: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\p2\`)
REPAIRED IN-ROUND (L2 floor / row validity), each re-measured in section 4:
* F1/F20 width at every site -> X1 (len 1 and 2 as the FIRST access, every site); F2 narrowed dominating predicate -> X2;
  F3 legal read re-arms -> X3; F4 re-arm by writes/other registers -> X3 widened; F5 seed collision -> fiq_status 0x60
  (enumerated: only the correct field pair gives 0x10 / 0x40); F6 narrow declined read value -> X1 value rows; F7/R1
  `&& idata`, `&& irq_enable` -> X4 (zero data / zero enable as the first access); R2 `writeflag` -> `!idata`/`idata` -> X4 +
  X5 (a legal ZERO Clear write must not announce); R4 text exchange -> row NO (announces arrive in site order N1..N5);
  F8 floor (b) at every site -> measured (M1, M1b-M1e); F9/F45/F48 gate pins -> distinct-green-id pins, ROWS=37 of 37,
  `count=1 ` with a field boundary; F10 C4 pin added; D2-tightening: pending probes' H1 now requires no prompt ANYWHERE.
CORRECTED IN PLACE (L4): F18/F19 teardown-first claim; F22 pending headers' arm K; F23 FIQ "unpinned everywhere"; F24 S3/E5;
  F25 arms L/T/K; F26 "sibling" read for N4/N5; F27 arm E's zeros; F28 NULL-callback comment; F29 0x70; F30 device comment
  ("no register changes, only this site's warn-once latch is set"); F36 gate display line; F37 send() comment; F38 table
  wording; F31/F32/F33/F39/F40 appended as dated corrections to PRETABLE.out (never edited in place).
  **F34: #539's own record claimed its E0-E6 distinct-GREEN-id gate fix shipped; HEAD never had it (the partial-blob commit
  dropped it).  #545's commit carries it and the CHANGELOG corrects #539's record.**
DISCLOSED, NOT ROWED (contract, clause e): F11 drain/witness legs are not gate-run (their own verdict rows enforce them);
  F12-F17 the legs cannot defend their own predicates (harness edits); M13 teardown-first stays green in all three launchers;
  F41 H1/H2 do not reproduce a device-initiated mid-session exit (none remains reachable except the SDRAM pair);
  F44 the seeds violate 7.3.30's identical-raw-status rule -- synthetic state, by design (the product has no fiq_status
  writer: fiqenableread); F47 arm S loads sp/lr (safe in stepped code); F50 DEVINIT's memset half is not rowed (calloc is).
NOTED, NO ACTION: F35 (a brief citation), F42 (send() now honours 30 s), F43 (the H1 text pin reads the probe's echo --
  it fails closed), F46 (SELFCHECK lines are deliberate), F49 (cosmetic).  Out-of-scope finds already FILED: armdesc3kill,
  armdacr2kill, fbirqsoftunimpl, hygienecensus.
DISAGREEMENTS D1-D10 are in P2_FINDINGS.md; my rulings: D1 L2 (the X-repair shipped); D2/D3 inside the closure (measured
  escape, cheap row); D4 re-seeded; D5 measured at every site; D6 H1/H2 replace the harness-failability property, not the
  old device channel (disclosed); D7 fixed; D8 600f9c4b; D9 policy, :1652 + Figure 7-2 nearest; D10 wrong record, fixed.

## 3. THE REPAIR DIFF -- 22 hunks, from EXACTLY what pass 2 reviewed (HEAD + the pass-2 patches) to the tree now
(md5 da9e8cf1; the gate_arm hunk is its footbridge block only -- the working file also carries an unrelated uncommitted
section from another round, which will not be staged)

```diff
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -572,7 +572,8 @@
 			odata = d->irq_status & d->irq_enable;
 		else if (!d->warned_irq_status_w) {
 			/*  #545: read-only register (7.3.29); the write is
-			    declined -- no state changes -- and announced once.  */
+			    declined -- no register changes, only this site's
+			    warn-once latch is set -- and announced once.  */
 			d->warned_irq_status_w = 1;
 			fatal("[ WARNING: footbridge write to irq status? "
 			    "(once) ]\n");
--- a/regress/diff_footbridge.c
+++ b/regress/diff_footbridge.c
@@ -616,8 +616,12 @@
 	 *  read EXPRESSIONS, the widths, and the latch -- fatal() is a counter here, so the announce
 	 *  is counted, never read (the misname check is the guest rows' job).
 	 *
-	 *  SEEDED BY DIRECT FIELD WRITE, NEVER THROUGH +0x188/+0x18c: this instance's d->irq
-	 *  callbacks are NULL (calloc), and the enable arms call INTERRUPT_ASSERT(d->irq).
+	 *  SEEDED BY DIRECT FIELD WRITE, NEVER THROUGH +0x188/+0x18c.  A bare calloc'd instance has
+	 *  NULL d->irq callbacks and the enable arms call INTERRUPT_ASSERT(d->irq), so this block
+	 *  installs counting no-ops FIRST; the seeds are still written directly, so that no enable-
+	 *  arm assert is mixed into the interrupt-output counts the rows below compare.
+	 *  Seeds (enumerated, pass 2): 0x18/0x30/0x60/0xc0 -- every field-for-field swap in either
+	 *  status expression yields a DIFFERENT value (0x50 collided: 0x50 & 0x30 == 0x18 & 0x30).
 	 *  fiq_status has no writer in the product; seeding it pins the +0x280/+0x284 expressions
 	 *  against a value the product never produces -- a NARROWING of that gap, not its closure.
 	 */
@@ -638,12 +642,12 @@
 		h->irq.interrupt_deassert = noop_deassert;
 		/*  seeds chosen so MASKED != RAW: a dropped `&` (raw returned as status) reds P0  */
 		h->irq_status = 0x18;  h->irq_enable = 0x30;	/*  masked 0x10, raw 0x18  */
-		h->fiq_status = 0x50;  h->fiq_enable = 0xc0;	/*  masked 0x40, raw 0x50  */
+		h->fiq_status = 0x60;  h->fiq_enable = 0xc0;	/*  masked 0x40, raw 0x60  */
 		fatal_calls = 0;	/*  this block counts announces from a clean baseline  */
 #define P_STATE_OK(tag) do { \
 		snprintf(nm2, sizeof(nm2), "%s -- irq_status preserved", tag); check_u(nm2, h->irq_status, 0x18); \
 		snprintf(nm2, sizeof(nm2), "%s -- irq_enable preserved", tag); check_u(nm2, h->irq_enable, 0x30); \
-		snprintf(nm2, sizeof(nm2), "%s -- fiq_status preserved", tag); check_u(nm2, h->fiq_status, 0x50); \
+		snprintf(nm2, sizeof(nm2), "%s -- fiq_status preserved", tag); check_u(nm2, h->fiq_status, 0x60); \
 		snprintf(nm2, sizeof(nm2), "%s -- fiq_enable preserved", tag); check_u(nm2, h->fiq_enable, 0xc0); } while (0)
 #define PN(suffix) (snprintf(nm, sizeof(nm), "%s: %s", dec[i].what, suffix), nm)
 		/*  the legal reads FIRST, on the seeded state: the expressions, not a constant 0  */
@@ -655,12 +659,12 @@
 		dev_footbridge_access(cpu, NULL, FIQ_STATUS, buf, 4, MEM_READ, h);
 		check_u("P0 FIQ_STATUS read = fiq_status & fiq_enable (0x40)", memory_readmax64(cpu, buf, 4), 0x40);
 		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
-		check_u("P0 FIQ_RAW_STATUS read = fiq_status (0x50)", memory_readmax64(cpu, buf, 4), 0x50);
+		check_u("P0 FIQ_RAW_STATUS read = fiq_status (0x60)", memory_readmax64(cpu, buf, 4), 0x60);
 		check_u("P0 the legal reads announce nothing", fatal_calls, 0);
 		for (i = 0; i < 5; i++) {
 			int a0 = irq_asserts, d0 = irq_deasserts, rv;
 			f0 = fatal_calls;
-			memory_writemax64(cpu, buf, 4, 0x70);	/*  a value inside BOTH enables  */
+			memory_writemax64(cpu, buf, 4, 0x70);	/*  bits in BOTH enables: 0x70&0x30=0x30, 0x70&0xc0=0x40  */
 			rv = dev_footbridge_access(cpu, NULL, dec[i].addr, buf, dec[i].len, dec[i].wf, h);
 			check_u(PN("handler returned 1 (declined, not failed)"), rv, 1);
 			check_u(PN("announced exactly once"), fatal_calls - f0, 1);
@@ -685,7 +689,7 @@
 		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 4, MEM_READ, h);
 		check_u("P7 IRQ_STATUS read after the declines (0x10)", memory_readmax64(cpu, buf, 4), 0x10);
 		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
-		check_u("P7 FIQ_RAW_STATUS read after the declines (0x50)", memory_readmax64(cpu, buf, 4), 0x50);
+		check_u("P7 FIQ_RAW_STATUS read after the declines (0x60)", memory_readmax64(cpu, buf, 4), 0x60);
 		/*  a LEGAL EnableClear write still works, next to the declined read of the same address  */
 		memory_writemax64(cpu, buf, 4, 0x10);
 		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, buf, 4, MEM_WRITE, h);
@@ -711,11 +715,119 @@
 		fatal_calls = 0;
 	}
 
-	/*  IDENTITY, as every differential here carries.  #545: 33 -> 111 (78 P-rows).  */
+	/*  #545 pass 2 (L2 floor repair, measured by the Opus seat): the P-rows above pinned width and latch at ONE site
+	    each, so a `len == 4` conjunct on any of the other four decline guards, a legal read that re-arms a latch, and
+	    a decline guard widened to swallow a LEGAL narrow read all passed every row.  X1: every site at len 1 and 2 as
+	    the FIRST access announces once (and the narrow declined read returns 0).  X2: legal narrow reads of the
+	    five readable registers return the low lanes and announce nothing.  X3: legal reads of every sibling at every
+	    width, legal enable writes, and reads of other registers re-arm NO latch.  X4/X5 (pass 2, codex): ZERO data
+	    or a zero enable as the first access still declines AND announces; a legal zero Clear write does not.  */
+	{
+		static const struct { uint64_t addr; int wf; const char *what; } s5[] = {
+			{ IRQ_STATUS, MEM_WRITE, "X1 write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "X1 write IRQ_RAW_STATUS" },
+			{ IRQ_ENABLE_CLEAR, MEM_READ, "X1 read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "X1 write FIQ_STATUS" },
+			{ FIQ_RAW_STATUS, MEM_WRITE, "X1 write FIQ_RAW_STATUS" } };
+		static const struct { uint64_t addr; uint64_t want; const char *what; } rd5[] = {
+			{ IRQ_STATUS, 0x10, "IRQ_STATUS" }, { IRQ_RAW_STATUS, 0x18, "IRQ_RAW_STATUS" },
+			{ FIQ_STATUS, 0x40, "FIQ_STATUS" }, { FIQ_RAW_STATUS, 0x60, "FIQ_RAW_STATUS" },
+			{ IRQ_ENABLE_SET, 0x30, "IRQ_ENABLE_SET" } };
+		unsigned char b[8];
+		char xn[160];
+		int i, w, f0;
+		struct footbridge_data *x;
+#define XSEED(x) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
+		(x)->irq_status = 0x18; (x)->irq_enable = 0x30; (x)->fiq_status = 0x60; (x)->fiq_enable = 0xc0; } while (0)
+		for (w = 1; w <= 2; w++)
+			for (i = 0; i < 5; i++) {
+				x = calloc(1, sizeof(*x)); XSEED(x);
+				fatal_calls = 0;
+				memory_writemax64(cpu, b, w, 0x70);
+				dev_footbridge_access(cpu, NULL, s5[i].addr, b, w, s5[i].wf, x);
+				snprintf(xn, sizeof(xn), "%s: len %d as the FIRST access announces once", s5[i].what, w);
+				check_u(xn, fatal_calls, 1);
+				if (s5[i].wf == MEM_READ) {	/*  the narrow declined read's VALUE (pass 2)  */
+					snprintf(xn, sizeof(xn), "X1 read IRQ_ENABLE_CLEAR: len %d declined read returns 0", w);
+					check_u(xn, memory_readmax64(cpu, b, w), 0);
+				}
+				free(x);
+			}
+		x = calloc(1, sizeof(*x)); XSEED(x);
+		fatal_calls = 0;
+		for (w = 1; w <= 2; w++)
+			for (i = 0; i < 5; i++) {
+				memset(b, 0, sizeof(b));
+				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
+				snprintf(xn, sizeof(xn), "X2 legal len %d read of %s = low lanes", w, rd5[i].what);
+				check_u(xn, memory_readmax64(cpu, b, w), rd5[i].want & (w == 1 ? 0xff : 0xffff));
+			}
+		check_u("X2 the legal narrow reads announce nothing", fatal_calls, 0);
+		for (i = 0; i < 5; i++) {
+			memory_writemax64(cpu, b, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
+		}
+		check_u("X3 the five declines latch (5 announces)", fatal_calls, 5);
+		f0 = fatal_calls;
+		for (w = 1; w <= 4; w *= 2)
+			for (i = 0; i < 5; i++)
+				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
+		for (i = 0; i < 5; i++) {
+			memory_writemax64(cpu, b, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
+		}
+		check_u("X3 legal reads of every sibling re-arm NO latch", fatal_calls - f0, 0);
+		/*  X3, widened (pass 2): legal WRITES to the four enable registers, and reads of registers outside the
+		    five above (VENDOR_ID, TIMER_1_VALUE, the silent FIQEnableClear read), re-arm no latch either.  */
+		f0 = fatal_calls;
+		memory_writemax64(cpu, b, 4, 0);
+		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
+		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
+		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_SET, b, 4, MEM_WRITE, x);
+		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
+		dev_footbridge_access(cpu, NULL, VENDOR_ID, b, 4, MEM_READ, x);
+		dev_footbridge_access(cpu, NULL, TIMER_1_VALUE, b, 4, MEM_READ, x);
+		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_READ, x);
+		for (i = 0; i < 5; i++) {
+			memory_writemax64(cpu, b, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
+		}
+		check_u("X3 legal writes and other-register reads re-arm NO latch", fatal_calls - f0, 0);
+		free(x);
+		/*  X4 (codex, pass 2): the FIRST access carries ZERO -- a zero-data write, or the +0x18c read with
+		    IRQEnable 0.  A latch guard conditioned on the data (`&& idata`) or on irq_enable, or a direction test
+		    rewritten as `!idata`, lets such an access through without an announce; each must announce once and
+		    change no field.  */
+		for (i = 0; i < 5; i++) {
+			x = calloc(1, sizeof(*x)); XSEED(x);
+			if (s5[i].wf == MEM_READ)
+				x->irq_enable = 0;
+			fatal_calls = 0;
+			memory_writemax64(cpu, b, 4, 0);
+			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
+			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable as the FIRST access announces once", s5[i].what + 3);
+			check_u(xn, fatal_calls, 1);
+			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable changes no field", s5[i].what + 3);
+			check_u(xn, (x->irq_status == 0x18) + (x->irq_enable == (s5[i].wf == MEM_READ ? 0u : 0x30u))
+			    + (x->fiq_status == 0x60) + (x->fiq_enable == 0xc0), 4);
+			free(x);
+		}
+		/*  X5 (codex, pass 2): a LEGAL ZERO EnableClear write is a write, not a declined read -- a direction test
+		    rewritten as `idata` sends it to the decline and announces.  */
+		x = calloc(1, sizeof(*x)); XSEED(x);
+		fatal_calls = 0;
+		memory_writemax64(cpu, b, 4, 0);
+		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
+		check_u("X5 a legal ZERO EnableClear write announces nothing", fatal_calls, 0);
+		check_u("X5 ... and leaves IRQEnable at 0x30", x->irq_enable, 0x30);
+#undef XSEED
+		free(x);
+		fatal_calls = 0;
+	}
+
+	/*  IDENTITY, as every differential here carries.  #545: 33 -> 149 (78 P-rows + 38 X-rows).  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "111");
+		check("IDENTITY row count -- guards against a stale copy", buf, "149");
 	}
 
 	printf("\n%d rows, %d failures\n", rows, fails);
--- a/regress/footbridge_sites_probe.py
+++ b/regress/footbridge_sites_probe.py
@@ -67,10 +67,20 @@
      and `dead` IDENTICALLY, and is separated only by exit == 0 and the fresh-reg values --
      a K2 without them goes green exactly when a product fix has FAILED (measured, pass 1).
   Negative controls (PRETABLE, not shipped): omit the `quit` -> the next `reg` succeeds and H2
-  reds; move the teardown ahead of the observation -> H2 must red (it does not observe anything).
+  reds (measured: M12).  NOT COVERED, and measured so (pass 2): moving the teardown AHEAD of the
+  H2 observation keeps H2 GREEN -- close() quits, drains and reaps exit 0, and the later `reg`
+  then fails on the closed descriptor with `dead` set, so the row cannot tell "death noticed
+  mid-session" from "descriptor already closed".  That reorder is a harness edit, not a
+  product one; the same reorder WITHOUT the quit is caught, but only by the exit == 0 clause
+  (the closed pty SIGHUPs the live child).  The two pending probes' legs have the same gap (move
+  s.close() ahead of the next send).  AND THE LEGS CANNOT DEFEND THEIR OWN PREDICATES: dropping
+  dead_before_close or prologue_ok from a row, relaxing exit == 0, reusing the quit's own result as
+  the next send's (quit already observes EOF), or dropping the name from H1's text each leaves a
+  green row that proves less.  Those are harness edits -- reviewed, not rowed.
 
 ARM S (#545) -- the five declined sites in ONE PROCESS.  Each site is accessed TWICE in its
-undefined direction with a LEGAL read of a sibling register between the two, and every access
+undefined direction with a LEGAL read between the two (a sibling register for N1-N3, the SAME
+register's legal read direction for N4/N5), and every access
 must (i) leave the process alive, (ii) leave all five interrupt registers unchanged, and (iii)
 announce EXACTLY ONCE across the whole arm, in the site's own text.  ONE process is the whole
 point: a latch shared between two sites, or one aggregate latch, is INVISIBLE to any design
@@ -88,15 +98,17 @@
      the LAST write of any pair shows here; r1 is A2's register in arm L and is free here).
   N0 the five distinct `(once)` texts each appear exactly once in the arm's diagnostics
      (5 on the fix; 4 under a two-site shared latch; 1 under one aggregate latch -- measured).
-  N1..N5 per-site: the site's own text appears exactly once (ACCESS-LOCAL text, so a misnamed
-     register reds its own row, not a total).
+  N1..N5 per-site: the site's own text appears exactly once.  These are COUNTS over the whole arm,
+     so two sites exchanging texts keeps them all green; row NO binds each text to its access (the
+     announces must arrive in the order N1..N5, the order arm S touches the sites).
   Widths (a byte or halfword decline) are NOT rowed here: a `len == 4` conjunct on the decline
   cannot be seen by a count that another access of the same site already latched.  They are
   rowed OFFLINE in regress/diff_footbridge.c (P-rows), which also pins state PRESERVATION with
   a NONZERO seeded status -- something no stepped guest can reach here (Q2 f).
-  S3 (a legal EnableClear write works, a zero write preserves) is E5's row already.
+  A legal EnableClear write working is E5's row (P = 0x2002) and the differential's P8 (0x10); a
+  legal ZERO Clear write (announces nothing, enable kept) is its X5 -- no guest row writes zero.
 
-ARM E -- #539's ACCEPT rows, in a FOURTH arm so that arms L/T/K are byte-identical to what
+ARM E -- #539's ACCEPT rows, in a FOURTH arm so that arms L/T (and K, until #545 retired it) are byte-identical to what
 they were.  E carries its own C1/A1 (E0 = 0 is also what an ABSENT device returns, so the
 E rows are meaningless unless this arm demonstrably reached the device) and then:
   E0 read IRQEnable before any write            -> 0            (reset value, 7.3.31)
@@ -138,7 +150,8 @@
 host timers are stopped at the prompt; measured with timer 1 armed), so S1/S2/S4/S5/SF1/SF2 pin
 the VALUE 0 and catch a widening (`&` -> `|`, `odata = enable`), never a narrowing -- the offline
 P-rows in diff_footbridge.c seed a nonzero status and pin that; the FIQ read EXPRESSION is
-unpinned everywhere (`fiq_status` has no writer in the tree: `fiqenableread`).  +0x28c
+unpinned by every GUEST row (`fiq_status` has no writer in the tree: `fiqenableread`); the
+differential's P0/X2 pin it only against a SYNTHETIC seeded fiq_status.  +0x28c
 (FIQEnableClear read, the FIQ twin of +0x18c) already declined SILENTLY before #545 and is
 deliberately unchanged -- a read of it returns 0 before and after, so there is no witness;
 it is `fiqenableread` facet (2), where the Opus seat's dissent (fix it in the same commit)
@@ -149,7 +162,7 @@
 `step` and CPSR I/F stay set; it needs a free-running arm with a positive delivery control,
 filed with IRQSoft; (b) +0x189..+0x18b: real hardware selects the same CSR by A[10:2] and
 returns lanes 1-3, the model routes them to `default:` and returns 0 -- a device-wide decode
-deviation, filed, not rowed; (c) irq_status and fiq_enable are 0 throughout, so a mutant
+deviation, filed, not rowed; (c) in arm E, irq_status and fiq_enable are both 0 (arm E sets neither), so a mutant
 returning either at +0x188 is caught by E1/E2 only through the value, not distinguished
 from a constant 0.  (d) D1 compares the disassembly of every STEPPED word; the landing pad is
 planted and never stepped, and a step that ends the process is not compared.  (e) E4 sees only
@@ -305,7 +318,10 @@
     #  as a literal `return wait(mark=_mark, echo=<x> if <x> else None)`, tightened three
     #  times because every looser prefix was a substring of the broken form too.  Written any
     #  other way, a probe is simply not covered by that ratchet -- which is worse than failing
-    #  it.  So timeout goes last, and send() ends on the pinned form.
+    #  it.  So timeout goes last, and send() ends on the pinned form.  (#545: send() now also
+    #  forwards its timeout -- `..., echo=x if x else None, timeout=timeout)`; the census at
+    #  gate_hygiene.sh's conv_mark accepts `,` or `)` after the echo expression, so the forwarded
+    #  form is still counted.  Before #545 this send() silently dropped its timeout argument.)
     def wait(mark=0, echo=None, timeout=60):
         t = time.time()
         while time.time() - t < timeout:
@@ -580,6 +596,18 @@
          "distinct-once=%d fatals=%d exit=%s" % (n0_cnt, len(S["fatals"]), S["exit"]),
          "ok" if n0_ok else "FAIL"))
 results.append(n0_ok)
+#  #545 pass 2 (codex): the N rows count each text over ALL of arm S's diagnostics, so two sites
+#  EXCHANGING their texts keeps every count green.  Arm S touches the sites in the order N1..N5,
+#  so the five announces must arrive in that order -- this binds each text to its own access.
+order = []
+for f in S["fatals"]:
+    hit = [t for t in ("N1", "N2", "N3", "N4", "N5") if TEXTS[t] in f]
+    order.append(hit[0] if len(hit) == 1 else "?")
+no_ok = s_alive and order == ["N1", "N2", "N3", "N4", "N5"]
+print("%-4s %-40s %-30s %s"
+      % ("NO", "the five announces arrive in access order", "order=%s" % (",".join(order) or "-"),
+         "ok" if no_ok else "FAIL"))
+results.append(no_ok)
 
 #  ---- #539: IRQEnable is readable.  Arm E first proves it reached the device (its own C1
 #  and A1: E0 == 0 is ALSO what an absent device returns), then the value rows. ----
--- a/regress/fbpending_drain_probe.py
+++ b/regress/fbpending_drain_probe.py
@@ -61,12 +61,13 @@
   T  negative control: MMU left on, so the footbridge is not mapped.  Must not return
      the device's answers.  (machine_cats.c's boot page tables map only the low 256 MB;
      the footbridge is at PA 0x42000000.)
-  K  failability control: arm D's prologue plus ONE instruction, a read of
-     IRQ_ENABLE_CLEAR (+0x18c, write-only per the DC21285), which dev_footbridge.c's
-     `case IRQ_ENABLE_CLEAR` read branch answers with fatal() then exit(1).  A probe in
-     which nothing can die proves nothing by surviving; K must die WITH its complaint AND
-     exit 1, and every surviving arm must reap exit 0.  #539 moved this from +0x188 (now
-     a readable register); the round that declines +0x18c retires the bridge.
+  H1/H2 harness legs (#545) -- they REPLACED arm K, a read of IRQ_ENABLE_CLEAR (+0x18c) that
+     the device used to answer with fatal() then exit(1); #545 declines it.  H1: an unknown -E
+     name -- no prompt anywhere in the buffer, the diagnostic naming it, exit 1.  H2: arm D's prologue verified (21 steps, r3/r5/r6/r7),
+     a fresh reg, quit, then one more reg that must fail with `dead` set BEFORE close(), exit 0.
+     Every surviving arm must reap exit 0.  NOT COVERED: moving s.close() ahead of that next
+     send keeps H2 green (the send fails on the closed descriptor), and the legs cannot defend
+     their own predicates -- harness edits, reviewed, not rowed (footbridge_sites_probe.py).
 
 Every RAM output word is poisoned with 0xDEADBEEF first and every verdict row requires
 the values it consults to be PRESENT.  Every planted instruction is checked, as it
@@ -615,7 +616,8 @@
     s = Session(emul=H1_NAME)
     prompt = s.wait(timeout=120)
     end = s.close()
-    h1 = dict(prompt=prompt, named=('Sorry, emulation "%s" is unknown' % H1_NAME) in s.buf, **end)
+    h1 = dict(prompt=prompt, noprompt=("GXemul>" not in s.buf),
+              named=('Sorry, emulation "%s" is unknown' % H1_NAME) in s.buf, **end)
     #  H2
     prog = build()
     s = Session()
@@ -738,7 +740,8 @@
         % (len(D.get("badis", [])) + len(X.get("badis", [])) + len(E["badis"]),
            " ".join("0x%x" % a for a in sorted(drain_words - E["covered"])) or "none"))
     row("H1 startup leg: unknown -E named, no prompt, exit 1",
-        H1["prompt"] is False and H1["named"] and H1.get("exit") == 1 and H1.get("signal") is None,
+        H1["prompt"] is False and H1.get("noprompt") is True and H1["named"]
+        and H1.get("exit") == 1 and H1.get("signal") is None,
         "prompt=%s named=%s exit=%s signal=%s" %
         (H1["prompt"], H1["named"], H1.get("exit"), H1.get("signal")))
     row("H2 quit leg: verified prologue, next send dead before close, exit 0",
--- a/regress/fbpending_witness.py
+++ b/regress/fbpending_witness.py
@@ -72,13 +72,13 @@
      against the disassembly the emulator prints as it EXECUTES them, rather than
      against a separate `unassemble` of words that might never run.
   T  negative control.  MMU left on.  Must not return 0x1011 or 0x00345678.
-  K  failability control.  Arm A's prologue plus ONE instruction, a guest read of
-     IRQ_ENABLE_CLEAR (footbridge+0x18c, write-only per the DC21285), which
-     dev_footbridge.c's `case IRQ_ENABLE_CLEAR` read branch answers with fatal() then
-     exit(1).  A probe in which nothing can die proves nothing by surviving; K must
-     kill the host (its complaint AND exit 1) and A must not (exit 0).  #539 moved this
-     from +0x188, which is a documented read-only register and now answers reads; the
-     bridge is retired by the round that declines +0x18c.
+  H1/H2 harness legs (#545) -- they REPLACED arm K, a read of IRQ_ENABLE_CLEAR (+0x18c) that
+     the device used to answer with fatal() then exit(1); #545 declines it.  H1: an unknown -E
+     name -- no prompt anywhere in the buffer, the diagnostic naming it, exit 1.  H2: arm A's prologue verified (18 steps, r3/r5/r6/r7),
+     a fresh reg, quit, then one more reg that must fail with `dead` set BEFORE close(), exit 0.
+     Every surviving arm must reap exit 0.  NOT COVERED: moving s.close() ahead of that next
+     send keeps H2 green (the send fails on the closed descriptor), and the legs cannot defend
+     their own predicates -- harness edits, reviewed, not rowed (footbridge_sites_probe.py).
 
 CONTROLS ARE NOT OPTIONAL AND ABSENT DATA MUST FAIL.  Every RAM word is poisoned with
 0xDEADBEEF before the run, every verdict row first requires the values it consults to be
@@ -495,7 +495,8 @@
     s = Session(emul=H1_NAME)
     prompt = s.wait(timeout=120)
     end = s.close()
-    h1 = dict(prompt=prompt, named=('Sorry, emulation "%s" is unknown' % H1_NAME) in s.buf, **end)
+    h1 = dict(prompt=prompt, noprompt=("GXemul>" not in s.buf),
+              named=('Sorry, emulation "%s" is unknown' % H1_NAME) in s.buf, **end)
     #  H2
     prog = MMU_OFF + prologue(*SENT_A) + [(0x48, NOP, NOPTXT, "landing pad")]
     s = Session()
@@ -659,7 +660,8 @@
         "%d mismatches, %d/%d offsets stepped"
         % (len(E["badis"]), len(E["covered"]), len(E["want"])))
     row("H1 startup leg: unknown -E named, no prompt, exit 1",
-        H1["prompt"] is False and H1["named"] and H1.get("exit") == 1 and H1.get("signal") is None,
+        H1["prompt"] is False and H1.get("noprompt") is True and H1["named"]
+        and H1.get("exit") == 1 and H1.get("signal") is None,
         "prompt=%s named=%s exit=%s signal=%s" %
         (H1["prompt"], H1["named"], H1.get("exit"), H1.get("signal")))
     row("H2 quit leg: verified prologue, next send dead before close, exit 0",
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -585,8 +585,17 @@
     check     "footbridge: row failures" \
               "$(grep -oE '[0-9]+ failures' "$FBLOG" | grep -oE '^[0-9]+')" "0"
     check_min "footbridge: rows actually run" \
-              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 33
+              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 149
     check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
+    #  #545: the five declined sites.  P0-P9 pin preservation under a NONZERO seeded status, the read
+    #  expressions, the latch per site and byte-first at IRQ_STATUS; X1-X3 (the pass-2 L2 repair) pin
+    #  byte/halfword-first at EVERY site, narrow legal reads, and that no legal access re-arms a latch;
+    #  X4/X5 pin ZERO data / a zero enable as the first access, and a legal zero Clear write.
+    #  Kill table: regress/artifacts/fbd5/{killtable,xtable}_20260919/.  Counted over GREEN lines.
+    check "footbridge: #545 P-rows green (P0-P9)" \
+          "$(grep -cE '^  ok    P[0-9] ' "$FBLOG")" "78"
+    check "footbridge: #545 X-rows green (X1-X5, the width/latch/zero-data closure)" \
+          "$(grep -cE '^  ok    X[1-5] ' "$FBLOG")" "38"
     #  Name each row that is the SOLE detector of something.
     check "footbridge: the zero-load row is present" \
           "$(grep -c 'load 0 becomes the full 24-bit span' "$FBLOG")" "1"
--- a/regress/gate_arm.sh (footbridge block)
+++ b/regress/gate_arm.sh (footbridge block)
@@ -1,6 +1,6 @@
 FBLOG=$LOGDIR/footbridge_sites.log
 python3 footbridge_sites_probe.py "$PMAX" "$STUB" > "$FBLOG" 2>&1 || true
-grep -E "^(  arm |C[0-9]|A[0-9]|I1|K1|D1|E(C1|A1|[0-6]) )" "$FBLOG" | sed 's/^/       /'
+grep -E "^(  arm |C[0-9]|A[0-9]|I1|H[12]|D1|E(C1|A1|[0-6])|S(C1|A1|[1-5]|F[12])|N[0-5O]) " "$FBLOG" | sed 's/^/       /'
 
 if ! grep -q "FOOTBRIDGE_SITES_" "$FBLOG"; then
     note "footbridge probe produced no verdict; last lines follow"
@@ -39,24 +39,32 @@
     check "footbridge: H2 quit leg green (prologue verified, dead, exit 0)" \
           "$(grep -cE '^H2 .*prologue=True next=False dead=True exit=0 .*ok$' "$FBLOG")" "1"
     #  #545: the five declined sites, ONE process (arm S).  N0 counts five DISTINCT once-announces
-    #  (a shared or aggregate latch reads 4 or 1); N1-N5 are per-site and access-local; S1-S5 and
-    #  SF1/SF2 pin every interrupt register unchanged through the declines, with the FINAL raw
-    #  reads after the last write of every pair.
-    check "footbridge: arm S controls (SC1 liveness, SA1 vendor) green" \
-          "$(grep -cE '^S(C1|A1) .*ok$' "$FBLOG")" "2"
+    #  (a shared or aggregate latch reads 4 or 1); N1-N5 count each site's text over the whole arm and NO
+    #  binds each text to its access (the announces arrive in site order); S1-S5 and SF1/SF2 pin every
+    #  interrupt register unchanged through the declines, with the FINAL raw reads after the last write
+    #  of every pair.  Every family is pinned by its DISTINCT green ids (a duplicated green line cannot
+    #  stand in for a missing id -- pass 2), and the probe's own total by ROWS=.
+    check "footbridge: the sites probe ran all 37 rows green (ROWS=37 of 37)" \
+          "$(grep -cE '^ROWS=37 of 37$' "$FBLOG")" "1"
+    check "footbridge: arm S controls SC1, SA1 -- two DISTINCT green ids" \
+          "$(grep -E '^S(C1|A1) .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "2"
     check "footbridge: N0 five sites, one process, five distinct once" \
           "$(grep -cE '^N0 .*distinct-once=5 fatals=5 exit=0 .*ok$' "$FBLOG")" "1"
+    check "footbridge: NO the five announces arrive in access order" \
+          "$(grep -cE '^NO .*order=N1,N2,N3,N4,N5 .*ok$' "$FBLOG")" "1"
     check "footbridge: N1-N5 each announced exactly once (count=1)" \
-          "$(grep -cE '^N[1-5] .*count=1.*ok$' "$FBLOG")" "5"
+          "$(grep -cE '^N[1-5] .*count=1 .*ok$' "$FBLOG")" "5"
     check "footbridge: N1-N5 are five DISTINCT green row ids" \
-          "$(grep -oE '^N[1-5] .*ok$' "$FBLOG" | cut -c1-2 | sort -u | wc -l)" "5"
-    check "footbridge: S1-S5 the legal reads between the declines" \
-          "$(grep -cE '^S[1-5] .*ok$' "$FBLOG")" "5"
+          "$(grep -E '^N[1-5] .*count=1 .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "5"
+    check "footbridge: S1-S5 the legal reads between the declines -- five DISTINCT green ids" \
+          "$(grep -E '^S[1-5] .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "5"
     check "footbridge: S3 IRQEnable intact at 0x30 through the declines" \
           "$(grep -cE '^S3 .*got=0x00000030 .*ok$' "$FBLOG")" "1"
-    check "footbridge: SF1/SF2 final raw status reads after every decline" \
-          "$(grep -cE '^SF[12] .*got=0x00000000 .*ok$' "$FBLOG")" "2"
+    check "footbridge: SF1/SF2 final raw status reads -- two DISTINCT green ids, both 0" \
+          "$(grep -E '^SF[12] .*got=0x00000000 .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "2"
     #  #545: the corrected controls -- C4 now requires the key present; C5 requires arm T's exit 0.
+    check "footbridge: C4 the MMU-on arm cannot see the device (key present)" \
+          "$(grep -cE '^C4 .*ok$' "$FBLOG")" "1"
     check "footbridge: C5 the MMU-on control arm survives, exit 0" \
           "$(grep -cE '^C5 .*ok$' "$FBLOG")" "1"
     #  #539: IRQEnable (+0x188) is readable -- reset 0, Set ORs, Clear clears, byte and
@@ -65,9 +73,11 @@
     check "footbridge: IRQEnable ACCEPT rows E0-E6 all green" \
           "$(grep -cE '^E[0-6] .*ok$' "$FBLOG")" "7"
     #  Seven green lines are not seven rows: a duplicated id could stand in for a missing one, so
-    #  the DISTINCT ids are counted too (with the count above, each E0-E6 appears exactly once).
-    check "footbridge: E0-E6 are seven DISTINCT row ids" \
-          "$(grep -oE '^E[0-6] ' "$FBLOG" | sort -u | wc -l | tr -d ' ')" "7"
+    #  the DISTINCT ids are counted OVER THE GREEN LINES -- seven distinct green ids proves
+    #  "each of E0-E6 is green" by itself (fable5, #539 F2: counting ids over all lines would
+    #  pass a duplicated green E2 beside a red E3).
+    check "footbridge: E0-E6 are seven DISTINCT green row ids" \
+          "$(grep -E '^E[0-6] .*ok$' "$FBLOG" | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')" "7"
     check "footbridge: IRQEnable reads 0 at reset (E0)" \
           "$(grep -cE '^E0 .*got=0x00000000 .*ok$' "$FBLOG")" "1"
     check "footbridge: Set ORs (E2 = P|Q; Clear is pinned by E5)" \
```

## 4. THE MEASUREMENTS (table 3, scratch trees only; logs durable in regress/artifacts/fbd5/table3_20260919/)
Offline differential, 149 rows, against FIX and 34 mutants: FIX 149/149; EVERY mutant red except M9 and Z9, which change
only an announce TEXT and are guest-only by design (the differential's fatal() is a counter).
Guest (sites probe 37 rows + the two pending probes), in a clone of build/: FIX 37/37 PASS, witness and drain H1/H2/R0 ok;
Z9 (IRQ_STATUS and IRQ_RAW_STATUS exchange texts) red on NO only; M1b-M1e (exit(1) reinstated at each other site) 21/37 --
arm S dies.  gate_offline PASS 348 on the repaired tree (pins 149/78/38).  gate_arm on the repaired gate file: NOT YET
RUN (it runs alone after this pass).  The sites probe's send() comment changed after table 3 (text only).

TABLE3_START 2026-09-19 12:48:18  SEC dev_footbridge.c md5 783c0c7f
OFF FIX  rc=0 149 rows, 0 failures     red: 
OFF M1   rc=1                          red: 
OFF M2   rc=1 149 rows, 6 failures     red: P1 write IRQ_STA,P6 five sites an,P8 ... announced,X3 legal reads o,X3 legal writes ,
OFF M3   rc=1 149 rows, 4 failures     red: P2 write IRQ_RAW,P6 five sites an,P8 ... announced,X3 the five decl,
OFF M4   rc=1 149 rows, 4 failures     red: P5 write FIQ_RAW,P6 five sites an,P8 ... announced,X3 the five decl,
OFF M5   rc=1 149 rows, 3 failures     red: P3 read IRQ_ENAB,X1 read IRQ_ENAB,
OFF M6   rc=1 149 rows, 13 failures    red: P1 write IRQ_STA,P2 write IRQ_RAW,P3 read IRQ_ENAB,P4 write FIQ_STA,P5 write FIQ_RAW,P7 IRQ_STATUS re,P9 ... and store,X
OFF M7   rc=1 149 rows, 4 failures     red: P0 IRQ_STATUS re,P7 IRQ_STATUS re,X2 legal len 1 r,X2 legal len 2 r,
OFF M8   rc=1 149 rows, 3 failures     red: P0 FIQ_STATUS re,X2 legal len 1 r,X2 legal len 2 r,
OFF M9   rc=0 149 rows, 0 failures     red: 
OFF M10  rc=1 149 rows, 6 failures     red: P3 read IRQ_ENAB,P6 five sites an,P8 ... announced,X3 legal reads o,X3 legal writes ,
OFF M11  rc=1 149 rows, 3 failures     red: P9 a BYTE write ,X1 write IRQ_STA,
OFF A1   rc=1 149 rows, 2 failures     red: X1 write FIQ_RAW,
OFF A2   rc=1 149 rows, 2 failures     red: X1 read IRQ_ENAB,
OFF A3   rc=1 149 rows, 2 failures     red: X1 write IRQ_RAW,
OFF A4   rc=1 149 rows, 2 failures     red: X1 write FIQ_STA,
OFF B1   rc=1 149 rows, 1 failures     red: X3 legal reads o,
OFF B2   rc=1 149 rows, 1 failures     red: X3 legal reads o,
OFF B3   rc=1 149 rows, 1 failures     red: X3 legal reads o,
OFF G1   rc=1 149 rows, 3 failures     red: X2 legal len 1 r,X2 legal len 2 r,X2 the legal nar,
OFF G2   rc=1 149 rows, 3 failures     red: X2 legal len 1 r,X2 legal len 2 r,X2 the legal nar,
OFF Z1   rc=1 149 rows, 1 failures     red: X4 write IRQ_STA,
OFF Z1b  rc=1 149 rows, 1 failures     red: X4 write FIQ_RAW,
OFF Z2   rc=1 149 rows, 1 failures     red: X4 read IRQ_ENAB,
OFF Z3   rc=1 149 rows, 1 failures     red: X4 write IRQ_STA,
OFF Z4   rc=1 149 rows, 1 failures     red: X5 a legal ZERO ,
OFF Z5   rc=1 149 rows, 4 failures     red: P0 IRQ_STATUS re,P7 IRQ_STATUS re,X2 legal len 1 r,X2 legal len 2 r,
OFF Z6   rc=1 149 rows, 4 failures     red: P0 IRQ_STATUS re,P7 IRQ_STATUS re,X2 legal len 1 r,X2 legal len 2 r,
OFF Z7   rc=1 149 rows, 1 failures     red: X3 legal writes ,
OFF Z7b  rc=1 149 rows, 1 failures     red: X3 legal writes ,
OFF Z8   rc=1 149 rows, 2 failures     red: X1 read IRQ_ENAB,
OFF Z9   rc=0 149 rows, 0 failures     red: 
OFF M1b  rc=1                          red: 
OFF M1c  rc=1                          red: 
OFF M1d  rc=1                          red: 
OFF M1e  rc=1                          red: 
A RESTORED (cmp == SEC), sentinel cleared
BUILD_FIX rc=0 FRESH 9fa0c1f9
SITES FIX  ROWS=37 of 37 FOOTBRIDGE_SITES_PASS   red: 
TABLE3B_START (guest half, re-run after the 12:53 stop) 2026-09-19 13:00:40  SEC dev_footbridge.c md5 783c0c7f
BUILD_FIX rc=0 FRESH 9fa0c1f9
SITES FIX  ROWS=37 of 37 FOOTBRIDGE_SITES_PASS   red: 
WITNESS FIX rc=0 ok:R0 ok:H1 ok:H2  FBPENDING_VERDICT=PASS
DRAIN FIX rc=0 ok:R0 ok:H1 ok:H2  FBDRAIN_VERDICT=REPORT-ONLY
BUILD_Z9 rc=0 FRESH ec3cc0c6
SITES Z9   ROWS=36 of 37 FOOTBRIDGE_SITES_FAIL   red: NO,
BUILD_M1b rc=0 FRESH e296f72c
SITES M1b  ROWS=21 of 37 FOOTBRIDGE_SITES_FAIL   red: SC1,SA1,S1,S2,S3,S4,S5,SF1,SF2,N1,N2,N3,N4,N5,N0,NO,
BUILD_M1c rc=0 FRESH 5cc6102d
SITES M1c  ROWS=21 of 37 FOOTBRIDGE_SITES_FAIL   red: SC1,SA1,S1,S2,S3,S4,S5,SF1,SF2,N1,N2,N3,N4,N5,N0,NO,
BUILD_M1d rc=0 FRESH ec1e8ad7
SITES M1d  ROWS=21 of 37 FOOTBRIDGE_SITES_FAIL   red: SC1,SA1,S1,S2,S3,S4,S5,SF1,SF2,N1,N2,N3,N4,N5,N0,NO,
BUILD_M1e rc=0 FRESH 8085c785
SITES M1e  ROWS=21 of 37 FOOTBRIDGE_SITES_FAIL   red: SC1,SA1,S1,S2,S3,S4,S5,SF1,SF2,N1,N2,N3,N4,N5,N0,NO,
BUILD_RESTORED rc=0 FRESH 9fa0c1f9
B RESTORED (cmp == SEC, binary fresh), sentinel cleared
TABLE3B_DONE 2026-09-19 13:03:37

## 5. QUESTIONS
Q1 ADJUDICATE F1-F50 / D1-D10 / R1-R6 as disposed in section 2 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each
   for any you would change (silence = uphold).  **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted essentially
   every finding and repaired or disclosed all of them; that is a suspicious number, and agreement is not evidence.
Q2 THE REPAIR'S OWN FLOOR, on the SHIPPED COMPOSITE (guest rows + differential + gate pins): name the smallest edit to the
   FIXED device source that passes all of it now, and the row you expected to catch it.  Candidates I did NOT build: a
   latch guard conditioned on a register field NOT seeded nonzero in X4; a decline that changes the INTERRUPT OUTPUT on a
   repeated or narrow access (only the first word decline counts asserts); a legal Set/Clear write that re-arms a latch
   only when its data is NONZERO (X3's widened writes carry 0).
Q3 THE ROWS AND PINS I ADDED: can any of X1-X5, NO, or the new gate pins pass while the thing it names is false?  (The
   earlier pins failed that test; mine were written the same day.)
Q4 WHAT DID ALL NINE OF US MISS?  Standing licence: anything else you found while verifying.
End with a seat record: model, files read, nothing run / what you ran.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
