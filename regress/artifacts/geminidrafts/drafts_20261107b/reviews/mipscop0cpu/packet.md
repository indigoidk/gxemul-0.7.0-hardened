# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipscop0cpu` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipscop0cpu`, state `open`)

**title:** cpus/cpu_mips_instr.c COP0-function default arm (#236) -- raises RI without the CU0 check, so user mode gets RI instead of Coprocessor Unusable, and prints an unlatched `fatal()` on every translation -- WRONG-RESULT (+ log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T23 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A2-64).  Source URLs: https://github.com/rpajarola/gxemul/commit/12306ee4747fd15a0c67cb2ecc3318ff2f7256d4.  Our site at de8c7547: src/cpus/cpu_mips_instr.c:4930-4938.  Portable fix: yes -- port rpajarola 12306ee (cop0 part).  Filing check (TRIAGE.md): `mipscop0tail` covers only the goto-bad arms.  Not a duplicate of `mipscop0tail` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_mips_instr.c:4937 ic->f = instr(reserved);

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..9caab5df 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -4927,15 +4927,16 @@ X(to_be_translated)
 				} else
 					goto bad;
 				break;
-			default:if (!cpu->translation_readahead)
-					fatal("UNIMPLEMENTED cop0 (func "
-					    "0x%02x)\n", iword & 0xff);
-				/*  #236: A reserved/unimplemented COP0 function
-				    is a Reserved Instruction on real MIPS, not a
-				    reason to halt the host; raise RI instead of
-				    "goto bad" (cpu->running = 0).  */
-				ic->f = instr(reserved);
-				break;
+			default:
+				{
+					static int warned = 0;
+					if (!warned && !cpu->translation_readahead) {
+						fatal("UNIMPLEMENTED cop0 (func "
+						    "0x%02x)\n", iword & 0xff);
+						warned = 1;
+					}
+				}
+				goto bad;
 			}
 			break;
 		}
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 4270-5806 (`+` marks a line the diff added or the point of a deletion)

