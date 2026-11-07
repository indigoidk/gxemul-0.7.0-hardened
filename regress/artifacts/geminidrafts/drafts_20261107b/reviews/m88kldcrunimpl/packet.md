# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kldcrunimpl` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kldcrunimpl`, state `open`)

**title:** src/cpus/cpu_m88k.c:503-507 -- m88k_ldcr's default arm stops the emulated CPU on an ldcr of any control register its switch does not list (cr21-cr63; the switch lists cr0-cr20) -- CPU-STOP (supervisor only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 506: `cpu->running = false;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k.c b/src/cpus/cpu_m88k.c
index bef69d4c..02ca33ed 100644
--- a/src/cpus/cpu_m88k.c
+++ b/src/cpus/cpu_m88k.c
@@ -500,11 +500,17 @@ void m88k_ldcr(struct cpu *cpu, uint32_t *r32ptr, int cr)
 
 		break;
 
-	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
-		    "ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\n",
-		    cr, m88k_cr_name(cpu, cr));
-		cpu->running = false;
-		return;
+	default: {
+			static bool warned = false;
+			if (!warned) {
+				debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
+				    "ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\n",
+				    cr, m88k_cr_name(cpu, cr));
+				warned = true;
+			}
+		}
+		/* #m88kldcrunimpl: ignore unimplemented register reads to avoid crashing */
+		break;
 	}
 
 	*r32ptr = retval;
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k.c` -- post-edit lines 434-517 (`+` marks a line the diff added or the point of a deletion)

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
  503|+ 	default: {
  504|+ 			static bool warned = false;
  505|+ 			if (!warned) {
  506|+ 				debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  507|+ 				    "ldcr: UNIMPLEMENTED cr = 0x%02x (%s)\n",
  508|+ 				    cr, m88k_cr_name(cpu, cr));
  509|+ 				warned = true;
  510|+ 			}
  511|+ 		}
  512|+ 		/* #m88kldcrunimpl: ignore unimplemented register reads to avoid crashing */
  513|+ 		break;
  514|  	}
  515|  
  516|  	*r32ptr = retval;
  517|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KLDCRUNIMPL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KLDCRUNIMPL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
