OPUS_MSR_PASS2R5_1009

VERDICT: SHIP-WITH-CHANGES | 1 floor breach.  The breach is clause (e), the contract.  Product code is unchanged and still correct.  Codex's prediction is CONFIRMED by measurement: a decline that forces N on the FIRST (latch-CLEAR) DPI or pop restore scores 47/47.  Two more edits do the same: OR-ing the old CPSR's bits 31:8 into that decline, and forcing N on a latch-clear pop accept.  The contract bullet "forcing it to 0 or to 1, with the latch clear or set" is therefore false for bits 31:8 on both restore paths.  Two fixes work.  For this commit I recommend the L4 narrowing: it is comment-only and AST-identical, so no re-table is owed.  The alternative is a zero-observation reorder of the two restore grid sessions.  It is MEASURED: the same 5 escape texts all go red (46/47), with the fix still 47/47.  But it owes a full re-table, so file it.  `M_msr_argmask`: disclosure is the correct grade (Q2).  My prototype loop row kills it, and also its immediate-form twin, and stays green on the fix.  It is licensed but not owed.  The gate section is correct on the fixed and HEAD logs, but it must go BEFORE `gate_end`.  Placed literally after it, I measured gate 14 exiting 0 with failing checks.

RECORDS NOTE ON THIS SEAT: every score below was copied from `KTR5_LANE*.out` / `KTR5W2_LANE*.out`, which the driver wrote, and not from my predictions.  The "prediction" column is what I expected before the runs.  Every prediction held, but only the logs are the evidence.

## How this was measured

- **Clones.** `/tmp/gxopus562r5/LANE1..5/tree`, made by `cp -a` of my r4 clone.  Nothing was written to GXEMUL-SEC, est, build, build-asan or /tmp/gxsec-build.  Five lanes ran concurrently.
- **Baseline.** The 4 SEC working-tree files (md5 `67805fcd`, `71e3bfcc`, `e2baa870`, `9929566b`) were `cmp`-checked against SEC before the first mutant, at every restore, and at the end.  The SEC diff equals `fix5.diff` line for line (sorted compare, 9 hunks).  HEAD legs used `git show HEAD:` (ef577140) of the same 4 files.
- **Probe.** A frozen copy of `regress/arm_msrmode_probe.py`, md5 `97555f3a` (47 rows, 43 sessions), copied at 03:19.  **The SEC probe was edited at 03:26:42**, to md5 `edd47c92`: the main loop applied the panel's records corrections (G1, grid cov scope, `step call`).  Its AST minus the module docstring is identical to the copy I measured; I checked that with `ast.dump`.  So every score here transfers to `edd47c92`.
- **Builds.** Each build ran `rm -f src/cpus/*.o gxemul; make -j2` and then checked `[ gxemul -nt <each of 4 sources> ]`.  A clone-local `.MUTANT` sentinel was set per mutant.  Mutants are in `mutr5.py`.  Every find-text must occur exactly once (presence pin), so a mutant that failed to apply is reported, never scored.
- **Controls.**
  - The 47-row BASE was 47/47 in LANE1-4, both before and after.
  - The 48-row prototype BASE was 48/48 in LANE5.
  - The reorder prototype BASE was 47/47 (wave 2, LANE1).
  - Every lane ended `RESTORED ... sentinel cleared` after both waves.  `finalcheck.sh` re-verified all 5 clones afterwards: no `.MUTANT`, sources `cmp`-clean vs SEC, binaries newer than the sources.
  - All 36 preserved logs end in their completion sentinel (`ARMMSRMODE_DONE` / `LOOPSTANDALONE_DONE`).
  - The SEC product md5s were unchanged at the end.
  - Wave 1 ran 03:30-05:03; wave 2 ran 04:40-05:40.
