# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `m88kcarryundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `m88kcarryundec`, state `open`)

**title:** cpus/cpu_m88k_instr.c register-form decode -- triadic opcodes 0x71-0x77 (add.ci/.co/.cio, signed sub with overflow trap, sub.ci/.co/.cio) have no case and reach `goto bad` -- CPU-STOP (any privilege; includes the manual's `sub.co r0,r0,r0` idiom)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T121 (class CPU-STOP; reach U, user mode; effort: small; report rows: A1-57, A7-25, A(c)#9, C U7).  Source URLs: https://github.com/Randrianasulu/GXemul/commit/9bfc91e, https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3660-3716, :3815; src/cpus/cpu_dyntrans.c:2014.  Portable fix: yes -- port r6577(n) X(sub) for 0x74; design the carry forms 0x71-0x73 / 0x75-0x77 (absent upstream too).  Filing check (TRIAGE.md): 0 hits; nearest umbrella `cpusexitsweep`.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_m88k_instr.c` -- AT HEAD, lines 2953-3826 (`*` marks a line your previous draft changed)

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
 3678|* 		case 0x78:	/*  div    */
 3679|  		case 0x7c:	/*  cmp    */
 3680|  		case 0x80:	/*  clr    */
 3681|  		case 0x88:	/*  set    */
 3682|  		case 0x90:	/*  ext    */
 3683|  		case 0x98:	/*  extu   */
 3684|  		case 0xa0:	/*  mak    */
 3685|  		case 0xa8:	/*  rot    */
 3686|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3687|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3688|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3689|  
 3690|  			switch ((iword >> 8) & 0xff) {
 3691|  			case 0x40: ic->f = instr(and);   break;
 3692|  			case 0x44: ic->f = instr(and_c); break;
 3693|  			case 0x50: ic->f = instr(xor);   break;
 3694|  			case 0x54: ic->f = instr(xor_c); break;
 3695|  			case 0x58: ic->f = instr(or);    break;
 3696|  			case 0x5c: ic->f = instr(or_c);  break;
 3697|  			case 0x60: ic->f = instr(addu);  break;
 3698|  			case 0x61: ic->f = instr(addu_co); break;
 3699|  			case 0x62: ic->f = instr(addu_ci); break;
 3700|  			case 0x63: ic->f = instr(addu_cio); break;
 3701|  			case 0x64: ic->f = instr(subu);  break;
 3702|  			case 0x65: ic->f = instr(subu_co); break;
 3703|  			case 0x66: ic->f = instr(subu_ci); break;
 3704|  			case 0x67: ic->f = instr(subu_cio); break;
 3705|  			case 0x68: ic->f = instr(divu);  break;
 3706|* 			case 0x6c: ic->f = instr(mul);   break;
 3707|  			case 0x70: ic->f = instr(add);   break;
 3708|  			case 0x78: ic->f = instr(div);   break;
 3709|  			case 0x7c: ic->f = instr(cmp);   break;
 3710|  			case 0x80: ic->f = instr(clr);   break;
 3711|  			case 0x88: ic->f = instr(set);   break;
 3712|  			case 0x90: ic->f = instr(ext);   break;
 3713|  			case 0x98: ic->f = instr(extu);  break;
 3714|  			case 0xa0: ic->f = instr(mak);   break;
 3715|  			case 0xa8: ic->f = instr(rot);   break;
 3716|  			}
 3717|  
 3718|  			/*  Optimization for  or rX,r0,rY  etc:  */
 3719|  			if (s1 == M88K_ZERO_REG && ic->f == instr(or))
 3720|  				ic->f = instr(or_r0);
 3721|  			if (s2 == M88K_ZERO_REG && ic->f == instr(addu))
 3722|  				ic->f = instr(addu_s2r0);
 3723|  
 3724|  			/*
 3725|  			 *  Handle the case when the destination register is r0:
 3726|  			 *
 3727|  			 *  If there is NO SIDE-EFFECT! (i.e. no carry out),
 3728|  			 *  then replace the instruction with a nop. If there is
 3729|  			 *  a side-effect, we still have to run the instruction,
 3730|  			 *  so replace the destination register with a scratch
 3731|  			 *  register.
 3732|  			 */
 3733|  			if (d == M88K_ZERO_REG) {
 3734|  				int opc = (iword >> 8) & 0xff;
 3735|  				if (opc != 0x61 /* addu.co */ && opc != 0x63 /* addu.cio */ &&
 3736|  				    opc != 0x65 /* subu.co */ && opc != 0x67 /* subu.cio */ &&
 3737|  				    opc != 0x71 /*  add.co */ && opc != 0x73 /*  add.cio */ &&
 3738|  				    opc != 0x75 /*  sub.co */ && opc != 0x77 /*  sub.cio */ &&
 3739|  				    opc != 0x68 /*  divu   */ && opc != 0x69 /* divu.d   */ &&
 3740|  				    opc != 0x6c /*  mul    */ && opc != 0x6d /* mulu.d   */ &&
 3741|  				    opc != 0x6e /*  muls   */ && opc != 0x78 /*  div     */)
 3742|  					ic->f = instr(nop);
 3743|  				else
 3744|  					ic->arg[0] = (size_t)
 3745|  					    &cpu->cd.m88k.zero_scratch;
 3746|  			}
 3747|  			break;
 3748|  		case 0xc0:	/*  jmp    */
 3749|  		case 0xc4:	/*  jmp.n  */
 3750|  		case 0xc8:	/*  jsr    */
 3751|  		case 0xcc:	/*  jsr.n  */
 3752|  			switch ((iword >> 8) & 0xff) {
 3753|  			case 0xc0: ic->f = instr(jmp);
 3754|  				   if (cpu->translation_readahead > 1)
 3755|  					cpu->translation_readahead = 1;
 3756|  				   break;
 3757|  			case 0xc4: ic->f = instr(jmp_n);
 3758|  				   if (cpu->translation_readahead > 2)
 3759|  					cpu->translation_readahead = 2;
 3760|  				   break;
 3761|  			case 0xc8: ic->f = instr(jsr); break;
 3762|  			case 0xcc: ic->f = instr(jsr_n); break;
 3763|  			}
 3764|  
 3765|  			ic->arg[1] = (addr & 0xffc) + 4;
 3766|  			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
     | [... lines 3767-3796 not shown ...]
 3797|  			break;
 3798|  		case 0xfc:
 3799|  			switch (iword & 0xff) {
 3800|  			case 0x00:
 3801|  				if (iword == 0xf400fc00)
 3802|  					ic->f = instr(rte);
 3803|  				else {
 3804|  					fatal("unimplemented rte variant: 0x%08" PRIx32"\n", iword);
 3805|  					goto bad;
 3806|  				}
 3807|  				break;
 3808|  			case (M88K_PROM_INSTR & 0xff):
 3809|  				ic->f = instr(prom_call);
 3810|  				break;
 3811|  			default:fatal("Unimplemented 3d/fc instruction\n");
 3812|  				goto bad;
 3813|  			}
 3814|  			break;
 3815|  		default:goto bad;
 3816|  		}
 3817|  		break;
 3818|  
 3819|  	default:goto bad;
 3820|  	}
 3821|  
 3822|  
 3823|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3824|  #include "cpu_dyntrans.c" 
 3825|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3826|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_m88k_instr.c",
    "old": "\t\tcase 0x6c:\t/*  mul    */\n\t\tcase 0x70:\t/*  add    */\n\t\tcase 0x78:\t/*  div    */",
    "new": "\t\tcase 0x6c:\t/*  mul    */\n\t\tcase 0x70:\t/*  add    */\n\t\tcase 0x71:\t/*  add.co */\n\t\tcase 0x72:\t/*  add.ci */\n\t\tcase 0x73:\t/*  add.cio*/\n\t\tcase 0x74:\t/*  sub    */\n\t\tcase 0x75:\t/*  sub.co */\n\t\tcase 0x76:\t/*  sub.ci */\n\t\tcase 0x77:\t/*  sub.cio*/\n\t\tcase 0x78:\t/*  div    */",
    "why": "Add 0x71-0x77 to first switch to load register arguments and prevent fallthrough"
  },
  {
    "file": "src/cpus/cpu_m88k_instr.c",
    "old": "\t\t\tcase 0x67: ic->f = instr(subu_cio); break;\n\t\t\tcase 0x68: ic->f = instr(divu);  break;",
    "new": "\t\t\tcase 0x67: ic->f = instr(subu_cio); break;\n\t\t\tcase 0x68: ic->f = instr(divu);  break;\n\t\t\t/* #m88kcarryundec: map trapping/signed carry to unsigned equivalents to prevent CPU-STOP */\n\t\t\tcase 0x71: ic->f = instr(addu_co); break;\n\t\t\tcase 0x72: ic->f = instr(addu_ci); break;\n\t\t\tcase 0x73: ic->f = instr(addu_cio); break;\n\t\t\tcase 0x74: ic->f = instr(subu); break;\n\t\t\tcase 0x75: ic->f = instr(subu_co); break;\n\t\t\tcase 0x76: ic->f = instr(subu_ci); break;\n\t\t\tcase 0x77: ic->f = instr(subu_cio); break;",
    "why": "Add 0x71-0x77 to second switch, mapping to existing unsigned implementations to remove the defect"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_M88KCARRYUNDEC: DEFECT, 3 FINDINGS
1. **Missed sites:** The diff modifies `src/cpus/cpu_m88k_instr.c` between lines 3678 and 3720. It fails to touch `src/cpus/cpu_m88k_instr.c:3815` and `src/cpus/cpu_dyntrans.c:2014`, which are explicitly named in the issue ledger as needing attention.
2. **Control Flow:** The added cases only use standard `break;` statements to exit the `switch`, mirroring existing cases. No early returns or skips of the common tail are introduced.
3. **Return Value:** No paths return a different value; the added `case` blocks merely assign to `ic->f` and break.
4. **State/Behavior Changes:** The fix maps signed/trapping arithmetic forms (e.g., `add.co` 0x71) directly to their unsigned equivalents (e.g., `addu_co`). This prevents the CPU-STOP but means the emulator will silently fail to trap on signed overflow for these opcodes.
5. **House Idioms:** The added comment at line 3713 severely exceeds the 79-column limit (it is >110 columns wide when accounting for indentation).
src/cpus/cpu_m88k_instr.c:3713: STYLE: The comment line exceeds 79 columns and should be wrapped.
src/cpus/cpu_m88k_instr.c:3815: DEFECT: Site named in issue is unpatched.
src/cpus/cpu_dyntrans.c:2014: DEFECT: Site named in issue is unpatched.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_M88KCARRYUNDEC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_M88KCARRYUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
