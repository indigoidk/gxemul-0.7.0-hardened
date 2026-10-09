OPUS_MSR_F2_1007

VERDICT: 3 of 12 dispositions wrong (5, 7 and 11). #5's "TWO rows" leaves the restore guards' ACCEPT side unpinned. #7's conclusion stands, but its warrant is false: the text makes the RESULT unpredictable, not just M[4:0]. #11's single debugger row reaches only Save's backstop, so Load's `exit(1)` can stay and pass everything. The sketch also has a build break: a `static` helper cannot be called from the DPI template, which is a separate object.

Tree read: `GXEMUL-SEC/src` at `ef577140`. Read-only; nothing built.

---

## Q1: the twelve dispositions

1 | RIGHT: member 3. Every alternative fails as pass 1 argued, and nothing below changes that.

2 | RIGHT: there are seven `case` labels (`cpu_arm.c:526-558`, `:573-605`). There are six r13/r14 banks: usr/sys, fiq, irq, svc, abt, und.

3 | RIGHT: in msr_imm, Save runs on the old mode (`cpu_arm_instr.c:838-839`) before the CPSR write at `:841-842`. In DPI, Save runs unconditionally at `dpi:218`, also on the old mode. Both are harmless.

4 | RIGHT, and grok's claim is VERIFIED from source:
   * `cpu.c:71` is `zeroed_alloc(sizeof(struct cpu))`.
   * `arm_cpu_new` (`cpu_arm.c:127-138`) sets only `cpsr`. It never writes an SPSR.
   * Repo-wide, the ONLY SPSR writers are `arm_exception` (`cpu_arm.c:676-684`) and `msr_imm_spsr` (`cpu_arm_instr.c:862-879`). No loader, machine or debugger path writes one, because `put` registers only `pc`, `r0-r14` and `cpsr` (`cpu_arm.c:192-196`).
   * So `spsr_svc == 0` until the first exception. A `MOVS pc,lr` from boot SVC32 then runs: Save(SVC) at `dpi:218`, `cpsr = spsr_svc = 0` at `dpi:225`, Load with mode 0, which hits `default: exit(1)` at `cpu_arm.c:606-608`.
   * `LDM {..pc}^` takes the same route through `:1794` -> `:1808` -> `:1812`.
   * **Consequence the disposition does not state:** the restore helper now declines mode 0x00, which is `ARM_MODE_USR26`. The probe BANS `#0` as "the 26-bit hole, a different defect" (`arm_msrmode_probe.py:53-54`). Row (c) drives exactly that hole. The round must CLAIM modes 0x00-0x03 in its contract and correct that docstring line, or the sentence becomes a wrong record (L4) the moment row (c) lands.

5 | WRONG (count): the finding is right, but "TWO detector rows owed" is not enough. The restore guards ADD a predicate, so clause (d) and the accept-row rule each owe a row. Neither (a) nor (b) observes the ACCEPT side, because both stimuli are reserved values. So:
   * **An unconditional substitute passes all 17 rows plus (a)-(d).** The mutant drops the `if (!modelled)` and always keeps the current mode on restore. Every exception return would then stay in the exception mode. See Q3.
   * At least one restore ACCEPT row is owed. A shared helper makes one row carry both sites only if both sites call the same helper; otherwise one per site. Shape: `MSR SPSR_c,#0x1f ; MOVS pc,lr`, want `m=1f` with the usr/sys SP. This lands in SYS, so the readback stays privileged.

6 | RIGHT as policy (see 7).

7 | WRONG (warrant); the conclusion stands as POLICY.
   * **The warrant is false.** "Only M[4:0] is UNPREDICTABLE" does not match the text. `ddi0100i.txt:1877-1879` says "If any other value is programmed into the mode bits M[4:0], **the result** is UNPREDICTABLE". `:9691-9693` says "Several bits must not be changed to reserved values or **the results** are UNPREDICTABLE ... the mode bits (4:0)". The scope is the instruction's result, so whole-operation decline is EQUALLY conformant. grok's own pass-1 said so ("Whole-instruction refusal is also inside UNPREDICTABLE latitude", grok.txt:47).
   * **Being hard on the ruling, as asked:**
     * **MSR:** whole versus field differs on a guest only in I, F and T. Take `#0x14` from 0xd3. Field-only leaves SVC32 with IRQ/FIQ UNMASKED. Whole-op leaves them masked. Under both, the guest's next `mov sp,#...` clobbers r13_svc, because the mode never changed. So whole-op buys "no new interrupt exposure in a mode the guest did not ask to be in", and field-only buys "the masking the guest asked for". Neither is architecture. Record it as a policy choice, exactly as #8 is recorded.
     * **Restore paths: whole-op ("before side effects") is NOT viable.** In DPI, `cpu->pc` is already written at `dpi:215` and Save already ran at `:218`. In `arm_pop`, r0-r15 and the writeback (`:1742-1778`) are done before the SPSR is even selected. Declining "before side effects" there means not returning from the return. Field substitution is the only coherent restore policy.
     * So the ruling holds for the restore paths on the merits, and for MSR as policy. The record must not cite "only M[4:0]".

