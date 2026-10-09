OPUS_MSR_PASS2_1007

VERDICT: SHIP-WITH-CHANGES -- the code fix is correct at all three writers and both backstops, but the 26-row detector is swept clean (26/26) by EIGHT measured fix-side mutants from three classes | 3 floor breaches

Tree reviewed: `GXEMUL-SEC/src` working tree over HEAD `ef577140`, round files only. Every measurement below was taken in MY OWN clone, `/tmp/gxopus562/tree`. That clone is a `cp -a` of `/tmp/gxmsr2/fix` (configured, read only), with the four SEC working-tree fix files copied in and `cmp`-verified. The probe ran from a frozen copy of the SEC working-tree `regress/arm_msrmode_probe.py`. Each build did `rm src/cpus/*.o gxemul` and passed the freshness check `[ gxemul -nt <each of the 4 sources> ]`. Logs:
- `scratchpad/opus562/KT.out` and `KT2.out` (results); per-mutant `*.out` beside them, each ending `ARMMSRMODE_DONE`.
- `mut.py` and `mut2.py` (mutants); `kt.sh` and `kt2.sh` (drivers).

Clone final state: sentinel cleared, all four sources `cmp`-clean against SEC, binary fresh (`verify.sh`). I wrote nothing into any project tree.

```
OPUS KT  (15:03)  BASE             26/26  REDS=none
                  O_latch_msr      26/26  REDS=none      <- ESCAPE
                  O_mask_nibble    26/26  REDS=none      <- ESCAPE
                  O_dpi_svconly    26/26  REDS=none      <- ESCAPE
                  O_pop_svconly    26/26  REDS=none      <- ESCAPE
OPUS KT2 (15:32)  BASE             26/26  REDS=none
                  O_msr_noconj     24/26  REDS=no cbit,usr mask   (killed -- discharges an un-mutated conjunct)
                  O_latch_pop      26/26  REDS=none      <- ESCAPE
                  O_latch_dpi      26/26  REDS=none      <- ESCAPE
                  O_latch_load     26/26  REDS=none      <- ESCAPE
```

---

## Did the implementation honour what I asked for in pass 1 / F2? YES, on every item.

- **Restore ACCEPT rows:** `acc movs` and `acc ldm` (want `m=1f if=0`). `M_uncond_*` measured killed.
- **I/F pin on the restore rows:** `pin_if=True` on `rst movs`, `rst ldm` and `zero spsr`.
- **Both backstop rows:** `dbg save`, plus `dbg both` as the only carrier of Load's backstop. `M_load_exit` is measured killed by `dbg both`.
- **Extern helper:** `int arm_mode_is_modelled(uint32_t)` is declared in `cpu_arm.h` and is non-static. That is correct for `tmp_arm_dpi.o`.
- **No early returns.** In arm_pop, the decline sits between the selector and `switch_register_banks`, and the PC load still runs (`M_pop_return` measured killed). In DPI there is no `return` before `quick_pc_to_pointers`, and the `return` that skips the S-flag update still runs.
- **DPI captures `cur_mode` BEFORE the switch, and guards on `spsr_copied`** (`M_dpi_uncond_call` measured killed).
- **The 26-bit hole is now CLAIMED in the header**, and the stale "post-fix reserved mode with interrupts unmasked" sentence is gone.

What pass 1 / F2 did NOT ask for, and this pass finds missing, is below.

---

## Q1 -- Premise audit: which statements are wrong?

1. **The contract lines "the guard dropped at arm_pop (rst ldm) or DPI (rst movs, zero spsr)" and "a restore guard made unconditional (acc movs, acc ldm)" are true ONLY AT THE SVC32 LABEL.**
   - Every restore row, `latch ind` included, runs the restore from SVC32.
   - Both restore sites DISPATCH on the current mode to choose the SPSR: arm_pop's selector switch, and the DPI `switch (cur_mode)`. The selected value flows straight into `new_cpsr`, which the guard reads and the repair rewrites.
   - A guard dropped or conditioned at the IRQ, ABT, UND or FIQ label is invisible to the detector: `O_dpi_svconly` and `O_pop_svconly` score 26/26. So the brief's claim that the guards are "nulled-repair covered (see table)" overstates the coverage. See Q4.

