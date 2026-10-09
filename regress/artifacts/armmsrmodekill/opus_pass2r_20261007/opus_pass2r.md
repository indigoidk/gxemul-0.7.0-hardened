OPUS_MSR_PASS2R_1007

VERDICT: SHIP-WITH-CHANGES -- the product code is still correct, but the 38-row detector scored 38/38 against 21 of the 23 fix-side mutants I built (seven DEPENDS-ON families). The repair closed pass 2's cells exactly where pass 2's mutants struck and left the symmetric cells open | 5 floor breaches (classes), all L2

## How this was measured

All measurements were taken in my own WSL clones. Nothing was written to GXEMUL-SEC, est, build, build-asan or /tmp/gxsec-build.

**Clones.** `/tmp/gxopus562r/tree` (table KTR) and `/tmp/gxopus562r2/tree` (table KTR2), both `cp -a` of my pass-2 clone.

**Baseline.** Before mutant 1 in each clone, the four SEC working-tree files (cpu_arm.c, cpu_arm_instr.c, cpu_arm_instr_dpi.c, cpu_arm.h) were copied in and `cmp`-checked against SEC. The same check ran before every mutant.

**Builds.** Each build ran `rm src/cpus/*.o gxemul`, then checked `[ gxemul -nt <each of the 4 sources> ]`.

**Probe.** A frozen copy of SEC `regress/arm_msrmode_probe.py` (md5 797b612c, 38 rows) was used throughout.

**Sentinels.** Clone-local `.MUTANT` sentinels. Both clones were restored, `cmp`-clean against SEC, rebuilt fresh, and their sentinels cleared. BASE_AFTER read 38/38 in both tables (KTR_DONE and KTR2_DONE), and no `.MUTANT` sentinel remains in either clone.

**Concurrency.** The two tables ran at the same time. Both baselines read 38/38 under that load, and both controls were killed, so the vehicle is not blind.

**Artifacts** (scratchpad `msr/opus2r/`):
- `KTR.out` and `KTR2.out` -- the results;
- `logs/` and `logs2/` -- per-mutant probe output, each ending `ARMMSRMODE_DONE`;
- `mutr.py` and `mutr2.py` -- the mutants, presence-pinned (count == 1);
- `ktr.sh` and `ktr2.sh` -- the drivers.

## Q1 -- the kill table (BUILT, 23 mutants + 2 baselines)

```
KTR   BASE              38/38
      H_proj_ff         38/38  ESCAPE   helper: switch (mode & 0xff)   [projection WIDENED]
      R_dpi_clr17       38/38  ESCAPE   DPI keep-mode: (new_cpsr & ~0x17) | cur_mode
      R_dpi_clr1e       38/38  ESCAPE   DPI  ~0x1e
      R_dpi_clr1d       38/38  ESCAPE   DPI  ~0x1d
      R_pop_clr17       38/38  ESCAPE   pop  ~0x17
      R_pop_clr14       38/38  ESCAPE   pop  ~0x14
      L_dpi_latchlabel  38/38  ESCAPE   DPI repair only if SVC || latch clear
      L_pop_latchlabel  38/38  ESCAPE   pop  same
      E_msr_notfiq      38/38  ESCAPE   msr guard && cur != FIQ   (clause (e), see below)
      N_msr_clr1e       34/38  KILLED   NEG CONTROL: msr decline mask ~0x1e
                                        (kill 14, save 2s, kill 1e, latch ind)
      BASE_AFTER        38/38
KTR2  BASE              38/38   (BASE_AFTER 38/38 at the end)
      R_pop_clr1e       38/38  ESCAPE   (a) grok
      R_pop_clr1d       38/38  ESCAPE   (a) grok
      B_pop_only14      38/38  ESCAPE   (b) grok: pop guard && (new_cpsr & 0x1f) == 0x14
      C_pop_retflag1    38/38  ESCAPE   (c) codex: if (return_flag) -> if (1)
      D_dpi_pccmp1      38/38  ESCAPE   (d) codex: if (ic->arg[2] == &r[PC]) -> if (1)
      D_dpi_snots       38/38  ESCAPE   (d) codex: restore's #ifdef A__S -> #if 1
      E_dpi_irqlatch    38/38  ESCAPE   (e) codex: repair skipped at IRQ once latched
      E_pop_irqlatch    38/38  ESCAPE   (e)
      E_dpi_irqacc      38/38  ESCAPE   (e') valid SPSR declined at IRQ while latch clear
      E_pop_irqacc      38/38  ESCAPE   (e')
      F_dpi_iclr        38/38  ESCAPE   (f) codex: decline forces I=0
      F_pop_iclr        38/38  ESCAPE   (f)
      G_dpi_nocopied    37/38  KILLED   (g) deepseek: spsr_copied gate deleted -- dbg both
                                        (got `once`: DPI announces on a planted mode)
```

