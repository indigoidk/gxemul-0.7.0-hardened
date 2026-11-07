# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipsmuldivrd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipsmuldivrd`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_mips_instr.c:4590-4594 -- MULTU, DIV, DIVU, DDIV, DDIVU, DMULT, DMULTU, MTHI and MTLO with a nonzero rd field print `TODO: rd NON-zero` and reach goto bad, while MULT with a nonzero rd is accepted with rd ignored -- CPU-STOP (any privilege; a must-be-zero field)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- remove the goto bad for nonzero rd and ignore the rd field

## The code at the cited lines

### `src/cpus/cpu_mips_instr.c` around the row's cited line 4590 (HEAD 8d9df658, lines 4470-4710)

```c
 4470| 			if (ic->f == instr(nop))
 4471| 				cpu->cd.mips.combination_check = COMBINE(nop);
 4472| 			break;
 4473| 
 4474| 		case SPECIAL_ADD:
 4475| 		case SPECIAL_ADDU:
 4476| 		case SPECIAL_SUB:
 4477| 		case SPECIAL_SUBU:
 4478| 		case SPECIAL_DADD:
 4479| 		case SPECIAL_DADDU:
 4480| 		case SPECIAL_DSUB:
 4481| 		case SPECIAL_DSUBU:
 4482| 		case SPECIAL_SLT:
 4483| 		case SPECIAL_SLTU:
 4484| 		case SPECIAL_AND:
 4485| 		case SPECIAL_OR:
 4486| 		case SPECIAL_XOR:
 4487| 		case SPECIAL_NOR:
 4488| 		case SPECIAL_MOVN:
 4489| 		case SPECIAL_MOVZ:
 4490| 		case SPECIAL_MFHI:
 4491| 		case SPECIAL_MFLO:
 4492| 		case SPECIAL_MTHI:
 4493| 		case SPECIAL_MTLO:
 4494| 		case SPECIAL_DIV:
 4495| 		case SPECIAL_DIVU:
 4496| 		case SPECIAL_DDIV:
 4497| 		case SPECIAL_DDIVU:
 4498| 		case SPECIAL_MULT:
 4499| 		case SPECIAL_MULTU:
 4500| 		case SPECIAL_DMULT:
 4501| 		case SPECIAL_DMULTU:
 4502| 		case SPECIAL_TGE:
 4503| 		case SPECIAL_TGEU:
 4504| 		case SPECIAL_TLT:
 4505| 		case SPECIAL_TLTU:
 4506| 		case SPECIAL_TEQ:
 4507| 		case SPECIAL_TNE:
 4508| 			switch (s6) {
 4509| 			case SPECIAL_ADD:   ic->f = instr(add); break;
 4510| 			case SPECIAL_ADDU:  ic->f = instr(addu); break;
 4511| 			case SPECIAL_SUB:   ic->f = instr(sub); break;
 4512| 			case SPECIAL_SUBU:  ic->f = instr(subu); break;
 4513| 			case SPECIAL_DADD:  ic->f = instr(dadd); x64=1; break;
 4514| 			case SPECIAL_DADDU: ic->f = instr(daddu); x64=1; break;
 4515| 			case SPECIAL_DSUB:  ic->f = instr(dsub); x64=1; break;
 4516| 			case SPECIAL_DSUBU: ic->f = instr(dsubu); x64=1; break;
 4517| 			case SPECIAL_SLT:   ic->f = instr(slt); break;
 4518| 			case SPECIAL_SLTU:  ic->f = instr(sltu); break;
 4519| 			case SPECIAL_AND:   ic->f = instr(and); break;
 4520| 			case SPECIAL_OR:    ic->f = instr(or); break;
 4521| 			case SPECIAL_XOR:   ic->f = instr(xor); break;
 4522| 			case SPECIAL_NOR:   ic->f = instr(nor); break;
 4523| 			case SPECIAL_MFHI:  ic->f = instr(mov); break;
 4524| 			case SPECIAL_MFLO:  ic->f = instr(mov); break;
 4525| 			case SPECIAL_MTHI:  ic->f = instr(mov); break;
 4526| 			case SPECIAL_MTLO:  ic->f = instr(mov); break;
 4527| 			case SPECIAL_DIV:   ic->f = instr(div); break;
 4528| 			case SPECIAL_DIVU:  ic->f = instr(divu); break;
 4529| 			case SPECIAL_DDIV:  ic->f = instr(ddiv); x64=1; break;
 4530| 			case SPECIAL_DDIVU: ic->f = instr(ddivu); x64=1; break;
 4531| 			case SPECIAL_MULT : ic->f = instr(mult); break;
 4532| 			case SPECIAL_MULTU: ic->f = instr(multu); break;
 4533| 			case SPECIAL_DMULT: ic->f = instr(dmult); x64=1; break;
 4534| 			case SPECIAL_DMULTU:ic->f = instr(dmultu); x64=1; break;
 4535| 			case SPECIAL_TGE:   ic->f = instr(tge); break;
 4536| 			case SPECIAL_TGEU:  ic->f = instr(tgeu); break;
 4537| 			case SPECIAL_TLT:   ic->f = instr(tlt); break;
 4538| 			case SPECIAL_TLTU:  ic->f = instr(tltu); break;
 4539| 			case SPECIAL_TEQ:   ic->f = instr(teq); break;
 4540| 			case SPECIAL_TNE:   ic->f = instr(tne); break;
 4541| 			case SPECIAL_MOVN:  ic->f = instr(movn); break;
 4542| 			case SPECIAL_MOVZ:  ic->f = instr(movz); break;
 4543| 			}
 4544| 
 4545| 			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4546| 			ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rt];
 4547| 			ic->arg[2] = (size_t)&cpu->cd.mips.gpr[rd];
 4548| 
 4549| 			switch (s6) {
 4550| 			case SPECIAL_MFHI:
 4551| 				ic->arg[0] = (size_t)&cpu->cd.mips.hi;
 4552| 				break;
 4553| 			case SPECIAL_MFLO:
 4554| 				ic->arg[0] = (size_t)&cpu->cd.mips.lo;
 4555| 				break;
 4556| 			case SPECIAL_MTHI:
 4557| 				ic->arg[2] = (size_t)&cpu->cd.mips.hi;
 4558| 				break;
 4559| 			case SPECIAL_MTLO:
 4560| 				ic->arg[2] = (size_t)&cpu->cd.mips.lo;
 4561| 				break;
 4562| 			}
 4563| 			/*  Special cases for rd:  */
 4564| 			switch (s6) {
 4565| 			case SPECIAL_MTHI:
 4566| 			case SPECIAL_MTLO:
 4567| 			case SPECIAL_DIV:
 4568| 			case SPECIAL_DIVU:
 4569| 			case SPECIAL_DDIV:
 4570| 			case SPECIAL_DDIVU:
 4571| 			case SPECIAL_MULT:
 4572| 			case SPECIAL_MULTU:
 4573| 			case SPECIAL_DMULT:
 4574| 			case SPECIAL_DMULTU:
 4575| 				if (s6 == SPECIAL_MULT && rd != MIPS_GPR_ZERO) {
 4576| 					if (cpu->cd.mips.cpu_type.rev ==
 4577| 					    MIPS_R5900) {
 4578| 						ic->f = instr(mult_r5900);
 4579| 						break;
 4580| 					}
 4581| 					break;
 4582| 				}
 4583| 				if (s6 == SPECIAL_MULTU && rd!=MIPS_GPR_ZERO) {
 4584| 					if (cpu->cd.mips.cpu_type.rev ==
 4585| 					    MIPS_R5900) {
 4586| 						ic->f = instr(multu_r5900);
 4587| 						break;
 4588| 					}
 4589| 				}
 4590| 				if (rd != MIPS_GPR_ZERO) {
 4591| 					if (!cpu->translation_readahead)
 4592| 						fatal("TODO: rd NON-zero\n");
 4593| 					goto bad;
 4594| 				}
 4595| 				/*  These instructions don't use rd.  */
 4596| 				break;
 4597| 			case SPECIAL_TGE:
 4598| 			case SPECIAL_TGEU:
 4599| 			case SPECIAL_TLT:
 4600| 			case SPECIAL_TLTU:
 4601| 			case SPECIAL_TEQ:
 4602| 			case SPECIAL_TNE:
 4603| 				/*  In these instructions, rd is a 'code',
 4604| 				    only read by trap handling software.  */
 4605| 				break;
 4606| 			default:if (rd == MIPS_GPR_ZERO)
 4607| 					ic->f = instr(nop);
 4608| 			}
 4609| 
 4610| 			if (ic->f == instr(addu))
 4611| 				cpu->cd.mips.combination_check = COMBINE(addu);
 4612| 
 4613| 			break;
 4614| 
 4615| 		case SPECIAL_JR:
 4616| 		case SPECIAL_JALR:
 4617| 			ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rs];
 4618| 			ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rd];
 4619| 			if (s6 == SPECIAL_JALR && rd == MIPS_GPR_ZERO)
 4620| 				s6 = SPECIAL_JR;
 4621| 			ic->arg[2] = (addr & 0xffc) + 8;
 4622| 			switch (s6) {
 4623| 			case SPECIAL_JR:
 4624| 				if (rs == MIPS_GPR_RA) {
 4625| 					if (cpu->machine->show_trace_tree)
 4626| 						ic->f = instr(jr_ra_trace);
 4627| 					else
 4628| 						ic->f = instr(jr_ra);
 4629| 				} else {
 4630| 					ic->f = instr(jr);
 4631| 				}
 4632| 				if (cpu->translation_readahead > 2)
 4633| 					cpu->translation_readahead = 2;
 4634| 				break;
 4635| 			case SPECIAL_JALR:
 4636| 				if (cpu->machine->show_trace_tree)
 4637| 					ic->f = instr(jalr_trace);
 4638| 				else
 4639| 					ic->f = instr(jalr);
 4640| 				break;
 4641| 			}
 4642| 			if (cpu->delay_slot) {
 4643| 				if (!cpu->translation_readahead)
 4644| 					fatal("TODO: branch in delay "
 4645| 					    "slot? (1)\n");
 4646| 				goto bad;
 4647| 			}
 4648| 			break;
 4649| 
 4650| 		case SPECIAL_SYSCALL:
 4651| 			if (((iword >> 6) & 0xfffff) == 0x30378) {
 4652| 				/*  "Magic trap" for PROM emulation:  */
 4653| 				ic->f = instr(promemul);
 4654| 			} else {
 4655| 				ic->f = instr(syscall);
 4656| 			}
 4657| 			break;
 4658| 
 4659| 		case SPECIAL_BREAK:
 4660| 			/*  #235: Only treat "break 0x30378" as the GXemul reboot
 4661| 			    sentinel when executed from the injected reset stub
 4662| 			    (physical 0x1fc00000 = kseg0/1 0x9fc00000/0xbfc00000);
 4663| 			    a guest that executes this encoding from ordinary RAM
 4664| 			    must get a real Breakpoint exception, as on hardware,
 4665| 			    not a silent host reboot.  */
 4666| 			if (((iword >> 6) & 0xfffff) == 0x30378 &&
 4667| 			    (addr & 0x1fffffff) == 0x1fc00000) {
 4668| 				/*  "Magic trap" for REBOOT:  */
 4669| 				ic->f = instr(reboot);
 4670| 			} else {
 4671| 				ic->f = instr(break);
 4672| 			}
 4673| 			break;
 4674| 
 4675| 		case SPECIAL_SYNC:
 4676| 			ic->f = instr(nop);
 4677| 			break;
 4678| 
 4679| 		default:goto bad;
 4680| 		}
 4681| 		break;
 4682| 
 4683| 	case HI6_BEQ:
 4684| 	case HI6_BNE:
 4685| 	case HI6_BEQL:
 4686| 	case HI6_BNEL:
 4687| 	case HI6_BLEZ:
 4688| 	case HI6_BLEZL:
 4689| 	case HI6_BGTZ:
 4690| 	case HI6_BGTZL:
 4691| 		samepage_function = NULL;  /*  get rid of a compiler warning  */
 4692| 		switch (main_opcode) {
 4693| 		case HI6_BEQ:
 4694| 			ic->f = instr(beq);
 4695| 			samepage_function = instr(beq_samepage);
 4696| 			/*  Special case: comparing a register with itself:  */
 4697| 			if (rs == rt) {
 4698| 				ic->f = instr(b);
 4699| 				samepage_function = instr(b_samepage);
 4700| 			}
 4701| 			break;
 4702| 		case HI6_BNE:
 4703| 			ic->f = instr(bne);
 4704| 			samepage_function = instr(bne_samepage);
 4705| 			break;
 4706| 		case HI6_BEQL:
 4707| 			ic->f = instr(beql);
 4708| 			samepage_function = instr(beql_samepage);
 4709| 			/*  Special case: comparing a register with itself:  */
 4710| 			if (rs == rt) {
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

End with one line: `FIXDRAFT_MIPSMULDIVRD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