2. **The kill-table excerpt in the brief interleaves the ABORTED run 2a without saying so.**
   - Lines 46-48 (`FIXED_probe2 25/26`, `HEAD_probe2`, `BASE_probe2 25/26`) are run 2a. `KILLTABLE.out` itself records that run as "ABORTED after BASE (want omitted the generic once token)".
   - The brief prints two `FIXED_probe2` lines with different scores and no marker between them. Mark 2a as aborted, or drop those lines. Records only.

3. **"M_shared_msrpop ESCAPED the 25-row probe" understates the escapes.**
   - All three pairwise decline-share mutants escaped the 25-row probe: `M_shared_msrdpi_old` and `M_shared_popdpi_old` are both 25/25.
   - The next clause ("closes it and the two DPI pairings") implies this, but the escape count should read three, not one.

4. **"Both `default:` arms ... reachable only by a debugger `cpsr=` assignment" is right about the CAUSE but not about the TRIGGER.**
   - After a plant, the arms are reached by an ordinary guest instruction or event: an MSR, an exception entry, or an IRQ (`cpu_dyntrans.c` -> `arm_exception` -> Save).
   - Saying "reachable only from a debugger-planted reserved CPSR" is the accurate form. Not a defect.

5. **Holds, verified:**
   - "HEAD 16/26, every red `dead`": all ten FAIL lines in `HEAD_probe2.out` read `got=dead`.
   - `cpu_new` zero-fills `mode_warned` and every SPSR: `zeroed_alloc` is used, and `arm_cpu_new` writes only `cpsr`, which is SVC32 on both branches.
   - Exactly three guest CPSR-mode writers exist: grep of `arm.cpsr =` and of the `cpsr |=` sites.

## Q2 -- Is each guard right against its caller's real control flow?

**msr_imm -- correct.**
- The USR strip runs first.
- The guard tests the cached `ic->arg[0]` and clears only the local `mask`. It sits BEFORE `switch_register_banks` is computed, so no Save or Load runs, and `cpsr &= ~mask; |= new & mask` applies the rest of the field (I, F, T).
- The `msr` (register) form rewrites `arg[0]` on every call, so it is covered too.
- The `(mask & ARM_FLAG_MODE)` conjunct is load-bearing and is now MEASURED: dropping it reds `no cbit` and `usr mask` (`O_msr_noconj`, 24/26).

**arm_pop -- correct.**
- The decline sits after the selector `switch` and before `switch_register_banks`. There is no `return`; the PC load and `quick_pc_to_pointers` run.
- `new_cpsr` keeps the current mode, so banks are not switched, which is an identity.

**DPI -- correct.**
- `cur_mode` is captured before the switch, and `new_cpsr` defaults to the current CPSR.
- The guard is gated on `spsr_copied`. The CPSR is written once, `flags` is written after it, and Load runs on the same mode Save ran on (an identity).
- No early return; the `return` that skips the S-flag tail is untouched.

**Save/Load backstops -- correct.** Both functions are `void` and the `default:` arm is the last statement, so `return` is the only safe exit and no rollback is needed.

**Any path left to `exit(1)` or `running = 0` by a reserved mode?**
- **From guest-only state: none.** All three writers decline, and `arm_exception` writes only table modes.
- **From a debugger-planted reserved CPSR, three pre-existing `running = 0` arms remain:**
  - arm_pop's selector `default:` (`bdt_load: unimplemented mode`);
  - `msr_imm_spsr`'s `default:`;
  - `mrs_spsr`'s `default:`.

  All three are operator-only. They stop the CPU, not the process, and are out of scope.
- The USR/SYS `LDM {pc}^` / `MSR SPSR` stops are guest-reachable without privilege and are filed separately (correctly).

**Noted, pre-existing, not introduced:** in USR/SYS, DPI S-to-PC executes `flags = cpsr >> 28` on a CPSR whose top nibble may be stale relative to the live `cpu->cd.arm.flags`. HEAD does the same, and the case is UNPREDICTABLE architecturally. The fix preserves it byte for byte, which is right for this round.

## Q3 -- Smallest edit to the FIX that keeps all 26 rows green (BUILT AND MEASURED)

