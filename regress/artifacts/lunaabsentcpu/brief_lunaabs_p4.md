# PASS 4 -- `lunaabsentcpu` (#503): the CLOSING pass on the pass-3 repair (fix v2b + probe v5, 34 rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` (the fix is NOT yet applied to the tree; it lives in the clone baseline quoted below).  2026-09-06 ~12:25.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's board model (GXemul 0.7.0, hardened fork): the LUNA-88K interrupt
controller in `src/devices/dev_luna88k.c` and its detector `regress/luna_absentcpu_probe.py`.  The "guest" is the operating system
inside the emulator; a "slot" is one of the four per-cpu interrupt entries the device keeps; a "connected" slot is one whose
`interrupt_assert`/`interrupt_deassert` callbacks were installed at device init.  Plain engineering vocabulary.  **If you cannot read
files that is expected -- every fact is inlined; name any premise you cannot settle rather than guessing.**  Tree under review:
`GXEMUL-SEC/src/` (three pristine-2021 copies under the project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.
`python3` in git-bash is a Windows Store stub; a file-reading seat that needs Python uses
`C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.  **Do not print large excerpts of the project's records into your
transcript**; read narrowly and paraphrase in neutral terms.

## WHY A FOURTH PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID
pass that finds zero floor breaches surviving adjudication, with the denominator stated.  Pass 3 (fix v2 + probe v3, 27 rows;
deepseek, minimax, grok, kimi answered; codex REFUSED the packet on its content filter for the third time on this row -- a seat
failure, not agreement; glm BURNED; Opus 5 and Fable 5 walled until 12:50pm America/Chicago -- so every closure here is PROVISIONAL on
their re-fire; agy deliberately not fired) found these, all measured as escapes of the earlier instrument and all closed:
* **deepseek** -- the DEASSERT side of the walk was unobserved: `if (d->irqActive[0])` on the deassert test (a slot alias) passed 27/27.
  -> v4 sessions B3 (`redeliver`, `noreenter`) and C3 (`noreenter1`): after a delivery the cpu reads SOFT_INTn (clearing it) and the line
  must DEASSERT, so a wrong-slot latch test or a dropped deassert re-enters the vector.
* **minimax** -- `software_interrupt_status[cpu] && !irqActive[cpu]` on the sw bit passed 27/27: the SECOND walk with the IPI still
  pending deasserted the line; {pending: sw} x {irqActive: 1} was unrowed -> v4 row `reenter` (B3).
* **grok, kimi** -- session E pended only slot 3, so `if (cpu == 2) continue;` (M_SKIP2) was predicted 27/27: the interior cell of the
  slot axis -> v4 E pended slots 2 and 3.  Grok's records: `es438` is already CLOSED (cf4b083) -- the mask rows ANNOTATE it; the fix
  comment's "<= MAX_CPUS by construction" overclaimed (the `ncpus > 4` exit is what bounds it) -- reworded; `cpu3 deliver` read BADREGS
  not STOP under M_AND1 -- the packet's wording corrected.
* **kimi, landed after v4 was cut** -- (ii) `irqActive[cpu & 1]` at the four latch sites: every multi-pending session pended slots of
  DIFFERENT parity ({0,1} in C2; {2,3} in v4's E), so a same-parity pair was never pending together and the parity alias was invisible
  -> v5 session E pends ALL FOUR slots and requires all four arrivals; (iii) device-line delivery to a non-zero slot was unprobed (B2
  delivers SIO line 5 to slot 0 only) -> v5 session C4 (`-n 2`: MASK1 bit 30 + WR1 TX_IE, cpu 1 enters).
This pass closes if it finds zero floor breaches surviving adjudication in the (d) enumeration of the shipped composite.

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
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
   0x8000000b / EPSR 0x80000000 is the channel.  Sessions with several pending slots park each arrival off the vector and `continue`
   again so the next arrival is observed (up to four rounds of 15 s in session E).
5. A BOTH-SIDED NULL guard instead of the bound (`if (d->cpu_irq[cpu].interrupt_assert) INTERRUPT_ASSERT(...)` and the same on the
   deassert) is EQUIVALENT to the fix on every reachable configuration: DEVINIT connects exactly slots 0..ncpus-1 and the `ncpus > 4` exit
   keeps ncpus <= MAX_CPUS, so "slot has a callback" and "slot < ncpus" are the same predicate.  Measured 34/34 in table 4 (M_NULLAB), as
   predicted; it is an alternative FIX, not a defect, and is recorded as EQUIVALENT WITH ITS WARRANT (the warrant expires if a slot can
   ever be connected above the bound or disconnected below it).  Question for you: is that warrant complete?

## THE FIX, VERBATIM (fix v2b against SEC's `dev_luna88k.c`; the ONLY change from pass 3's packet is the reworded capture comment)
```diff
--- GXEMUL-SEC/src/devices/dev_luna88k.c	2026-08-19 18:08:45.193189600 -0500
+++ _scratchpad/lunaabs/killtable4/baseline_dev_luna88k.c	2026-09-06 11:31:14.511886500 -0500
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
 
@@ -1038,6 +1043,20 @@
 		exit(1);
 	}
 
