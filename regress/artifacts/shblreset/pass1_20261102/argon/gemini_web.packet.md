# Reading task: pass 1: shblreset (Argon) (Gemini web; 2026-11-02)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBP1SHBLRESET-5084` on a line of its own.

# PANEL PASS 1 -- `shblreset` (#577): a SuperH general exception taken with SR.BL set stores the power-on reset code where the manual says manual reset, and clobbers the TLB multiple-hit code

Fired 2026-11-02 17:5x.  HEAD `987cb596`.  Roster (owner 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3, Argon (Gemini web), Grok 4.7.
Astra is on its weekly wall (hotmail login, "try again at Nov 8th"); its pass 1 is OWED and recorded as SEAT WALLED.  The owner holds
every commit until Astra answers; the round runs to the F2 pass and then waits.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just the
derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `987cb596`.**  Do not read `./src/` under the project root (a pristine 2021 upstream
copy) nor `.claude/worktrees/` (an older fork copy); if your line numbers disagree with mine, say so rather than reconciling.
**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from this packet
rather than guessing.  **VERDICT LINE FIRST** (`VERDICT: PROCEED / PROCEED WITH CHANGES (<n>) / DO NOT PROCEED`), repeated last.
File-reading seats: scope your reading to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/sh_tlbmulti_probe.py`, `regress/gate_sh_rounding.sh`
(HEAD copies) and the manual `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\sh7750_hardware.txt`.  Reading only; nothing is to be built or run.

## 1. The defect as filed, the proposed fix, and the MEASURED witness

Ledger row `shblreset` (open, MED): "BL already set stores EXPEVT_RESET_POWER instead of EXPEVT_RESET_MANUAL".  `src/cpus/cpu_sh.c`,
`sh_exception()`, HEAD :910-918: when `sr & SH_SR_BL`, after a `fatal()` print, `expevt = EXPEVT_RESET_POWER;` -- EVERY exception code is
rewritten to H'000.  The manual (section 3) says a general exception with BL set performs a MANUAL reset with EXPEVT = H'020, and lists
the two TLB multiple-hit exceptions as reset-category in their own right with code H'140, which the BL rule therefore must not touch.

**Proposed fix (one predicate, one constant):**

```diff
-		/*  This is actually OK in two cases: a User Break,
-		    or on NMI interrupts if a special flag is set?  */
-		/*  TODO  */
-
-		expevt = EXPEVT_RESET_POWER;
+		/*  #577: a general exception taken with BL set is a MANUAL
+		    reset -- sh7750_hardware.txt 5.5.3 (:12302-12304), EXPEVT
+		    H'020 (:678-681) -- not a power-on reset (H'000), which is
+		    what stood here.  The two TLB multiple-hit exceptions are
+		    reset-category in their own right (Table 5.2, :12006 and
+		    :12010; code H'140, :12461) and keep their code.  A user
+		    break would be the other exemption; EXPEVT_BREAK is never
+		    raised in this tree.  Interrupts do not reach this path:
+		    cpu_dyntrans.c gates their delivery on BL.  */
+		if (expevt != EXPEVT_RESET_TLB_MULTI_HIT)
+			expevt = EXPEVT_RESET_MANUAL;
```

Control flow is unchanged: `EXPEVT_RESET_POWER`, `EXPEVT_RESET_MANUAL` and `EXPEVT_RESET_TLB_MULTI_HIT` share one arm (:1015-1021: pc =
0xa0000000, vbr = 0, SR |= IMASK, FD cleared); only the latched EXPEVT value differs.  The `fatal()` at :911 stays (disclosed below).

**Witness, rung 3, MEASURED 2026-11-02 17:4x** -- `regress/artifacts/shblreset/witness_20261102/sh_blreset_witness.py` on a fresh WSL clone
of HEAD (`/tmp/gxdivw`, binary newer than source) and on the same clone plus the fix (`/tmp/gxfix577`); unmodified in-tree `-E landisk
-M 64`, the rig kernel loaded for construction only; the cold debugger pre-sets SR, places one real guest instruction (TRAPA #1,
0xc301) or the committed multiple-hit program (`sh_tlbmulti_probe.py`'s three stores) at 0x8c010000, steps, and reads EXPEVT and PC
back with `print expevt` / `print pc`, anchored to the command echo (the dump does not show them):

```
                                 HEAD (witness_head.out)                    fixed (witness_fixed.out)
bl trapa expevt    sr=MD|BL      0x00000000 want 0x00000020 FAILED-FOR-THE-REASON-UNDER-TEST   0x00000020 ok
bl trapa pc        same session  0xa0000000 ok  (LIVENESS: the reset path ran)                 0xa0000000 ok
nobl trapa expevt  sr=MD         0x00000160 ok  (CONTROL: the general vector, EXPEVT readable)  0x00000160 ok
bl multihit        sr=MD|BL      0x00000000 want 0x00000140 FAILED-FOR-THE-REASON-UNDER-TEST   0x00000140 ok
RESULT                           2/4                                                            4/4
```

The second red row is the clobber half: on HEAD a BL-set guest's TLB multiple hit latches H'000, so its reset handler cannot tell a
multiple hit from a power-on.  Both halves are red for exactly the predicted value, and the same script reads 4/4 on the fixed clone
(clause (i) of the witness rule).

## 2. SETTLED PREMISES (C0 output and what is re-read today)

C0 at `987cb596`: `git log -1 -- src/cpus/cpu_sh.c` = `7e5c0f6c 2026-08-23 #458`; `-- regress/sh_tlbmulti_probe.py` = `0678450e
2026-08-22 #457`; `grep -c shblreset CHANGELOG.md` = 0; `OUTSTANDING_BUGS.md:24063` carries the id entry.  **The round has not shipped.**
`git log -L910,918:src/cpus/cpu_sh.c` returns one commit, the upstream import: the block is upstream residue.

* `EXPEVT_RESET_POWER 0x000`, `EXPEVT_RESET_MANUAL 0x020`, `EXPEVT_RESET_TLB_MULTI_HIT 0x140`, `EXPEVT_TRAPA 0x160`, `EXPEVT_BREAK 0x1e0`
  (`src/include/thirdparty/sh4_exception.h:57-73`).  `SH_SR_BL 0x10000000`, `SH_SR_MD 0x40000000`, `SH_SR_RB 0x20000000` (`cpu_sh.h:192-194`).
* `EXPEVT_RESET_MANUAL` appears at HEAD only in the define and in the :1016 case label; `EXPEVT_BREAK` only in the define: the user-break
  exemption the old comment mentions has no raiser in this tree (`git grep` over `src/`).
* The only raiser of `EXPEVT_RESET_TLB_MULTI_HIT` is `dev_sh4.c:1178` (the UTLB associative-write multiple hit, #457).
* Interrupts do not reach the BL block: `cpu_dyntrans.c:247-250` delivers an SH interrupt only when `!(sr & SH_SR_BL)` (quoted below).
  An NMI is not modelled separately in this tree (the old comment's "NMI interrupts if a special flag is set?" has no code behind it).
* `regress/sh_tlbmulti_probe.py:55-57` already records the clobber as a fact ("`cpu_sh.c` rewrites ANY expevt to `EXPEVT_RESET_POWER`
  when `SR.BL` is set ... a BL-set guest silently latches `0x000` instead") -- that note becomes a historical note under this fix.
* The committed `tlbm` rows all run with BL CLEAR (reset SR has BL clear; the `tlbm sr` row pre-sets 0x40008000), so no committed row
  re-pins under this fix (read from the probe; the pass-1 question Q5 asks you to check).
* Working tree: `regress/sh_tlbmulti_probe.py` is CLEAN; `regress/gate_sh_rounding.sh` holds three unrelated uncommitted hunks of
  this session's 09-17 work (old :530/:590/:822) AND round #576's two staged hunks are pending in a HEAD-based copy (not committed); this
  round's gate hunk (section 5) is staged the same way and the two rounds' copies are reconciled at whichever lands second.

**Stated as questions:**
* Does the manual's "registers of the other modules are set to their states following a manual reset" (5.5.3) carry any observable this
  round must model?  I believe NOT: the tree models neither reset's module effects, on either value, and this round changes the EXPEVT
  code only (disclosed, section 6).
* Is `EXPEVT_RESET_TLB_MULTI_HIT` the ONLY code the BL rule must exempt?  Table 5.2 lists power-on, manual, H-UDI and the two multiple
  hits as reset-category; of those only H'140 is ever raised through `sh_exception()` here.

## 3. THE CODE AND THE INTERRUPT GATE, VERBATIM (HEAD)

`src/cpus/cpu_sh.c:910-918`:
```c
	if (cpu->cd.sh.sr & SH_SR_BL) {
		fatal("[ sh_exception(): BL bit already set. ]\n");

		/*  This is actually OK in two cases: a User Break,
		    or on NMI interrupts if a special flag is set?  */
		/*  TODO  */

		expevt = EXPEVT_RESET_POWER;
	}
```
`:941-955` (the common code; EXPEVT is latched here, BEFORE the switch):
```c
	cpu->cd.sh.spc = cpu->pc;
	cpu->cd.sh.ssr = cpu->cd.sh.sr;
	cpu->cd.sh.sgr = cpu->cd.sh.r[15];

	if (intevt > 0) {
		cpu->cd.sh.intevt = intevt;
		expevt = -1;
	} else {
		cpu->cd.sh.expevt = expevt;
	}

	sh_update_sr(cpu, cpu->cd.sh.sr | SH_SR_MD | SH_SR_RB | SH_SR_BL);

	/*  Most exceptions set PC to VBR + 0x100.  */
	cpu->pc = vbr + 0x100;
```
`:1015-1021` (the reset arm the three codes share):
```c
	case EXPEVT_RESET_POWER:
	case EXPEVT_RESET_MANUAL:
	case EXPEVT_RESET_TLB_MULTI_HIT:
		cpu->pc = 0xa0000000;
		cpu->cd.sh.vbr = 0x00000000;
		sh_update_sr(cpu, (cpu->cd.sh.sr | SH_SR_IMASK) & ~SH_SR_FD);
		break;
```
`src/cpus/cpu_dyntrans.c:247-250`:
```c
		if (cpu->cd.sh.int_to_assert > 0 && !(cpu->cd.sh.sr & SH_SR_BL)
		    && ((cpu->cd.sh.sr & SH_SR_IMASK) >> SH_SR_IMASK_SHIFT)
		    < cpu->cd.sh.int_level)
			sh_exception(cpu, 0, cpu->cd.sh.int_to_assert, 0);
```

## 4. THE MANUAL, VERBATIM (`_scratchpad/sh7750_hardware.txt`, SH7750 Hardware Manual Rev. 7.00; line numbers from `awk NR`)

```
  678:                                    When a general exception other than a user break occurs, a
  679:                                    manual reset is executed. The value in EXPEVT at this time
  680: 6.6.2 Pair Single-       196        is H'0000 0020; the value of the SPC and SSR registers is
  681:                                    undefined.
12300: 5.5.3 Exception Requests and BL Bit
12301: When the BL bit in SR is 0, general exception and interrupts are accepted.
12302: When the BL bit in SR is 1 and a general exception other than a user break is generated, the CPU's
12303: internal registers and the registers of the other modules are set to their states following a manual
12304: reset, and the CPU branches to the same address as in a reset (H'A000 0000). For the operation in
12305: the event of a user break, see section 20, User Break Controller (UBC).
12306: If an ordinary interrupt occurs, the interrupt request is held pending and is accepted after the BL
```
Table 5.2 (:11998-12012), the reset category -- these lines are UNSTAGGERED (name and code on one line):
```
12000: Reset  Abort type Power-on reset                   1       1   H'A000 0000 --  H'000
12002:                      Manual reset                  1       2   H'A000 0000 --  H'020
12004:                      H-UDI reset                   1       1   H'A000 0000 --  H'000
12006:                      Instruction TLB multiple-hit  1       3   H'A000 0000 --  H'140
12010:                      Data TLB multiple-hit exception 1     4   H'A000 0000 --  H'140
12012: General Re-          User break before instruction 2       0   (VBR/DBR) H'100/-- H'1E0
12461:    Exception code H'140 is set in EXPEVT, initialization of VBR and SR is performed, and a
12462:    branch is made to PC = H'A000 0000.
```
(:678-681 is a revision-history table rendered with an interleaved column -- "6.6.2 Pair Single- 196" at :680 belongs to another
row; the sentence reads continuously across :678-681 without it.)

## 5. THE PROPOSED DETECTOR

**Vehicle: `regress/sh_tlbmulti_probe.py`** (clean at HEAD; its `session(pre=...)` already pre-sets SR, runs a program at CODE, and reads
`expevt`/`pc`/`vbr`/`sr` back through `print`).  Two rows appended, both under `pre=["sr=0x500000f0"]` (MD|BL, IMASK 0xf; RB clear
so the pre-exception stores use bank 0 exactly as the committed rows do):

| row | program | reads | want | channel: what differs under HEAD or a weakened fix |
|---|---|---|---|---|
| `tlbm bl general` | TRAPA #1 (0xc301), step 1 | expevt | 0x00000020 | HEAD and the verbatim reinstatement give 0x000; the identity body (no rewrite) gives 0x160 |
| `tlbm bl multihit` | the committed three-store program | expevt | 0x00000140 | HEAD gives 0x000; a fix without the exemption gives 0x020 |

A `pc` readback on the BL rows is not added: `tlbm pc` already pins the shared arm, and the fix does not touch it.  Gate
(`gate_sh_rounding.sh:254-259`): `sh_tlbmulti rows run` 6 -> 8 (EQUALITY); the two names join the per-row loop.  The probe's docstring
note at :55-57 is reworded to the past tense with the round number.

**Floor.**  (a) the base leg: the two new rows red (the witness already measured both values on HEAD); (b) the verbatim reinstatement
(`expevt = EXPEVT_RESET_POWER;`): both rows red; (c) identity body for a predicate round = the BL block deleted (no rewrite at all):
`tlbm bl general` reads 0x160 -> red, `tlbm bl multihit` reads 0x140 -> GREEN by construction (the row cannot distinguish "exempted" from
"never rewritten"), so clause (c) is carried by `tlbm bl general` alone -- stated in the contract; (d) the fix ADDS one predicate
(`expevt != EXPEVT_RESET_TLB_MULTI_HIT`), so the (d) mutants weaken it: `M_noexempt` (always MANUAL) -> `bl multihit` red;
`M_wrongexempt` (exempt TRAPA instead of the multiple hit, i.e. `expevt != EXPEVT_TRAPA`) -> `bl general` reads 0x160 red, `bl
multihit` reads 0x020 red; `M_power` (exempt kept, constant POWER) -> `bl general` red.  (e) the contract names the two general-exception
codes actually driven (TRAPA; the multiple hit) and discloses the rest: a re-introduction keyed to ONE other general code (say
`expevt == EXPEVT_RES_INST`) escapes both rows -- clause (e) material, since the body tests nothing on `expevt` beyond the new predicate.
**Q3 asks whether a second general code (RES_INST, a TLB miss) should ride as a row at two sessions.**

**De-escalation does not apply**: no host-stopping check is removed; the `fatal()` print stays.

## 6. DISCLOSED, NOT IN SCOPE

* The `fatal()` at :911 is unlatched and guest-drivable (a guest can take general exceptions with BL set in a loop): the held
  `floodclass` row's class; this round changes the code value only.  **Q4 asks whether a `(once)` latch should ride here** -- it is the
  house idiom, one field and two lines, same function, but it is a second behaviour change in a one-constant round.
* The manual's "registers of the other modules" manual-reset effects are not modelled under either value.
* SPC/SSR are "undefined" by the manual on this path; the tree stores pc and sr into them as for every exception; unchanged.
* H-UDI reset (H'000) has no raiser; nothing to exempt.

## 7. QUESTIONS

**Q1, premise audit.**  Which premise in sections 1-5 is false?  In particular: (a) is `EXPEVT_RESET_TLB_MULTI_HIT` the only code the
BL rule must exempt at HEAD; (b) does any committed row or guest path depend on H'000 being latched on this path; (c) is the user-break
sentence right (no raiser); (d) do interrupts truly never reach the block (the `intevt > 0` path sets `expevt = -1` AFTER the block --
walk it: an interrupt delivered with BL set would be rewritten too, so the `cpu_dyntrans.c` gate is load-bearing); (e) the witness
rows' encodings and wants.

**Q2, the partition.**  Over {general exception, TLB multiple hit, interrupt, user break} x {BL clear, BL set}: which cells does the fix
change, which does it leave, and does the detector (two new rows + the six committed) have a member in each reachable cell?

**Q3, candidate weakenings.**  For each, EQUIVALENT to the fixed form or not, the input at which it first differs, and the row that
reds: (a) `expevt = EXPEVT_RESET_POWER;` verbatim; (b) the block deleted; (c) exemption removed (always MANUAL); (d) exemption on the
wrong code (`!= EXPEVT_TRAPA`); (e) exemption widened to `expevt < 0x100` (every reset-category code); (f) `if (expevt == EXPEVT_TRAPA)
expevt = EXPEVT_RESET_MANUAL;` (keyed to the one general code the table drives).  Which are floor, which clause (e)?  Should a second
general-code row ride?

**Q4, option-set completeness.**  The disposition is to CORRECT THE CONSTANT with one exemption.  Is there a member this brief did not
name?  Does the unlatched `fatal()` ride here as `(once)`, or stay with `floodclass`?

**Q5, the vehicle.**  Two rows in `sh_tlbmulti_probe.py`, pin 6 -> 8.  Do the committed rows re-pin under the fix (I read NO: all run
BL clear)?  Is the SR pre-set 0x500000f0 right (RB clear, so the program's bank-0 seeds are the ones the stores use)?

**If, while verifying a claim, you found something ELSE -- say so.**  End with `VERDICT: PROCEED / PROCEED WITH CHANGES (<n>) / DO NOT
PROCEED`, and name every premise you could not settle from this packet.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBP1SHBLRESET: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
