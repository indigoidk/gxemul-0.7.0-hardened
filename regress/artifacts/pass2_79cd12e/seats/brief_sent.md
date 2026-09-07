# PASS 2 on commit `79cd12e` — the receipt that round did not file

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.
**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are
NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of them — say
so rather than reconciling.

**If you cannot read files that is expected** — the product diff is inlined in full below. Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. WHY THIS PASS IS HAPPENING AT ALL — and it is not a formality

`precommit_check.sh` section F refuses the next commit with:

    FAIL  NO PASS-2 RECEIPT for 79cd12e #502 pass 9-12 and #503
    FAIL  A round owes a pass 2 on its own diff.  R6 and R7 both shipped without one,
    FAIL  the second time one round after the first was caught and written down.

So this is a **retrospective** pass on shipped code. The late-dissent rule governs what your findings
can do:

* **WRONG RECORD → L4**, corrected in place. Closure is no shield for false prose.
* **MEASURED FALSE PASS** against the detector's floor, contract or obligations → **L2/L3**, fixed in
  a follow-up commit.
* **EVERYTHING ELSE, design dissents included → FILED as a new queue item**, carrying the dissent
  verbatim.

**Closure changes the LICENSE, never the truth-value.** Do not soften a finding because the code
already shipped — say what is true and I will route it.

## 2. WHAT SHIPPED — full disclosure, per the pass-2 checklist

    src/cpus/cpu_m88k.c              68 +   12 -     INLINED below
    src/devices/dev_luna88k.c        34 +    1 -     INLINED below
    src/devices/dev_wdc.c            12 +    1 -     INLINED below

    regress/luna_absentcpu_probe.py     783 +   NOT SHOWN -- new file, 783 lines; it is the
                                                 #503 detector and its content is summarised in §4
    regress/m88k_exc_probe.py           676 +   NOT SHOWN -- the #502 detector at v21
    regress/gate_m88k_rounding.sh       101 +   NOT SHOWN -- gate wiring for both probes
    regress/gate_sh_rounding.sh          21 +    5 -  NOT SHOWN -- unrelated round's wiring
    regress/asic_badaddr_probe.py         8 +    2 -  NOT SHOWN -- records-only
    regress/gdrom_cond_probe.py          15 +    3 -  NOT SHOWN
    regress/pit8253_latch_probe.py       12 +    1 -  NOT SHOWN
    ~70 files under regress/artifacts/          NOT SHOWN -- frozen evidence (kill tables,
                                                 frozen probe copies, PRETABLE blocks)
    CHANGELOG.md 596 +, OUTSTANDING_BUGS.md 231 +   NOT SHOWN -- records

**The three product files are the review target.** I am disclosing the rest rather than hiding it:
if you believe a NOT SHOWN file is load-bearing for a question below, say so and I will inline it in
a follow-up — that is a better outcome than you guessing.

## 3. THE TWO FIXES, as the round described them

**`#503 lunaabsentcpu` (`dev_luna88k.c`).** `reassert_interrupts()` walked a fixed CPU count and
called through a NULL interrupt pointer for CPUs the machine does not have. The fix captures
`d->ncpus` at DEVINIT and bounds the walk.

**`#502 m88kexcdeliver` (`cpu_m88k.c`).** The m88k exception core stopped EVERY guest CPU for a fault
raised on one. The round ran **twelve passes**; passes 9–12 closed a cell space the round's own
contract had disclosed.

**`dev_wdc.c`** carries an L4 records correction only — a census comment qualified to say it counts
helper CALLS, not successful pops.

## 4. THE QUESTIONS

### Q1 — THE PREMISE AUDIT, on the fix itself

For each of the two fixes: **is the guard right, and is it in the right place?** Specifically —

1. `#503` captures `ncpus` at **DEVINIT**. Is that value stable for the life of the device, or can
   the machine's CPU count change after init? If it can, the capture is a snapshot of a moving value
   and the bound is wrong.
2. `#502`'s repair closes cells in a state space. **Does the diff below actually close what its
   comments claim**, or does it close the cell the mutant used and leave the symmetric one open?
   That exact shape — *the original breach reproduced inside its own repair* — is what `#499` was
   caught doing, so it is worth checking rather than assuming.

### Q2 — THE SMALLEST EDIT

**What is the smallest edit to either fix that re-opens the defect and still passes its detector?**
Name the row you expect to stay green. This is the highest-yield question in the project's record and
it is the reason a retrospective pass is worth firing at all.

### Q3 — THE FLOOR, asked of the SHIPPED COMPOSITE

Per the repair-chain rule, review EFFORT is scoped to this diff, but the floor question is asked of
the shipped detector as a whole: **does a clean-sweep mutant exist in the clause-(d) DEPENDS-ON
enumeration** — the predicates dominating the edited lines, walked to the enclosing function
boundary, plus operand swaps drawn from fields the guarded body reads?

**If you find one, that is an L2 floor breach and it gets repaired**, however late. If you find none,
say so **with your denominator** — which cells, which mutant shapes you swept. *"Zero found"* and
*"zero looked for"* must not render the same.

