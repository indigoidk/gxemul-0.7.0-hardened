# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppclswxundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppclswxundec`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c -- lswx/stswx (31/533, 31/661) are undecoded (not even defined in opcodes_ppc.h) -- CPU-STOP

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T123 (class CPU-STOP; reach U, user mode; effort: small; report rows: A4-8).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8bcf95a20ad8285503b81a2796f8430dd513cf10, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3cdc32f0d3ab8f4d33f09a13a02b4c5cb80b3221.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:5172, :4874-4888 (lines of de8c7547; at 987cb596 :5201, :4903-4917).  Portable fix: yes -- port rs6000 8bcf95a, rs6000 3cdc32f.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port the mentioned commits to decode lswx/stswx

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 5172 (HEAD 8d9df658, lines 5052-5292)

```c
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
 5108| #else
 5109| 				    ppc_loadstore_indexed
 5110| #endif
 5111| 				    [size + 4*zero + 8*load + 16*update];
 5112| 			}
 5113| 			if (ra == 0 && update) {
 5114| 				if (!cpu->translation_readahead)
 5115| 					fatal("TODO: ra=0 && update?\n");
 5116| 				goto bad;
 5117| 			}
 5118| 			break;
 5119| 
 5120| 		case PPC_31_EXTSB:
 5121| 		case PPC_31_EXTSH:
 5122| 		case PPC_31_EXTSW:
 5123| 		case PPC_31_SLW:
 5124| 		case PPC_31_SLD:
 5125| 		case PPC_31_SRAW:
 5126| 		case PPC_31_SRW:
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
 5218| 			case PPC_31_SUBFE:  ic->f = instr(subfe); n64=1; break;
 5219| 			case PPC_31_SUBFME: ic->f = instr(subfme); n64=1; break;
 5220| 			case PPC_31_SUBFZE: ic->f = instr(subfze); n64=1;break;
 5221| 			}
 5222| 			if (rc) {
 5223| 				switch (xo) {
 5224| 				case PPC_31_ADD:
 5225| 					ic->f = instr(add_dot); break;
 5226| 				case PPC_31_ADDE:
 5227| 					ic->f = instr(adde_dot); break;
 5228| 				case PPC_31_ADDME:
 5229| 					ic->f = instr(addme_dot); break;
 5230| 				case PPC_31_ADDZE:
 5231| 					ic->f = instr(addze_dot); break;
 5232| 				case PPC_31_DIVW:
 5233| 					ic->f = instr(divw_dot); break;
 5234| 				case PPC_31_DIVWU:
 5235| 					ic->f = instr(divwu_dot); break;
 5236| 				case PPC_31_MULLW:
 5237| 					ic->f = instr(mullw_dot); break;
 5238| 				case PPC_31_MULHW:
 5239| 					ic->f = instr(mulhw_dot); break;
 5240| 				case PPC_31_MULHWU:
 5241| 					ic->f = instr(mulhwu_dot); break;
 5242| 				case PPC_31_SUBF:
 5243| 					ic->f = instr(subf_dot); break;
 5244| 				case PPC_31_SUBFC:
 5245| 					ic->f = instr(subfc_dot); break;
 5246| 				case PPC_31_SUBFE:
 5247| 					ic->f = instr(subfe_dot); break;
 5248| 				case PPC_31_SUBFME:
 5249| 					ic->f = instr(subfme_dot); break;
 5250| 				case PPC_31_SUBFZE:
 5251| 					ic->f = instr(subfze_dot); break;
 5252| 				default:if (!cpu->translation_readahead)
 5253| 						fatal("RC bit not yet "
 5254| 						    "implemented\n");
 5255| 					goto bad;
 5256| 				}
 5257| 			}
 5258| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5259| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5260| 			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 5261| 			if (cpu->cd.ppc.bits == 64 && n64) {
 5262| 				if (!cpu->translation_readahead)
 5263| 					fatal("Not yet for 64-bit mode\n");
 5264| 				goto bad;
 5265| 			}
 5266| 			break;
 5267| 
 5268| 		case PPC_31_LVX:
 5269| 		case PPC_31_LVXL:
 5270| 		case PPC_31_STVX:
 5271| 		case PPC_31_STVXL:
 5272| 			load = 0;
 5273| 			switch (xo) {
 5274| 			case PPC_31_LVX:
 5275| 			case PPC_31_LVXL:
 5276| 				load = 1; break;
 5277| 			}
 5278| 			rs = (iword >> 21) & 31;
 5279| 			ra = (iword >> 16) & 31;
 5280| 			rb = (iword >> 11) & 31;
 5281| 			ic->arg[0] = rs;
 5282| 			if (ra == 0)
 5283| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 5284| 			else
 5285| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5286| 			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5287| 			ic->f = load? instr(lvx) : instr(stvx);
 5288| 			break;
 5289| 
 5290| 		default:goto bad;
 5291| 		}
 5292| 		break;
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

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_ppclswxundec//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
