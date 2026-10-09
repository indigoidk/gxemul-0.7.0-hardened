OPUS_MSR_PASS1_1007

VERDICT: Member 3 is right, but the decline belongs at the THREE guest-reachable CPSR writers (msr_imm, arm_pop's `^` restore, the DPI S-to-PC restore). At each one, substitute the CURRENT mode into the incoming PSR value and apply every other bit. Do this before the bank-switch decision, so Save/Load never run on the bad value. Both `default:` arms become per-CPU latched backstops with NO rollback. The 17-row probe has no SPSR row, so it stays fully green when the caller-2/3 guards are left out. | 1 premise wrong (provenance only: two of the three files were NOT last changed in #524). Separately, an UNPRIVILEGED, guest-reachable halt of the whole emulator sits beside this row and is not filed.

Tree read: `GXEMUL-SEC/src` at `ef577140` (`git log -1` confirms). All line numbers in the brief match the fork.

---

## 1. Premise audit

**Verified true against the source:**

* cpu_arm.c `:522-563` (Save) and `:569-610` (Load): both `void`, nothing runs after the switch, `default:` ends in `fatal(); exit(1)` at `:559-561` and `:606-608`.
* msr_imm `:822-848`: Save runs on the OLD mode (`:838-839`), CPSR is rewritten (`:841-842`), then Load runs on the NEW mode (`:846-847`). Starting from SVC32, the process dies in Load and Save is never reached. Settled-premise bullet 1 holds.
* "Callers write CPSR between Save and Load": true for all four (`:841`, `:1808`, dpi `:221-229`, `:697-698`).
* `arm_exception`: Load always sees a modelled mode. `arm_exception_to_mode[]` (`cpu_arm.h:116-118`) has a `0` at index 5, but no caller passes 5. The full caller list is cpu_arm.c `:1753`, `:2677`; cpu_arm_instr.c `:999`, `:1012`, `:1025`; cpu_dyntrans.c `:209`; memory_arm.c `:269`, `:273`. The `:674` switch would `exit(1)` on 5 before Load in any case.
* Member 5 for MSR: `ddi0100i.txt:9577-9578` reads "Exceptions / None." Reserved mode bits are UNPREDICTABLE at `:1877-1879` (A2.5.7) and at `:9691-9693` (MSR notes).
* `grep -c armmsrmodekill CHANGELOG.md` = 0. No fix exists.

**WRONG (records only; the conclusion survives):** "the three files last changed in `#524` (`4dfc7165`)". Measured with `git log -1 -- <file>`:

    cpu_arm.c            2c615c3c  Round 112 (#367)
    cpu_arm_instr.c      4dfc7165  #524 (armbdt)      <- only this one
    cpu_arm_instr_dpi.c  a06e92fb  Round 71 (#311-#313)

"No fix exists" is still true. The CHANGELOG count and the live `exit(1)` both establish it.

**Under-stated (not wrong, but it changes Q3):** the brief calls `bdt_load`'s `default:` the "unimplemented mode" arm, as if only a reserved mode could reach it. USR32 and SYS32 reach it too. See §6.

### 1a. EVERY writer of CPSR mode bits, from the source

Method: grepped all of `src/` for `cd.arm.cpsr` and `cd.arm.spsr` (117 hits in 7 files) and read each write.

| # | site | writes mode bits? | guest can make it reserved? |
|---|---|---|---|
| W1 | `cpu_arm.c:127,133,136` arm_cpu_new | yes, the constant SVC32 | no |
| W2 | `cpu_arm.c:196` `CPU_SETTINGS_ADD_REGISTER32("cpsr")` (debugger `put cpsr`) | yes, raw, with no bank switch and no `flags` sync | **operator only**, not guest. It is the one way to PLANT a reserved CPSR, and therefore the way to exercise the backstops (see Q4) |
| W3 | `cpu_arm_instr.c:841-842` msr_imm (and `msr` via `:852-853`) | yes, when the c-byte is in the field mask | **YES**: privileged MSR CPSR_c. The USR32 mask at `:826-828` strips it in USR32 only. SYS32 and every reserved mode count as privileged here |
| W4 | `cpu_arm_instr.c:1808` arm_pop `return_flag` (LDM `{..pc}^`) | yes, `cpsr = new_cpsr` from the current mode's SPSR | **YES, indirectly**, through a poisoned SPSR (§1b) |
| W5 | `cpu_arm_instr_dpi.c:219-230` A__S with Rd=PC | yes, `cpsr = spsr_<mode>` | **YES, indirectly**, through a poisoned SPSR |
| W6 | `cpu_arm.c:697-698` arm_exception | yes, a constant from the table | no |
| -- | `cpu_arm.c:366-367, 671-672`; `cpu_arm_instr.c:835-836, 912-913` | top four bits only (flags merge) | n/a |
| -- | `cpu_arm.c:693,1517-1530,1681-1683,1777`; `cpu_arm_instr.c:355-494`; dpi `:245`; `emul.c:673` | T bit only | n/a |
| -- | `cpu_arm.c:714,717` | I/F only | n/a |
| -- | CPS / CPSID (`cpu_arm_instr.c:4099,4105`) | decoded as NOP | n/a |
| -- | coprocessor (`cpu_arm_coproc.c`), memory_arm.c, cpu_dyntrans.c | READ CPSR only | n/a |

So the brief's three guest writers (W3, W4, W5) are the complete guest set.

### 1b. EVERY writer of an SPSR

| site | guest can make it reserved? |
|---|---|
| `cpu_arm_instr.c:860-880` msr_imm_spsr (and `msr_spsr` `:897-901`) | **YES.** `MSR SPSR_c, #0x14` in any SPSR-bearing mode stores the reserved mode unvalidated. No bank switch, no kill at write time. A later `MOVS pc, lr` (W5) or `LDM {..pc}^` (W4) copies it into CPSR. **Answer to Q1: yes, a reserved mode reaches an SPSR and is restored later.** |
| `cpu_arm.c:674-687` arm_exception copies the CURRENT CPSR into `spsr_<new>` | only if CPSR is already reserved, i.e. only after an operator `put cpsr` once the fix is in |
| debugger | **no**: only `pc`, `r0..r14` and `cpsr` are registered (`:192-196`). No SPSR is `put`-able |

Consequence for the design: a guard in msr_imm alone leaves the SPSR route killing the process through W4/W5.

---

## 2. The disposition, per caller

Architecture: the result is UNPREDICTABLE (`:1877-1879`, `:9691-9693`). The glossary at `ddi0100i.txt:45062-45065` constrains it: *"UNPREDICTABLE instructions or results must not represent security holes. UNPREDICTABLE instructions must not halt or hang the processor, or any parts of the system."*

That one sentence rules out three of today's behaviours: `exit(1)`, every `running = 0` arm, and any choice that grants privilege. It does not mandate a particular register result. Everything below is reasoning inside that envelope.

* **MSR (W3): decline the MODE FIELD and apply the rest of the write** (flags; the c-byte's I, F and T bits). This is the narrowest refusal: the instruction does everything it can legitimately do and skips only the one thing the model cannot represent.
  * Whole-write decline is equally conformant, so the choice is policy. The probe's own `same svc` note already assumes field-only ("member 3 refuses the MODE FIELD, so I|F stay clear").
  * Neither choice is pinned by any row today (Q5).
  * Security check: the guest stays in the privileged mode it was already in, so nothing escalates.
* **LDM^ (W4) and MOVS pc (W5): the same field substitution.** CPSR := SPSR, except that M[4:0] keeps the current mode. The PC write and the flag, I, F and T restore still happen.
  * **FAULT is not supported by the text** for either path. LDM(3) lists only "Exceptions: Data Abort" (`:8138-8140`). Data-processing lists "Exceptions: None" (e.g. ADC `:6540-6541`). Their Operation is plain `CPSR = SPSR` (`:6549`, `:8155`).
  * The UNPREDICTABLE comes from the earlier MSR SPSR write (`:9691-9693`). Raising UND would invent an exception and clobber `spsr_und`/`lr_und`. If the guest is already in UND, that becomes a self-referential mess. Reject member 5 here as well.
* **Member review:**
  * 1 DELETE: wrong. CPSR stays reserved, then Save dies (the brief is correct).
  * 2 silent DECLINE: loses the diagnostic. A guest-drivable condition gets a latch (carrier rule).
  * 3: yes.
  * 4 ACCEPT: nothing computes a valid value.
  * 5 FAULT: no textual basis (above).
  * 6 BACKED ACCEPT: inventing a bank for 25 reserved encodings is a fabrication with no licence.
  * 7 IMPLEMENT: 26-bit modes 0x00-0x03 are named in `cpu_arm.h:104-107` but are a separate architecture feature with no case anywhere. Not this round.
* **An eighth member, or a refinement of 2/3:** *FIELD-DECLINE / SUBSTITUTE*. Accept the instruction and refuse only the poisoned field, by replacing it with the current value. It differs from DECLINE, which refuses the write, and from ACCEPT. It is what I recommend at every site. Name it, so a reviewer does not read "decline" as "skip the whole MSR".

**Scope note the brief omits:** the helper will also refuse modes 0x00-0x0F, the 26-bit hole. The probe docstring (`:59-61`) bans `#0` as a stimulus because "it rows the 26-bit hole, which is a DIFFERENT defect with its own disposition." Today mode 0 also reaches `default: exit(1)`. A helper that declines every non-modelled mode silently disposes of that defect too. That outcome is correct, but the round must CLAIM it (contract, clause (e)) or keep it out.

---

## 3. Where the decline lives

**Recommended: one out-of-line helper, called at W3, W4 and W5, before each site's `switch_register_banks` decision.** Two reasons for out-of-line:

* The DPI template is `#include`d **140 times** (`tmp_arm_dpi.c`). A latch or a large block inside it would be duplicated 140 times.
* The helper's case list should be the SAME seven `case` labels Save and Load use, so the helper and the bank code cannot disagree.

```c
/* cpu_arm.c */
int arm_mode_is_modelled(uint32_t psr)
{
	switch (psr & ARM_FLAG_MODE) {
	case ARM_MODE_USR32: case ARM_MODE_FIQ32: case ARM_MODE_IRQ32:
	case ARM_MODE_SVC32: case ARM_MODE_ABT32: case ARM_MODE_UND32:
	case ARM_MODE_SYS32: return 1;
	}
	return 0;
}
/*  Returns psr with a reserved mode field replaced by cur_mode.  */
uint32_t arm_psr_decline_reserved_mode(struct cpu *cpu, uint32_t psr,
    uint32_t cur_mode, const char *who)
{
	if (arm_mode_is_modelled(psr))
		return psr;
	if (!(cpu->cd.arm.warned_mode & 1)) {
		cpu->cd.arm.warned_mode |= 1;
		fatal("[ %s: reserved mode %i declined, mode unchanged (once) ]\n",
		    who, (int)(psr & ARM_FLAG_MODE));
	}
	return (psr & ~ARM_FLAG_MODE) | (cur_mode & ARM_FLAG_MODE);
}
```

The probe tests `"(once)" in t` (`arm_msrmode_probe.py:248`), so the LITERAL `(once)` is required. `(once per cpu)` would turn every kill row red.

### Sketch-rule traces

**W3, msr_imm.** Insert after `:828`, operating on the LOCAL mask:

```c
if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {
	(void) arm_psr_decline_reserved_mode(cpu, ic->arg[0], 0, "msr");
	mask &= ~ARM_FLAG_MODE;
}
```

* `mask` is byte-granular (`:4320-4325`), so `mask & 0x1f` is either 0 or 0x1f. Clearing 0x1f leaves bits 5-7 (T/F/I) writable.
* Trace: `switch_register_banks` becomes 0 at `:830`. The flags merge at `:835-836` is unchanged. Save is skipped. `:841-842` keeps the old M[4:0] and applies everything else. `flags` syncs at `:844`. Load is skipped. Nothing runs after `:847`. **Clean.**
* **Do NOT write `ic->arg[0]` or `ic->arg[1]`.** For msr_imm they belong to the cached translation, so the edit would persist into every later execution. (`msr` reloads `arg[0]` per call at `:852`; msr_imm does not.)
* USR32 needs no guard: the c-byte is already stripped at `:827`.

**W4, arm_pop.** Insert between `:1800` and `:1802`:

```c
new_cpsr = arm_psr_decline_reserved_mode(cpu, new_cpsr, cpu->cd.arm.cpsr, "ldm^");
```

* Trace: `switch_register_banks` is 0. `:1808` installs flags, I, F and T from the SPSR, with the mode unchanged. `:1809` syncs flags. Load is skipped. `:1816-1825`: the PC load and `quick_pc_to_pointers_arm` run exactly as they do for a modelled return. **Clean.**
* The register writes at `:1742-1775` happened earlier with `s_bit = 0` (because `return_flag`), so they are unaffected.

**W5, DPI A__S.** At `:217`, capture `uint32_t old_mode = cpu->cd.arm.cpsr & ARM_FLAG_MODE;` BEFORE `arm_save_register_bank` (C99 mixed declaration, inside the `if`). After the switch at `:230`:

```c
cpu->cd.arm.cpsr = arm_psr_decline_reserved_mode(cpu, cpu->cd.arm.cpsr, old_mode, "s-pc");
```

* Trace: Save runs on old_mode. CPSR := SPSR with the mode replaced by old_mode. `flags` syncs at `:231`. Load runs on old_mode, which reloads the bank Save just wrote; Save/Load on the same mode is an identity for every case (`:526-558` against `:573-605`). Then `quick_pc_to_pointers` at `:241` and the `pc & 1` → T step at `:243-247`. **Clean.**
* In USR/SYS the switch has no case and CPSR is unchanged, so the helper sees a modelled mode and does nothing.

**W6 (arm_exception) needs no guard.** Its mode is a table constant.

### What each placement leaves reachable

* **Helper at W3 only** (the shape of the brief's working position if the SPSR route is forgotten): `MSR SPSR_c,#0x14 ; MOVS pc,lr` from SVC still reaches Load's `default:`. Post-fix, that is the backstop, so CPSR is left reserved, no host death, but the invariant is broken.
* **Guards inside Save/Load with rollback:** Load cannot roll back. It is `void (struct cpu *)`, and by the time it runs the caller has already overwritten CPSR, so the old mode is gone. Save runs before the write, so there is nothing to roll back. Rollback would need a signature change at all four callers, which is the helper design with extra steps. Reject it as the primary mechanism.
* **Writer-side alternative (A):** guard W3 plus msr_imm_spsr instead of W4/W5. Then no PSR can ever hold a reserved mode, and W4/W5 are covered by induction (arm_exception only copies a modelled CPSR). It is complete for guest paths, but `MRS r0, SPSR` would no longer read back what the guest wrote.
* **Consumer-side (B, recommended):** guard W3, W4 and W5. SPSR storage stays faithful and the guard sits where the bank switch happens. Either A or B is complete. **What is NOT complete is W3 alone.**

---

## 4. The backstops

Once W3, W4 and W5 are guarded, both `default:` arms are **dead to the guest** but **live to the operator**: `put cpsr, 0x14` (W2) followed by any `step` that switches, takes an exception, or takes an IRQ (`cpu_dyntrans.c:208-209` → `arm_exception` → Save `default:`).

Keep them as member 3. Do not delete them, for two reasons:

* An `exit(1)` reachable from a debugger `put` is still a process kill.
* They are the tripwire for any FUTURE CPSR writer (the de-escalation clause's reasoning).

Shape:

* **Save `default:`** — latched announce, skip the memcpy, return. The reserved-mode `r8-r14` are not saved anywhere, which is acceptable under UNPREDICTABLE.
* **Load `default:`** — latched announce, leave `r[]` as is, return. **No rollback**, for the reason in §3.

**Latch location: a per-CPU field** (`uint8_t warned_mode` in `struct arm_cpu`, `cpu_arm.h:136`). `struct cpu` is `zeroed_alloc`'d (`cpu.c:71`), so it needs no init.

* Use separate BITS for decline, save-backstop and load-backstop. A shared bit would let an earlier guest decline silence a later backstop hit, and the backstop is the one you most want to see.
* The house idiom is N = 1 per instance. The one existing ARM latch (`cpu_arm_instr.c:4698`, `static int warned_undef`) is function-static and is the `staticlatchscope` class, so do not copy it.
* On single-CPU `testarm`, per-CPU and static are indistinguishable. Say so in the contract.

The backstops ARE testable, through an operator plant (`put cpsr, 0xd4` then `step` an `MSR CPSR_c,#0x13`). That is NOT a witness, since `armed` correctly rejects a debugger cpsr write as the vehicle. It is an acceptable DETECTOR row for the backstop claim, and without one the backstop claim has no carrier (L3).

---

## 5. Smallest edit that breaks the fix and stays green

**Mutant M1: omit the W5 guard** (or the W4 guard). One deleted line. **All 17 rows stay green, `kill 14` included.**

* Every row is an MSR CPSR stimulus; `grep` of the WORDS dict finds no `msr spsr`, no `movs pc`, no `ldm ^` (`arm_msrmode_probe.py:91-105`).
* Meanwhile `MSR SPSR_c,#0x14 ; MOVS pc,lr` (0xE361F014, 0xE1B0F00E, from SVC) installs reserved mode 0x14 in CPSR. Today that is process death in Load; after the fix with this mutant, it is a backstop line followed by execution in a reserved mode.
* **Owed:** two rows. Each is SPSR-poison then restore, read back with `MRS r3, cpsr` → want `m=13 ... once`. One row via MOVS pc, one via LDM `{pc}^`. That is the sibling-parity cell (W4 and W5 are siblings of W3).

Runners-up, all green today:

* **M2: a helper wrong on an unprobed reserved value.** Only 0x14 and 0x15 are driven. The reserved set is 25 values: 0x00-0x0F (16) plus 0x16, 0x18, 0x19, 0x1A, 0x1C, 0x1D, 0x1E. A range-style helper (e.g. `m >= ARM_MODE_UND32` admitting 0x1C-0x1E) passes. The defence is to build the helper from the SAME `case` list as Save/Load (as above). A cheap extra is one kill row at the top hole, `c_1e`.
* **M3: whole-write decline instead of field-only** (`mask &= ~ARM_FLAG_MODE` → `return;`). `classify()` reads only `cpsr & 0x1F` (`:245`), so the I/F policy is unpinned. Fix inside the EXISTING kill sessions: append the I and F bits to the got string. Under field-only, `#0x14` gives I=0, F=0; under whole-write, they stay at 0xd3's I=1, F=1. No new session.
* **M4: Load backstop with rollback plus no W3 guard** (if someone adds a rollback param). Green on `kill 14/15` and `save 2s`, because the fix's location becomes unobservable. This argues for the no-rollback backstop, which makes M4 inexpressible.

---

## 6. Something ELSE: an UNPRIVILEGED guest stops the whole emulator (not filed)

`grep` of OUTSTANDING_BUGS for USR/SYS against `msr_spsr`/`bdt_load` returns nothing. Two `running = 0` arms are reachable from **User mode** today:

* **`LDMFD sp!, {pc}^` in USR32/SYS32.** `arm_pop` `:1610-1619`: in USR32, `s_bit` is cleared, but `if (iw & 0x8000)` still sets `return_flag`. The `:1784` switch has no USR/SYS case → `default:` `:1795-1799`: `fatal`, `cpu->running = 0`.
* **`MSR SPSR_<any>, #x` in USR32/SYS32.** msr_imm_spsr `:860` has no USR/SYS case → `default:` `:881-893`: `running = 0`.
* With every CPU stopped, `emul.c:1052-1058` `break`s out of the main loop unless debugger-at-end is set. **The emulation ends.**
* The architecture forbids both: LDM(3) is "UNPREDICTABLE in User or System mode" (`:8167-8168`); MSR SPSR with no SPSR is UNPREDICTABLE (`:9640-9648`). By `:45064`, UNPREDICTABLE must not halt.
* Unlike `armmsrmodekill`, this needs **no privilege**: any user process on a guest OS can stop the machine. My reasoning is that it outranks this row on severity. Not measured; it needs a rung-3 witness. File it separately (round-scope rule).
* The design above should not absorb it silently, but the helper shape extends naturally: USR/SYS have no SPSR, so `ldm^` declines the CPSR restore and still loads PC.
* `mrs_spsr` in USR/SYS returns 0 (`:932-933`) and is fine. DPI S-to-PC in USR/SYS leaves CPSR unchanged and is fine.

## 7. Smaller records findings

* **`arm_msrmode_probe.py:50-51` is stale against the design it detects.** It says "post-fix the guest sits in a reserved mode with interrupts unmasked". Under the working position the post-fix mode is 0x13, and the kill rows want `m=13`. Its interrupt-hazard paragraph reasons from a state the fix forbids (L4, wrong record).
  * The true residue: with field-only decline, `#0x14` still CLEARS I and F, so the guest sits in SVC32 with IRQs enabled. Under `continue` it can now take IRQs, legitimately.
* **MSR applies T (bit 5) unfiltered** in privileged modes. `:9624-9626` makes that UNPREDICTABLE, and the model flips `cpsr` T without leaving dyntrans. It does not halt and is out of scope; noted only.
