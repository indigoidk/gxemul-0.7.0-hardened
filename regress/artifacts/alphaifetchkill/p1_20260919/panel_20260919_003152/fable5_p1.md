FABLE_SEAT_ALIVE_20260919_AIFKP1
claude-fable-5-1 | "# CHECKPOINT -- 2026-09-19 00:3x   HEAD: cdbe7d7 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3"
VERDICT: (e), GENERIC, THREE hunks -- hunk 1 as Opus shaped it (no `+1`, no latch), hunk 2 (entry guard), PLUS an epilogue guard keyed on `next_ic == &nothing_call` and NEVER on `!running`; D3 is REVERSED because "a PC row catches the probabilistic case" is a check that cannot fail at ~2^-21 per run.

# alphaifetchkill pass 1 -- Fable 5 seat, adjudicating the shape

**How I worked.**  Read-only; this file is the only write.  Read the packet, brief, `opus5_p1.md`,
`codex_advaifkp1.txt`, the D3 text of `agy.txt` and `ollama_glm.txt`, and the site in full: `cpu_dyntrans.c:100-466`
(the `I` macro, `run_instr`, the epilogue), `:618-838` (`PC_TO_POINTERS_GENERIC`), `:1983-2036` (the
unimplemented-instruction stop); plus `generate_head.c:133-150` (`nothing`/`nothing_call`), `cpu_alpha_instr.c:65-73`
(the `call_pal` precedent), `include/quick_pc_to_pointers.h`, and `cpu_alpha.h:123-125`.  I traced D3 by hand for
both caller kinds and for the device-halt path, since the coordinator's worry is a garbage PC in shipped code.

## Q1 -- GENERIC (D1 upheld)

