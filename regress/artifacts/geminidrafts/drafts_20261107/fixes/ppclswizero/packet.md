# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppclswizero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppclswizero`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c:X(lswi) -- the unfilled low-order bytes of the last register keep stale data (zero-filled only in MODE_POWER), and the byte assembly uses signed-overflow shifts -- WRONG-RESULT (+ host UB)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T22 (class WRONG-RESULT; reach U, user mode; effort: small; report rows: A4-17, A(b-1) class 1 (lswi shifts)).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3cdc32f0d3ab8f4d33f09a13a02b4c5cb80b3221, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/e88c21b997c83d816aea2f4806ed05a5723e5492.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:3056-3059.  Portable fix: yes -- port rs6000 3cdc32f, rs6000 e88c21b.  Filing check (TRIAGE.md): only `mrwstore2` mentions lswi, for partial completion.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port the mentioned commits to fix zero-fills and shifts

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 3056 (HEAD d2a6f233, lines 3011-3101)

```c
 3011| 	MODE_uint_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
 3012| 	unsigned char d[4];
 3013| 	int rs = ic->arg[0];
 3014| 
 3015| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
 3016| 	    / sizeof(struct ppc_instr_call);
 3017| 	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
 3018| 	    << PPC_INSTR_ALIGNMENT_SHIFT);
 3019| 	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
 3020| 
 3021| 	while (rs <= 31) {
 3022| 		uint32_t tmp = cpu->cd.ppc.gpr[rs];
 3023| 		if (cpu->byte_order == EMUL_BIG_ENDIAN) {
 3024| 			d[3] = tmp; d[2] = tmp >> 8;
 3025| 			d[1] = tmp >> 16; d[0] = tmp >> 24;
 3026| 		} else {
 3027| 			d[0] = tmp; d[1] = tmp >> 8;
 3028| 			d[2] = tmp >> 16; d[3] = tmp >> 24;
 3029| 		}
 3030| 		if (cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d),
 3031| 		    MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
 3032| 			/*  exception  */
 3033| 			return;
 3034| 		}
 3035| 
 3036| 		rs ++;
 3037| 		addr += sizeof(uint32_t);
 3038| 	}
 3039| }
 3040| 
 3041| 
 3042| /*
 3043|  *  Load/store string:
 3044|  *
 3045|  *  arg[0] = rs   (well, rt for lswi)
 3046|  *  arg[1] = ptr to ra (or ptr to zero)
 3047|  *  arg[2] = nb
 3048|  */
 3049| X(lswi)
 3050| {
 3051| 	MODE_uint_t addr = reg(ic->arg[1]);
 3052| 	int rt = ic->arg[0], nb = ic->arg[2];
 3053| 	int sub = 0;
 3054| 
 3055| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
 3056| 	    / sizeof(struct ppc_instr_call);
 3057| 	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
 3058| 	    << PPC_INSTR_ALIGNMENT_SHIFT);
 3059| 	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
 3060| 
 3061| 	while (nb > 0) {
 3062| 		unsigned char d;
 3063| 		if (cpu->memory_rw(cpu, cpu->mem, addr, &d, 1,
 3064| 		    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
 3065| 			/*  exception  */
 3066| 			return;
 3067| 		}
 3068| 
 3069| 		if (cpu->cd.ppc.mode == MODE_POWER && sub == 0)
 3070| 			cpu->cd.ppc.gpr[rt] = 0;
 3071| 		cpu->cd.ppc.gpr[rt] &= ~(0xff << (24-8*sub));
 3072| 		cpu->cd.ppc.gpr[rt] |= (d << (24-8*sub));
 3073| 		sub ++;
 3074| 		if (sub == 4) {
 3075| 			rt = (rt + 1) & 31;
 3076| 			sub = 0;
 3077| 		}
 3078| 		addr ++;
 3079| 		nb --;
 3080| 	}
 3081| }
 3082| X(stswi)
 3083| {
 3084| 	MODE_uint_t addr = reg(ic->arg[1]);
 3085| 	int rs = ic->arg[0], nb = ic->arg[2];
 3086| 	uint32_t cur = cpu->cd.ppc.gpr[rs];
 3087| 	int sub = 0;
 3088| 
 3089| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
 3090| 	    / sizeof(struct ppc_instr_call);
 3091| 	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
 3092| 	    << PPC_INSTR_ALIGNMENT_SHIFT);
 3093| 	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
 3094| 
 3095| 	while (nb > 0) {
 3096| 		unsigned char d = cur >> 24;
 3097| 		if (cpu->memory_rw(cpu, cpu->mem, addr, &d, 1,
 3098| 		    MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
 3099| 			/*  exception  */
 3100| 			return;
 3101| 		}
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

End with one line: `FIXDRAFT_PPCLSWIZERO: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
