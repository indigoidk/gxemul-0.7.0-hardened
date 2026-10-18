## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING

An Argon reading flagged fifteen places where this file departs from its seats
(`fidelity_20261018/argon_rulA563_numbered.md`, A1-A15).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7
(`fidelity_20261018/grok_fid.txt`) then verified every flag against the seat files; where they split, the main loop
settled it by reading the cited lines.  **No grade and no row's oracle changes.**  Items 1-6 change what a builder
does; item 7 corrects attributions only.  The sentences they correct stay in place below.

1. **N5's sequence (A6; both seats CONFIRMED).**  F4 below calls "one 2-byte store then 4-byte stores step 2, 6, 10,
   14, ..., past 12, then on to 514" MEASURED.  The measured run is ONE 2-byte store, THREE 4-byte stores (occupancy 2,
   6, 10, 14 -- past 12 without touching it), then 2-byte stores to 514 (`fable5/meas_A/scratch_f4.c`, the push
   sequence before `occ =`; output `f4_run.txt`).  The continuous 4-byte stride is Astra's REASONED sequence
   (`astra/A_563/codex_adjA.txt`, F4), never run.  N5 uses the measured form, or measures the other before relying on
   it.
2. **VD1, N4's mutant (A8; both CONFIRMED).**  VD1 is `consumed = len == 4 ? 4 : 2` (`packet_A_563.md`, F15).  "VD1 is
   the downward bound move `len >= 1`" is the PACKET author's own added warrant (its "MINE" paragraph), not FB-A's
   answer.  Over the reachable widths, 1 to 8, it describes the same behaviour -- VD1 differs from HEAD's
   `len == 4 ? 4 : (len >= 2 ? 2 : 1)` (`src/devices/dev_wdc.c`) only at width 1, as FB-A's own ruling (iii) says, and
   the two forms part only at the unreachable width 0 -- but the table's mutant, and the one to code, is the ternary.
   N4's oracle (32767) is unchanged.
3. **The PRETABLE (A13, A14, A15; Grok CONFIRMED A13 and A14 and PARTLY A15; Astra REFUTED A13, PARTLY A14 and A15).**
   F25's "extended" is Astra's extension (`codex_adjA.txt`, F25 and its G0/G2 and width cells), adopted by this ruling
   over a seat split: Grok runs N1-N3 only, drops N4 as a floor row, keeps F4 -- N5's cell -- a disclose, says "No
   width-8 row is owed" (N6), and asks the PRETABLE to run VD1 and the
   `atapi_cmd_in_progress || (atapi_len != 0 && atapi_received != 0)` mutant and EXPECT THEM GREEN; Fable 5.1 specifies
   N1-N5; FB-A specifies N1-N5 with width 8 "not floor-owed".  The ruling overrides Grok on N4-N6; that dissent is
   recorded here, beside the rows it opposed.  The PRETABLE ALSO owes, from Astra: N2's "one-sided count qualification"
   (Astra's phrase, stated once and with no input or oracle -- derive it from F3's boundary-interrupt oracle, or ask
   the seat) and all width variants, measured (the width ones are carried by F24 and N6); N3's DRIVEN reachability
   sequence, measured separately from its synthesized fixture; and, from Grok, that
   `atapi_cmd_in_progress || (atapi_len != 0 && atapi_received != 0)` mutant as an expected-green control.  (Grok's
   expected-green VD1 is the overridden half: N4 detects it.)
4. **N6 carries Astra's second-pop variants (Grok's Q3).**  F24 below enumerates `len >= 2` -> `len == 2 || len == 4`
   at both endian pop sites; the N6 bullet omits it.  N6's width-8 fixture is measured against both sites' variant
   (`codex_adjA.txt`, F24 and its table rows).
5. **"Every existing row byte-identical" has named exceptions (Astra's Q3).**  N4 adds a count read to the existing
   1-byte walk, and R14/R15 change existing oracles.  And the disabled-direction partitions Astra required -- disabled
   READ and WRITE wherever existing rows do not discharge them -- are OWED: each such cell gets a row or a recorded
   discharge in the per-guard ledger (What the packet missed, item 4).
6. **G0's flag-only member (Argon's builder line; Astra and Grok agree the rows stand).**  The discriminator grades the
   flag-only candidate (e) in the ledger WITH its delta; the build list's G0/G2 rows still include it if the PRETABLE
   measures it distinguishing.  A row built for an (e) cell is L1, which this ruling chose.
7. **Attributions, records only.**  (A4, A7, A9) Fable 5.1's own ruling (`fable5/fable5_adj_A_563_v2.md`) is the seated
   vote and concurs on F4/D7, the repair-path discriminator, N5 and the case-partition reading; FB-A is credited for
   the measurement and the notes Fable read; the per-guard LEDGER form (What the packet missed, item 4) is Astra's
   alone -- no other seat proposes replacing HELD/EXHAUSTED.  (A3) "the chain does NOT close" is this file's paraphrase
   of FB-A's and Astra's conclusions that REPAIR4 as disposed was insufficient; Fable's ruling says a repair without N5
   closes half the joint.  (A11) the 262655-pair count is Grok's and the packet's; Astra's point is the lost wrapped
   dispatch.  (A12) F17 is not 3/3: Astra and Grok REFINE, and Grok CANNOT SETTLE the SUMMARY3 hunk counts and the grep
   FAIL count of 63.  (A1) Grok's "2 changed" is its own header, which names D3/F15 and F16; its body also changes F17
   (REFINE).  FB-A's "2 changed" (F4, D7) likewise sits beside an F25 strengthen that adds N5 to the PRETABLE.  (A2)
   Fable 5.1 listed five WDC addresses in four groups (0x1f0/0x170, 0x900001f0, 0x14000180, 0x14000000); "every base
   except macppc" overstated it -- it also omits hpcmips' 0x140001f0 (`src/devices/dev_pcic.c`), beside macppc's
   0xf3020000 (`src/promemul/of.c`).  (A5) Grok's disclose rested on the channel fact the measurement refuted AND on
   classifying F4 with the latches; both were its reasons.  (A10) REFUTED by both seats: FB-A's list is exactly the
   four this file quotes.
