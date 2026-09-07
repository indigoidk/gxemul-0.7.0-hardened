# PASS 2 -- `lunaabsentcpu` (#503): the DIFF and its detector.  Tree `GXEMUL-SEC/src/`, HEAD `83df95c`.  2026-09-06 ~09:50.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's board model (GXemul 0.7.0, hardened fork): `src/devices/dev_luna88k.c`,
the OMRON LUNA-88K interrupt controller model.  The "guest" is the operating system inside the emulator.  Plain engineering vocabulary:
"the emulator process exits", "a slot that was never connected", "a bounded walk".  **If you cannot read files that is expected -- every
fact is inlined; name any premise you cannot settle rather than guessing.**  Tree under review: `GXEMUL-SEC/src/` (three pristine-2021 copies
under the project root are NOT this fork).  **VERDICT LINE FIRST.**  Cite by grep anchor.  `python3` in git-bash is a Windows Store stub; a
file-reading seat that needs Python uses `C:\Users\User00\AppData\Local\Programs\Python\Python312\python.exe`.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
Check the premises, not just the derivations.  This brief's author has already been wrong once in this round (the filing said "#438's probe
stores to MASK1 with bit 26 clear"; 0x84000100 has bit 26 SET -- the probe missed the defect because nothing was pending and it never
stored SOFT_INT1).  Where a claim below is checkable, check it.

## THE DEFECT (measured, HEAD 83df95c)
`reassert_interrupts()` walks all `MAX_CPUS` (4) slots and calls `INTERRUPT_ASSERT(d->cpu_irq[cpu])` -- a bare call through a function
pointer -- but DEVINIT connects `cpu_irq[1..3]` only for `ncpus >= 2/3/4`; on the default ONE-cpu luna-88k the pointers are the memset's
NULL.  Two ordinary supervisor stores -- `INT_ST_MASK1 <- 0xfc000000` then `SOFT_INT1 <- 1` -- make the walk find `status & enable`
non-zero on slot 1 with `irqActive[1] == 0` and call NULL: the emulator dies with SIGSEGV.  The SIO device line 5 (bit 30; a WR1 TX_IE
store to 0x51000004) reaches the same walk with NO software-interrupt store.  Witness, rung 3, unmodified `-e luna-88k`:
`regress/artifacts/lunaabsentcpu/probe_v2_head.out` -- rows `soft1` and `siofirst` HALT "HOST DIED (signal 11)"; 15/17 (the denominator
drops from 22 because the host dies mid-session and the remaining rows of that session cannot run).

## SETTLED PREMISES, RE-INLINED (each a QUESTION if you can check it)
1. The walk (anchor `static void reassert_interrupts`): per slot `status = d->interrupt_status` (machine-wide: the six shared device lines,
   `1 << (line + 25)`, lines 1..6 -> bits 26..31), `enable = d->interrupt_enable[cpu]`, `if (d->software_interrupt_status[cpu]) status |=
   (1 << 26)`, then `if (status & enable) { if (!d->irqActive[cpu]) INTERRUPT_ASSERT(d->cpu_irq[cpu]); d->irqActive[cpu] = 1; } else {
   if (d->irqActive[cpu]) INTERRUPT_DEASSERT(d->cpu_irq[cpu]); d->irqActive[cpu] = 0; }`.
2. `INTERRUPT_ASSERT(istruct)` is `(istruct).interrupt_assert(&(istruct))` -- no NULL check (src/include/interrupt.h).
3. DEVINIT: `memset(d, 0, ...)`; `INTERRUPT_CONNECT(devinit->interrupt_path, d->cpu_irq[0])`; then under `// HACK for trying out CPUs 1, 2
   and 3`: `if (devinit->machine->ncpus >= 2) INTERRUPT_CONNECT("machine[0].cpu[1]", d->cpu_irq[1]);` and likewise `>= 3` / `>= 4`.  Later
   in DEVINIT an `ncpus > 4` check exits the process at init time (so the walk never runs with ncpus > MAX_CPUS).
4. The store arms index by ADDRESS (`cpunr = (addr - INT_ST_MASK0) / 4`, likewise SOFT_INT0..3) and never compare with ncpus; both call
   `reassert_interrupts(d)` after the store.  `case RESET_CPU_ALL:` in the same switch DOES bound by `cpu->machine->ncpus`.
