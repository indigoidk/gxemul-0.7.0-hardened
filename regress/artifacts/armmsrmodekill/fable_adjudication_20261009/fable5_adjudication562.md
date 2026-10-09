FABLE_SEAT_ALIVE_20261009_562
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: RATIFY WITH CHANGES (3) -- all nine rulings stand on the rules as written and on the evidence re-checked; three records corrections before the commit (one Astra correction survives in the staged ledger, the round's own adjudication record is stale at birth, PRETABLE5's mtime-order claim is void since its append).

Adjudicating seat: Fable 5.1, fired 2026-10-09 13:1x after the owner lifted the hold.  Badge: none of the #562 work is
mine; the main loop's rulings were Opus 5.5 badge A and this is the independent review of them.

## What I READ and what I RAN (kept apart)

READ (working tree, HEAD ef577140 + #562): the product diff and every enclosing function -- `msr_imm`/`X(msr)`
(`cpu_arm_instr.c:822-873`), `msr_imm_spsr`/`mrs_spsr` (`:875-957`), `arm_pop` whole (`:1621-1862`), the DPI
template's S-to-PC block (`cpu_arm_instr_dpi.c:207-267`), `arm_mode_is_modelled`/Save/Load/`arm_exception`
(`cpu_arm.c:529-784`), the reset (`cpu_arm.c:127-138`), `cpu_arm.h:95-269`, the CPS decode (`cpu_arm_instr.c:4125-4153`);
the 47-row probe in full; the gate section; the three records files and `vals562_draft.json`; the staging scripts
(`stage562.py`, `mk562_ledger.py`, `post562.py`, `manifest562.py`, `spec562.json`); PRETABLE5 with its CORRECTIONS,
SHIPPED_vs_FROZEN, the PASS2R5 brief, all eight seat answers (codex read at its final answer), `opus_pass2r5.md`,
`codex_confirm562.txt`, `cleanbuild.out`, `xscale_ab.out`, `xscale_clean.out`, both gate-14 logs' heads and tails.

RAN (read-only, no build, no gate, nothing written to any project tree): greps over `src/` for every writer of
`cd.arm.cpsr` and every `arm_exception()` caller; greps for `cd.arm.` readers outside `src/cpus`, includers of
`quick_pc_to_pointers.h` and `sizeof(struct cpu)` outside `src/cpus`; `md5sum` of the probe and gate against their
TESTED/frozen copies and a comment-stripped `diff` of the gate; my own `ast.dump` comparison (astcheck.py, in my scratch
dir) of the working probe against `killtable5_20261008/probe_frozen.py`, `opus_pass2r5_20261009/probe_frozen.py`, the
gate-TESTED copy and the staged copy; an `awk` recount of both `KILLTABLE5_lanes*.out`; `grep` of the witness and
run_head/run_fixed trailers; a read of the staged `check_probe_wiring.py`, `ledger_stage.json`, `matrix.html` and
`stage562/MANIFEST.txt`; `git --no-optional-locks diff --cached --stat` and `--numstat` on `precommit_check.sh`.
No WSL clone was built: every ruling below is settled by reading plus the preserved logs, and I say where a ruling
rests on a log I did not regenerate.

## The nine rulings

**R1 | UPHELD.**  Member 3 at the three guest writers of CPSR.M is correctly chosen and correctly scoped, and the
premise holds: the complete set of CPSR mode-field writers in the model is the reset (`cpu_arm.c:127-138`, SVC32 on
both branches), `msr_imm` (`:860-861`; `X(msr)` only reloads `arg[0]` and calls it), `arm_pop`'s `^` restore (`:1843`),
the DPI S-to-PC (`dpi.c:249`) and `arm_exception` (`cpu_arm.c:747-748`, whose table holds only modelled modes for the
seven exceptions any caller raises).  Every other `cpsr` write in `src/` is a T-bit or flag-nibble sync (grep, 36
sites).  CPS is not a writer: only the two exact words `cpsid i`/`cpsid f` are decoded, as NOPs (`:4133-4143`).  No
value a real guest of these cores writes is declined: the seven banked modes are the only ARMv4/v5/v6 modes;
`arm_cpu_types.h:102` does list a CORTEX-A5, but the model has no MON/HYP banks, no SMC and no mode-changing CPS, so
declining 0x16/0x1a there is the only available disposition anyway.  The zero-SPSR decline (I/F cleared, SVC kept)
is UNPREDICTABLE space that no real kernel reaches (both Linux and NetBSD write the SPSR before `movs pc,lr`).
Codex's whole-operation dissent is recorded, not absorbed -- correct: neither policy is architectural.

**R2 | UPHELD.**  After R1 no GUEST path installs an unmodelled mode, so the backstops are reachable only after a
debugger `cpsr=` plant (`CPU_SETTINGS_ADD_REGISTER32("cpsr", ...)`, `cpu_arm.c:196`, no bank switch).  The callers
named in each `default:` comment are exactly right, verified from source: Save is called unconditionally by
`arm_exception` (`:719`) and by the DPI (`dpi.c:221`) and conditionally by `msr_imm` (`:858`) -- and NOT by `arm_pop`
from a planted mode, because its selector `default:` (`:1814-1818`) returns before any Save (`:1841`); Load is
reached on the plant only by the DPI (its `default: spsr_copied = 0` leaves CPSR on the plant, `:233`, then `:251`).
Announce-and-return is correct there: there is no bank to save into or load from; `dbg save` measures the only
observable consequence (`sp0`).  Latent, not reachable, worth one sentence somewhere: `ARM_EXCEPTION_TO_MODE[5]` is
0 (`cpu_arm.h:126`, the 26-bit address exception) -- no caller raises 5 (grep: RESET/UND/SWI/PREF_ABT/DATA_ABT/
IRQ/FIQ only), and `arm_exception` would `exit(1)` at its own "unimplemented exception nr" (`:735-736`) before the
mode write.

**R3 | UPHELD.**  `uint32_t mask = ic->arg[1];` (`:824`), the decline edits `mask` only (`:846`), nothing in
`msr_imm` writes `ic->arg[]`; `X(msr)` refreshes `arg[0]` from the register on every execution (`:871`), which also
refutes glm's final-pass R1 ("the shown guard cannot be the measured fix").

**R4 | UPHELD.**  `arm_pop`: no early return between the guard (`:1826-1835`) and the PC load (`:1851-1861`);
`switch_register_banks` is computed from the CORRECTED `new_cpsr` (`:1837`), so a decline never calls Save/Load.
DPI: `new_cpsr` local, `spsr_copied` set only by the five SPSR arms, the decline keyed on it, `cpsr = new_cpsr` once
(`:249`), flags and Load after.  kimi-k3's ELSE ("the `default:` arm is NEW behaviour: S-to-PC from USR/SYS went
fatal at HEAD") is FALSE -- HEAD's switch had no `default:` either, so USR/SYS fell through with CPSR unchanged and
Load ran on a modelled mode; the new `default:` reproduces that fall-through byte for byte.  Correctly not filed;
say so in one clause (see Other, item 5) so it is not re-raised.

**R5 | UPHELD, and independently re-measured.**  AST minus the module docstring: the working probe (md5 59b99365),
the staged copy, `killtable5_20261008/probe_frozen.py` (8a9a9cac), `opus_pass2r5_20261009/probe_frozen.py`
(97555f3a) and the gate-TESTED copy (5ddc3242) are IDENTICAL (my ast.dump hash 87561d3f for all five) -- every kill
table and both gate runs transfer.  Recount of both lane files: 110 non-BASE runs, 104 distinct names, exactly one
at 47/47 (`M_msr_argmask`), 16 BASE legs at 47/47.  `run_head.out` 18/47 with the 29 named reds and
`TALLY_MATCHES_HEAD_EXPECT=yes`; `run_fixed.out` 47/47; the 17-row witness 14/17 with `kill 14,kill 15,save 2s`.
Row and session arithmetic re-derived from the probe: 47 rows (3 static), 43 sessions.  `grid cov` asserts G1 only
(read `grid_cov()`); G2/G3/G4 hold by construction of `grid_obs()`, as the header now says.

**R6 | UPHELD on the floor question.**  Under the carrier's rules as written, NONE of the eight measured escapes is a
floor cell, so clause (e) may absorb them.  The derivation, site by site:

* The floor at each RESTORE (pass-11 bound: the guard's dominating predicates x the device-STATE lvalues the repair
  path reads, jointly reachable; plus the 2026-09-09 label clause, because the selector switch's value flows into
  `new_cpsr`, which the guard reads) is {5 labels} x {latch clear, set} x {SPSR mode modelled, unmodelled} = 20 cells
  per path.  Every one of the 20 is ROWED (`src <path> <label>` R1..R4), on a whole-word channel that reds when the
  cell is exempted or its repair nulled (R_*/B_*/L_* kills in table 5).
* The five restore escapes (`N_*_forceN_first`, `N_*_orold_first`, `E_pop_forceN_clracc`) act on bits 31:8 of the
  VALUE BEING WRITTEN, conditioned on the latch.  The body masks and case-compares only `& 0x1f` (the helper); bits
  31:8 are tested nowhere.  Pass 11: "the bits of the single value being written are single-operand MARGINALS, not
  floor; joint cells outside the floor are clause-(e) coverage debt."  Outside the floor.
* The label x latch x mode-bit residue (126/160) is "a floor cell crossed with a single bit of a COMPARED value";
  #549 D1 pins that as the two-axis joint NOT CLAIMED discloses, and pins "TESTS means masks or compares as a case":
  the helper is a case-compare of the field, whose generating set is its regions (modelled / unmodelled), both of
  which every rowed cell drives.  Outside the floor.
* The two msr cells (`M_msr_clr0f_irq_first`, `M_msr_skip_irq_first`) are conditioned on the current-mode LABEL at
  `msr_imm`, where the label is NOT a body-tested partition: within the enclosing function the current mode is
  compared only as `== USR32` (`:826`) and `!= new mode` (`:850`), the six-way switch lives in Save/Load, i.e. in
  callees, which the DEPENDS-ON bound excludes.  So the floor at msr is {USR, non-USR} x {latch} x {helper} x
  {c-field in mask}, all rowed (usr mask, kill 14/15/1e/03, latch rpt, no cbit, msr wide).  Outside the floor.
* `M_msr_argmask` keeps the repair and ADDS a persistent side effect on `ic->arg[1]`; it weakens no dominating
  predicate and is not an operand swap from a body-read field; translation reuse is not a partition the body tests.
  The added comment is a claim sentence, and CLAIM -> ROW is discharged by the explicit no-row sentence that now
  cites the measurement.  Disclosure is the correct grade; the OWED dissent (deepseek, glm, kimi-k3) is argued from
  "the comment names the invariant", which is not one of the three enumerators the carrier binds the floor to.
  Codex's own final answer reaches the same grade ("disclosure is defensible under the adopted bound").
* The one real breach was of the CONTRACT (clause (e)): the header claimed force-1 "with the latch clear or set"
  and four cited carriers that cannot see the latch-clear cell on DPI/pop.  The L4 narrowing is permitted by (e)'s
  letter -- the clause asks that the header be falsifiable and true, and after the narrowing it is -- and the
  narrowed text cites the measurement that forced it, which is what keeps a post-measurement narrowing from being
  the oracle-correction shape in records form.  It is the WEAKER of the two in-round repairs; the stronger one (the
  zero-observation reorder, measured: the five go 46/47, fix 47/47, one carrier shifts) is filed with its table,
  by owner ruling.  Nothing here reopens the owner's choice.

  Wording precision for the records (not a change): "the bodies never test bits 31:8" explains the five restore
  escapes; the two msr cells are outside the floor for a DIFFERENT reason (the label is not body-tested at that
  site), and `M_msr_argmask` for a third (an added side effect is none of the three enumerators).  The CHANGELOG
  states only the first.

**R7 | UPHELD, scope independently verified.**  `xscale_ab.out`: HEAD 30/30 twice, both incremental #562 builds
28/30 twice (`ANCHOR_ISRC`, `ANCHOR_EXC`); `cleanbuild.out`: all three trees emptied (223/224/224 objects), parts
1 and 2 ok, "objects older than cpu_arm.h: 0" in each; `xscale_clean.out`: 30/30 twice on `build/` and
`/tmp/gxsec-build` (not build-asan -- the records now say so); `gate14_run2.out`: PASS 1110, 10:08:23-11:52:51,
msrmode 47/47.  Scope: `src/devices/Makefile.skel:15` lists `dev_i80321.o` with no header dependencies; outside
`src/cpus` the only reader of a `struct arm_cpu` field PAST `mode_warned` is `dev_i80321.c` (`:130-135`, `:440-446`
-- tmr0, tisr, tmr0_irq, tmr1_irq, i80321_isrc, i80321_inten); every other non-CPU access is `r[]`, `coproc[]` or
`cpsr`, all before the insertion; no file outside `src/cpus` includes `quick_pc_to_pointers.h` or uses
`sizeof(struct cpu)`; `cd` is the last member of `struct cpu` (`cpu.h:482-492`).  `testarm` attaches no i80321, so
the kill tables are unaffected.  `headerstaleobj` is the right filing and the right severity.

**R8 | UPHELD.**  Each row is filed for its stated reason and the reasons are true in the source: `armusrstop` --
`msr_imm_spsr`'s `default:` (`:900-913`) and `arm_pop`'s selector `default:` (`:1814-1818`) set `running = 0`, both
reachable from USR32/SYS32 by a guest (in USR32 the `^` strip at `:1631-1634` does not stop `return_flag` being set
at `:1635-1638`), and `mrs_spsr` answers 0 for USR/SYS (`:951-952`); `armspsrthumb` -- `:1852` masks the PC with
`0xfffffffc` and the DPI breaks out only for an odd PC (`dpi.c:262-266`); `armmmuvehicle`, `armmsrmodedebt`,
`headerstaleobj` -- as recorded.  Nothing this round OWES is missing from the filed list.  Three pre-existing
siblings that the round touched the neighbourhood of and nobody named -- for a floodclass note, not rows this
round owes: the UNLATCHED guest-drivable `fatal("[ bdt_load: s-bit: in usermode? ]")` (`:1632`, any USR-mode
`LDM ..{..}^` without PC); the unlatched `fatal("[ WARNING! Exception caused no mode change? ...")`
(`cpu_arm.c:759-760`, fired by every nested IRQ taken in IRQ mode, which real kernels with nested interrupts do);
and the latent `ARM_EXCEPTION_TO_MODE[5] = 0` from R2.

**R9 | CORRECT: 12 of 13 fully applied; item 4 survives in the staged ledger.**  Verified line by line in
`changelog_block.md`, `bugs_section.md`, `msg562.txt`, the probe docstring and the gate comment: items 1, 2, 3, 5, 6,
8, 10, 12, 13 applied; item 7 applied in B and in the staged `headerstaleobj` row ("can relink and report clearance
success"); item 9 applied in B and in the staged `armmmuvehicle` row (names `armsa1110areset`, `ARM_EXCEPTION_RESET`,
`X(reboot)`); item 11's three prospective claims are now MATERIALISED in `stage562/` -- the wiring has the detector
entry (line 873) plus 35 artifact lines for the 35 `.py` files under `artifacts/armmsrmodekill/`, the staged ledger
closes `armmsrmodekill` with the `probe:` witness and `closure.by = opus5-mainloop, badge A`, and the staged
`matrix.html` carries all five new rows (they are in the staged copies ONLY: the index today holds an unrelated
staged set, the probewiring redate, and the working tree none of #562's block -- the commit script swaps them in,
which is as designed).  **Item 4 is NOT fully applied:** the staged ledger's `armmsrmodekill.state_note`
(`ledger_stage.json` line 47801; same text in the working ledger) retains the "#562 IN WORK" segment with
"... `M_msr_argmask` 47/47 -- the cached-translation write, which NO stepping row can see ...", the exact sentence
Astra ruled FALSE (the filed `probe48.py` loop row is a stepping row that sees it, `KTR5_LANE5.out` 47/48).  The
fix is one clause: in `vals562_draft.json`'s `state_note_prefix` (or in `mk562_ledger.py` where the old note is
retained), append "(the IN WORK note's 'which NO stepping row can see' is FALSE -- none of the shipped 47 rows sees
it; the filed loop prototype does: opus_pass2r5_20261009/probe48.py, KTR5_LANE5.out)".  Correct in place; do not
delete the old segment.

