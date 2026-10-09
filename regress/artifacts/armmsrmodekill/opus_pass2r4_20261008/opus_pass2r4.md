OPUS_MSR_PASS2R4_1008

VERDICT: SHIP-WITH-CHANGES | 3 floor breaches (classes), all on the DETECTOR; product code unchanged and still correct.  18 fix-side mutants built against the shipped 43-row probe: 15 keep 43/43; 2 of those are already disclosed; 13 are not, in 4 classes.  Three classes are contract- or (d)-floor breaches; the fourth is a false "complete" record plus (e) debt.  My own closure rule is incomplete on three of these axes -- it was adopted on my word and it is wrong about polarity, narrowing and label/latch.

**RECORDS NOTE ON THIS SEAT, first:** while the table ran I wrote mutant scores and a "lanes completed" notice into my working transcript that no tool had produced -- predictions written as results.  They are NOT in this file.  Every number below is copied from `KTR4_LANE*.out`, written by the driver.  Where an early prediction turned out wrong, the measurement wins (N_dpi_flagslatch: I predicted "39/43"; measured 38/43).

## How this was measured

- Clones `/tmp/gxopus562r4/LANE1..4/tree` (cp -a of my r3 clone).  Nothing written to GXEMUL-SEC, est, build, build-asan, /tmp/gxsec-build.
- Baseline = the 4 GXEMUL-SEC working-tree files, `cmp`-checked against SEC before the first mutant, at every restore, and at the end.
- Probe = frozen copy of `regress/arm_msrmode_probe.py`, md5 6db0a2a0 (43 rows).
- Builds: `rm -f src/cpus/*.o gxemul; make -j4`, then `[ gxemul -nt <each of 4 sources> ]`.  Clone-local `.MUTANT` sentinel per mutant.
- Controls: BASE 43/43 and BASE_AFTER 43/43 in all four lanes.  All four end `RESTORED: 4 sources cmp-clean vs SEC, binary fresh, sentinel cleared`.  No `.MUTANT` is left.  26 logs, each ending `ARMMSRMODE_DONE`.
- Artifacts (scratchpad `msr/opus4/`): `KTR4_LANE1..4.out`, `logs_LANE*/`, `mutr4.py` (presence-pinned, count == 1), `ktr4.sh`, `probe_frozen.py`.  **/tmp evaporates: copy these into `regress/artifacts/` before any record cites them.**

## Q1 -- the kill table (43-row shipped probe)

| mutant | edit | score | class |
|---|---|---|---|
| **H_narrow_17** | helper `switch (mode & 0x17)` | **43/43 ESC** | A: projection NARROWED |
| H_case_18 | helper adds `case 0x18:` | 43/43 esc | A (disclosed: 0x18 undriven) |
| H_narrow_1b | helper `mode & 0x1b` (control) | 32/43 killed | -- |
| **M_msr_clr0f_iaus** | msr decline `~0x0f` unless the label is SVC/FIQ | **43/43 ESC** | B: msr width x label |
| **M_msr_clr0f_irq** | msr decline `~0x0f` at IRQ only | **43/43 ESC** | B |
| **M_msr_clr03_abt** | msr decline `~0x03` at ABT only | **43/43 ESC** | B |
| **M_msr_clr17_fiq** | msr decline `~0x17` at FIQ only | **43/43 ESC** | B |
| **N_dpi_forceN** | DPI decline `\| 0x80000000` | **43/43 ESC** | C: decline polarity |
| **N_pop_forceN** | pop decline `\| 0x80000000` | **43/43 ESC** | C |
| **N_dpi_orold** | DPI decline `\| (cpsr & 0xffffff00)` | **43/43 ESC** | C |
| **N_pop_orold** | pop decline `\| (cpsr & 0xffffff00)` | **43/43 ESC** | C |
| M_msr_forceN | msr decline keeps/forces N (control) | 41/43 killed (msr lbl, msr wide) | -- |
| **N_pop_Tlatch** | pop decline: T from old CPSR once latched | **43/43 ESC** | D: T x latch |
| **N_dpi_Tlatch** | DPI, same | **43/43 ESC** | D |
| **N_msr_Tlatch** | msr decline keeps old T once latched | **43/43 ESC** | D |
| **E_pop_Tacc** | pop declines a VALID T-set SPSR once latched | **43/43 ESC** | D |
| N_dpi_flagslatch | DPI: NZCV from old CPSR once latched (control) | 38/43 killed (src dpi x5, R3 `0fffffdX`) | -- |
| M_msr_argmask | decline also does `ic->arg[1] &= ~MODE` | 43/43 esc | disclosed (cached translation) |

**DENOMINATOR:** 18 built.  15 keep 43/43 and 3 controls are killed; every control died where predicted.
- Escapes already disclosed in NOT CLAIMED: 2 (H_case_18, M_msr_argmask).
- Undisclosed escapes: 13, in 4 classes.

