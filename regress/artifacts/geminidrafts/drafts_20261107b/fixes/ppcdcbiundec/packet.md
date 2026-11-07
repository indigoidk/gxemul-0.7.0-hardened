# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcdcbiundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcdcbiundec`, state `open`)

**title:** cpus/cpu_ppc_instr.c cache-op group -- dcbi (31/470) is undecoded, including in user mode where it is a privileged instruction -- CPU-STOP

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T125 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A4-11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3762e129146664c0ac8d4433f111e736c1da37c0, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3cdc32f0d3ab8f4d33f09a13a02b4c5cb80b3221.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:5172, :4782-4791.  Portable fix: yes -- port rs6000 3762e12, rs6000 3cdc32f.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc_instr.c` -- AT HEAD, lines 4084-5551 (`*` marks a line your previous draft changed)

```c
 4084|  X(to_be_translated)
 4085|  {
 4086|  	uint64_t addr, low_pc, tmp_addr;
 4087|  	uint32_t iword, mask;
 4088|  	unsigned char *page;
     | [... lines 4089-5160 not shown ...]
 5161|  			case PPC_31_NOR:  ic->f = instr(nor);
 5162|  					  rc_f  = instr(nor_dot); break;
 5163|  			case PPC_31_OR:   ic->f = rs == rb? instr(mr)
 5164|  						: instr(or);
 5165|  					  rc_f  = instr(or_dot); break;
 5166|  			case PPC_31_ORC:  ic->f = instr(orc);
 5167|  					  rc_f  = instr(orc_dot); break;
 5168|  			case PPC_31_XOR:  ic->f = instr(xor);
 5169|  					  rc_f  = instr(xor_dot); break;
 5170|  			case PPC_31_EQV:  ic->f = instr(eqv);
 5171|  					  rc_f  = instr(eqv_dot); break;
 5172|  			}
 5173|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 5174|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5175|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5176|  			if (rc)
 5177|  				ic->f = rc_f;
 5178|  			break;
 5179|  
 5180|  		case PPC_31_MULLW:
 5181|  		case PPC_31_MULHW:
 5182|  		case PPC_31_MULHWU:
 5183|  		case PPC_31_DIVW:
 5184|  		case PPC_31_DIVWU:
 5185|  		case PPC_31_ADD:
 5186|  		case PPC_31_ADDC:
 5187|  		case PPC_31_ADDE:
 5188|  		case PPC_31_ADDME:
 5189|  		case PPC_31_ADDZE:
 5190|  		case PPC_31_SUBF:
 5191|  		case PPC_31_SUBFC:
 5192|  		case PPC_31_SUBFE:
 5193|  		case PPC_31_SUBFME:
 5194|  		case PPC_31_SUBFZE:
 5195|  			rt = (iword >> 21) & 31;
 5196|  			ra = (iword >> 16) & 31;
 5197|  			rb = (iword >> 11) & 31;
 5198|  			oe_bit = (iword >> 10) & 1;
 5199|  			rc = iword & 1;
 5200|  			if (oe_bit) {
 5201|  				if (!cpu->translation_readahead)
 5202|  					fatal("oe_bit not yet implemented\n");
 5203|  				goto bad;
 5204|  			}
 5205|  			switch (xo) {
 5206|  			case PPC_31_MULLW:  ic->f = instr(mullw); break;
 5207|  			case PPC_31_MULHW:  ic->f = instr(mulhw); break;
 5208|  			case PPC_31_MULHWU: ic->f = instr(mulhwu); break;
 5209|  			case PPC_31_DIVW:   ic->f = instr(divw); n64=1; break;
 5210|  			case PPC_31_DIVWU:  ic->f = instr(divwu); n64=1; break;
 5211|  			case PPC_31_ADD:    ic->f = instr(add); break;
 5212|  			case PPC_31_ADDC:   ic->f = instr(addc); n64=1; break;
 5213|  			case PPC_31_ADDE:   ic->f = instr(adde); n64=1; break;
 5214|  			case PPC_31_ADDME:  ic->f = instr(addme); n64=1; break;
 5215|  			case PPC_31_ADDZE:  ic->f = instr(addze); n64=1; break;
 5216|  			case PPC_31_SUBF:   ic->f = instr(subf); break;
 5217|  			case PPC_31_SUBFC:  ic->f = instr(subfc); break;
 5218|  			case PPC_31_SUBFE:  ic->f = instr(subfe); n64=1; break;
 5219|  			case PPC_31_SUBFME: ic->f = instr(subfme); n64=1; break;
 5220|  			case PPC_31_SUBFZE: ic->f = instr(subfze); n64=1;break;
 5221|  			}
 5222|  			if (rc) {
 5223|  				switch (xo) {
 5224|  				case PPC_31_ADD:
 5225|  					ic->f = instr(add_dot); break;
 5226|  				case PPC_31_ADDE:
 5227|  					ic->f = instr(adde_dot); break;
 5228|  				case PPC_31_ADDME:
 5229|  					ic->f = instr(addme_dot); break;
 5230|  				case PPC_31_ADDZE:
 5231|  					ic->f = instr(addze_dot); break;
 5232|  				case PPC_31_DIVW:
 5233|  					ic->f = instr(divw_dot); break;
 5234|  				case PPC_31_DIVWU:
 5235|  					ic->f = instr(divwu_dot); break;
 5236|  				case PPC_31_MULLW:
 5237|  					ic->f = instr(mullw_dot); break;
 5238|  				case PPC_31_MULHW:
 5239|  					ic->f = instr(mulhw_dot); break;
 5240|  				case PPC_31_MULHWU:
 5241|  					ic->f = instr(mulhwu_dot); break;
 5242|  				case PPC_31_SUBF:
 5243|  					ic->f = instr(subf_dot); break;
 5244|  				case PPC_31_SUBFC:
 5245|  					ic->f = instr(subfc_dot); break;
 5246|  				case PPC_31_SUBFE:
 5247|  					ic->f = instr(subfe_dot); break;
 5248|  				case PPC_31_SUBFME:
 5249|  					ic->f = instr(subfme_dot); break;
 5250|  				case PPC_31_SUBFZE:
 5251|  					ic->f = instr(subfze_dot); break;
 5252|  				default:if (!cpu->translation_readahead)
 5253|  						fatal("RC bit not yet "
 5254|  						    "implemented\n");
 5255|  					goto bad;
 5256|  				}
 5257|  			}
 5258|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5259|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5260|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 5261|  			if (cpu->cd.ppc.bits == 64 && n64) {
 5262|  				if (!cpu->translation_readahead)
 5263|  					fatal("Not yet for 64-bit mode\n");
 5264|  				goto bad;
 5265|  			}
 5266|  			break;
 5267|  
 5268|  		case PPC_31_LVX:
 5269|  		case PPC_31_LVXL:
 5270|  		case PPC_31_STVX:
 5271|* 		case PPC_31_STVXL:
 5272|  			load = 0;
 5273|  			switch (xo) {
 5274|  			case PPC_31_LVX:
 5275|  			case PPC_31_LVXL:
 5276|  				load = 1; break;
 5277|  			}
 5278|  			rs = (iword >> 21) & 31;
 5279|  			ra = (iword >> 16) & 31;
 5280|  			rb = (iword >> 11) & 31;
 5281|  			ic->arg[0] = rs;
 5282|  			if (ra == 0)
 5283|  				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 5284|  			else
 5285|  				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5286|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5287|  			ic->f = load? instr(lvx) : instr(stvx);
 5288|  			break;
 5289|  
 5290|  		default:goto bad;
 5291|  		}
 5292|  		break;
 5293|  
 5294|  	case PPC_HI6_59:
 5295|  		xo = (iword >>  1) & 1023;
 5296|  		rt = (iword >> 21) & 31;
 5297|  		ra = (iword >> 16) & 31;
 5298|  		rb = (iword >> 11) & 31;
 5299|  		rs = (iword >>  6) & 31;	/*  actually frc  */
 5300|  		rc = iword & 1;
 5301|  
 5302|  		/*
 5303|  		 *  #326: Rc=1 no longer stops the emulator. Each case below
 5304|  		 *  sets rc_f to its record-form twin, and the substitution is
 5305|  		 *  applied once, after the switch. A case that forgets to set
 5306|  		 *  rc_f leaves it NULL and still reaches `goto bad` -- so a
 5307|  		 *  missed record form stays a loud halt rather than becoming a
 5308|  		 *  silent no-op that executes but never writes CR1. (The
 5309|  		 *  integer block uses the same rc_f shape with no such guard.)
 5310|  		 */
 5311|  		rc_f = NULL;
 5312|  
 5313|  		/*  NOTE: Some floating-point instructions are selected
 5314|  		    using only the lowest 5 bits, not all 10!  */
 5315|  		switch (xo & 31) {
 5316|  		case PPC_59_FDIVS:
 5317|  		case PPC_59_FSUBS:
 5318|  		case PPC_59_FADDS:
 5319|  			switch (xo & 31) {
 5320|  			case PPC_59_FDIVS: ic->f = instr(fdivs); rc_f = instr(fdivs_dot); break;
 5321|  			case PPC_59_FSUBS: ic->f = instr(fsubs); rc_f = instr(fsubs_dot); break;
 5322|  			case PPC_59_FADDS: ic->f = instr(fadds); rc_f = instr(fadds_dot); break;
 5323|  			}
 5324|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5325|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rb]);
 5326|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5327|  			break;
 5328|  		case PPC_59_FMULS:
 5329|  			ic->f = instr(fmuls); rc_f = instr(fmuls_dot);
 5330|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5331|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
     | [... lines 5332-5521 not shown ...]
 5522|  				 *  source and nowhere else; masking it would
 5523|  				 *  break a legitimate write.
 5524|  				 */
 5525|  				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
 5526|  				    PPC_FPSCR_VX);
 5527|  				break;
 5528|  			default:goto bad;
 5529|  			}
 5530|  		}
 5531|  		/*
 5532|  		 *  #326: apply the record form. The NULL guard keeps the
 5533|  		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
 5534|  		 *  rejected when their low bit is set, because that is a
 5535|  		 *  reserved encoding and not a record form.
 5536|  		 */
 5537|  		if (rc) {
 5538|  			if (rc_f == NULL)
 5539|  				goto bad;
 5540|  			ic->f = rc_f;
 5541|  		}
 5542|  		break;
 5543|  
 5544|  	default:goto bad;
 5545|  	}
 5546|  
 5547|  
 5548|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5549|  #include "cpu_dyntrans.c"
 5550|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5551|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "\t\tcase PPC_31_STVXL:\n\t\t\tload = 0;\n\t\t\tswitch (xo) {\n\t\t\tcase PPC_31_LVX:",
    "new": "\t\tcase 470: /* #310: dcbi - missing priv check */\n\t\t\tbreak;\n\n\t\tcase PPC_31_STVXL:\n\t\t\tload = 0;\n\t\t\tswitch (xo) {\n\t\t\tcase PPC_31_LVX:",
    "why": "Stubs out dcbi (xo 470) to prevent CPU-STOP, but cannot implement the proper user-mode privilege exception without the relevant headers."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCDCBIUNDEC: DEFECT, 2 FINDINGS
