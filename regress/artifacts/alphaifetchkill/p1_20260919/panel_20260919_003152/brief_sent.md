# `alphaifetchkill` PASS 1 -- a failed Alpha instruction-fetch translation ends the emulator process

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  **VERDICT LINE FIRST.**  **THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** at HEAD
`cdbe7d7`.  Pristine-2021 copies elsewhere under the project root are NOT this fork.  **If you cannot read
files, that is expected**: every fact you need is inlined; name any premise you cannot settle.

**Seats that read files: read ONLY** `GXEMUL-SEC/src/cpus/cpu_dyntrans.c`, `GXEMUL-SEC/src/cpus/memory_alpha.c`,
`GXEMUL-SEC/src/cpus/cpu_alpha.c`, `GXEMUL-SEC/src/cpus/cpu_alpha_instr.c`.

    VERDICT: <option> -- <one line naming the deciding item>

## 0. HAS THIS ALREADY SHIPPED? (run at brief-writing time)

    git log -1 -- src/cpus/cpu_dyntrans.c   ->  de1398e Hardening/fidelity/debuggability rounds 17–25 (#155–#250)
    grep -c alphaifetchkill CHANGELOG.md   ->  0 (the row is being filed now)

## 1. THE DEFECT, WITNESSED AT RUNG 3 ON THE COMMITTED BUILD

`regress/artifacts/alphaifetchkill/witness_HEAD_20260918/`: one unmodified `-E alpha -e alphabook1` process.  Paging is
armed (swpctx to a PCB whose ptbr names an all-zero L1 page).  The arming control holds: a raw-VA load walks, misses,
and keeps its sentinel.  Then ONE `JMP` to a raw VA (0x1044000).  The transcript shows two
`[ alpha_translate_v2p: 0x0000000001044000 wasn't found ]` lines, then
`FATAL: could not find physical address of the exception handler?`, and the process exits with status 1.

**The mechanism**, from `cpu_dyntrans.c`, `DYNTRANS_PC_TO_POINTERS_GENERIC` (`:622` on):

```c
	if (!ok) {
		uint64_t paddr;
		if (cpu->translate_v2p != NULL) {
			...
			ok = cpu->translate_v2p(cpu, vaddr, &paddr, FLAG_INSTR);
		} ...
		if (!ok) {
			/*  The PC is now set to the exception handler.  Try to find the paddr in the translation
			    arrays, or if that fails, call translate_v2p for the exception handler.  */
			cached_pc = cpu->pc;
			... look cached_pc up in the fast table ...
			if (!ok)
				ok = cpu->translate_v2p(cpu, cpu->pc, &paddr, FLAG_INSTR);
			if (!ok) {
				fatal("FATAL: could not find physical address of the exception handler?");
				exit(1);                                               <-- THE DEFECT (:729-733)
			}
		}
		physaddr = paddr;
	}
	... physaddr is used to find/allocate the translated page; cur_ic_page / next_ic are set at :830-833 ...
```

**Why Alpha always reaches it:** `alpha_translate_v2p` returns 0 on a miss WITHOUT moving `cpu->pc` (Alpha delivers no
memory-management fault in this tree -- the walk's own TODOs at `memory_alpha.c:120-126` say so).  So the "exception
handler" is the same PC, the retry fails the same way, and the host exits.  MIPS, ARM, PPC and SH move the PC to a
real handler before returning, so they get past the retry.

## 2. WHAT THE CODEX RESEARCH JOB FOUND (read-only, `_scratchpad/cxfarm_e8a2bc_20260918/codex_jA.txt`)

* **Replacing only `exit(1)` with `cpu->running = 0` is NOT enough**: it falls through to `physaddr = paddr` with no
  paddr supplied (`:736`).
* **A bare `return` is NOT enough**: it skips setting `cur_ic_page`/`next_ic` (`:830-833`), and the dispatch loop
  dereferences `next_ic` without checking `running` (`:114`, `:190`).
* **The in-tree precedent for stopping a CPU safely** is the unimplemented-instruction path (`:2002-2024`):
  `about_to_enter_single_step = true; ... cpu->running = 0; debugger_reset(); ic = next_ic = &nothing_call;
  next_ic++;`.  It is a design precedent, not a drop-in: the run entry resets instruction accounting after PC
  conversion, and the epilogue reconstructs the PC from instruction pointers (`:267`, `:394`).

## 3. THE OPTION SET (grep the tree first)

    (a) exit(1) -> cpu->running = 0 + a latched message, and NOTHING else       -- refuted above (garbage paddr)
    (b) return without a translation                                             -- refuted above (next_ic unset)
    (c) (e) for Alpha only; other architectures keep today's exit
    (d) deliver an Alpha ITB/ACV fault through PALcode                           -- a FEATURE (out of scope)
    (e) STOP THE CPU SAFELY, the unimplemented-instruction way: latched message, running = 0, next_ic -> nothing_call,
        debugger_reset(); the guest sees a stopped CPU, the host survives (and under -V the debugger prompt appears)

## 4. QUESTIONS

**Q1 -- PREMISES, as questions.**  Is it true that NO other architecture in this tree can reach `:729-733` today (read
each translator's failure path, or say which you did not)?  Does the single-step trace read (`:287`, `:325`) really
handle its own failure?  Is `nothing_call` usable from inside `pc_to_pointers`, or only from an instruction handler?

**Q2 -- WHICH OPTION**, and the exact code shape.  Inline the enclosing function's exits and state, for your shape,
what `cur_ic_page`, `next_ic` and `cpu->pc` hold on return, and what the run loop does next.

**Q3 -- THE WITNESS AS A DETECTOR.**  Which rows prove the host survives AND the CPU is stopped AND no garbage
executes (e.g. `pc` still the faulting VA, the debugger prompt, the latch once)?

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
