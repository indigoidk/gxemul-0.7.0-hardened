**Your token: `GLM_FIDF2_20261018`** -- open your answer with it.

# The rulings A/B fidelity corrections -- the shared-findings pass

## 0. What this is

On 2026-10-16 the main loop consolidated two adjudications (`regress/artifacts/adj_20261016/RULINGS_A_563.md`, #563; `RULINGS_B_asic.md`, asiceventaddr) from three seats each.  On 2026-10-18 an Argon reading flagged 27 places where the consolidations depart from their seats; GPT-6 Astra and Grok 4.7 then verified every flag against the seat files, independently.  The main loop settled their 13 splits by reading the cited lines and wrote the results as two FIDELITY CORRECTIONS blocks, plus inline pointers on the build-list lines they change.  Nothing existing is deleted.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the corrections are NOT yet in its files.  READ-ONLY.

## 1. The 27 flags, both verifications, and the settlement

| flag | GPT-6 Astra | Grok 4.7 | main loop's settlement | carried by block item |
|---|---|---|---|---|
| A1 | PARTLY | PARTLY | PARTLY | ruling A, item 7 |
| A2 | PARTLY | PARTLY | PARTLY | ruling A, item 7 |
| A3 | REFUTED | CONFIRMED | **PARTLY** | ruling A, item 7 |
| A4 | CONFIRMED | CONFIRMED | CONFIRMED | ruling A, item 7 |
| A5 | REFUTED | PARTLY | **PARTLY** | ruling A, item 7 |
| A6 | CONFIRMED | CONFIRMED | CONFIRMED | ruling A, item 1 |
| A7 | PARTLY | PARTLY | PARTLY | ruling A, item 7 |
| A8 | CONFIRMED | CONFIRMED | CONFIRMED | ruling A, item 2 |
| A9 | PARTLY | PARTLY | PARTLY | ruling A, item 7 |
| A10 | REFUTED | REFUTED | REFUTED | ruling A, item 7 |
| A11 | REFUTED | CONFIRMED | **PARTLY** | ruling A, item 7 |
| A12 | PARTLY | CONFIRMED | **CONFIRMED** | ruling A, item 7 |
| A13 | REFUTED | CONFIRMED | **CONFIRMED** | ruling A, item 3 |
| A14 | PARTLY | CONFIRMED | **CONFIRMED** | ruling A, item 3 |
| A15 | PARTLY | PARTLY | PARTLY | ruling A, item 3 |
| B1 | REFUTED | CONFIRMED | **PARTLY -- clarified, not reversed** | ruling B, item 1 |
| B2 | REFUTED | PARTLY | **PARTLY** | ruling B, item 7 |
| B3 | CONFIRMED | CONFIRMED | CONFIRMED | ruling B, item 8 |
| B4 | CONFIRMED | CONFIRMED | CONFIRMED | ruling B, item 8 |
| B5 | CONFIRMED | CONFIRMED | CONFIRMED | ruling B, item 6 |
| B6 | PARTLY | CONFIRMED | **CONFIRMED** | ruling B, item 6 |
| B7 | REFUTED | REFUTED | REFUTED | ruling B, item 8 |
| B8 | PARTLY | PARTLY | PARTLY | ruling B, item 8 |
| B9 | PARTLY | CONFIRMED | **CONFIRMED** | ruling B, item 7 |
| B10 | PARTLY | CONFIRMED | **CONFIRMED** | ruling B, item 3 |
| B11 | REFUTED | CONFIRMED | **PARTLY -- made explicit** | ruling B, item 2 |
| B12 | REFUTED | CONFIRMED | **PARTLY -- made explicit** | ruling B, item 2 |

## 2. Block A, as it will sit in RULINGS_A_563.md

## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING

An Argon reading flagged fifteen places where this file departs from its seats (`fidelity_20261018/argon_rulA563_numbered.md`,
A1-A15).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7 (`fidelity_20261018/grok_fid.txt`) then verified
every flag against the seat files; where they split, the main loop settled it by reading the cited lines.  **No grade and
no row's oracle changes.**  Items 1-6 change what a builder does; item 7 corrects attributions only.  The sentences they
correct stay in place below.

1. **N5's sequence (A6; both seats CONFIRMED).**  F4 below calls "one 2-byte store then 4-byte stores step 2, 6, 10, 14,
   ..., past 12, then on to 514" MEASURED.  The measured run is ONE 2-byte store, THREE 4-byte stores (occupancy 2, 6, 10,
   14 -- past 12 without touching it), then 2-byte stores to 514 (`fable5/meas_A/scratch_f4.c`, the push sequence before
   `occ =`; output `f4_run.txt`).  The continuous 4-byte stride is Astra's REASONED sequence (`astra/A_563/codex_adjA.txt`,
   F4), never run.  N5 uses the measured form, or measures the other before relying on it.
2. **VD1, N4's mutant (A8; both CONFIRMED).**  VD1 is `consumed = len == 4 ? 4 : 2` (`packet_A_563.md`, F15).  "VD1 is the
   downward bound move `len >= 1`" is the PACKET author's own added warrant (its "MINE" paragraph), not FB-A's answer.  It
   describes the same behaviour -- VD1 differs from HEAD only at width 1 -- but the table's mutant is the ternary form.  N4's
   oracle (32767) is unchanged.
3. **The PRETABLE (A13, A14, A15; Grok CONFIRMED A13 and A14 and PARTLY A15; Astra REFUTED A13, PARTLY A14 and A15).**  F25's "extended" is the MAIN
   LOOP's extension, and the seats split on it: Grok runs N1-N3 only, opposes N4, N5 and N6 ("No width-8 row is owed"), and
   asks the PRETABLE to run VD1 and the (`atapi_len > 0`, `atapi_received > 0`) mutant and EXPECT THEM GREEN; Fable 5.1
   specifies N1-N5; FB-A specifies N1-N5 with width 8 "not floor-owed".  The ruling overrides Grok on N4-N6; that dissent is
   recorded here, beside the rows it opposed.  The PRETABLE ALSO owes, from Astra: N2's one-sided count qualification,
   measured; N3's DRIVEN reachability sequence, measured separately from its synthesized fixture; and, from Grok, the
   (len > 0, received > 0) mutant as an expected-green control.  (Grok's expected-green VD1 is the overridden half: N4
   detects it.)
4. **N6 carries Astra's second-pop variants (Grok's Q3).**  F24 below enumerates `len >= 2` -> `len == 2 || len == 4` at
   both endian pop sites; the N6 bullet omits it.  N6's width-8 fixture is measured against both sites' variant
   (`codex_adjA.txt`, F24 and its table rows).
5. **"Every existing row byte-identical" has named exceptions (Astra's Q3).**  N4 adds a count read to the existing 1-byte
   walk, and R14/R15 change existing oracles.  And the disabled-direction partitions Astra required -- disabled READ and
   WRITE wherever existing rows do not discharge them -- are carried by the per-guard ledger (What the packet missed, item
   4): each such cell gets a row or a recorded discharge.
6. **G0's flag-only member (Argon's builder line; Astra and Grok agree the rows stand).**  The discriminator grades the
   flag-only candidate (e) in the ledger WITH its delta; the build list's G0/G2 rows still include it if the PRETABLE
   measures it distinguishing.  A row built for an (e) cell is L1, which this ruling chose.
