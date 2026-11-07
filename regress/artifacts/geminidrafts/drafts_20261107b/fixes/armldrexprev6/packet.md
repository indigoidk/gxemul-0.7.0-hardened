# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armldrexprev6` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armldrexprev6`, state `open`, severity `MED`)

**title:** src/cpus/cpu_arm_instr.c:4204,4220 -- aligned word LDREX and STREX are installed with no CPU-version test, so pre-ARMv6 models (the SA1110 that testarm and hpcarm select) execute them where the instructions exist only from version 6 and Undefined is owed -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- requires an ARMv6 version check to prevent executing undefined instructions.

## The code at the cited lines

### `src/cpus/cpu_arm_instr.c` around the row's cited line 4204 (HEAD 8d9df658, lines 4084-4324)

```c
 4084| 		memcpy(ib, page + (addr & 0xfff), sizeof(ib));
 4085| 	} else {
 4086| 		/*  fatal("TRANSLATION MISS! 0x%08x\n", addr);  */
 4087| 		if (!cpu->memory_rw(cpu, cpu->mem, addr, &ib[0],
 4088| 		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
 4089| 			fatal("to_be_translated(): "
 4090| 			    "read failed: TODO\n");
 4091| 			return;
 4092| 		}
 4093| 	}
 4094| 
 4095| 	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 4096| 		iword = READ_WORD_LE(ib);
 4097| 	else
 4098| 		iword = READ_WORD_BE(ib);
 4099| 
 4100| 
 4101| #define DYNTRANS_TO_BE_TRANSLATED_HEAD
 4102| #include "cpu_dyntrans.c"
 4103| #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
 4104| 
 4105| 
 4106| 	/*  The idea of taking bits 27..24 was found here:
 4107| 	    http://armphetamine.sourceforge.net/oldinfo.html  */
 4108| 	condition_code = iword >> 28;
 4109| 	main_opcode = (iword >> 24) & 15;
 4110| 	secondary_opcode = (iword >> 21) & 15;
 4111| 	u_bit = iword & 0x00800000;
 4112| 	w_bit = iword & 0x00200000;
 4113| 	s_bit = l_bit = iword & 0x00100000;
 4114| 	rn    = (iword >> 16) & 15;
 4115| 	rd    = (iword >> 12) & 15;
 4116| 	r8    = (iword >> 8) & 15;
 4117| 	// c     = (iword >> 7) & 31;
 4118| 	// t     = (iword >> 4) & 7;
 4119| 	rm    = iword & 15;
 4120| 
 4121| 	/*
 4122| 	 *  Translate the instruction:
 4123| 	 */
 4124| 
 4125| 	if ((iword >> 28) == 0xf) {
 4126| 		/*  The "never" condition is nowadays used for special encodings.  */
 4127| 		if ((iword & 0xfc70f000) == 0xf450f000) {
 4128| 			/*  Preload:  TODO.  Treat as NOP for now.  */
 4129| 			ic->f = instr(nop);
 4130| 			goto okay;
 4131| 		}
 4132| 
 4133| 		if (iword == 0xf10c0040) {
 4134| 			/*  cpsid f. Treat as NOP for now.  */
 4135| 			ic->f = instr(nop);
 4136| 			goto okay;
 4137| 		}
 4138| 
 4139| 		if (iword == 0xf10c0080) {
 4140| 			/*  cpsid i. Treat as NOP for now.  */
 4141| 			ic->f = instr(nop);
 4142| 			goto okay;
 4143| 		}
 4144| 
 4145| 		if (iword == 0xf57ff04f) {
 4146| 			/*  dsb sy. Treat as NOP for now.  */
 4147| 			ic->f = instr(nop);
 4148| 			goto okay;
 4149| 		}
 4150| 
 4151| 		if (iword == 0xf57ff05f) {
 4152| 			/*  dmb sy. Treat as NOP for now.  */
 4153| 			ic->f = instr(nop);
 4154| 			goto okay;
 4155| 		}
 4156| 
 4157| 		if (iword == 0xf57ff06f) {
 4158| 			/*  isb sy. Treat as NOP for now.  */
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
 4250| 			}
 4251| 			break;
 4252| 		}
 4253| 		if ((iword & 0x0f8000f0) == 0x00800090) {
 4254| 			/*  Long multiplication:  */
 4255| 			if (s_bit) {
 4256| 				if (!cpu->translation_readahead)
 4257| 					fatal("TODO: sbit mull\n");
 4258| 				goto bad;
 4259| 			}
 4260| 			ic->f = cond_instr(mull);
 4261| 			ic->arg[0] = iword;
 4262| 			break;
 4263| 		}
 4264| 		if ((iword & 0x0f900ff0) == 0x01000050) {
 4265| 			if (!cpu->translation_readahead)
 4266| 				fatal("TODO: q{,d}{add,sub}\n");
 4267| 			goto bad;
 4268| 		}
 4269| 		if ((iword & 0x0ff000d0) == 0x01200010) {
 4270| 			/*  bx or blx  */
 4271| 			if (iword & 0x20)
 4272| 				ic->f = cond_instr(blx_reg);
 4273| 			else {
 4274| 				if (cpu->machine->show_trace_tree &&
 4275| 				    rm == ARM_LR)
 4276| 					ic->f = cond_instr(bx_trace);
 4277| 				else
 4278| 					ic->f = cond_instr(bx);
 4279| 			}
 4280| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
 4281| 			ic->arg[2] = (addr & 0xffc) + 4;
 4282|                         break;
 4283|                 }
 4284| 		if ((iword & 0x0fb00ff0) == 0x1000090) {
 4285| 			if (iword & 0x00400000)
 4286| 				ic->f = cond_instr(swpb);
 4287| 			else
 4288| 				ic->f = cond_instr(swp);
 4289| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4290| 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
 4291| 			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rn]);
 4292| 			break;
 4293| 		}
 4294| 		if ((iword & 0x0fff0ff0) == 0x016f0f10) {
 4295| 			ic->f = cond_instr(clz);
 4296| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
 4297| 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rd]);
 4298| 			break;
 4299| 		}
 4300| 		if ((iword & 0x0ff00090) == 0x01000080) {
 4301| 			/*  TODO: smlaXX  */
 4302| 			goto bad;
 4303| 		}
 4304| 		if ((iword & 0x0ff00090) == 0x01400080) {
 4305| 			/*  TODO: smlalY  */
 4306| 			goto bad;
 4307| 		}
 4308| 		if ((iword & 0x0ff000b0) == 0x01200080) {
 4309| 			/*  TODO: smlawY  */
 4310| 			goto bad;
 4311| 		}
 4312| 		if ((iword & 0x0ff0f090) == 0x01600080) {
 4313| 			/*  smulXY (16-bit * 16-bit => 32-bit)  */
 4314| 			switch (iword & 0x60) {
 4315| 			case 0x00: ic->f = cond_instr(smulbb); break;
 4316| 			case 0x20: ic->f = cond_instr(smultb); break;
 4317| 			case 0x40: ic->f = cond_instr(smulbt); break;
 4318| 			default:   ic->f = cond_instr(smultt); break;
 4319| 			}
 4320| 			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
 4321| 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[r8]);
 4322| 			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rn]); /*  Rd  */
 4323| 			break;
 4324| 		}
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

End with one line: `FIXDRAFT_ARMLDREXPREV6: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- lines 4204 and 4220 show LDREX and STREX installed without version checks, but the fields to check the CPU architecture version (e.g., in the `cpu` or `cpu->cd.arm` structures) are not visible in this snippet.
The fix deliberately does not change anything because the necessary CPU version field is missing from the provided code snippet, so an accurate check cannot be drafted.
FIXDRAFT_ARMLDREXPREV6: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