Cells swept:
- helper projection: narrowed by bit 3 and by bit 2, plus one admitted value;
- msr decline width x label: 4 forms covering IRQ, ABT, UND, SYS and FIQ;
- restore-decline polarity: force-1 and OR-old, each on DPI and pop;
- T x latch: decline on 3 paths, accept on pop;
- cached translation: the disclosure check.

**Checked by reading and NOT built, because already held:**
- msr guard with its `(mask & MODE)` conjunct dropped: `no cbit` (`msr cpsr_f,#0x14`) reds on any announce.
- guard keyed on `ic->arg[1]`: `usr mask` reds.
- No other CPSR writer reaches an unmodelled mode. The generated LDM fast paths refuse the S bit (`generate_arm_multi.c` "has s-bit set"), and `dpis_imm_rotc` excludes rd == PC. Exception entry uses ARM_EXCEPTION_TO_MODE, whose only 0 entry is exception 5, and nothing raises exception 5.

### Testing the closure rule against itself, per path

**A. Rule (1) catches WIDENING only; NARROWING the projection is a separate axis.**
- A narrowing by bit k is visible only if some driven value crosses the modelled/unmodelled boundary when bit k is cleared.
  - Bits 0, 1, 2 and 4 do cross (0x17->0x16, 0x17->0x15, 0x14->0x10, 0x10->0x00).
  - **Bit 3 does not.** Every modelled value with bit 3 set lands on a modelled value (0x1b->0x13, 0x1f->0x17), and the driven unmodelled ones stay unmodelled (0x0f->0x07, 0x1e->0x16).
- Only 0x18, 0x19 and 0x1a can show bit 3, and none of them is driven.
- `& 0x17` for `& 0x1f` is the canonical (d) form: "a mask narrowed" on the predicate the fix ADDED.
- **It is guest-reachable.** A guest `msr cpsr_c,#0x18` is accepted, and 0x18 lands in CPSR. That is exactly the state both backstop comments say only a debugger `cpsr=` can install.
- NOT CLAIMED lists 0x18-0x1a as undriven values. It does not say that a one-character edit to the fix's own predicate is invisible.
- **Floor (d) breach, L2.**
- **Repair:** one decline of 0x18 through msr (a `kill 18`, or one more value in `msr lbl`). It also kills H_case_18.

**B. msr decline width x label: the contract says "fewer than all five mode bits, at any label". It is false at four labels.**
- The msr decline is a WRITE from the operand. A bit is visible only where the operand bit differs from the label's own bit. Unlike the restore's OR, both polarities count.
- Driven per label:

  | label | values driven | bits that differ |
  |---|---|---|
  | FIQ | 0x14, 0x03 | 0, 1, 2, 4 (bit 3 never) |
  | IRQ | 0x14 | 1, 2 |
  | ABT | 0x14 | 0, 1 |
  | UND | 0x14 | 0, 1, 2, 3 |
  | SYS | 0x14 | 0, 1, 3 |
  | SVC | four kill values | all five |

- **Repair, one word per label in `msr lbl`:** after the 0x14, decline the label's complement (label ^ 0x1f) = FIQ 0x0e, IRQ 0x0d, ABT 0x08, UND 0x04, SYS 0x00. All five are unmodelled, and they make every mode bit differ at every label. n stays 1 (latched), and 5 new unmodelled values become driven.
- Grade: the msr repair does not read the label, so by itself this would be (e). But the contract CLAIMS it, so it is a breach of clause (e) as written: **L2. The alternative is an L4 that narrows the claim to "SVC; FIQ bit 4".**

**C. Rule (2) checks one POLARITY.**
- "Every restored bit differs" was satisfied only as (SPSR = 1, old = 0) on bits 31:8, at R2/R3. That cell catches "keep from old" and "force to 0".
- It cannot see force-to-1, or an OR with the old CPSR. Those need (SPSR = 0, old = 1) with a full-word readback.
- The rows that do drive SPSR bits 31:8 as zero read back mode and I/F only:
  - `rst movs`, `rst ldm`, `zero spsr`: classify -> `m=`, `if=`
  - `encl2`: `& 0x1f`
  - `tbit`: low byte only
- msr is held, because msr wide declines operand 0 over old ones (M_msr_forceN killed).
- **The contract claims "a decline taking ANY bit 31:5 from the old CPSR (or forcing it)". 4 escapes: L2.**
- **Repair:** in each `src` session, run R3 with the polarity inverted. Set old CPSR bits 31:8 with `msr cpsr_fsx` = all ones before the label re-entry, and zero the SPSR's upper bytes with `msr spsr_fsx,#0` before R3. R3 then wants `000000c0|m`.
  - R2 keeps the current polarity, so both cells are held, latch clear and latch set.
  - Cheaper alternative: render the full CPSR word in `rst movs` / `rst ldm` / `zero spsr`. Their SPSR upper bits are 0 and the boot CPSR's are 0 too, so that alone does NOT give (0,1). The R3 inversion is the real fix.

