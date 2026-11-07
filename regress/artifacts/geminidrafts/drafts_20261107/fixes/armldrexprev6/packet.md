# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armldrexprev6` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armldrexprev6`, state `open`, severity `MED`)

**title:** src/cpus/cpu_arm_instr.c:4204,4220 -- aligned word LDREX and STREX are installed with no CPU-version test, so pre-ARMv6 models (the SA1110 that testarm and hpcarm select) execute them where the instructions exist only from version 6 and Undefined is owed -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- requires an ARMv6 version check to prevent executing undefined instructions.

## The code at the cited lines

### `src/cpus/cpu_arm_instr.c` around the row's cited line 4204 (HEAD 2d25df65, lines 4159-4249)

```c
 4159| 			ic->f = instr(nop);
 4160| 			goto okay;
 4161| 		}
 4162| 
 4163| 		switch (main_opcode) {
 4164| 		case 0xa:
 4165| 		case 0xb:
 4166| 			ic->f = instr(blx_imm);
 4167| 
 4168| 			/*  arg 1 = offset of current instruction  */
 4169| 			ic->arg[1] = addr & 0xffc;
 4170| 
 4171| 			/*  arg 0 = relative jump distance + 1 (to enable THUMB)  */
 4172| 			ic->arg[0] = (iword & 0x00ffffff) << 2;
 4173| 			/*  Sign-extend:  */
 4174| 			if (ic->arg[0] & 0x02000000)
 4175| 				ic->arg[0] |= 0xfc000000;
 4176| 			if (main_opcode == 0xb)
 4177| 				ic->arg[0] += 2;
 4178| 			ic->arg[0] = (int32_t)(ic->arg[0] + 8 + 1);
 4179| 			break;
 4180| 		default:
 4181| 			goto bad;
 4182| 		}
 4183| 		goto okay;
 4184| 	}
 4185| 
 4186| 	switch (main_opcode) {
 4187| 
 4188| 	case 0x0:
 4189| 	case 0x1:
 4190| 	case 0x2:
 4191| 	case 0x3:
 4192| 		/*  Check special cases first:  */
 4193| 		if ((iword & 0x0ff00fff) == 0x01900f9f) {
 4194| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4195| 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4196| 			ic->arg[2] = 0;
 4197| 
 4198| 			if (rd == ARM_PC || rn == ARM_PC) {
 4199| 				if (!cpu->translation_readahead)
 4200| 					fatal("ldrex with pc register: TODO\n");
 4201| 				goto bad;
 4202| 			}
 4203| 			
 4204| 			ic->f = cond_instr(ldrex);
 4205| 			break;
 4206| 		}
 4207| 
 4208| 		if ((iword & 0x0ff00ff0) == 0x01800f90) {
 4209| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4210| 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4211| 			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
 4212| 
 4213| 			if (rd == ARM_PC || rm == ARM_PC || rn == ARM_PC ||
 4214| 			    rd == rm || rd == rn) {
 4215| 				if (!cpu->translation_readahead)
 4216| 					fatal("strex with bad register: TODO\n");
 4217| 				goto bad;
 4218| 			}
 4219| 			
 4220| 			ic->f = cond_instr(strex);
 4221| 			break;
 4222| 		}
 4223| 
 4224| 		if ((iword & 0x0ff000f0) == 0x00600090) {
 4225| 			ic->arg[0] = iword;
 4226| 			ic->f = cond_instr(mls);
 4227| 			break;
 4228| 		}
 4229| 		
 4230| 		if ((iword & 0x0fc000f0) == 0x00000090) {
 4231| 			/*
 4232| 			 *  Multiplication:
 4233| 			 *  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])
 4234| 			 */
 4235| 			if (iword & 0x00200000) {
 4236| 				if (s_bit)
 4237| 					ic->f = cond_instr(mlas);
 4238| 				else
 4239| 					ic->f = cond_instr(mla);
 4240| 				ic->arg[0] = iword;
 4241| 			} else {
 4242| 				if (s_bit)
 4243| 					ic->f = cond_instr(muls);
 4244| 				else
 4245| 					ic->f = cond_instr(mul);
 4246| 				/*  NOTE: rn means rd in this case:  */
 4247| 				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
 4248| 				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
 4249| 				ic->arg[2] = (size_t)(&cpu->cd.arm.r[r8]);
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_ARMLDREXPREV6: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
