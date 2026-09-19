OPUS_SEAT_ALIVE_20260919_AIFKP1
claude-opus-5[1m]
VERDICT: e -- stop the CPU inside DYNTRANS_PC_TO_POINTERS_GENERIC exactly where the exit(1) is: set running = 0, point next_ic at &nothing_call (NOT +1), leave cur_ic_page and cpu->pc untouched, and return. Make it GENERIC: only Alpha can reach this line today, so the generic form changes no other architecture's behaviour, and nothing_call is in scope in every dyntrans architecture. Add a 2-line `if (!cpu->running) return 0;` after run_instr's initial pointer update so a stop on entry is deterministic.

# alphaifetchkill pass 1: Opus 5 seat

**Read-only.** No builds, no emulator runs, no writes except this file.
- **Read:** the brief; the witness artifacts (`RESULT.out`, `transcript_B.txt`, the frozen `vm_neighbour_measure.py`); codex jA; `cpu_dyntrans.c` in full; `memory_alpha.c`; the relevant parts of `cpu_alpha.c` and `cpu_alpha_instr.c`.
- **Beyond the brief's list, to answer Q1's other-architecture premise:**
  - the failure returns of `memory_{arm,ppc,sh,m88k,mips_v2p}.c`;
  - the PC and pointer-update lines of `{arm,ppc,sh,m88k,mips_cpu}_exception`;
  - `tmp_*_head.c` and `generate_head.c`, which define `nothing_call`;
  - `emul.c`'s run loop and `machine.c`'s `machine_run`.
- The tree is at HEAD `cdbe7d7`. `cpu_dyntrans.c` and `memory_alpha.c` are clean in the working tree.

## THE DIRECT ANSWERS

### 1. Does `nothing_call` work from inside `pc_to_pointers`?

Yes, both at the C level and in meaning.

- **It is in scope.** `nothing_call` is a file-static, `{ instr(nothing), {0,...} }`, emitted by `generate_head.c:145-148` into every `tmp_<arch>_head.c`.
  - That head is included near the top of `cpu_<arch>.c` (alpha :52, arm :60, mips :75, ppc :54, sh :58, m88k :59, riscv :49, i960 :54).
  - The tail that compiles `DYNTRANS_PC_TO_POINTERS_GENERIC` is included at the end (alpha :679).
  - So `&nothing_call` is visible inside the generic function for all 8 architectures. `about_to_enter_single_step` is declared in the same generated head (`generate_head.c:117-119`), and `debugger_reset()` is declared in `debugger.h`.
- **It is safe for every caller.** `instr(nothing)` does `next_ic--; ninstrs--;` (tmp_alpha_head.c:60-64). So once `next_ic == &nothing_call`, each dispatch step (`ic = next_ic++; ic->f(cpu, ic)`, :114) runs it and lands back on `&nothing_call`, and no guest instruction ever runs.
- **Every Alpha caller returns straight to the dispatch loop without touching `next_ic`:**
  - run_instr's initial update (:190);
  - `call_pal` (cpu_alpha_instr.c:69-72);
  - `jsr` (:104-108);
  - `jsr_0` (:145-149);
  - `br` (:184);
  - `br_return` (:211);
  - `end_of_page` (:757, which only decrements `n_translated_instrs` afterwards).
- **The delayed branches in MIPS, M88K and SH** increment `next_ic` only on the NOT-taken branch, never after `quick_pc_to_pointers` (cpu_mips_instr.c:201-203, cpu_m88k_instr.c:203-205, cpu_sh_instr.c:2500-2502).
- **In-tree precedents for pointing `next_ic` at `nothing_call` outside `to_be_translated`:**
  - cpu_alpha_instr.c:67, the `call_pal` handler after a PAL halt;
  - cpu_i960_instr.c:46, the `ABORT_EXECUTION` macro;
  - include/quick_pc_to_pointers.h:22.

### 2. What must `next_ic`, `cur_ic_page` and the PC hold on return?

