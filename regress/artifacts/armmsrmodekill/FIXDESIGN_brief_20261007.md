# armmsrmodekill -- pass 1: how should a reserved ARM mode be handled at the register-bank switch?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `ef577140`).  There
are THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers disagree with mine by hundreds
you are reading one of them — say so rather than reconciling.  Read-only: write nothing, build nothing.

**If you cannot read files that is expected** — every fact you need is inlined below.  Name any premise you cannot
settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim, ENUMERATE it.  And ENUMERATE THE RIGHT DOMAIN** — ask what the
PRODUCER of a value can actually emit before walking it.

**VERDICT LINE FIRST**, so your answer survives truncation:
`VERDICT: <recommended disposition in one line> | <n> premises wrong`

## 1. The defect (a design question; the reproduction is being repaired separately)

`arm_save_register_bank()` and `arm_load_register_bank()` in `src/cpus/cpu_arm.c` each switch on
`cpsr & ARM_FLAG_MODE` (5 bits) over the six modelled modes and end in

    default: fatal("arm_..._register_bank: unimplemented mode %i\n", cpsr & ARM_FLAG_MODE);
             exit(1);

so a guest that puts a RESERVED mode in CPSR ends the emulator PROCESS.  The ARM ARM calls a reserved M[4:0]
UNPREDICTABLE, not fatal.  A privileged `MSR CPSR_c, #0x14` (word `0xE321F014`) on `-E testarm` is the filed
trigger.

## 2. SETTLED PREMISES (re-inlined so nobody spends an answer re-deriving them; CHALLENGE any you doubt)

* **Save is not the first hit for MSR** -- in `msr_imm`, Save runs on the OLD mode (e.g. SVC32, modelled) and
  returns; CPSR is then rewritten; Load runs on the NEW (reserved) mode and dies.  A Load-only fix therefore makes
  the NEXT mode switch die in Save (CPSR now holds the reserved mode).  -- row `armmsrmodekill`, grok trace 2026-09-17.
* **Callers write CPSR BETWEEN Save and Load** (all four callers below).  So a decline placed only inside Load
  leaves CPSR holding the reserved mode unless Load also rolls it back.  -- same row.
* **Member 1, DELETE (just drop the `exit(1)`), is WRONG**: CPSR stays reserved and `r[]` stays on the previous
  bank -> silent wrong-bank execution, then the next switch hits Save's default.  -- same row.
* **Member 5, FAULT, is available on ARM but wrong for MSR**: the ARM ARM lists MSR as "Exceptions: None".
  -- same row.  (For the SPSR-restore callers the question is open -- see §4.)
* **`fatal()` does not exit**; it prints regardless of `-q`.  A guest-drivable `fatal()` needs a LATCH (house idiom
  `N = 1` per instance + a `(once)` marker in the text), not a verbosity flag.  -- carrier rule.
* **Has it shipped?**  `grep -c armmsrmodekill CHANGELOG.md` = 0; the three files last changed in `#524`
  (`4dfc7165`).  No fix exists.

## 3. The full code (verbatim at HEAD `ef577140`; line numbers in the left column)

### `src/cpus/cpu_arm.c` -- both functions

