# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kcarryundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kcarryundec`, state `open`, severity `MED`)

**title:** cpus/cpu_m88k_instr.c register-form decode -- triadic opcodes 0x71-0x77 (add.ci/.co/.cio, signed sub with overflow trap, sub.ci/.co/.cio) have no case and reach `goto bad` -- CPU-STOP (any privilege; includes the manual's `sub.co r0,r0,r0` idiom)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T121 (class CPU-STOP; reach U, user mode; effort: small; report rows: A1-57, A7-25, A(c)#9, C U7).  Source URLs: https://github.com/Randrianasulu/GXemul/commit/9bfc91e, https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3660-3716, :3815; src/cpus/cpu_dyntrans.c:2014.  Portable fix: yes -- port r6577(n) X(sub) for 0x74; design the carry forms 0x71-0x73 / 0x75-0x77 (absent upstream too).  Filing check (TRIAGE.md): 0 hits; nearest umbrella `cpusexitsweep`.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port r6577(n) X(sub) for 0x74 and design carry forms

## The code at the cited lines

### `src/cpus/cpu_m88k_instr.c` around the row's cited line 3660 (HEAD 2d25df65, lines 3615-3705)

```c
 3615| 
 3616| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3617| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3618| 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3619| 
 3620| 			if (op == 0 || op == 1) {
 3621| 				/*  ld or st:  */
 3622| 				ic->f = m88k_loadstore[ opsize
 3623| 				    + (op==1? M88K_LOADSTORE_STORE : 0)
 3624| 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3625| 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3626| 				       M88K_LOADSTORE_ENDIANNESS : 0)
 3627| 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 3628| 				    + (user? M88K_LOADSTORE_USR : 0)
 3629| 				    + M88K_LOADSTORE_REGISTEROFFSET ];
 3630| 
 3631| 				if (d == M88K_ZERO_REG && op == 0)
 3632| 					ic->arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
 3633| 
 3634| 				if (opsize == 3 && d == 31) {
 3635| 					fatal("m88k load/store of register "
 3636| 					    "pair r31/r0: TODO\n");
 3637| 					goto bad;
 3638| 				}
 3639| 			} else if (op == 2) {
 3640| 				/*  lda:  */
 3641| 				if (scaled) {
 3642| 					switch (opsize) {
 3643| 					case 0: ic->f = instr(addu); break;
 3644| 					case 1: ic->f = instr(lda_reg_2); break;
 3645| 					case 2: ic->f = instr(lda_reg_4); break;
 3646| 					case 3: ic->f = instr(lda_reg_8); break;
 3647| 					}
 3648| 				} else {
 3649| 					ic->f = instr(addu);
 3650| 				}
 3651| 				if (d == M88K_ZERO_REG)
 3652| 					ic->f = instr(nop);
 3653| 			} else {
 3654| 				/*  xmem:  */
 3655| 				ic->f = instr(xmem_slow);
 3656| 				ic->arg[0] = iword;
 3657| 				if (d == M88K_ZERO_REG)
 3658| 					ic->f = instr(nop);
 3659| 			}
 3660| 		} else switch ((iword >> 8) & 0xff) {
 3661| 		case 0x40:	/*  and    */
 3662| 		case 0x44:	/*  and.c  */
 3663| 		case 0x50:	/*  xor    */
 3664| 		case 0x54:	/*  xor.c  */
 3665| 		case 0x58:	/*  or     */
 3666| 		case 0x5c:	/*  or.c   */
 3667| 		case 0x60:	/*  addu   */
 3668| 		case 0x61:	/*  addu.co  */
 3669| 		case 0x62:	/*  addu.ci  */
 3670| 		case 0x63:	/*  addu.cio */
 3671| 		case 0x64:	/*  subu   */
 3672| 		case 0x65:	/*  subu.co  */
 3673| 		case 0x66:	/*  subu.ci  */
 3674| 		case 0x67:	/*  subu.cio */
 3675| 		case 0x68:	/*  divu   */
 3676| 		case 0x6c:	/*  mul    */
 3677| 		case 0x70:	/*  add    */
 3678| 		case 0x78:	/*  div    */
 3679| 		case 0x7c:	/*  cmp    */
 3680| 		case 0x80:	/*  clr    */
 3681| 		case 0x88:	/*  set    */
 3682| 		case 0x90:	/*  ext    */
 3683| 		case 0x98:	/*  extu   */
 3684| 		case 0xa0:	/*  mak    */
 3685| 		case 0xa8:	/*  rot    */
 3686| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3687| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3688| 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3689| 
 3690| 			switch ((iword >> 8) & 0xff) {
 3691| 			case 0x40: ic->f = instr(and);   break;
 3692| 			case 0x44: ic->f = instr(and_c); break;
 3693| 			case 0x50: ic->f = instr(xor);   break;
 3694| 			case 0x54: ic->f = instr(xor_c); break;
 3695| 			case 0x58: ic->f = instr(or);    break;
 3696| 			case 0x5c: ic->f = instr(or_c);  break;
 3697| 			case 0x60: ic->f = instr(addu);  break;
 3698| 			case 0x61: ic->f = instr(addu_co); break;
 3699| 			case 0x62: ic->f = instr(addu_ci); break;
 3700| 			case 0x63: ic->f = instr(addu_cio); break;
 3701| 			case 0x64: ic->f = instr(subu);  break;
 3702| 			case 0x65: ic->f = instr(subu_co); break;
 3703| 			case 0x66: ic->f = instr(subu_ci); break;
 3704| 			case 0x67: ic->f = instr(subu_cio); break;
 3705| 			case 0x68: ic->f = instr(divu);  break;
```

### `src/cpus/cpu_dyntrans.c` around the row's cited line 2014 (HEAD 2d25df65, lines 1969-2038)

```c
 1969| 
 1970| 
 1971| 	/*
 1972| 	 *  Finally finally :-), execute the instruction.
 1973| 	 *
 1974| 	 *  Note: The instruction might have changed during read-ahead, if
 1975| 	 *  instruction combinations are used.
 1976| 	 */
 1977| 
 1978| 	ic->f(cpu, ic);
 1979| 
 1980| 	return;
 1981| 
 1982| 
 1983| bad:	/*
 1984| 	 *  Nothing was translated. (Unimplemented or illegal instruction.)
 1985| 	 */
 1986| 
 1987| 	/*  Clear the translation, in case it was "half-way" done:  */
 1988| 	ic->f = TO_BE_TRANSLATED;
 1989| 
 1990| 	if (cpu->translation_readahead)
 1991| 		return;
 1992| 
 1993| 
 1994| 	/*
 1995| 	 *  Abort the emulation.  In principle, it may have been more accurate
 1996| 	 *  to treat invalid/unimplemented instructions as something that
 1997| 	 *  should cause e.g. an exception (depending on how the particular
 1998| 	 *  CPU works), but chances are that this is an unimplemented
 1999| 	 *  instruction that should be implemented for real.
 2000| 	 */
 2001| 
 2002| 	about_to_enter_single_step = true;
 2003| 
 2004| 	if (cpu->is_32bit)
 2005| 		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
 2006| 		    "UNIMPLEMENTED instruction at 0x%" PRIx32, (uint32_t)cpu->pc);
 2007| 	else
 2008| 		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
 2009| 		    "UNIMPLEMENTED instruction at 0x%" PRIx64, (uint64_t)cpu->pc);
 2010| 
 2011| 	if (!(single_step || cpu->machine->instruction_trace))
 2012| 		DISASSEMBLE(cpu, ib, 1, 0);
 2013| 
 2014| 	cpu->running = 0;
 2015| 
 2016| 	/*  Note: Single-stepping can jump here.  */
 2017| stop_running_translated:
 2018| 
 2019| 	// This makes sure that we stop in the debugger, even if e.g.
 2020| 	// "step 100" was executing and 50 steps remained.
 2021| 	debugger_reset();
 2022| 
 2023| 	ic = cpu->cd.DYNTRANS_ARCH.next_ic = &nothing_call;
 2024| 	cpu->cd.DYNTRANS_ARCH.next_ic ++;
 2025| 
 2026| #ifdef DYNTRANS_DELAYSLOT
 2027| 	/*  Special hack: If the bad instruction was in a delay slot,
 2028| 	    make sure that execution does not continue anyway:  */
 2029| 	if (cpu->delay_slot)
 2030| 		cpu->delay_slot |= EXCEPTION_IN_DELAY_SLOT;
 2031| #endif
 2032| 
 2033| 	/*  Execute the "nothing" instruction:  */
 2034| 	ic->f(cpu, ic);
 2035| 
 2036| #endif	/*  DYNTRANS_TO_BE_TRANSLATED_TAIL  */
 2037| 
 2038| 
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

End with one line: `FIXDRAFT_M88KCARRYUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