7. **Attributions, records only.**  (A4, A7, A9) Fable 5.1's own ruling (`fable5/fable5_adj_A_563_v2.md`) is the seated
   vote and concurs on F4/D7, the repair-path discriminator, N5 and the case-partition reading; FB-A is credited for the
   measurement and the notes Fable read.  (A3) "the chain does NOT close" is FB-A's and Astra's wording; Fable's ruling
   says a repair without N5 closes half the joint.  (A11) the 262655-pair count is Grok's and the packet's; Astra's point
   is the lost wrapped dispatch.  (A12) F17 is not 3/3: Astra and Grok REFINE, and Grok CANNOT SETTLE the SUMMARY3 hunk
   counts and the grep FAIL count of 63.  (A1) Grok's "2 changed" is its own header; its body also changes F15, F16, F17
   and D3.  (A2) Fable 5.1 listed four WDC addresses (0x1f0/0x170, 0x900001f0, 0x14000180, 0x14000000); "every base except
   macppc" overstated it -- it also omits hpcmips' 0x140001f0 (`src/devices/dev_pcic.c`), beside macppc's 0xf3020000
   (`src/promemul/of.c`).  (A5) Grok's disclose rested on the channel fact the measurement refuted AND on classifying F4
   with the latches; both were its reasons.  (A10) REFUTED by both seats: FB-A's list is exactly the four this file quotes.


## 3. Block B, as it will sit in RULINGS_B_asic.md

## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING

An Argon reading flagged twelve places where this file departs from its seats (`fidelity_20261018/argon_rulBasic_numbered.md`,
B1-B12).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7 (`fidelity_20261018/grok_fid.txt`) then verified
every flag against the seat files; where they split, the main loop settled it by reading the cited lines.  **No pin, sample
or grade changes.**  Items 1-5 change or make explicit what a builder does; items 6-8 correct the record.  The sentences
they correct stay in place below.

1. **Record 3 and the cases-file comment (B1; Grok CONFIRMED, Astra REFUTED -- clarified, not reversed).**  LEAVE the
   cases-file comment ("a stub that drifted from these two lines reds the committed header ...") UNCHANGED: pin C makes it
   true.  Rewrite only the packet's record 3, to describe the pinned behaviour (`fable5/fable5_adj_B_asic.md`, F3, and its
   §7).  F3 below says the same thing in a sentence that can be read as editing the comment.
2. **The contract lines Fable §7 requires (B11, B12; Grok CONFIRMED, Astra REFUTED as incorporated by reference).**  "Fable
   §7 as the delta" below includes them; stated here so the build list carries them.  DISCLOSES gains the five
   EQUIVALENT removals (`nooutparen` x3, `nocondparen`, `nocast`), naming `SYSASIC_EVENT_TO_ADDR(e) * 2` as the in-tree use
   that would see them, and LeakSanitizer (on by default under `-fsanitize=address`); the gate comment gains the VOID
   sentence.
3. **Link versus run (B10; Grok CONFIRMED, Astra PARTLY).**  A failed compile or link is VOID -- the preflight; a sanitizer
   abort AFTER a successful link stays a row FAIL.  `id_verdict`'s `run_rc != 0` must not conflate them, and Record 1 says
   so (`grok/B_asic/grok_adjB.txt`, D1).
