# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armldrexprev6` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armldrexprev6`, state `open`)

**title:** src/cpus/cpu_arm_instr.c:4204,4220 -- aligned word LDREX and STREX are installed with no CPU-version test, so pre-ARMv6 models (the SA1110 that testarm and hpcarm select) execute them where the instructions exist only from version 6 and Undefined is owed -- WRONG-RESULT

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 4204

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 5443a695..475f936e 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -4201,6 +4201,7 @@ X(to_be_translated)
 				goto bad;
 			}
 			
+			/* #armldrexprev6: Requires ARMv6 version check to goto bad; */
 			ic->f = cond_instr(ldrex);
 			break;
 		}
@@ -4217,6 +4218,7 @@ X(to_be_translated)
 				goto bad;
 			}
 			
+			/* #armldrexprev6: Requires ARMv6 version check to goto bad; */
 			ic->f = cond_instr(strex);
 			break;
 		}
```

## Every edited function, after the fix

### `src/cpus/cpu_arm_instr.c` -- post-edit lines 4061-5050 (`+` marks a line the diff added or the point of a deletion)

```c
 4061|  X(to_be_translated)
 4062|  {
 4063|  	uint32_t addr, low_pc, iword, imm = 0;
 4064|  	unsigned char *page;
 4065|  	unsigned char ib[4];
     | [... lines 4066-4093 not shown ...]
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
 4198|  			if (rd == ARM_PC || rn == ARM_PC) {
 4199|  				if (!cpu->translation_readahead)
 4200|  					fatal("ldrex with pc register: TODO\n");
 4201|  				goto bad;
 4202|  			}
 4203|  			
 4204|+ 			/* #armldrexprev6: Requires ARMv6 version check to goto bad; */
 4205|  			ic->f = cond_instr(ldrex);
 4206|  			break;
 4207|  		}
 4208|  
 4209|  		if ((iword & 0x0ff00ff0) == 0x01800f90) {
 4210|  			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4211|  			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4212|  			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
 4213|  
 4214|  			if (rd == ARM_PC || rm == ARM_PC || rn == ARM_PC ||
 4215|  			    rd == rm || rd == rn) {
 4216|  				if (!cpu->translation_readahead)
 4217|  					fatal("strex with bad register: TODO\n");
 4218|  				goto bad;
 4219|  			}
 4220|  			
 4221|+ 			/* #armldrexprev6: Requires ARMv6 version check to goto bad; */
 4222|  			ic->f = cond_instr(strex);
 4223|  			break;
 4224|  		}
 4225|  
 4226|  		if ((iword & 0x0ff000f0) == 0x00600090) {
 4227|  			ic->arg[0] = iword;
 4228|  			ic->f = cond_instr(mls);
 4229|  			break;
 4230|  		}
 4231|  		
 4232|  		if ((iword & 0x0fc000f0) == 0x00000090) {
 4233|  			/*
 4234|  			 *  Multiplication:
 4235|  			 *  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])
 4236|  			 */
 4237|  			if (iword & 0x00200000) {
 4238|  				if (s_bit)
 4239|  					ic->f = cond_instr(mlas);
 4240|  				else
 4241|  					ic->f = cond_instr(mla);
 4242|  				ic->arg[0] = iword;
 4243|  			} else {
 4244|  				if (s_bit)
 4245|  					ic->f = cond_instr(muls);
 4246|  				else
 4247|  					ic->f = cond_instr(mul);
 4248|  				/*  NOTE: rn means rd in this case:  */
 4249|  				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
 4250|  				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
 4251|  				ic->arg[2] = (size_t)(&cpu->cd.arm.r[r8]);
 4252|  			}
 4253|  			break;
 4254|  		}
 4255|  		if ((iword & 0x0f8000f0) == 0x00800090) {
 4256|  			/*  Long multiplication:  */
 4257|  			if (s_bit) {
 4258|  				if (!cpu->translation_readahead)
 4259|  					fatal("TODO: sbit mull\n");
 4260|  				goto bad;
 4261|  			}
 4262|  			ic->f = cond_instr(mull);
 4263|  			ic->arg[0] = iword;
 4264|  			break;
 4265|  		}
 4266|  		if ((iword & 0x0f900ff0) == 0x01000050) {
 4267|  			if (!cpu->translation_readahead)
 4268|  				fatal("TODO: q{,d}{add,sub}\n");
 4269|  			goto bad;
 4270|  		}
 4271|  		if ((iword & 0x0ff000d0) == 0x01200010) {
 4272|  			/*  bx or blx  */
 4273|  			if (iword & 0x20)
 4274|  				ic->f = cond_instr(blx_reg);
 4275|  			else {
 4276|  				if (cpu->machine->show_trace_tree &&
 4277|  				    rm == ARM_LR)
 4278|  					ic->f = cond_instr(bx_trace);
 4279|  				else
 4280|  					ic->f = cond_instr(bx);
 4281|  			}
     | [... lines 4282-5020 not shown ...]
 5021|  			ic->f = cond_instr(cdp);
 5022|  		}
 5023|  		if (iword == 0xee070f9a)
 5024|  			cpu->cd.arm.combination_check =
 5025|  			    COMBINE(netbsd_cacheclean);
 5026|  		break;
 5027|  
 5028|  	case 0xf:
 5029|  		/*  SWI:  */
 5030|  		/*  Default handler:  */
 5031|  		ic->f = cond_instr(swi);
 5032|  		ic->arg[0] = addr & 0xfff;
 5033|  		if (iword == 0xef8c64eb) {
 5034|  			/*  Hack for rebooting a machine:  */
 5035|  			ic->f = instr(reboot);
 5036|  		} else if (iword == 0xef8c64be) {
 5037|  			/*  Hack for openfirmware prom emulation:  */
 5038|  			ic->f = instr(openfirmware);
 5039|  		}
 5040|  		break;
 5041|  
 5042|  	default:goto bad;
 5043|  	}
 5044|  
 5045|  okay:
 5046|  
 5047|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5048|  #include "cpu_dyntrans.c" 
 5049|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5050|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMLDREXPREV6: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMLDREXPREV6: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
