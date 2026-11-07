# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `m88kexcsfu1` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `m88kexcsfu1`, state `open`)

**title:** m88kexcsfu1  the m88k exception core stops every guest CPU on SFU1_PRECISE (vector 114, 58 raise sites: any FP/mul/div with SFD1 set, or an FP divide by zero) and the latent SFU1_IMPRECISE, instead of delivering VBR+0x390/0x398

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_m88k.c` -- AT HEAD, lines 693-985 (`*` marks a line your previous draft changed)

```c
  693|  void m88k_exception(struct cpu *cpu, int vector, int is_trap)
  694|  {
  695|  	bool update_shadow_regs = true;
  696|  	bool implemented = false;
  697|  
  698|  	// TODO: Use a const char * instead or something like that, inside the switch...
  699|  
  700|  	switch (vector) {
  701|  
  702|  	case M88K_EXCEPTION_RESET:
  703|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "RESET", VERBOSITY_INFO, "%s", "");
  704|  		implemented = true;
  705|  		break;
  706|  
  707|  	case M88K_EXCEPTION_INTERRUPT:
  708|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTERRUPT", VERBOSITY_INFO, "%s", "");
  709|  		implemented = true;
  710|  		break;
  711|  
  712|  	case M88K_EXCEPTION_INSTRUCTION_ACCESS:
  713|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INSTRUCTION_ACCESS", VERBOSITY_INFO, "%s", "");
  714|  		implemented = true;
  715|  		break;
  716|  
  717|  	case M88K_EXCEPTION_DATA_ACCESS:
  718|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "DATA_ACCESS", VERBOSITY_INFO, "%s", "");
  719|  		implemented = true;
  720|  		break;
  721|  
  722|  	case M88K_EXCEPTION_MISALIGNED_ACCESS:
  723|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MISALIGNED_ACCESS", VERBOSITY_INFO, "%s", "");
  724|  		implemented = true;	/*  m88kexcdeliver  */
  725|  		break;
  726|  
  727|  	case M88K_EXCEPTION_UNIMPLEMENTED_OPCODE:
  728|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "UNIMPLEMENTED_OPCODE", VERBOSITY_INFO, "%s", "");
  729|  		implemented = true;	/*  m88kexcdeliver  */
  730|  		break;
  731|  
  732|  	case M88K_EXCEPTION_PRIVILEGE_VIOLATION:
  733|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "PRIVILEGE_VIOLATION", VERBOSITY_INFO, "%s", "");
  734|  		implemented = true;	/*  m88kexcdeliver  */
  735|  		break;
  736|  
  737|  	case M88K_EXCEPTION_BOUNDS_CHECK_VIOLATION:
  738|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "BOUNDS_CHECK_VIOLATION", VERBOSITY_INFO, "%s", "");
  739|  		implemented = true;	/*  m88kexcdeliver  */
  740|  		break;
  741|  
  742|  	case M88K_EXCEPTION_ILLEGAL_INTEGER_DIVIDE:
  743|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ILLEGAL_INTEGER_DIVIDE", VERBOSITY_INFO, "%s", "");
  744|  		implemented = true;	/*  m88kexcdeliver  */
  745|  		break;
  746|  
  747|  	case M88K_EXCEPTION_INTEGER_OVERFLOW:
  748|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "INTEGER_OVERFLOW", VERBOSITY_INFO, "%s", "");
  749|  		implemented = true;	/*  m88kexcdeliver  */
  750|  		break;
  751|  
  752|  	case M88K_EXCEPTION_ERROR:
  753|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "ERROR", VERBOSITY_INFO, "%s", "");
  754|  		implemented = true;	/*  m88kexcdeliver  */
  755|  		break;
  756|  
  757|  	case M88K_EXCEPTION_SFU1_PRECISE:
  758|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_PRECISE", VERBOSITY_ERROR, "%s", "");
  759|* 		break;
  760|  
  761|  	case M88K_EXCEPTION_SFU1_IMPRECISE:
  762|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "%s", "");
  763|* 		break;
  764|  
  765|  	case 0x80:	/*  up to OpenBSD 5.2  */
  766|  	case 0x1c2:	/*  from OpenBSD 5.3 and forward...  */
  767|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "syscall", VERBOSITY_INFO,
  768|  		    "r13=%i", cpu->cd.m88k.r[13]);
  769|  #if 0
  770|  		fatal("[ syscall %i(", cpu->cd.m88k.r[13]);
  771|  		m88k_cpu_functioncall_trace(cpu, 8);
  772|  		fatal(") ]\n");
  773|  #endif
  774|  		break;
  775|  
  776|  	case MVMEPROM_VECTOR:
  777|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MVMEPROM_VECTOR", VERBOSITY_INFO, "%s", "");
  778|  		break;
  779|  
  780|  	default:
  781|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unknown vector",
  782|  		    vector < M88K_EXCEPTION_USER_TRAPS_START ? VERBOSITY_ERROR
  783|  		    : VERBOSITY_INFO, "0x%03x", vector);
  784|  	}
  785|  
  786|  	/*
  787|  	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
  788|  	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
  789|  	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
  790|  	 *  6.8.3), like the four this fallback never covered.  Before, any of them
  791|  	 *  stopped EVERY guest CPU here: one divu by zero, in either mode, ended
  792|  	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
  793|  	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
  794|  	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
  795|  	 *  here, by design: SFU1_PRECISE/IMPRECISE (114/115; row m88kexcsfu1 --
  796|  	 *  faithful delivery needs the rest of the SFU1 exception state, which
  797|  	 *  the fork does not write) and vectors 11..113/116..127 (117 vectors
  798|  	 *  with the two SFU1 ones), which no literal-constant raise site names
  799|  	 *  but a supervisor tb0/tb1/tcnd can name directly (row
  800|  	 *  m88kexctaildefault; the probe's resid50/sfu1h rows pin that they
  801|  	 *  STILL halt).
  802|  	 */
  803|  	if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) {
  804|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unimplemented",
  805|  		    VERBOSITY_ERROR, "vector=0x%03x pc=0x%08x",
  806|  			vector,
  807|  			(int)cpu->pc);
  808|  		for (int j = 0; j < cpu->machine->ncpus; ++j)
  809|  			cpu->machine->cpus[j]->running = false;
  810|  		m88k_pc_to_pointers(cpu);
  811|  		return;
  812|  	}
  813|  
  814|  	/*  Stuff common for all exceptions:  */
  815|  	if (cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_SFRZ) {
  816|  		/*
  817|  		 *  Non-trap exceptions when the shadow freeze bit is already
  818|  		 *  set result in an Error exception:
  819|  		 */
  820|  		if (!is_trap) {
  821|  			vector = M88K_EXCEPTION_ERROR;
  822|  			fatal("[ SFRZ already set in PSR => ERROR ]\n");
  823|  		}
     | [... lines 824-955 not shown ...]
  956|  			    routes: the SFRZ re-route above (a fault inside a handler,
  957|  			    shadows deliberately frozen at the FIRST fault's values --
  958|  			    SXIP then names that first fault, not this one) and a
  959|  			    supervisor tb0/tb1/tcnd naming vector 10 directly (shadows
  960|  			    updated normally when that trap is taken UNFROZEN; inside a
  961|  			    handler it takes the is_trap exemption above and arrives
  962|  			    here with the shadows frozen).  Not modelled, disclosed: scoreboard
  963|  			    capture (the shadow-update path writes SSBR = 0; a frozen
  964|  			    SSBR keeps its old value) and fcr2/fcr4/fcr5 for the divide.  */
  965|  			break;
  966|  
  967|  #if 0
  968|  		// TODO: Read up more about SFU1 exceptions and how the
  969|  		// control registers look when they happen.
  970|  		case M88K_EXCEPTION_SFU1_PRECISE:
  971|  			cpu->cd.m88k.cr[M88K_CR_SNIP] = 0; //?
  972|  			cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
  973|  			//cpu->cd.m88k.cr[M88K_CR_SNIP] -= 4;
  974|  			//cpu->cd.m88k.cr[M88K_CR_SFIP] -= 4;
  975|  			break;
  976|  #endif
  977|  
  978|  		default:debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "m88k",
  979|  			    VERBOSITY_ERROR, "internal error");
  980|  			cpu->running = false;
  981|  		}
  982|  	}
  983|  
  984|  	m88k_pc_to_pointers(cpu);
  985|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_m88k.c",
    "old": "\tcase M88K_EXCEPTION_SFU1_PRECISE:\n\t\tdebugmsg_cpu(cpu, SUBSYS_EXCEPTION, \"SFU1_PRECISE\", VERBOSITY_ERROR, \"%s\", \"\");\n\t\tbreak;\n\n\tcase M88K_EXCEPTION_SFU1_IMPRECISE:\n\t\tdebugmsg_cpu(cpu, SUBSYS_EXCEPTION, \"SFU1_IMPRECISE\", VERBOSITY_ERROR, \"%s\", \"\");\n\t\tbreak;",
    "new": "\tcase M88K_EXCEPTION_SFU1_PRECISE:\n\t\tdebugmsg_cpu(cpu, SUBSYS_EXCEPTION, \"SFU1_PRECISE\", VERBOSITY_ERROR, \"%s\", \"\");\n\t\timplemented = true; /* #380: deliver to guest */\n\t\tbreak;\n\n\tcase M88K_EXCEPTION_SFU1_IMPRECISE:\n\t\tdebugmsg_cpu(cpu, SUBSYS_EXCEPTION, \"SFU1_IMPRECISE\", VERBOSITY_ERROR, \"%s\", \"\");\n\t\timplemented = true; /* #380: deliver to guest */\n\t\tbreak;",
    "why": "Deliver SFU1 exceptions to the guest to prevent the emulator from halting the guest CPUs."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_M88KEXCSFU1: DEFECT, 3 FINDINGS
