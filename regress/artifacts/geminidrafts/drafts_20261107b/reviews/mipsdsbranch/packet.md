# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipsdsbranch` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipsdsbranch`, state `open`)

**title:** src/cpus/cpu_mips_instr.c:4644, :4751, :4837, :5054, :5336 -- a branch or jump decoded in a delay slot prints `TODO: branch in delay slot` and reaches goto bad at five sites, where the operation is UNPREDICTABLE and must not halt -- CPU-STOP (any privilege)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/cpu_mips_instr.c:4642`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..aafd3eb8 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -4639,12 +4639,7 @@ X(to_be_translated)
 					ic->f = instr(jalr);
 				break;
 			}
-			if (cpu->delay_slot) {
-				if (!cpu->translation_readahead)
-					fatal("TODO: branch in delay "
-					    "slot? (1)\n");
-				goto bad;
-			}
+			/* #mipsdsbranch: unpredictable, do not halt */
 			break;
 
 		case SPECIAL_SYSCALL:
@@ -4746,11 +4741,7 @@ X(to_be_translated)
 			    & (MIPS_IC_ENTRIES_PER_PAGE - 1)));
 			ic->f = samepage_function;
 		}
-		if (cpu->delay_slot) {
-			if (!cpu->translation_readahead)
-				fatal("TODO: branch in delay slot? (2)\n");
-			goto bad;
-		}
+		/* #mipsdsbranch: unpredictable, do not halt */
 		break;
 
 	case HI6_ADDI:
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 4270-5796 (`+` marks a line the diff added or the point of a deletion)

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
 4642|+ 			/* #mipsdsbranch: unpredictable, do not halt */
 4643|  			break;
 4644|  
 4645|  		case SPECIAL_SYSCALL:
 4646|  			if (((iword >> 6) & 0xfffff) == 0x30378) {
 4647|  				/*  "Magic trap" for PROM emulation:  */
 4648|  				ic->f = instr(promemul);
 4649|  			} else {
 4650|  				ic->f = instr(syscall);
 4651|  			}
 4652|  			break;
 4653|  
 4654|  		case SPECIAL_BREAK:
 4655|  			/*  #235: Only treat "break 0x30378" as the GXemul reboot
 4656|  			    sentinel when executed from the injected reset stub
 4657|  			    (physical 0x1fc00000 = kseg0/1 0x9fc00000/0xbfc00000);
 4658|  			    a guest that executes this encoding from ordinary RAM
 4659|  			    must get a real Breakpoint exception, as on hardware,
 4660|  			    not a silent host reboot.  */
 4661|  			if (((iword >> 6) & 0xfffff) == 0x30378 &&
 4662|  			    (addr & 0x1fffffff) == 0x1fc00000) {
 4663|  				/*  "Magic trap" for REBOOT:  */
 4664|  				ic->f = instr(reboot);
 4665|  			} else {
 4666|  				ic->f = instr(break);
 4667|  			}
 4668|  			break;
 4669|  
 4670|  		case SPECIAL_SYNC:
 4671|  			ic->f = instr(nop);
 4672|  			break;
 4673|  
 4674|  		default:goto bad;
 4675|  		}
 4676|  		break;
 4677|  
 4678|  	case HI6_BEQ:
 4679|  	case HI6_BNE:
 4680|  	case HI6_BEQL:
 4681|  	case HI6_BNEL:
 4682|  	case HI6_BLEZ:
 4683|  	case HI6_BLEZL:
 4684|  	case HI6_BGTZ:
 4685|  	case HI6_BGTZL:
 4686|  		samepage_function = NULL;  /*  get rid of a compiler warning  */
 4687|  		switch (main_opcode) {
 4688|  		case HI6_BEQ:
 4689|  			ic->f = instr(beq);
 4690|  			samepage_function = instr(beq_samepage);
 4691|  			/*  Special case: comparing a register with itself:  */
 4692|  			if (rs == rt) {
 4693|  				ic->f = instr(b);
 4694|  				samepage_function = instr(b_samepage);
 4695|  			}
 4696|  			break;
 4697|  		case HI6_BNE:
 4698|  			ic->f = instr(bne);
 4699|  			samepage_function = instr(bne_samepage);
 4700|  			break;
 4701|  		case HI6_BEQL:
 4702|  			ic->f = instr(beql);
 4703|  			samepage_function = instr(beql_samepage);
 4704|  			/*  Special case: comparing a register with itself:  */
 4705|  			if (rs == rt) {
 4706|  				ic->f = instr(b);
 4707|  				samepage_function = instr(b_samepage);
 4708|  			}
 4709|  			break;
 4710|  		case HI6_BNEL:
 4711|  			ic->f = instr(bnel);
 4712|  			samepage_function = instr(bnel_samepage);
 4713|  			break;
 4714|  		case HI6_BLEZ:
 4715|  			ic->f = instr(blez);
 4716|  			samepage_function = instr(blez_samepage);
 4717|  			break;
 4718|  		case HI6_BLEZL:
 4719|  			ic->f = instr(blezl);
 4720|  			samepage_function = instr(blezl_samepage);
 4721|  			break;
 4722|  		case HI6_BGTZ:
 4723|  			ic->f = instr(bgtz);
 4724|  			samepage_function = instr(bgtz_samepage);
 4725|  			break;
 4726|  		case HI6_BGTZL:
 4727|  			ic->f = instr(bgtzl);
 4728|  			samepage_function = instr(bgtzl_samepage);
 4729|  			break;
 4730|  		}
 4731|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4732|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4733|  		ic->arg[2] = (int32_t) ( (imm << MIPS_INSTR_ALIGNMENT_SHIFT)
 4734|  		    + (addr & 0xffc) + 4 );
 4735|  		/*  Is the offset from the start of the current page still
 4736|  		    within the same page? Then use the samepage_function:  */
 4737|  		if ((uint32_t)ic->arg[2] < ((MIPS_IC_ENTRIES_PER_PAGE - 1)
 4738|  		    << MIPS_INSTR_ALIGNMENT_SHIFT) && (addr & 0xffc) < 0xffc) {
 4739|  			ic->arg[2] = (size_t) (cpu->cd.mips.cur_ic_page +
 4740|  			    ((ic->arg[2] >> MIPS_INSTR_ALIGNMENT_SHIFT)
 4741|  			    & (MIPS_IC_ENTRIES_PER_PAGE - 1)));
 4742|  			ic->f = samepage_function;
 4743|  		}
 4744|+ 		/* #mipsdsbranch: unpredictable, do not halt */
 4745|  		break;
 4746|  
 4747|  	case HI6_ADDI:
 4748|  	case HI6_ADDIU:
 4749|  	case HI6_SLTI:
 4750|  	case HI6_SLTIU:
 4751|  	case HI6_DADDI:
 4752|  	case HI6_DADDIU:
 4753|  	case HI6_ANDI:
 4754|  	case HI6_ORI:
 4755|  	case HI6_XORI:
 4756|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4757|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4758|  		if (main_opcode == HI6_ADDI ||
 4759|  		    main_opcode == HI6_ADDIU ||
 4760|  		    main_opcode == HI6_SLTI ||
 4761|  		    main_opcode == HI6_SLTIU ||
 4762|  		    main_opcode == HI6_DADDI ||
 4763|  		    main_opcode == HI6_DADDIU)
 4764|  			ic->arg[2] = (int16_t)iword;
 4765|  		else
 4766|  			ic->arg[2] = (uint16_t)iword;
 4767|  
 4768|  		switch (main_opcode) {
 4769|  		case HI6_ADDI:    ic->f = instr(addi); break;
 4770|  		case HI6_ADDIU:   ic->f = instr(addiu); break;
 4771|  		case HI6_SLTI:    ic->f = instr(slti); break;
 4772|  		case HI6_SLTIU:   ic->f = instr(sltiu); break;
 4773|  		case HI6_DADDI:   ic->f = instr(daddi); x64 = 1; break;
 4774|  		case HI6_DADDIU:  ic->f = instr(daddiu); x64 = 1; break;
 4775|  		case HI6_ANDI:    ic->f = instr(andi); break;
 4776|  		case HI6_ORI:     ic->f = instr(ori); break;
 4777|  		case HI6_XORI:    ic->f = instr(xori); break;
 4778|  		}
 4779|  
 4780|  		if (ic->arg[2] == 0) {
 4781|  			if ((cpu->is_32bit && ic->f == instr(addiu)) ||
 4782|  			    (!cpu->is_32bit && ic->f == instr(daddiu))) {
 4783|  				ic->f = instr(mov);
 4784|  				ic->arg[2] = ic->arg[1];
 4785|  			}
 4786|  		}
 4787|  
 4788|  		if (rt == MIPS_GPR_ZERO)
 4789|  			ic->f = instr(nop);
 4790|  
 4791|  		if (ic->f == instr(ori))
 4792|  			cpu->cd.mips.combination_check = COMBINE(ori);
 4793|  		if (ic->f == instr(addiu))
 4794|  			cpu->cd.mips.combination_check = COMBINE(addiu);
 4795|  		if (ic->f == instr(daddiu))
 4796|  			cpu->cd.mips.combination_check = COMBINE(b_daddiu);
 4797|  		break;
 4798|  
 4799|  	case HI6_LUI:
 4800|  		ic->f = instr(set);
 4801|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 4802|  		ic->arg[1] = (int32_t) (imm << 16);
 4803|  		/*  NOTE: Don't use arg[2] here. It can be used with
 4804|  		    instruction combinations, to do lui + addiu, etc.  */
     | [... lines 4805-5766 not shown ...]
 5767|  		ic->f = instr(cache);
 5768|  		break;
 5769|  
 5770|  	default:goto bad;
 5771|  	}
 5772|  
 5773|  
 5774|  #ifdef MODE32
 5775|  	if (x64) {
 5776|  		static int has_warned = 0;
 5777|  		if (!has_warned && !cpu->translation_readahead) {
 5778|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5779|  			    " instruction on an emulated 32-bit processor; "
 5780|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5781|  			has_warned = 1;
 5782|  		}
 5783|  		if (cpu->translation_readahead)
 5784|  			goto bad;
 5785|  		else
 5786|  			ic->f = instr(reserved);
 5787|  	}
 5788|  #else
 5789|  	(void)x64; // avoid compiler warning
 5790|  #endif
 5791|  
 5792|  
 5793|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5794|  #include "cpu_dyntrans.c" 
 5795|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5796|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSDSBRANCH: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSDSBRANCH: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