5. Delivery is observable only free-running (`cpu_dyntrans.c`: no interrupts while single-stepping): the probe parks the cpu on `br .`,
   breakpoints VBR+8 (the INTERRUPT vector), and `continue`s.  A cpu entering VBR+8 with PSR 0x8000000b / EPSR 0x80000000 is the channel.
6. Pass-1 rulings (nine seats; Opus measured 15 binaries, Fable ruled the option set): fix = option (a) ALONE -- bound the WALK to the
   connected-slot count captured at DEVINIT; the absent slots' MASK/SOFT registers stay guest-writable storage with readback (a board-model
   question, filed `lunaabsentmaskdecl`); the SIO line-5 row is MANDATORY; readbacks are asserted, not only survival.  Fable also proposed an
   alternative (F4): bound the reassert CALL in the two store arms and leave the walk untouched -- built as mutant M_CALLGUARD below.

## THE DIFF, VERBATIM (the fix as it will land in `GXEMUL-SEC/src/devices/dev_luna88k.c`; derived from SEC by the fix script and measured
## in a scratch clone -- SEC does not carry it yet because round #502 is uncommitted and shares the record files)
```diff
--- GXEMUL-SEC/src/devices/dev_luna88k.c	2026-08-19 18:08:45.193189600 -0500
+++ _scratchpad/lunaabs/killtable/baseline_dev_luna88k.c	2026-09-06 09:36:35.687520700 -0500
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
 
@@ -965,6 +970,18 @@
 	CHECK_ALLOCATION(d = (struct luna88k_data *) malloc(sizeof(struct luna88k_data)));
 	memset(d, 0, sizeof(struct luna88k_data));
 
+	/*  #503 (lunaabsentcpu): bound reassert_interrupts() to the slots connected
+	    below.  It walked all MAX_CPUS and called the NULL interrupt_assert of an
+	    unpopulated slot: on the default one-cpu machine a guest store of
+	    0xfc000000 to INT_ST_MASK1 followed by a store to SOFT_INT1 (or any device
+	    line whose bit that mask enables) killed the emulator with SIGSEGV --
+	    measured, regress/luna_absentcpu_probe.py.  The absent slots' MASK/SOFT
+	    registers stay guest-writable storage with readback (a board-model
+	    question, row lunaabsentmaskdecl); the `ncpus > 4' exit below still
+	    bounds this value to the array size.  Pre-existing upstream (the HACK
+	    comment's per-count connects and this walk are the 0.7.0 import).  */
+	d->ncpus = devinit->machine->ncpus;
+
 	// TODO: Values should correspond to the bootable disk id!
 	const int nsymbols = 2;
 	const char *s[2] = { "boot_unit", "boot_partition" };
```

## THE DETECTOR (`regress/luna_absentcpu_probe.py` v2, frozen md5 5a133aaa; its own header, verbatim, ends this section)
Rows: session A (one cpu, stepped): live, devsig, slot0, mask1, soft1, sio5, sio5clr, mask2, mask3, live2; session A2: siofirst (the
TX_IE store FIRST, no SOFT store); session B (one cpu, free-running): cpu0 setup, slot0 deliver (pc == VBR+8), slot0 shadow; session C
(`-n 2`): two cpus, cpu1 setup, mask1 land, survive, cpu1 deliver (cpu 1 enters VBR+8), cpu1 shadow, cpu0 parked; session D (`-n 2`,
nothing pending): nodeliver ctl.  22 rows; `LUNAABS_RESULT=<ok>/<rows>`, `LUNA_ABSENTCPU_WITNESS=PASS|PRE_FIX_SYMPTOM|FAIL`, `LUNAABS_DONE`.
Gate wiring (to land with the fix, beside the #438 luna probe in `gate_m88k_rounding.sh`): run it with `"$PMAX" "$IMAGES"`, pin
`LUNAABS_DONE`, `LUNA_ABSENTCPU_WITNESS=PASS`, `LUNAABS_RESULT=22/22`, and the named rows `soft1`, `siofirst`, `cpu1 deliver`,
`nodeliver ctl` OK.

```
lunaabsentcpu (#503) -- rung-3 WITNESS and DETECTOR for dev_luna88k.c reassert_interrupts().

THE DEFECT.  reassert_interrupts() walked all MAX_CPUS (4) slots and called INTERRUPT_ASSERT(d->cpu_irq[cpu]) --
a direct call through the struct's function pointer -- while DEVINIT connected cpu_irq[1..3] only under
`ncpus >= 2/3/4' and memset()s the device to zero.  The INT_ST_MASK0-3 and SOFT_INT0-3 store arms take their slot
from the ADDRESS (`cpunr = (addr - INT_ST_MASK0) / 4') with no ncpus bound, so on the default ONE-cpu luna-88k a
guest word store of 0xfc000000 to INT_ST_MASK1 (0x65000004) arms slot 1, and a following store of 1 to SOFT_INT1
(0x69000004) sets that slot's pending bit and calls reassert SYNCHRONOUSLY inside the store: a NULL function
pointer is called and the emulator process dies with SIGSEGV (MEASURED 2026-09-05: signal 11, no diagnostic).
Any device line whose bit the armed slot's mask enables kills the same way on a running guest -- the clock is line
6 (bit 31); the SIO TX-interrupt route (line 5, bit 30) is SYNCHRONOUS and guest-drivable while stepping (session A2).

THE FIX (#503, option (a) of the pass-1 set): `d->ncpus' captured at DEVINIT and the walk bounded `cpu < d->ncpus'.
The absent slots' registers stay guest-writable storage with readback (a MODEL question filed as lunaabsentmaskdecl).

ONE cold-debugger session per SESSION below, real m88k guest instructions (st/ld through real address decode and
real memory_rw), COMMITTED UNMODIFIED machine description (`-e luna-88k' + the committed rig image; `-n 2' for the
two-cpu accept rows is a command-line configuration of the same description, not a machine edit).  EVERY PLANTED
WORD IS DISASSEMBLED AND ITS TEXT CHECKED BEFORE IT IS STEPPED.

  session A  (1 cpu, stepped)          row          CHANNEL: the mutant it kills / the observable that differs
    C1  RAM word through the same decode            live         identity (floor c): 0x12345678 back
    C2  MASK0 <- 0xfc000000; ld = 0x00fc0000        devsig       RAM-vs-device: the handler's own >>8
    A1  SOFT_INT0 <- 1 on the CONNECTED slot 0      slot0        attribution: the same two stores survive; readback 1
    A2  MASK1 <- 0xfc000000 ALONE; ld = 0x00fc0000  mask1        option-(b)-shaped edits (a declined store reads 0)
    W1  SOFT_INT1 <- 1: THE WITNESS                 soft1        M_REVERT/M_OFFBY1/M_NULLA/M_LATCH/M_GUARDASSERT: host alive.
                                                                 TWO channels in one row -- the STORE exercises ASSERT, the
                                                                 READBACK (== 1; read clears the pending bit -> the next
                                                                 reassert takes the DEASSERT arm) exercises DEASSERT.
                                                                 Three mutants die on the readback, not the store.
    S1  SIO cmd <- 0x01 then 0x02 (WR1 TX_IE): a    sio5         M_CALLGUARD (bound the reassert CALL in the store arms,
        device line (5, bit 30) asserts and walks                loop untouched: W1 survives, this one still walks slot 1).
        the loop with slot 1 armed; ld MASK1 =                   The measured form of "the next enabled device line kills".
        0xa0fc0000 (level 5 in 31..29, mask in 23..16)
    S2  SIO cmd <- 0x28 (RESET_TX_IP), then WR1 <- 0 sio5clr     the DEASSERT walk with a line pending on slot 1 (an
        ld MASK1 = 0x00fc0000                                    ASSERT-only NULL guard dies here); level back to 0
    M2  MASK2 <- 0x84000100; ld = 0x00840001 (23..0) mask2       es438cells: the third label stores and reads back
    M3  MASK3 <- 0x84000100; ld = 0x00840001         mask3       es438cells: the fourth label
    C3  RAM again                                   live2        the machine still executes after everything above
  session A2 (1 cpu, stepped)  MASK1 armed then S1 FIRST: the SIO route's own pre-fix death, ordered before any SOFT store
    sio-first                                        siofirst     PRE-FIX: HALT at the TX_IE store (line 5 walks slot 1)
  session B  (1 cpu, FREE-RUNNING)  MASK0 <- 0x04000000 (bit 26 ONLY: no device line can raise it), SOFT_INT0 <- 1,
        VBR <- 0x40000 (RAM), PSR <- 0x80000000 (IND CLEAR), `br .' planted at VBR+8, breakpoint there, `continue'
    cpu0 setup / slot0 deliver / slot0 shadow        M_NOASSIGN (ncpus never assigned -> 0: the loop never runs, slot 0
                                                     is never asserted, every SURVIVAL row is green) and M_NOREASSERT2:
                                                     cpu 0 enters its INTERRUPT vector (pc == 0x40008), PSR 0x8000000b,
                                                     EPSR 0x80000000.  Stepping cannot deliver (`if (!single_step)').
  session C  (`-n 2', FREE-RUNNING)  cpu 1: VBR 0x40000, PSR 0x80000000, parked at `br .'; cpu 0 steps MASK1 <-
        0x04000000 and SOFT_INT1 <- 1, parks; breakpoint VBR+8; `continue'
    two cpus / cpu1 setup / mask1 land / survive /   M_HARD1 (`d->ncpus = 1' hardcoded -- the clause-(d) null repair:
    cpu1 deliver / cpu1 shadow / cpu0 parked         a TOTAL ESCAPE of every 1-cpu row, measured 20/20): cpu 1 enters
                                                     its vector (pc == 0x40008), IND set, cpu 0 still parked.
  session D  (`-n 2', control)  the same without the SOFT_INT1 store: NO vector entry within the wait
    nodeliver ctl                                    makes the two delivery rows attributable

RESULT words per row: OK / HALT (the host died: signal / exit) / BADREGS (a value assert failed) / STOP (no vector entry
before the wait ran out) / NOSTART.  Output: `LUNAABS_ROW=<name> RESULT=<word> ...' per row, `LUNAABS_RESULT=<ok>/<rows>',
`LUNA_ABSENTCPU_WITNESS=PASS|PRE_FIX_SYMPTOM|FAIL ...', `LUNAABS_DONE'.  Exit status is non-zero on any row that is not OK
(a gate can rely on it).  On HEAD the witness reads PRE_FIX_SYMPTOM at row soft1 (session A) and at siofirst (session A2).

CONTRACT (clause e): catches the walk bound reverted or off by one, an ASSERT-only NULL guard, a decline-once latch on
either arm, a guard moved inside the branch, the reassert CALL bounded in the store arms instead of the walk (sio5), the
bound never assigned (session B), the bound hardcoded to 1 (session C), a declined store to an absent slot (mask1/mask2/
mask3 readbacks), and the third/fourth MASK labels.  Does NOT catch: a both-sided NULL guard instead of the bound
(EQUIVALENT on every reachable configuration -- measured 20/20 + 8/8; the choice is warrant-based), a deleted reassert
in the SOFT arm alone (the clock's own reassert carries the delivery; disclosed debt), the clock/timer route (host-timer
driven, not steppable -- same loop as sio5), MASK1..3 written by a real guest kernel (no luna88k source on disk).

Encodings (cpu_m88k.c, the same source as regress/luna_intmask_probe.py):  ld rD,rS1,IMM16 op26=0x05 ; st rD,rS1,IMM16
op26=0x09 ; br . = c0000000.
usage: luna_absentcpu_probe.py <gxemul-binary> <images-dir>
```

## TABLE 1, MEASURED (`regress/artifacts/lunaabsentcpu/killtable/`.  PRETABLE_lunaabs.out was written before the table's 09:36:30 start
## (BASE.out is 09:37:19) but its mtime is now 09:45, because the dated correction was APPENDED to the same file after the table --
## so the order is asserted from this session's sequence of writes, NOT provable from the mtime; the same happened to #502's
## PRETABLE6.  Corrections go to a separate file from now on.  Baseline = SEC + the fix script, re-derived after every mutant.)
| mutant (exact edit against the fixed source) | score | red rows | reading |
|---|---|---|---|
| M_REVERT: walk `cpu < MAX_CPUS` again | 15/17 PRE_FIX_SYMPTOM | soft1, siofirst HALT (host died) | floor (b) |
| M_OFFBY1: `cpu <= d->ncpus` | 15/17 PRE_FIX_SYMPTOM | soft1, siofirst | one past |
| M_NOASSIGN: `d->ncpus` never assigned (0) | 17/19 FAIL | slot0 deliver, cpu1 deliver | no delivery anywhere |
| M_HARD1: `d->ncpus = 1` | 19/20 FAIL | cpu1 deliver | clause (d): every 1-cpu row green; only the -n 2 row sees it |
| M_SKIP1: walk unbounded, slot 1 skipped | 19/20 FAIL | cpu1 deliver | single-killer cell |
| M_NULLA: ASSERT-only NULL guard instead of the bound | 16/17 PRE_FIX_SYMPTOM | soft1 | the DEASSERT walk dies |
| M_NULLAB: both-sided NULL guard | 22/22 PASS | -- | EQUIVALENT (predicted; disclosed) |
| M_LATCH: decline the absent slot ONCE, then walk it | 15/17 PRE_FIX_SYMPTOM | soft1, siofirst | latch-then-deliver |
| M_GUARDASSERT: bound applied to the ASSERT call only | 16/17 PRE_FIX_SYMPTOM | soft1 | the DEASSERT walk still reaches NULL |
| **M_CALLGUARD: the F4 alternative (bound the reassert CALLS in the two store arms, walk untouched)** | **16/18 PRE_FIX_SYMPTOM** | **sio5, siofirst HALT** | **predicted EQUIVALENT -- KILLED: the SIO line reaches the walk through a THIRD caller (the device interrupt line), which the call-site guard does not cover.  The alternative is NOT a correct fix; the row that shows it is the sio5 row pass 1 made mandatory** |
| M_NOREASSERT: the SOFT arm no longer reasserts | 22/22 PASS | -- | disclosed debt confirmed: the clock's reassert carries delivery |
BASE 22/22 PASS before and after; clone `cmp`-clean against the re-derived baseline, sentinel clear.  HEAD (the witness) 15/17
PRE_FIX_SYMPTOM as above.  Prediction errors, recorded in the PRETABLE correction: the killing rows are soft1/siofirst, not mask1 (a MASK1
store with nothing pending walks slot 1 without calling anything); M_CALLGUARD was predicted equivalent and is killed.

## CONTRACT (what the detector claims and does not)
Catches: the walk reaching an unconnected slot by any route (device line, software interrupt, mask store), the bound being absent, one
too large, hardcoded, or applied to one call side only, a latch-then-deliver, and the alternative call-site fix; pins delivery to slot 0
(one cpu) and slot 1 (two cpus) with the vector entry and PSR/EPSR, and that nothing is delivered with nothing pending.  Does NOT catch:
a both-sided NULL guard (equivalent on every reachable configuration -- disclosed); the SOFT arm's redundant reassert (M_NOREASSERT: the
clock's reassert carries delivery -- disclosed debt); the ncpus > 4 configuration (DEVINIT exits at init time -- out of the guest's
reach); the absent slots' register semantics (storage with readback, as upstream; filed lunaabsentmaskdecl).

## QUESTIONS
Q1 THE DIFF: is it right and complete?  The capture `d->ncpus = devinit->machine->ncpus` sits right after the memset and BEFORE the
   existing `ncpus > 4` exit (Fable pass 1 said capture AFTER that exit or clamp) -- is the order material, given that exit ends the process
   at init time?  Is there any caller of reassert_interrupts() -- the SIO line, the clock tick, the two store arms -- for which the bound is
   wrong?  Is a walk bound the right member of the six-membered option set versus a decline of the STORES to absent slots (the pass-1 ruling
   said (a) alone; M_CALLGUARD now measures why the call-site form is insufficient)?
Q2 THE FLOOR: does a clean-sweep mutant exist in the (d) DEPENDS-ON enumeration of the shipped composite -- the predicate `cpu < d->ncpus`
   and the fields the walk's body reads (interrupt_status, interrupt_enable[cpu], software_interrupt_status[cpu], irqActive[cpu],
   cpu_irq[cpu]) -- with joint cells where the body tests them ({slot} x {pending} x {irqActive})?  Give the exact edit and the row that
   should have caught it, or CLOSE with your own denominator.
Q3 THE RECORDS: the ledger row `lunaabsentcpu` (HIGH, open) and its OUTSTANDING_BUGS block name option (a) alone and the cpu-1-asserting
   accept channel; the CHANGELOG #503 block is not yet written.  What must the block carry beyond the table above (the M_CALLGUARD finding,
   the prediction corrections, the witness numbers 15/17 with their denominator note)?
Q4 WHICH OF THE MAIN LOOP'S DISPOSITIONS IS WRONG?  Proposed: the fix as diffed; the detector with 22 rows wired in gate 11; M_NULLAB
   disclosed equivalent; M_NOREASSERT disclosed debt; M_CALLGUARD recorded as the alternative fix measured WRONG (a pass-1 proposal
   refuted by measurement, not a defect in anything shipped); `lunadefaultstop` (the `default:` arm's graceful stop) and `es438cells`
   unchanged; `lunaabsentmaskdecl` unchanged.  Name the wrong one(s).

VERDICT LINE FIRST (SHIP / SHIP WITH REPAIR: <which> / DO NOT SHIP), then Q1-Q4, then anything else, under a page.