1. The diff removes the emulator halt but fails to address the missing architected state (FPU exception registers and scoreboard) required for faithful delivery, which the issue notes the fork never writes. By delivering the exception anyway, it exposes the guest OS to unwritten or stale state.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips code. Setting `implemented = true` bypasses the fallback block and correctly routes flow to the common tail at `src/cpus/cpu_m88k.c:816` (`/* Stuff common for all exceptions: */`).
3. RETURN VALUE: No path returns a different value; the `m88k_exception` function returns `void`.
4. What ELSE does the diff change: Beyond delivering an incomplete exception, it renders the existing block comment at `src/cpus/cpu_m88k.c:797-799` incorrect, as SFU1_PRECISE and SFU1_IMPRECISE no longer land at the fallback halt "by design". 
5. House idioms: Because the guest CPU no longer halts on these exceptions, the `VERBOSITY_ERROR` diagnostics for SFU1_PRECISE and SFU1_IMPRECISE can now be triggered repeatedly by the guest, violating the idiom requiring a `(once)` latch for spammable messages.
`src/cpus/cpu_m88k.c:759` - DEFECT: Delivers exception without the required FPU/scoreboard state; fix: write the required exception registers before delivery, or revert.
`src/cpus/cpu_m88k.c:797` - DEFECT: Comment is rendered stale; fix: remove the claim that SFU1 exceptions land here by design.
`src/cpus/cpu_m88k.c:758` - STYLE: Diagnostic can now be repeatedly spammed by the guest; fix: add a static latch and `(once)` to the message string.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_M88KEXCSFU1: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_M88KEXCSFU1: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
