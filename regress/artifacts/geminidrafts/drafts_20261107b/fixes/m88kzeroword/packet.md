# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kzeroword` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kzeroword`, state `open`, severity `MED`)

**title:** cpus/cpu_m88k_instr.c -- instruction word 0x00000000 (`xmem.bu r0,r0,0`) is sent to `goto bad` -- CPU-STOP (SVR4's IPL runs through zero padding)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T126 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A7-28).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3047-3048.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 01.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 01.

## The code at the cited lines

### `src/cpus/cpu_m88k_instr.c` around the row's cited line 3047 (HEAD 2d25df65, lines 3002-3092)

```c
 3002| 		iword = LE32_TO_HOST(iword);
 3003| 	else
 3004| 		iword = BE32_TO_HOST(iword);
 3005| 
 3006| 
 3007| #define DYNTRANS_TO_BE_TRANSLATED_HEAD
 3008| #include "cpu_dyntrans.c"
 3009| #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
 3010| 
 3011| 
 3012| 	/*
 3013| 	 *  Translate the instruction:
 3014|  	 *
 3015| 	 *  NOTE: _NEVER_ allow writes to the zero register; all instructions
 3016| 	 *  that use the zero register as their destination should be treated
 3017| 	 *  as NOPs, except those that access memory (they should use the
 3018| 	 *  scratch register instead).
 3019| 	 */
 3020| 	if (cpu->cd.m88k.r[M88K_ZERO_REG] != 0) {
 3021| 		debugmsg_cpu(cpu, SUBSYS_CPU, "to_be_translated", VERBOSITY_ERROR,
 3022| 		    "INTERNAL ERROR! M88K_ZERO_REG != 0");
 3023| 		cpu->running = false;
 3024| 		goto bad;
 3025| 	}
 3026| 
 3027| 	op26   = (iword >> 26) & 0x3f;
 3028| 	op11   = (iword >> 11) & 0x1f;
 3029| 	op10   = (iword >> 10) & 0x3f;
 3030| 	d      = (iword >> 21) & 0x1f;
 3031| 	s1     = (iword >> 16) & 0x1f;
 3032| 	s2     =  iword        & 0x1f;
 3033| 	imm16  =  iword        & 0xffff;
 3034| 	// simm16 = (int16_t) (iword & 0xffff);
 3035| 	cr6    = (iword >>  5) & 0x3f;
 3036| 	d16    = ((int16_t) (iword & 0xffff)) * 4;
 3037| 	d26    = ((int32_t)((iword & 0x03ffffff) << 6)) >> 4;
 3038| 
 3039| 	switch (op26) {
 3040| 
 3041| 	case 0x00:
 3042| 	case 0x01:
 3043| 		ic->f = instr(xmem_slow);
 3044| 		ic->arg[0] = iword;
 3045| 		if (d == M88K_ZERO_REG)
 3046| 			ic->f = instr(nop);
 3047| 		if (iword == 0)
 3048| 			goto bad;
 3049| 		break;
 3050| 
 3051| 	case 0x02:	/*  ld.hu  */
 3052| 	case 0x03:	/*  ld.bu  */
 3053| 	case 0x04:	/*  ld.d   */
 3054| 	case 0x05:	/*  ld     */
 3055| 	case 0x06:	/*  ld.h   */
 3056| 	case 0x07:	/*  ld.b   */
 3057| 	case 0x08:	/*  st.d   */
 3058| 	case 0x09:	/*  st     */
 3059| 	case 0x0a:	/*  st.h   */
 3060| 	case 0x0b:	/*  st.b   */
 3061| 		{
 3062| 			int store = 0, signedness = 0, opsize = 0;
 3063| 
 3064| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3065| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3066| 			ic->arg[2] = imm16;
 3067| 
 3068| 			switch (op26) {
 3069| 			case 0x02: opsize = 1; break;
 3070| 			case 0x03: opsize = 0; break;
 3071| 			case 0x04: opsize = 3; break;
 3072| 			case 0x05: opsize = 2; break;
 3073| 			case 0x06: opsize = 1; signedness = 1; break;
 3074| 			case 0x07: opsize = 0; signedness = 1; break;
 3075| 			case 0x08: store = 1; opsize = 3; break;
 3076| 			case 0x09: store = 1; opsize = 2; break;
 3077| 			case 0x0a: store = 1; opsize = 1; break;
 3078| 			case 0x0b: store = 1; opsize = 0; break;
 3079| 			}
 3080| 
 3081| 			if (opsize == 3 && d == 31) {
 3082| 				fatal("m88k load/store of register pair r31/r0"
 3083| 				    " is not yet implemented\n");
 3084| 				goto bad;
 3085| 			}
 3086| 
 3087| 			ic->f = m88k_loadstore[ opsize
 3088| 			    + (store? M88K_LOADSTORE_STORE : 0)
 3089| 			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3090| 			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3091| 			       M88K_LOADSTORE_ENDIANNESS : 0) ];
 3092| 
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

End with one line: `FIXDRAFT_M88KZEROWORD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