**THE DENOMINATOR**, i.e. which cells were swept:

- **Helper.** Projection widened: 1 cell (0xff). The case-list, always-1 and range forms were already killed in tables 1 and 2.
- **msr_imm.**
  - Decline-mask narrowing by single bit: 0x1e built and killed. The 0x1d, 0x1b and 0x17 forms were not built; by reading, each one is killed by kill 14 or kill 1e.
  - Label conjunct: 1 cell (FIQ).
- **Restore mode-keep mask, by derivation.** Narrowing it to keep SPSR bit k gives mode = cur_mode | spsr_bit_k. Detection needs a declined SPSR with bit k = 1 at a label whose bit k = 0.
  - The rows decline only 0x14 and 0x00, so bits 0, 1 and 3 are never set in a declined SPSR. Bit 4 is set in every 32-bit mode, so a bit-4 narrowing is EQUIVALENT, not a gap.
  - So the space is 2 paths x 3 bits, and all of it escapes. Built: DPI 0x17, 0x1e, 0x1d and pop 0x17, 0x1e, 0x1d, 0x14 -- **7 of 7 escape**.
- **Label x latch x outcome.** Both paths. Built 6 cells, all escape:
  - all-non-SVC x latch-set;
  - IRQ x latch-set;
  - IRQ x accepted x latch-clear.
- **Value-restricted guard** (pop == 0x14): 1 cell, escapes.
- **Enclosing predicates** -- return_flag, the rd==PC compare, and the A__S restore: 3 cells, all escape.
- **I/F provenance in the decline:** 2 cells, both escape.
- **spsr_copied gate:** 1 cell, killed.