**Winner: delete ONE statement, `cpu->cd.arm.mode_warned |= ARM_MODEWARN_MSR;` -> `O_latch_msr`, 26/26.**
- **Why it stays green:** the detector never drives any announce site twice in one process. Every row runs a fresh process, and `latch ind` fires each decline exactly once. So "announces once" and "announces every time" render identically. `kill 14`, `kill 15` and `kill 1e` each still read ` once`.
- **Same escape at the other sites:** `O_latch_pop`, `O_latch_dpi` and `O_latch_load` are each 26/26. `O_latch_save` was not built, but its only carriers are `dbg save` and `dbg both`, which fire Save once each, so it is the same shape.
- **Consequence:** an unbounded `fatal()` per guest MSR, or per restore of a poisoned SPSR. `fatal()` cannot be silenced by `-q`. That is the guest-drivable log flood that member 3's LATCH exists to prevent, so the round's chosen disposition ("decline + LATCHED announce") is unpinned on its latch half.

**One-token runner-up: narrow the repair mask, `mask &= ~ARM_FLAG_MODE;` -> `mask &= ~0x0f;`. `O_mask_nibble`: 26/26.**
- **Why it stays green:** every MSR stimulus (0x14, 0x15, 0x1e) has bit 4 set, so the narrowed mask still writes bit 4 = 1 and keeps the old low nibble, giving `m=13`.
- **Consequence:** `MSR CPSR_c,#0x00..#0x0f` from SVC writes mode 0x03. Load's backstop then fires from a GUEST instruction, and the guest continues in a reserved 26-bit mode. That falsifies "the backstops are reachable only by a debugger plant".
- **Not covered by the disclosure:** `zero spsr` drives 0x00 through DPI, never through MSR. The existing disclosure covers "helper errors at 0x01-0x0f", and this is a MASK error, not a helper error.
- This is the canonical clause-(d) shape: a mask narrowed while still reading like the same check.

**Label conjunct: `&& cur_mode == ARM_MODE_SVC32` on the DPI guard (`O_dpi_svconly`), or the matching `(cpsr & MODE) == SVC32 &&` on arm_pop's guard (`O_pop_svconly`). Both 26/26.**
- **Why they stay green:** all restore rows run from SVC.
- **Consequence:** an IRQ, ABT, UND or FIQ handler returning through a poisoned or never-written SPSR puts the guest in a reserved mode, and Load's backstop fires from guest code. That is `M_drop_*`'s defect, re-opened at four of five labels.
- **The same hole admits the accept-side mutant.** For example, `if (cur_mode == ARM_MODE_IRQ32 || !modelled)` always keeps the mode on an IRQ return. Only `acc movs`/`acc ldm` could see that, and they run at the SVC label only.

## Q4 -- Floor check

- **(a) Pre-fix build: 16/26.** Verified.
- **(b) Verbatim reinstatement:**
  - `M_load_exit` is killed by `dbg both`, and `M_save_exit` by `dbg save` and `dbg both`.
  - The latched-`exit(1)` variants are killed the same way.
  - Pass.
- **(c) Identity:** the `row count` row equals 26, and the `enc ok`, `live`, `pc adv` and `armed` controls are present. Pass.
- **(d) Nulled repair:**
  - The drops and unconditional forms of all three guards are killed at the SVC label, and the helper `always1` and range forms are killed.
  - **Three un-mutated DEPENDS-ON classes escape, so (d) FAILS:**

  | breach | predicate the fix depends on | measured escape | cheapest repair (rows) |
  |---|---|---|---|
  | **F1: latch nulled** | the five ADDED `!(mode_warned & BIT)` predicates. Deleting the `|=` makes each always-true. | `O_latch_msr`/`pop`/`dpi`/`load`, 26/26 each | Drive each site TWICE in one session and require EXACTLY ONE text per site: count matches, not `any()`. Concretely: add a second `c_15` to `latch ind` and a second MOVS in `dbg both`. A second LDM^ and a second DPI decline need one more chained plant, or a sibling `latch rpt` session. About 1-2 sessions. |
  | **F2: repair mask narrowed** | the ADDED `mask &= ~ARM_FLAG_MODE` | `O_mask_nibble`, 26/26 | One kill row at a bit-4-clear value: `kill 03` = `MSR CPSR_c,#0x03` (0xE321F003), want `m=13 if=0 sp once`. It also kills a helper wrong at 0x03. One session. |
  | **F3: restore-selector LABEL axis** (carrier, 2026-09-09: the selector flows into `new_cpsr`, which the guarded body reads and writes) | arm_pop's and DPI's `switch` on the current mode x the guard's {modelled, unmodelled} partition: 5 labels x 2 per site, of which ONLY the SVC cells are rowed | `O_dpi_svconly` and `O_pop_svconly`, 26/26 each | Per site, ONE chained session: `MSR CPSR_c,#0xd2` (IRQ) -> `MSR SPSR_c,#0x14` -> restore -> MRS readback (want mode kept, 0x12), then the same at ABT, UND and FIQ. Use **`movs pc, r5` (0xE1B0F005)** for DPI, not `lr`, because r14 is banked in every exception mode while r5 is unbanked (FIQ banks only r8-r14). The latch makes only the first announce appear, so the channel is the per-label MODE READBACK, not the text. The accept side is the same chain with SPSR=0x1f and an MSR back to the next label. About 4 sessions. |

