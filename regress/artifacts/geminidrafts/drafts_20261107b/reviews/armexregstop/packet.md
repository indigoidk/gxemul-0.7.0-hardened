# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armexregstop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armexregstop`, state `open`)

**title:** src/cpus/cpu_arm_instr.c:4198-4201,4213-4217 -- LDREX naming PC, or STREX naming PC or a repeated register, reaches goto bad at decode, before the condition is tested, and stops the CPU; the operands are UNPREDICTABLE, which the ARM ARM says must not halt the processor -- CPU-STOP

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 4201| 				goto bad;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 5443a695..48d1f15f 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -4195,11 +4195,7 @@ X(to_be_translated)
 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 			ic->arg[2] = 0;
 
-			if (rd == ARM_PC || rn == ARM_PC) {
-				if (!cpu->translation_readahead)
-					fatal("ldrex with pc register: TODO\n");
-				goto bad;
-			}
+			/* #armexregstop: UNPREDICTABLE operands must not halt the CPU. */
 			
 			ic->f = cond_instr(ldrex);
 			break;
@@ -4210,12 +4206,7 @@ X(to_be_translated)
 			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
 
-			if (rd == ARM_PC || rm == ARM_PC || rn == ARM_PC ||
-			    rd == rm || rd == rn) {
-				if (!cpu->translation_readahead)
-					fatal("strex with bad register: TODO\n");
-				goto bad;
-			}
+			/* #armexregstop: UNPREDICTABLE operands must not halt the CPU. */
 			
 			ic->f = cond_instr(strex);
 			break;