8 | RIGHT: `ddi0406.txt:143212` reads "An instruction that is UNPREDICTABLE can be implemented as UNDEFINED". The ARMv5 glossary `ddi0100i.txt:45062-45065` forbids halting. Also respect `ddi0406.txt:143210`: "UNPREDICTABLE behavior must not be documented or promoted as having a defined effect". The code comment must call the decline an emulator POLICY, never architecture.

9 | RIGHT in substance. The sketch's `static`, however, contradicts it. See Q2-A.

10 | RIGHT: `msr` reloads `ic->arg[0]` on each call (`:852`); `msr_imm` reads the cached `arg[0]`/`arg[1]` (`:824`, `:833`). Change only the local `mask`.

11 | WRONG (carrier):
   * The backstops are reachable only through `put cpsr`. That part is verified: `CPU_SETTINGS_ADD_REGISTER32("cpsr", ...)` at `cpu_arm.c:196` does no bank switch and no `flags` sync.
   * Row (d), "put cpsr reserved, then a mode switch", reaches **Save's** `default:` only. Planted 0x14, then `MSR CPSR_c,#0x13`, sets `switch_register_banks`. Save hits the backstop, CPSR becomes 0x13, and Load(SVC) is a normal case.
   * Once W3/W4/W5 are guarded, the ONLY route to Load's `default:` is a planted reserved CPSR followed by a DPI S-to-PC. `dpi:219` has no case for 0x14, so CPSR stays reserved and `:232` Load fires. A planted CPSR followed by `LDM^` does not reach it: `arm_pop`'s selector `default:` (`:1795-1799`) sets `running = 0` first.
   * So the shipped detector leaves Load's backstop with NO carrier. Q3 shows that this lets the verbatim `exit(1)` survive.

12 | RIGHT, and FILED is correct.
   * The same `arm_pop` `default:` arm is also what a planted reserved CPSR plus `LDM^` reaches, and there it does `running = 0` rather than kill the process.
   * `mrs_spsr`'s `default:` (`:934-936`) is the same shape. It is operator-only once the fix lands, because USR/SYS have explicit cases at `:932-933`.
   * Neither interacts with this fix.

## Q2: the sketch against each caller's real control flow

**A. BUILD BREAK: `static int arm_mode_is_modelled` cannot serve the DPI caller.**
* `cpu_arm_instr_dpi.c` is not compiled inside `cpu_arm.c`. `generate_arm_dpi.c:97` emits `#include "cpu_arm_instr_dpi.c"` into `tmp_arm_dpi.c`, which `configure:179` builds as its OWN object (`CPU_ARCHS="$CPU_ARCHS tmp_arm_dpi.o ..."`).
* A `static` function in `cpu_arm.c` is invisible there. Declaring it non-static in `cpu_arm.h` while defining it `static` is itself a compile error.
* Make it extern, like `arm_save_register_bank`/`arm_load_register_bank` (`cpu_arm.h:345-346`). `tmp_arm_dpi.c` already sees `cpu_arm.h` through `cpu.h:248`, and it already calls those two externs.
* Pass 1's sketch used `int` (non-static). The brief's `static` is new.

**B. msr_imm.**
* `new_value` is declared at `:833`, AFTER `switch_register_banks` (`:830-832`). The guard must test `ic->arg[0]` (or move the declaration up) and must run before `:830`.
* Clearing `ARM_FLAG_MODE` from `mask` makes `switch_register_banks` 0, so neither Save nor Load runs and `:841-844` apply the rest of the write. Clean.
* USR32 needs no guard (`:826-828`). In SYS32 and in a planted reserved mode the guard is live, which is correct.

**C. arm_pop.**
* Insert between `:1800` and `:1802`, so `switch_register_banks` (`:1802-1803`) is computed on the substituted value.
* **Do NOT copy the adjacent `default:` arm's shape (`fatal ...; return;` at `:1795-1799`).** A `return` there skips `:1816-1825`, the PC load and `quick_pc_to_pointers_arm`, so the "return" falls through to the next instruction.
* Row (b) must observe execution AT THE BRANCH TARGET: the readback sits at the address in the loaded word, and the fall-through is a distinguishable trap.

