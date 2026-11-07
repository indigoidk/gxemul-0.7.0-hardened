# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipscop0cpu` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipscop0cpu`, state `open`)

**title:** cpus/cpu_mips_instr.c COP0-function default arm (#236) -- raises RI without the CU0 check, so user mode gets RI instead of Coprocessor Unusable, and prints an unlatched `fatal()` on every translation -- WRONG-RESULT (+ log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T23 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A2-64).  Source URLs: https://github.com/rpajarola/gxemul/commit/12306ee4747fd15a0c67cb2ecc3318ff2f7256d4.  Our site at de8c7547: src/cpus/cpu_mips_instr.c:4930-4938.  Portable fix: yes -- port rpajarola 12306ee (cop0 part).  Filing check (TRIAGE.md): `mipscop0tail` covers only the goto-bad arms.  Not a duplicate of `mipscop0tail` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_mips_instr.c` -- AT HEAD, lines 4270-5805 (`*` marks a line your previous draft changed)

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
 4930|* 			default:if (!cpu->translation_readahead)
 4931|* 					fatal("UNIMPLEMENTED cop0 (func "
 4932|* 					    "0x%02x)\n", iword & 0xff);
 4933|* 				/*  #236: A reserved/unimplemented COP0 function
 4934|  				    is a Reserved Instruction on real MIPS, not a
 4935|  				    reason to halt the host; raise RI instead of
 4936|  				    "goto bad" (cpu->running = 0).  */
 4937|  				ic->f = instr(reserved);
 4938|  				break;
 4939|  			}
 4940|  			break;
 4941|  		}
 4942|  
 4943|  		/*  rs contains the coprocessor opcode!  */
 4944|  		switch (rs) {
 4945|  		case COPz_CFCz:
 4946|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4947|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4948|  			ic->arg[2] = addr & 0xffc;
 4949|  			ic->f = instr(cfc0);
 4950|  			if (rt == MIPS_GPR_ZERO)
 4951|  				ic->f = instr(nop);
 4952|  			break;
 4953|  		case COPz_MFCz:
 4954|  		case COPz_DMFCz:
 4955|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4956|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4957|  			ic->arg[2] = addr & 0xffc;
 4958|  			ic->f = rs == COPz_MFCz? instr(mfc0) : instr(dmfc0);
 4959|  			if (rs == COPz_MFCz && (iword & 7) == 0 &&
 4960|  			    rd != COP0_COUNT)
 4961|  				ic->f = instr(mfc0_select0);
 4962|  			if (rs == COPz_DMFCz && (iword & 7) == 0 &&
 4963|  			    rd != COP0_COUNT)
 4964|  				ic->f = instr(dmfc0_select0);
 4965|  			if (rt == MIPS_GPR_ZERO)
 4966|  				ic->f = instr(nop);
 4967|  			break;
 4968|  		case COPz_MTCz:
 4969|  		case COPz_DMTCz:
 4970|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4971|  			ic->arg[1] = rd + ((iword & 7) << 5);
 4972|  			ic->arg[2] = addr & 0xffc;
 4973|  			ic->f = rs == COPz_MTCz? instr(mtc0) : instr(dmtc0);
 4974|  
 4975|  			if (cpu->cd.mips.cpu_type.exc_model == EXC3K &&
 4976|  			    rs == COPz_MTCz && rd == COP0_STATUS)
 4977|  				cpu->cd.mips.combination_check =
 4978|  				    COMBINE(netbsd_r3k_cache_inv);
 4979|  
 4980|  			break;
 4981|  		case COPz_MFMCz:
 4982|  			if ((iword & 0xffdf) == 0x6000) {
 4983|  				/*  MIPS32/64 rev 2 "ei" or "di":   */
 4984|  				if (cpu->cd.mips.cpu_type.isa_level < 32 ||
 4985|  				    cpu->cd.mips.cpu_type.isa_revision < 2) {
 4986|  					static int warning_ei_di = 0;
 4987|  					if (!warning_ei_di &&
 4988|  					    !cpu->translation_readahead) {
 4989|  						fatal("[ WARNING! MIPS32/64 "
 4990|  						    "revision 2 di or ei opcode"
 4991|  						    " used, but the %s process"
 4992|  						    "or does not implement "
 4993|  						    "such instructions. Only "
     | [... lines 4994-5775 not shown ...]
 5776|  		ic->f = instr(cache);
 5777|  		break;
 5778|  
 5779|  	default:goto bad;
 5780|  	}
 5781|  
 5782|  
 5783|  #ifdef MODE32
 5784|  	if (x64) {
 5785|  		static int has_warned = 0;
 5786|  		if (!has_warned && !cpu->translation_readahead) {
 5787|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5788|  			    " instruction on an emulated 32-bit processor; "
 5789|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5790|  			has_warned = 1;
 5791|  		}
 5792|  		if (cpu->translation_readahead)
 5793|  			goto bad;
 5794|  		else
 5795|  			ic->f = instr(reserved);
 5796|  	}
 5797|  #else
 5798|  	(void)x64; // avoid compiler warning
 5799|  #endif
 5800|  
 5801|  
 5802|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5803|  #include "cpu_dyntrans.c" 
 5804|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5805|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_mips_instr.c",
    "old": "\t\t\tdefault:if (!cpu->translation_readahead)\n\t\t\t\t\tfatal(\"UNIMPLEMENTED cop0 (func \"\n\t\t\t\t\t    \"0x%02x)\\n\", iword & 0xff);\n\t\t\t\t/*  #236: A reserved/unimplemented COP0 function\n\t\t\t\t    is a Reserved Instruction on real MIPS, not a\n\t\t\t\t    reason to halt the host; raise RI instead of\n\t\t\t\t    \"goto bad\" (cpu->running = 0).  */\n\t\t\t\tic->f = instr(reserved);\n\t\t\t\tbreak;",
    "new": "\t\t\tdefault:\n\t\t\t\t{\n\t\t\t\t\tstatic int warned = 0;\n\t\t\t\t\tif (!warned && !cpu->translation_readahead) {\n\t\t\t\t\t\tfatal(\"UNIMPLEMENTED cop0 (func \"\n\t\t\t\t\t\t    \"0x%02x)\\n\", iword & 0xff);\n\t\t\t\t\t\twarned = 1;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\t/*  #236: A reserved/unimplemented COP0 function\n\t\t\t\t    is a Reserved Instruction on real MIPS, not a\n\t\t\t\t    reason to halt the host; raise RI instead of\n\t\t\t\t    \"goto bad\" (cpu->running = 0).  */\n\t\t\t\tic->f = instr(reserved);\n\t\t\t\tbreak;",
    "why": "Latches the fatal() warning to prevent log flood on every translation, but resolving the CU0 check before RI is unsettled without executor context."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSCOP0CPU: DEFECT, 3 FINDINGS
1. The diff fails to remove the core defect described in the issue ("raises RI without the CU0 check"). It only addresses the "unlatched `fatal()`" log flood, leaving `ic->f = instr(reserved);` which will still unconditionally raise a Reserved Instruction exception instead of Coprocessor Unusable when accessed from user mode.
2. CONTROL FLOW: No. The diff only introduces a block with a static variable and does not alter control flow (no added `return`, `goto`, or `break`).
3. RETURN VALUE: No. The function's return path and value are unchanged.
4. What ELSE: The diff introduces a global `static int warned = 0;` latch. This causes the warning to print only once per emulator process, suppressing the warning for all subsequent device instances/CPUs rather than once per instance. 
5. House idioms: The added warning message does not include the required `(once)` text, and uses a global static latch instead of an instance field.
`src/cpus/cpu_mips_instr.c:4943`: DEFECT, needs to assign an instruction handler that performs a runtime CU0 check (or checks translation-time state) instead of unconditionally using `instr(reserved)`.
`src/cpus/cpu_mips_instr.c:4932`: DEFECT, `static int warned = 0;` should be an instance-level latch (e.g., a flag on the `cpu` struct).
`src/cpus/cpu_mips_instr.c:4934`: STYLE, message string is missing `(once)`.
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

End with two lines: `REVISION_MIPSCOP0CPU: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSCOP0CPU: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