4. **The frozen PRETABLE keeps an erratum beside it (Astra's Q3).**  The three PRETABLE/SUMMARY corrections (What the
   packet missed, item 3) go into the NEW build's records.  The preserved PRETABLE is not rewritten -- its mtime is the
   order proof -- and gets an erratum file beside it (`prescreen/prescreen_asic.md`: "record the erratum beside it
   rather than edit it").
5. **Larger-buffer scope (Astra's Q3).**  F7's `buf[9]`, `buf[16]` and `buf[64]` are green under the shipped stub (Grok);
   only `buf[16]` was measured under both extent pins, `sizeof` and AddressSanitizer (Fable's `cand_buf16`).  The disclosure
   claims no more than that.
6. **F15 was overturned 1 of 3 (B5, B6; Grok CONFIRMED both, Astra CONFIRMED B5 and PARTLY B6).**  Astra overturned;
   Grok and Fable 5.1 UPHELD the packet's F15, both holding that F1 and F2 refute the panel's CLEAN.  The overturn stands ON
   THE FILE, not the count: `finalpass_20261013/panel_20261013_234442/ollama_deepseek.txt` quotes the builder's summary
   ("VERDICT: BUILT") and then gives its own "VERDICT: BREACH" on the short buffer.  The two upholds' reading of the CLEAN is
   recorded here; F2's scope sentence below is Astra's interpretation, adopted.
7. **The prescreen (B2, B9).**  `prescreen/prescreen_asic.md` was written at 11:47, after Astra (11:32) and Grok (11:44)
   answered, and all three seats reported it absent.  Its ten LIVE items (What the packet missed, item 5) are the MAIN LOOP's
   reading of the file as it exists now, routed to packet D -- not a seat finding.  F6's "also `prescreen_asic.md` item 10"
   joins two issues: Fable's RED BY DESIGN `struct cpu` surface (a missing field fails to compile) and item 10's layout-masked
   access (disclose or pad), which goes to packet D.
8. **Attributions, records only.**  (B3) F7's buffer sizes are Grok's; Astra's is the "without claiming reentrant
   equivalence" clause.  (B4) Astra's F14 words are "eight accessible bytes at the passed pointer during the instrumented
   accesses"; "at least 8" and FROM BELOW are Fable's.  (B8) Fable's §3 table has 17 rows: sixteen parameter/extent cells
   plus the `struct cpu` surface.  (B7) REFUTED by both seats: `buf16` is Fable's own shorthand for `cand_buf16`.


## 4. The inline pointers (the whole diff of both files)

```diff
--- a/RULINGS_A_563.md
+++ b/RULINGS_A_563.md
@@ -12,2 +12,48 @@
 REPAIR4 is below.
+
+## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING
+
+An Argon reading flagged fifteen places where this file departs from its seats (`fidelity_20261018/argon_rulA563_numbered.md`,
+A1-A15).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7 (`fidelity_20261018/grok_fid.txt`) then verified
+every flag against the seat files; where they split, the main loop settled it by reading the cited lines.  **No grade and
+no row's oracle changes.**  Items 1-6 change what a builder does; item 7 corrects attributions only.  The sentences they
+correct stay in place below.
+
+1. **N5's sequence (A6; both seats CONFIRMED).**  F4 below calls "one 2-byte store then 4-byte stores step 2, 6, 10, 14,
+   ..., past 12, then on to 514" MEASURED.  The measured run is ONE 2-byte store, THREE 4-byte stores (occupancy 2, 6, 10,
+   14 -- past 12 without touching it), then 2-byte stores to 514 (`fable5/meas_A/scratch_f4.c`, the push sequence before
+   `occ =`; output `f4_run.txt`).  The continuous 4-byte stride is Astra's REASONED sequence (`astra/A_563/codex_adjA.txt`,
+   F4), never run.  N5 uses the measured form, or measures the other before relying on it.
+2. **VD1, N4's mutant (A8; both CONFIRMED).**  VD1 is `consumed = len == 4 ? 4 : 2` (`packet_A_563.md`, F15).  "VD1 is the
+   downward bound move `len >= 1`" is the PACKET author's own added warrant (its "MINE" paragraph), not FB-A's answer.  It
+   describes the same behaviour -- VD1 differs from HEAD only at width 1 -- but the table's mutant is the ternary form.  N4's
+   oracle (32767) is unchanged.
+3. **The PRETABLE (A13, A14, A15; Grok CONFIRMED A13 and A14 and PARTLY A15; Astra REFUTED A13, PARTLY A14 and A15).**  F25's "extended" is the MAIN
+   LOOP's extension, and the seats split on it: Grok runs N1-N3 only, opposes N4, N5 and N6 ("No width-8 row is owed"), and
+   asks the PRETABLE to run VD1 and the (`atapi_len > 0`, `atapi_received > 0`) mutant and EXPECT THEM GREEN; Fable 5.1
+   specifies N1-N5; FB-A specifies N1-N5 with width 8 "not floor-owed".  The ruling overrides Grok on N4-N6; that dissent is
+   recorded here, beside the rows it opposed.  The PRETABLE ALSO owes, from Astra: N2's one-sided count qualification,
+   measured; N3's DRIVEN reachability sequence, measured separately from its synthesized fixture; and, from Grok, the
+   (len > 0, received > 0) mutant as an expected-green control.  (Grok's expected-green VD1 is the overridden half: N4
+   detects it.)
+4. **N6 carries Astra's second-pop variants (Grok's Q3).**  F24 below enumerates `len >= 2` -> `len == 2 || len == 4` at
+   both endian pop sites; the N6 bullet omits it.  N6's width-8 fixture is measured against both sites' variant
+   (`codex_adjA.txt`, F24 and its table rows).
+5. **"Every existing row byte-identical" has named exceptions (Astra's Q3).**  N4 adds a count read to the existing 1-byte
+   walk, and R14/R15 change existing oracles.  And the disabled-direction partitions Astra required -- disabled READ and
+   WRITE wherever existing rows do not discharge them -- are carried by the per-guard ledger (What the packet missed, item
+   4): each such cell gets a row or a recorded discharge.
+6. **G0's flag-only member (Argon's builder line; Astra and Grok agree the rows stand).**  The discriminator grades the
+   flag-only candidate (e) in the ledger WITH its delta; the build list's G0/G2 rows still include it if the PRETABLE
+   measures it distinguishing.  A row built for an (e) cell is L1, which this ruling chose.
+7. **Attributions, records only.**  (A4, A7, A9) Fable 5.1's own ruling (`fable5/fable5_adj_A_563_v2.md`) is the seated
+   vote and concurs on F4/D7, the repair-path discriminator, N5 and the case-partition reading; FB-A is credited for the
+   measurement and the notes Fable read.  (A3) "the chain does NOT close" is FB-A's and Astra's wording; Fable's ruling
+   says a repair without N5 closes half the joint.  (A11) the 262655-pair count is Grok's and the packet's; Astra's point
+   is the lost wrapped dispatch.  (A12) F17 is not 3/3: Astra and Grok REFINE, and Grok CANNOT SETTLE the SUMMARY3 hunk
+   counts and the grep FAIL count of 63.  (A1) Grok's "2 changed" is its own header; its body also changes F15, F16, F17
+   and D3.  (A2) Fable 5.1 listed four WDC addresses (0x1f0/0x170, 0x900001f0, 0x14000180, 0x14000000); "every base except
+   macppc" overstated it -- it also omits hpcmips' 0x140001f0 (`src/devices/dev_pcic.c`), beside macppc's 0xf3020000
+   (`src/promemul/of.c`).  (A5) Grok's disclose rested on the channel fact the measurement refuted AND on classifying F4
+   with the latches; both were its reasons.  (A10) REFUTED by both seats: FB-A's list is exactly the four this file quotes.
 
@@ -100,3 +146,5 @@
 
-New rows (fixtures synthesised as the shipped PIO row does; every existing row byte-identical):
+**[2026-10-18: read FIDELITY CORRECTIONS items 1-6 above first.  Item 3 adds three PRETABLE measurements; items 1, 2, 4 and 5 sharpen the N5, N4, N6 and preservation lines below.]**
+
+New rows (fixtures synthesised as the shipped PIO row does; every existing row byte-identical) **[2026-10-18, FIDELITY CORRECTIONS item 5: N4 and R14/R15 are the named exceptions.]**:
 - **N1** `PIO: stale xfer, no early irq` (S4 Row 1; allocate the declared 36-byte buffer).
@@ -104,5 +152,5 @@
 - **N3** the F20 joint cell (valid 40000-byte transfer, cursor 32768, ack, two bytes preloaded) + its WRITE counterpart.
-- **N4** VD1: a count read after the first 1-byte DATA read of the 1-byte walk, want 32767.
+- **N4** VD1: a count read after the first 1-byte DATA read of the 1-byte walk, want 32767.  **[2026-10-18, FIDELITY CORRECTIONS item 2: VD1 is `consumed = len == 4 ? 4 : 2`.]**
 - **N5** `CMDOUT boundary read, no transfer`: ATAPI_PKT_CMD; stores stepping past 12 to 514; one width-2 DATA read;
-  oracle `rep_asserts == 0 && warned_null_xfer == 1` (FB-A).
+  oracle `rep_asserts == 0 && warned_null_xfer == 1` (FB-A).  **[2026-10-18, FIDELITY CORRECTIONS item 1: the measured stores are 2, 4, 4, 4, then 2-byte stores to 514.]**
 - **N6** width 8: arm three distinguishable bytes (e.g. `12 34 56`), one 8-byte DATA read, check returned bytes, count,
@@ -110,4 +158,4 @@
   `cons_eq2` count 2; `n_E_cons_ge4` 0 / COMPLETED; the applicable `pop_ge4` occ 0 and latch set; `n_C6` count 3 and
-  zeros).  A two-byte transfer would miss `n_E_cons_ge4` (#475 clamps it back).
-- **G0/G2 rows** for each of Astra's three candidates that the PRETABLE measures as distinguishing.
+  zeros).  A two-byte transfer would miss `n_E_cons_ge4` (#475 clamps it back).  **[2026-10-18, FIDELITY CORRECTIONS item 4: also measured against Astra's second-pop variants at both endian sites.]**
+- **G0/G2 rows** for each of Astra's three candidates that the PRETABLE measures as distinguishing.  **[2026-10-18, FIDELITY CORRECTIONS item 6: the flag-only member included, graded (e) with its delta.]**
 Oracle additions: R14 (DATA-OUT both count bytes), R15 (interrupt-count increment across the disabled DATA read).
--- a/RULINGS_B_asic.md
+++ b/RULINGS_B_asic.md
@@ -12,2 +12,44 @@
 scope or wording, and the load-bearing ones are MEASURED.
+
+## FIDELITY CORRECTIONS, 2026-10-18 -- this consolidation checked against its own seats; READ BEFORE BUILDING
+
+An Argon reading flagged twelve places where this file departs from its seats (`fidelity_20261018/argon_rulBasic_numbered.md`,
+B1-B12).  GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) and Grok 4.7 (`fidelity_20261018/grok_fid.txt`) then verified
+every flag against the seat files; where they split, the main loop settled it by reading the cited lines.  **No pin, sample
+or grade changes.**  Items 1-5 change or make explicit what a builder does; items 6-8 correct the record.  The sentences
+they correct stay in place below.
+
+1. **Record 3 and the cases-file comment (B1; Grok CONFIRMED, Astra REFUTED -- clarified, not reversed).**  LEAVE the
+   cases-file comment ("a stub that drifted from these two lines reds the committed header ...") UNCHANGED: pin C makes it
+   true.  Rewrite only the packet's record 3, to describe the pinned behaviour (`fable5/fable5_adj_B_asic.md`, F3, and its
+   §7).  F3 below says the same thing in a sentence that can be read as editing the comment.
+2. **The contract lines Fable §7 requires (B11, B12; Grok CONFIRMED, Astra REFUTED as incorporated by reference).**  "Fable
+   §7 as the delta" below includes them; stated here so the build list carries them.  DISCLOSES gains the five
+   EQUIVALENT removals (`nooutparen` x3, `nocondparen`, `nocast`), naming `SYSASIC_EVENT_TO_ADDR(e) * 2` as the in-tree use
+   that would see them, and LeakSanitizer (on by default under `-fsanitize=address`); the gate comment gains the VOID
+   sentence.
+3. **Link versus run (B10; Grok CONFIRMED, Astra PARTLY).**  A failed compile or link is VOID -- the preflight; a sanitizer
+   abort AFTER a successful link stays a row FAIL.  `id_verdict`'s `run_rc != 0` must not conflate them, and Record 1 says
+   so (`grok/B_asic/grok_adjB.txt`, D1).
+4. **The frozen PRETABLE keeps an erratum beside it (Astra's Q3).**  The three PRETABLE/SUMMARY corrections (What the
+   packet missed, item 3) go into the NEW build's records.  The preserved PRETABLE is not rewritten -- its mtime is the
+   order proof -- and gets an erratum file beside it (`prescreen/prescreen_asic.md`: "record the erratum beside it
+   rather than edit it").
+5. **Larger-buffer scope (Astra's Q3).**  F7's `buf[9]`, `buf[16]` and `buf[64]` are green under the shipped stub (Grok);
+   only `buf[16]` was measured under both extent pins, `sizeof` and AddressSanitizer (Fable's `cand_buf16`).  The disclosure
+   claims no more than that.
+6. **F15 was overturned 1 of 3 (B5, B6; Grok CONFIRMED both, Astra CONFIRMED B5 and PARTLY B6).**  Astra overturned;
+   Grok and Fable 5.1 UPHELD the packet's F15, both holding that F1 and F2 refute the panel's CLEAN.  The overturn stands ON
+   THE FILE, not the count: `finalpass_20261013/panel_20261013_234442/ollama_deepseek.txt` quotes the builder's summary
+   ("VERDICT: BUILT") and then gives its own "VERDICT: BREACH" on the short buffer.  The two upholds' reading of the CLEAN is
+   recorded here; F2's scope sentence below is Astra's interpretation, adopted.
+7. **The prescreen (B2, B9).**  `prescreen/prescreen_asic.md` was written at 11:47, after Astra (11:32) and Grok (11:44)
+   answered, and all three seats reported it absent.  Its ten LIVE items (What the packet missed, item 5) are the MAIN LOOP's
+   reading of the file as it exists now, routed to packet D -- not a seat finding.  F6's "also `prescreen_asic.md` item 10"
+   joins two issues: Fable's RED BY DESIGN `struct cpu` surface (a missing field fails to compile) and item 10's layout-masked
+   access (disclose or pad), which goes to packet D.
+8. **Attributions, records only.**  (B3) F7's buffer sizes are Grok's; Astra's is the "without claiming reentrant
+   equivalence" clause.  (B4) Astra's F14 words are "eight accessible bytes at the passed pointer during the instrumented
+   accesses"; "at least 8" and FROM BELOW are Fable's.  (B8) Fable's §3 table has 17 rows: sixteen parameter/extent cells
+   plus the `struct cpu` surface.  (B7) REFUTED by both seats: `buf16` is Fable's own shorthand for `cand_buf16`.
 
@@ -79,2 +121,4 @@
 
+**[2026-10-18: read FIDELITY CORRECTIONS items 1-5 above first -- item 1 says which Record 3 text to leave alone, and items 2-5 are build actions this list implies but does not spell out.]**
+
 Fable §7 as the delta: pins A (size_t), B (inside `run_row`, with the VOID preflight), C; the two SWEEP samples and two TX

```

## 5. The two verifications, verbatim

---- GPT-6 Astra (`fidelity_20261018/codex_fid.txt`) ----
ASTRA_FID_20261018
VERDICT: 6 confirmed, 10 refuted, 11 partly -- Attribution and measurement errors remain, but several alleged contradictions disappear when the complete answers, timeline, and incorporated build instructions are read.

**Q1.**

Citation aliases below identify files under `GXEMUL-SEC/regress/artifacts/adj_20261016/`; numbers following an alias are file line numbers.

A: **AF** = [RULINGS_A_563.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/RULINGS_A_563.md); **A1S** = [astra/A_563/codex_adjA.txt](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/astra/A_563/codex_adjA.txt); **A2S** = [grok/A_563/grok_adjA.txt](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/grok/A_563/grok_adjA.txt); **A3S** = [fable5/fable5_adj_A_563_v2.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/fable5/fable5_adj_A_563_v2.md); **A4S** = [fable5/FALLBACK_opus48_adj_A_563.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/fable5/FALLBACK_opus48_adj_A_563.md).

B: **BF** = [RULINGS_B_asic.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/RULINGS_B_asic.md); **B1S** = [astra/B_asic/codex_adjB.txt](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/astra/B_asic/codex_adjB.txt); **B2S** = [grok/B_asic/grok_adjB.txt](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/grok/B_asic/grok_adjB.txt); **B3S** = [fable5/fable5_adj_B_asic.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/fable5/fable5_adj_B_asic.md); **PS** = [prescreen/prescreen_asic.md](C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/adj_20261016/prescreen/prescreen_asic.md).

A1: PARTLY -- AF:8 reproduces A2S:4’s self-reported two, but A2S:24–26,37 changes four itemized labels; A4S:9 expressly counts F4/D7, while :91 says “UPHOLD, and strengthen”; F should distinguish Grok’s reported count from its four changed labels, without declaring FB-A’s third change compulsory.

A2: PARTLY -- AF:11’s exhaustive “every WDC base except macppc” exceeds A3S:47’s enumerated addresses; A4S:15 names cats/iyonix files but supplies no additional addresses proving Argon’s counterexample; F should reproduce the listed addresses and identify macppc’s omission without claiming exhaustiveness.

A3: REFUTED -- A3S:51 explicitly says that without N5 the next repair closes half a joint and the following pass finds the other half; that supports AF:11–12’s insufficiency summary despite the absence of the literal name `REPAIR4`.

A4: CONFIRMED -- AF:17–24,75 omits Fable from the local support lists although A3S:10,36,41,51,55 supplies F4/D7, the discriminator, and N5; F should add Fable’s concurrence while retaining FB-A’s measurement credit; AF:11 already acknowledges that concurrence in the roster.

A5: REFUTED -- A2S:13 expressly claims only `warned_null_xfer` moves, and :41 grounds D7 in those same channel facts; AF:17–18 correctly identifies that refuted premise and does not say it was Grok’s only rationale; A2S:59’s additional class interpretation does not negate it.

A6: CONFIRMED -- A1S:48–52 supplies the reasoned one-two-byte-plus-128-four-byte sequence; A4S:25,115 and A3S:51 give the measured sequence, confirmed by `fable5/meas_A/scratch_f4.c:416–423`: one two-byte store, three four-byte stores, then 250 two-byte stores; AF:19–20 should distinguish REASONED from MEASURED.

A7: PARTLY -- AF:9–11 explicitly distinguishes FB-A from resumed Fable, and genuine FB-A measurements and arguments remain correctly attributable; nevertheless the local ruling summaries omit Fable’s votes recorded at A3S:16,18–21,36–38,45,51,57; F should add those votes without mechanically replacing legitimate FB-A citations.

A8: CONFIRMED -- AF:33–36 presents the downward-bound warrant within “FB-A’s answer,” but it originates in `packet_A_563.md:129–136`; A4S:58 names the actual mutant `len == 4 ? 4 : 2`, and A1S:23 rejects the additional D2 warrant; F should identify the packet author’s warrant separately from FB-A’s case-partition argument.

A9: PARTLY -- A4S:59,96 supports the argument AF:41–42 attributes to FB-A; A3S:37–38,45 also supports the case partition and non-dominating-ternary conclusion; F should add Fable’s concurrence, while retaining FB-A’s provenance for the “far region’s branch” wording.

A10: REFUTED -- AF:51–52 describes FB-A’s list, and A4S:53 lists exactly those four addresses; A3S:47’s additional hpcmips address belongs to the separate resumed answer.

A11: REFUTED -- A1S:60 explicitly identifies lost wrapped-CDB dispatch, while :24,61–64 supplies the other normalization refinements; A2S:25,47 supplies the numerical sequence, also present in `packet_A_563.md:140–142`; AF:55–59 credits the combined rewrite, does not attribute every calculation to both seats, and does not claim unanimous support.

A12: PARTLY -- AF:60’s “records accepted (3/3)” overstates A2S:26, which cannot settle the hunk and grep counts; however AF:61–62 expressly preserves A1S:25’s rewrite requirement; F should qualify the consensus and name Grok’s unverified numerical records.

A13: REFUTED -- AF:68 explicitly says “extended,” and A1S:33,119–141 requires the additional G0/G2 witnesses and width fixture; F does not claim that every seat independently prescribed N1–N6.

A14: PARTLY -- A1S:135,141 expressly requires separate driven N3 reachability and N2’s one-sided count qualification, neither carried into AF:68–69,102–112; F should restore both; the broader width requirement is retained through AF:66–69,108–111.

A15: PARTLY -- Grok’s N5/N4/width dissent is already visible at AF:17,33,38–44, and A2S:53 rejects latch expansion rather than every additional cell; the omitted surviving obligation is A2S:59’s expected-green PRETABLE run of the positive-length/positive-cursor mutant; F should add that run and identify VD1’s proposed green outcome as rejected dissent, since adopted N4 detects it.

B1: REFUTED -- BF:24–25 directs rewriting Record 3 to describe the pinned behavior, making the existing cases-file sentence true; that matches B3S:35,44,116 and does not direct reversing the cases-file comment.

B2: REFUTED -- PS:291–293 contains item 10; `fidelity_20261018/fid_brief.md:29–31` places its creation after Astra/Grok answered and before BF; B1S:117, B2S:63, and B3S:15 do not establish absence at BF’s time.

B3: CONFIRMED -- B2S:20,48 supplies the specific `buf[9]/[16]/[64]` refinement; B1S:11 upholds F7 and :89 states a general larger-allocation limitation; BF:41 should credit this specific refinement to Grok, with Astra’s general compatibility stated separately.

B4: CONFIRMED -- BF:45–46’s attributed quotation adds “at least” and omits “during the instrumented accesses” from B1S:38; “at least 8” comes from B3S:43; F should use Astra’s exact wording or identify a combined paraphrase retaining the access qualification.

B5: CONFIRMED -- BF:47 gives Astra’s overturn without recording B2S:36 and B3S:55’s contrary upholds; F should say Astra’s attribution correction was adopted over those two upholds and explain the choice.

B6: PARTLY -- BF:49’s qualification is explicitly B1S:36, so it is neither invented nor wrongly attributed; B2S:36 and B3S:55 nevertheless reach the contrary CLEAN-refutation judgment; F should identify Astra’s interpretation as adopted and record the contrary judgments.

B7: REFUTED -- B3S:29 identifies `cand_buf16`, then uses `buf16` shorthand there and at :43,98; BF:52 does not introduce a different measured medium.

B8: PARTLY -- B3S:74–90 contains 17 table rows, but BF:70,84 faithfully repeats B3S:98’s sixteen parameter/extent cells, and BF:39 retains the separately described CPU surface; F should make the denominator explicit: sixteen parameter/extent cells plus the `struct cpu` surface, seventeen table rows.

B9: PARTLY -- The ten items exist at PS:264–293,313, and PS:3 already identifies packet-D routing; however none was adjudicated in these B answers (B1S:117; B2S:63; B3S:15,102); BF:73–76 should identify this as prescreen/main-loop routing rather than leave its relationship to the three-seat consolidation implicit.

B10: PARTLY -- B2S:34,40’s explicit successful-link/runtime-abort distinction and `id_verdict` proposal are omitted, but BF:54–55 already adopts the measured preflight remedy for unavailable libasan; F should state runtime sanitizer abort after successful linking is row FAIL, toolchain inability is VOID, and explain the adopted preflight remedy.

B11: REFUTED -- BF:63–64 already specifies five EQUIVALENT-disclosed removals, and :80 expressly adopts Fable §7, whose B3S:116 places them in DISCLOSES; B3S:45 supplies their names and exposing use.

B12: REFUTED -- BF:80 incorporates Fable §7; B3S:116 explicitly requires both LeakSanitizer in DISCLOSES and the VOID sentence in the gate comment, explained at :57; their omission from the inline recap does not remove those incorporated requirements.

**Q2.**

The concrete omissions concern PRETABLE checks. The flagged provenance errors do not establish a wrong N4 oracle, an invalid N5 endpoint, or a required erroneous edit to the B cases comment.

- **A PRETABLE / N2 and N3:** a builder following the condensed list could omit N2’s one-sided qualification check and measure only N3’s synthesized fixture, skipping its separately driven reachability sequence. Restore both requirements from A1S:135,141 to AF:68–69,102–104.
- **A PRETABLE / disclosed positive-length/positive-cursor cell:** AF:86–88,115 retains the disclosure but omits A2S:59’s explicit expected-green run. Add that control; do not restore Grok’s expected-green VD1 outcome against the adopted N4 ruling.
- **A N5:** reproducing AF:19–20’s sequence while labeling it the existing measurement would be wrong provenance. The measured stores are `2,4,4,4`, then 250 two-byte stores (`fable5/meas_A/scratch_f4.c:416–423`). The alternative sequence remains supported as REASONED by A1S:48–52; AF:106–107’s endpoint and oracle need no demonstrated correction.
- **A N4, G0/G2, R14/R15:** AF:105’s count of 32767 matches A1S:137; AF:112 requires all three distinguishing G0/G2 candidates, including the flag-only candidate; AF:113 preserves both count bytes and the interrupt-count increment. Neither A8 nor Argon’s unnumbered G0 argument establishes a wrong implementation here (A1S:74–76,120,137).
- **B build:** update Record 3 while retaining the cases comment’s now-true statement; include the five equivalent-removal disclosures, LeakSanitizer, and the gate VOID sentence. Those actions are already required by BF:24–25,63–64,80 and incorporated B3S:116. The confirmed B attribution/quotation flags do not prescribe a different pin or sample.

**Q3.**

Additional builder-relevant issues:

- **A’s blanket preservation instruction conflicts with its oracle changes.** AF:101 says every existing row remains byte-identical, but N4 modifies the existing one-byte walk, and R14/R15 modify existing oracles (A4S:166; A2S:26; A1S:137; AF:105,113). State the exceptions explicitly so the preservation sentence cannot suppress the required additions.
- **A drops the explicit disabled-WRITE coverage requirement.** A1S:99,120 requires applicable enabled/direction partitions, including disabled READ/WRITE checks where existing rows do not discharge them. AF:78–82,112 lists disabled READ candidates and the G2 WRITE counterpart, but does not carry that broader requirement. Restore it or supply the ledger proof that existing rows discharge those partitions.
- **B must preserve the frozen PRETABLE artifact.** BF:67–69,83 calls for corrections without carrying PS:295–298’s instruction to place the erratum beside the old PRETABLE because its mtime proves ordering. Distinguish correcting the new build’s records from rewriting the preserved artifact.
- **B conflates two CPU-stub issues.** BF:39’s “also prescreen item 10” joins missing-field compilation failures—B3S:47,90’s RED BY DESIGN—with PS:291–293’s masked layout-based access. The latter needs disclosure or padding; RED BY DESIGN does not dispose of it. BF:76 routes layout to D, so preserve that distinction.
- **B overstates larger-buffer measurement scope.** BF:41–42 reads as though all three sizes passed the shipped, `sizeof`, and ASan instruments. B2S:48 records all three shipped greens but specifically `buf[16]` under both extent pins; B3S:29 likewise measures `cand_buf16`. Correct the scope so `[9]` and `[64]` extent-pin checks are not treated as already measured.


---- Grok 4.7 (`fidelity_20261018/grok_fid.txt`) ----
I'll check each of Argon's 27 flags against the seat answers and the two rulings, without treating either side as already right. First I'll read the numbered flags and the ruling files they cite.The flags are specific about quotations, attributions, and counts. I'll read both rulings and the seat lines they cite before judging any of them.The rulings are in. Next I’ll check the seat lines each flag cites, starting with the A-side headers, F4 measurement, and the disputed attributions.The F4 harness does not match the 4-byte stride the ruling calls measured. I’ll read the seat passages the other flags cite, including the B-side prescreen timing.GROK_FID_20261018

VERDICT: 17 confirmed, 8 partly, 2 refuted -- the rulings mis-credit FB-A for Fable on several A items, label an unmeasured 4-byte N5 stride as measured, and on B adopt Astra's lone F15 overturn plus a prescreen list no seat ruled, while dropping Fable's DISCLOSES lines.

File mtimes were not re-stated here. The seat texts and the prescreen as it exists now were read. The 11:32 / 11:44 / 11:47 / 12:09 / 20:27 timeline below is the one given in the question.

## Q1

A1: PARTLY -- `RULINGS_A_563.md:8-9,11` copies the seats' own headers (`grok_adjA.txt:4` "2 rulings changed", `FALLBACK_opus48_adj_A_563.md:9` "2 rulings changed: F4, D7", `fable5_adj_A_563_v2.md:1` "(2)"); the bodies change more lines: Grok also `F17 REFINE` at `grok_adjA.txt:26` beside `F15` `:24`, `F16` `:25`, and `D3` `:37` (the header bundles D3/F15 as one), and FB-A also strengthens F25 at `FALLBACK_opus48_adj_A_563.md:91` beside F4 `:70` and D7 `:99`. F should say Grok's "2" omits the F17 refine, and FB-A's "2" sits beside an F25 strengthen that adds N5 to the pre-table.

A2: PARTLY -- `RULINGS_A_563.md:11` says S3 lists every WDC base except macppc `0xf3020000`. `fable5_adj_A_563_v2.md:47` lists only `0x1f0/0x170`, `0x900001f0`, `0x14000180`, and `0x14000000`. Macppc `0xf3020000` is real (`src/promemul/of.c:938`), and so is a second hpcmips base `0x140001f0` (`src/devices/dev_pcic.c:240`), which S3 also omits. Cats and iyonix are not extra bases: `machine_iyonix.c:82` calls `bus_isa_init` with flags 0, and `machine_cats.c` never calls it. `FALLBACK_opus48_adj_A_563.md:15` only names those files among files opened. F should say S3 lists those four and does not mention macppc or `0x140001f0`.

A3: CONFIRMED -- `fable5_adj_A_563_v2.md` never says `REPAIR4` or that the chain does not close. That text is `FALLBACK_opus48_adj_A_563.md:9` and `:120-130`, and `codex_adjA.txt:115-117`. S3:51 only says the next repair without N5 closes half a joint. F should attribute the insufficiency to FB-A and Astra, not to Fable 5.1.

A4: CONFIRMED -- `RULINGS_A_563.md:17-24` and `:75` name Astra and FB-A for the F4/D7 overturn, the repair-path discriminator, and N5. `fable5_adj_A_563_v2.md:10`, `:41`, `:51`, and `:55` rule `F4 DIFFER`, `D7 DIFFER`, the same discriminator, and row N5. `RULINGS_A_563.md:11` already records S3's outcome, and S3:3 says it used FB-A as a colleague's notes. F should add Fable 5.1 to the itemized F4/D7/N5 lines.

A5: PARTLY -- `grok_adjA.txt:13` says the F4 cell "moves only `warned_null_xfer`", and `:41` says D7 has "the same channel facts". That is the premise the measurement refutes (`f4_run.txt:2-4` vs `:12-14`). `grok_adjA.txt:59` also files F4 with F10, F11, F18, and F19 under the latch rule, and `:27` already treats F18's 514-byte INTRQ split as (e). `:41` is the channel-fact ground, not the rule ground. F should state both: the channel fact is refuted, and Grok's repair still classifies F4 with the latches.

A6: CONFIRMED -- `RULINGS_A_563.md:19-20` calls "one 2-byte store then 4-byte stores ... 14, ..., past 12, then on to 514" MEASURED in `f4_run.txt`. That file records only `occ=514` and `dispatched=no` (`f4_run.txt:3-4`). The harness is one 2-byte store, three 4-byte stores to 14, then 2-byte stores to 514 (`scratch_f4.c:416-423`; `FALLBACK_opus48_adj_A_563.md:25`, `:115`; `fable5_adj_A_563_v2.md:51`). The continuous 4-byte stride is Astra's unrun reasoning (`codex_adjA.txt:48-52`). F should split those two sequences and not tag the 4-byte tail MEASURED.

A7: PARTLY -- the itemized lines do cite FB-A where S3 also ruled (`fable5_adj_A_563_v2.md:16`, `:18-19`, `:21`, `:30`, `:36-38`, `:45-47`, `:51`, `:57`), but `RULINGS_A_563.md:9-11` already says FB-A is not the Fable seat and records S3's verdict. Several citations are true of FB-A's own text (the measurement, `FALLBACK_opus48_adj_A_563.md:53` bases, `:125` oracle). The per-guard ledger at `RULINGS_A_563.md:89-90` is Astra's (`codex_adjA.txt:133`); S2, S3, and S4 do not say replace HELD/EXHAUSTED with a ledger. F should cite S3 as the seated vote, FB-A for the measurement and the notes S3 used, and Astra alone for the ledger.

A8: CONFIRMED -- `RULINGS_A_563.md:33-36` puts "VD1 is the downward bound move `len >= 1`" in FB-A's answer to Grok. `FALLBACK_opus48_adj_A_563.md:58` defines VD1 as `consumed = len == 4 ? 4 : 2` and calls width 1 the below-bound region of `len >= 2`. S3 never says `len >= 1` (`fable5_adj_A_563_v2.md:21`, `:45`). The bound-move warrant is the packet's, `len >= 2` -> `len >= 1` (`packet_A_563.md:129`, `:133`), which Grok identifies as the packet's warrant (`grok_adjA.txt:45`). F should name the mutant `len == 4 ? 4 : 2` and attribute the bound-move sentence to the packet, not to FB-A.

A9: PARTLY -- "the far region's branch is discharged" is FB-A (`FALLBACK_opus48_adj_A_563.md:59`), and "D2 does not bind" the non-dominating ternary is FB-A (`:96`). Attributing that wording to FB-A is right. S3 states the same grade without that wording (`fable5_adj_A_563_v2.md:38`, `:45`) and `RULINGS_A_563.md:41-42` omits S3. F should cite both.

A10: REFUTED -- `RULINGS_A_563.md:51-52` quotes FB-A's list, and `FALLBACK_opus48_adj_A_563.md:53` says exactly "every real wdc base (0x1f0, 0x170, 0x14000000, 0x900001f0)". `fable5_adj_A_563_v2.md:47`'s extra `0x14000180` is S3's list, not a correction of the FB-A attribution. Cats and iyonix are not further bases (see A2).

A11: CONFIRMED -- the 262655 store/read-pair dispatch is the packet (`packet_A_563.md:140-141`) and Grok (`grok_adjA.txt:25`, `:47`). Astra's 262655 is raw occupancy −1 under the `<-1` mutant (`codex_adjA.txt:62`); Astra does say deletion can drop a wrapped dispatch (`:60`) without that pair count. `fable5_adj_A_563_v2.md:22` and `FALLBACK_opus48_adj_A_563.md:82` uphold (e) on the `write_in_progress` drain gate and the false "never wraps" record, without the pair count. F should not attribute the pair-count sentence to Astra.

A12: CONFIRMED -- `RULINGS_A_563.md:60` says "F17 -- records accepted (3/3)". `fable5_adj_A_563_v2.md:23` and `FALLBACK_opus48_adj_A_563.md:83` accept. `codex_adjA.txt:25` is `F17 REFINE` and rewrites R1–R5. `grok_adjA.txt:26` is `F17 REFINE`, refines the R15 warrant because `irq_off` is taken before the disabled DATA read, and `CANNOT SETTLE`s the SUMMARY3 hunk counts and the grep FAIL count of 63. The later clauses at `RULINGS_A_563.md:60-62` do record Astra's rewrite. F should drop "3/3" and record Grok's unsettle.

A13: CONFIRMED -- `RULINGS_A_563.md:68-69` says the pre-table measures N1–N6 and the G0/G2 candidates. `grok_adjA.txt:59` runs N1–N3 only, drops N4 as a floor row, and expects VD1 and the len>0/received>0 mutant green; `:37` says no width-8 row is owed; `:13` upholds F4 as disclose, which is the N5 cell. `fable5_adj_A_563_v2.md:31` adds N5 to "every new row" and does not require N6. `FALLBACK_opus48_adj_A_563.md:91`, `:127-128` specify N1–N5; `:61` says a width-8 row is not floor-owed. F should mark N1–N6 plus G0/G2 as the main loop's extension, with that seat split.

A14: CONFIRMED -- `codex_adjA.txt:141` requires the pre-table to measure N2's one-sided count qualification and all width variants; `:135` requires N3's driven reachability sequence to be measured separately from the synthesized fixture. `RULINGS_A_563.md:68-69` and `:112` say "every new row ... on HEAD and on its named mutants" and do not state either requirement.

A15: PARTLY -- `RULINGS_A_563.md:33` and `:123` record Grok's (e) dissent on VD1, `:17` records the F4 disclose as resting on a refuted premise, and `:86-88` plus `:115` include the (len>0, received>0) cell as (e). `RULINGS_A_563.md:78-85` and `:99-116` do not say Grok opposed N4, N5, and N6, and they do not say the pre-table runs VD1 and the len>0 mutant and expects them green (`grok_adjA.txt:36`, `:53`, `:59`; `:37` "No width-8 row is owed"). F should put that dissent and the "expect green" pre-table next to those rows, as positions the ruling overrides.

B1: CONFIRMED -- `RULINGS_B_asic.md:24-25` says Record 3 is rewritten to the pinned behaviour, "which makes the cases-file sentence true rather than reversed." `fable5_adj_B_asic.md:35` says the cases-file sentence becomes TRUE under pin C instead of being rewritten to say the opposite. `:44` and `:116` rewrite packet record 3, not the comment. The comment is `sysasic_range_cases.c:35-36` ("a stub that drifted from these two lines reds the committed header"). F should say: leave that comment; pin C makes it true; rewrite packet record 3 only.

B2: PARTLY -- all three seats say `prescreen_asic.md` was absent (`codex_adjB.txt:117`, `grok_adjB.txt:63`, `fable5_adj_B_asic.md:15`). On the given timeline Astra and Grok were right; the file was written at 11:47, and Fable's 12:09 answer still says absent. The file exists now. Item 10 (`prescreen_asic.md:291-293`, FX5) is the stub `struct cpu` layout (disclose or pad). Fable's ruling (`fable5_adj_B_asic.md:47`) is its own: the stub surface is `mem` and `memory_rw` only, RED BY DESIGN by text. `RULINGS_B_asic.md:39`'s "also" equates them. F should keep Fable's sentence as Fable's and mark item 10 as the main loop's later cross-reference.

B3: CONFIRMED -- `RULINGS_B_asic.md:41` attributes `buf[9]`, `buf[16]`, and `buf[64]` to "(Grok; Astra)". Only Grok adds those sizes (`grok_adjB.txt:20`, `:48`). Astra upholds F7 without them (`codex_adjB.txt:11`). Fable upholds `static8` reentrancy only (`fable5_adj_B_asic.md:48`). The "without claiming reentrant equivalence" clause is Astra's. F should split those two refinements.

B4: CONFIRMED -- `RULINGS_B_asic.md:45` quotes Astra as "at least eight accessible bytes at the passed pointer". `codex_adjB.txt:38` says "eight accessible bytes at the passed pointer during the instrumented accesses", with no "at least". "at least 8 bytes" is Fable (`fable5_adj_B_asic.md:43`). The same blend is at `RULINGS_B_asic.md:21-22`. F should quote Astra without "at least" and attribute FROM BELOW / "at least 8" to Fable.

B5: CONFIRMED -- `RULINGS_B_asic.md:47` rules "F15 -- OVERTURNED (Astra)" and does not say the vote is 1/3. Grok upholds (`grok_adjB.txt:36`). Fable upholds and says the three CLEANs and "BUILT" are refuted by measurement (`fable5_adj_B_asic.md:55`). F should state the 1/3 split.

B6: CONFIRMED -- `RULINGS_B_asic.md:48-49` adopts Astra (`codex_adjB.txt:36`): the panel CLEAN excluded the short buffer, so F2 does not refute it and F1 does. Grok the adjudicator says "F1 and F2 refute that CLEAN" (`grok_adjB.txt:36`). Fable upholds the packet's refutation of the CLEANs and "BUILT" (`fable5_adj_B_asic.md:55`; the packet's F15 is F1/F2, `packet_B_asic.md:110`). F should record that 2/3.

B7: REFUTED -- `fable5_adj_B_asic.md:29` names the medium `cand_buf16` and records PASS, and the sizeof cell on that row is "PASS (buf16)". `:98` lists `buf16` among the measured greens. `RULINGS_B_asic.md:52`'s `buf16` is Fable's own shorthand for that green.

B8: PARTLY -- `RULINGS_B_asic.md:70` says "Fable §3: sixteen". The §3 table has 17 rows (`fable5_adj_B_asic.md:74-90`). Fable's own summary says 16 (`:98`) by not counting the 17th row, the stub `struct cpu` surface, which `:90-92` places in RED BY DESIGN. F already states that surface at `:39`. F should say 16 in Fable's summary, plus that 17th row outside the 16.

B9: CONFIRMED -- `RULINGS_B_asic.md:73-76` lists ten LIVE items and does not say they are the main loop's. They match the file's own ten (`prescreen_asic.md:263-293`, count at `:313`). Every seat reported zero LIVE items (`codex_adjB.txt:117`, `grok_adjB.txt:63`, `fable5_adj_B_asic.md:15`, `:102`). Astra and Grok were right at their times; Fable's 12:09 "absent" is after the 11:47 write; the ruling is at 20:27. F should label the list as the main loop's reading of the file that exists now, routed to packet D, not a seat finding.

B10: CONFIRMED -- `grok_adjB.txt:4`, `:34`, and `:40` say `id_verdict` / `run_rc != 0` must not turn a failed link into a row FAIL (that is VOID), while a sanitizer abort after a successful link stays the row FAIL, and Record 1 must say so. `RULINGS_B_asic.md:51-57` states Fable's preflight and Astra's scope, and `:34` does not carry Grok's Record 1 sentence. The preflight covers the missing-libasan half (`fable5_adj_B_asic.md:36`, `:57`). F should add Grok's `run_rc` split and the Record 1 wording.

B11: CONFIRMED -- `fable5_adj_B_asic.md:45`, `:98`, and `:116` require `nooutparen` ×3, `nocondparen`, and `nocast` in DISCLOSES as EQUIVALENT, and name `SYSASIC_EVENT_TO_ADDR(e) * 2` as the use that would see them. `RULINGS_B_asic.md:63-64` says only that nine paren/cast removals are reclassified, four DETECT and five EQUIVALENT-disclosed. `:80-85` does not put the five into DISCLOSES or name that use. F should add both.

B12: CONFIRMED -- `fable5_adj_B_asic.md:57` and `:116` require LeakSanitizer in DISCLOSES (on by default under `-fsanitize=address`) and the VOID sentence in the gate comment. `RULINGS_B_asic.md:51-57` and `:80-85` have the instrument VOID and do not have either contract line.

## Q2

Three build-list items would be implemented wrong off a confirmed flag.

N5 in ruling A's repair (`RULINGS_A_563.md:106-107`, governed by `:19-20`, flag A6). A builder who copies the sentence marked MEASURED uses one 2-byte store and then 4-byte stores from occupancy 2 through 514. The run that produced `f4_run.txt` did three 4-byte stores to 14 and then 2-byte stores to 514 (`scratch_f4.c:416-423`). The 4-byte tail is Astra's unrun sequence (`codex_adjA.txt:48-52`). The build-list bullet itself only says "stores stepping past 12 to 514", which still fits the measured tail.

Record 3 / pin C in ruling B (`RULINGS_B_asic.md:24-25`, and "records 1-5 as refined" at `:82`, flag B1). A builder can edit the comment in `sysasic_range_cases.c:35-36` so that it "describes the pinned behaviour" or says the opposite of what it says now. Fable's instruction is to leave that sentence; pin C makes it true (`fable5_adj_B_asic.md:35`). Only packet record 3 is rewritten (`:44`, `:116`).

Ruling B's contract lines (`RULINGS_B_asic.md:80-85`, flags B11 and B12). A builder who follows that paragraph ships without five DISCLOSES entries (`nooutparen` ×3, `nocondparen`, `nocast`), without naming `SYSASIC_EVENT_TO_ADDR(e) * 2`, without LeakSanitizer, and without the VOID sentence in the gate comment (`fable5_adj_B_asic.md:45`, `:57`, `:116`).

Two narrower misses on the same lists. N4's bullet (`RULINGS_A_563.md:105`) is a count read, want 32767, against the existing mutant `len == 4 ? 4 : 2` (`packet_A_563.md:129`, `:136`). The prose at `:35-36` (flag A8) calls VD1 the move `len >= 1`. Coding that bare compare, rather than the inner change `len >= 2` -> `len >= 1`, is a different mutant; the inner change matches width-1 consumed 2. And the first G0 candidate, `!io_enabled && atapi_cmd_in_progress` (`:78-79`), is the "flag-only member" graded only in the ledger (`:83-85`), while `:112` and Astra (`codex_adjA.txt:74`, `:120`) require a fixture row if the pre-table shows the pop. That contradiction is Argon's unnumbered builder line, and it holds.

## Q3

Astra's second-pop variants are in the rulings and absent from the repair build list. `codex_adjA.txt:32`, `:101`, and `:131` require `len >= 2` -> `len == 2 || len == 4` at both endian sites `:1201/:1208`, measured on the width-8 fixture. `RULINGS_A_563.md:66-67` records that refine. The N6 bullet (`:108-111`) copies Astra's width-8 oracle and does not mention those variants, and `:99-116` does not either. Argon's A14 is the other Astra pre-table requirements (N2's one-sided count, the separate N3 reachability run), not this drop.

Argon's task 3 says no ruling in F lacks a seat and is unmarked. The `len >= 1` sentence (flag A8) is that ruling: no seat wrote it, and it is not marked as the main loop's. The packet wrote `len >= 2` -> `len >= 1` (`packet_A_563.md:133`).


## Questions

**Please do not simply ratify.**  Thirteen of the 27 flags split the two verifying seats, and the main loop settled each
split itself.  The load-bearing question is **WHICH OF MY 27 SETTLEMENTS IS WRONG?** -- and a seat whose verdict a
settlement OVERRODE is asked to be hardest on that one, and equally hard on any settlement that ADOPTED its own verdict.

**Q1.**  For each of the 13 SPLIT rows (bold in the table), one line: `<flag>: RIGHT | WRONG | PARTLY -- <why>`, with
the file:line that settles it.  A FILE-READING seat checks the seat files under
`GXEMUL-SEC/regress/artifacts/adj_20261016/` (S-files named in `fidelity_20261018/fid_brief.md`); a packet-fed seat rules
from the two verification answers inlined below and says NOT CHECKABLE where they do not settle it.

**Q2.**  Does any block item MISSTATE a seat, a file or a number -- especially items A1-A6 and B1-B5, which change what a
builder does?

**Q3.**  Is any build-changing correction still missing from the blocks?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