## The three changes

1. **R9 item 4 in the ledger** (above): the `state_note` clause, before `mk562_ledger.py` runs.
2. **The round's adjudication record is stale at birth.**  `changelog_block.md` (lines 122-123), `msg562.txt`
   (lines 48-49) and the closure note in `vals562_draft.json` say "Fable 5.1 was DELIBERATELY NOT FIRED ... the main
   loop (Opus 5.5) adjudicated, badge A."  True of every PASS; false of the ROUND the moment this file exists.  Add
   one sentence to each: "Fable 5.1 adjudicated the main loop's nine rulings before the commit, 2026-10-09 13:1x
   (`regress/artifacts/armmsrmodekill/fable_adjudication_20261009/fable5_adjudication562.md`): RATIFY WITH CHANGES
   (3), all nine rulings upheld, the changes applied" -- and copy this file to that durable path (it is in my
   scratch dir now, which the volatile-path rule forbids a record to cite).  Keep the badge-A sentence for the
   passes; it is true.
3. **PRETABLE5.out's first line is now false.**  It says "written BEFORE kill table 5 (mtime precedes every LANE
   output)"; the CORRECTIONS section appended at 08:13 on 2026-10-09 moved the file's mtime past every lane output
   (00:22-02:37), so the mtime no longer proves the order the pre-table rule relies on.  One clause in that
   CORRECTIONS section: "this append voids the mtime-order claim in line 1; the pre-table order now rests on the
   lanes' own start times in `lane*.log` and the main loop's word".  Going forward, append corrections to a SIBLING
   file (`PRETABLE5_CORRECTIONS.out`) so the original keeps its mtime as the order witness -- a one-line note for
   the carrier's pre-table block, since this is the first instance.

