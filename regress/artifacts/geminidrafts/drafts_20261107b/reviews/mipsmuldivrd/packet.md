# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipsmuldivrd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipsmuldivrd`, state `open`)

**title:** src/cpus/cpu_mips_instr.c:4590-4594 -- MULTU, DIV, DIVU, DDIV, DDIVU, DMULT, DMULTU, MTHI and MTLO with a nonzero rd field print `TODO: rd NON-zero` and reach goto bad, while MULT with a nonzero rd is accepted with rd ignored -- CPU-STOP (any privilege; a must-be-zero field)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 4590-4594

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..4aa0ea80 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -4587,12 +4587,7 @@ X(to_be_translated)
 						break;
 					}
 				}
-				if (rd != MIPS_GPR_ZERO) {
-					if (!cpu->translation_readahead)
-						fatal("TODO: rd NON-zero\n");
-					goto bad;
-				}
-				/*  These instructions don't use rd.  */
+				/*  #mipsmuldivrd: These instructions don't use rd; ignore rather than fault on non-zero  */
 				break;
 			case SPECIAL_TGE:
 			case SPECIAL_TGEU:
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 4270-5800 (`+` marks a line the diff added or the point of a deletion)

```c
 4270|  X(to_be_translated)
 4271|  {
 4272|  	uint64_t addr, low_pc;
 4273|  	uint32_t iword, imm;
 4274|  	unsigned char *page;
     | [... lines 4275-4479 not shown ...]
 4480|  		case SPECIAL_DSUB:
 4481|  		case SPECIAL_DSUBU:
 4482|  		case SPECIAL_SLT:
 4483|  		case SPECIAL_SLTU:
 4484|  		case SPECIAL_AND:
 4485|  		case SPECIAL_OR:
 4486|  		case SPECIAL_XOR:
 4487|  		case SPECIAL_NOR:
 4488|  		case SPECIAL_MOVN:
 4489|  		case SPECIAL_MOVZ:
 4490|  		case SPECIAL_MFHI:
 4491|  		case SPECIAL_MFLO:
 4492|  		case SPECIAL_MTHI:
 4493|  		case SPECIAL_MTLO:
 4494|  		case SPECIAL_DIV:
 4495|  		case SPECIAL_DIVU:
 4496|  		case SPECIAL_DDIV:
 4497|  		case SPECIAL_DDIVU:
 4498|  		case SPECIAL_MULT:
 4499|  		case SPECIAL_MULTU:
 4500|  		case SPECIAL_DMULT:
 4501|  		case SPECIAL_DMULTU:
 4502|  		case SPECIAL_TGE:
 4503|  		case SPECIAL_TGEU:
 4504|  		case SPECIAL_TLT:
 4505|  		case SPECIAL_TLTU:
 4506|  		case SPECIAL_TEQ:
 4507|  		case SPECIAL_TNE:
 4508|  			switch (s6) {
 4509|  			case SPECIAL_ADD:   ic->f = instr(add); break;
 4510|  			case SPECIAL_ADDU:  ic->f = instr(addu); break;
 4511|  			case SPECIAL_SUB:   ic->f = instr(sub); break;
 4512|  			case SPECIAL_SUBU:  ic->f = instr(subu); break;
 4513|  			case SPECIAL_DADD:  ic->f = instr(dadd); x64=1; break;
 4514|  			case SPECIAL_DADDU: ic->f = instr(daddu); x64=1; break;
 4515|  			case SPECIAL_DSUB:  ic->f = instr(dsub); x64=1; break;
 4516|  			case SPECIAL_DSUBU: ic->f = instr(dsubu); x64=1; break;
 4517|  			case SPECIAL_SLT:   ic->f = instr(slt); break;
 4518|  			case SPECIAL_SLTU:  ic->f = instr(sltu); break;
 4519|  			case SPECIAL_AND:   ic->f = instr(and); break;
 4520|  			case SPECIAL_OR:    ic->f = instr(or); break;
 4521|  			case SPECIAL_XOR:   ic->f = instr(xor); break;
 4522|  			case SPECIAL_NOR:   ic->f = instr(nor); break;
 4523|  			case SPECIAL_MFHI:  ic->f = instr(mov); break;
 4524|  			case SPECIAL_MFLO:  ic->f = instr(mov); break;
 4525|  			case SPECIAL_MTHI:  ic->f = instr(mov); break;
 4526|  			case SPECIAL_MTLO:  ic->f = instr(mov); break;
 4527|  			case SPECIAL_DIV:   ic->f = instr(div); break;
 4528|  			case SPECIAL_DIVU:  ic->f = instr(divu); break;
 4529|  			case SPECIAL_DDIV:  ic->f = instr(ddiv); x64=1; break;
 4530|  			case SPECIAL_DDIVU: ic->f = instr(ddivu); x64=1; break;
 4531|  			case SPECIAL_MULT : ic->f = instr(mult); break;
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
 4590|+ 				/*  #mipsmuldivrd: These instructions don't use rd; ignore rather than fault on non-zero  */
 4591|  				break;
 4592|  			case SPECIAL_TGE:
 4593|  			case SPECIAL_TGEU:
 4594|  			case SPECIAL_TLT:
 4595|  			case SPECIAL_TLTU:
 4596|  			case SPECIAL_TEQ:
 4597|  			case SPECIAL_TNE:
 4598|  				/*  In these instructions, rd is a 'code',
 4599|  				    only read by trap handling software.  */
 4600|  				break;
 4601|  			default:if (rd == MIPS_GPR_ZERO)
 4602|  					ic->f = instr(nop);
 4603|  			}
 4604|  
 4605|  			if (ic->f == instr(addu))
 4606|  				cpu->cd.mips.combination_check = COMBINE(addu);
 4607|  
 4608|  			break;
 4609|  
 4610|  		case SPECIAL_JR:
 4611|  		case SPECIAL_JALR:
 4612|  			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4613|  			ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rd];
 4614|  			if (s6 == SPECIAL_JALR && rd == MIPS_GPR_ZERO)
 4615|  				s6 = SPECIAL_JR;
 4616|  			ic->arg[2] = (addr & 0xffc) + 8;
 4617|  			switch (s6) {
 4618|  			case SPECIAL_JR:
 4619|  				if (rs == MIPS_GPR_RA) {
 4620|  					if (cpu->machine->show_trace_tree)
 4621|  						ic->f = instr(jr_ra_trace);
 4622|  					else
 4623|  						ic->f = instr(jr_ra);
 4624|  				} else {
 4625|  					ic->f = instr(jr);
 4626|  				}
 4627|  				if (cpu->translation_readahead > 2)
 4628|  					cpu->translation_readahead = 2;
 4629|  				break;
 4630|  			case SPECIAL_JALR:
 4631|  				if (cpu->machine->show_trace_tree)
 4632|  					ic->f = instr(jalr_trace);
 4633|  				else
 4634|  					ic->f = instr(jalr);
 4635|  				break;
 4636|  			}
 4637|  			if (cpu->delay_slot) {
 4638|  				if (!cpu->translation_readahead)
 4639|  					fatal("TODO: branch in delay "
 4640|  					    "slot? (1)\n");
 4641|  				goto bad;
 4642|  			}
 4643|  			break;
 4644|  
 4645|  		case SPECIAL_SYSCALL:
 4646|  			if (((iword >> 6) & 0xfffff) == 0x30378) {
 4647|  				/*  "Magic trap" for PROM emulation:  */
 4648|  				ic->f = instr(promemul);
 4649|  			} else {
 4650|  				ic->f = instr(syscall);
     | [... lines 4651-5770 not shown ...]
 5771|  		ic->f = instr(cache);
 5772|  		break;
 5773|  
 5774|  	default:goto bad;
 5775|  	}
 5776|  
 5777|  
 5778|  #ifdef MODE32
 5779|  	if (x64) {
 5780|  		static int has_warned = 0;
 5781|  		if (!has_warned && !cpu->translation_readahead) {
 5782|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5783|  			    " instruction on an emulated 32-bit processor; "
 5784|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5785|  			has_warned = 1;
 5786|  		}
 5787|  		if (cpu->translation_readahead)
 5788|  			goto bad;
 5789|  		else
 5790|  			ic->f = instr(reserved);
 5791|  	}
 5792|  #else
 5793|  	(void)x64; // avoid compiler warning
 5794|  #endif
 5795|  
 5796|  
 5797|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5798|  #include "cpu_dyntrans.c" 
 5799|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5800|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSMULDIVRD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSMULDIVRD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
