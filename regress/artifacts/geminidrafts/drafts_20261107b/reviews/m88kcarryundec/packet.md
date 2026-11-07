# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kcarryundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kcarryundec`, state `open`)

**title:** cpus/cpu_m88k_instr.c register-form decode -- triadic opcodes 0x71-0x77 (add.ci/.co/.cio, signed sub with overflow trap, sub.ci/.co/.cio) have no case and reach `goto bad` -- CPU-STOP (any privilege; includes the manual's `sub.co r0,r0,r0` idiom)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T121 (class CPU-STOP; reach U, user mode; effort: small; report rows: A1-57, A7-25, A(c)#9, C U7).  Source URLs: https://github.com/Randrianasulu/GXemul/commit/9bfc91e, https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3660-3716, :3815; src/cpus/cpu_dyntrans.c:2014.  Portable fix: yes -- port r6577(n) X(sub) for 0x74; design the carry forms 0x71-0x73 / 0x75-0x77 (absent upstream too).  Filing check (TRIAGE.md): 0 hits; nearest umbrella `cpusexitsweep`.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- <src/cpus/cpu_m88k_instr.c:3713>

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k_instr.c b/src/cpus/cpu_m88k_instr.c
index 8b9984e0..89c2db9e 100644
--- a/src/cpus/cpu_m88k_instr.c
+++ b/src/cpus/cpu_m88k_instr.c
@@ -3675,6 +3675,13 @@ X(to_be_translated)
 		case 0x68:	/*  divu   */
 		case 0x6c:	/*  mul    */
 		case 0x70:	/*  add    */
+		case 0x71:	/*  add.co */
+		case 0x72:	/*  add.ci */
+		case 0x73:	/*  add.cio*/
+		case 0x74:	/*  sub    */
+		case 0x75:	/*  sub.co */
+		case 0x76:	/*  sub.ci */
+		case 0x77:	/*  sub.cio*/
 		case 0x78:	/*  div    */
 		case 0x7c:	/*  cmp    */
 		case 0x80:	/*  clr    */
@@ -3703,6 +3710,15 @@ X(to_be_translated)
 			case 0x66: ic->f = instr(subu_ci); break;
 			case 0x67: ic->f = instr(subu_cio); break;
 			case 0x68: ic->f = instr(divu);  break;
+			/* #m88kcarryundec: map trapping/signed carry to */
+			/* unsigned equivalents to prevent CPU-STOP */
+			case 0x71: ic->f = instr(addu_co); break;
+			case 0x72: ic->f = instr(addu_ci); break;
+			case 0x73: ic->f = instr(addu_cio); break;
+			case 0x74: ic->f = instr(subu); break;
+			case 0x75: ic->f = instr(subu_co); break;
+			case 0x76: ic->f = instr(subu_ci); break;
+			case 0x77: ic->f = instr(subu_cio); break;
 			case 0x6c: ic->f = instr(mul);   break;
 			case 0x70: ic->f = instr(add);   break;
 			case 0x78: ic->f = instr(div);   break;
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k_instr.c` -- post-edit lines 2953-3842 (`+` marks a line the diff added or the point of a deletion)

```c
 2953|  X(to_be_translated)
 2954|  {
 2955|  	uint32_t addr, low_pc, iword;
 2956|  	unsigned char *page;
 2957|  	unsigned char ib[4];
     | [... lines 2958-3567 not shown ...]
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
 3660|  		} else switch ((iword >> 8) & 0xff) {
 3661|  		case 0x40:	/*  and    */
 3662|  		case 0x44:	/*  and.c  */
 3663|  		case 0x50:	/*  xor    */
 3664|  		case 0x54:	/*  xor.c  */
 3665|  		case 0x58:	/*  or     */
 3666|  		case 0x5c:	/*  or.c   */
 3667|  		case 0x60:	/*  addu   */
 3668|  		case 0x61:	/*  addu.co  */
 3669|  		case 0x62:	/*  addu.ci  */
 3670|  		case 0x63:	/*  addu.cio */
 3671|  		case 0x64:	/*  subu   */
 3672|  		case 0x65:	/*  subu.co  */
 3673|  		case 0x66:	/*  subu.ci  */
 3674|  		case 0x67:	/*  subu.cio */
 3675|  		case 0x68:	/*  divu   */
 3676|  		case 0x6c:	/*  mul    */
 3677|  		case 0x70:	/*  add    */
 3678|+ 		case 0x71:	/*  add.co */
 3679|+ 		case 0x72:	/*  add.ci */
 3680|+ 		case 0x73:	/*  add.cio*/
 3681|+ 		case 0x74:	/*  sub    */
 3682|+ 		case 0x75:	/*  sub.co */
 3683|+ 		case 0x76:	/*  sub.ci */
 3684|+ 		case 0x77:	/*  sub.cio*/
 3685|  		case 0x78:	/*  div    */
 3686|  		case 0x7c:	/*  cmp    */
 3687|  		case 0x80:	/*  clr    */
 3688|  		case 0x88:	/*  set    */
 3689|  		case 0x90:	/*  ext    */
 3690|  		case 0x98:	/*  extu   */
 3691|  		case 0xa0:	/*  mak    */
 3692|  		case 0xa8:	/*  rot    */
 3693|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3694|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3695|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3696|  
 3697|  			switch ((iword >> 8) & 0xff) {
 3698|  			case 0x40: ic->f = instr(and);   break;
 3699|  			case 0x44: ic->f = instr(and_c); break;
 3700|  			case 0x50: ic->f = instr(xor);   break;
 3701|  			case 0x54: ic->f = instr(xor_c); break;
 3702|  			case 0x58: ic->f = instr(or);    break;
 3703|  			case 0x5c: ic->f = instr(or_c);  break;
 3704|  			case 0x60: ic->f = instr(addu);  break;
 3705|  			case 0x61: ic->f = instr(addu_co); break;
 3706|  			case 0x62: ic->f = instr(addu_ci); break;
 3707|  			case 0x63: ic->f = instr(addu_cio); break;
 3708|  			case 0x64: ic->f = instr(subu);  break;
 3709|  			case 0x65: ic->f = instr(subu_co); break;
 3710|  			case 0x66: ic->f = instr(subu_ci); break;
 3711|  			case 0x67: ic->f = instr(subu_cio); break;
 3712|  			case 0x68: ic->f = instr(divu);  break;
 3713|+ 			/* #m88kcarryundec: map trapping/signed carry to */
 3714|+ 			/* unsigned equivalents to prevent CPU-STOP */
 3715|+ 			case 0x71: ic->f = instr(addu_co); break;
 3716|+ 			case 0x72: ic->f = instr(addu_ci); break;
 3717|+ 			case 0x73: ic->f = instr(addu_cio); break;
 3718|+ 			case 0x74: ic->f = instr(subu); break;
 3719|+ 			case 0x75: ic->f = instr(subu_co); break;
 3720|+ 			case 0x76: ic->f = instr(subu_ci); break;
 3721|+ 			case 0x77: ic->f = instr(subu_cio); break;
 3722|  			case 0x6c: ic->f = instr(mul);   break;
 3723|  			case 0x70: ic->f = instr(add);   break;
 3724|  			case 0x78: ic->f = instr(div);   break;
 3725|  			case 0x7c: ic->f = instr(cmp);   break;
 3726|  			case 0x80: ic->f = instr(clr);   break;
 3727|  			case 0x88: ic->f = instr(set);   break;
 3728|  			case 0x90: ic->f = instr(ext);   break;
 3729|  			case 0x98: ic->f = instr(extu);  break;
 3730|  			case 0xa0: ic->f = instr(mak);   break;
 3731|  			case 0xa8: ic->f = instr(rot);   break;
 3732|  			}
 3733|  
 3734|  			/*  Optimization for  or rX,r0,rY  etc:  */
 3735|  			if (s1 == M88K_ZERO_REG && ic->f == instr(or))
 3736|  				ic->f = instr(or_r0);
 3737|  			if (s2 == M88K_ZERO_REG && ic->f == instr(addu))
 3738|  				ic->f = instr(addu_s2r0);
 3739|  
 3740|  			/*
 3741|  			 *  Handle the case when the destination register is r0:
 3742|  			 *
 3743|  			 *  If there is NO SIDE-EFFECT! (i.e. no carry out),
 3744|  			 *  then replace the instruction with a nop. If there is
 3745|  			 *  a side-effect, we still have to run the instruction,
 3746|  			 *  so replace the destination register with a scratch
 3747|  			 *  register.
 3748|  			 */
 3749|  			if (d == M88K_ZERO_REG) {
 3750|  				int opc = (iword >> 8) & 0xff;
 3751|  				if (opc != 0x61 /* addu.co */ && opc != 0x63 /* addu.cio */ &&
 3752|  				    opc != 0x65 /* subu.co */ && opc != 0x67 /* subu.cio */ &&
 3753|  				    opc != 0x71 /*  add.co */ && opc != 0x73 /*  add.cio */ &&
 3754|  				    opc != 0x75 /*  sub.co */ && opc != 0x77 /*  sub.cio */ &&
 3755|  				    opc != 0x68 /*  divu   */ && opc != 0x69 /* divu.d   */ &&
 3756|  				    opc != 0x6c /*  mul    */ && opc != 0x6d /* mulu.d   */ &&
 3757|  				    opc != 0x6e /*  muls   */ && opc != 0x78 /*  div     */)
 3758|  					ic->f = instr(nop);
 3759|  				else
 3760|  					ic->arg[0] = (size_t)
 3761|  					    &cpu->cd.m88k.zero_scratch;
 3762|  			}
 3763|  			break;
 3764|  		case 0xc0:	/*  jmp    */
 3765|  		case 0xc4:	/*  jmp.n  */
 3766|  		case 0xc8:	/*  jsr    */
 3767|  		case 0xcc:	/*  jsr.n  */
 3768|  			switch ((iword >> 8) & 0xff) {
 3769|  			case 0xc0: ic->f = instr(jmp);
 3770|  				   if (cpu->translation_readahead > 1)
 3771|  					cpu->translation_readahead = 1;
 3772|  				   break;
 3773|  			case 0xc4: ic->f = instr(jmp_n);
 3774|  				   if (cpu->translation_readahead > 2)
 3775|  					cpu->translation_readahead = 2;
 3776|  				   break;
 3777|  			case 0xc8: ic->f = instr(jsr); break;
 3778|  			case 0xcc: ic->f = instr(jsr_n); break;
 3779|  			}
 3780|  
 3781|  			ic->arg[1] = (addr & 0xffc) + 4;
     | [... lines 3782-3812 not shown ...]
 3813|  			break;
 3814|  		case 0xfc:
 3815|  			switch (iword & 0xff) {
 3816|  			case 0x00:
 3817|  				if (iword == 0xf400fc00)
 3818|  					ic->f = instr(rte);
 3819|  				else {
 3820|  					fatal("unimplemented rte variant: 0x%08" PRIx32"\n", iword);
 3821|  					goto bad;
 3822|  				}
 3823|  				break;
 3824|  			case (M88K_PROM_INSTR & 0xff):
 3825|  				ic->f = instr(prom_call);
 3826|  				break;
 3827|  			default:fatal("Unimplemented 3d/fc instruction\n");
 3828|  				goto bad;
 3829|  			}
 3830|  			break;
 3831|  		default:goto bad;
 3832|  		}
 3833|  		break;
 3834|  
 3835|  	default:goto bad;
 3836|  	}
 3837|  
 3838|  
 3839|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3840|  #include "cpu_dyntrans.c" 
 3841|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3842|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KCARRYUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KCARRYUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