**D. DPI template.** The edit must sit inside `#ifdef A__S` (`dpi:216-232`), which is itself inside `#ifdef A__PC` and inside `if (ic->arg[2] == ...PC)`.
* Declare the new local inside `#ifdef A__S`. `old_pc`/`mask_within_page` at `:209-214` are `#ifndef A__S`; do not reuse them.
* **Capture the current mode BEFORE the switch**, because `:221-229` overwrite `cpsr`. Reading "current mode" after the switch substitutes the reserved mode with itself and is a no-op mutant.
* **Call the helper only on the arms that copied an SPSR.** USR/SYS, and a planted reserved mode, take no case and leave CPSR as it was. An unconditional call after the switch would:
  * in USR/SYS, see a modelled mode and do nothing (harmless);
  * in a planted reserved mode, announce on the DECLINE latch bit with no guest cause, and substitute old_mode, which is itself reserved. That misattributes an operator plant to the guest-decline bit.
  * Simplest shape: `new_cpsr` with `default: new_cpsr = cpu->cd.arm.cpsr;` and the guard applied only when an SPSR was selected.
* **Do not `return` early, and do not fall out of the block.**
  * `cpu->pc` is already the ALU result (`:215`). An early `return` skips `quick_pc_to_pointers` (`:241`), leaving `next_ic` stale against `pc`: the guest runs the word after `MOVS`.
  * Falling out of the block lets the S-flag update at `:257+` overwrite the restored flags (grok's point, verified). The `return` at `:248` must still run.
* Save (`:218`) on the old mode, then Load (`:232`) on the substituted, equal mode, is an identity for every case (`:526-558` against `:573-605`).

**E. Save/Load backstops.**
* The `return` with no rollback is fine in both functions: both are `void` and nothing follows the switch (`:562`, `:609`).
* Planted 0x14 plus `MOVS pc,lr` fires BOTH backstops in one instruction. That is the row Q3 needs, and with distinct latch bits it must match on the function NAME in the text, not on the generic `"(once)"` that `classify()` tests (`arm_msrmode_probe.py:284`).

**F. I/F pin.** The brief puts it in the kill rows only. It is equally owed in (a), (b) and (c):
* A restore mutant that SKIPS the CPSR write on a reserved SPSR leaves 0xd3, so it reads `m=13` exactly like the fix does.
* The poisoned and zero SPSRs both carry I=F=0, while boot CPSR has I=F=1. That distinguishes the two in the existing sessions.

## Q3: SMALLEST EDIT that still passes the 17 rows plus (a)-(d)

**Primary, a clause-(b) floor breach: leave `exit(1)` in `arm_load_register_bank`'s `default:`** and fix only Save's.
* All 17 rows pass. With W3 guarded, Load never sees 0x14/0x15. The pass-1 M2 sketch already measured 17/17 with the MSR guard in place (`witness_20261007/run_mutant_m2.out`).
* (a), (b) and (c) pass, because the restore guards hand Load a modelled mode.
* (d) passes, because the planted-mode-then-MSR stimulus reaches Save only (#11).
* That is a VERBATIM REINSTATEMENT of the removed defect at one of the two fixed sites, surviving the whole detector.
* **Owed row (d'):** `put cpsr 0xd4`, then `MOVS pc,lr` with a valid target. Want: alive, both backstop texts, and execution at the target.

**Runner-up, a clause-(d) breach of an ADDED predicate: drop the condition from the restore guard** (always keep the current mode). The rows pass as follows:

| rows | what the mutant shows | why the rows pass |
|---|---|---|
| (a), (b) | `m=13` | they want `m=13` |
| (c) | `m=13` | it wants `m=13` |
| 17 MSR rows | unchanged | they never restore |

* Every legitimate exception return is broken, yet no row of this detector reds. Whether the gate battery catches it through an ARM boot is UNMEASURED.
* **Owed:** the restore ACCEPT row in #5. One `MOVS` accept row covers both sites only if arm_pop and DPI share the helper. Otherwise add an `LDM^` accept row too.

**Third, coverage rather than floor: a helper wrong on an unprobed reserved value.** A range form such as `m >= 0x10 && m <= 0x13 || m == 0x17 || m >= 0x1b` admits 0x1c-0x1e. Only 0x14, 0x15 and (c)'s 0x00 are driven, so it passes.
* #9's shared-case-list design defends against it structurally.
* One cheap kill row at `c_1e` pins it. Disclose the rest under clause (e).

**Fourth: one shared latch bit** instead of #11's distinct bits.
* It passes everything, because each row is a fresh process.
* If the round CLAIMS distinct bits, a row must drive a guest decline and then a planted backstop in ONE session and expect both lines. Otherwise drop the claim.

## Something else

* The pass-1 kill rows read `m=13 sp once`. Under field-only, `#0x14` also CLEARS I and F, so the post-fix guest is in SVC with interrupts enabled. The probe's "post-fix ... reserved mode with interrupts unmasked" sentence (pass-1 §7) is still stale against the design.
* DPI S-to-PC ignores an SPSR with T set: there is no `abortdyntrans` on the restored T, and only `pc & 1` is consulted at `:243`. `arm_pop` forces `pc & ~3` (`:1817`). That is an old Thumb-return hole, out of scope. Noted only, so nobody credits this fix with T-correctness on restore.
