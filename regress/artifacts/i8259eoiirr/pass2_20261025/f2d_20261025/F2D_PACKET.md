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

**Reading scope (file-reading seats):** `GXEMUL-SEC/regress/i8259_eoi_probe.py` (the v2g copy in the working tree, md5 c1fa683e)
and its frozen twin `GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_132736/i8259_eoi_probe.frozen.py.txt`;
`witness_20261025f/`, `pass2_20261025/fixlegs_132736/`, `pass2_20261025/legs_133457/`; `killtable_20261025/` (`PRETABLE.out`
with its v2g block = the enumeration, `SCORES.txt` = the v2g table of record, `table_v2f_extra/`, `table_v2f/`,
`SCORES_v2f.txt`); `pass2_20261025/f2c_20261025/` (the six F2c answers and `F2C_RULINGS.md`); `GXEMUL-SEC/src/` for the product
sources.  Do not read `tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md`.  Do not build or run anything.

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

## 3. THE INSTRUMENT DIFF -- the banked frozen v2f copy -> the banked frozen v2g copy, every hunk INLINED

```diff
--- C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_114055/i8259_eoi_probe.frozen.py.txt	2026-10-25 11:46:59.240866700 -0500
+++ C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/fixlegs_132736/i8259_eoi_probe.frozen.py.txt	2026-10-25 13:34:57.746217800 -0500
@@ -51,6 +51,19 @@
            under the mask, returns the IRR 0x10 (FIX: the poll is one-shot) where a sticky poll would return 0x00 and
            HEAD returns 0x84 (`poll once`); masking leaves IRR; an un-acknowledged EOI while masked consumes
            (contract, both 0).
+  ack ip2  v2g (F2c): CP0 Cause bit 10 right after the poll that acknowledges the ONLY pending line: the recompute must drop
+  pit ip2  the CPU line (FIX 0; HEAD 1 -- its poll consumes nothing); `pit ip2` is the same cell with the 8253 as the source
+           (the event retired, nothing remains).  A recompute deleted or made constant-true leaves 1.
+  maskrem  v2g (F2c): both UARTs pending, line 4 MASKED, then the poll: it acknowledges line 3 and the recompute finds only a
+           MASKED request remaining -- Cause.IP2 reads 0 on FIX (`maskrem ip2`; HEAD 1; a recompute that ignores the mask 1);
+           the IRR after it keeps the masked bit (`maskrem irr after` FIX 0x10 / HEAD 0x18).
+  isrother v2g (F2c): line 3 acknowledged, line 4 pending and NOT acknowledged, then EOI 0x64 of line 4: the arm must take the
+           LEGACY branch for a line not in service whatever else is -- IRR bit 4 consumed (`isrother irr4` 0 both; an arm
+           testing "any ISR bit" leaves 1) and ISR keeps bit 3 (`isrother isr` FIX 0x08 / HEAD 0x00).
+  gtmask   v2g (F2c): the GT IACK read with the UART (4) and the RTC (8) pending but the master's cascade line 2 MASKED: the
+           acknowledge takes 4 and leaves the slave alone -- the read returns 4 in both columns (`gtmask iack`; HEAD's last_int
+           is 4) and slave ISR stays 0 (`gtmask isr8`; an arm that acknowledges the slave on every master acknowledge returns
+           8 and sets it); master ISR 0x10 on FIX (`gtmask isr`).
   maskeoi  v2e (F2b): line 4 ACKNOWLEDGED (poll 0x84), THEN masked (OCW1 0x10), then the specific EOI 0x64 -- Linux's
            mask-then-EOI order: ISR reads 0x00 in both columns (FIX: the ISR branch clears the bit; HEAD never set it);
            an EOI that takes the legacy branch for a masked in-service line leaves 0x10 (`maskeoi isr`).
@@ -94,7 +107,15 @@
 after an UNSUCCESSFUL poll (`poll once2`), a specific EOI that takes the legacy branch for a MASKED in-service line
 (`maskeoi isr`), a specific EOI that clears more than its own ISR bit (`spec eoi one`), an acknowledge whose recompute
 drops the CPU line while another request is pending (`nonspec ip2`), a GT WRITE that acknowledges (`gt write isr`),
-a GT read that returns the acknowledge's -1 with nothing pending (`quiet iack`).  OUTSIDE: the `default` read arm
+a GT read that returns the acknowledge's -1 with nothing pending (`quiet iack`); and, from the repair's own pass (v2g, the
+CLASS CLOSURE -- every predicate the fix adds, its body-tested partition, one row or one disclosure per cell): the recompute
+`d->irr & ~d->ier` {an unmasked request remains: `nonspec ip2`; nothing remains: `ack ip2`, `pit ip2`; only a masked request
+remains: `maskrem ip2`}, the EOI predicate `d->isr & bit` {in service and unmasked: `eoi acked`; in service and masked:
+`maskeoi isr`; not in service, nothing in service: `eoi noack`; not in service while ANOTHER line is: `isrother irr4`; masked
+and not in service: `masked eoi`}, the one-shot latch {after a successful poll: `poll once2`; after an unsuccessful one:
+`poll once`}, the scan order {two lines on one PIC: `poll first` 0x83, `gtboth iack` 8 -- lowest first}, the GT read
+{write: `gt write isr`; nothing pending: `quiet iack`; cascade with slave work: `gtcasc`, `gtboth`; non-cascade with slave
+work pending: `gtmask iack` / `gtmask isr8`}.  OUTSIDE: the `default` read arm
 (byte-identical to HEAD), priority inhibition by ISR (not modelled; filed i8259priority), level-triggered mode (ICW1
 LTIM; filed i8259ltim), special mask mode (OCW3 0x68, an empty arm; filed i8259smm), the PReP and footbridge vector
 reads (filed isaiackreaders), the OCW2 bytes that stop the emulation (filed i8259cmdhalt), an 8253 count of zero (filed
@@ -102,8 +123,11 @@
 two-SLAVE-request CPU-line case (a manual cascade pre-fold strands the second request; owed as i8259cascline -- the
 `nonspec ip2` row sees only the master-side recompute), and the retire guard's two conjuncts (a slave line-0 or a
 non-zero-line acknowledge retiring an 8253 event is observable only with a pending count >= 2, which only host time
-produces; disclosed, the band-row construction filed as pit8253retireguard).  The spurious IACK with nothing pending
-returns last_int as HEAD did (`quiet iack` pins it).
+produces; disclosed, the band-row construction filed as pit8253retireguard), a machine without ISA PICs (`pic1 == NULL`,
+MVME5500) or without a slave (`pic2 == NULL`) -- unobservable on a one-machine instrument, no witness machine here -- and the
+spurious cascade (`n2 < 0`: master line 2 pending with no unmasked slave request), unreachable while bus_isa.c re-folds bit 2
+from the slave's unmasked set on every ISA event.  The spurious IACK with nothing pending returns last_int as HEAD did
+(`quiet iack` pins it).
 A held level re-requests after the acknowledge within one tick (the ns16550 and the 8253 -- the sources these rows
 drive -- re-assert on every tick while their condition holds; the pckbc does NOT: it suppresses repeated assertions while
 already asserted, dev_pckbc.c, F2b) -- more generous than edge-mode hardware for those two, never less; disclosed, not rowed.
@@ -370,6 +394,7 @@
     e_ocw3_read(v1, OCW3_IRR)
     e_in(a2, PIC1_CMD)
     e_ocw3_read(a0, OCW3_POLL)
+    emit(mfc0(s5, COP0_CAUSE), "mfc0 s5,cause")
     e_ocw3_read(a1, OCW3_ISR)
     e_ocw3_read(a3, OCW3_IRR)
     e_ocw3_read(s0, OCW3_POLL)
@@ -383,7 +408,7 @@
     e_in(s3, PIC1_CMD)
     e_ocw3_read(s4, OCW3_ISR)
     p, halt = end()
-    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "isr": "a1", "irr_after": "a3",
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "cause": "s5", "isr": "a1", "irr_after": "a3",
                      "poll2": "s0", "once": "s1", "reassert": "s2", "eoi_acked": "s3", "isr2": "s4"}, None
 
 
@@ -457,6 +482,47 @@
                      "isr_both": "a3", "isr_one": "s0", "isr_none": "s1"}, None
 
 
+def build_maskrem():
+    """v2g (F2c): both UARTs pending, line 4 MASKED, then the poll -- it acknowledges line 3 and the recompute must find only a
+    MASKED request remaining: Cause.IP2 reads 0 on FIX (the line is dropped), 1 on HEAD (its poll consumes nothing) and 1 under a
+    recompute that ignores the mask; the IRR after it keeps the masked bit 4 (FIX 0x10; HEAD 0x18)."""
+    begin()
+    e_uart_level_on(UART3_IER, UART3_MCR)
+    e_uart_level_on()
+    e_delay()
+    e_ocw3_read(v1, OCW3_IRR)
+    e_in(a2, PIC1_CMD)
+    e_out(PIC1_IMR, 0x10)
+    e_in(a0, PIC1_IMR)
+    e_ocw3_read(a1, OCW3_POLL)
+    emit(mfc0(a3, COP0_CAUSE), "mfc0 a3,cause")
+    e_ocw3_read(s0, OCW3_IRR)
+    e_out(PIC1_IMR, 0x00)
+    p, halt = end()
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "imr": "a0", "poll": "a1", "cause": "a3", "irr_after": "s0"}, None
+
+
+def build_isrother():
+    """v2g (F2c): line 3 acknowledged (in service), line 4 pending and NOT acknowledged, then EOI 0x64 of line 4 -- the EOI arm
+    must take the LEGACY branch (line 4 is not in service, whatever else is): IRR bit 4 consumed (0 in both columns; an arm
+    that tests "any ISR bit" leaves it 1) and ISR keeps bit 3 (FIX 0x08; HEAD 0x00)."""
+    begin()
+    e_uart_level_on(UART3_IER, UART3_MCR)
+    e_uart_level_on()
+    e_delay()
+    e_ocw3_read(v1, OCW3_IRR)
+    e_in(a2, PIC1_CMD)
+    e_ocw3_read(a0, OCW3_POLL)
+    e_li(t5, OCW3_IRR)
+    e_li(t6, 0x64)
+    emit(sb(t6, PIC1_CMD, t0), "sb t6,%d(t0)" % PIC1_CMD)
+    emit(sb(t5, PIC1_CMD, t0), "sb t5,%d(t0)" % PIC1_CMD)
+    e_in(a1, PIC1_CMD)
+    e_ocw3_read(a3, OCW3_ISR)
+    p, halt = end()
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "irr_eoi": "a1", "isr": "a3"}, None
+
+
 def build_speceoi():
     """v2e (F2b): both UARTs acknowledged (ISR 0x18), then a SPECIFIC EOI of line 3 -- the ISR must lose exactly that bit
     (FIX 0x10; a specific EOI clearing the whole ISR reads 0x00, as HEAD does, which never sets ISR); the specific EOI
@@ -529,9 +595,10 @@
     e_ocw3_read(v1, OCW3_IRR)
     e_in(a2, PIC1_CMD)
     e_ocw3_read(a0, OCW3_POLL)
+    emit(mfc0(a3, COP0_CAUSE), "mfc0 a3,cause")
     e_ocw3_read(a1, OCW3_IRR)
     p, halt = end()
-    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "irr_after": "a1"}, None
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "poll": "a0", "cause": "a3", "irr_after": "a1"}, None
 
 
 def build_gt():
@@ -574,6 +641,31 @@
     return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "iack": "a0", "isr": "a1", "isr2": "a3"}, None
 
 
+def build_gtmask():
+    """v2g (F2c): the GT IACK read with the UART (IRQ 4) and the RTC (IRQ 8) pending but the master's CASCADE LINE 2 MASKED:
+    the acknowledge takes line 4 and must leave the slave alone (the cascade conjunct `n == 2`): the read returns 4 in both
+    columns (HEAD's last_int is 4 too) and slave ISR stays 0 (an arm that acknowledges the slave on every master acknowledge
+    returns 8 and sets slave ISR bit 0); master ISR 0x10 on FIX."""
+    begin()
+    e_out(CMOS_IDX, 0x0a)
+    e_out(CMOS_DAT, 0x26)
+    e_out(CMOS_IDX, 0x0b)
+    e_out(CMOS_DAT, 0x40)
+    e_uart_level_on()
+    e_long(); e_long(); e_long()
+    e_ocw3_read(v1, OCW3_IRR)
+    e_in(a2, PIC1_CMD)
+    e_out(PIC1_IMR, 0x04)
+    e_in(s0, PIC1_IMR)
+    emit(lui(t1, GT_HI), "lui t1,0x%x" % GT_HI)
+    emit(lw(a0, GT_IACK, t1), "lw a0,%d(t1)" % GT_IACK)
+    e_ocw3_read(a1, OCW3_ISR)
+    e_ocw3_read(a3, OCW3_ISR, PIC2_CMD)
+    e_out(PIC1_IMR, 0x00)
+    p, halt = end()
+    return p, halt, {"ram": "v0", "irr": "v1", "stable": "a2", "imr": "s0", "iack": "a0", "isr": "a1", "isr2": "a3"}, None
+
+
 def build_gtcasc():
     """The GT64120 IACK read with the mc146818 periodic interrupt pending on pic2: returns 8 in both columns (HEAD:
     last_int); FIX acknowledges the master's cascade line and the slave's line 0 (ISR 0x04 / 0x01)."""
@@ -638,9 +730,9 @@
 
 
 SESSION_ORDER = [("quiet", build_quiet), ("level", build_level), ("ack", build_ack), ("ack3", build_ack3),
-                 ("masked", build_masked), ("maskeoi", build_maskeoi), ("nonspec", build_nonspec), ("speceoi", build_speceoi),
-                 ("casc", build_casc), ("pit", build_pit),
-                 ("gt", build_gt), ("gtcasc", build_gtcasc), ("gtboth", build_gtboth), ("rate", build_rate)]
+                 ("masked", build_masked), ("maskeoi", build_maskeoi), ("maskrem", build_maskrem), ("nonspec", build_nonspec),
+                 ("speceoi", build_speceoi), ("isrother", build_isrother), ("casc", build_casc), ("pit", build_pit),
+                 ("gt", build_gt), ("gtcasc", build_gtcasc), ("gtboth", build_gtboth), ("gtmask", build_gtmask), ("rate", build_rate)]
 
 
 class Emu(object):
@@ -827,6 +919,7 @@
     a = sess.get("ack", {})
     rows.append(("ack irr4", "control", bit(a.get("irr"), 4), 1, 1, "eq"))
     rows.append(("poll byte", "contract", a.get("poll"), 0x84, 0x84, "eq"))
+    rows.append(("ack ip2", "symptom", bit(a.get("cause"), CAUSE_IP2), 1, 0, "eq"))
     rows.append(("poll isr", "symptom", a.get("isr"), 0x00, 0x10, "eq"))
     rows.append(("poll irr4", "symptom", bit(a.get("irr_after"), 4), 1, 0, "eq"))
     rows.append(("poll again", "symptom", a.get("once"), 0x84, 0x00, "eq"))
@@ -850,6 +943,12 @@
     rows.append(("maskeoi poll", "contract", me.get("poll"), 0x84, 0x84, "eq"))
     rows.append(("maskeoi imr", "control", me.get("imr"), 0x10, 0x10, "eq"))
     rows.append(("maskeoi isr", "contract", me.get("isr"), 0x00, 0x00, "eq"))
+    mr = sess.get("maskrem", {})
+    rows.append(("maskrem both irr", "control", (None if mr.get("irr") is None else mr.get("irr") & 0x18), 0x18, 0x18, "eq"))
+    rows.append(("maskrem imr", "control", mr.get("imr"), 0x10, 0x10, "eq"))
+    rows.append(("maskrem poll", "contract", mr.get("poll"), 0x83, 0x83, "eq"))
+    rows.append(("maskrem ip2", "symptom", bit(mr.get("cause"), CAUSE_IP2), 1, 0, "eq"))
+    rows.append(("maskrem irr after", "symptom", (None if mr.get("irr_after") is None else mr.get("irr_after") & 0x18), 0x18, 0x10, "eq"))
     ns = sess.get("nonspec", {})
     rows.append(("both irr", "control", (None if ns.get("irr") is None else ns.get("irr") & 0x18), 0x18, 0x18, "eq"))
     rows.append(("poll first", "contract", ns.get("poll_a"), 0x83, 0x83, "eq"))
@@ -865,6 +964,11 @@
     rows.append(("spec isr both", "symptom", se.get("isr_both"), 0x00, 0x18, "eq"))
     rows.append(("spec eoi one", "symptom", se.get("isr_one"), 0x00, 0x10, "eq"))
     rows.append(("spec eoi both", "contract", se.get("isr_none"), 0x00, 0x00, "eq"))
+    io_ = sess.get("isrother", {})
+    rows.append(("isrother both irr", "control", (None if io_.get("irr") is None else io_.get("irr") & 0x18), 0x18, 0x18, "eq"))
+    rows.append(("isrother poll", "contract", io_.get("poll"), 0x83, 0x83, "eq"))
+    rows.append(("isrother irr4", "contract", bit(io_.get("irr_eoi"), 4), 0, 0, "eq"))
+    rows.append(("isrother isr", "symptom", io_.get("isr"), 0x00, 0x08, "eq"))
     c = sess.get("casc", {})
     rows.append(("casc irr2", "control", bit(c.get("irr"), 2), 1, 1, "eq"))
     rows.append(("casc poll", "contract", c.get("poll"), 0x82, 0x82, "eq"))
@@ -876,6 +980,7 @@
     pt = sess.get("pit", {})
     rows.append(("pit irr0", "control", bit(pt.get("irr"), 0), 1, 1, "eq"))
     rows.append(("pit poll", "contract", pt.get("poll"), 0x80, 0x80, "eq"))
+    rows.append(("pit ip2", "symptom", bit(pt.get("cause"), CAUSE_IP2), 1, 0, "eq"))
     rows.append(("pit poll irr0", "symptom", bit(pt.get("irr_after"), 0), 1, 0, "eq"))
     g = sess.get("gt", {})
     rows.append(("gt irr4", "control", bit(g.get("irr"), 4), 1, 1, "eq"))
@@ -895,6 +1000,12 @@
     rows.append(("gtboth iack", "symptom", gb.get("iack"), 0x04, 0x08, "eq"))
     rows.append(("gtboth isr2", "symptom", gb.get("isr"), 0x00, 0x04, "eq"))
     rows.append(("gtboth isr8", "symptom", gb.get("isr2"), 0x00, 0x01, "eq"))
+    gm = sess.get("gtmask", {})
+    rows.append(("gtmask irr", "control", (None if gm.get("irr") is None else gm.get("irr") & 0x14), 0x14, 0x14, "eq"))
+    rows.append(("gtmask imr", "control", gm.get("imr"), 0x04, 0x04, "eq"))
+    rows.append(("gtmask iack", "contract", gm.get("iack"), 0x04, 0x04, "eq"))
+    rows.append(("gtmask isr", "symptom", gm.get("isr"), 0x00, 0x10, "eq"))
+    rows.append(("gtmask isr8", "contract", gm.get("isr2"), 0x00, 0x00, "eq"))
     r = sess.get("rate", {})
     rows.append(("rate imr", "control", r.get("imr"), 0xfe, 0xfe, "eq"))
     rows.append(("rate delivered", "control", r.get("count"), (1, None), (1, None), "band"))

```