1. The diff does not remove the entire defect. While it prevents `dcbi` (470) from falling through to `goto bad` (removing the CPU-STOP), it fails to implement the privilege check in user mode, merely adding a comment acknowledging the omission. 
2. YES. The added `break;` at line 5272 intercepts the intended fall-through for `PPC_31_LVX`, `PPC_31_LVXL`, and `PPC_31_STVX`. It causes these three opcodes to completely skip their decoding logic (lines 5275-5290), skipping the common tail line `ic->f = load? instr(lvx) : instr(stvx);` (line 5290).
3. UNSETTLED. The function `X(to_be_translated)` has no return statements in the provided snippet, and its return type is obscured by the macro definition and the trailing `#include "cpu_dyntrans.c"`.
4. The diff completely breaks the emulation of three previously working instructions (`LVX`, `LVXL`, `STVX`). Because their decode logic is now skipped, `ic->f` is never assigned, leaving their function pointers uninitialized or retaining previous state.
5. The added comment `/* #310: dcbi - missing priv check */` correctly uses the required `/* #NNN: ... */` format idiom.
src/cpus/cpu_ppc_instr.c:5272, DEFECT, move the `case 470: break;` block to after line 5291 so it does not intercept the vector load/store fall-through logic.
src/cpus/cpu_ppc_instr.c:5271, DEFECT, add the actual user-mode privilege check logic instead of just a comment and a no-op `break`.
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

End with two lines: `REVISION_PPCDCBIUNDEC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCDCBIUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
