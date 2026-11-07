# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppclswxundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppclswxundec`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c -- lswx/stswx (31/533, 31/661) are undecoded (not even defined in opcodes_ppc.h) -- CPU-STOP

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T123 (class CPU-STOP; reach U, user mode; effort: small; report rows: A4-8).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8bcf95a20ad8285503b81a2796f8430dd513cf10, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3cdc32f0d3ab8f4d33f09a13a02b4c5cb80b3221.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:5172, :4874-4888 (lines of de8c7547; at 987cb596 :5201, :4903-4917).  Portable fix: yes -- port rs6000 8bcf95a, rs6000 3cdc32f.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port the mentioned commits to decode lswx/stswx

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 5172 (HEAD d2a6f233, lines 5127-5217)

```c
 5127| 		case PPC_31_AND:
 5128| 		case PPC_31_NAND:
 5129| 		case PPC_31_ANDC:
 5130| 		case PPC_31_NOR:
 5131| 		case PPC_31_OR:
 5132| 		case PPC_31_ORC:
 5133| 		case PPC_31_XOR:
 5134| 		case PPC_31_EQV:
 5135| 			rs = (iword >> 21) & 31;
 5136| 			ra = (iword >> 16) & 31;
 5137| 			rb = (iword >> 11) & 31;
 5138| 			rc = iword & 1;
 5139| 			rc_f = NULL;
 5140| 			switch (xo) {
 5141| 			case PPC_31_EXTSB:ic->f = instr(extsb);
 5142| 					  rc_f  = instr(extsb_dot); break;
 5143| 			case PPC_31_EXTSH:ic->f = instr(extsh);
 5144| 					  rc_f  = instr(extsh_dot); break;
 5145| 			case PPC_31_EXTSW:ic->f = instr(extsw);
 5146| 					  rc_f  = instr(extsw_dot); break;
 5147| 			case PPC_31_SLW:  ic->f = instr(slw);
 5148| 					  rc_f  = instr(slw_dot); break;
 5149| 			case PPC_31_SLD:  ic->f = instr(sld);
 5150| 					  rc_f  = instr(sld_dot); break;
 5151| 			case PPC_31_SRAW: ic->f = instr(sraw);
 5152| 					  rc_f  = instr(sraw_dot); break;
 5153| 			case PPC_31_SRW:  ic->f = instr(srw);
 5154| 					  rc_f  = instr(srw_dot); break;
 5155| 			case PPC_31_AND:  ic->f = instr(and);
 5156| 					  rc_f  = instr(and_dot); break;
 5157| 			case PPC_31_NAND: ic->f = instr(nand);
 5158| 					  rc_f  = instr(nand_dot); break;
 5159| 			case PPC_31_ANDC: ic->f = instr(andc);
 5160| 					  rc_f  = instr(andc_dot); break;
 5161| 			case PPC_31_NOR:  ic->f = instr(nor);
 5162| 					  rc_f  = instr(nor_dot); break;
 5163| 			case PPC_31_OR:   ic->f = rs == rb? instr(mr)
 5164| 						: instr(or);
 5165| 					  rc_f  = instr(or_dot); break;
 5166| 			case PPC_31_ORC:  ic->f = instr(orc);
 5167| 					  rc_f  = instr(orc_dot); break;
 5168| 			case PPC_31_XOR:  ic->f = instr(xor);
 5169| 					  rc_f  = instr(xor_dot); break;
 5170| 			case PPC_31_EQV:  ic->f = instr(eqv);
 5171| 					  rc_f  = instr(eqv_dot); break;
 5172| 			}
 5173| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 5174| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5175| 			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5176| 			if (rc)
 5177| 				ic->f = rc_f;
 5178| 			break;
 5179| 
 5180| 		case PPC_31_MULLW:
 5181| 		case PPC_31_MULHW:
 5182| 		case PPC_31_MULHWU:
 5183| 		case PPC_31_DIVW:
 5184| 		case PPC_31_DIVWU:
 5185| 		case PPC_31_ADD:
 5186| 		case PPC_31_ADDC:
 5187| 		case PPC_31_ADDE:
 5188| 		case PPC_31_ADDME:
 5189| 		case PPC_31_ADDZE:
 5190| 		case PPC_31_SUBF:
 5191| 		case PPC_31_SUBFC:
 5192| 		case PPC_31_SUBFE:
 5193| 		case PPC_31_SUBFME:
 5194| 		case PPC_31_SUBFZE:
 5195| 			rt = (iword >> 21) & 31;
 5196| 			ra = (iword >> 16) & 31;
 5197| 			rb = (iword >> 11) & 31;
 5198| 			oe_bit = (iword >> 10) & 1;
 5199| 			rc = iword & 1;
 5200| 			if (oe_bit) {
 5201| 				if (!cpu->translation_readahead)
 5202| 					fatal("oe_bit not yet implemented\n");
 5203| 				goto bad;
 5204| 			}
 5205| 			switch (xo) {
 5206| 			case PPC_31_MULLW:  ic->f = instr(mullw); break;
 5207| 			case PPC_31_MULHW:  ic->f = instr(mulhw); break;
 5208| 			case PPC_31_MULHWU: ic->f = instr(mulhwu); break;
 5209| 			case PPC_31_DIVW:   ic->f = instr(divw); n64=1; break;
 5210| 			case PPC_31_DIVWU:  ic->f = instr(divwu); n64=1; break;
 5211| 			case PPC_31_ADD:    ic->f = instr(add); break;
 5212| 			case PPC_31_ADDC:   ic->f = instr(addc); n64=1; break;
 5213| 			case PPC_31_ADDE:   ic->f = instr(adde); n64=1; break;
 5214| 			case PPC_31_ADDME:  ic->f = instr(addme); n64=1; break;
 5215| 			case PPC_31_ADDZE:  ic->f = instr(addze); n64=1; break;
 5216| 			case PPC_31_SUBF:   ic->f = instr(subf); break;
 5217| 			case PPC_31_SUBFC:  ic->f = instr(subfc); break;
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

End with one line: `FIXDRAFT_PPCLSWXUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
