# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcmtmsrlbit` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcmtmsrlbit`, state `open`)

**title:** src/cpus/cpu_ppc_instr.c:4733-4741 -- mtmsr/mtmsrd with the L bit set print `TODO: mtmsr l-bit` and reach `goto bad` where Book III defines L=1 -- CPU-STOP (any privilege: no MSR[PR] test in the decoder)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 4826: 			if (l_bit) {

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..e4dc0d45 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -4823,11 +4823,10 @@ X(to_be_translated)
 		case PPC_31_MTMSRD:
 			rs = (iword >> 21) & 31;
 			l_bit = (iword >> 16) & 1;
-			if (l_bit) {
-				if (!cpu->translation_readahead)
-					fatal("TODO: mtmsr l-bit\n");
-				goto bad;
-			}
+			/*
+			 * #ppcmtmsrlbit: defer to executor to ensure MSR[PR]
+			 * privilege check
+			 */
 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 			ic->arg[1] = (addr & 0xfff) + 4;
 			ic->arg[2] = xo == PPC_31_MTMSRD;
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 4084-5550 (`+` marks a line the diff added or the point of a deletion)

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
 4826|+ 			/*
 4827|+ 			 * #ppcmtmsrlbit: defer to executor to ensure MSR[PR]
 4828|+ 			 * privilege check
 4829|+ 			 */
 4830|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4831|  			ic->arg[1] = (addr & 0xfff) + 4;
 4832|  			ic->arg[2] = xo == PPC_31_MTMSRD;
 4833|  			ic->f = instr(mtmsr);
 4834|  			break;
 4835|  
 4836|  		case PPC_31_MTCRF:
 4837|  			rs = (iword >> 21) & 31;
 4838|  			{
 4839|  				int i, fxm = (iword >> 12) & 255;
 4840|  				uint32_t tmp = 0;
 4841|  				for (i=0; i<8; i++, fxm <<= 1) {
 4842|  					tmp <<= 4;
 4843|  					if (fxm & 128)
 4844|  						tmp |= 0xf;
 4845|  				}
 4846|  				ic->arg[1] = (uint32_t)tmp;
 4847|  			}
 4848|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4849|  			ic->f = instr(mtcrf);
 4850|  			break;
 4851|  
 4852|  		case PPC_31_MFSRIN:
 4853|  		case PPC_31_MTSRIN:
 4854|  			rt = (iword >> 21) & 31;
 4855|  			rb = (iword >> 11) & 31;
 4856|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 4857|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4858|  			switch (xo) {
 4859|  			case PPC_31_MFSRIN: ic->f = instr(mfsrin); break;
 4860|  			case PPC_31_MTSRIN: ic->f = instr(mtsrin); break;
 4861|  			}
 4862|  			if (cpu->cd.ppc.bits == 64) {
 4863|  				if (!cpu->translation_readahead)
 4864|  					fatal("Not yet for 64-bit mode\n");
 4865|  				goto bad;
 4866|  			}
 4867|  			break;
 4868|  
 4869|  		case PPC_31_MFSR:
 4870|  		case PPC_31_MTSR:
 4871|  			rt = (iword >> 21) & 31;
 4872|  			ic->arg[0] = (iword >> 16) & 15;
 4873|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4874|  			switch (xo) {
 4875|  			case PPC_31_MFSR:   ic->f = instr(mfsr); break;
 4876|  			case PPC_31_MTSR:   ic->f = instr(mtsr); break;
 4877|  			}
 4878|  			if (cpu->cd.ppc.bits == 64) {
 4879|  				if (!cpu->translation_readahead)
 4880|  					fatal("Not yet for 64-bit mode\n");
 4881|  				goto bad;
 4882|  			}
 4883|  			break;
 4884|  
 4885|  		case PPC_31_SRAWI:
 4886|  			rs = (iword >> 21) & 31;
 4887|  			ra = (iword >> 16) & 31;
 4888|  			sh = (iword >> 11) & 31;
 4889|  			rc = iword & 1;
     | [... lines 4890-5520 not shown ...]
 5521|  				 *  source and nowhere else; masking it would
 5522|  				 *  break a legitimate write.
 5523|  				 */
 5524|  				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
 5525|  				    PPC_FPSCR_VX);
 5526|  				break;
 5527|  			default:goto bad;
 5528|  			}
 5529|  		}
 5530|  		/*
 5531|  		 *  #326: apply the record form. The NULL guard keeps the
 5532|  		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
 5533|  		 *  rejected when their low bit is set, because that is a
 5534|  		 *  reserved encoding and not a record form.
 5535|  		 */
 5536|  		if (rc) {
 5537|  			if (rc_f == NULL)
 5538|  				goto bad;
 5539|  			ic->f = rc_f;
 5540|  		}
 5541|  		break;
 5542|  
 5543|  	default:goto bad;
 5544|  	}
 5545|  
 5546|  
 5547|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5548|  #include "cpu_dyntrans.c"
 5549|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5550|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCMTMSRLBIT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCMTMSRLBIT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
