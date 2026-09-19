# `alphaifetchkill` PASS 1 -- CONSOLIDATED FINDINGS for the fable5 seat (LAST; every other seat has answered)

**Tree:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (HEAD `eec0f4a` since the peer's #536; `cpu_dyntrans.c` is unchanged
since de1398e).  **Use absolute paths.**  The brief is `brief_sent.md` in this directory.  The answers, all in this
directory:
- `codex.txt` and `kimi.txt` -- CLIs; the answer is the last `VERDICT:` block;
- `codex_advaifkp1.txt` -- the dedicated job;
- `agy.txt`, `grok.txt`;
- `ollama_{glm,deepseek,minimax,kimi}.txt`;
- `opus5_p1.md` -- the richest: an exact two-hunk shape, a mutant list and a new finding.

## VERDICTS -- option (e), STOP THE CPU SAFELY, all but one

    (e)  codex, codex_adv, agy, kimi CLI, kimi-k3, grok, glm, deepseek, opus5
    NOT-RATIFY (underspecified as briefed)  minimax -- answered by the consolidated shape below

## THE CONSOLIDATED SHAPE (Opus's, with every seat's constraint folded in; verify each line)

**Hunk 1** goes in `DYNTRANS_PC_TO_POINTERS_GENERIC`, in place of the `fatal(); exit(1);` at `cpu_dyntrans.c:729-733`:
1. A message naming the PC and the case: "no exception was taken" (the PC did not move) versus "the exception handler
   is not mapped".
2. `cpu->running = 0;`
3. `about_to_enter_single_step = true;`
4. `debugger_reset();`
5. `cpu->cd.DYNTRANS_ARCH.next_ic = &nothing_call;` -- **NOT `+1`**.
6. The delay-slot flag, as the unimplemented-instruction stop sets it.
7. `return;` -- leaving `cur_ic_page` and `cpu->pc` UNTOUCHED.

**Hunk 2** goes in `DYNTRANS_RUN_INSTR_DEF`, right after the entry `DYNTRANS_PC_TO_POINTERS(cpu)` (:183-191):
`if (!cpu->running) return 0;`.

**The precedents:**
- `cpu_alpha_instr.c:65-67` (the kimi CLI): `call_pal` already stops a CPU mid-handler with `running = 0;
  next_ic = &nothing_call;`.
- `cpu_i960_instr.c:46` (ABORT_EXECUTION).
- The unimplemented-instruction stop at `:2002-2024`.  That stop increments `next_ic` only because it EXECUTES
  `nothing` at once (`:2034`); here the caller dispatches next, so `+1` would call a garbage pointer.

## THE DISAGREEMENTS, each side in its own words

**D1 -- GENERIC or ALPHA-ONLY.**
- codex_adv: *"Alpha-only scope is preferred."*
- glm, kimi-k3, the kimi CLI and Opus: generic.  Opus: *"only Alpha can reach this line today, so the generic form
  changes no other architecture's behaviour."*  It supports this with a per-architecture table:
  - RISC-V and i960 have no translator;
  - MIPS vectors sit in kseg0/kseg1, which always translate;
  - ARM, PPC, SH and M88K re-enter `pc_to_pointers` for the handler from INSIDE the first call, so they succeed or
    recurse and never return to `:729`.
- **MY DISPOSITION: GENERIC**, provided D3's guard ships with it.  Opus shows the guard is what makes the generic claim
  safe: a pending IRQ on an architecture with delivery could otherwise re-point a stopped CPU at a handler.

**D2 -- `+1` or not.**
- codex_adv: the brief's copied sequence *"leaves next_ic one-past nothing_call"*.
- grok: *"do not copy next_ic++"*.
- Opus: NOT `+1`.
- **MY DISPOSITION: no `+1`.**  It is unanimous once stated.

**D3 -- the run-loop guard.**
- agy: *"otherwise the unrolled loop spins on nothing_call and epilogue low_pc recalculation clobbers cpu->pc"*.
- Opus: the epilogue leaves the PC alone only while `(&nothing_call - cur_ic_page)` lands outside the page's entry
  range, which is *"probabilistic, not deterministic"*.  The entry guard removes the entry-time case.
- glm: a *"three-site patch"*, with the epilogue latch-guarded.
- **MY DISPOSITION: hunk 2 as Opus shaped it.**  I would NOT add a separate epilogue guard: a PC row catches the
  probabilistic case if it ever bites.  **CHALLENGE THIS**; it is the disposition I am least sure of.

**D4 -- latch.**
- Opus: *"a stopped cpu cannot repeat it, so no latch is needed."*
- **MY DISPOSITION: agree.**  The message fires once per stop, and a detector row pins "exactly once".

## FINDINGS AND MY DISPOSITIONS

**F1. The witness has two defects as a DETECTOR (Opus).**
- The JMP target 0x1044000 is page-aligned, which blinds a PC row.  Use 0x1044080.
- Nothing is planted after the JMP, so a bare-`return` fix falls into zeros (CALL_PAL 0) and LOOKS like a stop.

**ACCEPT.**  The detector adds:
- a clean exit;
- the message exactly once;
- "All machines stopped" under `-V`;
- `pc` == the non-aligned target;
- a marker after the JMP keeps its sentinel;
- markers at the target's offset in the old code page, the identity page and page 0 keep theirs;
- three reach paths: JMP, falling off a mapped page, and `pc=` then step.

**F2. NEW, derived by reading, NOT witnessed (Opus): on ARM and PPC, possibly SH and M88K, an exception vector that
cannot be translated recurses without bound.**
- `arm_exception` has no nested-abort guard.
- `ppc_exception` (`cpu_ppc.c:335`) leaves instruction translation on.
- The likely effect is a host stack overflow and SIGSEGV.

**MY DISPOSITION: FILE as its own row (`excvecrecurse`), MED until witnessed.**  Opus proposes the ARM witness: MMU on,
the vector page unmapped, one jump to an unmapped VA.

**F3. Nine mutants are listed in `opus5_p1.md`, two of them equivalent on Alpha.  ACCEPT as the PRETABLE's starting set.**

## QUESTIONS

**Q1** -- generic or Alpha-only (D1)?
**Q2** -- the exact shape.  Is hunk 1 plus hunk 2 complete and safe, or is glm's epilogue guard owed (D3)?  No `+1`
(D2), no latch (D4)?
**Q3** -- the detector (F1): are these rows sufficient, and which of them are FLOOR?  Use your binding discriminator.
**Q4** -- which of my dispositions is wrong?  There are seven.  Be hardest on D3.

**IDENTITY -- the first three lines of your answer:**

    FABLE_SEAT_ALIVE_20260919_AIFKP1
    <your exact model id> | <the first line of C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md, verbatim>
    VERDICT: <option> -- <one line>

**READ-ONLY.**  Tables are re-running on this machine.  Run no builds, no emulator and no panel scripts.  Write only
`fable5_p1.md` in this directory.
