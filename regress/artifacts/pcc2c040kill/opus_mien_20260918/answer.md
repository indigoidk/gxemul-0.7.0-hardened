OPUS_SEAT_ALIVE_20260918_PCC2K

VERDICT: REAL-AND-RIGHTLY-FIXED. The emulator fix is correct. agy's prediction is MEASURED TRUE: an announce gated on !MIEN scores 16/16 on the shipped detector. That is a hole in the detector, not in the fix. A one-row repair using no new session kills it (16/17).

## Q1: premises

**P1: CONFIRMED.** The GENCTL byte arm stores `idata` unmasked and calls `reassert_interrupts(d)` in the same access (`dev_pcc2.c`, `case PCCTWO_GENCTL:`). The pre-fix C040 test ran first in that helper. So one `st.b` of 0x04 killed the host, and HEAD's `witness_HEAD_20260907.raw` shows it. C040 is a documented GENCTL bit. The VMESBCP2 section "Interrupt Prioritizer (MVME187)" (`_scratchpad/vmesbcp2.txt` ~:4545-4560) describes what it does on an MC88100 board. Writing it is legal.

**P2: CONFIRMED, and the manual makes the case stronger than the brief does.** That VMESBCP2 section says that with C040 set, the chip drives its level onto EIPL<2..0>* "assumed to be provided in the M68000-family MPU". With C040 clear, the INT pin is "connected to the INT pin on the MC88100" (:4370-4374 agrees). On an MVME187 the 88100 is wired to INT. So with C040 set, **the 88100's INT line really is not driven.** Leaving the CPU line deasserted is therefore close to the real board-level behaviour, not just a stand-in for a missing feature. "Implement EIPL delivery" is not a real option on this machine, because there is no 68040 to deliver to. Declining the write would be wrong: GENCTL has to read back what the guest wrote, and `c040 genctl` pins 0x06. So among accept / decline / decline-plus-latched-announce / implement, the right choice is ACCEPT THE WRITE + SUPPRESS ASSERTION, with a latched announce. The shipped code does exactly that. It also keeps the IPL recalculation, which matches "IPL2-IPL0 always reflect the encoded request level".

**P3: CONFIRMED for the function.** `reassert_interrupts()` no longer contains any `exit`. The only exit left in the file is `pcctwo_interrupt_common`'s `default: exit(1)`. It is keyed on `interrupt->line`, which is a constant fixed at wiring time and not a guest-controlled value. clmpcc does CONNECT lines 0xc (SCC_RXE) and 0xd (SCC_M), and neither has a case in that switch. But `grep` finds no `INTERRUPT_ASSERT` on `irq_scc_rxe` or `irq_scc_m` in `dev_clmpcc.c`. So this is a latent trap for whoever later adds that assert, and not a live kill. It is worth one filed line.

## Q2: severity and option choice

Before the fix, one legal guest byte store with no driver precondition terminated the host. That belongs at the top of the queue, alongside the other guest-drivable host kills (the `#501`/`#119` class in this same file). The option chosen is right, for the reasons under P2.

## Q3: what the shipped fix and detector still get wrong

1. **MEASURED: the announce is unpinned in the MIEN|C040 cell, which is the cell a driver actually uses.** I built mutants in a scratch clone (`/tmp/gxopus_pcc2k`, a `cp -a` of `build/`). Each build restored `dev_pcc2.c` from SEC, rebuilt, and checked `[ binary -nt source ]` (OK every time). SEC's working tree differs from HEAD by a comment-only hunk, so the code is the same. The probe was a frozen copy of the shipped one.

   | build | shipped 16-row probe | repaired probe (+1 row) |
   |---|---|---|
   | BASE | 16/16 | 17/17 (run twice) |
   | `M_announce_notmien`: latch test gets `!(GENCTL & MIEN) &&` | **16/16, a total escape** | **16/17**, `c040 says mien` red |
   | `M_announce_onlyifsuppressing`: latch test gets `assert &&` | 13/16 (`says`, `once`, `predirty` red) | not run |

   Why it escapes: `says`, `once` and `predirty` all write 0x04 with MIEN clear. The assert-row sessions write 0x06, but no row reads the announce in their transcripts. The fix's own comment calls MIEN and C040 "siblings gating one output", and the function tests both bits. So under the joint-cell rule, (C040 × MIEN) × announce is inside the enumeration, and one of its cells has no row. I'd grade it as an **in-rule cell of the shipped detector's floor (L2), cheap to close.** The repair is one row reusing the `td` transcript from the existing `c040 noassert` session:
   `row("c040 says mien", "yes" if SAYS in td else "no", "yes", ...)` inserted before `c040 genctl`. It adds no session and has been measured in both directions (table above).

   The second mutant is a side result. The detector requires the announce to fire at *write* time, even when nothing is pending. So it pins a specific design (announce on C040 entry), not just "announce when a delivery is actually suppressed". That design is fine, but it should be stated in the probe's contract.

2. **Minor wrong text in product code:** "assertion suppressed" prints on every first C040 write, including when MIEN is clear or nothing is pending, so nothing was suppressed. Also, per P2, "not implemented" is only half true: on MVME187 the INT line really is idle with C040 set. Suggested wording: "C040: interrupts routed to EIPL pins (no 68040 on this board); CPU INT not asserted (once)". This is an L4-grade records item and can be filed.

3. **Not measured by me, but I checked them in the source and they are plausible (agy):**
   - `M_warnassign` (`=` instead of `|=`) wipes the other latch bits. No row checks that earlier warn bits survive a C040 announce.
   - `assert_row()` never sets `r3`, so `I_ST_SCR` stores to address 0. This is harmless to the verdicts because the completion breakpoint is what decides the rows.
   - The probe header still says the detector "does NOT catch" the non-suppressing mutant. That is stale, because the L2 rows below it do catch it.

4. **The comment in `dev_pcc2.c` is uncommitted.** The working tree has an uncommitted 20-line hunk: the 2026-09-17 correction of the `return`-mutant sentence. The brief inlined that working-tree text as "AT HEAD". It is a comment only, but HEAD still carries the false sentence until it is committed.

Artifacts are all in this scratchpad directory, and every log ends in `PCC2C040_DONE`:
- the runs through the shipped probe: `BASE.raw`, `M_announce_notmien.raw`, `M_announce_onlyifsuppressing.raw`
- the runs through the repaired probe: `rep_BASE.raw`, `rep_M_announce_notmien.raw`
- the probe copies: `probe.frozen.py`, `probe.repaired.py`
- the scripts: `mutate.py`, `run.sh`, `run2.sh`
- the logs: `run.out`, `run2.out`

The clone's `.MUTANT` sentinel was cleared only after `cmp` against SEC came back clean and the binary was newer than the source. GXEMUL-SEC and `build/` were not written. /tmp is volatile, so copy these into `regress/artifacts/` before any record cites them.
