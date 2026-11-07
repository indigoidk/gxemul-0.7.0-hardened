# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppctblcarry` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppctblcarry`, state `open`)

**title:** PPC: an mftb polled at TBL == 0xffffffff pushes the 64-bit TBL cell to 2^32; the #141 batch update then truncates it and the carry into TBU is lost

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): shoddprfield`'s open rule question; Astra kept the grade. * `ppctblcarry` MED -- PPC: an `mftb` polled at TBL == 0xffffffff pushes the 64-bit TBL cell to 2^32; the #141 batch update truncates it and the carry into TBU is lost (cpu_ppc_instr.c:2789-2795; cpu_dyntrans.c:455-458; ppc_pem_32and64_2005.txt:1716). Rare, deterministic; keep TBL 32-bit in `X(mftb)`. * `armmrcr15fla

**The drafter's own reading:** STILL PRESENT: YES -- `2805| 	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..5b0a9f1e 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -2802,7 +2802,8 @@ X(mfspr_pmc1) {
 X(mftb) {
 	/*  NOTE/TODO: This increments the time base (slowly) if it
 	    is being polled.  */
-	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)
+	cpu->cd.ppc.spr[SPR_TBL] = (uint32_t)(cpu->cd.ppc.spr[SPR_TBL] + 1);
+	if (cpu->cd.ppc.spr[SPR_TBL] == 0)
 		cpu->cd.ppc.spr[SPR_TBU] ++;
 	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
 }
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 2706-2809 (`+` marks a line the diff added or the point of a deletion)

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
 2805|+ 	cpu->cd.ppc.spr[SPR_TBL] = (uint32_t)(cpu->cd.ppc.spr[SPR_TBL] + 1);
 2806|+ 	if (cpu->cd.ppc.spr[SPR_TBL] == 0)
 2807|  		cpu->cd.ppc.spr[SPR_TBU] ++;
 2808|  	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
 2809|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCTBLCARRY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCTBLCARRY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
