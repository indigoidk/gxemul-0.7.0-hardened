# `alphavmkill` PASS 1 -- one guest virtual address ends the emulator process, inside the Alpha translator

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  **VERDICT LINE FIRST.**  **THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** at HEAD
`cdbe7d7` (`memory_alpha.c` unchanged by the working tree).  Pristine-2021 copies elsewhere under the project root are NOT this fork.  **If you cannot read files
that is expected** -- every fact you need is inlined; name any premise you cannot settle.

**Seats that read files: read ONLY** `GXEMUL-SEC/src/cpus/memory_alpha.c`, `GXEMUL-SEC/src/cpus/memory_rw.c`,
`GXEMUL-SEC/src/cpus/cpu_alpha_instr_loadstore.c`, `GXEMUL-SEC/src/cpus/cpu_dyntrans.c`, and the witness
`_scratchpad/w541/alpha_vmkill_probe.py`.

    VERDICT: <member number> -- <one line naming the deciding item>

## 1. HAS THIS ALREADY SHIPPED?  (§C0, re-run at firing time)

    git log -1 -- src/cpus/memory_alpha.c      -> 2956c7e #509 sgimtedepth4dead: `depth == 4' is unreachable, so tiled MTE always took CI   (RUN at brief-writing time)
    grep -c alphavmkill CHANGELOG.md          -> 0

## 2. THE SITE -- the whole enclosing function's relevant arms, and the common tail

```c
int alpha_translate_v2p(struct cpu *cpu, uint64_t vaddr, uint64_t *return_paddr, int flags)
{
	uint64_t base = cpu->cd.alpha.pcb.apcb_ptbr << ALPHA_PAGESHIFT;
	uint64_t userMode = cpu->cd.alpha.ps & ALPHA_PSL_USERMODE;
	...
	/*  Kernel direct-mapped space (OSF/1, NetBSD):  */
	if (!userMode && (vaddr >= ALPHA_K0SEG_BASE && vaddr <= ALPHA_K0SEG_END)) {
		*return_paddr = vaddr & 0x000003ffffffffffULL;
		return 2;
	}

	/*  UGLY hack for now: Before virtual memory has been set up, ptbr is most likely zero.
	    In that case, simply map everything vaddr == paddr.  */
	if (!userMode && base == 0) {
		*return_paddr = vaddr & 0x000003ffffffffffULL;
if (vaddr == 0xfffffffd80000000ULL) {
	fatal("Alpha kernel virtual memory seems to want to be used. Not yet implemented.\n");
	exit(1);                                             <-- THE DEFECT
}
		if ((vaddr & ~0x7fff) == 0x0000000010000000ULL)       *return_paddr = (vaddr & 0x7fff) + HWRPB_PADDR;
		if ((vaddr & ~0xffffff) == 0xfffffe0000000000ULL)     *return_paddr = 0x7efa000 + (vaddr & 0xffffff);
		if ((vaddr & ~0x1fff) == 0x0000000020000000ULL)       *return_paddr = (vaddr & 0x1fff) + PROM_ARGSPACE_PADDR;
		return 2;
	}

if (vaddr == 0xfffffffd80000000ULL) fatal("AYONA3\n");       <-- a SECOND residue, walk path (ptbr != 0)
	... the three-level walk ...
not_found:
	fatal("[ alpha_translate_v2p: 0x%016" PRIx64" wasn't found ]\n", vaddr);
	return 0;
}
```

