# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcdecwrite` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcdecwrite`, state `open`)

**title:** cpus/cpu_ppc_instr.c:X(mtspr) DEC -- a software DEC write that flips bit 0 from 0 to 1 does not signal the decrementer exception -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T42 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A4-24).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/241f5e273caf75599ebb8ebc554e1e9faaacf508.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:2807-2810; src/cpus/cpu_dyntrans.c:450-454.  Portable fix: yes -- port rs6000 241f5e2.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc_instr.c` -- AT HEAD, lines 2706-2823 (`*` marks a line your previous draft changed)

```c
 2706|  X(mcrf)
 2707|  {
 2708|  	int bf_shift = ic->arg[0], bfa_shift = ic->arg[1];
 2709|  	uint32_t tmp = (cpu->cd.ppc.cr >> bfa_shift) & 0xf;
 2710|  	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
 2711|  	cpu->cd.ppc.cr |= (tmp << bf_shift);
 2712|  }
 2713|  
 2714|  
 2715|  /*
 2716|   *  crand, crxor etc:  Condition Register operations
 2717|   *
 2718|   *  arg[0] = copy of the instruction word
 2719|   */
 2720|  X(crand) {
 2721|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2722|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2723|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2724|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2725|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2726|  	if (ba & bb)
 2727|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2728|  }
 2729|  X(crandc) {
 2730|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2731|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2732|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2733|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2734|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2735|  	if (ba & !bb)	/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
 2736|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2737|  }
 2738|  X(creqv) {
 2739|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2740|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2741|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2742|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2743|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2744|  	if (!(ba ^ bb))
 2745|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2746|  }
 2747|  X(cror) {
 2748|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2749|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2750|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2751|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2752|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2753|  	if (ba | bb)
 2754|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2755|  }
 2756|  X(crorc) {
 2757|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2758|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2759|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2760|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2761|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2762|  	if (ba | !bb)	/*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */
 2763|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2764|  }
 2765|  X(crnor) {
 2766|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2767|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2768|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2769|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2770|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2771|  	if (!(ba | bb))
 2772|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2773|  }
 2774|  X(crxor) {
 2775|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2776|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2777|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2778|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2779|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2780|  	if (ba ^ bb)
 2781|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2782|  }
 2783|  
 2784|  
 2785|  /*
 2786|   *  mfspr: Move from SPR
 2787|   *
 2788|   *  arg[0] = pointer to destination register
 2789|   *  arg[1] = pointer to source SPR
 2790|   */
 2791|  X(mfspr) {
 2792|  	/*  TODO: Check permission  */
 2793|  	reg(ic->arg[0]) = reg(ic->arg[1]);
 2794|  }
 2795|  X(mfspr_pmc1) {
 2796|  	/*
 2797|  	 *  TODO: This is a temporary hack to make NetBSD/ppc detect
 2798|  	 *  a CPU of the correct (emulated) speed.
 2799|  	 */
 2800|  	reg(ic->arg[0]) = cpu->machine->emulated_hz / 10;
 2801|  }
 2802|  X(mftb) {
 2803|  	/*  NOTE/TODO: This increments the time base (slowly) if it
 2804|  	    is being polled.  */
 2805|  	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)
 2806|  		cpu->cd.ppc.spr[SPR_TBU] ++;
 2807|  	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
 2808|  }
 2809|  X(mftbu) {
 2810|  	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBU];
 2811|  }
 2812|  
 2813|  
 2814|  /*
 2815|   *  mtspr: Move to SPR.
 2816|   *
 2817|   *  arg[0] = pointer to source register
 2818|   *  arg[1] = pointer to the SPR
 2819|   */
 2820|  X(mtspr) {
 2821|  	/*  TODO: Check permission  */
 2822|* 	reg(ic->arg[1]) = reg(ic->arg[0]);
 2823|* }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "X(mtspr) {\n\t/*  TODO: Check permission  */\n\treg(ic->arg[1]) = reg(ic->arg[0]);\n}",
    "new": "X(mtspr) {\n\t/*  TODO: Check permission  */\n\tuint32_t old = reg(ic->arg[1]);\n\treg(ic->arg[1]) = reg(ic->arg[0]);\n\n\t/* #575: Signal decrementer exception if MSB flips 0 -> 1 */\n\tif (&reg(ic->arg[1]) == &cpu->cd.ppc.spr[SPR_DEC]) {\n\t\tif ((old >> 31) == 0 && (cpu->cd.ppc.spr[SPR_DEC] >> 31) == 1\n\t\t    && !(cpu->cd.ppc.cpu_type.flags & PPC_NO_DEC))\n\t\t\tcpu->cd.ppc.dec_intr_pending = 1;\n\t}\n}",
    "why": "Intercept mtspr to SPR_DEC and assert dec_intr_pending when the sign bit flips, mirroring the dyntrans hardware decrement logic."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCDECWRITE: DEFECT, 1 FINDINGS
1. **Site coverage**: The diff addresses the defect in `src/cpus/cpu_ppc_instr.c` but completely misses `src/cpus/cpu_dyntrans.c`, which the issue explicitly names.
2. **CONTROL FLOW**: No control flow keywords (`return`, `goto`, `break`) or early exits were added. No tail code is skipped.
3. **RETURN VALUE**: No path returns anything different; the function does not have an explicit return value.
4. **State changes**: The diff does not change or clear any unrelated state; it solely sets `cpu->cd.ppc.dec_intr_pending = 1` upon the specified condition. 
5. **House idioms**: The added comment correctly follows the `/* #NNN: ... */` pattern.
**Findings:**
`src/cpus/cpu_dyntrans.c:450`: DEFECT: The issue states the defect exists in `cpu_dyntrans.c` as well, but this file is unmodified. Fix: Port the same MSB flip check to the corresponding `mtspr` translation block in `cpu_dyntrans.c`.
FIXREVIEW_PPCDECWRITE: DEFECT, 1 FINDINGS
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

End with two lines: `REVISION_PPCDECWRITE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCDECWRITE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