- **`next_ic == &nothing_call`, and NOT `&nothing_call + 1`.**
  - The precedent at :2023-2024 increments and then EXECUTES `nothing` at once (:2034), which decrements it back.
  - Here nothing is executed before returning, so the caller's next dispatch step must find `&nothing_call` itself. With `+1`, that step would call a garbage function pointer and the host would crash.
- **`cur_ic_page` must be UNCHANGED.**
  - Do not set it to `&nothing_call`. That makes the epilogue's `low_pc` 0 (:395-400), which page-aligns `cpu->pc` and corrupts the PC the debugger shows.
  - Do not set it to NULL: :269 copies it into `cur_physpage`, which the statistics code dereferences (:74-76).
  - The precedent also leaves it alone.
- **`cpu->pc` must be UNCHANGED.** For Alpha, that is the address that could not be fetched, because `alpha_translate_v2p` never writes the PC. The epilogue leaves it alone as long as `(&nothing_call - cur_ic_page) / sizeof` falls outside [0, ENTRIES+1].
  - That is true in practice and it is the same property the unimplemented-instruction path relies on today. It is probabilistic, not deterministic.
  - A PC row catches it if it ever breaks (Q3), and the entry guard below removes it from the run_instr-entry case.
- **`cpu->running == 0`.**

### 3. Alpha-only or generic? GENERIC

**Only Alpha can reach :729 today** (Q1). So the generic form changes no other architecture's observable behaviour, leaves no dead `exit(1)` behind an `#ifdef`, and covers any future translator that fails without moving the PC.

The message should say which of the two cases happened, by comparing the PC before and after the first translation:
- "no exception was taken": Alpha;
- "the exception handler at X is not mapped": any architecture whose handler is also untranslatable, if one ever gets here.

### 4. Which detector rows prove the three things? See Q3.

Two witness defects need fixing first:
- the jump target is page-aligned, which blinds a PC row;
- nothing is planted after the `JMP`. That lets a bare-`return` fix fall through into zeros, which is `CALL_PAL 0`, and *look like* a stop.

---

## Q1 -- PREMISES

**"No other architecture reaches :729-733": TRUE, but for a stronger reason than the brief gives.**

| architecture | what an instruction-fetch translation failure does | reaches :729? |
|---|---|---|
| **alpha** | `not_found`: prints and returns 0; **the PC is not moved** (memory_alpha.c:192-198) | **yes**: the retry uses the same PC |
| riscv, i960 | no `translate_v2p` is set, so :681-684 sets `paddr = cached_pc; ok = 1` | never fails |
| mips | `mips_cpu_exception` (memory_mips_v2p.c:452) sets the PC to a **kseg0/kseg1** vector (cpu_mips.c:2175-2202) and calls `pc_to_pointers` (:2221/2223). Those segments always translate | no |
| arm | `arm_exception(PREF_ABT)` (memory_arm.c:268-269) sets the PC to the vector (cpu_arm.c:731) and calls `quick_pc_to_pointers` (:733) | **no, and see below** |
| ppc | `ppc_exception` (memory_ppc.c:313/322): PC = nr×0x100 (+0xfff00000), then `pc_to_pointers` (cpu_ppc.c:337-344) | **no, and see below** |
| sh | `sh_exception`: TLB miss sends the PC to `vbr+0x400` (cpu_sh.c:1025), then `sh_pc_to_pointers` (:1088) | **no, and see below** |
| m88k | `m88k_exception`: PC = VBR+8×vector (cpu_m88k.c:863), then `pc_to_pointers` (:980) | **no, and see below** |

- **The mechanism the brief omits:** every one of those exception routines RE-ENTERS `pc_to_pointers` for the handler from *inside* the first translation call.
  - If the handler translates, the outer retry finds it. So "they get past the retry" is true in that case.
  - **If it does NOT translate, the nested call raises again and re-enters again. The recursion never returns to the outer retry, so :729 is never reached.** See "found something else" 1.
  - So only a translator that fails WITHOUT moving the PC can reach :729, and in this tree that is only Alpha.
