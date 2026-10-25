# Reading task: F2C_PACKET_A (Gemini web; 2026-10-25)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-T19F2CA-183d` on a line of its own.

# F2c -- THE INSTRUMENT REPAIR'S OWN PASS, research item T19, ledger row `i8259eoiirr` (#574) -- GXemul hardened fork

Written 2026-10-25 by the main loop.  The pass-2 adjudication (F2b, six RATIFY WITH CHANGES) left the PRODUCT diff unchanged
and raised six unrowed cells of the fix's own predicates in the DETECTOR.  By the repair-chain rule a repair made in response
to a pass owes its own pass, scoped to the repair's diff, closing on the first pass that finds ZERO floor breaches -- with
the denominator stated.  **This pass reviews the instrument diff v2d -> v2e ONLY.**  The product diff (`dev_8259.c`,
`dev_gt.c`, `devices.h`) is the one pass 2 and F2b reviewed and is not re-litigated here; the tree is `GXEMUL-SEC/src/` at
HEAD `fa66b70d` (the three product files unchanged since `94b247db`); the fix lives only in the scratch clone `/tmp/gxt19/fix`.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Every candidate cell F2b named was MEASURED as a mutant against the v2d instrument BEFORE the repair (section 3.1), the
repair was then re-pinned on unmodified HEAD, re-measured on both legs and the floor legs (3.2), and the WHOLE table of
record re-run on the repaired instrument (3.3).  **Check the premises, not just the derivations**: a row's CHANNEL claim
(the mutant it kills, the observable that differs) is a construction claim -- say whether each new row is valid by
construction, and whether any row is vacuous.  **VERDICT LINE FIRST.**

**Self-review disclosed.**  Every seat here raised cells that this diff rows: be HARDER on the rows that answer your own
finding than on the others, and check that the ROW is right, not merely that the cell was.

**You cannot read files; every fact this pass depends on is inlined -- name any premise you cannot settle rather than guessing.**

**The roster for this pass:** GPT-6 Astra (ADJUDICATES -- its answer is the ruling of record, provisional until the roster
completes), Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: part A = the instrument diff and its measurements, Q1;
part B = the F2b dispositions, Q2/Q3), Gemini 4 Argon (web route, QUEUED behind the single sender).  Fable 5.1 HELD (its
question is recorded); kimi, minimax and the Opus seat deliberately not fired; agy quota-walled.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
BREACHES: <the floor breaches you find in the v2e instrument, with the mutant shape and the row that should catch it, or "zero -- denominator: <the cells you swept>">
~~~~

---

## 1. The repair, in one paragraph

