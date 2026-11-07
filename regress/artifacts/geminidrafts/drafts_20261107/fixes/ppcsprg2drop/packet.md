# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcsprg2drop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcsprg2drop`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c:X(mtspr_sprg2) -- SPRG2 writes are discarded on 32-bit CPUs (a FreeBSD hack) -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T43 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers [2026-11-02, records: in this emulator user mode reaches it too -- the MTSPR decode (cpu_ppc_instr.c:4701-4719) routes SPRG2 to X(mtspr_sprg2) with no privilege test, and X(mtspr) carries `TODO: Check permission` (:2807-2808); the architecture makes a user-mode SPRG2 write a privileged-instruction program interrupt (_scratchpad/ppc_oea_book3_v201.txt:1043, :1055-1058)]; effort: one-line; report rows: A4-26).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d13a974834e6781f7b25af10b9760e78a583b52d.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:2811-2818.  Portable fix: yes -- port rs6000 d13a974.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port the commit and enforce privilege check on SPRG2 writes

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 2811 (HEAD 2d25df65, lines 2766-2856)

```c
 2766| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2767| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2768| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2769| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2770| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2771| 	if (!(ba | bb))
 2772| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2773| }
 2774| X(crxor) {
 2775| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2776| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2777| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2778| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2779| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2780| 	if (ba ^ bb)
 2781| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2782| }
 2783| 
 2784| 
 2785| /*
 2786|  *  mfspr: Move from SPR
 2787|  *
 2788|  *  arg[0] = pointer to destination register
 2789|  *  arg[1] = pointer to source SPR
 2790|  */
 2791| X(mfspr) {
 2792| 	/*  TODO: Check permission  */
 2793| 	reg(ic->arg[0]) = reg(ic->arg[1]);
 2794| }
 2795| X(mfspr_pmc1) {
 2796| 	/*
 2797| 	 *  TODO: This is a temporary hack to make NetBSD/ppc detect
 2798| 	 *  a CPU of the correct (emulated) speed.
 2799| 	 */
 2800| 	reg(ic->arg[0]) = cpu->machine->emulated_hz / 10;
 2801| }
 2802| X(mftb) {
 2803| 	/*  NOTE/TODO: This increments the time base (slowly) if it
 2804| 	    is being polled.  */
 2805| 	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)
 2806| 		cpu->cd.ppc.spr[SPR_TBU] ++;
 2807| 	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
 2808| }
 2809| X(mftbu) {
 2810| 	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBU];
 2811| }
 2812| 
 2813| 
 2814| /*
 2815|  *  mtspr: Move to SPR.
 2816|  *
 2817|  *  arg[0] = pointer to source register
 2818|  *  arg[1] = pointer to the SPR
 2819|  */
 2820| X(mtspr) {
 2821| 	/*  TODO: Check permission  */
 2822| 	reg(ic->arg[1]) = reg(ic->arg[0]);
 2823| }
 2824| X(mtspr_sprg2) {
 2825| 	if (cpu->cd.ppc.bits == 32) {
 2826| 		// Ignore for now. FreeBSD/powerpc seems to write 0xffffffe0
 2827| 		// here, and read it back. If it is non-zero, it assumes a 64-bit
 2828| 		// cpu.
 2829| 	} else {
 2830| 		reg(ic->arg[1]) = reg(ic->arg[0]);
 2831| 	}
 2832| }
 2833| X(mtlr) {
 2834| 	cpu->cd.ppc.spr[SPR_LR] = reg(ic->arg[0]);
 2835| }
 2836| X(mtctr) {
 2837| 	cpu->cd.ppc.spr[SPR_CTR] = reg(ic->arg[0]);
 2838| }
 2839| 
 2840| 
 2841| /*
 2842|  *  rfi[d]:  Return from Interrupt
 2843|  */
 2844| X(rfi)
 2845| {
 2846| 	uint64_t tmp;
 2847| 
 2848| 	reg_access_msr(cpu, &tmp, 0, 0);
 2849| 	tmp &= ~0xffff;
 2850| 	tmp |= (cpu->cd.ppc.spr[SPR_SRR1] & 0xffff);
 2851| 	reg_access_msr(cpu, &tmp, 1, 0);
 2852| 
 2853| 	cpu->pc = cpu->cd.ppc.spr[SPR_SRR0];
 2854| 	quick_pc_to_pointers(cpu);
 2855| }
 2856| X(rfid)
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

End with one line: `FIXDRAFT_PPCSPRG2DROP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