```

## Every edited function, after the fix

### `src/cpus/cpu_arm_instr.c` -- post-edit lines 4061-5039 (`+` marks a line the diff added or the point of a deletion)

```c
 4061|  X(to_be_translated)
 4062|  {
 4063|  	uint32_t addr, low_pc, iword, imm = 0;
 4064|  	unsigned char *page;
 4065|  	unsigned char ib[4];
     | [... lines 4066-4087 not shown ...]
 4088|  		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
 4089|  			fatal("to_be_translated(): "
 4090|  			    "read failed: TODO\n");
 4091|  			return;
 4092|  		}
 4093|  	}
 4094|  
 4095|  	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 4096|  		iword = READ_WORD_LE(ib);
 4097|  	else
 4098|  		iword = READ_WORD_BE(ib);
 4099|  
 4100|  
 4101|  #define DYNTRANS_TO_BE_TRANSLATED_HEAD
 4102|  #include "cpu_dyntrans.c"
 4103|  #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
 4104|  
 4105|  
 4106|  	/*  The idea of taking bits 27..24 was found here:
 4107|  	    http://armphetamine.sourceforge.net/oldinfo.html  */
 4108|  	condition_code = iword >> 28;
 4109|  	main_opcode = (iword >> 24) & 15;
 4110|  	secondary_opcode = (iword >> 21) & 15;
 4111|  	u_bit = iword & 0x00800000;
 4112|  	w_bit = iword & 0x00200000;
 4113|  	s_bit = l_bit = iword & 0x00100000;
 4114|  	rn    = (iword >> 16) & 15;
 4115|  	rd    = (iword >> 12) & 15;
 4116|  	r8    = (iword >> 8) & 15;
 4117|  	// c     = (iword >> 7) & 31;
 4118|  	// t     = (iword >> 4) & 7;
 4119|  	rm    = iword & 15;
 4120|  
 4121|  	/*
 4122|  	 *  Translate the instruction:
 4123|  	 */
 4124|  
 4125|  	if ((iword >> 28) == 0xf) {
 4126|  		/*  The "never" condition is nowadays used for special encodings.  */
 4127|  		if ((iword & 0xfc70f000) == 0xf450f000) {
 4128|  			/*  Preload:  TODO.  Treat as NOP for now.  */
 4129|  			ic->f = instr(nop);
 4130|  			goto okay;
 4131|  		}
 4132|  
 4133|  		if (iword == 0xf10c0040) {
 4134|  			/*  cpsid f. Treat as NOP for now.  */
 4135|  			ic->f = instr(nop);
 4136|  			goto okay;
 4137|  		}
 4138|  
 4139|  		if (iword == 0xf10c0080) {
 4140|  			/*  cpsid i. Treat as NOP for now.  */
 4141|  			ic->f = instr(nop);
 4142|  			goto okay;
 4143|  		}
 4144|  
 4145|  		if (iword == 0xf57ff04f) {
 4146|  			/*  dsb sy. Treat as NOP for now.  */
 4147|  			ic->f = instr(nop);
 4148|  			goto okay;
 4149|  		}
 4150|  
 4151|  		if (iword == 0xf57ff05f) {
 4152|  			/*  dmb sy. Treat as NOP for now.  */
 4153|  			ic->f = instr(nop);
 4154|  			goto okay;
 4155|  		}
 4156|  
 4157|  		if (iword == 0xf57ff06f) {
 4158|  			/*  isb sy. Treat as NOP for now.  */
 4159|  			ic->f = instr(nop);
 4160|  			goto okay;
 4161|  		}
 4162|  
 4163|  		switch (main_opcode) {
 4164|  		case 0xa:
 4165|  		case 0xb:
 4166|  			ic->f = instr(blx_imm);
 4167|  
 4168|  			/*  arg 1 = offset of current instruction  */
 4169|  			ic->arg[1] = addr & 0xffc;
 4170|  
 4171|  			/*  arg 0 = relative jump distance + 1 (to enable THUMB)  */
 4172|  			ic->arg[0] = (iword & 0x00ffffff) << 2;
 4173|  			/*  Sign-extend:  */
 4174|  			if (ic->arg[0] & 0x02000000)
 4175|  				ic->arg[0] |= 0xfc000000;
 4176|  			if (main_opcode == 0xb)
 4177|  				ic->arg[0] += 2;
 4178|  			ic->arg[0] = (int32_t)(ic->arg[0] + 8 + 1);
 4179|  			break;
 4180|  		default:
 4181|  			goto bad;
 4182|  		}
 4183|  		goto okay;
 4184|  	}
 4185|  
 4186|  	switch (main_opcode) {
 4187|  
 4188|  	case 0x0:
 4189|  	case 0x1:
 4190|  	case 0x2:
 4191|  	case 0x3:
 4192|  		/*  Check special cases first:  */
 4193|  		if ((iword & 0x0ff00fff) == 0x01900f9f) {
 4194|  			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4195|  			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4196|  			ic->arg[2] = 0;
 4197|  
 4198|+ 			/* #armexregstop: UNPREDICTABLE operands must not halt the CPU. */
 4199|  			
 4200|  			ic->f = cond_instr(ldrex);
 4201|  			break;
 4202|  		}
 4203|  
 4204|  		if ((iword & 0x0ff00ff0) == 0x01800f90) {
 4205|  			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4206|  			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4207|  			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
 4208|  
 4209|+ 			/* #armexregstop: UNPREDICTABLE operands must not halt the CPU. */
 4210|  			
 4211|  			ic->f = cond_instr(strex);
 4212|  			break;
 4213|  		}
 4214|  
 4215|  		if ((iword & 0x0ff000f0) == 0x00600090) {
 4216|  			ic->arg[0] = iword;
 4217|  			ic->f = cond_instr(mls);
 4218|  			break;
 4219|  		}
 4220|  		
 4221|  		if ((iword & 0x0fc000f0) == 0x00000090) {
 4222|  			/*
 4223|  			 *  Multiplication:
 4224|  			 *  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])
 4225|  			 */
 4226|  			if (iword & 0x00200000) {
 4227|  				if (s_bit)
 4228|  					ic->f = cond_instr(mlas);
 4229|  				else
 4230|  					ic->f = cond_instr(mla);
 4231|  				ic->arg[0] = iword;
 4232|  			} else {
 4233|  				if (s_bit)
 4234|  					ic->f = cond_instr(muls);
 4235|  				else
 4236|  					ic->f = cond_instr(mul);
 4237|  				/*  NOTE: rn means rd in this case:  */
 4238|  				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
 4239|  				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
 4240|  				ic->arg[2] = (size_t)(&cpu->cd.arm.r[r8]);
 4241|  			}
 4242|  			break;
 4243|  		}
 4244|  		if ((iword & 0x0f8000f0) == 0x00800090) {
 4245|  			/*  Long multiplication:  */
 4246|  			if (s_bit) {
 4247|  				if (!cpu->translation_readahead)
 4248|  					fatal("TODO: sbit mull\n");
 4249|  				goto bad;
 4250|  			}
 4251|  			ic->f = cond_instr(mull);
 4252|  			ic->arg[0] = iword;
 4253|  			break;
 4254|  		}
 4255|  		if ((iword & 0x0f900ff0) == 0x01000050) {
 4256|  			if (!cpu->translation_readahead)
 4257|  				fatal("TODO: q{,d}{add,sub}\n");
 4258|  			goto bad;
 4259|  		}
 4260|  		if ((iword & 0x0ff000d0) == 0x01200010) {
 4261|  			/*  bx or blx  */
 4262|  			if (iword & 0x20)
 4263|  				ic->f = cond_instr(blx_reg);
 4264|  			else {
 4265|  				if (cpu->machine->show_trace_tree &&
 4266|  				    rm == ARM_LR)
 4267|  					ic->f = cond_instr(bx_trace);
 4268|  				else
 4269|  					ic->f = cond_instr(bx);
     | [... lines 4270-5009 not shown ...]
 5010|  			ic->f = cond_instr(cdp);
 5011|  		}
 5012|  		if (iword == 0xee070f9a)
 5013|  			cpu->cd.arm.combination_check =
 5014|  			    COMBINE(netbsd_cacheclean);
 5015|  		break;
 5016|  
 5017|  	case 0xf:
 5018|  		/*  SWI:  */
 5019|  		/*  Default handler:  */
 5020|  		ic->f = cond_instr(swi);
 5021|  		ic->arg[0] = addr & 0xfff;
 5022|  		if (iword == 0xef8c64eb) {
 5023|  			/*  Hack for rebooting a machine:  */
 5024|  			ic->f = instr(reboot);
 5025|  		} else if (iword == 0xef8c64be) {
 5026|  			/*  Hack for openfirmware prom emulation:  */
 5027|  			ic->f = instr(openfirmware);
 5028|  		}
 5029|  		break;
 5030|  
 5031|  	default:goto bad;
 5032|  	}
 5033|  
 5034|  okay:
 5035|  
 5036|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5037|  #include "cpu_dyntrans.c" 
 5038|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5039|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMEXREGSTOP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMEXREGSTOP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