- **Not read:** `sh_exception`'s SR.BL/double-fault handling; how m88k's supervisor CMMU translates VBR; whether `ppc_translate_v2p` special-cases exception mode.
- **The single-step trace read (:287-290 and :325) does handle its own failure, but only with a message.**
  - A failed read prints "XXX_run_instr(): could not read the instruction" and falls through to `I` at :325, which runs whatever `next_ic` the entry update (:190) left.
  - **Today** that failure arm is effectively unreachable for Alpha: an entry-time translation failure exits at :729 before :287.
  - **Under the fix without the entry guard:** an entry-time stop still runs the trace read. That is a third "wasn't found" line plus "could not read the instruction", then `I` runs `nothing_call`. Safe, but noisy.
  - More importantly, the interrupt block at :206-251 runs after :190 regardless. On an architecture with delivery, a pending IRQ would call its exception routine, which re-points `next_ic` at the handler, and **guest code would run on a CPU marked stopped** until `N_SAFE`. Alpha has no delivery, so for Alpha this is only noise. The entry guard in Q2 closes it for the generic claim.
- **`nothing_call` from `pc_to_pointers`:** yes; see direct answer 1.

## Q2 -- OPTION (e), GENERIC, THE EXACT SHAPE

**The enclosing function's exits today:** the normal end, which sets `cur_ic_page`/`next_ic` at :830-833, and the `exit(1)` at :729-733. Nothing is written before :736 (no `update_translation_table`, no page allocation), so an early return leaves no half-done state.

**Hunk 1, `DYNTRANS_PC_TO_POINTERS_GENERIC`, inside `if (!ok) {` at :670:**

```c
	if (!ok) {
		uint64_t paddr;
		uint64_t pc_before = cpu->pc;		/*  #NNN  */
		...					/*  :672-728 unchanged  */
			if (!ok) {
				/*  #NNN (alphaifetchkill): was fatal() + exit(1).
				    No instruction can be fetched at cpu->pc: the
				    translator failed without moving the PC (Alpha
				    delivers no MM fault), or the handler it moved
				    to is itself unmapped.  Stop THIS cpu the way
				    DYNTRANS_TO_BE_TRANSLATED_TAIL stops one on an
				    unimplemented instruction.  next_ic ->
				    nothing_call, which every caller dispatches
				    next and which runs no guest instruction;
				    cur_ic_page and cpu->pc are left alone, so
				    the PC still names the address that failed.
				    One message per stop: a stopped cpu cannot
				    repeat it, so no latch is needed.  */
				debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
				    "instruction fetch at 0x%" PRIx64 " cannot be"
				    " translated (%s); cpu stopped",
				    (uint64_t) cpu->pc, cpu->pc == pc_before ?
				    "no exception was taken" :
				    "the exception handler is not mapped");
				cpu->running = 0;
				about_to_enter_single_step = true;
				debugger_reset();
				cpu->cd.DYNTRANS_ARCH.next_ic = &nothing_call;
#ifdef DYNTRANS_DELAYSLOT
				if (cpu->delay_slot)
					cpu->delay_slot |= EXCEPTION_IN_DELAY_SLOT;
#endif
				return;
			}
```

**Hunk 2, `DYNTRANS_RUN_INSTR_DEF`, right after the initial `DYNTRANS_PC_TO_POINTERS(cpu)` (:183-191):**

```c
	if (!cpu->running)		/*  #NNN: the entry pointer update stopped it  */
		return 0;
```

- For Alpha, hunk 2 only removes the extra noise from the trace read, and makes the PC deterministic on entry because the epilogue's PC synchronisation is skipped.
- For the generic claim it is REQUIRED: it keeps the interrupt block from re-pointing a stopped CPU.
- It cannot alter a running CPU. `machine_run` calls `run_instr` only for CPUs with `running` set (machine.c:708-743), and :190 is the only thing between entry and this check.

**Choices within the shape:**
- **`debugmsg_cpu` at ERROR, not `fatal()`:** this mirrors the precedent at :2005-2009. ERROR stays visible under `-q`, the latched-`fatal()` warrant at dev_asc.c:250-257, and it trips break-on-ERROR like the precedent does. Either is defensible.
- **`about_to_enter_single_step = true`:** kept for parity with the precedent. It does nothing on single-CPU alphabook1, where the stop leaves no CPU running and emul.c:1052-1058 decides what happens. On `-n` ≥ 2 it drops into the debugger instead of letting the other CPUs run on beside a dead one. Dropping it is the alternative; the difference is measurable only with 2 or more CPUs.
- **No latch:** the CPU is stopped after the first message and can only be restarted from the debugger. The guest cannot repeat the message, so it cannot flood.