## Other findings (no change required)

4. The `rows failed` gate check (`gate_arm.sh:1987`) greps `' FAIL '` across whole row lines; it is green today only
   because the probe prints `note[:64]` and no note's first 64 characters contain ` FAIL ` (the `kill 14` note does,
   past the cut).  A future note edit can red the gate falsely -- loud, the safe direction; worth one comment.
5. The CHANGELOG's final-pass paragraph records deepseek's G3 category error but not kimi-k3's "new `default:`
   behaviour" ELSE, which was checked and is false (R4).  One clause avoids a re-raise.
6. `minimax`'s "43 + 3 = 46 sessions" is a misreading of PRETABLE5's "(the grid adds 3)" -- 43 INCLUDES the grid's
   three; the probe prints 43.  Nothing to fix.
7. Grok's "a paste after `gate_end` never runs" was wrong and the Opus seat's "it runs and masks" was right; the
   shipped section sits before `gate_end` (`:1946-1988`, `gate_end` at `:1990`) and the comment-stripped gate is
   byte-identical to the TESTED copy (my diff), so the second gate run is not re-owed.
8. `est/` identity for the four src files is enforced by `stage562.py` (it refuses otherwise) and recorded in
   `gate14_run2.out`'s clearance header; not re-run here.
9. Three seat answers I read in full raised nothing the main loop dropped: grok (0 breaches; the odd-PC T
   composition is disclosed), glm (its C1 was measured KILLED 39/47 by the Opus seat -- `nofire` on eight rows),
   agy (the `report_dead`/REDS parser hole, filed in `armmsrmodedebt`).
