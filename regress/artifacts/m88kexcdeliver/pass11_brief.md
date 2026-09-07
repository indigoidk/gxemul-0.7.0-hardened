# `m88kexcrrtrapmode` -- ONE question: is the filed cell real, and what is the smallest edit that exposes it?  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a CPU model in a hardware simulator for obsolete workstations (GXemul 0.7.0, a
maintained fork): the MC88100 exception-delivery path and the regression detector that defends it.  Plain engineering
vocabulary; no security framing is intended or wanted, and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`.  Ignore any other `src/` you find** -- three pristine-2021 upstream copies
sit under the project root and are NOT this fork; a copy reports line numbers off by hundreds and different arms.  The
file is `GXEMUL-SEC/src/cpus/cpu_m88k.c`, the detector `GXEMUL-SEC/regress/m88k_exc_probe.py`.

**If you cannot read files that is expected -- every fact is inlined below.  Name any premise you cannot settle from
this packet rather than guessing.**  VERDICT LINE FIRST.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A ten-pass chain on this detector has just closed.  **Three of those passes each found that a repair had reproduced,
inside itself, the class of defect it was repairing** -- a cell of a state space closed at the address the mutant used,
leaving the symmetric cell open.  This filing came out of the census written to end that pattern, so the obvious failure
mode is that I have filed a cell that is already covered, or mis-stated why it is not floor.  **Check the premises, not
just the derivations.**

## SETTLED PREMISES (established in earlier passes, re-inlined so you need not re-derive them)
1. `m88k_exception(cpu, vector, is_trap)` has: a dispatch `switch` on `vector` setting `implemented`; then a FALLBACK
   `if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented)` which prints and stops every CPU; then the SFRZ
   re-route; then a common path; then a tail `switch`.
2. The six software-settable MC88100 PSR bits are MODE (0x80000000), SER (0x20000000), C (0x10000000), SFD1 (0x08),
   IND (0x02), SFRZ (0x01).  BO and MXM cannot be set through `m88k_stcr` without stopping the CPU.
3. The detector has 57 fault rows + 2 controls and gate 11 pins it at 57/57 (PASS, 105 checks, 2026-09-06).
4. A cell (site, bit) is CLOSED iff two rows reach that site with DIFFERENT values of that bit -- polarity-free, because
   a mutant may condition in either direction.
5. `SER` is NOT an 88110-only bit.  `_scratchpad/mc88100.txt`, anchor `SER - Serial Mode`, documents it for the MC88100
   as software-settable, and `m88k_stcr` stores it verbatim.

## THE FULL ENCLOSING BLOCK, verbatim -- the re-route and the two lines around it
```c
	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
			vector, (int)cpu->pc);
		for (int j = 0; j < cpu->machine->ncpus; ++j)
			cpu->machine->cpus[j]->running = false;
		m88k_pc_to_pointers(cpu);
		return;
	}

	/*  Stuff common for all exceptions:  */
	if (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ) {
		/*
		 *  Non-trap exceptions when the shadow freeze bit is already
		 *  set result in an Error exception:
		 */
		if (!is_trap) {
			vector = M88K_EXCEPTION_ERROR;
			fatal("[ SFRZ already set in PSR => ERROR ]\n");
		}

		update_shadow_regs = false;
	} else {
		/*  Freeze shadow registers, and save the PSR:  */
		cpu->cd.m88k.cr[M88K_CR_EPSR] = cpu->cd.m88k.cr[M88K_CR_PSR];
	}

	m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR]
	    | M88K_PSR_SFRZ | M88K_PSR_IND | M88K_PSR_SFD1 | M88K_PSR_MODE,
	    M88K_CR_PSR, 0);

	if (update_shadow_regs) { ... }
```
**Note the common tail below the block**: an early `return` inserted here would skip the `m88k_stcr` that switches to
supervisor mode and the shadow-register saves.  A previous pass had four independent readers propose an early `return`
into a different function here without noticing its tail; the sketch rule exists because of that.

## THE MEASURED CENSUS (`regress/artifacts/m88kexcdeliver/CELLCENSUS.out`, deriver beside it)
At the re-route, by branch:

    non-trap side (8 rows)   MODE closed by errpriv/errunimpl · SER errser · C errc · SFD1 errdiv0 · IND errind
                             SFRZ open -- INVARIANT BY CONSTRUCTION, it is the guard
    trap side (14 rows)      SER closed by trapfrozenser · C trapfrozenc · IND trapfrozenind
                             MODE open -- all 14 rows carry MODE=1
                             SFD1 open -- all 14 rows carry SFD1=1
                             SFRZ open -- invariant by construction

## WHAT I FILED, AND THE THREE THINGS I WANT ATTACKED
**The filing:** at the TRAP side, MODE and SFD1 never vary, so a widened inner guard
`if (!is_trap || !(PSR & M88K_PSR_MODE))` escapes all 57 rows.  I claim the cell is REACHABLE because both halves exist
separately in the probe today -- `errpriv` has a frozen handler drop to user mode via `PSR_FRZUSER = 0x00000003`
(IND|SFRZ, MODE clear), and `trapfrozen128` takes a frozen user trap at vector 128 -- but no row combines them.  I claim
this is clause-(e) DEBT and not a floor breach, because the floor asks for the partitions the guarded body itself tests,
and that body tests only `is_trap` and the outer `PSR & SFRZ`, both polarities of both already rowed.

1. **IS THE CELL REACHABLE AT ALL?**  My reachability argument is a composition of two rows that were never composed.
   A user-mode `tb1` naming a vector BELOW 128 raises PRIVILEGE with `is_trap == 0` -- so the trap must name >= 128.
   Does a frozen user-mode trap at >= 128 actually reach this block with MODE clear, or does something earlier
   intervene?  **If it does not, the cell is UNREACHABLE and the filing should say so with its warrant, not sit open.**
2. **IS MY FLOOR/DEBT CALL RIGHT?**  I would rather be told this is a floor breach now than discover it later.  The
   competing reading is that the re-route's guarded body is the whole `if (PSR & SFRZ) { ... }` block, whose inner `if`
   tests `is_trap`, making {is_trap} x {MODE} a joint the body distinguishes -- which would make it floor and require an
   in-round repair.
3. **WHAT IS THE SMALLEST EDIT THAT EXPOSES IT AND STILL PASSES 57/57?**  Give me the exact mutant text against the
   block above.  If a smaller or more plausible one exists than the `||` widening I proposed, name that instead -- and
   say which existing row you expect to redden once the cell is closed, since a row whose named channel cannot vary
   under its named mutant is vacuous by construction.

## THE SECOND QUESTION, with the count named
Of the FOUR claims in this filing -- (i) MODE does not vary at the trap side, (ii) SFD1 does not vary there, (iii) the
cell is reachable by composing `errpriv`'s handler with `trapfrozen128`'s trap, (iv) it is debt rather than floor --
**WHICH IS WRONG?**  Assume at least one is.

VERDICT LINE FIRST (`REACHABLE-DEBT` / `REACHABLE-FLOOR` / `UNREACHABLE` / `ALREADY COVERED BY <row>`), then the mutant
text, then anything else.  Under a page.
