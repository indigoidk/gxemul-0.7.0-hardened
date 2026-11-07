# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcmtmsrlbit` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcmtmsrlbit`, state `open`)

**title:** src/cpus/cpu_ppc_instr.c:4733-4741 -- mtmsr/mtmsrd with the L bit set print `TODO: mtmsr l-bit` and reach `goto bad` where Book III defines L=1 -- CPU-STOP (any privilege: no MSR[PR] test in the decoder)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc_instr.c` -- AT HEAD, lines 4084-5551 (`*` marks a line your previous draft changed)

```c
 4084|  X(to_be_translated)
 4085|  {
 4086|  	uint64_t addr, low_pc, tmp_addr;
 4087|  	uint32_t iword, mask;
 4088|  	unsigned char *page;
     | [... lines 4089-4715 not shown ...]
 4716|  			case PPC_30_RLDICR: ic->f = instr(rldicr); break;
 4717|  			case PPC_30_RLDIMI: ic->f = instr(rldimi); break;
 4718|  			}
 4719|  			ic->arg[0] = iword;
 4720|  			if (cpu->cd.ppc.bits == 32) {
 4721|  				if (!cpu->translation_readahead)
 4722|  					fatal("TODO: rld* in 32-bit mode?\n");
 4723|  				goto bad;
 4724|  			}
 4725|  			break;
 4726|  
 4727|  		default:goto bad;
 4728|  		}
 4729|  		break;
 4730|  
 4731|  	case PPC_HI6_31:
 4732|  		xo = (iword >> 1) & 1023;
 4733|  		switch (xo) {
 4734|  
 4735|  		case PPC_31_CMPL:
 4736|  		case PPC_31_CMP:
 4737|  			bf = (iword >> 23) & 7;
 4738|  			l_bit = (iword >> 21) & 1;
 4739|  			ra = (iword >> 16) & 31;
 4740|  			rb = (iword >> 11) & 31;
 4741|  			if (xo == PPC_31_CMPL) {
 4742|  				if (l_bit)
 4743|  					ic->f = instr(cmpld);
 4744|  				else
 4745|  					ic->f = instr(cmplw);
 4746|  			} else {
 4747|  				if (l_bit)
 4748|  					ic->f = instr(cmpd);
 4749|  				else {
 4750|  					if (bf == 0)
 4751|  						ic->f = instr(cmpw_cr0);
 4752|  					else
 4753|  						ic->f = instr(cmpw);
 4754|  				}
 4755|  			}
 4756|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4757|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 4758|  			ic->arg[2] = 28 - 4*bf;
 4759|  			break;
 4760|  
 4761|  		case PPC_31_CNTLZW:
 4762|  			rs = (iword >> 21) & 31;
 4763|  			ra = (iword >> 16) & 31;
 4764|  			rc = iword & 1;
 4765|  			if (rc) {
 4766|  				if (!cpu->translation_readahead)
 4767|  					fatal("TODO: rc\n");
 4768|  				goto bad;
 4769|  			}
 4770|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4771|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4772|  			ic->f = instr(cntlzw);
 4773|  			break;
 4774|  
 4775|  		case PPC_31_MFSPR:
 4776|  			rt = (iword >> 21) & 31;
 4777|  			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
 4778|  			debug_spr_usage(cpu->pc, spr);
 4779|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4780|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.spr[spr]);
 4781|  			switch (spr) {
 4782|  			// Reuse SPR_TB* for TBR_TB*:
 4783|  			case TBR_TBL: ic->f = instr(mftb); break;
 4784|  			case TBR_TBU: ic->f = instr(mftbu); break;
 4785|  			case SPR_PMC1:	ic->f = instr(mfspr_pmc1); break;
 4786|  			default:	ic->f = instr(mfspr);
 4787|  			}
 4788|  			break;
 4789|  
 4790|  		case PPC_31_MTSPR:
 4791|  			rs = (iword >> 21) & 31;
 4792|  			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
 4793|  			debug_spr_usage(cpu->pc, spr);
 4794|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4795|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.spr[spr]);
 4796|  			switch (spr) {
 4797|  			case SPR_LR:
 4798|  				ic->f = instr(mtlr);
 4799|  				break;
 4800|  			case SPR_CTR:
 4801|  				ic->f = instr(mtctr);
 4802|  				break;
 4803|  			case SPR_SPRG2:
 4804|  				ic->f = instr(mtspr_sprg2);
 4805|  				break;
 4806|  			default:ic->f = instr(mtspr);
 4807|  			}
 4808|  			break;
 4809|  
 4810|  		case PPC_31_MFCR:
 4811|  			rt = (iword >> 21) & 31;
 4812|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4813|  			ic->f = instr(mfcr);
 4814|  			break;
 4815|  
 4816|  		case PPC_31_MFMSR:
 4817|  			rt = (iword >> 21) & 31;
 4818|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4819|  			ic->f = instr(mfmsr);
 4820|  			break;
 4821|  
 4822|  		case PPC_31_MTMSR:
 4823|  		case PPC_31_MTMSRD:
 4824|  			rs = (iword >> 21) & 31;
 4825|  			l_bit = (iword >> 16) & 1;
 4826|* 			if (l_bit) {
 4827|* 				if (!cpu->translation_readahead)
 4828|* 					fatal("TODO: mtmsr l-bit\n");
 4829|* 				goto bad;
 4830|* 			}
 4831|* 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4832|  			ic->arg[1] = (addr & 0xfff) + 4;
 4833|  			ic->arg[2] = xo == PPC_31_MTMSRD;
 4834|  			ic->f = instr(mtmsr);
 4835|  			break;
 4836|  
 4837|  		case PPC_31_MTCRF:
 4838|  			rs = (iword >> 21) & 31;
 4839|  			{
 4840|  				int i, fxm = (iword >> 12) & 255;
 4841|  				uint32_t tmp = 0;
 4842|  				for (i=0; i<8; i++, fxm <<= 1) {
 4843|  					tmp <<= 4;
 4844|  					if (fxm & 128)
 4845|  						tmp |= 0xf;
 4846|  				}
 4847|  				ic->arg[1] = (uint32_t)tmp;
 4848|  			}
 4849|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4850|  			ic->f = instr(mtcrf);
 4851|  			break;
 4852|  
 4853|  		case PPC_31_MFSRIN:
 4854|  		case PPC_31_MTSRIN:
 4855|  			rt = (iword >> 21) & 31;
 4856|  			rb = (iword >> 11) & 31;
 4857|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 4858|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4859|  			switch (xo) {
 4860|  			case PPC_31_MFSRIN: ic->f = instr(mfsrin); break;
 4861|  			case PPC_31_MTSRIN: ic->f = instr(mtsrin); break;
 4862|  			}
 4863|  			if (cpu->cd.ppc.bits == 64) {
 4864|  				if (!cpu->translation_readahead)
 4865|  					fatal("Not yet for 64-bit mode\n");
 4866|  				goto bad;
 4867|  			}
 4868|  			break;
 4869|  
 4870|  		case PPC_31_MFSR:
 4871|  		case PPC_31_MTSR:
 4872|  			rt = (iword >> 21) & 31;
 4873|  			ic->arg[0] = (iword >> 16) & 15;
 4874|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4875|  			switch (xo) {
 4876|  			case PPC_31_MFSR:   ic->f = instr(mfsr); break;
 4877|  			case PPC_31_MTSR:   ic->f = instr(mtsr); break;
 4878|  			}
 4879|  			if (cpu->cd.ppc.bits == 64) {
 4880|  				if (!cpu->translation_readahead)
 4881|  					fatal("Not yet for 64-bit mode\n");
 4882|  				goto bad;
 4883|  			}
 4884|  			break;
 4885|  
 4886|  		case PPC_31_SRAWI:
 4887|  			rs = (iword >> 21) & 31;
 4888|  			ra = (iword >> 16) & 31;
 4889|  			sh = (iword >> 11) & 31;
 4890|  			rc = iword & 1;
 4891|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
     | [... lines 4892-5521 not shown ...]
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
    "old": "\t\t\tl_bit = (iword >> 16) & 1;\n\t\t\tif (l_bit) {\n\t\t\t\tif (!cpu->translation_readahead)\n\t\t\t\t\tfatal(\"TODO: mtmsr l-bit\\n\");\n\t\t\t\tgoto bad;\n\t\t\t}",
    "new": "\t\t\tl_bit = (iword >> 16) & 1;\n\t\t\t/* #ppcmtmsrlbit: defer to executor to ensure MSR[PR] privilege check */",
    "why": "Remove decoder-level CPU-STOP on L=1; allows the executor to perform the required privilege checks first."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCMTMSRLBIT: DEFECT, 1 FINDINGS