- **Mutator.**  `mutr5.py` was md5 `f3fadd74` for wave 1 and `6f87c501` for wave 2.  The only difference is the added `M_pop_retafter` entry, so the shared mutant texts are byte-identical.
- **Artifacts** (scratchpad `msr/opus5/`):
  - Lane outputs and logs: `KTR5_LANE1..5.out`, `KTR5W2_LANE1..5.out`, `logs_LANE*/`, `logs2_LANE*/`.
  - Mutator and drivers: `mutr5.py`, `setup.sh`, `ktr5.sh`, `ktr5w2.sh`, `launch5.sh`, `launch5w2.sh`, `finalcheck.sh`, `headsrc/`.
  - Loop row: `loop_row.py`, `loop_standalone.py`, `looptest0.out`, `mk_probe48.py`, `probe48.py`.
  - Reorder prototype: `mk_probe47r.py`, `probe47r.py`.
  - Offline analysis: `latchcov.py` + `.out`, `gridcov_scope.py` + `.out`.
  - Gate tests: `gatetest/` (`harness.sh`, `harness_after.sh`, `mkfx.py`, `fx/`, `harness_results.txt`), plus `gate_section.sh` (the brief's section, verbatim).

  **/tmp evaporates: copy these into `regress/artifacts/` before any record cites them.**  Each `.py` among them then needs a `check_probe_wiring.py` MANIFEST class (see "Something else").

## Q1 -- the floor on the shipped composite: YES, a one-line edit keeps all 47 green

### Wave 1: the shipped 47-row probe (LANE5 used the 48-row prototype)

| mutant | edit (the fix is kept; this is added) | score | red rows | prediction |
|---|---|---|---|---|
| **N_pop_forceN_first** | pop latch-CLEAR block: `new_cpsr \|= 0x80000000;` | **47/47 ESC** | none | escape (codex + me) -- held |
| **N_dpi_forceN_first** | DPI latch-CLEAR block: same | **47/47 ESC** | none | escape -- held |
| **N_pop_orold_first** | pop latch-CLEAR block: `new_cpsr \|= cpu->cd.arm.cpsr & 0xffffff00;` | **47/47 ESC** | none | escape -- held |
| **N_dpi_orold_first** | DPI latch-CLEAR block: same | **47/47 ESC** | none | escape -- held |
| **E_pop_forceN_clracc** | before pop's guard: `if (!(mode_warned & POP)) new_cpsr \|= 0x80000000;` (every pop restore while the latch is clear, accepts included) | **47/47 ESC** | none | escape -- held |
| N_pop_clrN_first (force-0 twin) | pop latch-CLEAR block: `new_cpsr &= ~0x80000000;` | 41/47 killed | src pop x5 (R2 `7fffffdX`), grid pop (obs 0 `7ffffff1`) | killed -- held |
| N_dpi_clrN_first (force-0 twin) | DPI: same | 41/47 killed | src dpi x5, grid dpi (obs 0) | killed -- held |
| E_msr_forceN_clracc (control) | msr: `new_value = ic->arg[0] \| (latch MSR ? 0 : 0x80000000)` | 46/47 killed | **grid pop ALONE** (G4 p1 obs 52/54/56: `80000013 != 00000013`) | killed -- held |
| M_msr_forceN_first (control) | msr: N forced on the first (latch-clear) decline (3-part, `opus_first`) | 46/47 killed | **msr wide ALONE** (`80000011`) | killed -- held |
| **M_msr_clr0f_irq_first** (codex's cell) | msr decline clears only M[3:0] (bit 4 written) at IRQ, first decline only | **47/47 ESC** | none | escape -- held |
| **M_msr_skip_irq_first** | msr guard skipped at IRQ while the latch is clear | **47/47 ESC** | none | escape -- held |
| M_msr_argmask (48-row) | decline also `ic->arg[1] &= ~ARM_FLAG_MODE` | 47/48 | **msr loop only** (the 47 shipped rows green) | as killtable5 + loop kills -- held |
| M_msr_arg0cur (48-row) | decline rewrites `ic->arg[0]`'s mode to the current mode | 47/48 | **msr loop only** | shipped rows blind, loop kills -- held |
| HEAD (48-row) | HEAD ef577140 sources | 18/48 | the 29 shipped reds + msr loop; `TALLY_MATCHES_HEAD_EXPECT=yes`; msr loop dies in Load at mode 20 | -- |

BASE / BASE_AFTER:

- LANE1-4: BASE 47/47 and BASE_AFTER 47/47, each lane.
- LANE5: BASE 48/48 and BASE_AFTER green (loop row, standalone).
- All five lanes end `RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared`.
- Wave 1 ran 03:30-05:03.

**DENOMINATOR -- what I swept, and why there.**  `grid cov` checks (outcome x bit x polarity) **aggregated over latch states**.  The corrected header now says so.  The axis the CONTRACT names that `grid cov` does not model is the LATCH.  So the sweep is:

- {latch CLEAR} x {DPI, pop, msr} x {decline, accept} x {force-1, force-0, OR-old}, at bit 31.  OR-old covers bits 31:8.
- msr {IRQ} x {latch clear} x {guard skipped, width narrowed to M[3:0]}.  This is codex's label x latch x mode-bit product.
- The cached translation, in both forms.
- Plus HEAD.

**Count:**

- Wave 1 built 13 mutants: 11 on the shipped probe and 2 on the 48-row prototype.  **9 of the 13 keep all 47 shipped rows green**: the 7 marked ESC, plus the two cached-translation mutants, which only `msr loop` reds.
- Wave 2 adds M_pop_retafter (glm's C1; killed).  It also re-runs, on the reorder prototype, the 5 restore escapes, one force-0 twin and a BASE leg.

I re-derived codex's static counts independently, by enumerating every latch-clear decline in every row.

**First-clear decline x bits 31:8 x path: 72 cells, 48 unobserved** (all of DPI's and pop's force-1 cells).  On the msr path those cells are held by `msr wide` ALONE (M_msr_forceN_first).

**Label x latch x mode-bit: 126/160** (MSR 40/60, DPI 43/50, POP 43/50), with the missing cells exactly as codex lists them:

- msr has no latch-clear decline at IRQ/ABT/UND/SYS at all.
- The restores' latch-clear decline at IRQ/ABT/UND is src R2's SPSR 0x0f, which leaves IRQ bit 1, ABT bits 0-2 and UND bits 0,1,3 equal to the label's bit.

**Why exactly these escape -- the mechanism, from the logs:**

- Every latch-CLEAR restore decline that renders bits 31:8 has SPSR bits 31:8 = 1.  That covers grid dpi/pop obs 0 (p1, NEW `0xffffffee`) and src R2 (SPSR `0xffffffcf`).  So a forced 1 cannot change the word.
- The rows whose first-decline SPSR has those bits CLEAR read back only part of the word:
  - `rst movs`, `rst ldm`, `zero spsr`, `latch ind`: `m=`, `if=`
  - `latch rpt`: `a=..`
  - `tbit`: low byte
  - `encl2`: `& 0x1f`
- OLD's bits 31:8 are 0 at EVERY latch-clear restore decline in this probe (grid obs0 OLD `0x11`; src R2 after `cf_0`; `0xd3` elsewhere).  So OR-old is not merely unobserved, it is equivalent within the probe.
- The force-0 twins die on exactly the cells the force-1 forms cannot use.  This confirms the mutation sites are live.

**GRADE.**

- The class is outside the joint-cell FLOOR.  The restore body TESTS only the latch and (via the helper) M[4:0], never bits 31:8.  So under the carrier's generating-set rule this would be clause-(e) debt.
- But the CONTRACT CLAIMS it explicitly: "a decline OR accept taking ANY bit 31:5 from the old CPSR, or forcing it to 0 or to 1, **with the latch clear or set** (grid *: G1 complementary pairs; src R2/R3; tbit; msr wide)".  None of the four cited carriers can see the latch-clear cell on DPI or pop:
  - G1 is aggregated over latch states.
  - src R2 has SPSR bits 31:6 SET.
  - tbit renders the low byte.
  - msr wide is msr only.
- **A claimed edit that escapes is a breach of clause (e): L2, repair in-round.**  Because the class is outside the floor, the in-round repair may be the L4 (narrow the claim) rather than a new row.
- I count it as ONE breach class, matching codex.

**The two msr label x latch escapes** (M_msr_clr0f_irq_first, M_msr_skip_irq_first) are **outside the contract as worded**.  The msr bullets ("skipped at one current-mode label", "fewer than all five mode bits at ANY label") name no latch axis, and their cited carriers are latch-set rows.  So they are (e) debt to DISCLOSE.  They are not a second breach.  If the owner reads "at ANY label" as latch-independent, they become part of the same class and take the same L4.

### Wave 2: the zero-observation L2 alternative, measured (`probe47r.py`, md5 `c55be925`)

**The change.**  In `grid_obs()`, for the DPI and POP paths only, MOVE the first polarity-2 accept and the first polarity-2 decline to the front of the session, accept first.  As a result the site's latch-CLEAR accept and decline both see NEW bits 31:5 = 0 against OLD bits 31:6 = 1.

- The observation multiset is unchanged: counts 56/52/58, every want unchanged, `grid cov` 0 uncovered.
- Offline, `latchcov.py` shows the force-1 cells at latch clear covered for bits 5-31 on both restore paths, accept and decline.
- The latch-clear force-0 cells stay held by src R1/R2 (bits 31:6) and tbit (T).  The wave-1 force-0 kills above show src R2 carries them.
- The msr path is left as is: msr wide holds its latch-clear decline (M_msr_forceN_first), and grid pop's G4 holds its latch-clear accept (E_msr_forceN_clracc).

| mutant | probe | score | red rows |
|---|---|---|---|
| BASE (fix) | probe47r | **47/47** | none |
| N_pop_forceN_first | probe47r | **46/47 killed** | grid pop obs 1 `80000011 != 00000011` |
| N_dpi_forceN_first | probe47r | **46/47 killed** | grid dpi obs 1 `80000011` |
| N_pop_orold_first | probe47r | **46/47 killed** | grid pop obs 1 `ffffff11` |
| N_dpi_orold_first | probe47r | **46/47 killed** | grid dpi obs 1 `ffffff11` |
| E_pop_forceN_clracc | probe47r | **46/47 killed** | grid pop obs 0 `80000017 != 00000017` (the latch-clear ACCEPT) and obs 1 `80000011` |
| N_pop_clrN_first (force-0 twin) | probe47r | 42/47 killed | src pop x5 (R2) -- grid pop no longer carries it (its latch-clear cell is now p2), src R2 still does |
| M_pop_retafter (glm's C1) | SHIPPED 47 | 39/47 killed | rst ldm, latch ind, latch rpt, src pop x5 (all `nofire`) |

**The same five mutant texts that score 47/47 on the shipped probe are each killed by a reorder that adds no observation and changes no want.**  This is the measured L2 alternative.

It is NOT free, though.  It changes which observation runs with the latch clear, so mutants previously killed through grid obs 0's latch-clear p1 cell lose the grid as a carrier.  The measured instance is N_pop_clrN_first: 41/47 down to 42/47, still killed by src R2.

So adopting it owes the full re-table on probe47r, plus its own pass 2 under the repair-chain rule.  That is why I recommend the L4 for THIS commit and filing the reorder (with this table) as the follow-up.  If the owner takes it now, fold the loop row in with it.

## Q2 -- `M_msr_argmask`: DISCLOSURE is the right grade; the loop row is licensed, not owed

**Prototype, measured.**  The row is `loop_row.py`; `probe48.py` = the shipped probe plus that row before `row count`, with the identity at 48 and `msr loop` appended to the HEAD tally.  It is one session:

- r5 walks a table of eight operands on the DATA page (0x9200; outputs at 0x9400 -- never the code page, so no store invalidates a translation).
- Each pass, inside ONE `step 72`, executes the SAME translated `msr cpsr_fsxc,r1` (accept, DECLINE 0x0e, accepts, DECLINE 0x15, accepts) and the SAME translated `msr cpsr_c,#0x14` (always declined, from a different label each pass), reading the CPSR after each.
- Only r1 r3 r5 r6 r7 are used, unbanked in every mode.  All of its words are encoding-checked in-row (`enc` gate).

Results:

- **fix:** green.  Standalone `11 11 11 11 12 12 17 17 17 17 1b 1b 1f 1f 13 13 n=1` (BASE and BASE_AFTER); composite **48/48**.
- **M_msr_argmask:** composite **47/48, msr loop the only red**.  Got `11` x16: after the reg-form decline at pass 2, every later accept through that translation stays in FIQ.
- **M_msr_arg0cur** (immediate form): composite **47/48, msr loop the only red**.  Got `.. 12 11 17 11 ..`: from pass 3, the `#0x14` decline switches back to the stale FIQ.
- **HEAD:** `dead` (dies in Load at mode 20); composite 18/48 with exactly 30 reds.

So the row pins BOTH forms the NOT CLAIMED entry discloses.

Grok and codex say an immediate MSR in a loop would not distinguish `M_msr_argmask`.  That is right: the immediate's operand is a constant, always declined.  But the same comment forbids a second, equally plausible edit, which rewrites `ic->arg[0]` to the current mode.  That one is NOT equivalent in a loop, and the row kills it.

**Grade, from the repair's own DEPENDS-ON.**

- (1) The predicates dominating `mask &= ~ARM_FLAG_MODE` inside `msr_imm` are the USR32 strip, `(mask & ARM_FLAG_MODE)`, `!arm_mode_is_modelled(ic->arg[0])` and the latch test.  M_msr_argmask weakens none of them.
- (2) It is not an operand swap drawn from a field the guarded body reads.  It KEEPS the local repair and ADDS a write to `ic->arg[1]`, which is the local's source, never read by the body.
- Translation reuse is not a partition the body tests, so the joint-cell clause adds no cell.
- The added comment ("Only the local mask changes: ic->arg[] is a cached translation") is a claim sentence.  CLAIM -> ROW is discharged by "an explicit no-row sentence", and the corrected NOT CLAIMED entry is exactly that.

So by every rule the carrier states, the row is not OWED, and clause (e) disclosure is a correct grade.  glm's "behaviourally inside G3" reads G3 (a property of the generator's observation set) as a claim about re-executed translations; it is not one.

**Recommendation.**  The row carries a MEASURED delta (two cached-translation mutants killed, fix green, HEAD dead), so the addition licence permits it.

- **If the round takes the wave-2 L2 repair**, the probe is re-tabled anyway; fold the loop row into the same re-measure.
- **If it takes the L4**, ship with the disclosure and FILE the row, citing `KTR5_LANE5.out`.  Adding a row now would owe its own pass 2 under the repair-chain rule, against the owner's one-pass ruling.

## Q3 -- records

**FALSE, still in the tree at `edd47c92`:**

1. **Contract bullet "with the latch clear or set (grid *: G1 complementary pairs; src R2/R3; tbit; msr wide)".**  This is the Q1 breach.  Measured false for bits 31:8 on DPI and pop: force-1 and OR-old at the first decline, and force-1 at a latch-clear pop accept.  None of the four cited carriers can see that cell.

   **Suggested L4 text:** "... with the latch SET (grid G1); with the latch CLEAR the restore paths are observed only with SPSR bits 31:8 SET (grid obs 0, src R2) -- a force-1 or OR-old of bits 31:8 on a FIRST DPI/pop decline, or a force-1 on a latch-clear restore accept, is NOT CLAIMED (MEASURED 47/47: N_pop_forceN_first, N_dpi_forceN_first, N_pop_orold_first, N_dpi_orold_first, E_pop_forceN_clracc); on msr the latch-clear decline is held by msr wide ALONE and the latch-clear accept by grid pop's G4 p1 cells ALONE."

2. **The msr label x latch cells belong in NOT CLAIMED.**  msr has no latch-clear decline at IRQ/ABT/UND/SYS.  The restores' latch-clear mode-bit cells at IRQ/b1, ABT/b0-2 and UND/b0,1,3 are unobserved.  Measured: M_msr_clr0f_irq_first and M_msr_skip_irq_first both 47/47.

3. **The new header line "G2, G3 and G4 hold by the generator's construction ... NOT by a row" is TRUE.**  I measured it offline (`gridcov_scope.out`).  With the generator stripped of G3's 0x18-0x1a -- the very values that carry the repair-4 `& 0x17` kill -- `grid cov` still reads 0 uncovered.  It also reads 0 with msr's SYS label removed.  It notices only a lost restore label (ABT: 4).

   So a future generator edit can silently re-open H_narrow_17 while every static check stays green.  A cheap static extension would close it: assert the G2/G3/G4 sets in `grid cov`.  FILE that.

4. **PRETABLE5 §1 still files G2/G3/G4 under "COVERAGE TABLE (grid cov ...)".**  The 03:27 CORRECTIONS note fixes §2 and the addendum, but not this attribution.

**TRUE, re-checked:**

- **The corrected ic->arg[] paragraph.**  `debugger.c` clears at entry to an interaction and skips the clear while `debugger_n_steps_left_before_interaction > 0`, or during `step call` (now said).  `X(msr)` reloads `ic->arg[0]` from the register on every execution, so glm's R1 ("the guard reads a cached arg[0], so the shown fix cannot be the measured one") is refuted.
- **The PRETABLE5 CORRECTIONS note.**
- **killtable5's headline.**  110 RESULT lines, 104 distinct names, only M_msr_argmask at 47/47, 16 baselines 47/47.  Of the six shared names, H_narrow_17 is textually identical and the other five differ in text but are semantically equal, so "104 distinct" is right.
- **The HEAD tally.**  18/47, the 29 named reds; the grid rows die in Load at mode 14 (`run_head.out` diag).
- **G1's corrected wording and the 56/52/58 counts.**
- **The G2 80/80, G3 96/96 and G4 8/8 static counts.**
- **deepseek's G3 objection is a category error.**  The USR/SYS-LABEL restores that stop the CPU are labels, not accepted targets; G3 accepts 0x10 and 0x1f as targets from SPSR-bearing labels.

## Q4 -- gate 14: scores correctly; three changes before commit, two optional

I ran the section VERBATIM against canned logs.  The harness is `gatetest/harness.sh`: it uses lib.sh's real `check`/`gate_end`, with `python3` shadowed to print a fixture.

| fixture | result |
|---|---|
| fixed (`run_fixed.out`) | PASS 7/7: emitted 47, 47/47, REDS none |
| HEAD (`run_head.out`) | FAIL 2 of 7 (rows correct 18; reds = the 29); 29 FAIL rows displayed, emitted 47 |
| truncated (no DONE) / two DONE lines / REDS line empty | FAIL (fails closed) |
| `report_dead` shape (CONTROL=DEAD, RESULT=0/0, DONE, **no REDS line**) | FAIL as "no unique, valid completion record" -- closed, but MISDIAGNOSED |
| inconsistent producer: one row printed FAIL with RESULT 47/47 + REDS none | **PASS** |
| one row line replaced by a duplicate of another (47 lines) | **PASS** |
| **section placed AFTER `gate_end`**, earlier gate-14 check failing, HEAD log | **script exit status 0** -- run.sh would score gate 14 PASS |

**Changes required before commit:**

1. **Insert the section BEFORE `gate_end`, not after it.**  The brief says "appended".  Taken literally, the section runs after the verdict has been printed, and its last `check` sets the script's exit status.  That masks EVERY gate-14 failure, the new section's own included.  Grok's "a paste after gate_end never runs" is wrong: it runs, and it masks.
2. **Raise `SCORE_CLAIMS_MANIFEST` 32 -> 33** in `tools/precommit_check.sh`.  With the section inserted, `check_score_claims.py` prints `SCORE_CLAIMS_PINNED=33` and `SCORE_CLAIMS_PASS ... 12 of 33 stems also have a probe docstring checked`.  The one-token stem and the unquoted 47 are seen, and the docstring's x/47 claims pass.
3. **Fill the `MEASURED: <OWED ...>` line.**  My four BASE legs are 47/47 on md5 `97555f3a`, AST-identical to `edd47c92`.  They are a citable base leg once preserved under regress/artifacts.  If the committed bytes move again, a leg on those exact bytes is the clean citation.

**Optional:**

- Make `report_dead` print `ARMMSRMODE_REDS=control`, or let the parse accept CONTROL=DEAD without REDS, so a dead vehicle reads as dead.
- Add `check "arm_msrmode rows failed" "$(grep -E ' want=' "$MSRLOG" | grep -c ' FAIL ')" "0"`, which closes the aggregate-trust hole above.  I checked the fixed log: no note's first 64 characters contain " FAIL ".

`ARMMSRMODE_SESSIONS` (glm) does not need pinning: every session feeds a scored row, so a vanished session reds its row or drops the row count.

## Something else

- **The force-0 / force-1 asymmetry is the shape of the whole class.**  The grid's single latch-clear observation per path, obs 0, is polarity 1.  A latch-clear check can only see a forced value that DISAGREES with what that first decline expects.  Corollary: **the msr path's latch-clear coverage hangs on single rows by accident of session structure.**
  - msr wide is the sole carrier of the msr latch-clear decline (M_msr_forceN_first 46/47).
  - grid pop's three G4 p1 observations are the sole carrier of the msr latch-clear accept (E_msr_forceN_clracc 46/47).  They see it only because no msr decline ever happens in the pop session, so its OLD-setting MSRs all run with the msr latch clear.  Adding an msr decline to that session would silently drop this coverage.
- **glm's C1 is measured and HELD:** a pop decline that assigns the right CPSR word and then returns before the PC load (`M_pop_retafter`: a 3-part `opus_dec` flag set in the guard, then `if (opus_dec) return;` before the PC load).  **39/47 on the shipped probe**, with 8 reds: rst ldm, latch ind, latch rpt and src pop x5, every one `nofire`, because the landing at the restore target is part of each row.  grid pop and tbit stay green, as expected: the word is right, only the PC is stale.  glm's "if none observes PC ... keeps all 47 green" is false.  The PC channel is the `nofire` arming of every restore row.
- **check_probe_wiring.py.**  Its domain is `git ls-files -- '*.py'`, and a tracked `.py` with no MANIFEST class is UNCLASSIFIED (red).  Committing `arm_msrmode_probe.py` plus the 23 `.py` files under `artifacts/armmsrmodekill/` needs 24 MANIFEST entries, plus one per script of mine that is preserved.  It currently reports 6 problems from other rows (5 GHOSTs, 1 expired exemption).
- **The probe moved under this pass**, from 97555f3a to edd47c92 at 03:26:42.  The edit was docstring-only and AST-identical, so the measurements stand.  I note it because the frozen-copy rule is what made that checkable.
