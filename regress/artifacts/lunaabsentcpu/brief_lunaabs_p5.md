# PASS 5 -- `lunaabsentcpu` (#503): the closing pass on the PASS-4 REPAIR (probe v5 -> v6, 37 rows).  Tree `GXEMUL-SEC/src/`, HEAD `83df95c`; the fix is NOT yet applied to the tree and lives in the clone baseline quoted below.  2026-09-06.  SHORT BY DESIGN: one diff, one table, one question.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's board model (GXemul 0.7.0, hardened fork): the LUNA-88K interrupt
controller in `src/devices/dev_luna88k.c` and its detector.  The "guest" is the operating system inside the emulator; a "slot" is one of the
four per-CPU interrupt entries the device keeps; a "connected" slot is one whose callbacks were installed at device init.  Plain engineering
vocabulary.  **If you cannot read files that is expected -- every fact is inlined; name any premise you cannot settle rather than guessing.**

Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies under the project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by
grep anchor.  `python3` in git-bash is a Windows Store stub; a file-reading seat that needs Python uses
`C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

**EVERY PATH IN THIS PACKET IS A FROZEN ARTIFACT COPY.**  The probe under review is
`GXEMUL-SEC/regress/artifacts/lunaabsentcpu/luna_absentcpu_probe.v6.frozen.py` (md5 3be01e9d), not the working file -- because on pass 4 the
working file was edited three minutes before a seat read it, and the packet said 34 rows while the file had 37.  That seat caught it; the
rule is now in the brief template.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
On pass 4 two seats independently found a mutant that swept the whole detector, and a third BUILT it and confirmed 34/34.  **Check the
premises, not just the derivations.**

## WHY A FIFTH PASS, AND WHAT CLOSES IT
The repair-chain rule: a repair made in response to a pass owes its own pass, scoped to THAT diff; the chain closes on the first VALID pass
finding zero floor breaches surviving adjudication, with the denominator stated; and when consecutive passes find breaches of ONE CLASS, the
next repair closes the CLASS rather than the cell.  Pass 4 found exactly that, so this repair is a class closure.

**PASS 4's FINDINGS, all closed here:**
* **kimi and grok, independently** -- the walk's per-CPU READS can be aliased and probe v5 could not see it:
  `enable = d->interrupt_enable[cpu]` -> `[cpu & 1]`, and the twin `if (d->software_interrupt_status[cpu])` -> `[cpu & 1]`.  Both predicted
  **34/34, a total escape**, and neither had been run.  v5's session E writes the SAME mask bit and the same IPI value on all four slots, so
  a parity alias on a READ still finds a correctly-set partner; the parity alias v5 DOES kill is on a WRITE, consumed by the first arrival of
  each pair.
* **grok, the cause** -- v4's session E pended slots 2 and 3 with 0 and 1 IDLE, a configuration whose alias targets DISAGREE, and the v4->v5
  rewrite REPLACED it instead of adding beside it.  The repair for one cell of the class deleted the coverage of another.
* **opus5, MEASURED in two tables of its own** -- confirmed 34/34 on the frozen v5 by building it; measured the complementary trade
  (`M_IRQACTIVEP1` on v4 is 32/32, i.e. v4's E does NOT kill it, because slots 2 and 3 are in DIFFERENT parity classes); found `M_EXIT8`
  sweeps 37/37 but is EQUIVALENT (the machine layer carries its own `ncpus > 4` exit after `device_add`, measured both ways at `-n 5`); found
  `M_SWEQ1` escapes 37/37 as clause-(e) debt; and found an **L4 IN THE PRODUCT COMMENT** -- see below.
* **codex** -- SEAT FAILURE, content filter, fourth time on this row.  **glm / deepseek / minimax** -- SEAT FAILURE, an account-level weekly
  quota on the Ollama cloud (the seat file said only `429`; the response BODY carried the real reason, and the helper now surfaces it).
  **fable5** -- WALLED until the 9th.  All recorded by name, none counted as agreement.

## THE FIX, UNCHANGED IN CODE AND CORRECTED IN COMMENT
The code is fix v2b throughout: an `int ncpus` field, the walk bounded `cpu < d->ncpus`, and the capture
`d->ncpus = devinit->machine->ncpus;` placed below the device's own `ncpus > 4` exit.
**The capture comment claimed *"(delete that exit and a 5-cpu machine would walk `cpu_irq[4]`)"* and that is MEASURED FALSE.**
`machine_luna88k.c` does `device_add(machine, "luna88k")` and then carries a SECOND `ncpus > 4` exit AFTER it, so deleting the device's exit
lets DEVINIT capture 5 and the MACHINE layer ends the run before any guest instruction -- nothing walks.  Measured both ways at `-n 5`: base
prints the device's message, the mutant prints the machine's, both exit 1, neither walks.
**And the record of the earlier correction is wrong too**: the CHANGELOG records a pass-3 refutation of the pass-2 wording as ACCEPTED, and
that refutation is itself false -- both seats read only the device file and neither saw the machine-layer guard -- so the wording it
displaced was closer to right.  Both corrected in this round.

## THE PROBE DIFF (v5 -> v6), VERBATIM (frozen v6 md5 3be01e9d; 37 rows = v5's 34 plus three)
```diff
--- GXEMUL-SEC/regress/artifacts/lunaabsentcpu/killtable4/luna_absentcpu_probe.frozen.py	2026-09-06 12:14:35.689852400 -0500
+++ GXEMUL-SEC/regress/artifacts/lunaabsentcpu/luna_absentcpu_probe.v6.frozen.py	2026-09-06 14:31:06.794142400 -0500
@@ -72,6 +72,14 @@
     noreenter1                                       M_DEASSERT0 (`if (d->irqActive[0])' on the deassert side: slot 1's deassert
                                                      tests slot 0's latch, which is 0 here -> no DEASSERT -> cpu 1 re-enters) (deepseek)
   session E  (`-n 4', FREE-RUNNING)  all four cpus with VBR/PSR set and parked; MASKn bit 26 + SOFT_INTn for n = 0..3 from cpu 0
+  session E2 (`-n 4', FREE-RUNNING)  slots 2 and 3 pending, slots 0 and 1 IDLE -- the alias targets DISAGREE
+    cpu3 deliver23 / cpu2 deliver23 /             M_ENP1 (`enable = d->interrupt_enable[cpu & 1]'), M_SWP1
+    others idle23                                 (`software_interrupt_status[cpu & 1]') and their [0] forms M_EN0 / M_SW0:
+                                                  slot 2 aliases onto the IDLE slot 0 and slot 3 onto the IDLE slot 1, so the
+                                                  read returns 0 and neither cpu is asserted.  Session E cannot see any of
+                                                  them -- it writes the SAME mask bit and the same IPI on every slot, so a
+                                                  parity alias on a READ still finds a set partner (kimi and grok, pass 4,
+                                                  independently; v4 had this configuration and the v4->v5 rewrite deleted it)
     four cpus / cpu3 deliver / cpu2 deliver /        M_AND1 (`cpu_irq[cpu & 1]'), M_MIN2 (the bound clamped to two), M_SKIP2 (slot 2
     cpu1 deliver4 / cpu0 deliver4                    skipped) and M_IRQACTIVEP1 (`irqActive[cpu & 1]': the latch aliased by PARITY --
                                                      pairs {0,2} and {1,3} share one latch, so the second of each pair is dropped):
@@ -89,12 +97,13 @@
 either arm, a guard moved inside the branch, the reassert CALL bounded in the store arms instead of the walk (sio5), the
 bound never assigned (session B), the bound hardcoded to 1 (session C) or clamped to 2 (session E), slots 2/3 aliased onto 0/1
 (session E), a device line masked out of the walk or a walk of software-pending slots only (session B2), the per-slot latch
-collapsed onto slot 0 (session C2), the second walk after a delivery -- a still-pending IPI deasserted, a connected slot's DEASSERT or
+collapsed onto slot 0 (session C2), a per-cpu READ aliased by parity or onto slot 0 with the alias target IDLE (session E2:
+enable and software_interrupt_status, the class closure -- irqActive and cpu_irq were already covered by session E), the second walk after a delivery -- a still-pending IPI deasserted, a connected slot's DEASSERT or
 its `irqActive = 0' clear dropped, the deassert testing the wrong slot's latch (sessions B3, C3), and a deleted reassert in the SOFT arm
 (M_NOREASSERT: disclosed as debt on v2/v3 -- the clock's reassert carries DELIVERY -- and killed 29/31 by v4's noreenter rows, because
 the SOFT read-clear no longer triggers the deassert walk and the line stays asserted) --, a declined store to an absent slot
 (mask1/mask2/mask3 readbacks), and the third/fourth MASK labels.  Does NOT catch: a both-sided NULL guard instead of the bound
-(EQUIVALENT on every reachable configuration -- measured 22/22 in killtable/; the choice is warrant-based), the clock/timer route's own deassert timing (host-timer driven), the clock/timer route (host-timer
+(EQUIVALENT on every reachable configuration -- measured 34/34 in killtable4/, 22/22 on the v2 instrument in killtable/; the choice is warrant-based), the clock/timer route's own deassert timing (host-timer driven), the clock/timer route (host-timer
 driven, not steppable -- same loop as sio5), MASK1..3 written by a real guest kernel (no luna88k source on disk).
 
 Encodings (cpu_m88k.c, the same source as regress/luna_intmask_probe.py):  ld rD,rS1,IMM16 op26=0x05 ; st rD,rS1,IMM16
@@ -626,6 +635,45 @@
     s.close()
 
 
+# ------------------------------------------------------------------------------------------------- session E2 (-n 4, slots 2+3 only)
+def session_E2():
+    print("=== SESSION E2 (-n 4, FREE-RUNNING): slots 2 and 3 pending, slots 0 and 1 IDLE -- the alias targets DISAGREE")
+    s = boot(4)
+    if s is None:
+        row("cpu3 deliver23", "NOSTART"); row("cpu2 deliver23", "NOSTART"); row("others idle23", "NOSTART"); return
+    for c in (1, 2, 3):
+        s.send("focus %d" % c); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
+    s.send("focus 0")
+    s.send("r6=0x%08x" % SCRATCH)
+    for a, v, what in ((MASK0 + 8, 0x04000000, "MASK2"), (MASK0 + 12, 0x04000000, "MASK3"),
+                       (SOFT0 + 8, 1, "SOFT_INT2"), (SOFT0 + 12, 1, "SOFT_INT3")):
+        if not store(s, a, v):
+            died(s, "cpu3 deliver23", "died on the %s store on 4 cpus (slots 2 and 3 ARE connected here)" % what); s.close(); return
+    s.send("pc=0x%08x" % PARK)
+    s.send("breakpoint add 0x%08x" % (VBR + 8))
+    entered = set()
+    pcs = [None, None, None, None]
+    for attempt in (1, 2):
+        hit = s.cont_until_breakpoint(15.0)
+        if s.dead:
+            died(s, "cpu3 deliver23", "host died while free-running on 4 cpus"); s.close(); return
+        pcs = [s.reg("pc", cpu=c) for c in (0, 1, 2, 3)]
+        for c in (2, 3):
+            if pcs[c] == VBR + 8 and c not in entered:
+                entered.add(c)
+                s.send("focus %d" % c); s.send("pc=0x%08x" % PARK); s.send("focus 0")      # park the arrival off the vector
+        if not hit or len(entered) == 2:
+            break
+    row("cpu3 deliver23", "OK" if 3 in entered else "STOP",
+        "cpu 3 entered VBR+8 with slot 1 (its parity alias) IDLE" if 3 in entered else "cpu 3 never entered: entered=%s pcs=%s" % (sorted(entered), pcs))
+    row("cpu2 deliver23", "OK" if 2 in entered else "STOP",
+        "cpu 2 entered VBR+8 with slot 0 (its parity alias, and the [0] alias) IDLE" if 2 in entered else "cpu 2 never entered: entered=%s pcs=%s" % (sorted(entered), pcs))
+    idle = all(pcs[c] != VBR + 8 for c in (0, 1))
+    row("others idle23", "OK" if idle else "BADREGS",
+        "cpus 0 and 1 did not enter the vector" if idle else "cpu 0 or 1 took another slot's interrupt: pcs=%s" % pcs)
+    s.close()
+
+
 # ------------------------------------------------------------------------------------------------- sessions C / D
 def session_n2(deliver):
     name = "C" if deliver else "D"
@@ -687,6 +735,7 @@
     session_C4()
     session_n2(False)
     session_E()
+    session_E2()
     ok = sum(1 for _, r in rows if r == "OK")
     print("LUNAABS_RESULT=%d/%d" % (ok, len(rows)))
     halt_rows = [n for n, r in rows if r == "HALT"]
```
Product code in this repair: NONE.

## TABLE 5, MEASURED
| mutant (exact edit) | on frozen v5 (34 rows) | on frozen v6 (37 rows) | red rows on v6 |
|---|---|---|---|
| **M_ENP1** `enable = d->interrupt_enable[cpu & 1]` | **34/34 -- TOTAL ESCAPE** | 35/37 | cpu2 deliver23, cpu3 deliver23 |
| **M_SWP1** `if (d->software_interrupt_status[cpu & 1])` | **34/34 -- TOTAL ESCAPE** | 35/37 | the same two |
| M_EN0 `interrupt_enable[0]` | 29/32 (not a sweep) | 30/35 | |
| M_SW0 `software_interrupt_status[0]` | 30/32 (not a sweep) | 31/35 | |
| M_ENX1 `interrupt_enable[cpu ^ 1]` | 23/30 (not a sweep) | 26/33 | |
| M_ENSH1 `interrupt_enable[cpu >> 1]` | 29/32 (not a sweep) | 30/35 | |
| M_IRQACTIVEP1 (the pass-3 cell) | -- | 35/37 | cpu2/cpu3 deliver23 |
| M_SWLATCH 34/37, M_NODEASSERT 34/36, M_NOCLEAR 36/37, M_DEASSERT0 36/37, M_SKIP2 35/37, M_MASK30 35/37, M_SWONLY 32/36, M_IRQACTIVE0 31/37, M_AND1 32/37, M_MIN2 33/37, M_HARD1 26/35, M_SKIP1 30/35, M_NOASSIGN 19/33, M_NOREASSERT 34/36 | -- | all killed | |
| M_REVERT 30/32, M_OFFBY1 26/29, M_NULLA 31/32, M_LATCH 30/32, M_GUARDASSERT 31/32, M_CALLGUARD 31/33 | -- | PRE_FIX_SYMPTOM | the defect's own two routes |
| **M_NULLAB** (a both-sided NULL guard) | -- | **37/37** | none -- PREDICTED EQUIVALENT, measured so for the fifth table running |

**The two predicted sweeps are measured sweeps.**  Two seats predicted 34/34 without running anything; the frozen v5
instrument returns exactly that, and probe v6 kills both on the restored session's rows.  The four alias forms that
PRETABLE5 predicted would NOT sweep did not sweep -- that prediction was written to be refutable and held.

BASE **37/37** before the table and **37/37** after it; the clone `cmp`s clean against its baseline and left no
sentinel.  HEAD `83df95c` with this instrument: **30/32, PRE_FIX_SYMPTOM (soft1, siofirst)** -- the process ends on
exactly the defect's two routes.  Full log: `regress/artifacts/lunaabsentcpu/killtable5/driver.log`.

## THE CLOSURES NOW IN THE CONTRACT
* **the bound**: reverted / off by one / never assigned / hardcoded / clamped / at the callers / assert-only / latch-then-walk.
* **the slot axis**: every slot has a single-pending delivery row, a four-pending row (session E), and -- for slots 2 and 3 -- a row under a
  machine where their alias targets are IDLE (session E2).  Slots 0 and 1 need no E2 row: their `& 1` and `[0]` targets are themselves.
* **the per-CPU ARRAY axis, which is the class this repair closes**: `interrupt_enable`, `software_interrupt_status`, `irqActive` and
  `cpu_irq` each now have a configuration in which their alias target DISAGREES.
* **DISCLOSED, each with its reason**: the both-sided NULL guard (EQUIVALENT, warrant below); `M_SWEQ1` (the body tests nonzero-ness and
  never partitions the nonzero class); a slot-SPECIFIC fold of 2 and 3 (not a single-token edit); the clock/timer route (host-timer driven,
  not steppable); the MASK registers as a real guest kernel writes them (no luna88k OS source on disk).

## THE M_NULLAB WARRANT, NARROWED BY PASS 4 AND STILL OPEN FOR CHALLENGE
A both-sided NULL guard instead of the bound measures EQUIVALENT on every reachable configuration (34/34 across four tables), so it is
recorded as an alternative fix rather than a defect.  Pass 4 narrowed the warrant: `interrupt_handler_lookup` aborts on an UNKNOWN name, but
an **EMPTY** name installs non-NULL `no_interrupt_assert` / `no_interrupt_deassert` stubs, so "has a callback" and "slot < ncpus" differ in
MECHANISM and coincide here only because slots 1..3 use literal non-empty names.  **Is a measured equivalence with a stated expiry the right
disposition, or does the round owe a choice between the two forms?**

## THE ONE QUESTION
**Does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the SHIPPED COMPOSITE (fix v2b + probe v6)?**  The measuring seat
closed pass 4 with a DERIVED denominator rather than a list, and that derivation is the thing to attack: session C (slot 0 idle, slot 1
pending) reds unless `f(0)=0` and `f(1)=1`, which kills `[0]`, `[cpu^1]`, `[cpu>>1]`, `[cpu|1]`, `[cpu&2]`, `[cpu|2]` and `[3-cpu]`; session
E2 reds unless `f({2,3})` lies inside `{2,3}`, which kills `[cpu&1]`; session E constrains `f` **not at all**, which is exactly why v5 was
blind.  **Is that derivation right, and is "a function of `cpu` alone" the correct closure boundary -- or is that boundary itself the next
cell someone finds outside it?**

Second question, with the count named: of the pass-4 dispositions (ONE class closure with three new rows; TWO extra mutants replacing a
disclosure with a measurement; ONE product-comment L4; ONE records correction of an accepted-but-false refutation; ONE narrowed warrant on
the NULL-guard equivalence), **WHICH IS WRONG?**

VERDICT LINE FIRST (CLOSE THE CHAIN / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer with its denominator, then anything else,
under a page.