**Smallest edit (Q1's literal question): one token -- `ARM_FLAG_MODE` -> `0xff` in `arm_mode_is_modelled()` (H_proj_ff), 38/38.**

It is also the most serious escape. With that edit, every MSR CPSR_c that changes mode with I or F set is DECLINED and stays in the current mode. That includes `msr cpsr_c, #0xd2` (IRQ, interrupts masked), the standard kernel stack-setup idiom. The same happens to every SPSR restore whose SPSR has I or F set.

No row drives a helper input with bits 7:5 set. Every c_XX immediate has I=F=T=0, every `MSR SPSR_c` writes 0x14 or 0x1f, and `sf_c0` touches only the flags byte. The contract claims only that a DROPPED projection is caught, and the N|Z rows do catch that. A WIDENED projection is a different edit, and it is invisible.

The runner-up is also one token: `~ARM_FLAG_MODE` -> `~0x17` (or `~0x1e`, `~0x1d`) in either restore's keep-mode expression. This is exactly pass 2's F2 (`O_mask_nibble`), moved from msr_imm to the two restores. The repair added kill 03 at msr_imm only.

### Grading

| class | mutants | why it is floor |
|---|---|---|
| **1. Helper projection width** | H_proj_ff | Clause (d): it weakens the `& ARM_FLAG_MODE` predicate the fix ADDED. **L2.** |
| **2. Restore keep-mode mask width** | R_* x7 | Clause (d) on the added repair expression. It is the same class as pass-2 F2. Two consecutive passes, one class, so the next repair owes the **CLASS CLOSURE**. **L2.** |
| **3. Label x latch x outcome** | L_*, E_*_irqlatch, E_*_irqacc | The repair path READS the latch, and the label selects new_cpsr. By the pass-11 floor ({label} x the device-state lvalues the repair path reads, jointly reachable), these are floor cells. Pass 2 asked for "repair only while latch clear" and it was closed at SVC only, so this is the second pass on one class -> **CLASS CLOSURE. L2.** |
| **4. I/F provenance** | F_dpi_iclr, F_pop_iclr | The contract CLAIMS "the restore not taking N/Z/I/F from the SPSR (src * rows read the whole CPSR word)". Every declined SPSR has I=F=0, so forcing I to 0 is invisible. A breach of the stated contract: **L2/L4**. |
| **5. Enclosing predicates** | C_pop_retflag1, D_dpi_pccmp1, D_dpi_snots | `return_flag` and `ic->arg[2]==&r[PC]` dominate the edited lines inside the enclosing function, so they fall under DEPENDS-ON clause (1). **L2 by the letter.** D_dpi_snots is a compile-time selector, not a runtime predicate. I grade it with this class because it decides whether the edited block runs at all. |
| (e) disclosable | B_pop_only14 | 0x14 versus other unmodelled values is a value the body never tests as a case (the helper's `default`). The class-2 closure row kills it for free. |
| (e) disclosable | E_msr_notfiq | msr_imm's body tests no current-mode label, only USR, and `usr mask` rows that (my pass-2 ruling stands). It is NOT in the NOT CLAIMED list; add it. |

## Cheapest closing rows -- as CLASS CLOSURES, one diff

### Closure A: the value-and-bit class (classes 1, 2 and 4, plus B_pop_only14)

Change the ten existing `src {dpi,pop} x {fiq irq abt und svc}` sessions. Add no new sessions.

**1. Enter each label with I and F set.** Use `msr cpsr_c, #0xd1/#0xd2/#0xd7/#0xdb/#0xd3` (new WORDS `c_d1` etc.) instead of `c_11`...
- This kills **H_proj_ff's msr half**: the entry would be declined.

**2. Decline value: SPSR := N|Z|I|F|0x0f.** Use `msr spsr_c, #0xcf` after `sf_c0`. Want `c00000c0|cur`.
- 0x0f sets SPSR mode bits 0 to 3.
- Every detectable (bit, label) cell is then hit: bit0 at IRQ, bit1 at FIQ, bit2 at FIQ/IRQ/SVC/UND, and bit3 at every label except UND.
- That covers all 3 x 2 restore-mask cells (and kills every R_*).
- The I=F=1 value kills **F_*_iclr**.
- A value other than 0x14 kills **B_pop_only14**.

**3. Accept value: SPSR := N|Z|I|F|0x1f** (`msr spsr_c, #0xdf`). Want `c00000df`.
- This kills **H_proj_ff's restore half**.

**4. Keep 0x14 and 0x00 covered** at SVC by the existing `rst *` and `zero spsr` rows.

**Enumeration to write into the CONTRACT:**
- Restore keep-mode bits {0,1,2,3} x labels: every detectable cell is rowed.
- Bit 4 is EQUIVALENT: all modelled modes have it set.
- Helper input bits 7:5 are rowed set and clear (the c_XX rows carry them clear).
- Higher bits are rowed by N|Z.

### Closure B: the label x latch x outcome class (class 3)

The space per path: 5 labels x {latch clear, set} x {declined, accepted} = 20 cells, 40 in total.

Today **24/40** cells are rowed:
- declined/clear: 10;
- accepted/set: 10;
- declined/set: SVC only (2);
- accepted/clear: SVC only (2).

To close all 40, extend each `src` session to FOUR restores in one process, with the announce count still == 1 and each step read back:

1. ACCEPT (0xdf, latch clear)
2. DECLINE (0xcf: latch clear -> set)
3. DECLINE again (latch set)
4. ACCEPT (latch set)

That adds two restores per session and no new sessions. It kills L_*, E_*_irqlatch and E_*_irqacc.

**Merge it with closure A** (same sessions, same values): **10 sessions, 4 readbacks each**.

### Closure C: the enclosing predicates (class 5), one new session

In SVC with `spsr_svc` = 0x1f, chain three steps, each followed by `mrs` + `str` (want m=13 every time):

1. `ldmia r5, {pc}` (0xE8958000: plain LDM, no ^). Kills C_pop_retflag1.
2. `add pc, r6, #0` (0xE286F000: a non-S DPI to PC that is not the `mov pc,lr`->`ret` shortcut). Kills D_dpi_snots.
3. `add r0, pc, #0` (0xE28F0000: Rn=PC, Rd!=PC), then store r0. Want CODE-relative pc+8. Kills D_dpi_pccmp1 (the mutant jumps).

**Row count** grows by 1 (or by 3 if each control gets its own row). Re-run all 23 mutants here plus the table-2/3 set.

## Q2 -- the label clause

The rowed product {5 labels} x {declined, accepted} x {dpi, pop} is **NOT the closure**. It is missing two axes.

1. **The latch state the repair path reads.** Measured: 6 of 6 escape. Codex's 40-cell count is right, and my Closure B rows it all.
2. **The bit content of the declined SPSR.** The keep-mode repair MASKS the SPSR's mode bits. By the 2026-09-25 pin ("TESTS means masks or compares as a case"), every masked bit is part of the generating set at each floor cell. The rows drive bits 0, 1 and 3 clear only.

**The zero-SPSR cell at SVC/DPI only is NOT a missing axis.** 0x00 and 0x14 sit in the same helper partition, and 0x00 adds no set bit over 0x14. Disclose it per path, as codex says. It is value debt, not floor.

## Q3 -- records

1. **Load backstop comment (cpu_arm.c) -- FALSE about its triggers.**
   - The comment says Load's default is reached "by any later mode switch (guest MSR, S-to-PC return, exception or IRQ) that leaves it in place".
   - In fact a guest MSR to a modelled mode, and exception or IRQ entry, call Load on a MODELLED mode. `arm_exception` ORs the table mode in before Load.
   - The only route to Load's default is a DPI S-to-PC executed while the planted mode is current: no SPSR is copied (`spsr_copied` = 0), so CPSR keeps the plant and Load runs on it.
   - L4; reword to name that one carrier. (Codex reached the same reading.)
2. **Save backstop comment: "ANY later mode switch gets here" -- an overclaim.**
   - An `LDM {..pc}^` from a planted mode stops the CPU at arm_pop's selector `default:` (`bdt_load: unimplemented mode`, running=0) BEFORE Save.
   - Add "except the LDM^ return, which stops the CPU (pre-existing)".
3. **CONTRACT "restore not taking N/Z/I/F from the SPSR"** -- the I/F part is refuted by F_*_iclr. Narrow it, or land Closure A.
4. **CONTRACT "dropping its `& ARM_FLAG_MODE` projection"** -- true as written, but it omits WIDENING, which escapes (H_proj_ff). Land Closure A, or add it to NOT CLAIMED.
5. **NOT CLAIMED "0x01-0x0f escapes"** -- 0x03 is now driven, so a helper wrong at 0x03 is killed by kill 03. Write 0x01-0x02 and 0x04-0x0f. (Codex's point; verified against the row.)
6. **Probe comment "`dbg both` ... the only carrier of Load's backstop, and of their distinct latch bits"** -- stale: `latch rpt` also carries both.
7. **"Table 3: Zero escapes on the final probe"** -- true of the mutants measured, but not a closure claim. 21 measured escapes now exist against that same 38-row probe.
8. **DPI comment "T is forced after Load for an odd destination PC" -- TRUE by reading.** On the A__S path, `arm_load_register_bank` runs, then control falls to `quick_pc_to_pointers` and `if (cpu->pc & 1) cpsr |= ARM_FLAG_T` (cpu_arm_instr_dpi.c, after the `#endif`). It is unrowed and disclosed, which is correct.
9. **The tallies HOLD.** fixed 38/38, HEAD 16/38 and 22 reds are consistent with my BASE runs. The negative controls behaved: N_msr_clr1e and G_dpi_nocopied were both killed.

## Q4 -- is NOT CLAIMED honest?

**No: it is honest about what it lists, but it omits five measured escape classes, and one of them hides a guest-visible regression class on testarm.**

**H_proj_ff.** The FIX itself is correct: it declines nothing valid, which I verified by reading the helper. But the detector cannot see a one-token edit that would make every interrupt-masked mode switch a silent no-op on the mode field. The round claims "declines ONLY unmodelled modes", and the I/F-carrying half of the accept side is unrowed.

**The other four classes** do not hide a host kill:
- Classes 2 and 3 land on the BACKSTOP or keep a wrong mode. That gives UNPREDICTABLE guest state plus an announce, not process death.
- Classes 4 and 5 give wrong-but-alive guest state.

**Also missing from NOT CLAIMED:** the msr_imm label conjunct (E_msr_notfiq), and the per-path value coverage (0x15/0x1e through MSR only; 0x00 through DPI/SVC only).

## Something else

- **The pattern is `#499`'s, measured again.** Pass 2 found three classes (latch, MSR mask, label). The repair closed each one only where its mutant struck: the latch at SVC, the mask at msr_imm, and the label at latch-clear/declined-first. Two passes on the same classes means the CHAIN rule's amendment applies now: enumerate the space from the function's own inputs (labels x latch x outcome x masked bits) and close it in one diff, as above. Another cell-by-cell repair will produce a pass 3 breach.
- **Cost estimate.**
  - Closures A and B modify the existing 10 sessions: 2 extra restores and 2 new WORDS each.
  - Closure C adds 1 session.
  - The probe's runtime grows by roughly 10%.
  - The re-table needs all 23 of these mutants, plus the 36 from tables 2/3, plus BASE before and after.
