VERDICT: PROCEED WITH CHANGES (4)

OPUS 5.5 seat, #577 `shblreset`, pass 1 (design brief `brief_shblreset_p1.md`). This was written after the fix was built and
measured, as the coordinator asked. I judge the design on its own terms and mark with **[answered]** each point the later record
(packet 2 / the kill-table artifacts) already settles. Reading only. HEAD source via `git show HEAD:`, the manual via
`awk 'NR>=A && NR<=B'`.

**The design is right**: one predicate and one constant. The four changes below are about the DETECTOR and two premises the brief
states as fact. Two of the detector changes are floor matters for the design as written.

## Q1 -- premise audit

**(a) Is H'140 the only code to exempt?** TRUE at HEAD. `git grep 'sh_exception('` lists twenty raisers: cpu_sh_instr.c
(RES_INST, FPU_DISABLE/SLOT, ADDR_ERR_LD/ST, SLOT_INST, TRAPA), memory_sh.c:249/:368 (TLB miss/prot/mod), cpu_dyntrans.c:250
(interrupts), and dev_sh4.c:1178, the only `EXPEVT_RESET_TLB_MULTI_HIT`. Nothing raises H'000, H'020 or H'1E0 (`EXPEVT_BREAK`
appears only in `sh4_exception.h:73`).

**(b) Does any committed row or guest path depend on H'000 here?** No row does. The six committed `tlbm` rows run with BL clear;
`tlbm single` wants 0x0, but it raises nothing. This is MEASURED, not merely read: on HEAD `tlbm expevt` reads 0x140, which it
could not do if the default session had BL set (base_head.raw, 7/10 with all six committed rows ok) **[answered]**. For a guest
path, a landisk kernel has no handler at 0xa0000000 that inspects EXPEVT, so the observable is for software with its own reset
code. MED is generous; I would not argue it down.

**(c) The user-break sentence.** "No raiser" is true, but it is the weaker half. The manual's UBC section (`:41448-41452`) says
that with BL=1 a break condition sets CMFA/CMFB and **exception handling is not started**. So the user break is not an exemption
the BL block needs at all: it never becomes an exception. The pass-1 comment ("A user break would be the other exemption")
mis-describes it **[answered: the shipping comment says "suppressed at the UBC (:41448-41452) and never reaches here"]**.

