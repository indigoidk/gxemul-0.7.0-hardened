# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kexcsfu1` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kexcsfu1`, state `open`)

**title:** m88kexcsfu1  the m88k exception core stops every guest CPU on SFU1_PRECISE (vector 114, 58 raise sites: any FP/mul/div with SFD1 set, or an FP divide by zero) and the latent SFU1_IMPRECISE, instead of delivering VBR+0x390/0x398

**state_note (head):** DEFECT, MEDIUM -- split from m88kexcdeliver because faithful delivery needs the FP exception registers FPHS1/FPLS1/FPHS2/FPLS2/FPPT/FPRH/FPRL/FPIT (MC88100 UM Fig 6-1, mc88100.txt:8486-8514, sec 6.8.1), which the fork never writes (grep -c 'FPHS1\|FPLS1\|FPPT' src/cpus/*.c = 0); the FPU-disabled case (sec 6.8.4.1, :10324) needs only EPSR.SFD1.  [2026-11-02, records: faithful delivery also owes the scoreboard, which this note did not name -- MC88100 UM 6.8.4 (mc88100.txt:10318-10322): in every precise FP case, the FPU-disabled one included, the destination scoreboard bit(s) are set before the exception is recognized and the handler clears them; the SSBR holds the scoreboard in effect at the exception for rte to restore (6.4.3.1.1, mc88100.txt:8873-8877).  `m88kdivcontext`'s title assigns precise FP delivery to this row and records no scoreboard duty either]  FPECR is already set at the raise sites (X(fdiv_sss) sets FDVZ).  Witness: rung-3 FP-divide-by-zero or FP-with-SFD1-set probe on testm88k; pre-fix `unimplemented vector=0x072' and the machine stops.  Same fallback as m88kexcdeliver (cpu_m88k.c, anchor `vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented'), pre-existing upstream.  Rank below m88kexcdeliver.  Provenance: retrospective re-check (owner directive 2026-09-04) batch 2 -- GPT-6 Astra (codex, max effort) read-only review, adjudicated by Fable 5.1; artifacts regress/artifacts/retro_20260905/batch2_m88k/ (astra_batch2.txt, fable_adj_batch2.md).  The other seven panel seats were DELIBERATELY NOT FIRED on the retrospective (owner scope); the fix round runs the full nine-seat panel.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_m88k.c:759

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k.c b/src/cpus/cpu_m88k.c
index bef69d4c..33da4d9c 100644
--- a/src/cpus/cpu_m88k.c
+++ b/src/cpus/cpu_m88k.c
@@ -756,10 +756,12 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 
 	case M88K_EXCEPTION_SFU1_PRECISE:
 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_PRECISE", VERBOSITY_ERROR, "%s", "");
+		implemented = true;	/*  #380  */
 		break;
 
 	case M88K_EXCEPTION_SFU1_IMPRECISE:
 		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "%s", "");
+		implemented = true;	/*  #380  */
 		break;
 
 	case 0x80:	/*  up to OpenBSD 5.2  */
@@ -792,10 +794,8 @@ void m88k_exception(struct cpu *cpu, int vector, int is_trap)
 	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
 	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
 	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