**What a `return 0` does to the callers** (the handler's RETURN VALUE is a contract):
* `memory_rw.c`: a failed translation zeroes a READ buffer (#244) and returns MEMORY_ACCESS_FAILED.
* `cpu_alpha_instr_loadstore.c`: `if (!cpu->memory_rw(...)) return;` (#215) -- the load/store is ABANDONED; the
  destination register is left UNCHANGED.  **Alpha has no exception delivery on this path** (the carrier's option-set
  rule: member 5 FAULT is NOT available on Alpha).
* `cpu_dyntrans.c:670-734`, INSTRUCTION FETCH: a failed translation is assumed to have raised an exception and moved
  the PC; the code re-looks-up `cpu->pc`, re-translates it, and on a second failure does `fatal("FATAL: could not find
  physical address of the exception handler?"); exit(1);` (`:729-733`).  **Alpha's translator moves no PC**, so on
  Alpha EVERY I-fetch translation failure ends the host there.  So a DECLINE here (`return 0`) fixes the LOAD and
  STORE cells but an I-FETCH at this VA would still die -- via that generic kill, filed separately as
  `alphaifetchkill`.  **Check this reading** before relying on it; it decides what the round can claim.

## 3. THE WITNESS (rung 3) -- `_scratchpad/w541/alpha_vmkill_probe.py`, MEASURED 2026-09-18 on the committed build

Unmodified `-E alpha -e alphabook1`, cold debugger, ptbr == 0, supervisor mode.  Two `step` commands; the controls are
printed between them so a host death after them is attributable:

    live       raw-VA load of a planted RAM cell through the base==0 arm         -> VAL_A      (LIVENESS)
    hwrpb sig  raw-VA load at 0x10000008 -> the arm's HWRPB remap                -> "HWRPB"    (SIGNATURE)
    alive      one LDQ from 0xfffffffd80000000                                    -> survives   (DEFECT)
    continued  the instruction after it executed                                  -> 0x1234     (DEFECT)
    A death without the kill's own text scores 0/0 (a different defect), never 3/5.
    WANTED: 3/5 on the committed build; 5/5 after any fix that stops the host dying.
    MEASURED on build/ (two-part clearance CLEAN/fresh): 3/5 -- `live' 0xaaaa0000aaaa, `hwrpb sig' 0x4250525748
    ("HWRPB"), `alive' DIED, `continued' absent, and the kill's own text on the transcript (vmmsg=1), so the death
    is attributed to this site (regress/artifacts/alphavmkill/witness_HEAD_20260918/probe_HEAD.raw).

## 4. THE OPTION SET -- all seven members, grep-the-tree first

    1 DELETE the whole block        2 DECLINE silently (return 0)     3 DECLINE + LATCHED ANNOUNCE (`(once)`)
    4 ACCEPT (keep the identity result, drop only exit(1))            5 FAULT -- NOT AVAILABLE on Alpha
    6 BACKED ACCEPT                 7 IMPLEMENT kernel VM -- a feature, out of scope ("only fixes, no feature adds")

**The file's own precedent**: grok's 2026-09-08 assess refuted ACCEPT on a premise and confirmed FAULT would need Alpha
MM delivery built first.  **#215 is the tree's Alpha idiom for a failed translation**: abandon the access, leave the
destination unchanged, print once per miss (`not_found` -- itself UNLATCHED).

## 5. QUESTIONS

**Q1 -- PREMISES, as questions.**  Is `0xfffffffd80000000` special to any guest (NetBSD/alpha's VPT base is
`0xfffffffc00000000`; is this address inside the self-mapped page table)?  Does member 4 (drop only `exit(1)`, keep the
identity mapping to paddr `0x3fd80000000`) hand the guest a WRONG TRANSLATION that silently succeeds -- and what does an
access to that paddr (far past RAM, no device) then return?  Is `0` (member 2/3) better or worse for a guest than that?

**Q2 -- WHICH MEMBER, and why that one over its neighbours.**  State what each member does to a load, a store, and an
instruction fetch at that address, and what the witness would print under each.

**Q3 -- THE SECOND RESIDUE.**  `:94`'s `fatal("AYONA3\n")` is the same vaddr on the WALK path, a meaningless
unlatched message.  Under the reopening rule (same file, same semantic class, same detector, no new oracle), does it
join this round, or is it its own row?

**Q4 -- THE WITNESS.**  Do the controls prove what their notes claim?  Is the attribution guard (the kill's own text)
sufficient?  What rows will the DETECTOR owe once a member is chosen (a load, a store, an I-fetch; the destination's
value under the chosen member; the latch firing once)?

**Q5 -- ORDER OF ROUNDS.**  `alphaifetchkill` (filed today, HIGH: every Alpha I-fetch translation failure ends the
host at `cpu_dyntrans.c:729-733`) sits UNDER this row's I-fetch cell.  Should this round take its load/store cells and
DISCLOSE the I-fetch cell against that row, or should `alphaifetchkill` go first?  Name the measurable consequence of
each order.

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
