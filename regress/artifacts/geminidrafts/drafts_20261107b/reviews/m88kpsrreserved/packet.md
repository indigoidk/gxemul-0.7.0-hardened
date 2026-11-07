# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kpsrreserved` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kpsrreserved`, state `open`)

**title:** cpus/cpu_m88k.c:m88k_stcr PSR/EPSR -- reserved bits 27..4 are stored verbatim where the MC88100 ignores writes to them -- WRONG-RESULT (SVR4 resumes processes at spl7)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T39 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A7-24, A(c)#9).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k.c:553, :557; src/cpus/cpu_m88k_instr.c:2249.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 01 mask (it also leaves hard-wired bits 9-4 unmodelled).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/cpu_m88k.c:558` violates 79 columns and `src/cpus/cpu_m88k_instr.c` is unpatched.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k.c b/src/cpus/cpu_m88k.c
index bef69d4c..7724be4f 100644
--- a/src/cpus/cpu_m88k.c
+++ b/src/cpus/cpu_m88k.c
@@ -554,11 +554,14 @@ void m88k_stcr(struct cpu *cpu, uint32_t value, int cr, int rte)
 			cpu->invalidate_translation_caches(
 			    cpu, 0, INVALIDATE_ALL);
 
-		cpu->cd.m88k.cr[cr] = value;
+		/* #m88kpsrreserved: bits 27..4 are reserved and ignored */
+		cpu->cd.m88k.cr[cr] = (value & 0xf000000f) |
+		    (old & 0x0ffffff0);
 		break;
 
 	case M88K_CR_EPSR:
-		cpu->cd.m88k.cr[cr] = value;
+		cpu->cd.m88k.cr[cr] = (value & 0xf000000f) |
+		    (old & 0x0ffffff0);
 		break;
 
 	case M88K_CR_SXIP:
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k.c` -- post-edit lines 520-610 (`+` marks a line the diff added or the point of a deletion)

```c
  520|  void m88k_stcr(struct cpu *cpu, uint32_t value, int cr, int rte)
  521|  {
  522|  	uint32_t old = cpu->cd.m88k.cr[cr];
  523|  
  524|  	switch (cr) {
  525|  
  526|  	case M88K_CR_PSR:	/*  Processor Status Register  */
  527|  		if ((cpu->byte_order == EMUL_LITTLE_ENDIAN
  528|  		    && !(value & M88K_PSR_BO)) ||
  529|  		    (cpu->byte_order == EMUL_BIG_ENDIAN
  530|  		    && (value & M88K_PSR_BO))) {
  531|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  532|  			    "stcr: TODO: attempt to change endianness by flipping"
  533|  			    " the endianness bit in the PSR. How should this"
  534|  			    " be handled? Aborting.");
  535|  			cpu->running = false;
  536|  			return;
  537|  		}
  538|  
  539|  		if (!rte && old & M88K_PSR_MODE && !(value & M88K_PSR_MODE))
  540|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  541|  			    "stcr: WARNING! the PSR_MODE bit is being"
  542|  			    " cleared; this should be done using the RTE "
  543|  			    "instruction only, according to the M88100 "
  544|  			    "manual! Continuing anyway.");
  545|  
  546|  		if (value & M88K_PSR_MXM) {
  547|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  548|  			    "stcr: TODO: MXM support");
  549|  			cpu->running = false;
  550|  			return;
  551|  		}
  552|  
  553|  		if ((old & M88K_PSR_MODE) != (value & M88K_PSR_MODE))
  554|  			cpu->invalidate_translation_caches(
  555|  			    cpu, 0, INVALIDATE_ALL);
  556|  
  557|+ 		/* #m88kpsrreserved: bits 27..4 are reserved and ignored */
  558|+ 		cpu->cd.m88k.cr[cr] = (value & 0xf000000f) |
  559|+ 		    (old & 0x0ffffff0);
  560|  		break;
  561|  
  562|  	case M88K_CR_EPSR:
  563|+ 		cpu->cd.m88k.cr[cr] = (value & 0xf000000f) |
  564|+ 		    (old & 0x0ffffff0);
  565|  		break;
  566|  
  567|  	case M88K_CR_SXIP:
  568|  	case M88K_CR_SNIP:
  569|  	case M88K_CR_SFIP:
  570|  		cpu->cd.m88k.cr[cr] = value;
  571|  		break;
  572|  
  573|  	case M88K_CR_SSBR:	/*  Shadow ScoreBoard Register  */
  574|  		if (value & 1)
  575|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  576|  			    "stcr: WARNING! bit 0 non-zero when"
  577|  			    " writing to SSBR (?)");
  578|  
  579|  		cpu->cd.m88k.cr[cr] = value;
  580|  		break;
  581|  
  582|  	case M88K_CR_VBR:
  583|  		if (value & 0x00000fff)
  584|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  585|  			    "stcr: WARNING! bits 0..11 non-zero when"
  586|  			    " writing to VBR (?)");
  587|  
  588|  		cpu->cd.m88k.cr[cr] = value;
  589|  		break;
  590|  
  591|  	case M88K_CR_DMT0:
  592|  	case M88K_CR_DMT1:
  593|  	case M88K_CR_DMT2:
  594|  		cpu->cd.m88k.cr[cr] = value;
  595|  		break;
  596|  
  597|  	case M88K_CR_SR0:	/*  Supervisor Storage Registers 0..3  */
  598|  	case M88K_CR_SR1:
  599|  	case M88K_CR_SR2:
  600|  	case M88K_CR_SR3:
  601|  		cpu->cd.m88k.cr[cr] = value;
  602|  		break;
  603|  
  604|  	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  605|  		    "stcr: UNIMPLEMENTED cr = 0x%02x (%s)",
  606|  		    cr, m88k_cr_name(cpu, cr));
  607|  		cpu->running = false;
  608|  		return;
  609|  	}
  610|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KPSRRESERVED: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KPSRRESERVED: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