## 4. MEASURED, in this order (every number read from the named artifact)

### 4.1 The F2c cells as mutants against the UNCHANGED v2f instrument (`killtable_20261025/table_v2f_extra/SCORES.txt`)

```
  D_recompute_raw   101/101 CONTROL=OK   ESCAPED  reds: 
  D_recompute_true  99/101  CONTROL=OK   KILLED   reds: rate poll byte 0x00 want 0x80 ; rate storm 0x3c3c head 5000..inf
  D_recompute_none  99/101  CONTROL=OK   KILLED   reds: rate poll byte 0x00 want 0x80 ; rate storm 0x395b head 5000..inf
  D_eoi_anyisr      101/101 CONTROL=OK   ESCAPED  reds: 
  D_gt_nocasc2      101/101 CONTROL=OK   ESCAPED  reds: 
  D_scan_high       94/101  CONTROL=OK   KILLED   reds: poll first 0x84 want 0x83 ; poll once2 0x08 head 0x83 ; poll second 0x83 head 0x83 ; spec 
```

### 4.2 The v2g cycle

* `witness_20261025f/` -- v2g on the UNMODIFIED HEAD clone, HEAD column: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=123/123 (before any v2g fix measurement).
* `pass2_20261025/fixlegs_132736/` -- v2g, BOTH legs: I8259EOI_CONTROL_base=OK I8259EOI_RESULT_base=123/123 I8259EOI_CONTROL_fix=OK I8259EOI_RESULT_fix=123/123; rate: rate storm 0x1c84 head 5000..inf fix 1..1000 [HEAD] ok; rate storm 0x03 head 5000..inf fix 1..1000 [FIX] ok;
* `pass2_20261025/legs_133457/` -- L0 (the pre-fix build in GATE mode vs the FIX column): I8259EOI_CONTROL=OK I8259EOI_RESULT=91/123, exactly the 32 symptom rows red; L3 (`/bin/false`): I8259EOI_CONTROL=FAIL I8259EOI_RESULT=0/123, sentinel present.
* History: v2f = `witness_20261025e/` 101/101, `fixlegs_114055/` 101/101 both legs, `legs_114659/` L0 75/101 (26 symptom rows), L3 0/101; its table of record `SCORES_v2f.txt` / `table_v2f/`: 23 mutants, 20 killed, 3 escaped (the disclosed three).


