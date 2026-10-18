**Your token: `ASTRA_FIDCONF_20261018`** -- open your answer with it.

# The rulings A/B fidelity corrections -- the confirm: the FINAL blocks, after the shared-findings pass

## 0. What this is

The shared-findings pass (`packet_fidf2_*.md` beside this file; answers `codex_fidf2.txt`, `grok_fidf2.txt`,
`glm_fidf2.txt`, and Argon's in `_scratchpad/gweb/jobs_20261018_argonpack15/fidf2/gemini_web.out`) raised flags against
the two FIDELITY CORRECTIONS blocks.  Every one was settled -- applied, or refuted from a file -- and the blocks were
rebuilt.  This pass CONFIRMS the final text only.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the blocks are
NOT yet in its files.  READ-ONLY: write nothing to any project tree.

## 1. What changed since the shared-findings packet, and why

- **From your own flags (codex_fidf2.txt):** A3 -- "the chain does NOT close" is now this file's paraphrase of FB-A's
  and Astra's conclusions; A13 -- the PRETABLE extension is Astra's, adopted over a seat split; A7 -- "five WDC addresses
  in four groups"; B2 -- the five removals are equivalent for every in-tree use and `SYSASIC_EVENT_TO_ADDR(e) * 2` is the
  use that WOULD see them; B3 -- VOID comes from the capability preflight only, and a candidate's own compile/link
  failure and its post-link sanitizer abort both stay row FAILs.
- **From Argon (pack 15):** block A item 3 also owes "all width variants"; item 7 credits the per-guard ledger form to
  Astra alone (no other seat proposed it -- checked by grep in all four A answers).
- **From GLM (glm_fidf2.txt):** item 2 cites FB-A's ruling (iii) for "differs only at width 1"; item 5 states the
  disabled-direction cells as OWED, not as already carried; item 7's A1 adds FB-A's F25 strengthen; B3 "Record 1 must
  name"; B6 gives the deepseek file's line facts (its second line quotes "VERDICT: BUILT", its fourth is its own
  "VERDICT: BREACH").
- **From Grok (grok_fidf2.txt):** A1 -- Grok's header names D3/F15 and F16, its body adds F17; item 3 -- Grok's positions
  per row and the expected-green mutant written as `atapi_cmd_in_progress || (atapi_len != 0 && atapi_received != 0)`;
  item 3 -- "N2's one-sided count qualification" is flagged as stated once with no input or oracle; item 2 -- HEAD's
  `len == 4 ? 4 : (len >= 2 ? 2 : 1)` (src/devices/dev_wdc.c) named, and the two VD1 forms part only at width 0.
- Both blocks were reflowed to 120 columns; every word was proved unchanged by the reflow.

## 2. Block A, final
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

## 3. Block B, final

## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING

An Argon reading flagged twelve places where this file departs from its seats
(`fidelity_20261018/argon_rulBasic_numbered.md`, B1-B12).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7
(`fidelity_20261018/grok_fid.txt`) then verified every flag against the seat files; where they split, the main loop
settled it by reading the cited lines.  **No pin, sample or grade changes.**  Items 1-5 change or make explicit what a
builder does; items 6-8 correct the record.  The sentences they correct stay in place below.

1. **Record 3 and the cases-file comment (B1; Grok CONFIRMED, Astra REFUTED -- clarified, not reversed).**  LEAVE the
   cases-file comment ("a stub that drifted from these two lines reds the committed header ...") UNCHANGED: pin C makes
   it true.  Rewrite only the packet's record 3, to describe the pinned behaviour (`fable5/fable5_adj_B_asic.md`, F3,
   and its §7).  F3 below says the same thing in a sentence that can be read as editing the comment.
2. **The contract lines Fable §7 requires (B11, B12; Grok CONFIRMED, Astra REFUTED as incorporated by reference).**
   "Fable §7 as the delta" below includes them; stated here so the build list carries them.  DISCLOSES gains the five
   EQUIVALENT removals (`nooutparen` x3, `nocondparen`, `nocast`) -- equivalent for every in-tree use -- naming
   `SYSASIC_EVENT_TO_ADDR(e) * 2` as the use that WOULD see them, and LeakSanitizer (on by default under
   `-fsanitize=address`); the gate comment gains the VOID sentence.
