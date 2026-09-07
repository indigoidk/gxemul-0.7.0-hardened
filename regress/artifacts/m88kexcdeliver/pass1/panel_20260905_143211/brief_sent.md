# PASS-1 DESIGN BRIEF -- `m88kexcdeliver` (HIGH): the m88k exception core stops every guest CPU for five trap-like exception classes instead of delivering them.  Tree `GXEMUL-SEC/src/`, HEAD `ab9ae13`.  2026-09-05.

## CONTEXT AND VOCABULARY
An ordinary software-correctness review of an open-source machine emulator (GXemul 0.7.0, a hardened fork): its MC88100
CPU model's exception delivery.  The "guest" is the operating system running inside the emulator (OpenBSD/luna88k on the
project's m88k rig).  Use plain engineering vocabulary: "the emulation stops", "the exception is delivered".

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them -- say so rather than
reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a vector offset, an encoding, a count of
raise sites -- ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

## CITE BY GREP ANCHOR, NOT BY LINE NUMBER
Same-file references positional or by construct name; cross-file references as a VERIFIED-UNIQUE grep anchor, e.g.
`grep -n 'vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented' GXEMUL-SEC/src/cpus/cpu_m88k.c`.

## HAS THIS ROUND ALREADY SHIPPED?  (run 2026-09-05)
    git log -1 -- src/cpus/cpu_m88k.c      -> ed242c0 2026-08-12 Round 121 (#380) -- the file is untouched since #380
    grep -c m88kexcdeliver CHANGELOG.md    -> 1  (the FILING in the retrospective batch-2 block, ab9ae13; no fix round)
    ls regress/ | grep m88k               -> gate_m88k_rounding.sh  m88k_idle_probe.py  m88k_rounding_probe.py  (no exception probe)
The round has NOT run.  The row was filed 2026-09-05 from the Astra + Fable retrospective of #380 (pre-existing upstream
code; `git log -L` on the fallback returns only the 0.7.0 import).

## 1. SETTLED PREMISES, RE-INLINED (each is a QUESTION if you can check it)

Settled by the retrospective batch-2 adjudication (Fable 5.1, `regress/artifacts/retro_20260905/batch2_m88k/fable_adj_batch2.md`)
and by the main loop's own reading and measurement today:

* **The fallback.**  `m88k_exception()` in `cpu_m88k.c` marks only RESET / INTERRUPT / INSTRUCTION_ACCESS / DATA_ACCESS
  `implemented = true`.  Nine other switch cases print a `VERBOSITY_ERROR` debugmsg and `break`, so
  `if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented)` prints `unimplemented vector=0x%03x pc=...`, sets
  `running = false` on EVERY guest CPU, and returns.  `emul.c` then breaks its main loop: **a graceful guest-drivable machine
  halt**, not an abort.  -- warrant: the function is inlined in full below; the probe output below shows it.
* **Reachable classes by raise site** (deriver `grep -o -E 'm88k_exception\(cpu, *M88K_EXCEPTION_[A-Z0-9_]+' src/cpus/cpu_m88k*.c
  | sort | uniq -c`, run 2026-09-05): SFU1_PRECISE 58, PRIVILEGE_VIOLATION 10 (ldcr/stcr/xcr/rte/ld.usr/st.usr/tb0/tb1/tcnd in
  user mode), ILLEGAL_INTEGER_DIVIDE 4 (divu/div by zero, ANY mode), INTEGER_OVERFLOW 3 (add/sub, any mode),
  MISALIGNED_ACCESS 1 (load/store template, any mode), UNIMPLEMENTED_OPCODE 1 (prom_call in user mode).  BOUNDS_CHECK,
  ERROR and SFU1_IMPRECISE have NO raise site today (ERROR is only the internal re-route at `SFRZ already set in PSR`).
* **Scope of THIS round: the five trap-like classes** -- PRIVILEGE_VIOLATION (vector 6, VBR+0x30), ILLEGAL_INTEGER_DIVIDE
  (8, +0x40), INTEGER_OVERFLOW (9, +0x48), MISALIGNED_ACCESS (4, +0x20), UNIMPLEMENTED_OPCODE (5, +0x28).  SFU1 is the
  separate row `m88kexcsfu1` (needs FP exception registers the fork never writes).  Offsets checked against the manual's
  Table 6-1 (`mc88100.txt:8524-8538`) and the section headings inlined below.
