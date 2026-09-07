# PASS 3 -- `lunaabsentcpu` (#503): the CLOSING pass on the pass-2 repair (fix v2 + probe v3, 27 rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c`.  2026-09-06 ~10:30.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's board model (GXemul 0.7.0, hardened fork): `src/devices/dev_luna88k.c`,
the OMRON LUNA-88K interrupt controller model, and its detector `regress/luna_absentcpu_probe.py`.  Plain engineering vocabulary ("the
emulator process exits", "an unconnected slot", "a bounded walk").  **If you cannot read files that is expected -- every fact is inlined;
name any premise you cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the
project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub; a
file-reading seat uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## WHY A THIRD PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID
pass that finds zero floor breaches surviving adjudication, with the denominator stated.  Pass 2 (five seats answered: deepseek, glm,
minimax, grok, kimi; GPT-6 Astra REFUSED the packet twice on its content filter; Opus 5 and Fable 5 are walled on an Anthropic session
limit until 12:50pm America/Chicago and are re-fired when it lifts -- every closure here is PROVISIONAL on that roster gap) found:
* **deepseek** (+ grok's ask-again `M_SWONLY`): no row proved a DEVICE line delivers to a CONNECTED slot -- masking line 5 in the walk, or
  walking only software-pending slots, passed 22/22.  -> session B2 `sio5 deliver`.
* **glm** (+ grok's `min(n, 2)`): every session ran ncpus in {1, 2}, so `cpu_irq[cpu & 1]` or a bound clamped to 2 passed 22/22 and
  misroute slots 2/3 on a 3/4-cpu machine.  -> session E (`-n 4`): `four cpus`, `cpu3 deliver`, `others idle`.
* **kimi**: the per-slot latch `irqActive[cpu]` collapsed onto slot 0 passed 22/22 (no session ever had TWO slots pending) and is not
  equivalent -- with both IPIs pending cpu 1's is dropped.  -> session C2 `both deliver`.
* **minimax** (and Fable on pass 1): with the capture ABOVE the DEVINIT `ncpus > 4` exit, that exit had become load-bearing for the walk's
  bound.  -> the capture moved BELOW it.
* **grok**: three of the main loop's "unchanged" dispositions named rows that are not ledger rows (`lunadefaultstop`, `es438cells`,
  `lunaabsentmaskdecl` -- `es438` is the row); the ledger's witness field is still `none`; sio5clr did not kill M_NULLA (the host had
  already died at soft1); the SIO reaches the walk through the third AND fourth callers.  -> records, below.
All five closed in ONE repair (fix v2 + probe v3).  This pass closes if it finds zero floor breaches surviving adjudication in the (d)
enumeration of the shipped composite.

## SETTLED PREMISES, RE-INLINED
1. The walk (anchor `static void reassert_interrupts`): per slot `status = d->interrupt_status` (machine-wide; the six device lines are
   `1 << (line + 25)`, lines 1..6 -> bits 26..31); `enable = d->interrupt_enable[cpu]`; `if (d->software_interrupt_status[cpu]) status |=
   (1 << 26)`; `if (status & enable) { if (!d->irqActive[cpu]) INTERRUPT_ASSERT(d->cpu_irq[cpu]); d->irqActive[cpu] = 1; } else {
   if (d->irqActive[cpu]) INTERRUPT_DEASSERT(d->cpu_irq[cpu]); d->irqActive[cpu] = 0; }`.  FOUR callers: the INT_ST_MASKn store arm, the
   SOFT_INTn store/read arm, `luna88k_interrupt_assert` and `luna88k_interrupt_deassert` (the device lines; also the clock).
2. `INTERRUPT_ASSERT(istruct)` is `(istruct).interrupt_assert(&(istruct))` -- no NULL check.  DEVINIT connects slot 0 always and slots
   1..3 under `ncpus >= 2/3/4`; later in DEVINIT `ncpus > 4` prints and `exit(1)`s.  `emul.c` maps ncpus 0 -> 1; `-n` is 1..256.
3. Store arms index by ADDRESS (`cpunr = (addr - INT_ST_MASK0) / 4`) and never compare with ncpus.  The absent slots' MASK/SOFT registers
   stay guest-writable storage with readback (a board-model question; `lunaabsentmaskdecl`, filed as a row in this round's records).
4. Delivery is observable only free-running; the probe parks a cpu on `br .`, breakpoints VBR+8 and `continue`s; a cpu at VBR+8 with PSR
   0x8000000b / EPSR 0x80000000 is the channel.  Sessions with several pending slots park the first arrival off the vector and `continue`
   again so the second arrival is observed.

## THE FIX, VERBATIM (fix v2 against SEC's dev_luna88k.c; the ONLY change from the pass-2 packet's fix is the capture site)
```diff
--- GXEMUL-SEC/src/devices/dev_luna88k.c	2026-08-19 18:08:45.193189600 -0500
+++ GXEMUL-SEC/regress/artifacts/lunaabsentcpu/killtable2/baseline_dev_luna88k.c	2026-09-06 10:22:39.437302400 -0500
@@ -87,6 +87,11 @@
 
 
 struct luna88k_data {
+	/*  #503 (lunaabsentcpu): the number of CPUs actually INTERRUPT_CONNECTed at
+	    DEVINIT.  Slots at or above this index were never connected, so their
+	    cpu_irq[].interrupt_assert/deassert pointers are the memset's NULL.  The
+	    walk bound and the connect predicate are the same number on purpose.  */
+	int		ncpus;
 	struct interrupt cpu_irq[MAX_CPUS];
 	int		irqActive[MAX_CPUS];
 	uint32_t	interrupt_enable[MAX_CPUS];
@@ -167,7 +172,7 @@
 {
 	int cpu;
 
-	for (cpu = 0; cpu < MAX_CPUS; cpu++) {
+	for (cpu = 0; cpu < d->ncpus; cpu++) {		/*  #503  */
 		// printf("cpu%i: status = 0x%08x, enable = 0x%08x\n",
 		//	cpu, d->interrupt_status, d->interrupt_enable[0]);
 
@@ -1038,6 +1043,19 @@
 		exit(1);
 	}
 
+	/*  #503 (lunaabsentcpu): bound reassert_interrupts() to the slots connected
+	    above.  It walked all MAX_CPUS and called the NULL interrupt_assert of an
+	    unpopulated slot: on the default one-cpu machine a guest store of
+	    0xfc000000 to INT_ST_MASK1 followed by a store to SOFT_INT1 (or any device
+	    line whose bit that mask enables) ended the emulator process with a segmentation fault --
+	    measured, regress/luna_absentcpu_probe.py.  Captured BELOW the `ncpus > 4'
+	    exit so the bound is <= MAX_CPUS by construction, not by that exit.  The
+	    absent slots' MASK/SOFT registers stay guest-writable storage with
+	    readback (a board-model question, row lunaabsentmaskdecl).  Pre-existing
+	    upstream (the HACK comment's per-count connects and this walk are the
+	    0.7.0 import).  */
+	d->ncpus = devinit->machine->ncpus;
+
 	add_cmmu_for_cpu(devinit, 0, CMMU_I0, CMMU_D0);
 	add_cmmu_for_cpu(devinit, 1, CMMU_I1, CMMU_D1);
 	add_cmmu_for_cpu(devinit, 2, CMMU_I2, CMMU_D2);
```

## THE PROBE DIFF (v2 -> v3), VERBATIM (frozen v3 md5 902de3c0)
```diff
--- GXEMUL-SEC/regress/artifacts/lunaabsentcpu/luna_absentcpu_probe.v2.py	2026-09-06 09:45:28.426425500 -0500
+++ GXEMUL-SEC/regress/artifacts/lunaabsentcpu/luna_absentcpu_probe.v3.py	2026-09-06 10:22:39.525334200 -0500
@@ -49,10 +49,22 @@
   session C  (`-n 2', FREE-RUNNING)  cpu 1: VBR 0x40000, PSR 0x80000000, parked at `br .'; cpu 0 steps MASK1 <-
         0x04000000 and SOFT_INT1 <- 1, parks; breakpoint VBR+8; `continue'
     two cpus / cpu1 setup / mask1 land / survive /   M_HARD1 (`d->ncpus = 1' hardcoded -- the clause-(d) null repair:
-    cpu1 deliver / cpu1 shadow / cpu0 parked         a TOTAL ESCAPE of every 1-cpu row, measured 20/20): cpu 1 enters
+    cpu1 deliver / cpu1 shadow / cpu0 parked         a TOTAL ESCAPE of every 1-cpu row; measured 19/20, cpu1 deliver alone red): cpu 1 enters
                                                      its vector (pc == 0x40008), IND set, cpu 0 still parked.
   session D  (`-n 2', control)  the same without the SOFT_INT1 store: NO vector entry within the wait
-    nodeliver ctl                                    makes the two delivery rows attributable
+    nodeliver ctl                                    makes the delivery rows attributable
+  session B2 (1 cpu, FREE-RUNNING)  MASK0 <- 0x40000000 (bit 30 = SIO line 5), WR1 TX_IE, `continue'
+    sio5 deliver                                     M_MASK30 (the walk ignores line 5) and M_SWONLY (walk only slots with a
+                                                     software interrupt pending): a DEVICE line must deliver to a CONNECTED
+                                                     slot -- cpu 0 enters VBR+8.  v2 had no such row (deepseek, grok, pass 2)
+  session C2 (`-n 2', FREE-RUNNING)  MASK0+MASK1 bit 26, SOFT_INT0+SOFT_INT1: BOTH slots pending at once
+    both deliver                                     M_IRQACTIVE0 (the per-slot latch collapsed onto slot 0 drops cpu 1's IPI
+                                                     when slot 0 is pending too): both cpus reach VBR+8, in either order
+                                                     (the first arrival is parked off the vector, then `continue' again) (kimi)
+  session E  (`-n 4', FREE-RUNNING)  cpus 1..3 parked with VBR/PSR set; MASK3 + SOFT_INT3 from cpu 0
+    four cpus / cpu3 deliver / others idle           M_AND1 (`cpu_irq[cpu & 1]': slots 2/3 alias onto 0/1) and M_MIN2 (the
+                                                     bound clamped to two): the LAST slot delivers to cpu 3 and to nobody
+                                                     else -- v2 never ran more than two cpus (glm, grok, pass 2)
 
 RESULT words per row: OK / HALT (the the emulator process exited: signal / exit) / BADREGS (a value assert failed) / STOP (no vector entry
 before the wait ran out) / NOSTART.  Output: `LUNAABS_ROW=<name> RESULT=<word> ...' per row, `LUNAABS_RESULT=<ok>/<rows>',
@@ -61,10 +73,14 @@
 
 CONTRACT (clause e): catches the walk bound reverted or off by one, an ASSERT-only NULL guard, a decline-once latch on
 either arm, a guard moved inside the branch, the reassert CALL bounded in the store arms instead of the walk (sio5), the
-bound never assigned (session B), the bound hardcoded to 1 (session C), a declined store to an absent slot (mask1/mask2/
-mask3 readbacks), and the third/fourth MASK labels.  Does NOT catch: a both-sided NULL guard instead of the bound
-(EQUIVALENT on every reachable configuration -- measured 20/20 + 8/8; the choice is warrant-based), a deleted reassert
-in the SOFT arm alone (the clock's own reassert carries the delivery; disclosed debt), the clock/timer route (host-timer
+bound never assigned (session B), the bound hardcoded to 1 (session C) or clamped to 2 (session E), slots 2/3 aliased onto 0/1
+(session E), a device line masked out of the walk or a walk of software-pending slots only (session B2), the per-slot latch
+collapsed onto slot 0 (session C2), a declined store to an absent slot (mask1/mask2/mask3 readbacks), and the third/fourth MASK
+labels.  Does NOT catch: a both-sided NULL guard instead of the bound
+(EQUIVALENT on every reachable configuration -- measured 22/22 in killtable/; the choice is warrant-based), a deleted reassert
+in the SOFT arm alone (the clock's own reassert carries the delivery; disclosed debt), a connected slot's DEASSERT (no row observes a
+post-clear deassert free-running: handlers are `br .' with IND set and never rte -- kimi, grok), the `irqActive[cpu] = 0' clear
+itself (same reason), the clock/timer route (host-timer
 driven, not steppable -- same loop as sio5), MASK1..3 written by a real guest kernel (no luna88k source on disk).
 
 Encodings (cpu_m88k.c, the same source as regress/luna_intmask_probe.py):  ld rD,rS1,IMM16 op26=0x05 ; st rD,rS1,IMM16
@@ -394,6 +410,97 @@
     s.close()
 
 
+# ------------------------------------------------------------------------------------------------- session B2
+def session_B2():
+    print("=== SESSION B2 (1 cpu, FREE-RUNNING): slot 0 delivery through a DEVICE line -- MASK0 bit 30 (SIO line 5), WR1 TX_IE")
+    s = boot(1)
+    if s is None:
+        row("sio5 deliver", "NOSTART"); return
+    s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
+    if not store(s, MASK0, 0x40000000):
+        died(s, "sio5 deliver", "died arming slot 0 for line 5"); s.close(); return
+    # arm the SIO transmitter interrupt: WR1 select, then TX_IE -- sio_tx_pending raises line 5 (bit 30) machine-wide
+    if not store(s, SIOCMD0, 0x01) or not store(s, SIOCMD0, 0x02):
+        died(s, "sio5 deliver", "died on the WR1 TX_IE store with slot 0 armed"); s.close(); return
+    s.send("pc=0x%08x" % PARK)
+    s.send("breakpoint add 0x%08x" % (VBR + 8))
+    hit = s.cont_until_breakpoint(15.0)
+    if s.dead:
+        died(s, "sio5 deliver", "the emulator process exited while free-running with line 5 pending on slot 0"); s.close(); return
+    pc = s.reg("pc")
+    if not hit:
+        row("sio5 deliver", "STOP", "no vector entry within 15 s (pc=%s) -- the device line was never delivered to slot 0" % (("0x%08x" % pc) if pc is not None else "?"))
+        s.close(); return
+    row("sio5 deliver", "OK" if value(s, "B2 cpu0 pc == VBR+8 via SIO line 5 (a device line, not SOFT_INT)", pc, VBR + 8) else "BADREGS")
+    s.close()
+
+
+# ------------------------------------------------------------------------------------------------- session C2 (-n 2, both pending)
+def session_C2():
+    print("=== SESSION C2 (-n 2, FREE-RUNNING): BOTH slots pending -- MASK0+MASK1 bit 26, SOFT_INT0+SOFT_INT1; both cpus must enter")
+    s = boot(2)
+    if s is None:
+        row("both deliver", "NOSTART"); return
+    s.send("focus 1"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
+    s.send("focus 0"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000")
+    s.send("r6=0x%08x" % SCRATCH)
+    for a, v, what in ((MASK0, 0x04000000, "MASK0"), (MASK0 + 4, 0x04000000, "MASK1"), (SOFT0, 1, "SOFT_INT0"), (SOFT0 + 4, 1, "SOFT_INT1")):
+        if not store(s, a, v):
+            died(s, "both deliver", "died on the %s store on 2 cpus" % what); s.close(); return
+    s.send("pc=0x%08x" % PARK)
+    s.send("breakpoint add 0x%08x" % (VBR + 8))
+    entered = set()
+    for attempt in (1, 2):
+        hit = s.cont_until_breakpoint(15.0)
+        if s.dead:
+            died(s, "both deliver", "the emulator process exited while free-running with both slots pending"); s.close(); return
+        pcs = {c: s.reg("pc", cpu=c) for c in (0, 1)}
+        for c in (0, 1):
+            if pcs[c] == VBR + 8 and c not in entered:
+                entered.add(c)
+                # move the arrived cpu off the vector (its IND is set now, so it will not re-enter) and let the other one run
+                s.send("focus %d" % c); s.send("pc=0x%08x" % PARK); s.send("focus 0")
+        if len(entered) == 2 or not hit:
+            break
+    if len(entered) == 2:
+        row("both deliver", "OK", "cpu 0 and cpu 1 both entered VBR+8 with both IPIs pending (the per-slot latch is per slot)")
+    else:
+        row("both deliver", "STOP", "only cpus %s entered the vector within the wait -- an IPI was dropped" % sorted(entered))
+    s.close()
+
+
+# ------------------------------------------------------------------------------------------------- session E (-n 4)
+def session_E():
+    print("=== SESSION E (-n 4, FREE-RUNNING): the LAST slot -- MASK3 + SOFT_INT3 deliver to cpu 3, cpus 0..2 stay out of the vector")
+    s = boot(4)
+    if s is None:
+        row("four cpus", "NOSTART"); return
+    mark = len(s.buf); s.send("machine")
+    four = ("cpu3" in s.buf[mark:]) or ("cpu 3" in s.buf[mark:])
+    row("four cpus", "OK" if four else "BADREGS", "the `machine' listing names cpu3" if four else "no cpu3 in the machine listing")
+    for c in (1, 2, 3):
+        s.send("focus %d" % c); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
+    s.send("focus 0")
+    s.send("r6=0x%08x" % SCRATCH)
+    if not store(s, MASK0 + 12, 0x04000000):
+        died(s, "cpu3 deliver", "died on the MASK3 store on 4 cpus"); s.close(); return
+    if not store(s, SOFT0 + 12, 1):
+        died(s, "cpu3 deliver", "died on the SOFT_INT3 store on 4 cpus (slot 3 IS connected here)"); s.close(); return
+    s.send("pc=0x%08x" % PARK)
+    s.send("breakpoint add 0x%08x" % (VBR + 8))
+    hit = s.cont_until_breakpoint(15.0)
+    if s.dead:
+        died(s, "cpu3 deliver", "the emulator process exited while free-running on 4 cpus"); s.close(); return
+    pcs = [s.reg("pc", cpu=c) for c in (0, 1, 2, 3)]
+    if not hit:
+        row("cpu3 deliver", "STOP", "no vector entry within 15 s (cpu3 pc=%s)" % (("0x%08x" % pcs[3]) if pcs[3] is not None else "?"))
+        s.close(); return
+    row("cpu3 deliver", "OK" if value(s, "E cpu3 pc == VBR+8 (INTERRUPT vector on the LAST slot)", pcs[3], VBR + 8) else "BADREGS")
+    idle = all(pcs[c] != VBR + 8 for c in (0, 1, 2))
+    row("others idle", "OK" if idle else "BADREGS", "cpus 0..2 did not enter the vector" if idle else "another cpu took slot 3's interrupt: pcs=%s" % pcs)
+    s.close()
+
+
 # ------------------------------------------------------------------------------------------------- sessions C / D
 def session_n2(deliver):
     name = "C" if deliver else "D"
@@ -447,8 +554,11 @@
     prefix = any(r == "HALT" for _, r in rows)
     session_A2()
     session_B()
+    session_B2()
     session_n2(True)
+    session_C2()
     session_n2(False)
+    session_E()
     ok = sum(1 for _, r in rows if r == "OK")
     print("LUNAABS_RESULT=%d/%d" % (ok, len(rows)))
     halt_rows = [n for n, r in rows if r == "HALT"]
```

## TABLE 2, MEASURED (`regress/artifacts/lunaabsentcpu/killtable2/`; PRETABLE2_lunaabs.out mtime BEFORE the 10:06:23 start, untouched
## since -- corrections, if any, go to a separate file; baseline = SEC + fix_lunaabs.py v2, re-derived in the clone after every mutant;
## frozen probe v3 md5 902de3c0; BASE 27/27 PASS before and after; clone sentinel clear)
| mutant (exact edit) | score | red rows | reading |
|---|---|---|---|
| **M_MASK30**: `status = d->interrupt_status & ~(1 << 30);` | 26/27 FAIL | sio5 deliver STOP | the pass-2 escape, now a kill |
| **M_SWONLY**: `if (!d->software_interrupt_status[cpu]) continue;` at the top of the walk | 26/27 FAIL | sio5 deliver STOP | grok's ask-again, killed by the same row |
| **M_IRQACTIVE0**: all four `irqActive[cpu]` -> `irqActive[0]` | 26/27 FAIL | both deliver STOP | kimi's escape, now a kill |
| **M_AND1**: `cpu_irq[cpu & 1]` at ASSERT and DEASSERT | 25/27 FAIL | cpu3 deliver STOP, others idle BADREGS (cpu 1 took slot 3's interrupt) | glm's escape, now a kill |
| **M_MIN2**: `d->ncpus = ncpus > 2 ? 2 : ncpus` | 26/27 FAIL | cpu3 deliver STOP | grok's disclosed clamp, now a kill |
| M_REVERT (walk back to MAX_CPUS) | 20/22 PRE_FIX_SYMPTOM | soft1, siofirst HALT (process exited) | floor (b) |
| M_OFFBY1 (`<=`) | 20/22 | soft1, siofirst HALT | |
| M_NOASSIGN (bound never assigned) | 18/23 FAIL | slot0 deliver, sio5 deliver, both deliver, cpu1 deliver, cpu3 deliver | |
| M_HARD1 (`d->ncpus = 1`) | 21/24 FAIL | both deliver, cpu1 deliver, cpu3 deliver | |
| M_SKIP1 (slot 1 skipped) | 23/25 FAIL | both deliver, cpu1 deliver | |
| M_NULLA (ASSERT-only NULL guard) | 21/22 | soft1 HALT | |
| M_NULLAB (both-sided NULL guard) | 27/27 PASS | -- | EQUIVALENT (disclosed) |
| M_LATCH (decline once, then walk) | 20/22 | soft1, siofirst HALT | |
| M_GUARDASSERT (bound on the ASSERT call only) | 21/22 | soft1 HALT | |
| M_CALLGUARD (the pass-1 F4 alternative: bound the CALLS) | 21/23 | sio5, siofirst HALT | the alternative is NOT a fix (device-line callers) |
| M_NOREASSERT (SOFT arm's reassert removed) | 27/27 PASS | -- | disclosed debt: the clock's reassert carries delivery |
The RESULT denominators shrink when the host exits mid-session (the remaining rows of that session cannot run) -- a consequence, not a
row loss.  HEAD (the witness) with the final instrument: **20/22 PRE_FIX_SYMPTOM** (`probe_v3_head.out`: soft1 and siofirst HALT, signal 11;
every new session -- B2, C2, E -- passes on HEAD, which is the accept-side control for the new rows).

## CONTRACT (probe docstring)
Catches: the walk reaching an unconnected slot by any route (device line, software interrupt, mask store); the bound absent, one too
large, hardcoded to 1, clamped to 2, or applied to one call side only; slots 2/3 aliased onto 0/1; a device line masked out of the walk or
a walk of software-pending slots only; the per-slot latch collapsed onto slot 0; a latch-then-deliver; the alternative call-site fix; a
declined store to an absent slot (mask1/2/3 readbacks).  Does NOT catch (disclosed): a both-sided NULL guard (equivalent on every reachable
configuration); the SOFT arm's redundant reassert; a connected slot's DEASSERT and the `irqActive[cpu] = 0` clear (no row observes a
post-clear deassert free-running: handlers are `br .` with IND set and never rte); ncpus > 4 (DEVINIT exits at init time); MASK1..3 as a
real guest kernel writes them (no luna88k kernel source on disk).

## RECORDS THIS ROUND CARRIES (from pass 2)
File as rows: `lunadefaultstop` LOW (the switch's `default:` graceful stop plus the unimplemented RESET_CPU0..3 / SOFT_INT_FLAG* arms --
pass-1 F13 said "file separately" and nobody did), `lunaabsentmaskdecl` LOW documented-only (the absent slots' registers stay storage with
readback -- the design hold from pass 1).  `es438`: its owed mask2/mask3 pair is discharged by this detector's rows -- annotate/close on
this round.  The ledger witness field becomes `probe:regress/luna_absentcpu_probe.py` at closure.  The header's stale predictions (20/20,
20/20 + 8/8) were corrected; the sio5clr channel note corrected (the host had died at soft1, so sio5clr never scored M_NULLA); the M_CALLGUARD
note says third AND fourth callers.  PRETABLE (table 1) had its correction APPENDED to the same file, which refreshed its mtime -- stated;
PRETABLE2 is untouched.

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (fix v2 + probe v3)?**  The enumeration:
the dominating predicate `cpu < d->ncpus` (its constant's source, its bound both ways, its slot set 0..3); the body-read fields
`interrupt_status` (per device line), `interrupt_enable[cpu]`, `software_interrupt_status[cpu]`, `irqActive[cpu]`, `cpu_irq[cpu]`; joint cells
where the body tests them ({slot} x {pending: sw, device line, none} x {irqActive}).  If you find one, give the exact edit and the row that
should have caught it (a predicted sweep is a measurement owed -- say so); if none, CLOSE with your own denominator.  Second question, with
the count named: of the nine pass-3 dispositions (the capture move, three new sessions, two disclosed equivalents/debts, three filings/
annotations -- lunadefaultstop, lunaabsentmaskdecl, es438), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer with its denominator, then anything else,
under a page.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