1. The diff successfully removes the defect from `mtmsr/mtmsrd` at lines 4822-4831. It misses the exact site named in the issue (`src/cpus/cpu_ppc_instr.c:4733-4741`), but that is because lines 4733-4741 in the current code handle `PPC_31_CMP` and `PPC_31_CMPL`, which is an issue-description line number mismatch, not a missed fix.
2. The diff adds no `return`, `goto`, `break`, or early exit. Instead, it *removes* the `goto bad;`, meaning the function no longer skips its common tail (e.g., `src/cpus/cpu_ppc_instr.c:5545` `#include "cpu_dyntrans.c"`). 
3. Because the code no longer branches to `bad`, it falls through and continues building the translation. The precise return value is UNSETTLED because neither the function signature nor `cpu_dyntrans.c` are shown, but it implies a successful instruction translation instead of an error/abort.
4. Beyond removing the defect and suppressing the `TODO` message, the diff changes the emulator's state by actually populating `ic->arg[0]`, `ic->arg[1]`, `ic->arg[2]`, and `ic->f = instr(mtmsr);` for the `l_bit == 1` path. It successfully leaves alone every guest CPU state it touches here, as it only reads fields and takes the address of `gpr` and `spr` pointers for deferred execution.
5. House idioms: The new comment successfully carries the `/* #ppcmtmsrlbit: ... */` tag idiom, but it violates the 79-column limit (it spans ~97 columns when accounting for the 3 leading tabs).
**Claim Refutations:**
* Claim: `src/cpus/cpu_ppc_instr.c:4733-4741 -- mtmsr/mtmsrd with the L bit set print TODO: mtmsr l-bit and reach goto bad` -> BROKEN. In the post-edit code, lines 4733-4741 evaluate `CMP`/`CMPL` logic, not `mtmsr`.
* Claim: `where Book III defines L=1 -- CPU-STOP (any privilege: no MSR[PR] test in the decoder)` -> UNSETTLED. Book III architecture documentation is outside the bounds of this review.
* Claim: `The drafter's own reading: STILL PRESENT: YES -- 4826: if (l_bit) {` -> BROKEN. In the post-edit text, line 4826 contains the newly added comment, not the `if (l_bit)` check.
**Findings:**
`src/cpus/cpu_ppc_instr.c:4826` STYLE split the comment across two lines to stay within 79 columns
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

End with two lines: `REVISION_PPCMTMSRLBIT: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCMTMSRLBIT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
