# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ofemulnodata` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input defects.  You cannot read files; work from the text.  FIX ONLY, as exact edits -- no tests, probes
or reproduction steps.

## The issue

**title:** src/promemul/of.c of_emul(): the OpenFirmware emulation entry calls fatal() + exit(1) when machine->md.of_data is NULL, which is true on every machine except macppc with PROM emulation on (machine_macppc.c returns before of_emul_init when it is off) -- and the ARM and PowerPC decoders route their OpenFirmware magic instruction to it with no machine or privilege check

**state_note (head):** filed 2026-10-16 from the adjudication of the agy pack's second readings (packet D, H1): all three seats FILE, HIGH, own row (regress/artifacts/adj_20261016/astra/D_secondreadings/codex_adjD.txt, grok/D_secondreadings/grok_adjD.txt, fable5/fable5_adj_D_secondreadings_v2_FABLE.md).  Source: prescreen_audits5.md of_two/F9.  READ at HEAD by all three: of.c:1096-1101 (the NULL check and the exit), :1078 (the only writer, of_emul_init, called only from machine_macppc.c:99); ARM decode cpu_arm_instr.c:5034-5036 -> X(openfirmware) :988-991; PowerPC decode cpu_ppc_instr.c:4400-4402 -> X(openfirmware) :3956-3958.  A guest instruction therefore ends the emulator process on machines that never set up OpenFirmware.  Not covered by ofopenexit or ofpeerexit (other sites in the same file); Fable 5.1: may share one round with them.  A rung-3 ATTEMPT exists, made by claude-opus-4-8 in the Fable seat's fallback run (so it is not a Fable ruling and owes review before it counts as the witness): regress/artifacts/adj_20261016/fable5/meas_D/witness_hostexit.py and .out, at HEAD e483d931 on the unmodified ARM test machine (the emulator prints `of_emul(): no of_data struct?' and the process exits 1), each with a benign-instruction liveness control that stays alive. ||  [2026-10-21] ARGON SCOPING (packet-fed, a reading not a measurement; regress/artifacts/ofemulnodata/argon_scope_20261021/gemini_web.out, dispositions DISPOSITIONS.md): THREE rounds, not one -- of.c:1100 (this row), :394 (ofpeerexit) and :448 (ofopenexit) differ in semantic class, fix design and detector (the round-scope rule); of.c:549, :577, :1120 and :1201 are UNREACHABLE (machine-setup helpers; arch-switch defaults only ARM and PowerPC reach).  DESIGN for this row: gate the magic word at the DECODERS (cpu_arm_instr.c's SWI case, cpu_ppc_instr.c's sc case) on `cpu->machine->md.of_data != NULL`, so a machine without OpenFirmware executes the word as the architectural SWI / system call it encodes (FAULT) -- NOT an early return inside of_emul, whose callers' tails then jump to the link register as if the call had returned.  Detector: the SWI-exception row on an ARM machine, the sc-exception rows on a non-macppc PowerPC machine and on macppc without PROM emulation, and macppc-with-PROM-emulation accept rows (an OF service still answers).  The title was corrected the same day: macppc without PROM emulation also has of_data NULL (read at machine_macppc.c's `if (!machine->prom_emulation) return;` before of_emul_init).

## Your earlier draft, and why it was incomplete

It edited only the ARM caller.  A review found the PowerPC caller missed; your revision agreed but could not see that file.
Both decoders reach the defect through ONE function, so this packet shows that function and both call sites:

### `src/promemul/of.c` lines 1080-1125 (HEAD 8d9df658)

```c
 1080| 	return ofd;
 1081| }
 1082| 
 1083| 
 1084| /*
 1085|  *  of_emul():
 1086|  *
 1087|  *  OpenFirmware call emulation.
 1088|  */
 1089| int of_emul(struct cpu *cpu)
 1090| {
 1091| 	int i, nargs, nret, ofs, retval = 0;
 1092| 	char service[50];
 1093| 	char *arg[OF_N_MAX_ARGS];
 1094| 	uint64_t base, ptr;
 1095| 	struct of_service *os;
 1096| 	struct of_data *of_data = cpu->machine->md.of_data;
 1097| 
 1098| 	if (of_data == NULL) {
 1099| 		fatal("of_emul(): no of_data struct?\n");
 1100| 		exit(1);
 1101| 	}
 1102| 
 1103| 	/*
 1104| 	 *  The first argument register points to "prom_args":
 1105| 	 *
 1106| 	 *	char *service;		(probably 32 bit)
 1107| 	 *	int nargs;
 1108| 	 *	int nret;
 1109| 	 *	char *args[10];
 1110| 	 */
 1111| 
 1112| 	switch (cpu->cpu_family->arch) {
 1113| 	case ARCH_ARM:
 1114| 		base = cpu->cd.arm.r[0];
 1115| 		break;
 1116| 	case ARCH_PPC:
 1117| 		base = cpu->cd.ppc.gpr[3];
 1118| 		break;
 1119| 	default:fatal("of_emul(): unimplemented arch (TODO)\n");
 1120| 		exit(1);
 1121| 	}
 1122| 
 1123| 	/*  TODO: how about 64-bit OpenFirmware?  */
 1124| 	ptr   = load_32bit_word(cpu, base);
 1125| 	nargs = load_32bit_word(cpu, base + 4);
```

### `src/cpus/cpu_arm_instr.c` lines 975-1000 (HEAD 8d9df658)

```c
  975| X(cdp) {
  976| 	uint32_t low_pc = ((size_t)ic - (size_t)
  977| 	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
  978| 	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
  979| 	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
  980| 	arm_cdp(cpu, ic->arg[0]);
  981| }
  982| Y(cdp)
  983| 
  984| 
  985| /*
  986|  *  openfirmware:
  987|  */
  988| X(openfirmware)
  989| {
  990| 	/*  TODO: sync pc?  */
  991| 	of_emul(cpu);
  992| 	cpu->pc = cpu->cd.arm.r[ARM_LR];
  993| 	if (cpu->machine->show_trace_tree)
  994| 		cpu_functioncall_trace_return(cpu);
  995| 	quick_pc_to_pointers_arm(cpu);
  996| }
  997| 
  998| 
  999| /*
 1000|  *  reboot:
```

### `src/cpus/cpu_ppc_instr.c` lines 3955-3980 (HEAD 8d9df658)

```c
 3955| {
 3956| 	/*  Synchronize the PC (pointing to _after_ this instruction)  */
 3957| 	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[1];
 3958| 
 3959| 	ppc_exception(cpu, PPC_EXCEPTION_SC);
 3960| 
 3961| 	/*  This caused an update to the PC register, so there is no need
 3962| 	    to worry about the next instruction being an end_of_page.  */
 3963| }
 3964| 
 3965| 
 3966| /*
 3967|  *  openfirmware:
 3968|  */
 3969| X(openfirmware)
 3970| {
 3971| 	of_emul(cpu);
 3972| 
 3973| 	cpu->pc = cpu->cd.ppc.spr[SPR_LR];
 3974| 	if (cpu->machine->show_trace_tree)
 3975| 		cpu_functioncall_trace_return(cpu);
 3976| 
 3977| 	quick_pc_to_pointers(cpu);
 3978| 
 3979| 	if (!cpu->running) {
 3980| 		cpu->n_translated_instrs --;
```

Your earlier edits:

```json
(none)
```

## WHAT TO RETURN

1. `STILL PRESENT: YES|NO|UNSETTLED -- <the line>`.
2. If YES: EXACTLY ONE ```json edit list, the COMPLETE fix (not a delta): [{"file", "old", "new", "why"}], each `old` occurring
   EXACTLY ONCE in its file.  PREFER the single site both callers share (`of_emul()`'s missing-`of_data` arm) over editing each
   caller -- one guard then covers both decoders.  Say what `of_emul()`'s return value means to each caller as the code shows
   it, and keep each caller's behaviour after the call correct.  The house idiom for a guest-reachable diagnostic is ONE
   announcement per machine (a latch) with `(once)` in the text -- never an unbounded `fatal()` -- and never `exit()`.
   Tabs stay tabs; lines within 79 columns; tag a new comment `/* #NNN: ... */`.
3. What the fix deliberately does not change.

End with one line: `FIXDRAFT_OFEMULNODATA: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