* **PSR at reset** is `M88K_PSR_MODE | M88K_PSR_IND` (`cpu_m88k.c`, anchor `cr[M88K_CR_PSR] = M88K_PSR_MODE | M88K_PSR_IND`):
  supervisor, interrupts off, **FPU ENABLED (SFD1 clear)** -- so `divu` by zero reaches ILLEGAL_INTEGER_DIVIDE, not SFU1.
  VBR resets to 0, so vector v lands at address 8*v in the testm88k RAM.
* **rte resumes at SNIP, never at SXIP** -- both in the manual (`mc88100.txt:8983-8985`, verbatim below) and in the fork
  (`X(rte)`: "First try the NIP, if it is Valid").  The common path sets SXIP = pc | V, SNIP = pc+4 | V, SFIP = SNIP+4.
* **The witness EXISTS and is rung 3** (below): the probe was run today against the committed `build/gxemul` (HEAD, rebuilt
  14:17): three fault rows HALT, two controls DONE.

## 2. THE MEASURED WITNESS (rung 3, committed `testm88k`, no machine or device edits) -- `_scratchpad/m88kexc/m88k_exc_probe.py`, output `probe_head.out`

Per row: a one-instruction program at 0x10000 planted with `put w` (a liveness marker `addu r9,r0,r10` first, the test
instruction at 0x10004, then `br .`), registers seeded with `rN=`, `breakpoint add <8*vector>`, `continue`, then `reg`.

    M88KEXC_ROW=div0      RESULT=HALT     pc=0x00010004 r2=0xdeadbeef halted=True stopped=True
        [ exception ILLEGAL_INTEGER_DIVIDE:  ]  [ exception unimplemented: vector=0x008 pc=0x00010004 ]  (repeated)  emul: All machines stopped.
    M88KEXC_ROW=ovf       RESULT=HALT     pc=0x00010004 r2=0xdeadbeef halted=True stopped=True     (vector=0x009)
    M88KEXC_ROW=misalign  RESULT=HALT     pc=0x00010004 r2=0xdeadbeef halted=True stopped=True     (vector=0x004)
    M88KEXC_ROW=live      RESULT=DONE     pc=0x00010008 r2=0x00000006     (divu r2,r3,r4 with r3=0x60, r4=0x10 -> 6: LIVENESS control)
    M88KEXC_ROW=attrib    RESULT=DONE     pc=0x00010008 r2=0x00000001     (the SAME divu as div0 with a non-zero divisor: ATTRIBUTION control)

