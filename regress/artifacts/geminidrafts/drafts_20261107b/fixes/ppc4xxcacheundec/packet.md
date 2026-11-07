# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppc4xxcacheundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppc4xxcacheundec`, state `open`)

**title:** src/cpus/cpu_ppc_instr.c:5201 -- dccci and iccci (defined in opcodes_ppc.h, no case) reach the opcode-31 default `goto bad` on the PPC405GP model -- CPU-STOP (PPC405GP only via -C)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc_instr.c` -- AT HEAD, lines 4084-5551 (`*` marks a line your previous draft changed)

```c
 4084|  X(to_be_translated)
 4085|  {
 4086|  	uint64_t addr, low_pc, tmp_addr;
 4087|  	uint32_t iword, mask;
 4088|  	unsigned char *page;
     | [... lines 4089-5179 not shown ...]
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
 5271|  		case PPC_31_STVXL:
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
 5290|* 		default:goto bad;
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
 5332|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rs]); /* frc */
 5333|  			break;
 5334|  		default:/*  Use all 10 bits of xo:  */
 5335|  			switch (xo) {
 5336|  			default:goto bad;
 5337|  			}
 5338|  		}
 5339|  		/*  #326: apply the record form, guarded.  */
 5340|  		if (rc) {
 5341|  			if (rc_f == NULL)
 5342|  				goto bad;
 5343|  			ic->f = rc_f;
 5344|  		}
 5345|  		break;
 5346|  
 5347|  	case PPC_HI6_63:
 5348|  		xo = (iword >>  1) & 1023;
 5349|  		rt = (iword >> 21) & 31;
 5350|  		ra = (iword >> 16) & 31;
     | [... lines 5351-5521 not shown ...]
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
    "old": "\t\tdefault:goto bad;\n\t\t}\n\t\tbreak;\n\n\tcase PPC_HI6_59:",
    "new": "\t\tcase PPC_31_DCCCI:\n\t\tcase PPC_31_ICCCI:\n\t\t\tbreak;\n\t\tdefault:goto bad;\n\t\t}\n\t\tbreak;\n\n\tcase PPC_HI6_59:",
    "why": "Treat PPC405GP cache instructions dccci and iccci as no-ops to avoid CPU halt."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPC4XXCACHEUNDEC: DEFECT, 1 FINDINGS
1. The diff removes the defect at the site named by the drafter (`src/cpus/cpu_ppc_instr.c:5290`), adding the missing cases so they no longer fall through to the `default: goto bad;`.
2. CONTROL FLOW: The added `break;` exits the `switch (xo)` and then hits the `break;` at line 5295 to exit the outer opcode switch. It successfully reaches the COMMON TAIL at `<src/cpus/cpu_ppc_instr.c:5551>`. It does not skip the tail.
3. RETURN VALUE: No return paths are changed; the function does not explicitly return in this block.
4. ELSE: The diff leaves `ic->f` completely unassigned for these instructions, whereas all other valid instruction cases in this function assign `ic->f = instr(...)`. This will cause the emulator to execute whatever function pointer was previously in `ic->f` (or crash if null) when running this block.
5. STYLE: No style violations introduced.
`src/cpus/cpu_ppc_instr.c:5292`: DEFECT: `ic->f` is not assigned for DCCCI/ICCCI, leaving the instruction handler uninitialized. Fix: `ic->f = instr(nop); break;` (or the appropriate cache instruction).
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

End with two lines: `REVISION_PPC4XXCACHEUNDEC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPC4XXCACHEUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR REVISED DRAFT FAILED TO BUILD -- correct it (a build repair, not another review)

```text
tmp_ppc_head.c:42:18: error: 'ppc_instr_dccci' undeclared (first use in this function); did you mean 'ppc_instr_dcbz'?
tmp_ppc_head.c:42:18: error: 'ppc_instr_iccci' undeclared (first use in this function); did you mean 'ppc_instr_bcctr'?
tmp_ppc_tail.c:77:18: error: 'ppc32_instr_dccci' undeclared (first use in this function); did you mean 'ppc32_instr_dcbz'?
```

The build generates `ppc_instr_<name>` from each `X(<name>) { ... }` handler; `instr(dccci)` needs an `X(dccci)` that does not
exist.  THIS FILE'S IDIOM for a cache operation the model does not simulate is to decode it to the existing no-op handler,
shown here from HEAD -- prefer adding the 4xx cases to this group over defining new handlers:

### `src/cpus/cpu_ppc_instr.c` lines 4900-4910 (HEAD)

```c
 4900| 		case PPC_31_SYNC:
 4901| 		case PPC_31_DSSALL:
 4902| 		case PPC_31_EIEIO:
 4903| 		case PPC_31_DCBST:
 4904| 		case PPC_31_DCBTST:
 4905| 		case PPC_31_DCBF:
 4906| 		case PPC_31_DCBT:
 4907| 		case PPC_31_ICBI:
 4908| 			ic->f = instr(nop);
 4909| 			break;
 4910| 
```

### `src/include/opcodes_ppc.h` lines 146-152 (HEAD)

```c
  146| #define	  PPC_31_SLBIE		  434
  147| #define	  PPC_31_STHUX		  439
  148| #define	  PPC_31_OR		  444
  149| #define	  PPC_31_DCCCI		  454
  150| #define	  PPC_31_DIVWU		  459
  151| #define	  PPC_31_MTSPR		  467
  152| #define	  PPC_31_DCBI		  470
```

Your revised edits:

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "\t\tdefault:goto bad;\n\t\t}\n\t\tbreak;\n\n\tcase PPC_HI6_59:",
    "new": "\t\tcase PPC_31_DCCCI:\n\t\t\tic->f = instr(dccci); break;\n\t\tcase PPC_31_ICCCI:\n\t\t\tic->f = instr(iccci); break;\n\t\tdefault:goto bad;\n\t\t}\n\t\tbreak;\n\n\tcase PPC_HI6_59:",
    "why": "Add cases for cache instructions dccci and iccci, assigning the instruction handlers to ic->f to avoid uninitialized execution or halts."
  }
]
```

Return the COMPLETE corrected edit list, then end with `FIXDRAFT_PPC4XXCACHEUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