(no definition of a name you used was found in HEAD's src/ -- the name may not exist)


## Added by the coordinator: the definitions your description pointed at

Your previous reply described what was missing without naming it; these are the definitions HEAD has for it.  If the
model carries NO field that distinguishes the architecture version you need, say so as UNSETTLED -- do not invent one.

### `src/include/cpu_arm.h` lines 38-62 (the ARM CPU type each cpu carries as cpu->cd.arm.cpu_type)

```c
   38| 
   39| /*  ARM CPU types:  */
   40| struct arm_cpu_type_def {
   41| 	const char	*name;
   42| 	uint32_t	cpu_id;
   43| 	int		flags;
   44| 	int		icache_shift;
   45| 	int		iway;
   46| 	int		dcache_shift;
   47| 	int		dway;
   48| };
   49| 
   50| 
   51| #define	ARM_SL			10
   52| #define	ARM_FP			11
   53| #define	ARM_IP			12
   54| #define	ARM_SP			13
   55| #define	ARM_LR			14
   56| #define	ARM_PC			15
   57| #define	N_ARM_REGS		16
   58| 
   59| #define	ARM_REG_NAMES		{				\
   60| 	"r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7",		\
   61| 	"r8", "r9", "sl", "fp", "ip", "sp", "lr", "pc"  }
   62| 
```

Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.
