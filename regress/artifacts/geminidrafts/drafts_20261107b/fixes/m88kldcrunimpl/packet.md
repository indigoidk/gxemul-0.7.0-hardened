# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `m88kldcrunimpl` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `m88kldcrunimpl`, state `open`)

**title:** src/cpus/cpu_m88k.c:503-507 -- m88k_ldcr's default arm stops the emulated CPU on an ldcr of any control register its switch does not list (cr21-cr63; the switch lists cr0-cr20) -- CPU-STOP (supervisor only)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_m88k.c` -- AT HEAD, lines 434-511 (`*` marks a line your previous draft changed)

```c
  434|  void m88k_ldcr(struct cpu *cpu, uint32_t *r32ptr, int cr)
  435|  {
  436|  	uint32_t retval = cpu->cd.m88k.cr[cr];
  437|  
  438|  	switch (cr) {
  439|  
  440|  	case M88K_CR_PID:
  441|  	case M88K_CR_PSR:
  442|  	case M88K_CR_EPSR:
  443|  	case M88K_CR_SSBR:
  444|  	case M88K_CR_SXIP:
  445|  	case M88K_CR_SNIP:
  446|  	case M88K_CR_SFIP:
  447|  	case M88K_CR_VBR:
  448|  	case M88K_CR_DMD0:
  449|  	case M88K_CR_DMD1:
  450|  	case M88K_CR_DMD2:
  451|  	case M88K_CR_SR0:
  452|  	case M88K_CR_SR1:
  453|  	case M88K_CR_SR2:
  454|  	case M88K_CR_SR3:
  455|  		break;
  456|  
  457|  	case M88K_CR_DMT0:
  458|  	case M88K_CR_DMT1:
  459|  	case M88K_CR_DMT2:
  460|  		/*
  461|  		 *  Catch some possible internal errors in the emulator:
  462|  		 *
  463|  		 *  For valid memory Load transactions, the Destination Register
  464|  		 *  should not be zero.
  465|  		 *
  466|  		 *  The Byte Order bit should be the same as the CPU's.
  467|  		 */
  468|  		if (retval & DMT_VALID && !(retval & DMT_WRITE)) {
  469|  			if (DMT_DREGBITS(retval) == M88K_ZERO_REG) {
  470|  				debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  471|  				    "ldcr: DMT DREG = zero? Internal error.");
  472|  				cpu->running = false;
  473|  				return;
  474|  			}
  475|  		}
  476|  		if (!!(cpu->cd.m88k.cr[M88K_CR_PSR] & M88K_PSR_BO)
  477|  		    != !!(retval & DMT_BO) && retval & DMT_VALID) {
  478|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  479|  			    "ldcr: DMT byte order not same as CPUs?");
  480|  			cpu->running = false;
  481|  			return;
  482|  		}
  483|  
  484|  		break;
  485|  
  486|  	case M88K_CR_DMA0:
  487|  	case M88K_CR_DMA1:
  488|  	case M88K_CR_DMA2:
  489|  		/*
  490|  		 *  Catch some possible internal errors in the emulator:
  491|  		 *  The lowest 2 bits of the transaction address registers
  492|  		 *  should always be zero.
  493|  		 */
  494|  		if (retval & 3) {
  495|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  496|  			    "ldcr: DMAx not word-aligned? Internal error.");
  497|  			cpu->running = false;
  498|  			return;
  499|  		}
  500|  
  501|  		break;
  502|  
  503|  	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  504|  		    "ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\n",
  505|  		    cr, m88k_cr_name(cpu, cr));
  506|* 		cpu->running = false;
  507|* 		return;
  508|* 	}
  509|  
  510|  	*r32ptr = retval;
  511|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_m88k.c",
    "old": "\tdefault:debugmsg_cpu(cpu, SUBSYS_CPU, \"m88k\", VERBOSITY_ERROR,\n\t\t    \"ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\\n\",\n\t\t    cr, m88k_cr_name(cpu, cr));\n\t\tcpu->running = false;\n\t\treturn;",
    "new": "\tdefault:debugmsg_cpu(cpu, SUBSYS_CPU, \"m88k\", VERBOSITY_ERROR,\n\t\t    \"ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\\n\",\n\t\t    cr, m88k_cr_name(cpu, cr));\n\t\t/* #m88kldcrunimpl: ignore unimplemented register reads to avoid crashing */\n\t\tbreak;",
    "why": "Prevent emulator termination on unimplemented control register loads."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_M88KLDCRUNIMPL: DEFECT, 1 FINDINGS
1. Yes, the diff removes the `cpu->running = false` defect at the named site in the `default:` case.
2. CONTROL FLOW: The added `break` Replaces a `return`, which means it now RUNS the common tail it previously skipped: `*r32ptr = retval;` at line 510. This is the desired behavior (returning a value instead of aborting).
3. RETURN VALUE: The function is `void` and has no return value.
4. What ELSE does the diff change: The guest now receives the value of `cpu->cd.m88k.cr[cr]` when reading an unimplemented register, as it falls through to the assignment at line 510. Furthermore, because the emulator no longer stops, the guest can now trigger the `debugmsg_cpu` repeatedly by putting the read in a loop.
5. House idioms: The existing `debugmsg_cpu` is now a spam vector because the CPU continues executing. It must be throttled to print ONCE. The comment carries the correct tag format.
src/cpus/cpu_m88k.c:503: DEFECT: Since the CPU no longer stops, the guest can spam the log. The diagnostic should be updated to print ONCE. `default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR, ...` -> needs a latch or similar mechanism.
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

End with two lines: `REVISION_M88KLDCRUNIMPL: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_M88KLDCRUNIMPL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