-	 *  here, by design: SFU1_PRECISE/IMPRECISE (114/115; row m88kexcsfu1 --
-	 *  faithful delivery needs the rest of the SFU1 exception state, which
-	 *  the fork does not write) and vectors 11..113/116..127 (117 vectors
-	 *  with the two SFU1 ones), which no literal-constant raise site names
+	 *  here, by design: vectors 11..113/116..127 (115 vectors),
+	 *  which no literal-constant raise site names
 	 *  but a supervisor tb0/tb1/tcnd can name directly (row
 	 *  m88kexctaildefault; the probe's resid50/sfu1h rows pin that they
 	 *  STILL halt).
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k.c` -- post-edit lines 693-985 (`+` marks a line the diff added or the point of a deletion)

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
  759|+ 		implemented = true;	/*  #380  */
  760|  		break;
  761|  
  762|  	case M88K_EXCEPTION_SFU1_IMPRECISE:
  763|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "SFU1_IMPRECISE", VERBOSITY_ERROR, "%s", "");
  764|+ 		implemented = true;	/*  #380  */
  765|  		break;
  766|  
  767|  	case 0x80:	/*  up to OpenBSD 5.2  */
  768|  	case 0x1c2:	/*  from OpenBSD 5.3 and forward...  */
  769|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "syscall", VERBOSITY_INFO,
  770|  		    "r13=%i", cpu->cd.m88k.r[13]);
  771|  #if 0
  772|  		fatal("[ syscall %i(", cpu->cd.m88k.r[13]);
  773|  		m88k_cpu_functioncall_trace(cpu, 8);
  774|  		fatal(") ]\n");
  775|  #endif
  776|  		break;
  777|  
  778|  	case MVMEPROM_VECTOR:
  779|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "MVMEPROM_VECTOR", VERBOSITY_INFO, "%s", "");
  780|  		break;
  781|  
  782|  	default:
  783|  		debugmsg_cpu(cpu, SUBSYS_EXCEPTION, "unknown vector",
  784|  		    vector < M88K_EXCEPTION_USER_TRAPS_START ? VERBOSITY_ERROR
  785|  		    : VERBOSITY_INFO, "0x%03x", vector);
  786|  	}
  787|  
  788|  	/*
  789|  	 *  m88kexcdeliver (2026-09-05): the seven trap-like classes above are
  790|  	 *  DELIVERED (VBR + 8*vector, SXIP = the faulting instruction, SNIP = the
  791|  	 *  next one, destination register unchanged -- MC88100 UM 6.4.3/6.5/6.6/
  792|  	 *  6.8.3), like the four this fallback never covered.  Before, any of them
  793|  	 *  stopped EVERY guest CPU here: one divu by zero, in either mode, ended
  794|  	 *  the emulation (measured: regress/m88k_exc_probe.py rows div0/udiv0).
  795|  	 *  Pre-existing upstream code (this fallback is the 0.7.0 import),
  796|  	 *  surfaced by the 2026-09-05 retrospective of #380.  What still lands
  797|+ 	 *  here, by design: vectors 11..113/116..127 (115 vectors),
  798|+ 	 *  which no literal-constant raise site names
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
  824|  
  825|  		update_shadow_regs = false;
  826|  	} else {
  827|  		/*  Freeze shadow registers, and save the PSR:  */
  828|  		cpu->cd.m88k.cr[M88K_CR_EPSR] = cpu->cd.m88k.cr[M88K_CR_PSR];
  829|  	}
  830|  
  831|  	m88k_stcr(cpu, cpu->cd.m88k.cr[M88K_CR_PSR]
  832|  	    | M88K_PSR_SFRZ	/*  Freeze shadow registers,          */
  833|  	    | M88K_PSR_IND	/*  disable interrupts,               */
  834|  	    | M88K_PSR_SFD1	/*  disable the floating point unit,  */
  835|  	    | M88K_PSR_MODE,	/*  and switch to supervisor mode.    */
  836|  	    M88K_CR_PSR, 0);
  837|  
  838|  	if (update_shadow_regs) {
  839|  		cpu->cd.m88k.cr[M88K_CR_SSBR] = 0;
  840|  
  841|  		cpu->cd.m88k.cr[M88K_CR_SXIP] = cpu->pc | M88K_XIP_V;
  842|  
  843|  		/*  SNIP is the address to return to, when executing rte:  */
  844|  		if (cpu->delay_slot) {
  845|  			if (vector == M88K_EXCEPTION_DATA_ACCESS) {
  846|  				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
  847|  				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.cr[M88K_CR_SNIP]+4;
  848|  			} else if (vector == M88K_EXCEPTION_INSTRUCTION_ACCESS) {
  849|  				/*  If we are in a delay slot, then pc is
  850|  				    something like 0xc6000 here (not 0xc5ffc).  */
  851|  				cpu->cd.m88k.cr[M88K_CR_SNIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
  852|  				cpu->cd.m88k.cr[M88K_CR_SFIP] = 0;
  853|  			} else {
  854|  				/*  Perhaps something like this could work:  */
  855|  				cpu->cd.m88k.cr[M88K_CR_SNIP] = (cpu->pc + 4) | M88K_NIP_V;
  856|  				cpu->cd.m88k.cr[M88K_CR_SFIP] = cpu->cd.m88k.delay_target | M88K_NIP_V;
  857|  			}
  858|  		} else {
     | [... lines 859-955 not shown ...]
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

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KEXCSFU1: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_M88KEXCSFU1: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