v2e adds two sessions and six rows and relabels nine.  `maskeoi`: line 4 acknowledged (poll), THEN masked (OCW1 0x10), then
the specific EOI 0x64 -- `maskeoi isr` wants ISR 0x00 in both columns (the fix's ISR branch; HEAD never sets ISR), and the
F2b mutant `D_eoi_maskcond` (the ISR branch conditioned on the line being unmasked) leaves 0x10.  `speceoi`: both UARTs
acknowledged (ISR 0x18, `spec isr both` 0x00/0x18), the specific EOI 0x63 -- `spec eoi one` wants 0x10 (FIX) / 0x00 (HEAD);
`B_spec_isr0` (the arm clearing the whole ISR) reads 0x00.  In `nonspec`, between the two polls: `mfc0 s3,cause` --
`nonspec ip2` wants Cause bit 10 = 1 in both columns (the acknowledge of line 3 recomputes with line 4 pending; `D_deassert`
reads 0), and a command-port read WITHOUT another OCW3 -- `poll once2` wants the IRR 0x10 (FIX: the latch reverted after a
SUCCESSFUL poll) / 0x83 (HEAD's unconsumed poll byte); `D_latch_cond` (revert only after an unsuccessful poll) reads 0x84.
In `quiet`: a GT IACK read with nothing pending -- `quiet iack` wants last_int 0 in both columns; `D_gt_always` reads
0xffffffff.  In `gt`: a WRITE to the IACK register before the read -- `gt write isr` wants ISR 0x00 both; `D_gt_write` (the
read-only guard dropped) reads 0x10.  The both-columns DEVICE values (poll bytes, IACK values) are CONTRACT rows from v2e
on, not controls -- a mutant that reds one is a KILL, not an instrument failure.  101 rows in 14 sessions, 26 of
them symptom rows.  The SHIPPED revision is v2f: v2e with `spec polls` relabelled a SYMPTOM row after v2e's own L0 leg showed
its columns differ (HEAD 0x8383 -- its second poll re-reports line 3 -- vs FIX 0x8384); no other change, every measurement
below is of v2f, and v2e's cycle artifacts stand as history.  NOT rowed, disclosed: the retire guard's two conjuncts (`D_retire_anypic`, `D_retire_anyline`: a wrong
extra retirement is observable only with a pending count >= 2, which only host time produces -- filed `pit8253retireguard`
with the band-row construction) and the two-SLAVE-request stall (`D_fold`: the owed `i8259cascline` row; `nonspec ip2` sees
only the master-side recompute).

## 2. THE INSTRUMENT DIFF -- the banked frozen v2d copy -> the banked frozen v2e copy, every hunk INLINED

```diff
--- C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_090053/i8259_eoi_probe.frozen.py.txt	2026-10-25 09:06:04.207328700 -0500
+++ C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_114055/i8259_eoi_probe.frozen.py.txt	2026-10-25 11:46:59.240866700 -0500
@@ -23,14 +23,18 @@
 `eoi x8` as SYMPTOM rows wanting the request bit KEPT after an un-acknowledged EOI.  Under (G') an EOI with no
 preceding acknowledge keeps the legacy consume, so those two rows are RE-PINNED here as the CONTRACT row `eoi noack`
 (both columns 0); the symptom rows are the ACKNOWLEDGE rows below.  Each revision of this probe is run on the
-UNMODIFIED HEAD clone first (HEAD column: witness_20261025b/ for v2, witness_20261025c/ for v2d) and the pre-fix build
+UNMODIFIED HEAD clone first (HEAD column: witness_20261025b/ for v2, witness_20261025c/ for v2d, witness_20261025d/ for
+v2e) and the pre-fix build
 is measured RED against the FIX column (the L0 leg) before any fix measurement is trusted.  Honest order note: the fix
 clone was built (07:56) before the re-pinned probe first ran on HEAD (08:01); what precedes every fix MEASUREMENT is
 the HEAD run, not the code change.  The pass-1 witness ran at 06:51 (WSL clock; witness_20261025/RESULTS_base.txt).
 
 ROWS (kinds: control = the instrument's own liveness/signature; contract = pinned either way; symptom = HEAD red /
-FIX green; the rate row is a BAND):
-  quiet    nothing pending: IRR 0, ISR 0, poll byte 0x00, IMR 0.
+FIX green; the rate row is a BAND.  v2e relabelled the both-columns DEVICE values -- the poll bytes and the IACK
+values -- from control to contract: a model value pinned either way is a contract about the model, not an
+instrument control, and a mutant that reds one is KILLED, not an instrument failure (F2b, four seats)):
+  quiet    nothing pending: IRR 0, ISR 0, poll byte 0x00, IMR 0; the GT IACK read returns last_int 0 in both columns
+           (`quiet iack`, v2e: a read that handed back the acknowledge's -1 would read 0xffffffff).
   level    the ISA ns16550 (IRQ 4) level: IRR bit 4 set; ISR 0; `eoi noack` (EOI 0x64 with no acknowledge) leaves
            IRR bit 4 CLEAR in both columns (the legacy consume, see above); the level re-asserts within a tick.
   ack      the SYMPTOM core: OCW3 poll + read -> byte 0x84 (both); then ISR reads 0x10 (FIX) / 0x00 (HEAD); IRR bit 4
@@ -47,7 +51,14 @@
            under the mask, returns the IRR 0x10 (FIX: the poll is one-shot) where a sticky poll would return 0x00 and
            HEAD returns 0x84 (`poll once`); masking leaves IRR; an un-acknowledged EOI while masked consumes
            (contract, both 0).
-  gtboth   the GT IACK read with the UART (IRQ 4) AND the RTC (IRQ 8) pending: FIX returns 8 (the cascade, line 2,
+  maskeoi  v2e (F2b): line 4 ACKNOWLEDGED (poll 0x84), THEN masked (OCW1 0x10), then the specific EOI 0x64 -- Linux's
+           mask-then-EOI order: ISR reads 0x00 in both columns (FIX: the ISR branch clears the bit; HEAD never set it);
+           an EOI that takes the legacy branch for a masked in-service line leaves 0x10 (`maskeoi isr`).
+  speceoi  v2e (F2b): both UARTs acknowledged by two polls (`spec polls`, the two poll bytes: FIX 0x83 then 0x84; HEAD
+           0x83 twice, its first poll having consumed nothing -- a symptom row, the nonspec session's `poll second` fact),
+           ISR 0x18 (`spec isr both`), then the SPECIFIC EOI 0x63: ISR loses exactly bit 3 (`spec eoi one` FIX 0x10 /
+           HEAD 0x00 -- a specific EOI clearing the whole ISR reads 0x00); then 0x64 clears the rest (0x00 both).
+  gtboth  the GT IACK read with the UART (IRQ 4) AND the RTC (IRQ 8) pending: FIX returns 8 (the cascade, line 2,
            outranks line 4; then the slave's line 0) and sets master ISR bit 2 and slave ISR bit 0; HEAD returns its
            last_int 4 (bus_isa's flat scan skips line 2) and sets nothing -- the row that pins the returned line.
   NOTE on `nonspec`: the second poll acknowledges IRQ 4 while IRQ 3 is in service because the model has no priority
@@ -56,13 +67,18 @@
   round-trip and the device-signature rows carry that.
   nonspec  both UARTs pending: two polls acknowledge 3 then 4 (HEAD's second poll returns 3 again); ISR 0x18 (FIX);
            the non-specific EOI 0x20 resets the LOWEST set ISR bit (FIX 0x10; HEAD 0x00 -- never set); a second 0x20
-           resets the other (0x00 both).
+           resets the other (0x00 both).  Between the two polls (v2e, F2b): a CP0 Cause read -- IP2 still asserted in
+           both columns (`nonspec ip2`: the acknowledge's recompute sees line 4 pending; a bare DEASSERT would drop the
+           CPU line) -- and a command-port read WITHOUT another OCW3 (`poll once2`: FIX returns the IRR 0x10, the latch
+           having reverted after a SUCCESSFUL poll; HEAD returns its unconsumed poll byte 0x83; a latch that reverts
+           only after an unsuccessful poll returns 0x84).
   casc     the mc146818 periodic interrupt (IRQ 8, on pic2) after a long wait: the master poll returns 0x82 and sets
            master ISR bit 2 (FIX), the slave poll returns 0x80 and sets slave ISR bit 0 (FIX); the two specific EOIs
            (0x60 to the slave, 0x62 to the master) clear both.
   pit      8253 counter 0 at 291 Hz after a long wait: IRR bit 0 = 1; the poll returns 0x80 and (FIX) clears the bit.
-  gt       the GT64120 IACK read (KSEG1 0xbbe00c34) with the UART level on: returns 4 in both columns; FIX sets ISR
-           bit 4 and clears IRR bit 4 (HEAD: ISR 0, IRR 1).
+  gt       the GT64120 IACK register (KSEG1 0xbbe00c34) with the UART level on: a WRITE to it first (v2e) acknowledges
+           nothing (`gt write isr` 0x00 in both columns: HEAD's write arm is a no-op, the fix's guard is MEM_READ); the
+           READ returns 4 in both columns; FIX sets ISR bit 4 and clears IRR bit 4 (HEAD: ISR 0, IRR 1).
   gtcasc   the GT IACK read with the mc146818 periodic interrupt pending on pic2: returns 8 in both columns; FIX
            acknowledges the master's cascade line (ISR 0x04) and the slave's line 0 (ISR 0x01); the two EOIs clear both.
   rate     IRQ 0 DELIVERIES counted by a guest handler at the general exception vector (poll + specific EOI) over 180M
@@ -74,12 +90,23 @@
 read that acknowledges nothing (`gt isr`, `gt irr4`) or returns the legacy line instead of the acknowledged one
 (`gtboth iack`), an acknowledge that does not retire the 8253's event (`rate
 storm`/`rate band`), a cascade acknowledge that strands or skips the slave (`casc isr2`, `casc isr8`), a non-specific
-EOI that clears every ISR bit (`nonspec lowest`).  OUTSIDE: the `default` read arm (byte-identical to HEAD), priority
-inhibition by ISR (not modelled; filed i8259priority), level-triggered mode (ICW1 LTIM; filed i8259ltim), the PReP
-and footbridge vector reads (filed isaiackreaders), the OCW2 bytes that stop the emulation (filed i8259cmdhalt), an
-8253 count of zero (filed pit8253count0), the spurious IACK with nothing pending (returns last_int, as HEAD).
-A held level re-requests after the acknowledge within one tick (the model's devices re-assert every tick while a
-condition holds) -- more generous than edge-mode hardware, never less; disclosed, not rowed.
+EOI that clears every ISR bit (`nonspec lowest`); and, from the pass-2 adjudication (v2e): a latch that reverts only
+after an UNSUCCESSFUL poll (`poll once2`), a specific EOI that takes the legacy branch for a MASKED in-service line
+(`maskeoi isr`), a specific EOI that clears more than its own ISR bit (`spec eoi one`), an acknowledge whose recompute
+drops the CPU line while another request is pending (`nonspec ip2`), a GT WRITE that acknowledges (`gt write isr`),
+a GT read that returns the acknowledge's -1 with nothing pending (`quiet iack`).  OUTSIDE: the `default` read arm
+(byte-identical to HEAD), priority inhibition by ISR (not modelled; filed i8259priority), level-triggered mode (ICW1
+LTIM; filed i8259ltim), special mask mode (OCW3 0x68, an empty arm; filed i8259smm), the PReP and footbridge vector
+reads (filed isaiackreaders), the OCW2 bytes that stop the emulation (filed i8259cmdhalt), an 8253 count of zero (filed
+pit8253count0), the one-shot latch's revert target (the IRR, not the last RR/RIS selection; filed i8259ocw3revert), the
+two-SLAVE-request CPU-line case (a manual cascade pre-fold strands the second request; owed as i8259cascline -- the
+`nonspec ip2` row sees only the master-side recompute), and the retire guard's two conjuncts (a slave line-0 or a
+non-zero-line acknowledge retiring an 8253 event is observable only with a pending count >= 2, which only host time
+produces; disclosed, the band-row construction filed as pit8253retireguard).  The spurious IACK with nothing pending
+returns last_int as HEAD did (`quiet iack` pins it).
+A held level re-requests after the acknowledge within one tick (the ns16550 and the 8253 -- the sources these rows
+drive -- re-assert on every tick while their condition holds; the pckbc does NOT: it suppresses repeated assertions while
+already asserted, dev_pckbc.c, F2b) -- more generous than edge-mode hardware for those two, never less; disclosed, not rowed.
 
 CONTROLS: every emitted WORD of every guest program is checked against the emulator's own disassembler (CONTROL 0);
 each session parks at its halt breakpoint with the pc verified; a RAM round-trip through the same store/load shapes
@@ -201,6 +228,18 @@
     return 0x40800000 | (rt << 16) | (rd << 11)
 
 
+def mfc0(rt, rd):
+    return 0x40000000 | (rt << 16) | (rd << 11)
+
+
+def sw(rt, off, base):
+    return I(0x2b, base, rt, off)
+
+
+COP0_CAUSE = 13
+CAUSE_IP2 = 10                      # Cause bit 10 = IP2: the ISA bus's CPU line (cpu[N].2; cpu_mips.c sets 1 << (8 + 2))
+
+
 ERET = 0x42000018
 NOP = 0
 prog = []
@@ -288,14 +327,18 @@
 
 
 def build_quiet():
+    """Nothing pending: every register reads 0, the poll byte is 0x00, and the GT IACK read with nothing pending returns
+    last_int (0 at reset) in both columns -- a GT read that handed back the acknowledge's -1 would read 0xffffffff."""
     begin()
     e_ocw3_read(v1, OCW3_IRR)
     e_in(a2, PIC1_CMD)
     e_ocw3_read(a0, OCW3_ISR)
     e_ocw3_read(a1, OCW3_POLL)
     e_in(a3, PIC1_IMR)
+    emit(lui(t1, GT_HI), "lui t1,0x%x" % GT_HI)
+    emit(lw(s0, GT_IACK, t1), "lw s0,%d(t1)" % GT_IACK)
     p, halt = end()
-    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "isr": "a0", "poll": "a1", "imr": "a3"}, None
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "isr": "a0", "poll": "a1", "imr": "a3", "iack": "s0"}, None
 
 
 def build_level():
@@ -390,7 +433,10 @@
 
 
 def build_nonspec():
-    """Both UARTs pending: poll twice (3 then 4), ISR 0x18, the non-specific EOI resets the lowest ISR bit, twice."""
+    """Both UARTs pending: poll (acknowledges 3; line 4 still pending), then -- v2e -- CP0 Cause read right after it
+    (IP2 must still be asserted: the acknowledge's recompute sees line 4) and a command-port read WITHOUT another OCW3
+    (the one-shot latch after a SUCCESSFUL poll: FIX returns the IRR 0x10, a sticky latch 0x84, HEAD its unconsumed poll
+    byte 0x83); then poll again (4), ISR 0x18, the non-specific EOI resets the lowest ISR bit, twice."""
     begin()
     e_uart_level_on(UART3_IER, UART3_MCR)
     e_uart_level_on()
@@ -398,6 +444,8 @@
     e_ocw3_read(v1, OCW3_IRR)
     e_in(a2, PIC1_CMD)
     e_ocw3_read(a0, OCW3_POLL)
+    emit(mfc0(s3, COP0_CAUSE), "mfc0 s3,cause")
+    e_in(s2, PIC1_CMD)
     e_ocw3_read(a1, OCW3_POLL)
     e_ocw3_read(a3, OCW3_ISR)
     e_out(PIC1_CMD, EOI_NONSPEC)
@@ -405,10 +453,51 @@
     e_out(PIC1_CMD, EOI_NONSPEC)
     e_ocw3_read(s1, OCW3_ISR)
     p, halt = end()
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll_a": "a0", "cause": "s3", "once2": "s2", "poll_b": "a1",
+                     "isr_both": "a3", "isr_one": "s0", "isr_none": "s1"}, None
+
+
+def build_speceoi():
+    """v2e (F2b): both UARTs acknowledged (ISR 0x18), then a SPECIFIC EOI of line 3 -- the ISR must lose exactly that bit
+    (FIX 0x10; a specific EOI clearing the whole ISR reads 0x00, as HEAD does, which never sets ISR); the specific EOI
+    of line 4 then clears the rest (0x00 both)."""
+    begin()
+    e_uart_level_on(UART3_IER, UART3_MCR)
+    e_uart_level_on()
+    e_delay()
+    e_ocw3_read(v1, OCW3_IRR)
+    e_in(a2, PIC1_CMD)
+    e_ocw3_read(a0, OCW3_POLL)
+    e_ocw3_read(a1, OCW3_POLL)
+    e_ocw3_read(a3, OCW3_ISR)
+    e_eoi(3)
+    e_ocw3_read(s0, OCW3_ISR)
+    e_eoi(4)
+    e_ocw3_read(s1, OCW3_ISR)
+    p, halt = end()
     return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll_a": "a0", "poll_b": "a1", "isr_both": "a3",
                      "isr_one": "s0", "isr_none": "s1"}, None
 
 
+def build_maskeoi():
+    """v2e (F2b): line 4 acknowledged (in service), THEN masked by OCW1 0x10, then the specific EOI 0x64 -- Linux's
+    mask-then-EOI order.  The EOI must take the ISR branch (ISR reads 0x00 in both columns: FIX clears the bit, HEAD
+    never set it); an EOI that takes the legacy branch for a masked line leaves ISR 0x10."""
+    begin()
+    e_uart_level_on()
+    e_delay()
+    e_ocw3_read(v1, OCW3_IRR)
+    e_in(a2, PIC1_CMD)
+    e_ocw3_read(a0, OCW3_POLL)
+    e_out(PIC1_IMR, 0x10)
+    e_in(a1, PIC1_IMR)
+    e_eoi(4)
+    e_ocw3_read(a3, OCW3_ISR)
+    e_out(PIC1_IMR, 0x00)
+    p, halt = end()
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "imr": "a1", "isr": "a3"}, None
+
+
 def build_casc():
     """The mc146818 periodic interrupt (IRQ 8, pic2) at 1024 Hz after a long wait: the cascade acknowledge."""
     begin()
@@ -446,18 +535,22 @@
 
 
 def build_gt():
-    """The GT64120 interrupt-acknowledge read with the UART level on: the value, ISR and IRR after it."""
+    """The GT64120 interrupt-acknowledge register with the UART level on: v2e first WRITES it (a write acknowledges
+    nothing -- ISR stays 0x00 in both columns; HEAD's write arm is a no-op and the fix's guard is `writeflag ==
+    MEM_READ`), then the READ: the value, ISR and IRR after it."""
     begin()
     e_uart_level_on()
     e_delay()
     e_ocw3_read(v1, OCW3_IRR)
     e_in(a2, PIC1_CMD)
     emit(lui(t1, GT_HI), "lui t1,0x%x" % GT_HI)
+    emit(sw(zero, GT_IACK, t1), "sw zr,%d(t1)" % GT_IACK)
+    e_ocw3_read(s0, OCW3_ISR)
     emit(lw(a0, GT_IACK, t1), "lw a0,%d(t1)" % GT_IACK)
     e_ocw3_read(a1, OCW3_ISR)
     e_ocw3_read(a3, OCW3_IRR)
     p, halt = end()
-    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "iack": "a0", "isr": "a1", "irr_after": "a3"}, None
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "isr_write": "s0", "iack": "a0", "isr": "a1", "irr_after": "a3"}, None
 
 
 def build_gtboth():
@@ -545,7 +638,8 @@
 
 
 SESSION_ORDER = [("quiet", build_quiet), ("level", build_level), ("ack", build_ack), ("ack3", build_ack3),
-                 ("masked", build_masked), ("nonspec", build_nonspec), ("casc", build_casc), ("pit", build_pit),
+                 ("masked", build_masked), ("maskeoi", build_maskeoi), ("nonspec", build_nonspec), ("speceoi", build_speceoi),
+                 ("casc", build_casc), ("pit", build_pit),
                  ("gt", build_gt), ("gtcasc", build_gtcasc), ("gtboth", build_gtboth), ("rate", build_rate)]
 
 
@@ -723,6 +817,7 @@
     rows.append(("quiet isr", "control", q.get("isr"), 0x00, 0x00, "eq"))
     rows.append(("quiet poll", "control", q.get("poll"), 0x00, 0x00, "eq"))
     rows.append(("quiet imr", "control", q.get("imr"), 0x00, 0x00, "eq"))
+    rows.append(("quiet iack", "contract", q.get("iack"), 0x00, 0x00, "eq"))
     lv = sess.get("level", {})
     rows.append(("level irr4", "control", bit(lv.get("irr"), 4), 1, 1, "eq"))
     rows.append(("level isr", "contract", lv.get("isr"), 0x00, 0x00, "eq"))
@@ -731,7 +826,7 @@
     rows.append(("eoi noack isr", "contract", lv.get("isr2"), 0x00, 0x00, "eq"))
     a = sess.get("ack", {})
     rows.append(("ack irr4", "control", bit(a.get("irr"), 4), 1, 1, "eq"))
-    rows.append(("poll byte", "control", a.get("poll"), 0x84, 0x84, "eq"))
+    rows.append(("poll byte", "contract", a.get("poll"), 0x84, 0x84, "eq"))
     rows.append(("poll isr", "symptom", a.get("isr"), 0x00, 0x10, "eq"))
     rows.append(("poll irr4", "symptom", bit(a.get("irr_after"), 4), 1, 0, "eq"))
     rows.append(("poll again", "symptom", a.get("once"), 0x84, 0x00, "eq"))
@@ -740,7 +835,7 @@
     rows.append(("eoi acked isr", "contract", a.get("isr2"), 0x00, 0x00, "eq"))
     a3 = sess.get("ack3", {})
     rows.append(("ack3 irr3", "control", bit(a3.get("irr"), 3), 1, 1, "eq"))
-    rows.append(("poll3 byte", "control", a3.get("poll"), 0x83, 0x83, "eq"))
+    rows.append(("poll3 byte", "contract", a3.get("poll"), 0x83, 0x83, "eq"))
     rows.append(("poll3 isr", "symptom", a3.get("isr"), 0x00, 0x08, "eq"))
     rows.append(("in-service irr3", "control", bit(a3.get("reassert"), 3), 1, 1, "eq"))
     rows.append(("eoi acked3", "symptom", bit(a3.get("eoi_acked"), 3), 0, 1, "eq"))
@@ -750,33 +845,47 @@
     rows.append(("poll masked", "symptom", mk.get("poll"), 0x84, 0x00, "eq"))
     rows.append(("poll once", "symptom", mk.get("once"), 0x84, 0x10, "eq"))
     rows.append(("masked eoi", "contract", bit(mk.get("masked_eoi"), 4), 0, 0, "eq"))
+    me = sess.get("maskeoi", {})
+    rows.append(("maskeoi irr4", "control", bit(me.get("irr"), 4), 1, 1, "eq"))
+    rows.append(("maskeoi poll", "contract", me.get("poll"), 0x84, 0x84, "eq"))
+    rows.append(("maskeoi imr", "control", me.get("imr"), 0x10, 0x10, "eq"))
+    rows.append(("maskeoi isr", "contract", me.get("isr"), 0x00, 0x00, "eq"))
     ns = sess.get("nonspec", {})
     rows.append(("both irr", "control", (None if ns.get("irr") is None else ns.get("irr") & 0x18), 0x18, 0x18, "eq"))
-    rows.append(("poll first", "control", ns.get("poll_a"), 0x83, 0x83, "eq"))
+    rows.append(("poll first", "contract", ns.get("poll_a"), 0x83, 0x83, "eq"))
+    rows.append(("nonspec ip2", "contract", bit(ns.get("cause"), CAUSE_IP2), 1, 1, "eq"))
+    rows.append(("poll once2", "symptom", ns.get("once2"), 0x83, 0x10, "eq"))
     rows.append(("poll second", "symptom", ns.get("poll_b"), 0x83, 0x84, "eq"))
     rows.append(("isr both", "symptom", ns.get("isr_both"), 0x00, 0x18, "eq"))
     rows.append(("nonspec lowest", "symptom", ns.get("isr_one"), 0x00, 0x10, "eq"))
     rows.append(("nonspec twice", "contract", ns.get("isr_none"), 0x00, 0x00, "eq"))
+    se = sess.get("speceoi", {})
+    rows.append(("spec both irr", "control", (None if se.get("irr") is None else se.get("irr") & 0x18), 0x18, 0x18, "eq"))
+    rows.append(("spec polls", "symptom", (None if se.get("poll_a") is None or se.get("poll_b") is None else (se.get("poll_a") << 8) | se.get("poll_b")), 0x8383, 0x8384, "eq"))
+    rows.append(("spec isr both", "symptom", se.get("isr_both"), 0x00, 0x18, "eq"))
+    rows.append(("spec eoi one", "symptom", se.get("isr_one"), 0x00, 0x10, "eq"))
+    rows.append(("spec eoi both", "contract", se.get("isr_none"), 0x00, 0x00, "eq"))
     c = sess.get("casc", {})
     rows.append(("casc irr2", "control", bit(c.get("irr"), 2), 1, 1, "eq"))
-    rows.append(("casc poll", "control", c.get("poll"), 0x82, 0x82, "eq"))
+    rows.append(("casc poll", "contract", c.get("poll"), 0x82, 0x82, "eq"))
     rows.append(("casc isr2", "symptom", c.get("isr"), 0x00, 0x04, "eq"))
-    rows.append(("casc slave poll", "control", c.get("poll2"), 0x80, 0x80, "eq"))
+    rows.append(("casc slave poll", "contract", c.get("poll2"), 0x80, 0x80, "eq"))
     rows.append(("casc isr8", "symptom", c.get("isr2"), 0x00, 0x01, "eq"))
     rows.append(("casc eoi isr", "contract", c.get("isr_eoi"), 0x00, 0x00, "eq"))
     rows.append(("casc eoi isr8", "contract", c.get("isr2_eoi"), 0x00, 0x00, "eq"))
     pt = sess.get("pit", {})
     rows.append(("pit irr0", "control", bit(pt.get("irr"), 0), 1, 1, "eq"))
-    rows.append(("pit poll", "control", pt.get("poll"), 0x80, 0x80, "eq"))
+    rows.append(("pit poll", "contract", pt.get("poll"), 0x80, 0x80, "eq"))
     rows.append(("pit poll irr0", "symptom", bit(pt.get("irr_after"), 0), 1, 0, "eq"))
     g = sess.get("gt", {})
     rows.append(("gt irr4", "control", bit(g.get("irr"), 4), 1, 1, "eq"))
-    rows.append(("gt iack", "control", g.get("iack"), 0x04, 0x04, "eq"))
+    rows.append(("gt write isr", "contract", g.get("isr_write"), 0x00, 0x00, "eq"))
+    rows.append(("gt iack", "contract", g.get("iack"), 0x04, 0x04, "eq"))
     rows.append(("gt isr", "symptom", g.get("isr"), 0x00, 0x10, "eq"))
     rows.append(("gt irr4 after", "symptom", bit(g.get("irr_after"), 4), 1, 0, "eq"))
     gc = sess.get("gtcasc", {})
     rows.append(("gtcasc irr2", "control", bit(gc.get("irr"), 2), 1, 1, "eq"))
-    rows.append(("gtcasc iack", "control", gc.get("iack"), 0x08, 0x08, "eq"))
+    rows.append(("gtcasc iack", "contract", gc.get("iack"), 0x08, 0x08, "eq"))
     rows.append(("gtcasc isr2", "symptom", gc.get("isr"), 0x00, 0x04, "eq"))
     rows.append(("gtcasc isr8", "symptom", gc.get("isr2"), 0x00, 0x01, "eq"))
     rows.append(("gtcasc eoi isr", "contract", gc.get("isr_eoi"), 0x00, 0x00, "eq"))
@@ -789,7 +898,7 @@
     r = sess.get("rate", {})
     rows.append(("rate imr", "control", r.get("imr"), 0xfe, 0xfe, "eq"))
     rows.append(("rate delivered", "control", r.get("count"), (1, None), (1, None), "band"))
-    rows.append(("rate poll byte", "control", r.get("lastpoll"), 0x80, 0x80, "eq"))
+    rows.append(("rate poll byte", "contract", r.get("lastpoll"), 0x80, 0x80, "eq"))
     rows.append(("rate storm", "symptom", r.get("count"), (5000, None), (1, 1000), "band"))
     for name, _ in SESSION_ORDER:
         if name == "rate":

```
**THIS FIRING ANSWERS QUESTION 1 ONLY** (the instrument diff and its measurements: is every new row valid by construction, is any new row vacuous, is the table of record read right).  The dispositions and Q2/Q3 go to a separate firing.  Keep hidden reasoning short; VERDICT line first.


## 3. MEASURED, in this order (every number read from the named artifact)

### 3.1 The F2b cells as mutants against the UNCHANGED v2d instrument (`killtable_20261025/table_v2d_extra/SCORES.txt`)

```
  D_eoi_maskcond   84/84  CONTROL=OK   ESCAPED  reds: 
  D_latch_cond     84/84  CONTROL=OK   ESCAPED  reds: 
  B_spec_isr0      84/84  CONTROL=OK   ESCAPED  reds: 
  D_deassert       84/84  CONTROL=OK   ESCAPED  reds: 
  D_gt_always      84/84  CONTROL=OK   ESCAPED  reds: 
  D_retire_anypic  84/84  CONTROL=OK   ESCAPED  reds: 
  D_retire_anyline 84/84  CONTROL=OK   ESCAPED  reds: 
```

### 3.2 The v2e cycle

* `witness_20261025e/` -- the shipped revision on the UNMODIFIED HEAD clone, HEAD column: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=101/101 (before any fix measurement of it).
* `pass2_20261025/fixlegs_114055/` -- BOTH legs: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=101/101 I8259EOI_CONTROL_fix=OK I8259EOI_RESULT_fix=101/101; rate: rate storm 0x1c10 head 5000..inf fix 1..1000 [HEAD] ok; rate storm 0x03 head 5000..inf fix 1..1000 [FIX] ok;
* `pass2_20261025/legs_114659/` -- L0 (the pre-fix build in GATE mode vs the FIX column): I8259EOI_CONTROL=OK I8259EOI_RESULT=75/101, exactly the 26 symptom rows red; L3 (`/bin/false`): I8259EOI_CONTROL=FAIL I8259EOI_RESULT=0/101, sentinel present.
* History: `witness_20261025d/` (v2e, 101/101 on HEAD), `fixlegs_112709/` (v2e, 101/101 both legs), `legs_113314/` (v2e L0 75/101: the 25 symptom rows plus `spec polls`, which was mislabelled a contract row -- its columns differ -- and is a symptom row in the shipped revision; L3 0/101).


### 3.3 The table of record on v2e

**23 mutants, 20 KILLED, 3 ESCAPED (D_fold, D_retire_anypic, D_retire_anyline)** -- `killtable_20261025/SCORES.txt`, every mutant re-run from the frozen v2e copy; the v2d table kept as `SCORES_v2d.txt` + `table_v2d/`.

```
  B_eoi            99/101 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked3 0x00 head 0x00
  B_poll           82/101 CONTROL=OK   KILLED   reds: poll isr 0x00 head 0x00 ; poll irr4 0x01 head 0x01 ; poll again 0x84 head 0x84 ; eoi acked
  B_gt             94/101 CONTROL=OK   KILLED   reds: gt isr 0x00 head 0x00 ; gt irr4 after 0x01 head 0x01 ; gtcasc isr2 0x00 head 0x00 ; gtcasc
  B_nonspec        100/101 CONTROL=OK   KILLED   reds: nonspec lowest 0x00 head 0x00
  D_eoi_n4         97/101 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00 ; maskeoi isr 0x10 want 0x00 ; spe
  D_eoi_n3         98/101 CONTROL=OK   KILLED   reds: eoi acked3 0x00 head 0x00 ; spec eoi one 0x18 head 0x00 ; spec eoi both 0x08 want 0x00
  D_eoi_ier        91/101 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00 ; eoi acked3 0x00 head 0x00 ; mask
  D_scan_raw       98/101 CONTROL=OK   KILLED   reds: masked irr4 0x00 want 0x01 ; poll masked 0x84 head 0x84 ; poll once 0x00 head 0x84
  D_noretire       100/101 CONTROL=OK   KILLED   reds: rate storm 0x1c2a head 5000..inf
  M_sticky         98/101 CONTROL=OK   KILLED   reds: poll once 0x00 head 0x84 ; poll once2 0x84 head 0x83 ; poll second 0x00 head 0x83
  M_noack_isr      86/101 CONTROL=OK   KILLED   reds: poll isr 0x00 head 0x00 ; eoi acked 0x00 head 0x00 ; poll3 isr 0x00 head 0x00 ; eoi acked3
  M_noack_irr      89/101 CONTROL=OK   KILLED   reds: poll irr4 0x01 head 0x01 ; poll again 0x10 head 0x84 ; poll once2 0x18 head 0x83 ; poll se
  D_gt_nocasc      97/101 CONTROL=OK   KILLED   reds: gtcasc iack 0x02 want 0x08 ; gtcasc isr8 0x00 head 0x00 ; gtboth iack 0x02 head 0x04 ; gtb
  D_gt_noassign    100/101 CONTROL=OK   KILLED   reds: gtboth iack 0x04 head 0x04
  D_gt_write       100/101 CONTROL=OK   KILLED   reds: gt write isr 0x10 want 0x00
  D_fold           101/101 CONTROL=OK   ESCAPED  reds: 
  D_eoi_maskcond   100/101 CONTROL=OK   KILLED   reds: maskeoi isr 0x10 want 0x00
  D_latch_cond     99/101 CONTROL=OK   KILLED   reds: poll once2 0x84 head 0x83 ; poll second 0x00 head 0x83
  B_spec_isr0      100/101 CONTROL=OK   KILLED   reds: spec eoi one 0x00 head 0x00
  D_deassert       100/101 CONTROL=OK   KILLED   reds: nonspec ip2 0x00 want 0x01
  D_gt_always      100/101 CONTROL=OK   KILLED   reds: quiet iack 0xffffffff want 0x00
  D_retire_anypic  101/101 CONTROL=OK   ESCAPED  reds: 
  D_retire_anyline 101/101 CONTROL=OK   ESCAPED  reds: 
```

Escapes beyond the three disclosed (D_fold, the two retire-guard conjuncts): **NONE**.

(End of part A.)

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`T19F2CA: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
