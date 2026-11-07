# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcsprg2drop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcsprg2drop`, state `open`)

**title:** cpus/cpu_ppc_instr.c:X(mtspr_sprg2) -- SPRG2 writes are discarded on 32-bit CPUs (a FreeBSD hack) -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T43 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers [2026-11-02, records: in this emulator user mode reaches it too -- the MTSPR decode (cpu_ppc_instr.c:4701-4719) routes SPRG2 to X(mtspr_sprg2) with no privilege test, and X(mtspr) carries `TODO: Check permission` (:2807-2808); the architecture makes a user-mode SPRG2 write a privileged-instruction program interrupt (_scratchpad/ppc_oea_book3_v201.txt:1043, :1055-1058)]; effort: one-line; report rows: A4-26).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d13a974834e6781f7b25af10b9760e78a583b52d.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:2811-2818.  Portable fix: yes -- port rs6000 d13a974.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/cpu_ppc_instr.c:2825`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..bb9d8d35 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -2822,13 +2822,8 @@ X(mtspr) {
 	reg(ic->arg[1]) = reg(ic->arg[0]);
 }
 X(mtspr_sprg2) {
-	if (cpu->cd.ppc.bits == 32) {
-		// Ignore for now. FreeBSD/powerpc seems to write 0xffffffe0
-		// here, and read it back. If it is non-zero, it assumes a 64-bit
-		// cpu.
-	} else {
-		reg(ic->arg[1]) = reg(ic->arg[0]);
-	}
+	/* #ppcsprg2drop: FreeBSD hack removed */
+	reg(ic->arg[1]) = reg(ic->arg[0]);
 }
 X(mtlr) {
 	cpu->cd.ppc.spr[SPR_LR] = reg(ic->arg[0]);
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 2706-2827 (`+` marks a line the diff added or the point of a deletion)

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
 2822|  	reg(ic->arg[1]) = reg(ic->arg[0]);
 2823|  }
 2824|  X(mtspr_sprg2) {
 2825|+ 	/* #ppcsprg2drop: FreeBSD hack removed */
 2826|+ 	reg(ic->arg[1]) = reg(ic->arg[0]);
 2827|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCSPRG2DROP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCSPRG2DROP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
