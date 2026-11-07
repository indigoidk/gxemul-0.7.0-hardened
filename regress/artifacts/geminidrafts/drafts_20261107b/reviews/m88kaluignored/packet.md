# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kaluignored` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kaluignored`, state `open`)

**title:** src/cpus/cpu_m88k_instr.c:3660,3815 -- the register-form switch keys on bits 15:8, so a divu, mul, div or cmp word with nonzero bits 9:8, which the MC88100 does not decode, finds no case and reaches goto bad, stopping the CPU -- CPU-STOP

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_m88k_instr.c:3660

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k_instr.c b/src/cpus/cpu_m88k_instr.c
index 8b9984e0..7075907a 100644
--- a/src/cpus/cpu_m88k_instr.c
+++ b/src/cpus/cpu_m88k_instr.c
@@ -3657,7 +3657,9 @@ X(to_be_translated)
 				if (d == M88K_ZERO_REG)
 					ic->f = instr(nop);
 			}
-		} else switch ((iword >> 8) & 0xff) {
+			/* #m88kaluignored: mask bits 9:8 for div/mul/cmp */
+		} else switch ((((iword >> 8) & 0xe8) == 0x68) ?
+		    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) {
 		case 0x40:	/*  and    */
 		case 0x44:	/*  and.c  */
 		case 0x50:	/*  xor    */
@@ -3687,7 +3689,9 @@ X(to_be_translated)
 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 
-			switch ((iword >> 8) & 0xff) {
+			/* #m88kaluignored: apply identical filter */
+			switch ((((iword >> 8) & 0xe8) == 0x68) ?
+			    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) {
 			case 0x40: ic->f = instr(and);   break;
 			case 0x44: ic->f = instr(and_c); break;
 			case 0x50: ic->f = instr(xor);   break;
@@ -3732,6 +3736,8 @@ X(to_be_translated)
 			 */
 			if (d == M88K_ZERO_REG) {
 				int opc = (iword >> 8) & 0xff;
+				/* #m88kaluignored: mask bits 9:8 to retain side effects */
+				opc = ((opc & 0xe8) == 0x68) ? (opc & 0xfc) : opc;
 				if (opc != 0x61 /* addu.co */ && opc != 0x63 /* addu.cio */ &&
 				    opc != 0x65 /* subu.co */ && opc != 0x67 /* subu.cio */ &&
 				    opc != 0x71 /*  add.co */ && opc != 0x73 /*  add.cio */ &&
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k_instr.c` -- post-edit lines 2953-3832 (`+` marks a line the diff added or the point of a deletion)

```c
 2953|  X(to_be_translated)
 2954|  {
 2955|  	uint32_t addr, low_pc, iword;
 2956|  	unsigned char *page;
 2957|  	unsigned char ib[4];
     | [... lines 2958-3549 not shown ...]
 3550|  			/*  Same operand shape as tb0/tb1, but arg[0] is the
 3551|  			    m5 condition MASK rather than a bit position.  */
 3552|  			ic->arg[0] = d;
 3553|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3554|  			ic->arg[2] = iword & 0x1ff;
 3555|  			ic->f = instr(tcnd);
 3556|  			break;
 3557|  
 3558|  		default:goto bad;
 3559|  		}
 3560|  		break;
 3561|  
 3562|  	case 0x3d:
 3563|  		if ((iword & 0xf000) <= 0x3fff ) {
 3564|  			/*  Load, Store, xmem, and lda:  */
 3565|  			int op = 0, opsize, user = 0, wt = 0;
 3566|  			int signedness = 1, scaled = 0;
 3567|  
 3568|  			switch (iword & 0xf000) {
 3569|  			case 0x2000: op = 1; /* st */  break;
 3570|  			case 0x3000: op = 2; /* lda */ break;
 3571|  			default:     if ((iword & 0xf800) >= 0x0800)
 3572|  					op = 0; /* ld */
 3573|  				     else
 3574|  					op = 3; /* xmem */
 3575|  			}
 3576|  
 3577|  			/*  for (most) ld, st, lda:  */
 3578|  			opsize = (iword >> 10) & 3;
 3579|  
 3580|  			/*  Turn opsize into x, where size = 1 << x:  */
 3581|  			opsize = 3 - opsize;
 3582|  
 3583|  			if (op == 3) {
 3584|  				/*  xmem:  */
 3585|  				switch ((iword >> 10) & 3) {
 3586|  				case 0: opsize = 0; break;
 3587|  				case 1: opsize = 2; break;
 3588|  				default:fatal("Weird xmem opsize/type?\n");
 3589|  					goto bad;
 3590|  				}
 3591|  			} else {
 3592|  				if ((iword & 0xf800) == 0x800) {
 3593|  					signedness = 0;
 3594|  					if ((iword & 0xf00) < 0xc00)
 3595|  						opsize = 1;
 3596|  					else
 3597|  						opsize = 0;
 3598|  				} else {
 3599|  					if (opsize >= 2 || op == 1)
 3600|  						signedness = 0;
 3601|  				}
 3602|  			}
 3603|  
 3604|  			if (iword & 0x100)
 3605|  				user = 1;
 3606|  			if (iword & 0x80)
 3607|  				wt = 1;
 3608|  			if (iword & 0x200)
 3609|  				scaled = 1;
 3610|  
 3611|  			if (wt) {
 3612|  				fatal("wt bit not yet implemented! TODO\n");
 3613|  				goto bad;
 3614|  			}
 3615|  
 3616|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3617|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3618|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3619|  
 3620|  			if (op == 0 || op == 1) {
 3621|  				/*  ld or st:  */
 3622|  				ic->f = m88k_loadstore[ opsize
 3623|  				    + (op==1? M88K_LOADSTORE_STORE : 0)
 3624|  				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3625|  				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3626|  				       M88K_LOADSTORE_ENDIANNESS : 0)
 3627|  				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 3628|  				    + (user? M88K_LOADSTORE_USR : 0)
 3629|  				    + M88K_LOADSTORE_REGISTEROFFSET ];
 3630|  
 3631|  				if (d == M88K_ZERO_REG && op == 0)
 3632|  					ic->arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
 3633|  
 3634|  				if (opsize == 3 && d == 31) {
 3635|  					fatal("m88k load/store of register "
 3636|  					    "pair r31/r0: TODO\n");
 3637|  					goto bad;
 3638|  				}
 3639|  			} else if (op == 2) {
 3640|  				/*  lda:  */
 3641|  				if (scaled) {
 3642|  					switch (opsize) {
 3643|  					case 0: ic->f = instr(addu); break;
 3644|  					case 1: ic->f = instr(lda_reg_2); break;
 3645|  					case 2: ic->f = instr(lda_reg_4); break;
 3646|  					case 3: ic->f = instr(lda_reg_8); break;
 3647|  					}
 3648|  				} else {
 3649|  					ic->f = instr(addu);
 3650|  				}
 3651|  				if (d == M88K_ZERO_REG)
 3652|  					ic->f = instr(nop);
 3653|  			} else {
 3654|  				/*  xmem:  */
 3655|  				ic->f = instr(xmem_slow);
 3656|  				ic->arg[0] = iword;
 3657|  				if (d == M88K_ZERO_REG)
 3658|  					ic->f = instr(nop);
 3659|  			}
 3660|+ 			/* #m88kaluignored: mask bits 9:8 for div/mul/cmp */
 3661|+ 		} else switch ((((iword >> 8) & 0xe8) == 0x68) ?
 3662|+ 		    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) {
 3663|  		case 0x40:	/*  and    */
 3664|  		case 0x44:	/*  and.c  */
 3665|  		case 0x50:	/*  xor    */
 3666|  		case 0x54:	/*  xor.c  */
 3667|  		case 0x58:	/*  or     */
 3668|  		case 0x5c:	/*  or.c   */
 3669|  		case 0x60:	/*  addu   */
 3670|  		case 0x61:	/*  addu.co  */
 3671|  		case 0x62:	/*  addu.ci  */
 3672|  		case 0x63:	/*  addu.cio */
 3673|  		case 0x64:	/*  subu   */
 3674|  		case 0x65:	/*  subu.co  */
 3675|  		case 0x66:	/*  subu.ci  */
 3676|  		case 0x67:	/*  subu.cio */
 3677|  		case 0x68:	/*  divu   */
 3678|  		case 0x6c:	/*  mul    */
 3679|  		case 0x70:	/*  add    */
 3680|  		case 0x78:	/*  div    */
 3681|  		case 0x7c:	/*  cmp    */
 3682|  		case 0x80:	/*  clr    */
 3683|  		case 0x88:	/*  set    */
 3684|  		case 0x90:	/*  ext    */
 3685|  		case 0x98:	/*  extu   */
 3686|  		case 0xa0:	/*  mak    */
 3687|  		case 0xa8:	/*  rot    */
 3688|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3689|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3690|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3691|  
 3692|+ 			/* #m88kaluignored: apply identical filter */
 3693|+ 			switch ((((iword >> 8) & 0xe8) == 0x68) ?
 3694|+ 			    ((iword >> 8) & 0xfc) : ((iword >> 8) & 0xff)) {
 3695|  			case 0x40: ic->f = instr(and);   break;
 3696|  			case 0x44: ic->f = instr(and_c); break;
 3697|  			case 0x50: ic->f = instr(xor);   break;
 3698|  			case 0x54: ic->f = instr(xor_c); break;
 3699|  			case 0x58: ic->f = instr(or);    break;
 3700|  			case 0x5c: ic->f = instr(or_c);  break;
 3701|  			case 0x60: ic->f = instr(addu);  break;
 3702|  			case 0x61: ic->f = instr(addu_co); break;
 3703|  			case 0x62: ic->f = instr(addu_ci); break;
 3704|  			case 0x63: ic->f = instr(addu_cio); break;
 3705|  			case 0x64: ic->f = instr(subu);  break;
 3706|  			case 0x65: ic->f = instr(subu_co); break;
 3707|  			case 0x66: ic->f = instr(subu_ci); break;
 3708|  			case 0x67: ic->f = instr(subu_cio); break;
 3709|  			case 0x68: ic->f = instr(divu);  break;
 3710|  			case 0x6c: ic->f = instr(mul);   break;
 3711|  			case 0x70: ic->f = instr(add);   break;
 3712|  			case 0x78: ic->f = instr(div);   break;
 3713|  			case 0x7c: ic->f = instr(cmp);   break;
 3714|  			case 0x80: ic->f = instr(clr);   break;
 3715|  			case 0x88: ic->f = instr(set);   break;
 3716|  			case 0x90: ic->f = instr(ext);   break;
 3717|  			case 0x98: ic->f = instr(extu);  break;
 3718|  			case 0xa0: ic->f = instr(mak);   break;
 3719|  			case 0xa8: ic->f = instr(rot);   break;
 3720|  			}
 3721|  
 3722|  			/*  Optimization for  or rX,r0,rY  etc:  */
 3723|  			if (s1 == M88K_ZERO_REG && ic->f == instr(or))
 3724|  				ic->f = instr(or_r0);
 3725|  			if (s2 == M88K_ZERO_REG && ic->f == instr(addu))
 3726|  				ic->f = instr(addu_s2r0);
 3727|  
 3728|  			/*
 3729|  			 *  Handle the case when the destination register is r0:
 3730|  			 *
 3731|  			 *  If there is NO SIDE-EFFECT! (i.e. no carry out),
 3732|  			 *  then replace the instruction with a nop. If there is
 3733|  			 *  a side-effect, we still have to run the instruction,
 3734|  			 *  so replace the destination register with a scratch
 3735|  			 *  register.
 3736|  			 */
 3737|  			if (d == M88K_ZERO_REG) {
 3738|  				int opc = (iword >> 8) & 0xff;
 3739|+ 				/* #m88kaluignored: mask bits 9:8 to retain side effects */
 3740|+ 				opc = ((opc & 0xe8) == 0x68) ? (opc & 0xfc) : opc;
 3741|  				if (opc != 0x61 /* addu.co */ && opc != 0x63 /* addu.cio */ &&
 3742|  				    opc != 0x65 /* subu.co */ && opc != 0x67 /* subu.cio */ &&
 3743|  				    opc != 0x71 /*  add.co */ && opc != 0x73 /*  add.cio */ &&
 3744|  				    opc != 0x75 /*  sub.co */ && opc != 0x77 /*  sub.cio */ &&
 3745|  				    opc != 0x68 /*  divu   */ && opc != 0x69 /* divu.d   */ &&
 3746|  				    opc != 0x6c /*  mul    */ && opc != 0x6d /* mulu.d   */ &&
 3747|  				    opc != 0x6e /*  muls   */ && opc != 0x78 /*  div     */)
 3748|  					ic->f = instr(nop);
 3749|  				else
 3750|  					ic->arg[0] = (size_t)
 3751|  					    &cpu->cd.m88k.zero_scratch;
 3752|  			}
 3753|  			break;
 3754|  		case 0xc0:	/*  jmp    */
 3755|  		case 0xc4:	/*  jmp.n  */
 3756|  		case 0xc8:	/*  jsr    */
 3757|  		case 0xcc:	/*  jsr.n  */
 3758|  			switch ((iword >> 8) & 0xff) {
 3759|  			case 0xc0: ic->f = instr(jmp);
 3760|  				   if (cpu->translation_readahead > 1)
 3761|  					cpu->translation_readahead = 1;
 3762|  				   break;
 3763|  			case 0xc4: ic->f = instr(jmp_n);
 3764|  				   if (cpu->translation_readahead > 2)
 3765|  					cpu->translation_readahead = 2;
 3766|  				   break;
 3767|  			case 0xc8: ic->f = instr(jsr); break;
 3768|  			case 0xcc: ic->f = instr(jsr_n); break;
 3769|  			}
 3770|  
 3771|  			ic->arg[1] = (addr & 0xffc) + 4;
 3772|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3773|  
 3774|  			if (((iword >> 8) & 0x04) == 0x04)
 3775|  				ic->arg[1] = (addr & 0xffc) + 8;
 3776|  
 3777|  			if (cpu->machine->show_trace_tree &&
 3778|  			    s2 == M88K_RETURN_REG) {
 3779|  				if (ic->f == instr(jmp))
 3780|  					ic->f = instr(jmp_trace);
 3781|  				if (ic->f == instr(jmp_n))
 3782|  					ic->f = instr(jmp_n_trace);
 3783|  			}
 3784|  			if (cpu->machine->show_trace_tree) {
 3785|  				if (ic->f == instr(jsr))
 3786|  					ic->f = instr(jsr_trace);
 3787|  				if (ic->f == instr(jsr_n))
 3788|  					ic->f = instr(jsr_n_trace);
 3789|  			}
 3790|  			break;
 3791|  		case 0xe8:	/*  ff1  */
 3792|  		case 0xec:      /*  ff0  */
 3793|  			switch ((iword >> 8) & 0xff) {
 3794|  			case 0xe8: ic->f = instr(ff1); break;
 3795|  			case 0xec: ic->f = instr(ff0); break;
 3796|  			}
 3797|  
 3798|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3799|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3800|  
     | [... lines 3801-3802 not shown ...]
 3803|  			break;
 3804|  		case 0xfc:
 3805|  			switch (iword & 0xff) {
 3806|  			case 0x00:
 3807|  				if (iword == 0xf400fc00)
 3808|  					ic->f = instr(rte);
 3809|  				else {
 3810|  					fatal("unimplemented rte variant: 0x%08" PRIx32"\n", iword);
 3811|  					goto bad;
 3812|  				}
 3813|  				break;
 3814|  			case (M88K_PROM_INSTR & 0xff):
 3815|  				ic->f = instr(prom_call);
 3816|  				break;
 3817|  			default:fatal("Unimplemented 3d/fc instruction\n");
 3818|  				goto bad;
 3819|  			}
 3820|  			break;
 3821|  		default:goto bad;
 3822|  		}
 3823|  		break;
 3824|  
 3825|  	default:goto bad;
 3826|  	}
 3827|  
 3828|  
 3829|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3830|  #include "cpu_dyntrans.c" 
 3831|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3832|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KALUIGNORED: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KALUIGNORED: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
