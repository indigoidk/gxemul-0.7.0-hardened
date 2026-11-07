# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mipsdsbranch` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mipsdsbranch`, state `open`)

**title:** src/cpus/cpu_mips_instr.c:4644, :4751, :4837, :5054, :5336 -- a branch or jump decoded in a delay slot prints `TODO: branch in delay slot` and reaches goto bad at five sites, where the operation is UNPREDICTABLE and must not halt -- CPU-STOP (any privilege)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_mips_instr.c` -- AT HEAD, lines 4270-5805 (`*` marks a line your previous draft changed)

```c
 4270|  X(to_be_translated)
 4271|  {
 4272|  	uint64_t addr, low_pc;
 4273|  	uint32_t iword, imm;
 4274|  	unsigned char *page;
     | [... lines 4275-4531 not shown ...]
 4532|  			case SPECIAL_MULTU: ic->f = instr(multu); break;
 4533|  			case SPECIAL_DMULT: ic->f = instr(dmult); x64=1; break;
 4534|  			case SPECIAL_DMULTU:ic->f = instr(dmultu); x64=1; break;
 4535|  			case SPECIAL_TGE:   ic->f = instr(tge); break;
 4536|  			case SPECIAL_TGEU:  ic->f = instr(tgeu); break;
 4537|  			case SPECIAL_TLT:   ic->f = instr(tlt); break;
 4538|  			case SPECIAL_TLTU:  ic->f = instr(tltu); break;
 4539|  			case SPECIAL_TEQ:   ic->f = instr(teq); break;
 4540|  			case SPECIAL_TNE:   ic->f = instr(tne); break;
 4541|  			case SPECIAL_MOVN:  ic->f = instr(movn); break;
 4542|  			case SPECIAL_MOVZ:  ic->f = instr(movz); break;
 4543|  			}
 4544|  
 4545|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4546|  			ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4547|  			ic->arg[2] = (size_t)&cpu->cd.mips.gpr[rd];
 4548|  
 4549|  			switch (s6) {
 4550|  			case SPECIAL_MFHI:
 4551|  				ic->arg[0] = (size_t)&cpu->cd.mips.hi;
 4552|  				break;
 4553|  			case SPECIAL_MFLO:
 4554|  				ic->arg[0] = (size_t)&cpu->cd.mips.lo;
 4555|  				break;
 4556|  			case SPECIAL_MTHI:
 4557|  				ic->arg[2] = (size_t)&cpu->cd.mips.hi;
 4558|  				break;
 4559|  			case SPECIAL_MTLO:
 4560|  				ic->arg[2] = (size_t)&cpu->cd.mips.lo;
 4561|  				break;
 4562|  			}
 4563|  			/*  Special cases for rd:  */
 4564|  			switch (s6) {
 4565|  			case SPECIAL_MTHI:
 4566|  			case SPECIAL_MTLO:
 4567|  			case SPECIAL_DIV:
 4568|  			case SPECIAL_DIVU:
 4569|  			case SPECIAL_DDIV:
 4570|  			case SPECIAL_DDIVU:
 4571|  			case SPECIAL_MULT:
 4572|  			case SPECIAL_MULTU:
 4573|  			case SPECIAL_DMULT:
 4574|  			case SPECIAL_DMULTU:
 4575|  				if (s6 == SPECIAL_MULT && rd != MIPS_GPR_ZERO) {
 4576|  					if (cpu->cd.mips.cpu_type.rev ==
 4577|  					    MIPS_R5900) {
 4578|  						ic->f = instr(mult_r5900);
 4579|  						break;
 4580|  					}
 4581|  					break;
 4582|  				}
 4583|  				if (s6 == SPECIAL_MULTU && rd!=MIPS_GPR_ZERO) {
 4584|  					if (cpu->cd.mips.cpu_type.rev ==
 4585|  					    MIPS_R5900) {
 4586|  						ic->f = instr(multu_r5900);
 4587|  						break;
 4588|  					}
 4589|  				}
 4590|  				if (rd != MIPS_GPR_ZERO) {
 4591|  					if (!cpu->translation_readahead)
 4592|  						fatal("TODO: rd NON-zero\n");
 4593|  					goto bad;
 4594|  				}
 4595|  				/*  These instructions don't use rd.  */
 4596|  				break;
 4597|  			case SPECIAL_TGE:
 4598|  			case SPECIAL_TGEU:
 4599|  			case SPECIAL_TLT:
 4600|  			case SPECIAL_TLTU:
 4601|  			case SPECIAL_TEQ:
 4602|  			case SPECIAL_TNE:
 4603|  				/*  In these instructions, rd is a 'code',
 4604|  				    only read by trap handling software.  */
 4605|  				break;
 4606|  			default:if (rd == MIPS_GPR_ZERO)
 4607|  					ic->f = instr(nop);
 4608|  			}
 4609|  
 4610|  			if (ic->f == instr(addu))
 4611|  				cpu->cd.mips.combination_check = COMBINE(addu);
 4612|  
 4613|  			break;
 4614|  
 4615|  		case SPECIAL_JR:
 4616|  		case SPECIAL_JALR:
 4617|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4618|  			ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rd];
 4619|  			if (s6 == SPECIAL_JALR && rd == MIPS_GPR_ZERO)
 4620|  				s6 = SPECIAL_JR;
 4621|  			ic->arg[2] = (addr & 0xffc) + 8;
 4622|  			switch (s6) {
 4623|  			case SPECIAL_JR:
 4624|  				if (rs == MIPS_GPR_RA) {
 4625|  					if (cpu->machine->show_trace_tree)
 4626|  						ic->f = instr(jr_ra_trace);
 4627|  					else
 4628|  						ic->f = instr(jr_ra);
 4629|  				} else {
 4630|  					ic->f = instr(jr);
 4631|  				}
 4632|  				if (cpu->translation_readahead > 2)
 4633|  					cpu->translation_readahead = 2;
 4634|  				break;
 4635|  			case SPECIAL_JALR:
 4636|  				if (cpu->machine->show_trace_tree)
 4637|  					ic->f = instr(jalr_trace);
 4638|  				else
 4639|  					ic->f = instr(jalr);
 4640|  				break;
 4641|  			}
 4642|* 			if (cpu->delay_slot) {
 4643|* 				if (!cpu->translation_readahead)
 4644|* 					fatal("TODO: branch in delay "
 4645|* 					    "slot? (1)\n");
 4646|* 				goto bad;
 4647|* 			}
 4648|* 			break;
 4649|  
 4650|  		case SPECIAL_SYSCALL:
 4651|  			if (((iword >> 6) & 0xfffff) == 0x30378) {
 4652|  				/*  "Magic trap" for PROM emulation:  */
 4653|  				ic->f = instr(promemul);
 4654|  			} else {
 4655|  				ic->f = instr(syscall);
 4656|  			}
 4657|  			break;
 4658|  
 4659|  		case SPECIAL_BREAK:
 4660|  			/*  #235: Only treat "break 0x30378" as the GXemul reboot
 4661|  			    sentinel when executed from the injected reset stub
 4662|  			    (physical 0x1fc00000 = kseg0/1 0x9fc00000/0xbfc00000);
 4663|  			    a guest that executes this encoding from ordinary RAM
 4664|  			    must get a real Breakpoint exception, as on hardware,
 4665|  			    not a silent host reboot.  */
 4666|  			if (((iword >> 6) & 0xfffff) == 0x30378 &&
 4667|  			    (addr & 0x1fffffff) == 0x1fc00000) {
 4668|  				/*  "Magic trap" for REBOOT:  */
 4669|  				ic->f = instr(reboot);
 4670|  			} else {
 4671|  				ic->f = instr(break);
 4672|  			}
 4673|  			break;
 4674|  
 4675|  		case SPECIAL_SYNC:
 4676|  			ic->f = instr(nop);
 4677|  			break;
 4678|  
 4679|  		default:goto bad;
 4680|  		}
 4681|  		break;
 4682|  
 4683|  	case HI6_BEQ:
 4684|  	case HI6_BNE:
 4685|  	case HI6_BEQL:
 4686|  	case HI6_BNEL:
 4687|  	case HI6_BLEZ:
 4688|  	case HI6_BLEZL:
 4689|  	case HI6_BGTZ:
 4690|  	case HI6_BGTZL:
 4691|  		samepage_function = NULL;  /*  get rid of a compiler warning  */
 4692|  		switch (main_opcode) {
 4693|  		case HI6_BEQ:
 4694|  			ic->f = instr(beq);
 4695|  			samepage_function = instr(beq_samepage);
 4696|  			/*  Special case: comparing a register with itself:  */
 4697|  			if (rs == rt) {
 4698|  				ic->f = instr(b);
 4699|  				samepage_function = instr(b_samepage);
 4700|  			}
 4701|  			break;
 4702|  		case HI6_BNE:
 4703|  			ic->f = instr(bne);
 4704|  			samepage_function = instr(bne_samepage);
 4705|  			break;
 4706|  		case HI6_BEQL:
 4707|  			ic->f = instr(beql);
 4708|  			samepage_function = instr(beql_samepage);
 4709|  			/*  Special case: comparing a register with itself:  */
 4710|  			if (rs == rt) {
 4711|  				ic->f = instr(b);
 4712|  				samepage_function = instr(b_samepage);
 4713|  			}
 4714|  			break;
 4715|  		case HI6_BNEL:
 4716|  			ic->f = instr(bnel);
 4717|  			samepage_function = instr(bnel_samepage);
 4718|  			break;
 4719|  		case HI6_BLEZ:
 4720|  			ic->f = instr(blez);
 4721|  			samepage_function = instr(blez_samepage);
 4722|  			break;
 4723|  		case HI6_BLEZL:
 4724|  			ic->f = instr(blezl);
 4725|  			samepage_function = instr(blezl_samepage);
 4726|  			break;
 4727|  		case HI6_BGTZ:
 4728|  			ic->f = instr(bgtz);
 4729|  			samepage_function = instr(bgtz_samepage);
 4730|  			break;
 4731|  		case HI6_BGTZL:
 4732|  			ic->f = instr(bgtzl);
 4733|  			samepage_function = instr(bgtzl_samepage);
 4734|  			break;
 4735|  		}
 4736|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4737|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4738|  		ic->arg[2] = (int32_t) ( (imm << MIPS_INSTR_ALIGNMENT_SHIFT)
 4739|  		    + (addr & 0xffc) + 4 );
 4740|  		/*  Is the offset from the start of the current page still
 4741|  		    within the same page? Then use the samepage_function:  */
 4742|  		if ((uint32_t)ic->arg[2] < ((MIPS_IC_ENTRIES_PER_PAGE - 1)
 4743|  		    << MIPS_INSTR_ALIGNMENT_SHIFT) && (addr & 0xffc) < 0xffc) {
 4744|  			ic->arg[2] = (size_t) (cpu->cd.mips.cur_ic_page +
 4745|  			    ((ic->arg[2] >> MIPS_INSTR_ALIGNMENT_SHIFT)
 4746|  			    & (MIPS_IC_ENTRIES_PER_PAGE - 1)));
 4747|  			ic->f = samepage_function;
 4748|  		}
 4749|* 		if (cpu->delay_slot) {
 4750|* 			if (!cpu->translation_readahead)
 4751|* 				fatal("TODO: branch in delay slot? (2)\n");
 4752|* 			goto bad;
 4753|* 		}
 4754|* 		break;
 4755|  
 4756|  	case HI6_ADDI:
 4757|  	case HI6_ADDIU:
 4758|  	case HI6_SLTI:
 4759|  	case HI6_SLTIU:
 4760|  	case HI6_DADDI:
 4761|  	case HI6_DADDIU:
 4762|  	case HI6_ANDI:
 4763|  	case HI6_ORI:
 4764|  	case HI6_XORI:
 4765|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4766|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4767|  		if (main_opcode == HI6_ADDI ||
 4768|  		    main_opcode == HI6_ADDIU ||
 4769|  		    main_opcode == HI6_SLTI ||
 4770|  		    main_opcode == HI6_SLTIU ||
 4771|  		    main_opcode == HI6_DADDI ||
 4772|  		    main_opcode == HI6_DADDIU)
 4773|  			ic->arg[2] = (int16_t)iword;
 4774|  		else
 4775|  			ic->arg[2] = (uint16_t)iword;
 4776|  
 4777|  		switch (main_opcode) {
 4778|  		case HI6_ADDI:    ic->f = instr(addi); break;
 4779|  		case HI6_ADDIU:   ic->f = instr(addiu); break;
 4780|  		case HI6_SLTI:    ic->f = instr(slti); break;
 4781|  		case HI6_SLTIU:   ic->f = instr(sltiu); break;
 4782|  		case HI6_DADDI:   ic->f = instr(daddi); x64 = 1; break;
 4783|  		case HI6_DADDIU:  ic->f = instr(daddiu); x64 = 1; break;
 4784|  		case HI6_ANDI:    ic->f = instr(andi); break;
 4785|  		case HI6_ORI:     ic->f = instr(ori); break;
 4786|  		case HI6_XORI:    ic->f = instr(xori); break;
 4787|  		}
 4788|  
 4789|  		if (ic->arg[2] == 0) {
 4790|  			if ((cpu->is_32bit && ic->f == instr(addiu)) ||
 4791|  			    (!cpu->is_32bit && ic->f == instr(daddiu))) {
 4792|  				ic->f = instr(mov);
 4793|  				ic->arg[2] = ic->arg[1];
 4794|  			}
 4795|  		}
 4796|  
 4797|  		if (rt == MIPS_GPR_ZERO)
 4798|  			ic->f = instr(nop);
 4799|  
 4800|  		if (ic->f == instr(ori))
 4801|  			cpu->cd.mips.combination_check = COMBINE(ori);
 4802|  		if (ic->f == instr(addiu))
 4803|  			cpu->cd.mips.combination_check = COMBINE(addiu);
 4804|  		if (ic->f == instr(daddiu))
 4805|  			cpu->cd.mips.combination_check = COMBINE(b_daddiu);
 4806|  		break;
 4807|  
 4808|  	case HI6_LUI:
 4809|  		ic->f = instr(set);
 4810|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4811|  		ic->arg[1] = (int32_t) (imm << 16);
 4812|  		/*  NOTE: Don't use arg[2] here. It can be used with
 4813|  		    instruction combinations, to do lui + addiu, etc.  */
 4814|  		if (rt == MIPS_GPR_ZERO)
     | [... lines 4815-5775 not shown ...]
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
    "old": "\t\t\tif (cpu->delay_slot) {\n\t\t\t\tif (!cpu->translation_readahead)\n\t\t\t\t\tfatal(\"TODO: branch in delay \"\n\t\t\t\t\t    \"slot? (1)\\n\");\n\t\t\t\tgoto bad;\n\t\t\t}",
    "new": "\t\t\t/* #mipsdsbranch: unpredictable, do not halt */",
    "why": "Remove goto bad for branch in delay slot, letting the already-assigned instruction function execute (or do nothing) unpredictably."
  },
  {
    "file": "src/cpus/cpu_mips_instr.c",
    "old": "\t\tif (cpu->delay_slot) {\n\t\t\tif (!cpu->translation_readahead)\n\t\t\t\tfatal(\"TODO: branch in delay slot? (2)\\n\");\n\t\t\tgoto bad;\n\t\t}",
    "new": "\t\t/* #mipsdsbranch: unpredictable, do not halt */",
    "why": "Remove goto bad for branch in delay slot to avoid CPU-STOP."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MIPSDSBRANCH: DEFECT, 2 FINDINGS
1. The diff does **not** remove the defect at every site the issue names. It successfully addresses `src/cpus/cpu_mips_instr.c:4644` (now around line 4642) and `:4751` (now around line 4744). However, it entirely misses the three other sites explicitly listed in the issue: `:4837`, `:5054`, and `:5336`.
2. CONTROL FLOW: The added `break;` (by removing `goto bad;`) does not skip the common tail; rather, it *restores* the path to the common tail (`AFTER:5774` onwards, into `#include "cpu_dyntrans.c"`). The original `goto bad;` skipped the tail. What `goto bad;` skips is UNSETTLED because the `bad:` label is not shown in the snippet.
3. RETURN VALUE: UNSETTLED. The `bad:` label and the return statements in `cpu_dyntrans.c` are not shown, so we cannot determine what the exact return values are on either path.
4. ELSE changed: The guest can now successfully translate and execute a branch instruction placed in a delay slot, as `ic->f` is set (e.g., `ic->f = instr(jr);`) and execution continues to the tail instead of hitting the `fatal(...)` crash. The diagnostic message `"TODO: branch in delay slot?"` is no longer printed.
5. House idioms: The new comments use `/* #mipsdsbranch: unpredictable, do not halt */`, which matches the requested `/* #NNN: ... */` tag format.
**Findings:**
`src/cpus/cpu_mips_instr.c:4837`: DEFECT. Missing fix for sites 4837, 5054, and 5336. Apply the same block removal at these locations.
`src/cpus/cpu_mips_instr.c:5770`: QUESTION. The exact behavior of the `bad:` label and the function's return value are UNSETTLED because the label is out of the excerpt's bounds.
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

End with two lines: `REVISION_MIPSDSBRANCH: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MIPSDSBRANCH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
