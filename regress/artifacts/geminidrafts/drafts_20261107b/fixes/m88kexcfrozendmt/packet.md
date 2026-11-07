# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kexcfrozendmt` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kexcfrozendmt`, state `open`, severity `low`)

**title:** m88kexcfrozendmt  cpu_m88k.c m88k_exception(): the common path zeroes DMT0-2/DMD0-2/DMA0-2 (`Default to no memory transactions') OUTSIDE the update_shadow_regs guard, so a TRAP taken while shadowing is frozen clears the exception-time registers the manual says it leaves untouched

**state_note (head):**

Pre-existing, by reading (codex and kimi independently, #502 pass 2).  UM 6.5.5 (mc88100.txt:9290-9294): traps executed while shadowing is frozen do not cause the error exception and 'none of the exception-time or shadow registers are modified'.  The fork: the SFRZ branch leaves the shadows and EPSR alone (update_shadow_regs = false) but the DMT/DMD/DMA zeroing sits after the guard and runs for every exception.  #502's `trapfrozen' row observes pc and the shadows, not DMT -- disclosed in its contract.  Guest-visible only to a handler that inspects the DMT registers of the FIRST fault after issuing a trap while still frozen (a data-access handler that makes a syscall/trap before re-enabling shadowing) -- LOW.  Fix shape: move the zeroing under the guard (or skip it when is_trap && SFRZ); row: trapfrozen extended to read DMT0 after a first fault that set it (a data-access fault) followed by a trap.  Provenance: #502 pass 2 (codex, kimi) + adjudication pass.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- The bug is well-understood and a specific fix shape and row extension are provided.

## The code at the cited lines

### `src/cpus/cpu_m88k.c` around line 689 -- LOCATED BY THE COORDINATOR from the name `m88k_exception` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 569-809)

```c
  569| 
  570| 	case M88K_CR_SSBR:	/*  Shadow ScoreBoard Register  */
  571| 		if (value & 1)
  572| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  573| 			    "stcr: WARNING! bit 0 non-zero when"
  574| 			    " writing to SSBR (?)");
  575| 
  576| 		cpu->cd.m88k.cr[cr] = value;
  577| 		break;
  578| 
  579| 	case M88K_CR_VBR:
  580| 		if (value & 0x00000fff)
  581| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  582| 			    "stcr: WARNING! bits 0..11 non-zero when"
  583| 			    " writing to VBR (?)");
  584| 
  585| 		cpu->cd.m88k.cr[cr] = value;
  586| 		break;
  587| 
  588| 	case M88K_CR_DMT0:
  589| 	case M88K_CR_DMT1:
  590| 	case M88K_CR_DMT2:
  591| 		cpu->cd.m88k.cr[cr] = value;
  592| 		break;
  593| 
  594| 	case M88K_CR_SR0:	/*  Supervisor Storage Registers 0..3  */
  595| 	case M88K_CR_SR1:
  596| 	case M88K_CR_SR2:
  597| 	case M88K_CR_SR3:
  598| 		cpu->cd.m88k.cr[cr] = value;
  599| 		break;
  600| 
  601| 	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  602| 		    "stcr: UNIMPLEMENTED cr = 0x%02x (%s)",
  603| 		    cr, m88k_cr_name(cpu, cr));
  604| 		cpu->running = false;
  605| 		return;
  606| 	}
  607| }
  608| 
  609| 
  610| /*
  611|  *  m88k_fstcr():
  612|  *
  613|  *  Write to a floating-point control register.
  614|  */
  615| void m88k_fstcr(struct cpu *cpu, uint32_t value, int fcr)
  616| {
  617| 	switch (fcr) {
  618| 
  619| 	case 63:
  620| 		/*  #298: the FPCR's RM field (bits 15:14) is now decoded by
  621| 		    the single-precision result stores, so a guest calling
  622| 		    fpsetround() -- which writes exactly this field -- is
  623| 		    doing something IMPLEMENTED, and warning "UNIMPLEMENTED"
  624| 		    for it would be dishonest (a panel seat's finding, same
  625| 		    class as #270). Warn only for bits outside RM, which
  626| 		    really are ignored.  */
  627| 		if ((value & ~(uint32_t)M88K_FPCR_RM_MASK) == 0)
  628| 			break;
  629| 
  630| 		// fall through
  631| 
  632| 	case 0:
  633| 	case 62:
  634| 		// Don't warn for writes with the value zero for these, for now.
  635| 		if (value == 0)
  636| 			break;
  637| 
  638| 		// fall through
  639| 
  640| 	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  641| 		    "WARNING: fstcr: write 0x%08x to UNIMPLEMENTED fcr = 0x%02x (%s)",
  642| 		    value, fcr, m88k_fcr_name(cpu, fcr));
  643| 	}
  644| 
  645| 	cpu->cd.m88k.fcr[fcr] = value;
  646| }
  647| 
  648| 
  649| /*
  650|  *  m88k_memory_transaction_debug_dump():
  651|  *
  652|  *  Debug dump of the memory transaction registers of a cpu.
  653|  */
  654| static void m88k_memory_transaction_debug_dump(struct cpu *cpu, int n)
  655| {
  656| 	uint32_t dmt = cpu->cd.m88k.dmt[n];
  657| 
  658| 	debug("[ DMT%i: ", n);
  659| 	if (dmt & DMT_VALID) {
  660| 		if (dmt & DMT_BO)
  661| 			debug("Little-Endian, ");
  662| 		else
  663| 			debug("Big-Endian, ");
  664| 		if (dmt & DMT_DAS)
  665| 			debug("Supervisor, ");
  666| 		else
  667| 			debug("User, ");
  668| 		if (dmt & DMT_DOUB1)
  669| 			debug("DOUB1, ");
  670| 		if (dmt & DMT_LOCKBAR)
  671| 			debug("LOCKBAR, ");
  672| 		if (dmt & DMT_WRITE)
  673| 			debug("store, ");
  674| 		else {
  675| 			debug("load.%c(r%i), ",
  676| 			    dmt & DMT_SIGNED? 's' : 'u',
  677| 			    DMT_DREGBITS(dmt));
  678| 		}
  679| 		debug("bytebits=0x%x ]\n", DMT_ENBITS(dmt));
  680| 
  681| 		debug("[ DMD%i: 0x%08" PRIx32"; ", n, cpu->cd.m88k.dmd[n]);
  682| 		debug("DMA%i: 0x%08" PRIx32" ]\n", n, cpu->cd.m88k.dma[n]);
  683| 	} else
  684| 		debug("not valid ]\n");
  685| }
  686| 
  687| 
  688| /*
  689|  *  m88k_exception():
  690|  *
  691|  *  Cause an exception.
  692|  */
  693| void m88k_exception(struct cpu *cpu, int vector, int is_trap)
  694| {
  695| 	bool update_shadow_regs = true;
  696| 	bool implemented = false;
  697| 
  698| 	// TODO: Use a const char * instead or something like that, inside the switch...
  699| 
  700| 	switch (vector) {
  701| 
  702| 	case M88K_EXCEPTION_RESET:
  703| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "RESET", VERBOSITY_INFO, "%s", "");
  704| 		implemented = true;
  705| 		break;
  706| 
  707| 	case M88K_EXCEPTION_INTERRUPT:
  708| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTERRUPT", VERBOSITY_INFO, "%s", "");
  709| 		implemented = true;
  710| 		break;
  711| 
  712| 	case M88K_EXCEPTION_INSTRUCTION_ACCESS:
  713| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INSTRUCTION_ACCESS", VERBOSITY_INFO, "%s", "");
  714| 		implemented = true;
  715| 		break;
  716| 
  717| 	case M88K_EXCEPTION_DATA_ACCESS:
  718| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "DATA_ACCESS", VERBOSITY_INFO, "%s", "");
  719| 		implemented = true;
  720| 		break;
  721| 
  722| 	case M88K_EXCEPTION_MISALIGNED_ACCESS:
  723| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_INFO, "%s", "");
  724| 		implemented = true;	/*  m88kexcdeliver  */
  725| 		break;
  726| 
  727| 	case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
  728| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_INFO, "%s", "");
  729| 		implemented = true;	/*  m88kexcdeliver  */
  730| 		break;
  731| 
  732| 	case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
  733| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_INFO, "%s", "");
  734| 		implemented = true;	/*  m88kexcdeliver  */
  735| 		break;
  736| 
  737| 	case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
  738| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "%s", "");
  739| 		implemented = true;	/*  m88kexcdeliver  */
  740| 		break;
  741| 
  742| 	case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
  743| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_INFO, "%s", "");
  744| 		implemented = true;	/*  m88kexcdeliver  */
  745| 		break;
  746| 
  747| 	case M88K_EXCEPTION_INTEGER_OVERFLOW:
  748| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_INFO, "%s", "");
  749| 		implemented = true;	/*  m88kexcdeliver  */
  750| 		break;
  751| 
  752| 	case M88K_EXCEPTION_ERROR:
  753| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_INFO, "%s", "");
  754| 		implemented = true;	/*  m88kexcdeliver  */
  755| 		break;
  756| 
  757| 	case M88K_EXCEPTION_SFU1_PRECISE:
  758| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_PRECISE", VERBOSITY_ERROR, "%s", "");
  759| 		break;
  760| 
  761| 	case M88K_EXCEPTION_SFU1_IMPRECISE:
  762| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "%s", "");
  763| 		break;
  764| 
  765| 	case 0x80:	/*  up to OpenBSD 5.2  */
  766| 	case 0x1c2:	/*  from OpenBSD 5.3 and forward...  */
  767| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "syscall", VERBOSITY_INFO,
  768| 		    "r13=%i", cpu->cd.m88k.r[13]);
  769| #if 0
  770| 		fatal("[ syscall %i(", cpu->cd.m88k.r[13]);
  771| 		m88k_cpu_functioncall_trace(cpu, 8);
  772| 		fatal(") ]\n");
  773| #endif
  774| 		break;
  775| 
  776| 	case MVMEPROM_VECTOR:
  777| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MVMEPROM_VECTOR", VERBOSITY_INFO, "%s", "");
  778| 		break;
  779| 
  780| 	default:
  781| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unknown vector",
  782| 		    vector < M88K_EXCEPTION_USER_TRAPS_START ? VERBOSITY_ERROR
  783| 		    : VERBOSITY_INFO, "0x%03x", vector);
  784| 	}
  785| 
  786| 	/*
  787| 	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
  788| 	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
  789| 	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
  790| 	 *  6.8.3), like the four this fallback never covered.  Before, any of them
  791| 	 *  stopped EVERY guest CPU here: one divu by zero, in either mode, ended
  792| 	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
  793| 	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
  794| 	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
  795| 	 *  here, by design: SFU1_PRECISE/IMPRECISE (114/115; row m88kexcsfu1 --
  796| 	 *  faithful delivery needs the rest of the SFU1 exception state, which
  797| 	 *  the fork does not write) and vectors 11..113/116..127 (117 vectors
  798| 	 *  with the two SFU1 ones), which no literal-constant raise site names
  799| 	 *  but a supervisor tb0/tb1/tcnd can name directly (row
  800| 	 *  m88kexctaildefault; the probe's resid50/sfu1h rows pin that they
  801| 	 *  STILL halt).
  802| 	 */
  803| 	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
  804| 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
  805| 		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
  806| 			vector,
  807| 			(int)cpu->pc);
  808| 		for (int j = 0; j < cpu->machine->ncpus; ++j)
  809| 			cpu->machine->cpus[j]->running = false;
```


RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_M88KEXCFROZENDMT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