- **Grading.**
  - F1 and F2 weaken predicates the fix ADDED, which is clause (d) in its original form. They are L2 and should be repaired in-round.
  - F3 is the label clause (`sgimtedepth4dead`, 2026-09-09): "a detector rowing one label ... was swept by `&& dst_tlb == MTE_TLB_A`". Same shape, same grade, and the cells are trivially guest-reachable by privileged MSR mode switches.
- **The msr_imm guard has NO label axis.** Its body tests only `== USR32`, and that partition is rowed by `usr mask`. An `&& cur == SVC` conjunct there is a value the body never tests as a case, so it is clause (e), disclosable.
- **Discharged this pass:**
  - `(mask & ARM_FLAG_MODE)` conjunct dropped: `O_msr_noconj` 24/26, killed by `no cbit` and `usr mask`.
  - `spsr_copied`: `M_dpi_uncond_call`, killed.

## Q5 -- Records: added claims a row or measurement does not support

1. **The `cpu_arm.h` comment** says "the three guest declines and the two register-bank backstops each announce once per CPU, independently", and all five message texts carry `(once)`.
   - INDEPENDENTLY is measured: `latch ind`, `dbg both`, and table 2.
   - ONCE is measured by nothing; F1 escapes at all four sites tested.
   - The comment is true by reading and unpinned. Repair F1, or the CONTRACT owes a "latch once-ness: NOT CLAIMED" line.
2. **Probe CONTRACT bullets 3 and 4** (guard dropped / unconditional at arm_pop and DPI) need "at the SVC32 label" until F3 lands. As written, they claim coverage that `O_*_svconly` refutes. That is L4.
3. **Probe CONTRACT, NOT-CLAIMED list:** add the repair-mask width (F2) unless `kill 03` lands.
4. **Probe docstring, lines 38-41: "verified by reading cpu_arm.c at HEAD: cpu_arm.c:606-608 ... :559-561 ... exit(1)".**
   - After this commit, HEAD has no `exit(1)` there, and the arms have moved to about `:585` and `:641`.
   - Line 2's "One privileged MSR ends the PROCESS" now describes pre-#562 behaviour.
   - Qualify both as "pre-#562 (ef577140)". Minor L4.
5. **Save backstop comment:** "a debugger `cpsr=` assignment still does [get here]". Tighten it to "only after a debugger `cpsr=` plant (then any mode switch, exception or IRQ reaches it)". Not false, just imprecise about the trigger.
6. **msr_imm comment:** "Only the local mask changes: ic->arg[] is a cached translation". Correct by reading (`arg[0]` is never written in `msr_imm`) and honestly disclosed as unrowed. No action.
7. **The DDI 0100I / ARMv7 citations and "POLICY, not an architectural requirement"** match my F2 ruling. Good.

## Something else

- **The record should name the cost asymmetry.** F2 and F3 re-open the guest-to-reserved-mode path, but post-fix that lands on a BACKSTOP, not a process death. So the escapes' guest consequence is "UNPREDICTABLE state plus an announce", not a host kill. That is why they are floor breaches against the round's CLAIMS ("reachable only by a debugger"; "decline at the three writers") rather than severity regressions.
- **F1 is the one with host-side cost:** an unbounded `fatal()` stream that is unsilenceable under `-q`.
- **Suggested in-round repair size:** roughly six new or extended sessions (F1: 1-2, F2: 1, F3: 4), then a re-run of the eight `O_*` mutants plus BASE. The mutant definitions are in `scratchpad/opus562/mut.py` and `mut2.py`, presence-pinned like the round's `mutate.py`.
- **Not built:** `O_latch_save`, and an accept-side label mutant. Both are predicted to escape for the reasons above; neither is measured.