### Q4 — WHAT DID THE ROUND'S OWN TWELVE PASSES MISS?

`#502` ran twelve passes and each of the first several found a real defect. A round that converges
after twelve passes has either genuinely converged or stopped looking. **You have the diff and none
of the fatigue.**

**If, while verifying a claim, you found something ELSE — say so.** Tonight's best findings arrived
that way, including two defects in code everyone had called correct.

---

## 5. THE PRODUCT DIFF, VERBATIM

Produced with `git show --format= 79cd12e -- 'src/*'` — the `--format=` matters: `git show | head`
inlines the COMMIT MESSAGE and can yield **zero diff lines**, which blinded three panels in one
session before the cause was found.

```diff
diff --git a/src/cpus/cpu_m88k.c b/src/cpus/cpu_m88k.c
index 71c5c08..2edd518 100644
--- a/src/cpus/cpu_m88k.c
+++ b/src/cpus/cpu_m88k.c
@@ -716,31 +716,38 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 		break;
 
 	case M88K_EXCEPTION_MISALIGNED_ACCESS:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_INTEGER_OVERFLOW:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_ERROR:
-		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_ERROR, "");
+		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_INFO, "");
+		implemented = true;	/*  m88kexcdeliver  */
 		break;
 
 	case M88K_EXCEPTION_SFU1_PRECISE:
@@ -772,6 +779,23 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 		    : VERBOSITY_INFO, "0x%03x", vector);
 	}
 
+	/*
+	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
+	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
+	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
+	 *  6.8.3), like the four this fallback never covered.  Before, any of them
+	 *  stopped EVERY guest CPU here: one divu by zero, in either mode, ended
+	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
+	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
+	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
+	 *  here, by design: SFU1_PRECISE/IMPRECISE (114/115; row m88kexcsfu1 --
+	 *  faithful delivery needs the rest of the SFU1 exception state, which
+	 *  the fork does not write) and vectors 11..113/116..127 (117 vectors
+	 *  with the two SFU1 ones), which no literal-constant raise site names
+	 *  but a supervisor tb0/tb1/tcnd can name directly (row
+	 *  m88kexctaildefault; the probe's resid50/sfu1h rows pin that they
+	 *  STILL halt).
+	 */
 	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
 		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
@@ -896,13 +920,45 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 			m88k_memory_transaction_debug_dump(cpu, 1);
 			break;
 
-#if 0
+		case M88K_EXCEPTION_MISALIGNED_ACCESS:
+		case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
+		case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
+		case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
 		case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
-			/*  TODO: Is it correct to continue on the instruction
-			    _after_ the division by zero? Or should the PC
-			    be backed up one step?  */
+		case M88K_EXCEPTION_INTEGER_OVERFLOW:
+		case M88K_EXCEPTION_ERROR:
+			/*  m88kexcdeliver: OUTSIDE A DELAY SLOT the common path above
+			    is already the architectural contract for these -- SXIP =
+			    the faulting instruction, SNIP = the next one, SFIP = SNIP+4,
+			    and rte resumes at SNIP (UM 6.4.3.1.4: "the processor
+			    hardware does not use the SXIP on return from an exception"),
+			    so the upstream doubt that sat here in an #if 0 ("should the
+			    PC be backed up one step?") is answered NO: 6.5.x/6.8.3 say
+			    the destination register is unchanged (6.6: and the carry
+			    bit, for the overflow case), and a handler that wants
+			    re-execution arranges SNIP/SFIP itself.  INSIDE a delay slot
+			    the else-arm above ("Perhaps something like this could
+			    work") is upstream's guess and the manual disagrees (Table
+			    6-3: the shadows copy XIP/NIP/FIP, and UM 6.2 defines FIP as
+			    the taken branch's target while the branch executes, so for
+			    a fault in its delay slot NIP = target, FIP = target+4) --
+			    pre-existing, now reachable by ordinary faults, row
+			    m88kdslotshadow.
+			    Without these labels the classes reached the default: below,
+			    which stops the cpu -- the one-site fix was measured to do
+			    exactly that; with them, nothing below 128 reaches that
+			    default any more (it is unreachable code kept as the
+			    tripwire for an eighth class).  ERROR arrives here by TWO
+			    routes: the SFRZ re-route above (a fault inside a handler,
+			    shadows deliberately frozen at the FIRST fault's values --
+			    SXIP then names that first fault, not this one) and a
+			    supervisor tb0/tb1/tcnd naming vector 10 directly (shadows
+			    updated normally when that trap is taken UNFROZEN; inside a
+			    handler it takes the is_trap exemption above and arrives
+			    here with the shadows frozen).  Not modelled, disclosed: scoreboard
+			    capture (the shadow-update path writes SSBR = 0; a frozen
+			    SSBR keeps its old value) and fcr2/fcr4/fcr5 for the divide.  */
 			break;
-#endif
 
 #if 0
 		// TODO: Read up more about SFU1 exceptions and how the
diff --git a/src/devices/dev_luna88k.c b/src/devices/dev_luna88k.c
index 41cbf1b..61a63ad 100644
--- a/src/devices/dev_luna88k.c
+++ b/src/devices/dev_luna88k.c
@@ -87,6 +87,14 @@
 
 
 struct luna88k_data {
+	/*  #503 (lunaabsentcpu): the number of CPUs actually INTERRUPT_CONNECTed at
+	    DEVINIT.  Slots at or above this index were never connected, so their
+	    cpu_irq[].interrupt_assert/deassert pointers are the memset's NULL.  The
+	    walk bound and the connect predicate carry the same VALUE -- not one
+	    shared field: the connect predicates read machine->ncpus directly while
+	    the walk reads this snapshot.  The equality holds because nothing in
+	    this fork mutates the count after device init (pass 2, codex).  */
+	int		ncpus;
 	struct interrupt cpu_irq[MAX_CPUS];
 	int		irqActive[MAX_CPUS];
 	uint32_t	interrupt_enable[MAX_CPUS];
@@ -167,7 +175,7 @@ static void reassert_interrupts(struct luna88k_data *d)
 {
 	int cpu;
 
-	for (cpu = 0; cpu < MAX_CPUS; cpu++) {
+	for (cpu = 0; cpu < d->ncpus; cpu++) {		/*  #503  */
 		// printf("cpu%i: status = 0x%08x, enable = 0x%08x\n",
 		//	cpu, d->interrupt_status, d->interrupt_enable[0]);
 
@@ -1038,6 +1046,31 @@ DEVINIT(luna88k)
 		exit(1);
 	}
 
+	/*  #503 (lunaabsentcpu): bound reassert_interrupts() to the slots connected
+	    above.  It walked all MAX_CPUS and called the NULL interrupt_assert of an
+	    unpopulated slot: on the default one-cpu machine a guest store of
+	    0xfc000000 to INT_ST_MASK1 followed by a store to SOFT_INT1 (or any device
+	    line whose bit that mask enables) killed the emulator with SIGSEGV --
+	    measured, regress/luna_absentcpu_probe.py.  Captured below the `ncpus > 4'
+	    exit above -- but note what that does and does not buy, because the
+	    pass-2 revision was made on a claim codex then refuted: RELOCATING THE
+	    CAPTURE DOES NOT REMOVE THE DEPENDENCE ON THAT EXIT.  Above or below, the
+	    assignment supplies the same bound whenever execution reaches the walk,
+	    since the walk is downstream of the exit either way; both placements rely
+	    on initialization rejecting excessive counts.  A clamp to MAX_CPUS is
+	    what would make the walk independent of them, and the addition licence
+	    refuses one without a measured delta -- no accepted configuration fails.
+	    TWO exits bound the value, not one: machine_luna88k.c carries its own
+	    `ncpus > 4' guard AFTER its device_add, so deleting the exit above lets
+	    DEVINIT capture 5 and the MACHINE layer ends the run before any guest
+	    instruction -- measured both ways at -n 5.  Deleting BOTH is what would
+	    walk cpu_irq[4].  The
+	    absent slots' MASK/SOFT registers stay guest-writable storage with
+	    readback (a board-model question, row lunaabsentmaskdecl).  Pre-existing
+	    upstream (the HACK comment's per-count connects and this walk are the
+	    0.7.0 import).  */
+	d->ncpus = devinit->machine->ncpus;
+
 	add_cmmu_for_cpu(devinit, 0, CMMU_I0, CMMU_D0);
 	add_cmmu_for_cpu(devinit, 1, CMMU_I1, CMMU_D1);
 	add_cmmu_for_cpu(devinit, 2, CMMU_I2, CMMU_D2);
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index 18cc64e..efddc89 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -1139,7 +1139,18 @@ DEVICE_ACCESS(wdc)
 				    asked for. The reads above take one byte,
 				    two if len >= 2, four only if len == 4 --
 				    so a 3- or 8-byte access consumes 2 (widths
-				    1..8 pop 1, 2, 2, 4, 2, 2, 2, 2; "1 or 2" until 2026-09-05)
+				    1..8 ATTEMPT 1, 2, 2, 4, 2, 2, 2, 2 pops --
+				    those are CALL counts, and the pops succeed
+				    only while bytes remain: wdc_get_inbuf()
+				    returns (uint64_t) -1 on an empty ring
+				    WITHOUT advancing the tail, so with q bytes
+				    queued a width-w access pops min(q, calls).
+				    "1 or 2" until 2026-09-05; the unqualified
+				    pop counts until 2026-09-06, when a pass-2
+				    seat read the helper instead of this
+				    comment.  NOTE `consumed' below is computed
+				    from `len' alone and so counts ATTEMPTS
+				    too -- row wdcconsumedattempts)
 				    while `len` says 3 or 8. Subtracting the
 				    requested length let atapi_len step PAST
 				    zero, which its `== 0` test then never
```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