Only Alpha reaches `:729` today: its translator returns 0 without moving the PC; RISC-V/i960 have no translator
(`:681-684` succeeds); MIPS vectors always translate; ARM/PPC/SH/M88K re-enter `pc_to_pointers` from inside the
exception routine and never return to the outer retry (which is also F2's recursion).  So the generic form is
behaviour-identical on Alpha and unreachable elsewhere, and it removes a latent host kill for any future translator
that fails in place; the `#ifdef DYNTRANS_ALPHA` form (M9) keeps that kill for nothing.  Generic is SAFE only with hunk
2 (the interrupt block at `:206-251` runs after `:190` and, on a delivery-capable architecture, would re-point a
stopped CPU at a handler) and with the epilogue guard below.  codex_adv's Alpha-only preference is the conservative
reading of a packet that lacked Opus's per-architecture table; the table answers it.

## Q2 -- THE SHAPE.  D2 and D4 upheld; D3 REVERSED.

**D2, no `+1` -- upheld, and it is the precedent read correctly.**  `:2023-2024` increments and then EXECUTES `nothing`
at `:2034`, whose body is `next_ic--; ninstrs--;` (`generate_head.c:138-141`), so the precedent nets back to
`&nothing_call` before anything dispatches.  Hunk 1 returns without executing, so `next_ic` must BE `&nothing_call`;
`+1` hands the next `I` (`:114`, `ic = next_ic++; ic->f(...)`) a pointer one past a static and the host crashes.
codex_adv's objection to the brief's literal "(c)" was exactly this and the consolidated shape fixes it.

**D4, no latch -- upheld.**  A stopped CPU is not re-run (`machine_run` filters on `running`), and the only way to hit
the message again is an explicit debugger `continue` with the PC still on the unfetchable address -- one message per
user action, not guest-drivable.  glm's latch would also need semantics nobody has pinned.

**D3 -- REVERSED: add an epilogue guard, and the KEY is the whole ruling.**  Trace, by caller:

*Case A, `run_instr` entry (`:190`).*  Hunk 1 fires, hunk 2 returns 0 before the trace read, the dispatch loop and
the epilogue.  `cpu->pc` untouched, deterministic.  Correct.

*Case B, an instruction handler (`jsr`/`br`/`call_pal`/`end_of_page`) inside the dispatch loop.*  Hunk 1 returns;
the loop continues: every `I` runs `nothing`, which lands back on the sentinel, until `n_translated_instrs >=
N_SAFE_DYNTRANS_LIMIT` -- a BOUNDED spin of ~8K no-op dispatches, microseconds, and `ninstrs` nets to the real count
(`nothing`'s `ninstrs--` cancels the loop's `+120`s).  That spin is what today's unimplemented-instruction stop and
`call_pal` halt already do; do NOT add a `!running` break inside the 120-way unrolled hot loop.  **Then the epilogue
runs** (`:394-414`): `low_pc = ((size_t)next_ic - (size_t)cur_ic_page) / sizeof(IC)` with `next_ic == &nothing_call`
(a file static) and `cur_ic_page` a translation-cache page -- a difference of gigabytes, `/sizeof`, then **truncated
into `int low_pc` (`:180`)**.  The truncated value is uniformly garbage; it satisfies `0 <= low_pc < 2048` (Alpha:
`ALPHA_IC_ENTRIES_PER_PAGE = 1 << 11`) or the two `== ENTRIES(+1)` arms with probability about 2050/2^32 ~ 2^-21 per
run, and under ASLR every run rolls again.  When it lands, `cpu->pc` is page-aligned or bumped a page: the debugger
shows a wrong PC and the fix's own contract sentence ("the PC still names the address that failed") is false.  Opus
named this honestly as "probabilistic, not deterministic"; the `int` truncation is the ROOT CAUSE (a 64-bit `low_pc`
could never satisfy the range).

**Why the packet's disposition is wrong on its own reason.**  "A PC row catches the probabilistic case if it ever
bites" -- it cannot: a row that passes with probability 1 - 2^-21 whether or not the guard exists returns the same
answer in both states.  That is the carrier's check-that-cannot-fail, and a hazard of this shape bites in a real
debugging session, not in a gate.

**The RIGHT guard, one line around the PC-sync block only:**

    if (cpu->cd.DYNTRANS_ARCH.next_ic != &nothing_call) {   /*  #NNN: a sentinel stop already left pc correct;
                                                                  syncing from the sentinel is garbage  */
        ... :395-414 unchanged ...
    }

It fires exactly when the sync's operand is meaningless, and every path that installs the sentinel has already left
`cpu->pc` correct: hunk 1 (untouched), `:2002-2034` (pc set before `bad:`), `call_pal` (`:65-67`, pc computed
first), i960 `ABORT_EXECUTION`, and -- a case nobody named -- `quick_pc_to_pointers_arm` (`quick_pc_to_pointers.h:20-25`),
which puts a RUNNING Thumb CPU's `next_ic` on the sentinel after a BX handler has set the PC, and then hits this same
epilogue.  `nothing_call` is visible in `run_instr` (same TU as the head that defines it), and `next_ic`'s type
matches.  **The guard converts "probabilistically correct" into "deterministically correct" on every sentinel path
and changes nothing else.**

**The TWO WRONG keys, named so they do not ship:**
- **`if (!cpu->running)` -- WRONG.**  A device handler can clear `running` mid-block (the 8259 "unimplemented
  command" arm; `halt_on_nonexistant_memaccess`); the loop does not check `running` (`:114`), so real instructions
  keep executing until `N_SAFE`, with `next_ic`/`cur_ic_page` still VALID page pointers.  There the epilogue sync is
  what makes `pc` right; a `!running` guard would leave it stale at the block start -- a REGRESSION for every
  device-driven halt.  It also misses the running-Thumb case.  This is the trap the coordinator feared.
- **glm's new `ifetch_stop_latched` field -- WRONG site for the key.**  It guards only this stop, leaving the
  identical hazard on the unimplemented-instruction, `call_pal` and Thumb paths, and adds a latch whose semantics
  glm itself says are unpinned.

**Is the guard owed, or filed?  OWED, and it is falsifiable.**  Its warrant is a derivation, not "cannot hurt": the
sync is provably meaningless when `next_ic` is the sentinel and provably needed otherwise.  Its kill mutant is the
LICENSED COMPOSITE (carrier shape ii, each part green alone): {epilogue guard removed} + {M5, `cur_ic_page =
&nothing_call` in hunk 1} -> `low_pc == 0` deterministically -> `pc` page-aligned -> the `pc` row (non-aligned target
`0x1044080`) REDS.  Guard-removed alone is green (probabilistically); M5 alone under the guard is green (sync skipped).
**Consequence for the PRETABLE: M5 becomes EQUIVALENT once the guard ships; the composite replaces it.**

**Other choices within hunk 1, upheld:** `debugmsg_cpu` at ERROR (precedent `:2005-2009`; visible under `-q`; trips
break-on-ERROR); `about_to_enter_single_step` kept for parity (only observable on `-n >= 2`); `debugger_reset()` kept
(the `step 100` case at `:2019-2021`); `cur_ic_page` untouched (NULL would crash `:269`->statistics; the sentinel would
make `low_pc` 0); delay-slot flag as `:2026-2031`; the message on its own line (Opus #3: the FATAL had none).

## Q3 -- THE DETECTOR, with the binding discriminator

Applying #540's rule (floor = body-induced partitions that flow into an operand of the edited statement, crossed with
the dominating predicates):

- **Hunk 1's floor** is one reachable cell: second-`!ok` with `pc == pc_before` (Alpha).  The `pc != pc_before`
  branch of the message selector is unreachable in this tree (no architecture returns to `:729` with a moved PC):
  DISCLOSE, with M7 (stop only when moved, keep the exit for Alpha's case -> `alive` reds) as its pin.  Rows for the
  cell: **alive** (clean `WIFEXITED` 0), **no FATAL**, **stop msg x1 after a further `step 3`**, **stopped** (`-V`
  "All machines stopped", CTRL-T `stopped`), **ninstrs frozen**, **pc == 0x1044080 exactly**, **no fall-through**
  (marker after the JMP keeps SENT: kills M3/(b)), **no garbage page** (markers in the old code page, the identity
  page and paddr 0: kills M2/(a)).
- **Hunk 2's floor** is its dominating predicate, `!running` after `:190`: rowed by reach path 3 (`pc=<unmapped>` then
  `step 1`), whose channel is deterministic -- no extra `wasn't found`/`could not read the instruction` lines (M8 reds
  it; on Alpha M8 is otherwise equivalent and its interrupt-block hazard is disclosed as delivery-arch-only).
- **The epilogue guard's floor** is `next_ic == &nothing_call` at the epilogue, reached only via case B: the `pc` row
  under the JMP path, killed by the composite above.
- **Clause (e), not floor:** JMP vs `end_of_page` (same path through hunk 1; keep both as free pins), single-step vs
  free-running (changes the spin length, not any guard operand; the witness steps -- add a breakpoint+`continue`
  reach if cheap, else disclose), `-V` vs no `-V` (Opus #2: settled by `emul.c:1052-1058`; the row must say which it
  asserts).

F1's two witness defects (page-aligned target; nothing planted after the JMP) are real and both blind the rows above;
ACCEPT.  The rows are SUFFICIENT once the composite is added and M5 is re-predicted.

## Q4 -- the seven dispositions

**D3 REVERSED** (above): add the sentinel-keyed epilogue guard; never the `!running` form.  **D1, D2, D4 upheld.**
**F1 upheld.**  **F2 upheld**: `excvecrecurse` is a different class (unbounded recursion -> host stack overflow), on
architectures this fix does not touch, unwitnessed -- its own row, MED until Opus's ARM vehicle (MMU on, vector page
unmapped, one jump) witnesses it.  **F3 upheld and AMENDED**: nine mutants as the PRETABLE's start, plus the composite
{guard removed + M5}; M5 alone re-predicted EQUIVALENT under the guard; M9 equivalent-on-Alpha, disclosed as the
untestable generic claim.

How I checked: I traced the `I` macro and the epilogue for entry and handler callers, confirmed `nothing`'s body and
`nothing_call`'s definition in the generator, confirmed the `int` truncation at `:180`/`:395`, found the running-Thumb
sentinel path in `quick_pc_to_pointers.h`, and traced a device-driven `running = 0` through the unchecked loop to show
why `!running` is the wrong key.  The one disposition that turned on an argument rather than a reading was D3, and
the argument was a check that cannot fail.

## Found something else
1. **The same probabilistic PC clobber exists today on three shipped paths** -- the unimplemented-instruction stop,
   `call_pal` HALT, and every ARM Thumb switch through `quick_pc_to_pointers_arm` (a RUNNING CPU; derived, not
   witnessed).  The sentinel-keyed guard fixes all three as a side effect.  Record that as a fact in the CHANGELOG,
   not as this round's claim; the ARM case deserves its own witness (BX to Thumb, then CTRL-T `pc`).
2. **A device-driven `running = 0` does not stop the dispatch loop**: guest code runs up to `N_SAFE` more instructions
   after a device "halt" (`:114` never checks `running`).  Pre-existing, not this round -- but it is the fact that
   makes `!running` the wrong epilogue key, and it belongs in the record so nobody "tidies" the key later.
3. **Root cause of the probabilism is `int low_pc` truncating a `size_t`** (`:180`, `:395`).  A width change would
   also cure it but alters the `>= 0`/`== ENTRIES(+1)` arms for every architecture; the sentinel guard is the surgical
   form.  Noted so the record explains WHY the hazard is probabilistic rather than leaving "in practice" as the
   warrant.