**What happens after the return:**
1. The caller returns to the loop. A jump, branch or `end_of_page` returns; `call_pal` already returned.
2. Each dispatch step runs `nothing`, which lands back on `&nothing_call`.
   - In the multi-instruction loop it spins until `n_translated_instrs >= N_SAFE_DYNTRANS_LIMIT` (8191, cpu.h:328-329), then breaks. The `ninstrs--` in `nothing` exactly cancels the loop's `+120`s, so **`ninstrs` does not advance**.
   - In single-step mode it runs once, `n_instrs = 1`, which is also net zero.
3. The epilogue: `low_pc` is garbage, so the PC is left alone.
4. `machine_run` sees no running CPU. Then emul.c:1052-1058 decides:
   - **with `-V`/`-K`:** "All machines stopped." and the debugger prompt;
   - **otherwise:** `break`, and gxemul exits normally with status 0 (main.c:807, :821). That is the same ending as a guest `CALL_PAL 0`.
5. On re-entry from the entry guard: `return 0` before any accounting.

**Why not (a), (b) or (c):**
- **(a) is undefined behaviour:** `physaddr = paddr` with `paddr` never set (:736). If the stale stack value names an already-translated page, that page's translated instructions run at the new offset.
- **(b) falls through** to the instruction after the jump in the OLD page, because `next_ic` was already advanced past the jump.
- **(c) is (e) behind `#ifdef DYNTRANS_ALPHA`.** On Alpha it is identical. Elsewhere it keeps an `exit(1)` that nothing reaches, and it leaves a future translator with the host kill.

## Q3 -- THE WITNESS AS A DETECTOR

Session B, as written, cannot tell three wrong fixes apart from the right one:
- a PC-alignment mutant is invisible, because the target 0x1044000 is page-aligned;
- **(b) looks like a stop:** the fall-through reaches zeros at CODE+0x2c, which is `CALL_PAL 0`, which prints PALcode 0x0 and halts;
- nothing is planted where a garbage page would run.

**Rows owed, using the same vehicle (armed with an all-zero first-level table):**

| row | how | proves / catches |
|---|---|---|
| **alive** | a clean exit after `quit` (`WIFEXITED` and status 0); the frozen harness already requires this | the host survived. Catches M1 and M4 |
| **no FATAL** | the "could not find physical" count == 0, and the exit status is not 256 | the old kill is gone |
| **stop msg ×1** | the new message count == 1, **even after a further `step 3`** | the stop happened, and the CPU stayed stopped: a running CPU would re-enter :190 and repeat it. Catches M6 |
| **stopped** | under `-V`: "All machines stopped." present. **CTRL-T (0x14) at the prompt** prints `ninstrs=..., pc=..., stopped` (debugger.c:498-524, via `!cpu->running`) | the CPU's own running flag |
| **ninstrs frozen** | CTRL-T's `ninstrs` is the same before and after the extra `step 3` | no instruction executed after the stop |
| **pc** | `print pc` == the target EXACTLY, with the target **not page-aligned** (e.g. 0x1044080) | the PC is kept. Catches M5, which page-aligns it |
| **no fall-through** | plant `lda t7,0x999(zero)` right AFTER the `JMP`; t7 keeps SENT | catches M3 (b) |
| **no garbage page** | plant a marker (`lda t6,0x777(zero)`) at the target's page offset (+0x080) in (i) the CODE page (the stale previous page), (ii) physical 0x1044000+0x80 (the identity page), (iii) physical 0x80 (paddr 0); t6 keeps SENT | nothing from a garbage page ran. Catches M2 (a) |
| **controls** | the existing arming row (t2 == SENT plus "wasn't found" at 0x1056000), and a pre-jump marker (t5) set before the `JMP` | paging is armed and the CPU was executing |
| **caller cells** | the same checks, reached through (1) a **`JMP`** (an instruction handler), (2) a **fall-through off the end of a mapped page into an unmapped page** (`end_of_page`, :757), and (3) **`pc=<unmapped>` then `step 1`** (run_instr entry, :190, which exercises hunk 2 and the trace read) | the stop is safe for each kind of caller |