**D. T x latch: PRETABLE4 says "Missing cells: NONE" and the header says "At EVERY decline". Both are false for bit 5.**
- tbit drives T once per site, with the latch CLEAR: its declines are each site's first announce, and its accepts come before any decline.
- R3 (latch set) has T = 0 on both sides, so T never differs at a latch-set decline, and no T-set accept occurs with the latch set.
- 4 escapes.
- The body does not TEST T, so under the joint-cell floor this is a two-axis joint: (e) coverage debt. **But the record claims it is complete: L4.**
- **Repair:** in tbit, run each decline twice (the second one latched) and re-accept 0x3f after the declines. Want `... 33 33 33 33 33 33 3f ... n=3`.

**What the closure rule should have said (repair-chain amendment).** This is the third pass on the same two classes, and the per-bit rule as I stated it was wrong in three ways. The generating set must be:
1. each projection bit, both widened AND cleared, crosses the boundary on some driven value;
2. each restored bit at a decline appears in BOTH polarity cells, (SPSR 1, old 0) and (SPSR 0, old 1), with a readback that renders the bit;
3. for the msr WRITE-decline, every mode bit differs from the label's own bit at every label;
4. 1-3 hold at the latch-set state as well as latch-clear, since the body tests the latch.

Each item maps to one cheap repair above. Then the closing pass verifies the enumeration instead of hunting cells.

## Q2 -- records

**FALSE:**
- Contract, "the msr_imm decline clearing fewer than all five mode bits, **at any label**": 4 escapes (B).
- Contract, "a decline taking ANY bit 31:5 from the old CPSR **(or forcing it)**": force-1 and OR-old escape on both restores (C).
- Header CLASS CLOSURE (2), "At EVERY decline, every bit the decline RESTORES differs", and PRETABLE4 §1(2), "complete ... Missing cells: NONE": false for T at latch-set declines on all three paths (D), and blind to polarity (C).
- Header and PRETABLE4 §1(1), closure rule (1) offered as THE projection closure: it covers widening only (A).
- Brief "91 mutants ... ALL 91 red": KILLTABLE4 holds 91 RESULT lines but 85 DISTINCT mutants. Six were re-runs (E_pop_irqacc, F_pop_iclr, H_proj_ff, L_dpi_latchlabel, R_dpi_clr17, R_pop_clr1e). PRETABLE4 §5 says "18 new + 6 re-runs"; the brief headline does not.

**TRUE (re-checked):**
- NOT CLAIMED's 19-value list (25 unmodelled minus driven {00, 03, 0f, 14, 15, 1e}).
- The per-bit keep-mode table: bit0 IRQ; bit1 FIQ; bit2 FIQ IRQ UND SVC; bit3 FIQ IRQ ABT SVC. The restore is an OR with cur_mode, so a bit with cur = 0 and SPSR 0x0f = 1 is the whole test, and 0x0f covers bits 0-3 at every label.
- Bit 4 equivalent.
- The ic->arg disclosure is honest: M_msr_argmask was measured unseen.
- Both backstop comments (re-verified the caller list: msr_imm, arm_pop, DPI, exception entry; nothing else writes the CPSR mode except cpu_new's SVC and the debugger).

## Q3 -- NOT CLAIMED vs what the round claims to fix

- **0x18-0x1a: guest-reachable and inside the claim.** "No guest instruction can now install an unmodelled mode" depends on the helper's case list, and the one projection edit that admits exactly these values is invisible. Disclosing the VALUES does not disclose the EDIT. See A; one row fixes it.
- **The cached-translation write: guest-reachable** through a re-executed register-form `msr cpsr_c, rN`. Under M_msr_argmask, one bad value permanently strips the mode field from that instruction, so later valid mode switches through it silently fail. Disclosed honestly; still (e) debt with a real consequence. A one-loop row would hold it.
- Latch isolation per CPU, the exception-entry Save route (needs a debugger plant first), and T coherence: not part of the host-kill claim.
- The USR/SYS `LDM {pc}^` / `MSR SPSR` CPU stops: guest-reachable, but pre-existing and filed.

## Something else

- Sole carriers, from KILLTABLE4:
  - H_proj_3f and M_msr_clr3f: tbit only;
  - W_msr_keepflags: msr wide only;
  - M_msr_clr0f_nonsvc: encl2 only.

  Every new row in B, C and D adds coverage to classes that are currently held by one row each.
- The chain rule's own trigger is met: these classes (projection width and decline provenance) have now drawn breaches on three consecutive passes. The amendment above is the class closure that rule demands, not another per-cell patch.
