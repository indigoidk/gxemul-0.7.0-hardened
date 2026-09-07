# PASS 6 -- `lunaabsentcpu` (#503): the pass-2 REVISION of the fix owes its own pass.  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a device model in a hardware simulator for obsolete workstations (GXemul 0.7.0, a
maintained fork): the LUNA-88K interrupt controller's per-CPU walk.  Plain engineering vocabulary; no security framing
is intended or wanted, and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`.  Ignore any other `src/` you find** -- three pristine-2021 upstream copies
sit under the project root and are NOT this fork.  The file is `GXEMUL-SEC/src/devices/dev_luna88k.c`.

**If you cannot read files that is expected -- every fact is inlined below.  Name any premise you cannot settle from
this packet rather than guessing; an honest "not checkable from the packet" outranks a confident guess.**  VERDICT LINE
FIRST.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
**This is a repair made in response to a pass 2, and the standing rule is that such a repair owes its own pass** --
because the obligation follows the MATERIAL, not the narrative.  A sibling chain on another row has just spent three
consecutive passes finding that each repair reproduced, inside itself, the defect class it was repairing.  **Assume this
one does too until you have tested that.**  Check the premises, not just the derivations.

## THE DEFECT (settled on passes 1-2; re-inlined because it is load-bearing for every question below)
`reassert_interrupts()` walked `for (cpu = 0; cpu < MAX_CPUS; cpu++)` and called
`cpu_irq[cpu].interrupt_assert(...)`.  DEVINIT only `INTERRUPT_CONNECT`s the slots the machine actually has, and the
struct is `memset` to zero, so **an unpopulated slot's function pointer is NULL**.  On the default one-CPU machine a
guest store of `0xfc000000` to `INT_ST_MASK1` followed by a store to `SOFT_INT1` -- or to any device line whose bit that
mask enables -- dereferences NULL and kills the emulator with SIGSEGV.  **Measured**, `regress/luna_absentcpu_probe.py`.
Pre-existing upstream: the HACK comment's per-count connects and this walk are both the 0.7.0 import.

## THE FIX UNDER REVIEW, verbatim (the ONLY product-code change; three hunks)
```c
 struct luna88k_data {
+	/*  #503 (lunaabsentcpu): the number of CPUs actually INTERRUPT_CONNECTed at
+	    DEVINIT.  Slots at or above this index were never connected, so their
+	    cpu_irq[].interrupt_assert/deassert pointers are the memset's NULL.  The
+	    walk bound and the connect predicate are the same number on purpose.  */
+	int		ncpus;
 	struct interrupt cpu_irq[MAX_CPUS];
```
```c
-	for (cpu = 0; cpu < MAX_CPUS; cpu++) {
+	for (cpu = 0; cpu < d->ncpus; cpu++) {		/*  #503  */
```
```c
 	if (devinit->machine->ncpus > 4) {
 		printf("LUNA 88K can't have more than 4 CPUs.\n");
 		exit(1);
 	}
+
+	/*  #503 ... Captured BELOW the `ncpus > 4' exit above, so the value stored
+	    here is <= MAX_CPUS.  TWO exits bound it, not one: machine_luna88k.c
+	    carries its own `ncpus > 4' guard AFTER its device_add, so deleting the
+	    exit above lets DEVINIT capture 5 and the MACHINE layer ends the run
+	    before any guest instruction -- measured both ways at -n 5.  Deleting
+	    BOTH is what would walk cpu_irq[4].  ...  */
+	d->ncpus = devinit->machine->ncpus;
```

## WHAT THE PASS-2 REVISION CHANGED, and why it is not "cannot hurt"
Pass 1's form captured `ncpus` **ABOVE** the `> 4` exit.  The Fable pass-1 seat asked for the capture to move below it
(or for a clamp); the minimax pass-2 seat supplied the reason that makes it more than tidiness: **with the capture above
the exit, that exit became LOAD-BEARING for the walk's bound**, where pre-fix the walk was bounded by `MAX_CPUS`
whatever `ncpus` was.  So the revision removes a dependency the fix itself had introduced.  A comment claiming
"delete that exit and a 5-cpu machine would walk `cpu_irq[4]`" was CORRECTED in the same revision: there are TWO exits,
and deleting only the DEVINIT one is caught by `machine_luna88k.c` before any guest instruction runs -- measured both
ways at `-n 5`.

## THE THREE QUESTIONS
1. **Does this revision reproduce the defect it repairs?**  The defect class is *a bound and the thing it bounds
   getting out of step*.  The fix makes `d->ncpus` the single number used by both the connect predicate and the walk.
   **Is there any path that populates `cpu_irq[]` beyond `d->ncpus`, or that changes `machine->ncpus` after DEVINIT
   captures it?**  If `machine->ncpus` can be mutated later (CPU hot-add, a machine that adds CPUs after devices), the
   capture is a snapshot of a moving value and the fix is wrong in a new way.
2. **Is the DECLINE the right disposition for the absent slots' registers?**  The absent slots' MASK and SOFT registers
   remain guest-writable storage with readback.  The de-fatalisation option set here has six members -- DELETE,
   DECLINE (silent), DECLINE + LATCHED ANNOUNCE, ACCEPT, FAULT (model the space unmapped, the `dev_unreadable.c`
   idiom), BACKED ACCEPT.  **This fix takes none of them for the registers** -- it leaves them accepting and only bounds
   the WALK.  Is that right, or does a store to an absent CPU's mask deserve one of the six?  (Filed separately as
   `lunaabsentmaskdecl`; I want to know if it should have been in-round.)
3. **The detector**: `regress/luna_absentcpu_probe.py` v7, 37 rows.  Its kill table killed `M_NOASSIGN`, `M_HARD1`,
   `M_LATCH`, `M_NULLA`, `M_NULLAB`, `M_CALLGUARD`, `M_GUARDASSERT`, `M_NOREASSERT`.  **What is the smallest edit to
   the fix that still passes all 37 rows?**  Name the mutant text and the row you expect to redden once it is closed.

## THE SECOND QUESTION, with the count named
Of this revision's dispositions -- (i) capture below the exit rather than clamp; (ii) `int` rather than `unsigned`;
(iii) the walk bound and connect predicate sharing one number; (iv) leaving the absent slots' registers accepting;
(v) the corrected two-exits comment; (vi) filing `lunaabsentmaskdecl` rather than fixing it in-round --
**WHICH IS WRONG?**  Assume at least one is.

VERDICT LINE FIRST (SHIP / ONE MORE REPAIR: <which> / DO NOT SHIP), then the answer, then anything else.  Under a page.
