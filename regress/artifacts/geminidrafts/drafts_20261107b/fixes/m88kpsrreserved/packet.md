# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `m88kpsrreserved` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `m88kpsrreserved`, state `open`)

**title:** cpus/cpu_m88k.c:m88k_stcr PSR/EPSR -- reserved bits 27..4 are stored verbatim where the MC88100 ignores writes to them -- WRONG-RESULT (SVR4 resumes processes at spl7)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T39 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A7-24, A(c)#9).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k.c:553, :557; src/cpus/cpu_m88k_instr.c:2249.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 01 mask (it also leaves hard-wired bits 9-4 unmodelled).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_m88k.c` -- AT HEAD, lines 520-607 (`*` marks a line your previous draft changed)

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
  557|* 		cpu->cd.m88k.cr[cr] = value;
  558|* 		break;
  559|  
  560|  	case M88K_CR_EPSR:
  561|* 		cpu->cd.m88k.cr[cr] = value;
  562|* 		break;
  563|  
  564|  	case M88K_CR_SXIP:
  565|  	case M88K_CR_SNIP:
  566|  	case M88K_CR_SFIP:
  567|  		cpu->cd.m88k.cr[cr] = value;
  568|  		break;
  569|  
  570|  	case M88K_CR_SSBR:	/*  Shadow ScoreBoard Register  */
  571|  		if (value & 1)
  572|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  573|  			    "stcr: WARNING! bit 0 non-zero when"
  574|  			    " writing to SSBR (?)");
  575|  
  576|  		cpu->cd.m88k.cr[cr] = value;
  577|  		break;
  578|  
  579|  	case M88K_CR_VBR:
  580|  		if (value & 0x00000fff)
  581|  			debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_WARNING,
  582|  			    "stcr: WARNING! bits 0..11 non-zero when"
  583|  			    " writing to VBR (?)");
  584|  
  585|  		cpu->cd.m88k.cr[cr] = value;
  586|  		break;
  587|  
  588|  	case M88K_CR_DMT0:
  589|  	case M88K_CR_DMT1:
  590|  	case M88K_CR_DMT2:
  591|  		cpu->cd.m88k.cr[cr] = value;
  592|  		break;
  593|  
  594|  	case M88K_CR_SR0:	/*  Supervisor Storage Registers 0..3  */
  595|  	case M88K_CR_SR1:
  596|  	case M88K_CR_SR2:
  597|  	case M88K_CR_SR3:
  598|  		cpu->cd.m88k.cr[cr] = value;
  599|  		break;
  600|  
  601|  	default:debugmsg_cpu(cpu, SUBSYS_CPU, "m88k", VERBOSITY_ERROR,
  602|  		    "stcr: UNIMPLEMENTED cr = 0x%02x (%s)",
  603|  		    cr, m88k_cr_name(cpu, cr));
  604|  		cpu->running = false;
  605|  		return;
  606|  	}
  607|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_m88k.c",
    "old": "\t\tcpu->cd.m88k.cr[cr] = value;\n\t\tbreak;\n\n\tcase M88K_CR_EPSR:\n\t\tcpu->cd.m88k.cr[cr] = value;\n\t\tbreak;",
    "new": "\t\t/* #m88kpsrreserved: bits 27..4 are reserved and writes are ignored */\n\t\tcpu->cd.m88k.cr[cr] = (value & 0xf000000f) | (old & 0x0ffffff0);\n\t\tbreak;\n\n\tcase M88K_CR_EPSR:\n\t\tcpu->cd.m88k.cr[cr] = (value & 0xf000000f) | (cpu->cd.m88k.cr[cr] & 0x0ffffff0);\n\t\tbreak;",
    "why": "Mask out reserved bits 27..4 to prevent guest from altering them (fixes SVR4 spl7 issue)."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_M88KPSRRESERVED: DEFECT, 2 FINDINGS
1. The diff fails to remove the defect at every site the issue names. While it patches `src/cpus/cpu_m88k.c:557` and `562`, it entirely misses `src/cpus/cpu_m88k_instr.c:2249` which was explicitly named in the ledger (`The issue:41`).
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips any code. The control flow remains identical, simply replacing direct assignments with bitwise expressions before existing `break;` statements (`src/cpus/cpu_m88k.c:559, 563`).
3. RETURN VALUE: The function `m88k_stcr` has a `void` return type (`src/cpus/cpu_m88k.c:520`), so no return value is changed.
4. ELSE CHANGED: The diff preserves the previous state of bits 27..4 (which includes the hard-wired bits 9-4 mentioned in `The issue:42`) instead of overwriting them with the guest's input. It introduces no other state changes or side effects.
5. HOUSE IDIOMS: The proposed changes violate the 79-column limit. Assuming 8-space tabs, line 562 evaluates to 98 columns, and line 558 evaluates to 81 columns (`src/cpus/cpu_m88k.c:558, 562`).
src/cpus/cpu_m88k_instr.c:2249: DEFECT: Apply the reserved bit mask to EPSR/PSR writes in this file as well.
src/cpus/cpu_m88k.c:562: STYLE: cpu->cd.m88k.cr[cr] = (value & 0xf000000f) |\n\t\t    (old & 0x0ffffff0);
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

End with two lines: `REVISION_M88KPSRRESERVED: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_M88KPSRRESERVED: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
