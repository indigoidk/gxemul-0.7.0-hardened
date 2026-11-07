# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armclrexundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armclrexundec`, state `open`)

**title:** src/cpus/cpu_arm_instr.c:4180-4181 -- CLREX (0xF57FF01F) matches none of the unconditional-space checks and reaches goto bad, stopping the CPU, though the model list includes an ARMv7 CORTEX-A5 -- CPU-STOP

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 4180-4181

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 5443a695..7abfac16 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -4160,6 +4160,12 @@ X(to_be_translated)
 			goto okay;
 		}
 
+		if (iword == 0xf57ff01f) {
+			/* #armclrexundec: clrex. Treat as NOP for now.  */
+			ic->f = instr(nop);
+			goto okay;
+		}
+
 		switch (main_opcode) {
 		case 0xa:
 		case 0xb:
```

## Every edited function, after the fix

### `src/cpus/cpu_arm_instr.c` -- post-edit lines 4061-5054 (`+` marks a line the diff added or the point of a deletion)

```c
 4061|  X(to_be_translated)
 4062|  {
 4063|  	uint32_t addr, low_pc, iword, imm = 0;
 4064|  	unsigned char *page;
 4065|  	unsigned char ib[4];
 4066|  	int condition_code, main_opcode, secondary_opcode, s_bit, rn, rd, r8;
 4067|  	int p_bit, u_bit, w_bit, l_bit, regform, rm, any_pc_reg; // , c, t
 4068|  	void (*samepage_function)(struct cpu *, struct arm_instr_call *);
 4069|  
 4070|  	/*  Figure out the address of the instruction:  */
 4071|  	low_pc = ((size_t)ic - (size_t)cpu->cd.arm.cur_ic_page)
 4072|  	    / sizeof(struct arm_instr_call);
 4073|  	addr = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
 4074|  	    ARM_INSTR_ALIGNMENT_SHIFT);
 4075|  	addr += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
 4076|  	cpu->pc = addr;
 4077|  	addr &= ~((1 << ARM_INSTR_ALIGNMENT_SHIFT) - 1);
 4078|  
 4079|  	/*  Read the instruction word from memory:  */
 4080|  	page = cpu->cd.arm.host_load[addr >> 12];
 4081|  
 4082|  	if (page != NULL) {
 4083|  		/*  fatal("TRANSLATION HIT! 0x%08x\n", addr);  */
 4084|  		memcpy(ib, page + (addr & 0xfff), sizeof(ib));
 4085|  	} else {
 4086|  		/*  fatal("TRANSLATION MISS! 0x%08x\n", addr);  */
 4087|  		if (!cpu->memory_rw(cpu, cpu->mem, addr, &ib[0],
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
 4163|+ 		if (iword == 0xf57ff01f) {
 4164|+ 			/* #armclrexundec: clrex. Treat as NOP for now.  */
 4165|+ 			ic->f = instr(nop);
 4166|+ 			goto okay;
 4167|+ 		}
 4168|+ 
 4169|  		switch (main_opcode) {
 4170|  		case 0xa:
 4171|  		case 0xb:
 4172|  			ic->f = instr(blx_imm);
 4173|  
 4174|  			/*  arg 1 = offset of current instruction  */
 4175|  			ic->arg[1] = addr & 0xffc;
 4176|  
 4177|  			/*  arg 0 = relative jump distance + 1 (to enable THUMB)  */
 4178|  			ic->arg[0] = (iword & 0x00ffffff) << 2;
 4179|  			/*  Sign-extend:  */
 4180|  			if (ic->arg[0] & 0x02000000)
 4181|  				ic->arg[0] |= 0xfc000000;
 4182|  			if (main_opcode == 0xb)
 4183|  				ic->arg[0] += 2;
 4184|  			ic->arg[0] = (int32_t)(ic->arg[0] + 8 + 1);
 4185|  			break;
 4186|  		default:
 4187|  			goto bad;
 4188|  		}
 4189|  		goto okay;
 4190|  	}
 4191|  
 4192|  	switch (main_opcode) {
 4193|  
 4194|  	case 0x0:
 4195|  	case 0x1:
 4196|  	case 0x2:
 4197|  	case 0x3:
 4198|  		/*  Check special cases first:  */
 4199|  		if ((iword & 0x0ff00fff) == 0x01900f9f) {
 4200|  			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4201|  			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4202|  			ic->arg[2] = 0;
 4203|  
 4204|  			if (rd == ARM_PC || rn == ARM_PC) {
 4205|  				if (!cpu->translation_readahead)
 4206|  					fatal("ldrex with pc register: TODO\n");
 4207|  				goto bad;
 4208|  			}
 4209|  			
 4210|  			ic->f = cond_instr(ldrex);
 4211|  			break;
 4212|  		}
 4213|  
 4214|  		if ((iword & 0x0ff00ff0) == 0x01800f90) {
 4215|  			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
 4216|  			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
 4217|  			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
 4218|  
 4219|  			if (rd == ARM_PC || rm == ARM_PC || rn == ARM_PC ||
 4220|  			    rd == rm || rd == rn) {
 4221|  				if (!cpu->translation_readahead)
 4222|  					fatal("strex with bad register: TODO\n");
 4223|  				goto bad;
 4224|  			}
 4225|  			
 4226|  			ic->f = cond_instr(strex);
 4227|  			break;
 4228|  		}
     | [... lines 4229-5024 not shown ...]
 5025|  			ic->f = cond_instr(cdp);
 5026|  		}
 5027|  		if (iword == 0xee070f9a)
 5028|  			cpu->cd.arm.combination_check =
 5029|  			    COMBINE(netbsd_cacheclean);
 5030|  		break;
 5031|  
 5032|  	case 0xf:
 5033|  		/*  SWI:  */
 5034|  		/*  Default handler:  */
 5035|  		ic->f = cond_instr(swi);
 5036|  		ic->arg[0] = addr & 0xfff;
 5037|  		if (iword == 0xef8c64eb) {
 5038|  			/*  Hack for rebooting a machine:  */
 5039|  			ic->f = instr(reboot);
 5040|  		} else if (iword == 0xef8c64be) {
 5041|  			/*  Hack for openfirmware prom emulation:  */
 5042|  			ic->f = instr(openfirmware);
 5043|  		}
 5044|  		break;
 5045|  
 5046|  	default:goto bad;
 5047|  	}
 5048|  
 5049|  okay:
 5050|  
 5051|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5052|  #include "cpu_dyntrans.c" 
 5053|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5054|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMCLREXUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMCLREXUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