```c
 4270|  X(to_be_translated)
 4271|  {
 4272|  	uint64_t addr, low_pc;
 4273|  	uint32_t iword, imm;
 4274|  	unsigned char *page;
     | [... lines 4275-4819 not shown ...]
 4820|  		switch (main_opcode) {
 4821|  		case HI6_J:
 4822|  			ic->f = instr(j);
 4823|  			if (cpu->translation_readahead > 2)
 4824|  				cpu->translation_readahead = 2;
 4825|  			break;
 4826|  		case HI6_JAL:
 4827|  			if (cpu->machine->show_trace_tree)
 4828|  				ic->f = instr(jal_trace);
 4829|  			else
 4830|  				ic->f = instr(jal);
 4831|  			break;
 4832|  		}
 4833|  		ic->arg[0] = (iword & 0x03ffffff) << 2;
 4834|  		ic->arg[1] = (addr & 0xffc) + 8;
 4835|  		if (cpu->delay_slot) {
 4836|  			if (!cpu->translation_readahead)
 4837|  				fatal("TODO: branch in delay slot (=%i)? (3);"
 4838|  				    " addr=%016" PRIx64" iword=%08" PRIx32"\n",
 4839|  				    cpu->delay_slot, (uint64_t)addr, iword);
 4840|  			goto bad;
 4841|  		}
 4842|  		break;
 4843|  
 4844|  	case HI6_COP0:
 4845|  		/*  TODO: Is checking bit 25 enough, or perhaps all bits
 4846|  		    25..21 must be checked?  */
 4847|  		if ((iword >> 25) & 1) {
 4848|  			ic->arg[2] = addr & 0xffc;
 4849|  			switch (iword & 0xff) {
 4850|  			case COP0_TLBR:
 4851|  				ic->f = instr(tlbr);
 4852|  				break;
 4853|  			case COP0_TLBWI:
 4854|  			case COP0_TLBWR:
 4855|  				ic->f = instr(tlbw);
 4856|  				ic->arg[0] = (iword & 0xff) == COP0_TLBWR;
 4857|  				break;
 4858|  			case COP0_TLBP:
 4859|  				ic->f = instr(tlbp);
 4860|  				break;
 4861|  			case COP0_RFE:
 4862|  				ic->f = instr(rfe);
 4863|  				break;
 4864|  			case COP0_ERET:
 4865|  				/*  #231: (panel: Codex/Fable/agy/Ollama) ERET is
 4866|  				    MIPS-III+; on an R3000 (EXC3K) that encoding is
 4867|  				    Reserved -> RI. Decode-gate mirrors the WAIT/STANDBY
 4868|  				    pattern below; X(reserved) does the PC-sync + RI.  */
 4869|  				ic->f = cpu->cd.mips.cpu_type.exc_model == EXC3K?
 4870|  				    instr(reserved) : instr(eret);
 4871|  				break;
 4872|  			case COP0_DERET:
 4873|  				ic->f = instr(deret);
 4874|  				break;
 4875|  			case COP0_WAIT:
 4876|  				ic->f = instr(wait);
 4877|  				if (cpu->cd.mips.cpu_type.rev != MIPS_RM5200 &&
 4878|  				    cpu->cd.mips.cpu_type.isa_level < 32) {
 4879|  					static int warned = 0;
 4880|  					ic->f = instr(reserved);
 4881|  					if (!warned &&
 4882|  					    !cpu->translation_readahead) {
 4883|  						fatal("{ WARNING: Attempt to "
 4884|  						    "execute the WAIT instruct"
 4885|  					            "ion, but the emulated CPU "
 4886|  						    "is neither RM52xx, nor "
 4887|  						    "MIPS32/64! }\n");
 4888|  						warned = 1;
 4889|  					}
 4890|  				}
 4891|  				break;
 4892|  			case COP0_STANDBY:
 4893|  			case COP0_SUSPEND:
 4894|  			case COP0_HIBERNATE:
 4895|  				/*  #237: STANDBY/SUSPEND/HIBERNATE are VR41xx
 4896|  				    (R4100) power-management instructions. Treat
 4897|  				    them as idle ('wait') only on the R4100; on
 4898|  				    every other CPU (including the R3000/R4000
 4899|  				    audit targets) they are Reserved Instructions
 4900|  				    -> RI, not a host halt. Previously HIBERNATE
 4901|  				    did "goto bad" (running = 0) and SUSPEND did
 4902|  				    an unconditional reboot at any PC.  */
 4903|  				/*  NOTE: Reusing the 'wait' instruction:  */
 4904|  				ic->f = instr(wait);
 4905|  				if (cpu->cd.mips.cpu_type.rev != MIPS_R4100) {
 4906|  					static int warned = 0;
 4907|  					ic->f = instr(reserved);
 4908|  					if (!warned &&
 4909|  					    !cpu->translation_readahead) {
 4910|  						fatal("{ WARNING: Attempt to "
 4911|  						    "execute a R41xx instruct"
 4912|  					            "ion, but the emulated CPU "
 4913|  						    "doesn't support it! }\n");
 4914|  						warned = 1;
 4915|  					}
 4916|  				}
 4917|  				break;
 4918|  			case COP0_EI:
 4919|  				if (cpu->cd.mips.cpu_type.rev == MIPS_R5900) {
 4920|  					ic->f = instr(ei_r5900);
 4921|  				} else
 4922|  					goto bad;
 4923|  				break;
 4924|  			case COP0_DI:
 4925|  				if (cpu->cd.mips.cpu_type.rev == MIPS_R5900) {
 4926|  					ic->f = instr(di_r5900);
 4927|  				} else
 4928|  					goto bad;
 4929|  				break;
 4930|+ 			default:
 4931|+ 				{
 4932|+ 					static int warned = 0;
 4933|+ 					if (!warned && !cpu->translation_readahead) {
 4934|+ 						fatal("UNIMPLEMENTED cop0 (func "
 4935|+ 						    "0x%02x)\n", iword & 0xff);
 4936|+ 						warned = 1;
 4937|+ 					}
 4938|+ 				}
 4939|+ 				goto bad;
 4940|  			}
 4941|  			break;
 4942|  		}
 4943|  
 4944|  		/*  rs contains the coprocessor opcode!  */
 4945|  		switch (rs) {
 4946|  		case COPz_CFCz:
 4947|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4948|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4949|  			ic->arg[2] = addr & 0xffc;
 4950|  			ic->f = instr(cfc0);
 4951|  			if (rt == MIPS_GPR_ZERO)
 4952|  				ic->f = instr(nop);
 4953|  			break;
 4954|  		case COPz_MFCz:
 4955|  		case COPz_DMFCz:
 4956|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4957|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4958|  			ic->arg[2] = addr & 0xffc;
 4959|  			ic->f = rs == COPz_MFCz? instr(mfc0) : instr(dmfc0);
 4960|  			if (rs == COPz_MFCz && (iword & 7) == 0 &&
 4961|  			    rd != COP0_COUNT)
 4962|  				ic->f = instr(mfc0_select0);
 4963|  			if (rs == COPz_DMFCz && (iword & 7) == 0 &&
 4964|  			    rd != COP0_COUNT)
 4965|  				ic->f = instr(dmfc0_select0);
 4966|  			if (rt == MIPS_GPR_ZERO)
 4967|  				ic->f = instr(nop);
 4968|  			break;
 4969|  		case COPz_MTCz:
 4970|  		case COPz_DMTCz:
 4971|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4972|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4973|  			ic->arg[2] = addr & 0xffc;
 4974|  			ic->f = rs == COPz_MTCz? instr(mtc0) : instr(dmtc0);
 4975|  
 4976|  			if (cpu->cd.mips.cpu_type.exc_model == EXC3K &&
 4977|  			    rs == COPz_MTCz && rd == COP0_STATUS)
 4978|  				cpu->cd.mips.combination_check =
 4979|  				    COMBINE(netbsd_r3k_cache_inv);
 4980|  
 4981|  			break;
 4982|  		case COPz_MFMCz:
 4983|  			if ((iword & 0xffdf) == 0x6000) {
 4984|  				/*  MIPS32/64 rev 2 "ei" or "di":   */
 4985|  				if (cpu->cd.mips.cpu_type.isa_level < 32 ||
 4986|  				    cpu->cd.mips.cpu_type.isa_revision < 2) {
 4987|  					static int warning_ei_di = 0;
 4988|  					if (!warning_ei_di &&
 4989|  					    !cpu->translation_readahead) {
 4990|  						fatal("[ WARNING! MIPS32/64 "
 4991|  						    "revision 2 di or ei opcode"
 4992|  						    " used, but the %s process"
 4993|  						    "or does not implement "
 4994|  						    "such instructions. Only "
 4995|  						    "printing this "
 4996|  						    "warning once. ]\n",
 4997|  						    cpu->cd.mips.cpu_type.name);
 4998|  						warning_ei_di = 1;
 4999|  					}
     | [... lines 5000-5776 not shown ...]
 5777|  		ic->f = instr(cache);
 5778|  		break;
 5779|  
 5780|  	default:goto bad;
 5781|  	}
 5782|  
 5783|  
 5784|  #ifdef MODE32
 5785|  	if (x64) {
 5786|  		static int has_warned = 0;
 5787|  		if (!has_warned && !cpu->translation_readahead) {
 5788|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5789|  			    " instruction on an emulated 32-bit processor; "
 5790|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5791|  			has_warned = 1;
 5792|  		}
 5793|  		if (cpu->translation_readahead)
 5794|  			goto bad;
 5795|  		else
 5796|  			ic->f = instr(reserved);
 5797|  	}
 5798|  #else
 5799|  	(void)x64; // avoid compiler warning
 5800|  #endif
 5801|  
 5802|  
 5803|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5804|  #include "cpu_dyntrans.c" 
 5805|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5806|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSCOP0CPU: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSCOP0CPU: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
