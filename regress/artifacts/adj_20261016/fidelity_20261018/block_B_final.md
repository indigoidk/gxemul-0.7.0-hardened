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
   EQUIVALENT removals (`nooutparen` x3, `nocondparen`, `nocast`) -- equivalent for every in-tree use -- with
   `SYSASIC_EVENT_TO_ADDR(e) * 2` named as a use whose NUMERIC VALUE exposes only ADDR's outer-parenthesis removal:
   ADDR expands RANGE_OK but never BITMASK, and `nocast` changes only the expression's TYPE (`int` to `size_t`), which
   a comparison such as `< -1` would see -- so Fable's sentence presenting it for all five over-reaches (Astra, the two
   confirm passes; the macros in `fable5/meas_B/media/COMPOSITE_header_6b5cc648.h`), and LeakSanitizer (on by default
   under `-fsanitize=address`); the gate comment gains the VOID sentence.
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
