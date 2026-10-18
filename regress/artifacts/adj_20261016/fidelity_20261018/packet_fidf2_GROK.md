**Your token: `GROK_FIDF2_20261018`** -- open your answer with it.

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

## 5. The two verifications

Read them in full: `regress/artifacts/adj_20261016/fidelity_20261018/codex_fid.txt` (GPT-6 Astra) and `grok_fid.txt` (Grok 4.7); Argon's numbered flags beside them.

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