```c
522	void arm_save_register_bank(struct cpu *cpu)
523	{
524		/*  Save away current registers:  */
525		switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
526		case ARM_MODE_USR32:
527		case ARM_MODE_SYS32:
528			memcpy(cpu->cd.arm.default_r8_r14,
529			    &cpu->cd.arm.r[8], sizeof(uint32_t) * 7);
530			break;
531		case ARM_MODE_FIQ32:
532			memcpy(cpu->cd.arm.fiq_r8_r14,
533			    &cpu->cd.arm.r[8], sizeof(uint32_t) * 7);
534			break;
535		case ARM_MODE_IRQ32:
536			memcpy(cpu->cd.arm.default_r8_r14,
537			    &cpu->cd.arm.r[8], sizeof(uint32_t) * 5);
538			cpu->cd.arm.irq_r13_r14[0] = cpu->cd.arm.r[13];
539			cpu->cd.arm.irq_r13_r14[1] = cpu->cd.arm.r[14];
540			break;
541		case ARM_MODE_SVC32:   /* ... same shape, svc_r13_r14 ... */
546			break;
547		case ARM_MODE_ABT32:   /* ... same shape, abt_r13_r14 ... */
552			break;
553		case ARM_MODE_UND32:   /* ... same shape, und_r13_r14 ... */
558			break;
559		default:fatal("arm_save_register_bank: unimplemented mode %i\n",
560			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
561			exit(1);
562		}
563	}

569	void arm_load_register_bank(struct cpu *cpu)
570	{
571		/*  Load new registers:  */
572		switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
573		case ARM_MODE_USR32:
574		case ARM_MODE_SYS32:
575			memcpy(&cpu->cd.arm.r[8],
576			    cpu->cd.arm.default_r8_r14, sizeof(uint32_t) * 7);
577			break;
578		case ARM_MODE_FIQ32:
579			memcpy(&cpu->cd.arm.r[8], cpu->cd.arm.fiq_r8_r14,
580			    sizeof(uint32_t) * 7);
581			break;
582		case ARM_MODE_IRQ32:   /* memcpy default 5, then r13/r14 from irq_r13_r14 */
587			break;
588		case ARM_MODE_SVC32:   /* ... svc ... */
593			break;
594		case ARM_MODE_ABT32:   /* ... abt ... */
599			break;
600		case ARM_MODE_UND32:   /* ... und ... */
605			break;
606		default:fatal("arm_load_register_bank: unimplemented mode %i\n",
607			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
608			exit(1);
609		}
610	}
```
*(The SVC/ABT/UND arms are CONDENSED here -- each is the IRQ arm's shape with its own `_r13_r14` array.  Both
functions are `void`; neither has any code after the switch.)*

### Caller 1 -- `msr_imm` (and `msr`, which sets `arg[0]` from a register and calls it), `src/cpus/cpu_arm_instr.c`

```c
822	X(msr_imm)
823	{
824		uint32_t mask = ic->arg[1];
826		if ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32) {
827			mask &= 0xff000000;
828		}
830		int switch_register_banks = (mask & ARM_FLAG_MODE) &&
831		    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
832		    (ic->arg[0] & ARM_FLAG_MODE));
833		uint32_t new_value = ic->arg[0];
835		cpu->cd.arm.cpsr &= 0x0fffffff;
836		cpu->cd.arm.cpsr |= (cpu->cd.arm.flags << 28);
838		if (switch_register_banks)
839			arm_save_register_bank(cpu);
841		cpu->cd.arm.cpsr &= ~mask;
842		cpu->cd.arm.cpsr |= (new_value & mask);
844		cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
846		if (switch_register_banks)
847			arm_load_register_bank(cpu);
848	}
```

### Caller 2 -- `LDM ... ^` with PC in the list (`bdt_load`), `src/cpus/cpu_arm_instr.c`

```c
	/* new_cpsr = the SPSR of the CURRENT mode, chosen by a switch whose default: is */
1795		default:fatal("bdt_load: unimplemented mode %i\n",
1796			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
1797			cpu->running = 0;
1798			cpu->cd.arm.next_ic = &nothing_call;
1799			return;
1800		}
1802		switch_register_banks = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
1803		    (new_cpsr & ARM_FLAG_MODE);
1805		if (switch_register_banks)
1806			arm_save_register_bank(cpu);
1808		cpu->cd.arm.cpsr = new_cpsr;
1809		cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
1811		if (switch_register_banks)
1812			arm_load_register_bank(cpu);
```

### Caller 3 -- data-processing with S and destination PC (`MOVS pc, lr`, `SUBS pc, lr, #4`), `src/cpus/cpu_arm_instr_dpi.c`