**(d) Interrupts. THE BRIEF'S FRAMING IS FALSE, in the direction that makes the comment over-claim.** Walk `sh_exception()` as
the brief invites. The BL block rewrites the LOCAL `expevt`. Then `:945-947` does `if (intevt > 0) { intevt = ...; expevt = -1; }`
and **never stores `cd.sh.expevt`**. Then `switch (expevt)` takes `case -1`. So an interrupt reaching the block with BL set would
have its rewritten value thrown away. EXPEVT, INTEVT and the vector are unaffected under HEAD and under the fix. **The
`cpu_dyntrans.c:247` gate is NOT load-bearing for anything this round changes.** It is load-bearing only for whether a BL-set
interrupt is delivered at all, which is a different and correct behaviour (held pending, `:12306`). The pass-1 comment's
"Interrupts do not reach this path" is true but rests on the wrong fact **[answered: the shipping comment adds "the intevt path
below discards expevt before storing it"]**. Note one consequence for Q2: the interrupt cells cannot carry a row and need none.

**(e) Encodings and wants.** `trapa #1` = `11000011 iiiiiiii` = 0xc301. The `sh_tlbmulti_probe.py` witness rows want 0x020 and
0x140. Both are correct against `:12383-12384` (5.6.1 (2) Manual Reset, which also lists "a general exception other than a user
break ... while the BL bit is set" among its SOURCES at `:12376`) and against `:12499`. The brief cites H'020 to `:678-681`, which is
the revision-history reprint; cite `:12383-12384` **[answered, P2]**. The brief also cites H'140 to `:12461`, the INSTRUCTION TLB
multiple hit. The tree's only raiser is the UTLB associative write, which `3.7.4` calls a DATA TLB multiple hit, i.e. 5.6.1 (5)
Operand TLB Multiple-Hit, `:12499`. Same code, wrong sentence (change C4).

**Premise I could not settle:** whether `Initialize_Module(Manual)`'s effects (`:12302-12304`) differ observably from power-on
for any module this tree models. I believe the brief is right that neither value models them. I did not audit every module.

## Q2 -- the partition

Taking {general, TLB multiple hit, interrupt, user break} x {BL clear, BL set}:

| cell | fix changes it? | row in the PROPOSED detector (2 new + 6 committed) |
|---|---|---|
| general, BL set | YES (H'000 -> H'020) | `tlbm bl general` (TRAPA only) |
| multi-hit, BL set | YES (H'000 -> H'140) | `tlbm bl multihit` |
| multi-hit, BL clear | no | the six committed rows |
| **general, BL clear** | no | **NONE** |
| interrupt, either | no, inert by (d) | not rowable; none owed |
| user break, either | unreachable (no raiser; UBC suppresses under BL) | none |

**The empty (general, BL clear) cell is a floor gap for the design as written (change C1).** The fix DEPENDS ON its dominating
predicate `cpu->cd.sh.sr & SH_SR_BL`. Clause (d)'s DEPENDS-ON bound (1) puts that guard in the enumeration. A widened guard
(`& (SH_SR_BL | SH_SR_MD)`) rewrites a BL-clear general exception to H'020, and NO proposed row runs one: the committed rows are all
multiple hits (exempt), and both new rows run with BL set. So the proposed eight rows would be swept clean by a guard mutant.
**[answered: `tlbm trapa`, sr = MD only, wants H'160; `M_guard` measured 9/10 with `tlbm trapa` reading 0x020, M_guard.raw]**.

Also worth a disclosure line now: the guard's partition beyond BL. Every BL row runs MD|BL. A guard NARROWED to
`(sr & SH_SR_BL) && (sr & SH_SR_MD)` keeps every row green and changes a reachable cell. BL=1 with MD=0 is reachable by
`ldc Rm,SR` or `rte` from privileged code. The body tests nothing on MD, so this is clause (e), not floor. Name it.

## Q3 -- candidate weakenings

| | form | equivalent? | first differs at | proposed rows that red | class |
|---|---|---|---|---|---|
| a | `expevt = EXPEVT_RESET_POWER;` | no | any BL-set exception | both | floor (b) |
| b | block deleted | no | BL-set TRAPA (H'160) | `bl general` only; `bl multihit` reads H'140 either way | floor (c), carried by one row, as the brief says |
| c | always MANUAL | no | BL-set multi-hit | `bl multihit` (0x020) | floor (d) |
| d | `!= EXPEVT_TRAPA` | no | both | both | floor (d) |
| e | `expevt < 0x100` exempt | no | **see below** | `bl multihit` only | floor (d) |
| f | `if (expevt == EXPEVT_TRAPA) MANUAL` | no | any other BL-set general code | **NONE: a total escape of the proposed detector** | see below |

**(e)'s description is false (change C2, premise).** "Widened to `expevt < 0x100` (every reset-category code)" is wrong because
H'140 is NOT below 0x100. The form exempts H'000-H'0E0, which are the TLB misses and the address errors (GENERAL codes), and
REWRITES the multiple hit. It is not a widening of the exemption; it removes it and adds four general-code exemptions. Against the
proposed rows: `bl multihit` reads 0x020 (red), and `bl general` (TRAPA 0x160 >= 0x100) is rewritten to 0x020 (green)
**[answered: PRETABLE_CORRECTION.out quotes the prediction it refutes; M_lt100 measured 8/10, red at mhit AND at the misaligned-load
row, 0x0e0 < 0x100]**.

**(f) is the shape that matters.** With TRAPA the only general code driven, the rewrite keyed to TRAPA is indistinguishable from
the fix on every proposed row. The body's own partition is {== 0x140, != 0x140}, so strictly the second general code is clause
(e), not floor. But a TOTAL escape bought by a single-member sample of the cell the round exists to fix is exactly what the
ask-again would spend itself on, and one row closes it. **Change C3: ride a second general code, a misaligned load (`mov.l @r1,r2`,
0x6212, r1 odd, H'0E0 -> want H'020).** It is chosen BELOW 0x100 so it also discriminates (e) **[answered: `tlbm bl ldmis`,
M_trapaonly 9/10]**. The undriven remainder (H'040-H'0C0, H'100, H'120, H'180, H'1A0, H'800, H'820) goes into the contract in BOTH
directions **[answered: P3, and `M_resinst` measured a total escape, 10/10, filed as `shblundriven`]**.

## Q4 -- option set

Members: (1) correct the constant, exempt one code (proposed); (2) exempt by CATEGORY (`expevt` in {000, 020, 140}), which is
equivalent today because nothing raises 000/020, and reads better only if a raiser ever arrives; (3) model `Manual_reset()` fully
(`:12391`, `Initialize_CPU`/`Initialize_Module`), out of scope and partly unfaithful for the multiple hit (`cpu_sh.c`'s own #457
comment explains why not reinitialising is the faithful part); (4) DELETE the BL block, which is wrong, because it delivers H'160 to
VBR+0x100 where the manual says reset. (1) is right. (2) is a comment sentence at most: say that a future H-UDI or RESET-pin raiser
(both H'000) would need its own exemption.

**The `fatal()`**: leave it with `floodclass`. It is now an ARCHITECTURAL event announced as if it were an emulator fault, which
makes the wording worse, not just the frequency. That is still a second behaviour change in a one-constant round; file the wording
with the latch.

## Q5 -- the vehicle

Committed rows do not re-pin: they run BL clear and raise only H'140 or nothing **[answered: fixed.raw 10/10, the six committed rows
ok]**. SR pre-set 0x500000f0: the value is right, but the brief's REASON ("RB clear so the bank-0 seeds are the ones the stores
use") is not the mechanism. The debugger's `sr=` does not go through `sh_update_sr()`, so no bank swap happens, and `r0=` writes the
array the instructions read whatever RB says **[answered: P9, post-table edit 3]**.

## Found while checking

* The TEA/PTEH sentence of the multiple-hit transition (`:12496-12498`, "the virtual address ... is set in TEA ... VPN in PTEH")
  is not modelled: dev_sh4.c:1178 passes vaddr 0 and the reset arm sets neither. This is pre-existing (#457), not this round's.
  What TEA should hold for an associative WRITE is not settled from the text I read. CANNOT SETTLE; worth a filing question.

## The changes

C1. Add a BL-CLEAR general-exception row (a guard-side floor cell). **[done: `tlbm trapa` + M_guard]**
C2. Correct the brief's description of `expevt < 0x100` (it exempts general codes and rewrites H'140). **[done in
    PRETABLE_CORRECTION]**
C3. A second general code below 0x100 rides as a row. Disclose the rest both ways. Disclose an MD-qualified guard.
    **[done except the MD disclosure]**
C4. Cite H'020 at `:12383-12384` **[done]** and the multiple hit at `:12499`, the operand side and the tree's only raiser. The
    shipping comment still cites only `:12461`.

VERDICT: PROCEED WITH CHANGES (4)
