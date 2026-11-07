# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppccntlzwrc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppccntlzwrc`, state `open`, severity `MED`)

**title:** src/cpus/cpu_ppc_instr.c:4672-4680 -- the record form cntlzw. prints `TODO: rc` and reaches `goto bad` instead of setting CR0 -- CPU-STOP (user mode, every model)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- implement Rc=1 condition

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 4672 (HEAD 8d9df658, lines 4552-4792)

```c
 4552| 			    (new_pc & ~mask_within_page)) {
 4553| 				ic->f = samepage_function;
 4554| 				ic->arg[0] = (size_t) (
 4555| 				    cpu->cd.ppc.cur_ic_page +
 4556| 				    ((new_pc & mask_within_page) >> 2));
 4557| 			}
 4558| 		}
 4559| 		if (aa_bit) {
 4560| 			if (lk_bit) {
 4561| 				if (cpu->machine->show_trace_tree) {
 4562| 					ic->f = instr(bla_trace);
 4563| 				} else {
 4564| 					ic->f = instr(bla);
 4565| 				}
 4566| 			} else {
 4567| 				ic->f = instr(ba);
 4568| 			}
 4569| 			ic->arg[0] = (ssize_t)tmp_addr;
 4570| 		}
 4571| 		break;
 4572| 
 4573| 	case PPC_HI6_19:
 4574| 		xo = (iword >> 1) & 1023;
 4575| 		switch (xo) {
 4576| 
 4577| 		case PPC_19_BCLR:
 4578| 		case PPC_19_BCCTR:
 4579| 			bo = (iword >> 21) & 31;
 4580| 			bi = (iword >> 16) & 31;
 4581| 			bh = (iword >> 11) & 3;
 4582| 			lk_bit = iword & 1;
 4583| 			if (xo == PPC_19_BCLR) {
 4584| 				if (lk_bit)
 4585| 					ic->f = instr(bclr_l);
 4586| 				else {
 4587| 					ic->f = instr(bclr);
 4588| 					if (!cpu->machine->show_trace_tree &&
 4589| 					    (bo & 0x14) == 0x14)
 4590| 						ic->f = instr(bclr_20);
 4591| 				}
 4592| 			} else {
 4593| 				if (!(bo & 4)) {
 4594| 					if (!cpu->translation_readahead)
 4595| 						fatal("TODO: bclr/bcctr "
 4596| 						    "bo bit 2 clear!\n");
 4597| 					goto bad;
 4598| 				}
 4599| 				if (lk_bit)
 4600| 					ic->f = instr(bcctr_l);
 4601| 				else
 4602| 					ic->f = instr(bcctr);
 4603| 			}
 4604| 			ic->arg[0] = bo;
 4605| 			ic->arg[1] = 31 - bi;
 4606| 			ic->arg[2] = bh;
 4607| 			break;
 4608| 
 4609| 		case PPC_19_ISYNC:
 4610| 			/*  TODO  */
 4611| 			ic->f = instr(nop);
 4612| 			break;
 4613| 
 4614| 		case PPC_19_RFI:
 4615| 			ic->f = instr(rfi);
 4616| 			break;
 4617| 
 4618| 		case PPC_19_RFID:
 4619| 			ic->f = instr(rfid);
 4620| 			break;
 4621| 
 4622| 		case PPC_19_MCRF:
 4623| 			bf = (iword >> 23) & 7;
 4624| 			bfa = (iword >> 18) & 7;
 4625| 			ic->arg[0] = 28 - 4*bf;
 4626| 			ic->arg[1] = 28 - 4*bfa;
 4627| 			ic->f = instr(mcrf);
 4628| 			break;
 4629| 
 4630| 		case PPC_19_CRAND:
 4631| 		case PPC_19_CRANDC:
 4632| 		case PPC_19_CREQV:
 4633| 		case PPC_19_CROR:
 4634| 		case PPC_19_CRORC:
 4635| 		case PPC_19_CRNOR:
 4636| 		case PPC_19_CRXOR:
 4637| 			switch (xo) {
 4638| 			case PPC_19_CRAND:  ic->f = instr(crand); break;
 4639| 			case PPC_19_CRANDC: ic->f = instr(crandc); break;
 4640| 			case PPC_19_CREQV:  ic->f = instr(creqv); break;
 4641| 			case PPC_19_CROR:   ic->f = instr(cror); break;
 4642| 			case PPC_19_CRORC:  ic->f = instr(crorc); break;
 4643| 			case PPC_19_CRNOR:  ic->f = instr(crnor); break;
 4644| 			case PPC_19_CRXOR:  ic->f = instr(crxor); break;
 4645| 			}
 4646| 			ic->arg[0] = iword;
 4647| 			break;
 4648| 
 4649| 		default:goto bad;
 4650| 		}
 4651| 		break;
 4652| 
 4653| 	case PPC_HI6_RLWNM:
 4654| 	case PPC_HI6_RLWINM:
 4655| 		ra = (iword >> 16) & 31;
 4656| 		mb = (iword >> 6) & 31;
 4657| 		me = (iword >> 1) & 31;   
 4658| 		rc = iword & 1;
 4659| 		mask = 0;
 4660| 		for (;;) {
 4661| 			mask |= ((uint32_t)0x80000000 >> mb);
 4662| 			if (mb == me)
 4663| 				break;
 4664| 			mb ++; mb &= 31;
 4665| 		}
 4666| 		switch (main_opcode) {
 4667| 		case PPC_HI6_RLWNM:
 4668| 			ic->f = rc? instr(rlwnm_dot) : instr(rlwnm); break;
 4669| 		case PPC_HI6_RLWINM:
 4670| 			ic->f = rc? instr(rlwinm_dot) : instr(rlwinm); break;
 4671| 		}
 4672| 		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4673| 		ic->arg[1] = mask;
 4674| 		ic->arg[2] = (uint32_t)iword;
 4675| 		break;
 4676| 
 4677| 	case PPC_HI6_RLWIMI:
 4678| 		rs = (iword >> 21) & 31;
 4679| 		ra = (iword >> 16) & 31;
 4680| 		ic->f = instr(rlwimi);
 4681| 		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4682| 		ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4683| 		ic->arg[2] = (uint32_t)iword;
 4684| 		break;
 4685| 
 4686| 	case PPC_HI6_LMW:
 4687| 	case PPC_HI6_STMW:
 4688| 		/*  NOTE: Loads use rt, not rs.  */
 4689| 		rs = (iword >> 21) & 31;
 4690| 		ra = (iword >> 16) & 31;
 4691| 		ic->arg[0] = rs;
 4692| 		if (ra == 0)
 4693| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 4694| 		else
 4695| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4696| 		ic->arg[2] = (int32_t)(int16_t)iword;
 4697| 		switch (main_opcode) {
 4698| 		case PPC_HI6_LMW:
 4699| 			ic->f = instr(lmw);
 4700| 			break;
 4701| 		case PPC_HI6_STMW:
 4702| 			ic->f = instr(stmw);
 4703| 			break;
 4704| 		}
 4705| 		break;
 4706| 
 4707| 	case PPC_HI6_30:
 4708| 		xo = (iword >> 2) & 7;
 4709| 		switch (xo) {
 4710| 
 4711| 		case PPC_30_RLDICL:
 4712| 		case PPC_30_RLDICR:
 4713| 		case PPC_30_RLDIMI:
 4714| 			switch (xo) {
 4715| 			case PPC_30_RLDICL: ic->f = instr(rldicl); break;
 4716| 			case PPC_30_RLDICR: ic->f = instr(rldicr); break;
 4717| 			case PPC_30_RLDIMI: ic->f = instr(rldimi); break;
 4718| 			}
 4719| 			ic->arg[0] = iword;
 4720| 			if (cpu->cd.ppc.bits == 32) {
 4721| 				if (!cpu->translation_readahead)
 4722| 					fatal("TODO: rld* in 32-bit mode?\n");
 4723| 				goto bad;
 4724| 			}
 4725| 			break;
 4726| 
 4727| 		default:goto bad;
 4728| 		}
 4729| 		break;
 4730| 
 4731| 	case PPC_HI6_31:
 4732| 		xo = (iword >> 1) & 1023;
 4733| 		switch (xo) {
 4734| 
 4735| 		case PPC_31_CMPL:
 4736| 		case PPC_31_CMP:
 4737| 			bf = (iword >> 23) & 7;
 4738| 			l_bit = (iword >> 21) & 1;
 4739| 			ra = (iword >> 16) & 31;
 4740| 			rb = (iword >> 11) & 31;
 4741| 			if (xo == PPC_31_CMPL) {
 4742| 				if (l_bit)
 4743| 					ic->f = instr(cmpld);
 4744| 				else
 4745| 					ic->f = instr(cmplw);
 4746| 			} else {
 4747| 				if (l_bit)
 4748| 					ic->f = instr(cmpd);
 4749| 				else {
 4750| 					if (bf == 0)
 4751| 						ic->f = instr(cmpw_cr0);
 4752| 					else
 4753| 						ic->f = instr(cmpw);
 4754| 				}
 4755| 			}
 4756| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4757| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 4758| 			ic->arg[2] = 28 - 4*bf;
 4759| 			break;
 4760| 
 4761| 		case PPC_31_CNTLZW:
 4762| 			rs = (iword >> 21) & 31;
 4763| 			ra = (iword >> 16) & 31;
 4764| 			rc = iword & 1;
 4765| 			if (rc) {
 4766| 				if (!cpu->translation_readahead)
 4767| 					fatal("TODO: rc\n");
 4768| 				goto bad;
 4769| 			}
 4770| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4771| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4772| 			ic->f = instr(cntlzw);
 4773| 			break;
 4774| 
 4775| 		case PPC_31_MFSPR:
 4776| 			rt = (iword >> 21) & 31;
 4777| 			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
 4778| 			debug_spr_usage(cpu->pc, spr);
 4779| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 4780| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.spr[spr]);
 4781| 			switch (spr) {
 4782| 			// Reuse SPR_TB* for TBR_TB*:
 4783| 			case TBR_TBL: ic->f = instr(mftb); break;
 4784| 			case TBR_TBU: ic->f = instr(mftbu); break;
 4785| 			case SPR_PMC1:	ic->f = instr(mfspr_pmc1); break;
 4786| 			default:	ic->f = instr(mfspr);
 4787| 			}
 4788| 			break;
 4789| 
 4790| 		case PPC_31_MTSPR:
 4791| 			rs = (iword >> 21) & 31;
 4792| 			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
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

End with one line: `FIXDRAFT_PPCCNTLZWRC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL  edit 1 src/cpus/cpu_ppc_instr.c: old occurs 0 times
```

The previous edits:

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "\t\t\tif (rc) {\n\t\t\t\tif (!cpu->translation_readahead)\n\t\t\t\t\tfatal(\"TODO: rc\\n\");\n\t\t\t\t\tgoto bad;\n\t\t\t}\n\t\t\tic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);\n\t\t\tic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);\n\t\t\tic->f = instr(cntlzw);",
    "new": "\t\t\tic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);\n\t\t\tic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);\n\t\t\tic->f = rc ? instr(cntlzw_dot) : instr(cntlzw);",
    "why": "Implement Rc=1 condition for cntlzw by dispatching to the record-form handler."
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
