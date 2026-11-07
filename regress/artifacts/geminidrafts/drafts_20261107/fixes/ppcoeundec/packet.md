# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcoeundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcoeundec`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c XO decode -- the OE=1 forms and `addc.` are undecoded (the oe_bit check is dead code) -- CPU-STOP

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T128 (class CPU-STOP; reach U, user mode; effort: small-medium; report rows: A4-10).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/93b20502079f2b3b6732940fc1ae89e22b3b7ba4, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/e88c21b997c83d816aea2f4806ed05a5723e5492.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:5062-5137.  Portable fix: partial, or an idea only -- partial: rs6000 93b2050, rs6000 e88c21b (OE set incomplete; do not port its CA rewrite).  Filing check (TRIAGE.md): 0 hits.  Do not port rs6000's CA rewrite (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md F).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port partial OE fixes, excluding CA rewrite

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 5062 (HEAD d2a6f233, lines 5017-5107)

```c
 5017| 			break;
 5018| 
 5019| 		case PPC_31_LBZX:
 5020| 		case PPC_31_LBZUX:
 5021| 		case PPC_31_LHAX:
 5022| 		case PPC_31_LHAUX:
 5023| 		case PPC_31_LHZX:
 5024| 		case PPC_31_LHZUX:
 5025| 		case PPC_31_LWZX:
 5026| 		case PPC_31_LWZUX:
 5027| 		case PPC_31_LHBRX:
 5028| 		case PPC_31_LWBRX:
 5029| 		case PPC_31_LFDX:
 5030| 		case PPC_31_LFDUX:	/*  #310  */
 5031| 		case PPC_31_LFSX:
 5032| 		case PPC_31_LFSUX:	/*  #310  */
 5033| 		case PPC_31_STBX:
 5034| 		case PPC_31_STBUX:
 5035| 		case PPC_31_STHX:
 5036| 		case PPC_31_STHUX:
 5037| 		case PPC_31_STWX:
 5038| 		case PPC_31_STWUX:
 5039| 		case PPC_31_STDX:
 5040| 		case PPC_31_STDUX:
 5041| 		case PPC_31_STHBRX:
 5042| 		case PPC_31_STWBRX:
 5043| 		case PPC_31_STFDX:
 5044| 		case PPC_31_STFDUX:	/*  #310  */
 5045| 		case PPC_31_STFSX:
 5046| 		case PPC_31_STFSUX:	/*  #310  */
 5047| 			rs = (iword >> 21) & 31;
 5048| 			ra = (iword >> 16) & 31;
 5049| 			rb = (iword >> 11) & 31;
 5050| 			if (ra == 0)
 5051| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 5052| 			else
 5053| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5054| 			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5055| 			load = 0; zero = 1; size = 0; update = 0;
 5056| 			byterev = 0; fp = 0;
 5057| 			ic->f = NULL;
 5058| 			switch (xo) {
 5059| 			case PPC_31_LBZX:  load = 1; break;
 5060| 			case PPC_31_LBZUX: load=update=1; break;
 5061| 			case PPC_31_LHAX:  size=1; load=1; zero=0; break;
 5062| 			case PPC_31_LHAUX: size=1; load=update=1; zero=0; break;
 5063| 			case PPC_31_LHZX:  size=1; load=1; break;
 5064| 			case PPC_31_LHZUX: size=1; load=update = 1; break;
 5065| 			case PPC_31_LWZX:  size=2; load=1; break;
 5066| 			case PPC_31_LWZUX: size=2; load=update = 1; break;
 5067| 			case PPC_31_LHBRX: size=1; load=1; byterev=1;
 5068| 					   ic->f = instr(lhbrx); break;
 5069| 			case PPC_31_LWBRX: size=2; load=1; byterev=1;
 5070| 					   ic->f = instr(lwbrx); break;
 5071| 			case PPC_31_LFDX:  size=3; load=1; fp=1;
 5072| 					   ic->f = instr(lfdx); break;
 5073| 			case PPC_31_LFDUX: size=3; load=1; fp=1; update=1;
 5074| 					   ic->f = instr(lfdux); break;	/*  #310  */
 5075| 			case PPC_31_LFSX:  size=2; load=1; fp=1;
 5076| 					   ic->f = instr(lfsx); break;
 5077| 			case PPC_31_LFSUX: size=2; load=1; fp=1; update=1;
 5078| 					   ic->f = instr(lfsux); break;	/*  #310  */
 5079| 			case PPC_31_STBX:  break;
 5080| 			case PPC_31_STBUX: update = 1; break;
 5081| 			case PPC_31_STHX:  size=1; break;
 5082| 			case PPC_31_STHUX: size=1; update = 1; break;
 5083| 			case PPC_31_STWX:  size=2; break;
 5084| 			case PPC_31_STWUX: size=2; update = 1; break;
 5085| 			case PPC_31_STDX:  size=3; break;
 5086| 			case PPC_31_STDUX: size=3; update = 1; break;
 5087| 			case PPC_31_STHBRX:size=1; byterev = 1;
 5088| 					   ic->f = instr(sthbrx); break;
 5089| 			case PPC_31_STWBRX:size=2; byterev = 1;
 5090| 					   ic->f = instr(stwbrx); break;
 5091| 			case PPC_31_STFDX: size=3; fp=1;
 5092| 					   ic->f = instr(stfdx); break;
 5093| 			case PPC_31_STFDUX:size=3; fp=1; update=1;
 5094| 					   ic->f = instr(stfdux); break;	/*  #310  */
 5095| 			case PPC_31_STFSX: size=2; fp=1;
 5096| 					   ic->f = instr(stfsx); break;
 5097| 			case PPC_31_STFSUX:size=2; fp=1; update=1;
 5098| 					   ic->f = instr(stfsux); break;	/*  #310  */
 5099| 			}
 5100| 			if (fp)
 5101| 				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rs]);
 5102| 			else
 5103| 				ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 5104| 			if (!byterev && ic->f == NULL) {
 5105| 				ic->f =
 5106| #ifdef MODE32
 5107| 				    ppc32_loadstore_indexed
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

End with one line: `FIXDRAFT_PPCOEUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