+	/*  #503 (lunaabsentcpu): bound reassert_interrupts() to the slots connected
+	    above.  It walked all MAX_CPUS and called the NULL interrupt_assert of an
+	    unpopulated slot: on the default one-cpu machine a guest store of
+	    0xfc000000 to INT_ST_MASK1 followed by a store to SOFT_INT1 (or any device
+	    line whose bit that mask enables) killed the emulator with SIGSEGV --
+	    measured, regress/luna_absentcpu_probe.py.  Captured BELOW the `ncpus > 4'
+	    exit above, which guarantees the value is <= MAX_CPUS before it is
+	    stored (delete that exit and a 5-cpu machine would walk cpu_irq[4]).  The
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
(Review question on the comment, not the code: the phrase "killed the emulator with SIGSEGV" describes the pre-fix symptom in plain
terms -- is any claim in the comment false against the code above it?)

## THE PROBE DIFF (v4 -> v5), VERBATIM (frozen v5 md5 3fd0198f; 34 rows: v4's 32 + `cpu1 deliver4`, `cpu0 deliver4`, `sio5 deliver1`, minus `others idle`)
```diff
--- regress/artifacts/lunaabsentcpu/killtable3/luna_absentcpu_probe.frozen.py	(v4)
+++ _scratchpad/lunaabs/luna_absentcpu_probe.py	(v5)
@@ -71,10 +71,14 @@
   session C3 (`-n 2', FREE-RUNNING)  cpu 1 delivered, then cpu 0 reads SOFT_INT1 (clears it): slot 1 must DEASSERT
     noreenter1                                       M_DEASSERT0 (`if (d->irqActive[0])' on the deassert side: slot 1's deassert
                                                      tests slot 0's latch, which is 0 here -> no DEASSERT -> cpu 1 re-enters) (deepseek)
-  session E  (`-n 4', FREE-RUNNING)  cpus 1..3 parked with VBR/PSR set; MASK2+SOFT_INT2 and MASK3+SOFT_INT3 from cpu 0
-    four cpus / cpu3 deliver / cpu2 deliver /        M_AND1 (`cpu_irq[cpu & 1]': slots 2/3 alias onto 0/1), M_MIN2 (the bound
-    others idle                                      clamped to two) and M_SKIP2 (slot 2 skipped -- kimi, pass 3: v3 never pended
-                                                     slot 2): cpus 2 and 3 both enter, in either order; cpus 0/1 do not
+  session E  (`-n 4', FREE-RUNNING)  all four cpus with VBR/PSR set and parked; MASKn bit 26 + SOFT_INTn for n = 0..3 from cpu 0
+    four cpus / cpu3 deliver / cpu2 deliver /        M_AND1 (`cpu_irq[cpu & 1]'), M_MIN2 (the bound clamped to two), M_SKIP2 (slot 2
+    cpu1 deliver4 / cpu0 deliver4                    skipped) and M_IRQACTIVEP1 (`irqActive[cpu & 1]': the latch aliased by PARITY --
+                                                     pairs {0,2} and {1,3} share one latch, so the second of each pair is dropped):
+                                                     all four cpus enter VBR+8, in any order (kimi, pass 3: every earlier multi-pending
+                                                     session pended slots of different parity)
+  session C4 (`-n 2', FREE-RUNNING)  MASK1 <- 0x40000000 (bit 30), WR1 TX_IE: a DEVICE line delivering to a NON-ZERO slot
+    sio5 deliver1                                    (B2 delivers line 5 to slot 0 only -- kimi, pass 3): cpu 1 enters VBR+8
 
 RESULT words per row: OK / HALT (the host died: signal / exit) / BADREGS (a value assert failed) / STOP (no vector entry
 before the wait ran out) / NOSTART.  Output: `LUNAABS_ROW=<name> RESULT=<word> ...' per row, `LUNAABS_RESULT=<ok>/<rows>',
@@ -86,10 +90,11 @@
 bound never assigned (session B), the bound hardcoded to 1 (session C) or clamped to 2 (session E), slots 2/3 aliased onto 0/1
 (session E), a device line masked out of the walk or a walk of software-pending slots only (session B2), the per-slot latch
 collapsed onto slot 0 (session C2), the second walk after a delivery -- a still-pending IPI deasserted, a connected slot's DEASSERT or
-its `irqActive = 0' clear dropped, the deassert testing the wrong slot's latch (sessions B3, C3) --, a declined store to an absent slot
+its `irqActive = 0' clear dropped, the deassert testing the wrong slot's latch (sessions B3, C3), and a deleted reassert in the SOFT arm
+(M_NOREASSERT: disclosed as debt on v2/v3 -- the clock's reassert carries DELIVERY -- and killed 29/31 by v4's noreenter rows, because
+the SOFT read-clear no longer triggers the deassert walk and the line stays asserted) --, a declined store to an absent slot
 (mask1/mask2/mask3 readbacks), and the third/fourth MASK labels.  Does NOT catch: a both-sided NULL guard instead of the bound
-(EQUIVALENT on every reachable configuration -- measured 22/22 in killtable/; the choice is warrant-based), a deleted reassert
-in the SOFT arm alone (the clock's own reassert carries the delivery; disclosed debt), the clock/timer route's own deassert timing (host-timer driven), the clock/timer route (host-timer
+(EQUIVALENT on every reachable configuration -- measured 22/22 in killtable/; the choice is warrant-based), the clock/timer route's own deassert timing (host-timer driven), the clock/timer route (host-timer
 driven, not steppable -- same loop as sio5), MASK1..3 written by a real guest kernel (no luna88k source on disk).
 
@@ -528,6 +533,28 @@
     s.close()
 
 
+# ------------------------------------------------------------------------------------------------- session C4 (-n 2, device line -> slot 1)
+def session_C4():
+    print("=== SESSION C4 (-n 2, FREE-RUNNING): a DEVICE line delivering to slot 1 -- MASK1 bit 30 (SIO line 5) + WR1 TX_IE")
+    s = boot(2)
+    if s is None:
+        row("sio5 deliver1", "NOSTART"); return
+    s.send("focus 1"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK); s.send("focus 0")
+    s.send("r6=0x%08x" % SCRATCH)
+    if not store(s, MASK0 + 4, 0x40000000):
+        died(s, "sio5 deliver1", "died arming slot 1 for line 5 on 2 cpus"); s.close(); return
+    if not store(s, SIOCMD0, 0x01) or not store(s, SIOCMD0, 0x02):
+        died(s, "sio5 deliver1", "died on the WR1 TX_IE store with slot 1 armed"); s.close(); return
+    s.send("pc=0x%08x" % PARK)
+    s.send("breakpoint add 0x%08x" % (VBR + 8))
+    hit = s.cont_until_breakpoint(15.0)
+    if s.dead:
+        died(s, "sio5 deliver1", "host died while free-running with line 5 pending on slot 1"); s.close(); return
+    pc1 = s.reg("pc", cpu=1)
+    row("sio5 deliver1", "OK" if (hit and pc1 == VBR + 8) else "STOP", "cpu 1 entered VBR+8 via SIO line 5" if (hit and pc1 == VBR + 8) else "cpu 1 never entered via the device line (pc1=%s)" % pc1)
+    s.close()
+
+
 # ------------------------------------------------------------------------------------------------- session C2 (-n 2, both pending)
@@ -564,7 +591,7 @@
 def session_E():
-    print("=== SESSION E (-n 4, FREE-RUNNING): the LAST two slots -- MASK2+SOFT_INT2 and MASK3+SOFT_INT3 deliver to cpus 2 and 3, cpus 0/1 idle")
+    print("=== SESSION E (-n 4, FREE-RUNNING): ALL FOUR slots pending -- MASKn bit 26 + SOFT_INTn for n = 0..3; every cpu must enter")
     s = boot(4)
@@ -575,27 +602,27 @@
         s.send("focus %d" % c); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
     s.send("focus 0")
     s.send("r6=0x%08x" % SCRATCH)
-    for a, v, what in ((MASK0 + 8, 0x04000000, "MASK2"), (MASK0 + 12, 0x04000000, "MASK3"), (SOFT0 + 8, 1, "SOFT_INT2"), (SOFT0 + 12, 1, "SOFT_INT3")):
-        if not store(s, a, v):
-            died(s, "cpu3 deliver", "died on the %s store on 4 cpus (slots 2 and 3 ARE connected here)" % what); s.close(); return
+    s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000")                                  # cpu 0 too: all four take an IPI
+    for n in (0, 1, 2, 3):
+        if not store(s, MASK0 + 4 * n, 0x04000000) or not store(s, SOFT0 + 4 * n, 1):
+            died(s, "cpu3 deliver", "died on the MASK%d/SOFT_INT%d stores on 4 cpus (every slot IS connected here)" % (n, n)); s.close(); return
     s.send("pc=0x%08x" % PARK)
     s.send("breakpoint add 0x%08x" % (VBR + 8))
     entered = set()
-    for attempt in (1, 2):
+    for attempt in (1, 2, 3, 4):
         hit = s.cont_until_breakpoint(15.0)
         if s.dead:
             died(s, "cpu3 deliver", "host died while free-running on 4 cpus"); s.close(); return
         pcs = [s.reg("pc", cpu=c) for c in (0, 1, 2, 3)]
-        for c in (2, 3):
+        for c in (0, 1, 2, 3):
             if pcs[c] == VBR + 8 and c not in entered:
                 entered.add(c)
                 s.send("focus %d" % c); s.send("pc=0x%08x" % PARK); s.send("focus 0")      # park the arrival off the vector (IND set now)
-        if not hit or len(entered) == 2:
+        if not hit or len(entered) == 4:
             break
-    row("cpu3 deliver", "OK" if 3 in entered else "STOP", ...)
-    row("cpu2 deliver", "OK" if 2 in entered else "STOP", ...)
-    idle = all(pcs[c] != VBR + 8 for c in (0, 1))
-    row("others idle", "OK" if idle else "BADREGS", ...)
+    for c in (3, 2, 1, 0):
+        row("cpu%d deliver" % c if c >= 2 else "cpu%d deliver4" % c, "OK" if c in entered else "STOP",
+            "cpu %d entered VBR+8 with all four slots pending" % c if c in entered else "cpu %d never entered: entered=%s pcs=%s" % (c, sorted(entered), pcs))
     s.close()
@@ -657,6 +684,7 @@
     session_C3()
+    session_C4()
     session_n2(False)
     session_E()
```
Product code in this repair: NONE (the fix is v2b throughout).  Gate wiring (owed at commit, not yet done): `python3
luna_absentcpu_probe.py "$PMAX" "$IMAGES"` in gate 11 beside the #438 probe, pinning `LUNAABS_DONE`, `LUNA_ABSENTCPU_WITNESS=PASS`,
`LUNAABS_RESULT=34/34` and the named rows.

## TABLE 4, MEASURED (`_scratchpad/lunaabs/killtable4/` -> `regress/artifacts/lunaabsentcpu/killtable4/`; PRETABLE4_lunaabs.out mtime ~11:00, BEFORE the 11:31 start, untouched; baseline = SEC + fix_lunaabs.py v2b, re-derived in the clone after every mutant and `cmp`-checked; frozen v5 md5 3fd0198f; BASE 34/34 before and after; clone sentinel clear at the end)
| mutant (exact edit) | score on v5 | witness word | red rows / note |
|---|---|---|---|
| M_IRQACTIVEP1: `irqActive[cpu & 1]` at the four latch sites | 32/34 | FAIL | cpu3 deliver, cpu2 deliver (cpus 0 and 1 arrived first and took the two parity-shared latches) -- AS PREDICTED |
| M_SWLATCH: the latch keyed on the sw bit | 32/34 | FAIL | reenter, both deliver |
| M_NODEASSERT: the connected slot's DEASSERT dropped | 31/33 | FAIL | noreenter, noreenter1 (33 rows produced) |
| M_NOCLEAR: the `irqActive = 0` clear dropped | 33/34 | FAIL | redeliver |
| M_DEASSERT0: `if (d->irqActive[0])` on the deassert side | 33/34 | FAIL | noreenter1 |
| M_SKIP2: `if (cpu == 2) continue;` | 33/34 | FAIL | cpu2 deliver |
| M_MASK30: line 5's bit masked out of the walk | 32/34 | FAIL | sio5 deliver (B2) AND sio5 deliver1 (C4) |
| M_SWONLY: a walk of software-pending slots only | 29/33 | FAIL | sio5 deliver, sio5 deliver1, noreenter, noreenter1 (33 produced) |
| M_IRQACTIVE0: the latch collapsed onto slot 0 | 29/34 | FAIL | both deliver, noreenter1, cpu3 deliver, cpu2 deliver, cpu1 deliver4 (the three E rows + both deliver predicted; noreenter1 as on v4) |
| M_AND1: `cpu_irq[cpu & 1]` | 32/34 | FAIL | cpu2/cpu3 deliver -- AS PREDICTED |
| M_MIN2: the bound clamped to two | 32/34 | FAIL | cpu2/cpu3 deliver -- AS PREDICTED |
| M_REVERT: the walk back to `cpu < MAX_CPUS` | 27/29 | PRE_FIX_SYMPTOM | the process ends on soft1 / siofirst (the defect) |
| M_OFFBY1: `cpu <= d->ncpus` | 23/26 | PRE_FIX_SYMPTOM | |
| M_NOASSIGN: the capture deleted (ncpus stays 0) | 18/30 | FAIL | all twelve delivery rows STOP -- nothing delivers (30 produced) |
| M_HARD1: the bound hardcoded to 1 | 25/32 | FAIL | cpu1 deliver, both deliver, noreenter1, sio5 deliver1, cpu3/cpu2/cpu1 deliver4 (32 produced) |
| M_SKIP1: slot 1 skipped | 27/32 | FAIL | cpu1 deliver, both deliver, noreenter1, sio5 deliver1, cpu1 deliver4 (32 produced) |
| M_NULLA: an ASSERT-only NULL guard instead of the bound | 28/29 | PRE_FIX_SYMPTOM | the DEASSERT walk still reaches NULL |
| **M_NULLAB: a BOTH-sided NULL guard instead of the bound** | **34/34** | PASS | **EQUIVALENT, as predicted (premise 5) -- an alternative fix, recorded with its warrant, not a breach** |
| M_LATCH: decline the absent slot once, then walk it | 27/29 | PRE_FIX_SYMPTOM | |
| M_GUARDASSERT: the bound applied to the ASSERT call only | 28/29 | PRE_FIX_SYMPTOM | |
| M_CALLGUARD: the bound at the CALLERS instead of the walk | 28/30 | PRE_FIX_SYMPTOM | (pass 2 had predicted this equivalent; it is not -- the clock's path bypasses it) |
| M_NOREASSERT: the reassert deleted in the SOFT arm | 31/33 | FAIL | killed by the noreenter rows (disclosure withdrawn in v4) |
Every prediction in PRETABLE4 held except one in the SAFE direction: it predicted M_NOREASSERT would "stay green" on v5's new rows,
and it stays KILLED by v4's noreenter rows (31/33) as it was on v4 (29/31) -- the prediction concerned the new rows only and was
carelessly worded; recorded.  HEAD (`83df95c`, `/tmp/gxopus501p4`, `cmp`-checked == HEAD) with this instrument: **27/29**,
`LUNA_ABSENTCPU_WITNESS=PRE_FIX_SYMPTOM (soft1, siofirst)` -- the two rows on which the process ends with a segmentation fault (signal
11) are exactly the defect's two routes (the SOFT_INT1 store; the SIO TX_IE line with MASK1 bit 30 set).  The fix on the clone: 34/34.

## THE CLOSURES NOW IN THE CONTRACT (probe docstring)
* the bound: reverted / off by one / never assigned / hardcoded / clamped / at the callers / assert-only / latch-then-walk (sessions A, B, C, E).
* the slot axis: every slot 0..3 has a single-pending delivery row and a four-pending delivery row (E); slots 0 and 1 have device-line rows (B2, C4).
* the latch: per-slot, both polarities, both parities (C2, E; M_IRQACTIVE0, M_IRQACTIVEP1); the deassert side after a clear (B3, C3).
* the absent slots' registers: guest-writable storage with readback (mask1/2/3), the third/fourth MASK labels.
* DISCLOSED: the both-sided NULL guard (equivalent, warrant above); the clock/timer route (host-timer driven, not steppable);
  MASK1..3 as a real guest kernel writes them (no luna88k source on disk); the SIO deassert timing.

## THE DENOMINATOR THIS PASS CLAIMS CLOSED (tables 1-4, every score in a named log under `regress/artifacts/lunaabsentcpu/`)
The walk's bound predicate in every form a plausible edit takes (10 mutants); the slot axis at every reachable slot and pairing (E all
four; M_SKIP1/M_SKIP2/M_AND1/M_MIN2); the per-slot latch and its aliases (M_IRQACTIVE0, M_IRQACTIVEP1, M_SWLATCH); the deassert side
(M_NODEASSERT, M_NOCLEAR, M_DEASSERT0); the callers (M_CALLGUARD, M_NOREASSERT, M_MASK30, M_SWONLY); the device line to slots 0 and 1.

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (fix v2b + probe v5)?**  The enumeration:
the predicates dominating the diff's edited lines up to the function boundary (the walk's `cpu < d->ncpus`; inside the body `status &
enable`, `!d->irqActive[cpu]`, `d->irqActive[cpu]`, `d->software_interrupt_status[cpu]`; at the capture, the `ncpus > 4` exit that
dominates it), operand swaps drawn only from the fields those bodies read (`interrupt_status`, `interrupt_enable[cpu]`,
`software_interrupt_status[cpu]`, `irqActive[cpu]`, `cpu_irq[cpu]`, `ncpus`), and joint cells where the body's own tests distinguish
them ({status & enable: 0, !0} x {irqActive: 0, 1} per slot; {slot} x {parity}).  Review EFFORT is scoped to the v4 -> v5 diff above; the
FLOOR question is asked of the composite.  If you find one, give the exact edit and the row that should have caught it; if none, CLOSE
with YOUR OWN denominator.  Second question, with the count named: of the pass-3 dispositions (FIVE row closures -- B3, C3, E all
four, C4, reenter; ONE equivalence recorded with a warrant (M_NULLAB); ONE disclosure withdrawn (M_NOREASSERT); THREE records
corrections -- es438 annotated not closed, the capture comment reworded, STOP/BADREGS wording), WHICH IS WRONG?

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer to the one question with its
denominator, then anything else, under a page.