3. **Link versus run (B10; Grok CONFIRMED, Astra PARTLY; wording corrected on the shared-findings pass).**  VOID comes
   from the capability PREFLIGHT only -- a trivial program compiled, linked and run under `-fsanitize=address` -- so a
   toolchain that cannot compile, link or start an instrumented binary (Grok's missing-`libasan` case) is VOID with its
   reason, never a red header row.  Inside `id_verdict` a candidate's OWN compile or link failure (`rc`) stays a row
   FAIL -- the missing-field `struct cpu` case is RED BY DESIGN -- and so does a sanitizer abort after a successful
   link (`run_rc`), the extent red's channel, which Record 1 must name (`grok/B_asic/grok_adjB.txt`, F14 and D1; the
   instrument:  `fable5/meas_B/variants/pinned_preflight/sysasic_range_check.py`).
4. **The frozen PRETABLE keeps an erratum beside it (Astra's Q3).**  The three PRETABLE/SUMMARY corrections (What the
   packet missed, item 3) go into the NEW build's records.  The preserved PRETABLE is not rewritten -- its mtime is the
   order proof -- and gets an erratum file beside it (`prescreen/prescreen_asic.md`: "record the erratum beside it
   rather than edit it").
5. **Larger-buffer scope (Astra's Q3).**  F7's `buf[9]`, `buf[16]` and `buf[64]` are green under the shipped stub
   (Grok); only `buf[16]` was measured under both extent pins, `sizeof` and AddressSanitizer (Fable's `cand_buf16`).
   The disclosure claims no more than that.
6. **F15 was overturned 1 of 3 (B5, B6; Grok CONFIRMED both, Astra CONFIRMED B5 and PARTLY B6).**  Astra overturned;
   Grok and Fable 5.1 UPHELD the packet's F15, both holding that F1 and F2 refute the panel's CLEAN.  The overturn
   stands ON THE FILE, not the count: `finalpass_20261013/panel_20261013_234442/ollama_deepseek.txt` quotes the
   builder's summary ("VERDICT: BUILT", its second line) and then gives its own "VERDICT: BREACH" on the short buffer
   (its fourth line; read 2026-10-18).  The two upholds' reading of the CLEAN is recorded here; F2's scope sentence
   below is Astra's interpretation, adopted.
7. **The prescreen (B2, B9).**  `prescreen/prescreen_asic.md` was written at 11:47, after Astra (11:32) and Grok
   (11:44) answered, and all three seats reported it absent.  Its ten LIVE items (What the packet missed, item 5) are
   the MAIN LOOP's reading of the file as it exists now, routed to packet D -- not a seat finding.  F6's "also
   `prescreen_asic.md` item 10" joins two issues: Fable's RED BY DESIGN `struct cpu` surface (a missing field fails to
   compile) and item 10's layout-masked access (disclose or pad), which goes to packet D.
8. **Attributions, records only.**  (B3) F7's buffer sizes are Grok's; Astra's is the "without claiming reentrant
   equivalence" clause.  (B4) Astra's F14 words are "eight accessible bytes at the passed pointer during the
   instrumented accesses"; "at least 8" and FROM BELOW are Fable's.  (B8) Fable's §3 table has 17 rows: sixteen
   parameter/extent cells plus the `struct cpu` surface.  (B7) REFUTED by both seats: `buf16` is Fable's own shorthand
   for `cand_buf16`.

## 4. Questions

**Q1.**  For each change listed in section 1: `APPLIED CORRECTLY | WRONG | NEW DEFECT -- <why>`, with file:line.
**Q2.**  Is anything in either final block now false against the seat files, the source, or the rulings it corrects?
**Q3.**  Name the ONE line most likely still to mislead a builder -- or say none, with the check that rules each out.

**Format:** the token, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line starting
`FLAG:`.  Facts and flags only.