### 4.3 The table of record on v2g

**29 mutants, 26 KILLED, 3 ESCAPED (D_fold, D_retire_anypic, D_retire_anyline)** -- `killtable_20261025/SCORES.txt`, every mutant re-run from the frozen v2g copy.

```
  B_eoi             121/123 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked3 0x00 head 0x00
  B_poll            99/123  CONTROL=OK   KILLED   reds: ack ip2 0x01 head 0x01 ; poll isr 0x00 head 0x00 ; poll irr4 0x01 head 0x01 ; poll again 0
  B_gt              115/123 CONTROL=OK   KILLED   reds: gt isr 0x00 head 0x00 ; gt irr4 after 0x01 head 0x01 ; gtcasc isr2 0x00 head 0x00 ; gtcasc
  B_nonspec         122/123 CONTROL=OK   KILLED   reds: nonspec lowest 0x00 head 0x00
  D_eoi_n4          119/123 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00 ; maskeoi isr 0x10 want 0x00 ; spe
  D_eoi_n3          120/123 CONTROL=OK   KILLED   reds: eoi acked3 0x00 head 0x00 ; spec eoi one 0x18 head 0x00 ; spec eoi both 0x08 want 0x00
  D_eoi_ier         113/123 CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00 ; eoi acked3 0x00 head 0x00 ; mask
  D_scan_raw        117/123 CONTROL=OK   KILLED   reds: masked irr4 0x00 want 0x01 ; poll masked 0x84 head 0x84 ; poll once 0x00 head 0x84 ; gtmas
  D_noretire        122/123 CONTROL=OK   KILLED   reds: rate storm 0x1cd7 head 5000..inf
  M_sticky          120/123 CONTROL=OK   KILLED   reds: poll once 0x00 head 0x84 ; poll once2 0x84 head 0x83 ; poll second 0x00 head 0x83
  M_noack_isr       106/123 CONTROL=OK   KILLED   reds: poll isr 0x00 head 0x00 ; eoi acked 0x00 head 0x00 ; poll3 isr 0x00 head 0x00 ; eoi acked3
  M_noack_irr       107/123 CONTROL=OK   KILLED   reds: ack ip2 0x01 head 0x01 ; poll irr4 0x01 head 0x01 ; poll again 0x10 head 0x84 ; maskrem ip
  D_gt_nocasc       119/123 CONTROL=OK   KILLED   reds: gtcasc iack 0x02 want 0x08 ; gtcasc isr8 0x00 head 0x00 ; gtboth iack 0x02 head 0x04 ; gtb
  D_gt_noassign     122/123 CONTROL=OK   KILLED   reds: gtboth iack 0x04 head 0x04
  D_gt_write        122/123 CONTROL=OK   KILLED   reds: gt write isr 0x10 want 0x00
  D_fold            123/123 CONTROL=OK   ESCAPED  reds: 
  D_eoi_maskcond    122/123 CONTROL=OK   KILLED   reds: maskeoi isr 0x10 want 0x00
  D_latch_cond      121/123 CONTROL=OK   KILLED   reds: poll once2 0x84 head 0x83 ; poll second 0x00 head 0x83
  B_spec_isr0       122/123 CONTROL=OK   KILLED   reds: spec eoi one 0x00 head 0x00
  D_deassert        122/123 CONTROL=OK   KILLED   reds: nonspec ip2 0x00 want 0x01
  D_gt_always       122/123 CONTROL=OK   KILLED   reds: quiet iack 0xffffffff want 0x00
  D_retire_anypic   123/123 CONTROL=OK   ESCAPED  reds: 
  D_retire_anyline  123/123 CONTROL=OK   ESCAPED  reds: 
  D_recompute_raw   122/123 CONTROL=OK   KILLED   reds: maskrem ip2 0x01 head 0x01
  D_recompute_true  118/123 CONTROL=OK   KILLED   reds: ack ip2 0x01 head 0x01 ; maskrem ip2 0x01 head 0x01 ; pit ip2 0x01 head 0x01 ; rate poll b
  D_recompute_none  118/123 CONTROL=OK   KILLED   reds: ack ip2 0x01 head 0x01 ; maskrem ip2 0x01 head 0x01 ; pit ip2 0x01 head 0x01 ; rate poll b
  D_eoi_anyisr      122/123 CONTROL=OK   KILLED   reds: isrother irr4 0x01 want 0x00
  D_gt_nocasc2      121/123 CONTROL=OK   KILLED   reds: gtmask iack 0x08 want 0x04 ; gtmask isr8 0x01 want 0x00
  D_scan_high       114/123 CONTROL=OK   KILLED   reds: poll first 0x84 want 0x83 ; poll once2 0x08 head 0x83 ; poll second 0x83 head 0x83 ; spec 
```

Escapes beyond the three disclosed (D_fold, the two retire-guard conjuncts): **NONE**.

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
