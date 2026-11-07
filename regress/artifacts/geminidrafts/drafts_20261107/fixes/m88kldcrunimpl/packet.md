# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kldcrunimpl` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kldcrunimpl`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_m88k.c:503-507 -- m88k_ldcr's default arm stops the emulated CPU on an ldcr of any control register its switch does not list (cr21-cr63; the switch lists cr0-cr20) -- CPU-STOP (supervisor only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Unimplemented register access crashes the emulator via run-loop termination, violating robustness goals.

## The code at the cited lines

### `src/cpus/cpu_m88k.c` around the row's cited line 503 (HEAD 2d25df65, lines 458-548)

```c
  458| 	case M88K_CR_DMT1:
  459| 	case M88K_CR_DMT2:
  460| 		/*
  461| 		 *  Catch some possible internal errors in the emulator:
  462| 		 *
  463| 		 *  For valid memory Load transactions, the Destination Register
  464| 		 *  should not be zero.
  465| 		 *
  466| 		 *  The Byte Order bit should be the same as the CPU's.
  467| 		 */
  468| 		if (retval & DMT_VALID && !(retval & DMT_WRITE)) {
  469| 			if (DMT_DREGBITS(retval) == M88K_ZERO_REG) {
  470| 				debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  471| 				    "ldcr: DMT DREG = zero? Internal error.");
  472| 				cpu->running = false;
  473| 				return;
  474| 			}
  475| 		}
  476| 		if (!!(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_BO)
  477| 		    != !!(retval & DMT_BO) && retval & DMT_VALID) {
  478| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  479| 			    "ldcr: DMT byte order not same as CPUs?");
  480| 			cpu->running = false;
  481| 			return;
  482| 		}
  483| 
  484| 		break;
  485| 
  486| 	case M88K_CR_DMA0:
  487| 	case M88K_CR_DMA1:
  488| 	case M88K_CR_DMA2:
  489| 		/*
  490| 		 *  Catch some possible internal errors in the emulator:
  491| 		 *  The lowest 2 bits of the transaction address registers
  492| 		 *  should always be zero.
  493| 		 */
  494| 		if (retval & 3) {
  495| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  496| 			    "ldcr: DMAx not word-aligned? Internal error.");
  497| 			cpu->running = false;
  498| 			return;
  499| 		}
  500| 
  501| 		break;
  502| 
  503| 	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  504| 		    "ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\n",
  505| 		    cr, m88k_cr_name(cpu, cr));
  506| 		cpu->running = false;
  507| 		return;
  508| 	}
  509| 
  510| 	*r32ptr = retval;
  511| }
  512| 
  513| 
  514| /*
  515|  *  m88k_stcr():
  516|  *
  517|  *  Write to a control register.
  518|  *  (Used by both the stcr and rte instructions.)
  519|  */
  520| void m88k_stcr(struct cpu *cpu, uint32_t value, int cr, int rte)
  521| {
  522| 	uint32_t old = cpu->cd.m88k.cr[cr];
  523| 
  524| 	switch (cr) {
  525| 
  526| 	case M88K_CR_PSR:	/*  Processor Status Register  */
  527| 		if ((cpu->byte_order == EMUL_LITTLE_ENDIAN
  528| 		    && !(value & M88K_PSR_BO)) ||
  529| 		    (cpu->byte_order == EMUL_BIG_ENDIAN
  530| 		    && (value & M88K_PSR_BO))) {
  531| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  532| 			    "stcr: TODO: attempt to change endianness by flipping"
  533| 			    " the endianness bit in the PSR. How should this"
  534| 			    " be handled? Aborting.");
  535| 			cpu->running = false;
  536| 			return;
  537| 		}
  538| 
  539| 		if (!rte && old & M88K_PSR_MODE && !(value & M88K_PSR_MODE))
  540| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  541| 			    "stcr: WARNING! the PSR_MODE bit is being"
  542| 			    " cleared; this should be done using the RTE "
  543| 			    "instruction only, according to the M88100 "
  544| 			    "manual! Continuing anyway.");
  545| 
  546| 		if (value & M88K_PSR_MXM) {
  547| 			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  548| 			    "stcr: TODO: MXM support");
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_M88KLDCRUNIMPL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