**Variants to build for the kill table:**
- **M1** `exit(1)` put back → `alive`.
- **M2** option (a): no return → the no-garbage rows, or a crash.
- **M3** option (b): return with `next_ic` unchanged → no fall-through.
- **M4** `next_ic = &nothing_call + 1` → host crash, so `alive`.
- **M5** `cur_ic_page = &nothing_call` → `pc`.
- **M6** `running = 0` left out → message count, or a hang.
- **M7** stop only when `pc != pc_before`, keeping the exit for Alpha's case → `alive`.
- **M8** hunk 2 removed → trace-read noise in cell 3. On Alpha that is otherwise **equivalent**; disclose it, because the interrupt-block hazard it prevents exists only on architectures with delivery.
- **M9** the `#ifdef DYNTRANS_ALPHA` form → **equivalent on Alpha**. Disclose that the generic claim is untestable here, since no other architecture reaches the line.

## FOUND SOMETHING ELSE

1. **A separate host-death class, derived by reading and NOT witnessed: an untranslatable exception VECTOR recurses without bound.**
   - The chain is `translate_v2p → X_exception → pc_to_pointers → translate_v2p → ...`, ending in a host stack overflow.
   - **ARM:** `arm_exception` has no nested-abort guard (cpu_arm.c:616-734). A guest that turns the MMU on with the vector page unmapped, then takes one prefetch abort, would recurse.
   - **PPC:** `ppc_exception` clears only EE, RI and PR (cpu_ppc.c:335), so **MSR[IR] stays set** and the vector itself is fetched through the MMU. The 32-bit OEA clears IR and DR on interrupt entry; I believe so but did not read it. Check `_scratchpad/ppc_oea_book3_v201.txt`.
   - **SH and M88K:** the same shape; not settled (see Q1's "not read").
   - **MIPS is immune** (kseg0/1 vectors).
   - This round's fix does not touch it, because the recursion never returns to :729. File it as its own row with a witness per architecture, for example an ARM machine with the MMU on and page 0 unmapped, then one jump to an unmapped address.
2. **Codex's "clean shutdown versus debugger entry cannot be established" is settled by emul.c:1052-1058 and main.c:473-475.** `-V` and `-K` set `debugger_enter_at_end_of_run`, which gives "All machines stopped." and the prompt. Otherwise the run loop breaks and main returns 0. alphavmkill's session A already MEASURED the `-V` branch: "All machines stopped" once, and a clean exit.
3. **The witness transcript's FATAL line has no newline** ("...exception handler?quit"), so the text runs into the next output. Give the new message its own line. It is also why a naive grep of `^FATAL` misses it.
4. **The epilogue's PC synchronisation** uses a garbage `low_pc` whenever `next_ic` points at `nothing_call`. That happens in both this fix and the unimplemented-instruction path (:2002-2034). It is safe only because the static-versus-heap address gap lands outside [0, ENTRIES+1]. A generic `if (!cpu->running)` skip of the synchronisation would make it deterministic for both. File it; it is not needed here.

## MEASUREMENTS TO RUN

1. **In a scratch clone:** hunks 1+2 applied, then cells 1-3 above, then M1-M7.
   - Predicted for the fix: alive, stop message ×1, no FATAL, `pc` = the raw target exactly (for example 0x1044080), t6/t7 = SENT, CTRL-T shows "stopped" with `ninstrs` unchanged.
2. **ARM recursion witness** (for item 1): `-E testarm` or `cats` with the MMU on, the vector page unmapped, and one jump to an unmapped address.
   - Predicted: repeated "arm memory fault" lines, then SIGSEGV (wait status signal 11).
   - The PPC equivalent: IR on, vectors unmapped.