Encodings (triadic form `0xf4000000 | D<<21 | S1<<16 | sub<<8 | S2`, calibrated on the exemplar's `or r0,r0,r0` = f4005800):
`divu r2,r3,r0` = f4436800 (sub 0x68); `add r2,r3,r4` = f4437004 (sub 0x70; r3=0x7fffffff, r4=1 -> `d != dx` in X(add));
`ld r2,r3,0` = 14430000 (opcode 0x15 form, r3 = 0x20001 -> `addr & 3` in the load/store template); `br .` = c3ffffff.
**CHECK the encodings** -- the sub-op field position was read from the decoder (`switch ((iword >> 8) & 0xff)` under
`case 0x3d`), and a wrong field yields a different instruction that could HALT for a different reason (an unimplemented opcode
also halts today, so a wrong encoding would fake the symptom).  The `live` row's correct quotient is the control against that.
Device-signature control: N/A -- this is the CPU core, not a device; the attribution control replaces it.

## 3. THE ENCLOSING FUNCTION, IN FULL (`cpu_m88k.c`, `void m88k_exception(struct cpu *cpu, int vector, int is_trap)`; blank lines removed, otherwise verbatim as of ab9ae13)

```c
void m88k_exception(struct cpu *cpu, int vector, int is_trap)
{
	bool update_shadow_regs = true;
	bool implemented = false;
	// TODO: Use a const char * instead or something like that, inside the switch...
	switch (vector) {
	case M88K_EXCEPTION_RESET:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "RESET", VERBOSITY_INFO, "");
		implemented = true;
		break;
	case M88K_EXCEPTION_INTERRUPT:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTERRUPT", VERBOSITY_INFO, "");
		implemented = true;
		break;
	case M88K_EXCEPTION_INSTRUCTION_ACCESS:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INSTRUCTION_ACCESS", VERBOSITY_INFO, "");
		implemented = true;
		break;
	case M88K_EXCEPTION_DATA_ACCESS:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "DATA_ACCESS", VERBOSITY_INFO, "");
		implemented = true;
		break;
	case M88K_EXCEPTION_MISALIGNED_ACCESS:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_INTEGER_OVERFLOW:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_ERROR:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_SFU1_PRECISE:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_PRECISE", VERBOSITY_ERROR, "");
		break;
	case M88K_EXCEPTION_SFU1_IMPRECISE:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "");
		break;
	case 0x80:	/*  up to OpenBSD 5.2  */
	case 0x1c2:	/*  from OpenBSD 5.3 and forward...  */
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "syscall", VERBOSITY_INFO,
		    "r13=%i", cpu->cd.m88k.r[13]);
#if 0
		fatal("[ syscall %i(", cpu->cd.m88k.r[13]);
		m88k_cpu_functioncall_trace(cpu, 8);
		fatal(") ]\n");
#endif
		break;
	case MVMEPROM_VECTOR:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MVMEPROM_VECTOR", VERBOSITY_INFO, "");
		break;
	default:
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unknown vector",
		    vector < M88K_EXCEPTION_USER_TRAPS_START ? VERBOSITY_ERROR
		    : VERBOSITY_INFO, "0x%03x", vector);
	}
	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
			vector,
			(int)cpu->pc);
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
	    | M88K_PSR_SFRZ	/*  Freeze shadow registers,          */
	    | M88K_PSR_IND	/*  disable interrupts,               */
	    | M88K_PSR_SFD1	/*  disable the floating point unit,  */
	    | M88K_PSR_MODE,	/*  and switch to supervisor mode.    */
	    M88K_CR_PSR, 0);
	if (update_shadow_regs) {
		cpu->cd.m88k.cr[M88K_CR_SSBR] = 0;
		cpu->cd.m88k.cr[M88K_CR_SXIP] = cpu->pc | M88K_XIP_V;
		/*  SNIP is the address to return to, when executing rte:  */
		if (cpu->delay_slot) {
			if (vector == M88K_EXCEPTION_DATA_ACCESS) {
				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP]+4;
			} else if (vector == M88K_EXCEPTION_INSTRUCTION_ACCESS) {
				/*  If we are in a delay slot, then pc is
				    something like 0xc6000 here (not 0xc5ffc).  */
				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
				cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
			} else {
				/*  Perhaps something like this could work:  */
				cpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;
				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
			}
		} else {
			cpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;
			cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP]+4;
		}
		if (vector == M88K_EXCEPTION_INSTRUCTION_ACCESS)
			cpu->cd.m88k.cr[M88K_CR_SXIP] |= M88K_XIP_E;
	}
	cpu->pc = cpu->cd.m88k.cr[M88K_CR_VBR] + 8 * vector;
	if (cpu->delay_slot)
		cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT;
	else
		cpu->delay_slot = NOT_DELAYED;
	/*  Default to no memory transactions:  */
	cpu->cd.m88k.cr[M88K_CR_DMT0] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMD0] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMA0] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMT1] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMD1] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMA1] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMT2] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMD2] = 0;
	cpu->cd.m88k.cr[M88K_CR_DMA2] = 0;
	/*  Vector-specific handling:  */
	if (vector < M88K_EXCEPTION_USER_TRAPS_START) {
		switch (vector) {
		case M88K_EXCEPTION_RESET:
			fatal("[ m88k_exception: reset ]\n");
			for (int j = 0; j < cpu->machine->ncpus; ++j)
				cpu->machine->cpus[j]->running = false;
			break;
		case M88K_EXCEPTION_INTERRUPT:
			/*  When returning with rte, we want to re-  */
			/*  execute the interrupted instruction:  */
			cpu->cd.m88k.cr[M88K_CR_SNIP] -= 4;
			cpu->cd.m88k.cr[M88K_CR_SFIP] -= 4;
			break;
		case M88K_EXCEPTION_INSTRUCTION_ACCESS:
			/*  When returning with rte, we want to re-  */
			/*  execute the instruction in SXIP, not SNIP/SFIP,  */
			/*  (unless the exception was in a delay-slot):  */
			if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
				cpu->cd.m88k.cr[M88K_CR_SNIP] = 0;
				cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
			}
			break;
		case M88K_EXCEPTION_DATA_ACCESS:
			/*  Update the memory transaction registers:  */
			cpu->cd.m88k.cr[M88K_CR_DMT0] = cpu->cd.m88k.dmt[0];
			cpu->cd.m88k.cr[M88K_CR_DMD0] = cpu->cd.m88k.dmd[0];
			cpu->cd.m88k.cr[M88K_CR_DMA0] = cpu->cd.m88k.dma[0];
			cpu->cd.m88k.cr[M88K_CR_DMT1] = cpu->cd.m88k.dmt[1];
			cpu->cd.m88k.cr[M88K_CR_DMD1] = cpu->cd.m88k.dmd[1];
			cpu->cd.m88k.cr[M88K_CR_DMA1] = cpu->cd.m88k.dma[1];
			cpu->cd.m88k.cr[M88K_CR_DMT2] = 0;
			cpu->cd.m88k.cr[M88K_CR_DMD2] = 0;
			cpu->cd.m88k.cr[M88K_CR_DMA2] = 0;
			m88k_memory_transaction_debug_dump(cpu, 0);
			m88k_memory_transaction_debug_dump(cpu, 1);
			break;
#if 0
		case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
			/*  TODO: Is it correct to continue on the instruction
			    _after_ the division by zero? Or should the PC
			    be backed up one step?  */
			break;
#endif
#if 0
		// TODO: Read up more about SFU1 exceptions and how the
		// control registers look when they happen.
		case M88K_EXCEPTION_SFU1_PRECISE:
			cpu->cd.m88k.cr[M88K_CR_SNIP] = 0; //?
			cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
			//cpu->cd.m88k.cr[M88K_CR_SNIP] -= 4;
			//cpu->cd.m88k.cr[M88K_CR_SFIP] -= 4;
			break;
#endif
		default:debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "m88k",
			    VERBOSITY_ERROR, "internal error");
			cpu->running = false;
		}
	}
	m88k_pc_to_pointers(cpu);
}
```

**THE TAIL HAS A `default:` ARM THAT STOPS THE CPU.**  The retrospective adjudication's sketch -- *"nothing but
`implemented = true` for the five"* -- is a SKETCH in the sense this project's sketch rule names: with `implemented = true`
alone, the five vectors pass the fallback, take the common path, and then land in the vector-specific `default:`, which
prints `internal error` and sets THIS cpu's `running = false`.  On the single-CPU testm88k that is the same halt with a
different message.  The fix therefore has TWO sites in one function: the `implemented` flag AND a tail arm.  Also note the
upstream author's own doubt in the `#if 0` block ("Is it correct to continue on the instruction _after_ the division by
zero?").

## 4. WHAT THE MANUAL SAYS (MC88100 User's Manual, pdftotext `_scratchpad/mc88100.txt`; verbatim, extracted-text lines)

    8983-8985  "The processor hardware does not use the SXIP on return from an exception; an rte instruction resumes
               execution at the instruction pointed to by the SNIP."
    9030-9032  "4. Instruction execution resumes after the instruction corresponding to NIP is prefetched.  The instruction
               pointed to by the SNIP is the first instruction to execute after the return."
    8979       "If an instruction causes a precise exception, the SXIP points to that instruction."
    9231-9240  6.5.2 Misaligned Access (Vector Offset $20): "...precise exception; the exception condition is detected before
               the memory access is dispatched to the data unit. When this exception occurs, the SXIP contains the address of
               the instruction that caused the exception. For a ld or xmem instruction, the appropriate scoreboard bit is set.
               The exception handler can emulate the memory access in software or can discard the instruction..."
    9243-9246  "This exception can be masked by setting the MXM bit (bit 2) in the PSR. If ... masked ... the processor rounds
               the address down to a consistent boundary".
    9248-9255  6.5.3 Unimplemented Opcode ($28): "The SXIP points to the instruction that caused the exception. The exception
               handler can fetch, decode, and process this instruction ... or can discard the instruction".
    9257-9269  6.5.4 Privilege Violation ($30): three conditions (control register access other than FPCR/FPSR in user mode;
               .usr in user mode; trap vectors 0-127 in user mode).  "the instruction that caused the exception is pointed to
               by the SXIP. The privileged operation is not performed."
    10300-10305 6.8.3 Integer-Divide Error: "occurs when the divisor of a div or divu instruction is zero or when either
               operand is negative in a div instruction. The SXIP points to the instruction that caused the exception. The
               destination register is not changed, but the scoreboard bit is set for the destination register."
    10308-10314 "...fcr2 and fcr4 contain the source operands, and fcr5 contains the destination register number."
    (6.6 Integer Overflow, offset $48: not re-extracted here -- a file-reading seat should grep it; PACKET-FED seats: treat
     "SXIP = the add/sub instruction, SNIP = next" as a premise to CONDITION on, not to assume.)

So for all five, the ARCHITECTURAL contract is: SXIP = the faulting instruction (V set), the operation is not performed
(destination unchanged), rte resumes at SNIP = the next instruction.  That is exactly what the common path already produces
when it is reached (SNIP = pc + 4 | V).  The fork does not model the scoreboard (SSBR is written 0), nor fcr2/fcr4/fcr5.

## 5. THE DESIGN UNDER REVIEW (option set -- name any member this brief did not)

**D1 (proposed): DELIVER the five through the existing common path.**  In the FIRST switch, set `implemented = true` in the
five cases (MISALIGNED_ACCESS, UNIMPLEMENTED_OPCODE, PRIVILEGE_VIOLATION, ILLEGAL_INTEGER_DIVIDE, INTEGER_OVERFLOW); in the
TAIL switch add the five as `case` labels with a bare `break` (no SNIP/SFIP adjustment: the manual's rte-at-SNIP semantics
are the common path's defaults), replacing the `#if 0` ILLEGAL_INTEGER_DIVIDE block.  Delete nothing else: the fallback
stays for the genuinely unimplemented vectors (BOUNDS_CHECK, ERROR, SFU1 x2) and for unknown vectors below 128.
Keep the `unimplemented` fallback's text.  Questions for the panel, each with a measurable consequence:
  Q-D1a  Message level: the four implemented classes print at VERBOSITY_INFO; the five print at VERBOSITY_ERROR today.  A
         delivered exception that a guest OS handles routinely (a user program's divide by zero -> SIGFPE) should not be an
         ERROR-level line.  Proposal: change the five to VERBOSITY_INFO.  Consequence: the boot-log hygiene gate (gate 6)
         and `#261`'s opt-in break-on-ERROR treat ERROR lines specially; an INFO line is invisible at default verbosity.
         Is there a hygiene row that would red either way?
  Q-D1b  BOUNDS_CHECK_VIOLATION (vector 7, offset $38) has no raise site (tbnd is disassembler-only) -- include it in the five
         for consistency (zero cost, no row can observe it) or leave it unimplemented (an honest "not modelled")?
  Q-D1c  ERROR (vector 10, $50): the common path RE-ROUTES a non-trap exception taken with SFRZ already set to ERROR; ERROR is
         unimplemented, so today a double fault halts the machine.  Real hardware enters the error handler.  In scope?
         (OpenBSD's error-exception handler panics; the halt and the panic are both "guest dead" -- but the guest's panic
         message is the guest's, and the emulator's halt is ours.)  The main loop proposes OUT OF SCOPE for this round: file.
  Q-D1d  MISALIGNED: the manual says the ld/xmem scoreboard bit is set; the fork has no scoreboard.  Anything a guest handler
         (OpenBSD `m88100_trap` T_MISALGNFLT) would read that the fork leaves wrong?  DMT0 is zeroed by the common path for
         every vector but DATA_ACCESS -- correct for a PRECISE exception detected before dispatch (manual 9236-9237)?
  Q-D1e  ILLEGAL_INTEGER_DIVIDE: fcr2/fcr4/fcr5 (manual 10308-10314) are not written.  OpenBSD's SIGFPE path does not read
         them (belief -- packet-fed seats condition on it; file-reading seats may check `sys/arch/m88k` knowledge but it is
         NOT on disk).  In scope as a follow-up row, not this round?

**D2 (rejected, name why if you disagree): the naive `implemented = true` only.**  Reaches the tail `default:` -> `running =
false` for this CPU.  Measurable: the probe's fault rows print `internal error` and `All machines stopped`, pc == 8*vector.
This is ALSO the (d)-shaped mutant for the kill table (the guard changed, the repair nulled by the tail).

**D3: decline/latched-announce forms** are NOT members here: these are architected CPU exceptions with guest handlers;
suppressing them lies to the guest.  (The device option set does not apply to a CPU exception core -- say so if you
disagree.)

## 6. THE DETECTOR (ships with the fix): `regress/m88k_exc_probe.py`, wired into gate 11 (`gate_m88k_rounding.sh`) as a new section

Rows (each asserts RESULT and, for delivered rows, `pc == 8*vector`, `SXIP == 0x10004 | V`, PSR has SFRZ|IND|SFD1|MODE,
`r2` unchanged (destination not written), and the machine still RUNNING -- no `All machines stopped`):
    div0 DELIVER @0x40 | ovf DELIVER @0x48 | misalign DELIVER @0x20 | live DONE r2=6 | attrib DONE r2=1
    + PRIVILEGE (vector 6, @0x30) and UNIMPLEMENTED_OPCODE (vector 5, @0x28) rows, which need USER MODE: proposed route --
      a supervisor `stcr rS,cr1` that clears PSR.MODE (the fork's `m88k_stcr` handles the mode switch), then `ldcr r2,cr1`
      (privileged in user mode -> vector 6) or a user-mode `tb1 0,r0,0x10` (trap vector < 128 -> vector 6 per #380's
      restriction and manual 9264); UNIMPLEMENTED_OPCODE via `prom_call` in user mode (the fork's only raise site).
      QUESTION: give the exact encodings for `stcr`/`ldcr` from the decoder (`case 0x20` group) -- the packet does not
      carry them; and say whether clearing MODE by `stcr` while the next instruction is already translated behaves as on
      hardware in this fork (translation caches are mode-tagged?).
Kill table (scratch clone, frozen probe): M_REVERT5 (drop `implemented = true` at each class in turn, floor (b)); M_NAIVE (D2:
tail default left in place -- the (d) mutant: guard changed, repair nulled); M_VEC4 (`+ 4 * vector`: breakpoint not hit,
pc mismatch); M_NOSHADOW (`update_shadow_regs = false` for the five: SXIP stale); M_SNIPX (SNIP = pc, re-execute: the div0
row loops -- observable as the breakpoint hit with SNIP == SXIP); M_MODE (skip the PSR supervisor switch: PSR row reds);
M_LEVEL (VERBOSITY_INFO -> ERROR: NOT observable by these rows -- DISCLOSED under clause (e) unless a hygiene row exists).
Contract line: "catches: a class returned to the fallback; a class reaching the tail default; a wrong vector base; a stale
SXIP; a wrong return address; a wrong PSR.  Does not catch: message level; fcr2/fcr4/fcr5; scoreboard bits; the
delay-slot arms (no row executes a faulting instruction in a delay slot -- QUESTION: should one?)".

## 7. QUESTIONS (answer all; VERDICT LINE FIRST)

1. **THE PREMISE AUDIT.**  Is the reading of the two switches right -- does D1 deliver, and does D2 halt?  Is "rte resumes
   at SNIP" the right contract for ALL five (the `#if 0` doubt about the divide: should the PC be backed up)?  Are the
   encodings right?  Is the raise-site census right?  Is SFD1 really clear at reset on testm88k (else div0 is an SFU1 row)?
2. **THE SMALLEST EDIT that breaks D1 and still passes the detector.**  Name the row you expect to stay green.  The main loop
   expects M_LEVEL to escape (disclosed) -- what else?
3. **OPTION-SET COMPLETENESS.**  Q-D1a..e above.  Is there a member this brief did not name?  Grep the fork for the idiom:
   how do the OTHER CPU cores in this tree (MIPS `mips_cpu_exception`, SH `sh_exception`, ARM, PPC) treat an exception class
   they recognise but do not fully model -- deliver, or stop?  The precedent decides Q-D1b/c.
4. **THE GUEST.**  OpenBSD/luna88k boots on this project's rig today WITHOUT this fix -- so no boot path raises any of the
   five.  What in a booted system would (a userland divide by zero; `ldcr` from userland; a misaligned access with MXM
   clear)?  Is there a boot-gate row (gate_ab) whose behaviour could CHANGE once these deliver (e.g. a kernel that
   deliberately probes with a privileged instruction and expects a trap)?  Say what a measuring seat should run.
5. **RECORDS.**  The fix removes upstream's "unimplemented" halt for five classes: what does the CHANGELOG block owe (the
   `#if 0` doubt resolved by manual citation; the retrospective provenance; the split from `m88kexcsfu1`)?

If, while verifying a claim, you found something ELSE -- say so.  agy is DELIBERATELY NOT FIRED (reserved for measurement).


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
