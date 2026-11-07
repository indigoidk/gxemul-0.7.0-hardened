# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88kzeroword` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88kzeroword`, state `open`)

**title:** cpus/cpu_m88k_instr.c -- instruction word 0x00000000 (`xmem.bu r0,r0,0`) is sent to `goto bad` -- CPU-STOP (SVR4's IPL runs through zero padding)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T126 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A7-28).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3047-3048.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 01.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `3047| 		if (iword == 0)` and `3048| 			goto bad;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_m88k_instr.c b/src/cpus/cpu_m88k_instr.c
index 8b9984e0..e5f2e78e 100644
--- a/src/cpus/cpu_m88k_instr.c
+++ b/src/cpus/cpu_m88k_instr.c
@@ -3044,8 +3044,6 @@ X(to_be_translated)
 		ic->arg[0] = iword;
 		if (d == M88K_ZERO_REG)
 			ic->f = instr(nop);
-		if (iword == 0)
-			goto bad;
 		break;
 
 	case 0x02:	/*  ld.hu  */
```

## Every edited function, after the fix

### `src/cpus/cpu_m88k_instr.c` -- post-edit lines 2953-3824 (`+` marks a line the diff added or the point of a deletion)

```c
 2953|  X(to_be_translated)
 2954|  {
 2955|  	uint32_t addr, low_pc, iword;
 2956|  	unsigned char *page;
 2957|  	unsigned char ib[4];
 2958|  	uint32_t op26, op10, op11, d, s1, s2, cr6, imm16;
 2959|  	int32_t d16, d26; //, simm16;
 2960|  	int offset, shift;
 2961|  	int in_crosspage_delayslot = 0;
 2962|  	void (*samepage_function)(struct cpu *, struct m88k_instr_call *)=NULL;
 2963|  
 2964|  	/*  Figure out the (virtual) address of the instruction:  */
 2965|  	low_pc = ((size_t)ic - (size_t)cpu->cd.m88k.cur_ic_page)
 2966|  	    / sizeof(struct m88k_instr_call);
 2967|  
 2968|  	/*  Special case for branch with delayslot on the next page:  */
 2969|  	if (cpu->delay_slot == TO_BE_DELAYED && low_pc == 0) {
 2970|  		/*  fatal("[ delay-slot translation across page "
 2971|  		    "boundary ]\n");  */
 2972|  		in_crosspage_delayslot = 1;
 2973|  	}
 2974|  
 2975|  	addr = cpu->pc & ~((M88K_IC_ENTRIES_PER_PAGE-1)
 2976|  	    << M88K_INSTR_ALIGNMENT_SHIFT);
 2977|  	addr += (low_pc << M88K_INSTR_ALIGNMENT_SHIFT);
 2978|  	cpu->pc = (uint32_t)addr;
 2979|  	addr &= ~((1 << M88K_INSTR_ALIGNMENT_SHIFT) - 1);
 2980|  
 2981|  	/*  Read the instruction word from memory:  */
 2982|  	page = cpu->cd.m88k.host_load[(uint32_t)addr >> 12];
 2983|  
 2984|  	if (page != NULL) {
 2985|  		/*  fatal("TRANSLATION HIT!\n");  */
 2986|  		memcpy(ib, page + (addr & 0xffc), sizeof(ib));
 2987|  	} else {
 2988|  		/*  fatal("TRANSLATION MISS!\n");  */
 2989|  		if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
 2990|  		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
 2991|  			fatal("to_be_translated(): read failed: TODO\n");
 2992|  			goto bad;
 2993|  		}
 2994|  	}
 2995|  
 2996|  	{
 2997|  		uint32_t *p = (uint32_t *) ib;
 2998|  		iword = *p;
 2999|  	}
 3000|  
 3001|  	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
 3002|  		iword = LE32_TO_HOST(iword);
 3003|  	else
 3004|  		iword = BE32_TO_HOST(iword);
 3005|  
 3006|  
 3007|  #define DYNTRANS_TO_BE_TRANSLATED_HEAD
 3008|  #include "cpu_dyntrans.c"
 3009|  #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
 3010|  
 3011|  
 3012|  	/*
 3013|  	 *  Translate the instruction:
 3014|   	 *
 3015|  	 *  NOTE: _NEVER_ allow writes to the zero register; all instructions
 3016|  	 *  that use the zero register as their destination should be treated
 3017|  	 *  as NOPs, except those that access memory (they should use the
 3018|  	 *  scratch register instead).
 3019|  	 */
 3020|  	if (cpu->cd.m88k.r[M88K_ZERO_REG] != 0) {
 3021|  		debugmsg_cpu(cpu, SUBSYS_CPU, "to_be_translated", VERBOSITY_ERROR,
 3022|  		    "INTERNAL ERROR! M88K_ZERO_REG != 0");
 3023|  		cpu->running = false;
 3024|  		goto bad;
 3025|  	}
 3026|  
 3027|  	op26   = (iword >> 26) & 0x3f;
 3028|  	op11   = (iword >> 11) & 0x1f;
 3029|  	op10   = (iword >> 10) & 0x3f;
 3030|  	d      = (iword >> 21) & 0x1f;
 3031|  	s1     = (iword >> 16) & 0x1f;
 3032|  	s2     =  iword        & 0x1f;
 3033|  	imm16  =  iword        & 0xffff;
 3034|  	// simm16 = (int16_t) (iword & 0xffff);
 3035|  	cr6    = (iword >>  5) & 0x3f;
 3036|  	d16    = ((int16_t) (iword & 0xffff)) * 4;
 3037|  	d26    = ((int32_t)((iword & 0x03ffffff) << 6)) >> 4;
 3038|  
 3039|  	switch (op26) {
 3040|  
 3041|  	case 0x00:
 3042|  	case 0x01:
 3043|  		ic->f = instr(xmem_slow);
 3044|  		ic->arg[0] = iword;
 3045|  		if (d == M88K_ZERO_REG)
 3046|  			ic->f = instr(nop);
 3047|+ 		break;
 3048|  
 3049|  	case 0x02:	/*  ld.hu  */
 3050|  	case 0x03:	/*  ld.bu  */
 3051|  	case 0x04:	/*  ld.d   */
 3052|  	case 0x05:	/*  ld     */
 3053|  	case 0x06:	/*  ld.h   */
 3054|  	case 0x07:	/*  ld.b   */
 3055|  	case 0x08:	/*  st.d   */
 3056|  	case 0x09:	/*  st     */
 3057|  	case 0x0a:	/*  st.h   */
 3058|  	case 0x0b:	/*  st.b   */
 3059|  		{
 3060|  			int store = 0, signedness = 0, opsize = 0;
 3061|  
 3062|  			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3063|  			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3064|  			ic->arg[2] = imm16;
 3065|  
 3066|  			switch (op26) {
 3067|  			case 0x02: opsize = 1; break;
 3068|  			case 0x03: opsize = 0; break;
 3069|  			case 0x04: opsize = 3; break;
 3070|  			case 0x05: opsize = 2; break;
 3071|  			case 0x06: opsize = 1; signedness = 1; break;
 3072|  			case 0x07: opsize = 0; signedness = 1; break;
 3073|  			case 0x08: store = 1; opsize = 3; break;
 3074|  			case 0x09: store = 1; opsize = 2; break;
 3075|  			case 0x0a: store = 1; opsize = 1; break;
 3076|  			case 0x0b: store = 1; opsize = 0; break;
 3077|  			}
 3078|  
 3079|  			if (opsize == 3 && d == 31) {
 3080|  				fatal("m88k load/store of register pair r31/r0"
 3081|  				    " is not yet implemented\n");
 3082|  				goto bad;
 3083|  			}
 3084|  
 3085|  			ic->f = m88k_loadstore[ opsize
 3086|  			    + (store? M88K_LOADSTORE_STORE : 0)
 3087|  			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3088|  			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3089|  			       M88K_LOADSTORE_ENDIANNESS : 0) ];
 3090|  
 3091|  			if (!store && d == 0)
 3092|  				ic->arg[0] = (size_t) &cpu->cd.m88k.zero_scratch;
 3093|  		}
 3094|  		break;
 3095|  
 3096|  	case 0x10:	/*  and    imm  */
 3097|  	case 0x11:	/*  and.u  imm  */
 3098|  	case 0x12:	/*  mask   imm  */
 3099|  	case 0x13:	/*  mask.u imm  */
 3100|  	case 0x14:	/*  xor    imm  */
 3101|  	case 0x15:	/*  xor.u  imm  */
 3102|  	case 0x16:	/*  or     imm  */
 3103|  	case 0x17:	/*  or.u   imm  */
 3104|  	case 0x18:	/*  addu   imm  */
 3105|  	case 0x19:	/*  subu   imm  */
 3106|  	case 0x1a:	/*  divu   imm  */
 3107|  	case 0x1b:	/*  mulu   imm  */
     | [... lines 3108-3794 not shown ...]
 3795|  			break;
 3796|  		case 0xfc:
 3797|  			switch (iword & 0xff) {
 3798|  			case 0x00:
 3799|  				if (iword == 0xf400fc00)
 3800|  					ic->f = instr(rte);
 3801|  				else {
 3802|  					fatal("unimplemented rte variant: 0x%08" PRIx32"\n", iword);
 3803|  					goto bad;
 3804|  				}
 3805|  				break;
 3806|  			case (M88K_PROM_INSTR & 0xff):
 3807|  				ic->f = instr(prom_call);
 3808|  				break;
 3809|  			default:fatal("Unimplemented 3d/fc instruction\n");
 3810|  				goto bad;
 3811|  			}
 3812|  			break;
 3813|  		default:goto bad;
 3814|  		}
 3815|  		break;
 3816|  
 3817|  	default:goto bad;
 3818|  	}
 3819|  
 3820|  
 3821|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3822|  #include "cpu_dyntrans.c" 
 3823|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 3824|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KZEROWORD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KZEROWORD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