```c
216	#ifdef A__S
217		/*  Copy the right SPSR into CPSR:  */
218		arm_save_register_bank(cpu);
219		switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
220		case ARM_MODE_FIQ32:
221			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_fiq; break;
222		case ARM_MODE_IRQ32:
223			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_irq; break;
224		case ARM_MODE_SVC32:
225			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_svc; break;
226		case ARM_MODE_ABT32:
227			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_abt; break;
228		case ARM_MODE_UND32:
229			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_und; break;
230		}
231		cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
232		arm_load_register_bank(cpu);
```
*(Note: unconditional Save and Load, no `switch_register_banks` test; no `default:` -- in USR/SYS32 CPSR is left
unchanged.)*

### Caller 4 -- `arm_exception()`, `src/cpus/cpu_arm.c`

```c
669		arm_save_register_bank(cpu);              /* on the CURRENT mode */
   ...
697		cpu->cd.arm.cpsr &= ~ARM_FLAG_MODE;
698		cpu->cd.arm.cpsr |= arm_exception_to_mode[exception_nr];   /* always a modelled mode */
   ...
720		arm_load_register_bank(cpu);
```
*(Load here always sees a modelled mode.  Save sees whatever mode the guest was in -- so an exception taken while
CPSR holds a reserved mode dies in Save.)*

## 4. The question: which disposition, and where?

The project's option set for a guest-drivable host kill has seven members; please consider every one, and say if
there is an eighth:

1 DELETE · 2 DECLINE (silent) · 3 DECLINE + LATCHED ANNOUNCE (`(once)`) · 4 ACCEPT · 5 FAULT · 6 BACKED ACCEPT ·
7 IMPLEMENT.

The row's working position (challenge it): **member 3, and the decline must happen BEFORE Save** -- i.e. a reserved
mode is never allowed into CPSR at all -- because every caller writes CPSR between Save and Load.  That suggests one
shared helper, e.g. `int arm_mode_is_modelled(uint32_t mode)`, consulted by each caller before it writes the mode
bits, plus the two `default:` arms changed from `exit(1)` to a latched announce as a backstop.

Questions:

1. **Premise audit.**  Which premise in §2 or §3 is wrong?  In particular: can a reserved mode reach CPSR by any
   path OTHER than the three writers shown (MSR, `LDM ^`, data-processing S-to-PC)?  Can it reach an SPSR (via
   `MSR SPSR_c`, `msr_imm_spsr`) and so be restored later by callers 2 and 3?  Enumerate the writers of CPSR and of
   each SPSR from the source if you can read it; say plainly if you cannot.
2. **The disposition.**  For EACH caller, what should happen when the incoming mode is reserved?  For MSR the ARM
   ARM says "Exceptions: None", so the mode write is declined -- but do the OTHER fields in the same MSR (flags, I/F
   bits, the c-byte's T bit) still apply, or is the whole write declined?  For callers 2 and 3 (restoring an SPSR
   the guest itself poisoned), is declining the mode change right, or is FAULT (undefined-instruction) the better
   model?  Cite the architecture text you rely on, or say you are reasoning.
3. **Where the decline lives.**  One helper consulted by every caller, versus guards inside Save/Load that roll CPSR
   back, versus both.  What does each leave reachable?  Apply the sketch rule: a proposed edit must be run against
   each caller's real control flow above, including what happens AFTER Load returns (the `flags` copy, the PC
   write, `quick_pc_to_pointers`).
4. **The backstop.**  If every caller is guarded, are the two `default:` arms dead?  Should they still be latched
   announces (member 3) rather than deleted, and where does the latch state live (per-CPU field vs function-static)?
5. **"What is the SMALLEST EDIT that breaks the fix and still passes?"**  Name the edit and the row of a detector
   you would expect to stay green under it.  (The detector is a 17-row debugger-driven probe on `-E testarm` being
   repaired now; its rows are: `enc ok`, `live`, `pc adv`, `armed`, `no cbit`, `kill 14`, `kill 15`, `save 2s`,
   `acc usr`, `acc fiq/irq/abt/und/sys`, `same svc`, `usr mask`, `row count`.)

**If, while verifying a claim, you found something ELSE — say so.**
