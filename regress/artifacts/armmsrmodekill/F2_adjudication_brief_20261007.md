# armmsrmodekill -- pass 1 ADJUDICATION: the panel's findings, shared, with my disposition on each

Open with `VERDICT: <n> of 12 dispositions wrong` (VERDICT LINE FIRST).  Read-only; write nothing, build nothing.
Tree `GXEMUL-SEC/src/` at HEAD `ef577140` (ignore any other src/ under the project root).

Pass 1 (brief `FIXDESIGN_brief_20261007.md`) was answered by: GPT-6 Astra (codex), grok, agy, glm, deepseek, minimax,
kimi-k3:cloud, and Opus 5.5.  Fable 5.1 adjudication is ON HOLD by owner instruction (2026-10-07) -- deliberately not
fired.  **This pass shares every seat's findings so you can correct each other.**  Seats whose finding is ADOPTED below:
be HARDEST on that finding, including whether the FIX is right, not only whether the finding was.

**THE LOAD-BEARING QUESTION: which of my 12 dispositions is wrong?**

## Measured since pass 1 (the witness)

The 17-row rung-3 probe `regress/arm_msrmode_probe.py` (repaired by the Opus seat in a scratch clone: aligned dump,
little-endian swap, arming-vs-result transcript split, `save 2s` slots) on a FRESH HEAD build: **14/17, the three
named reds exactly** (`kill 14`, `kill 15`, `save 2s`: each `dead`, diagnosis `load mode 20` / `load mode 21` /
`load=yes save=no`); all controls green.  Mutant M1 (both `default:` arms `exit(1)` -> `return;`): still the same three
reds (got `m=14 sp` etc. -- a silent decline leaves the reserved mode in CPSR, which is not the fixed state).  Mutant
M2 (a sketch: `msr_imm` refuses a reserved mode field with a `(once)` latch): 17/17.

## The findings and my dispositions

| # | finding | seat(s) | disposition |
|---|---|---|---|
| 1 | Member 3 (decline + latched announce) is the disposition | all eight | ADOPTED |
| 2 | "six modelled modes" is wrong: SEVEN mode values (`10 11 12 13 17 1b 1f`), six banks (USR/SYS share) | glm, kimi, codex, grok, minimax | ADOPTED -- wording corrected in the round's records |
| 3 | "decline must happen BEFORE Save" overstates: the bad mode enters at the CPSR write between Save and Load; Save runs on the old (modelled) mode | codex, grok | ADOPTED -- the guard sits at the CPSR write, before Load; Save on the old mode is harmless |
| 4 | ZERO-INITIALISED SPSR: `cpu_new` zero-fills the cpu (`cpu.c` zero-alloc), so an SPSR never written holds mode `0x00`; the first `MOVS pc,lr` / `LDM {..pc}^` from SVC32 before any exception writes `spsr_svc` loads mode 0 and dies -- NO MSR needed | grok | ADOPTED -- the restore-path guards are REQUIRED, not optional; a detector row is owed for it |
| 5 | Restore paths (callers 2 `arm_pop` `^`, 3 DPI S-to-PC) also reach the kill via `MSR SPSR_c` poisoning; a fix guarding only `msr_imm` leaves every current row green (the "smallest breaking edit") | opus, kimi, deepseek, minimax, agy | ADOPTED -- guard all three guest writers; TWO detector rows owed (one per restore path) |
| 6 | Decline ONLY the mode field; apply the rest of the write (flags, I/F, T) | grok, opus, glm, agy | ADOPTED -- see 7 |
| 7 | DISSENT: decline the WHOLE operation before side effects (codex: "whole-operation decline before side effects and explicit bank-helper failure propagation") | codex | NOT ADOPTED -- under the owner's arrangement grok rules Astra's findings, and grok ruled field-only.  Warrant: MSR's architected effect on the other fields is defined; only M[4:0] is UNPREDICTABLE.  **Codex: be hard on this ruling.  What does whole-operation decline buy that field-only loses, measured on a guest?** |
| 8 | FAULT is a LEGAL implementation of UNPREDICTABLE (ARMv7 glossary: may be implemented as UNDEFINED) -- the brief's "member 5 is wrong" overstated | codex, grok | ADOPTED as a correction of the premise; NOT chosen -- ARMv5 text (`ddi0100i`) lists MSR "Exceptions: None", data-processing none, LDM(3) Data Abort only, and the glossary forbids halting; decline is the minimal policy.  Recorded as a policy choice, not an architectural requirement |
| 9 | The helper should key on the SAME seven `case` labels as Save/Load (one source of truth), living outside the DPI template (included ~140 times) | opus | ADOPTED |
| 10 | In `msr_imm`, change only the LOCAL `mask`; never write `ic->arg[0]` / `ic->arg[1]` (cached translation) | opus | ADOPTED |
| 11 | Backstops: keep both `default:` arms as per-CPU latched announces with NO rollback; they stay reachable via the debugger `put cpsr` (writable setting, no bank switch) -- a debugger-driven row is owed to carry the backstop claim | opus, codex, glm, deepseek | ADOPTED -- latch in a per-CPU field, distinct bits for the decline and each backstop; message carries `(once)` |
| 12 | NEW DEFECT (not this row): a USER-mode guest stops the whole emulator: `LDMFD sp!,{..pc}^` and `MSR SPSR_x` in USR/SYS reach `default:` arms that set `running = 0` (`arm_pop`, `msr_imm_spsr`) | opus | FILED as its own row (owner, 2026-10-07); NOT fixed here |

## The proposed fix, as a sketch (CHECK IT against each caller's real control flow)

* `static int arm_mode_is_modelled(uint32_t mode)` in `cpu_arm.c` (declared in `cpu_arm.h`): `switch (mode & ARM_FLAG_MODE)` over the seven labels -> 1, `default` -> 0.
* `msr_imm`: after the USR mask line, if `(mask & ARM_FLAG_MODE)` and `!arm_mode_is_modelled(new_value)`: latched
  announce `(once)`, then `mask &= ~ARM_FLAG_MODE` -- BEFORE `switch_register_banks` is computed (so no bank switch).
* `arm_pop` `^` restore and DPI S-to-PC restore: if the SPSR's mode is not modelled, latched announce, then replace
  M[4:0] of the value written to CPSR with the CURRENT mode (all other bits from the SPSR apply); bank switch decided
  on the result.  In DPI there is no `new_cpsr` local -- the sketch adds one before the switch.
* Save/Load `default:`: `fatal(... (once) ...)` latched per-CPU, then `return` -- no `exit(1)`, no rollback.
* Detector: add rows for (a) SPSR-poisoned `MOVS pc,lr`, (b) SPSR-poisoned `LDM {..pc}^`, (c) zero-SPSR `MOVS pc,lr`
  from boot SVC32, (d) a debugger `put cpsr` reserved value then a mode switch (backstop), and pin I/F in the kill rows'
  readback (field-only vs whole-operation).

Questions, each `<n> | RIGHT / WRONG: <why>`:
1. Which of dispositions 1-12 is wrong?
2. Check the sketch against each caller's control flow (sketch rule): what does it leave reachable, or break?
3. "What is the SMALLEST EDIT to the sketched fix that still passes the 17 rows PLUS rows (a)-(d)?"
**If, while verifying, you found something ELSE — say so.**
