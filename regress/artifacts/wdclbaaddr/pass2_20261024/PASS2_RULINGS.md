# T4 `wdclbaaddr` (-> #572) -- PASS-2 RULINGS, main loop 087a90, 2026-10-24 21:1x-22:0x

Pass 2 reviewed the real diff: `src/devices/dev_wdc.c` (five `#572` sites), the revised detector `regress/wdc_lba_probe.py`
(5e4ecd47 at packet time), the four harness hunks and the measurements under `../detector_20261024/`.  Packet: `packet.md`
(135,076 b, the five hunks inlined), `packet_compact.md`, `packet_packetfed.md` (one question per firing for the packet-fed
seats).  Launcher: the frozen copy `t4/launch_p2.run-*.sh`.

## Roster and verdicts (verified by CONTENT -- verdict line present, no echoed brief, no refusal)

| seat | file | bytes | verdict |
|---|---|---|---|
| GPT-6 Astra (ultra, pointer form, refusal 0) | `codex_t4p2.txt` | see `ls -l` | LAND WITH CHANGES |
| Grok 4.7 (xhigh, plan mode, WORKING tree) | `grok_t4p2.txt` | | LAND WITH CHANGES |
| Gemini 4 Argon through agy (file-reading; exit 0; no cross-seat text) | `argon_agy_t4p2.txt` | | LAND WITH CHANGES |
| GLM 5.3 Q1-2 / Q3-4 (packet-fed) | `ollama_glm_t4p2_Q12.txt` / `_Q34.txt` | | LAND WITH CHANGES x2 |
| DeepSeek v4-pro Q1-2 / Q3-4 (packet-fed) | `ollama_deepseek_t4p2_Q12.txt` / `_Q34.txt` | | LAND WITH CHANGES / READY TO LAND |
| Fable 5.1 | `fable5.HELD.txt` | | HELD (owner ruling 2026-10-21; question recorded) |
| kimi, minimax, Opus review seat | `roster_NOT_FIRED.txt` | | DELIBERATELY NOT FIRED (owner roster 2026-10-23/24) |

**No seat found a product-code defect.**  Every owed change is a record, a contract sentence, or one unmeasured floor leg.

## Findings, consolidated (K-numbers are the F2 packet's), with the disposition and how it was checked

K1  Pre-table per-row kill PREDICTIONS wrong (Astra, Argon, Grok, GLM).  CHECKED against `raw_mut/*.out`: each named row's
    red/green under each named variant was read from the log, not inferred.  L4 -> `PRETABLE.out` keeps the block verbatim
    and carries a dated CORRECTIONS section; the shipped contract already followed the applicator's labels; a NOTE on the
    V14 suffix convention added to the contract.
K2  Clause (b) at the readback site unmeasured (Astra): the V17 built dropped only reserved bit 5.  MEASURED after pass 2:
    V17v (the verbatim pre-#572 composition over the new decode) on the kill-table instrument fc878c42, GATE vs FIX ->
    30/33 CONTROL=FAIL, KILLED by the three readback rows (`SCORES_V17v.txt`, `raw_mut/V17v.out`).  Added to CATCHES.
K3  Further single-edit variants no row sees (Astra, Argon, GLM, Grok, DeepSeek): the head mask narrowed; a sector-count
    qualification; a shift of 23; a joint cylinder/sector cell.  DISCLOSED under clause (e) in the contract's BLIND list.
    Not rowed: the arm's body tests none of `head`, `sector`, `cyl`, so their body-induced partition is EMPTY -- coverage
    debt above the floor.  CORRECTED per Astra's F2 (K3): a row on THIS image could see a narrowed head mask, which redirects
    an out-of-image head address into the backed image, so no larger image is needed for that cell; GLM drew that distinction
    and recommended disclosure because a row re-md5s the instrument.  `wdclbaimage` carries the cyl_hi cells only.
K4  The wiring MANIFEST text "differs only in its module docstring" FALSE (Astra, Argon, Grok): the shipped probe differs
    from the instrument in the `id geo` predicate (8 executable lines, `rev_equivalence.txt`).  L4 -> the hunk regenerated
    from HEAD's file with the predicate change and the (a)/(b) transfer stated; dry-applies, compiles.
K5  "Every want is a literal" overclaims (Astra).  Docstring corrected: literal or derived at run time from the IDENTIFY
    geometry, so a dead or wrong geometry read fails those rows.
K6  Words 60-61 claim (DeepSeek, GLM).  TRUE of the tree (`dev_wdc.c` stores `total_size / 512` into words 57-58 and
    60-61); the CHANGELOG cites the lines; no row owed (existing code, not a consequence of the fix).
K7  `wdclbaadvertise` cited before it exists (Grok, GLM).  The three rows land in the same commit (`ledger_ops_pass1.json`).
K8  `RESULTS_fix.txt` is a two-leg run dated 19:02:13 (Grok, GLM, Argon).  Records say so -- CORRECTED per both F2 adjudicators:
    the first wording "19:02-19:04" glued that file's start to `twoleg/RESULTS.txt`'s 19:04:46 (the revised detector's run);
    the records now say "dated 19:02:13".
K9  The gate-10 shell block unexecuted (Astra, Grok, GLM).  RUN after pass 2 as the gate will be committed: HEAD's
    `gate_sh_rounding.sh` + this round's hunk (an LF copy, md5 3f932e0f, 1779 lines), `PMAX` = the fix clone's binary
    (its `dev_wdc.c` cmp CLEAN vs SEC; provenance MEASURED in `CLONE_PROVENANCE.txt`: 496 of 505 tracked src files identical
    to HEAD plus this round's `dev_wdc.c`, the PowerPC decoder at its pre-#571 revision, the pmax layout's six declared
    divergence paths and two generated .index files -- nothing on the wdc/piix4/malta path differs from HEAD), no build tree
    touched -- RESULT (`GATE10_RUN.txt`, 2026-10-24
    23:24 -> 2026-10-25 00:57, 93 minutes; `gate10_wdc_lba.log`): the block's five checks ALL OK (result parses; control OK;
    rows run 33; rows correct 33; sentinel 1; the probe log 33/33 CONTROL=OK); the gate's own verdict FAIL 1 of 405, the one
    red being `gdrom_default rows run got=62 want=60` -- the WORKING TREE's `gdrom_default_probe.py` carries the peer
    session's uncommitted two extra rows against HEAD's pin of 60; not this round's file.  The FIRST attempt (21:55) died in 2 s: the copy had been written CRLF by `git apply`
    OUTSIDE the repo, where the SYSTEM `core.autocrlf=true` applies (HEAD's blob and the WT are LF, 0 CR bytes); the
    landing script shared the recipe and now pins `-c core.autocrlf=false` and refuses a copy whose CR count differs
    from HEAD's.  (An apparatus error of mine on the way: `grep -c $'\r$'` degenerated to a match-everything pattern
    and "found" every committed gate script CRLF; `tr -cd '\r' | wc -c` refuted it -- 0 bytes in every one.)
K10 Build report name and hunk count (Astra).  `BUILD_REPORT_mainloop.md`, written by the main loop from the artifacts;
    the builder sub-agent never delivered its own and was stopped at 21:5x while about to regenerate the hunks.
K11 "nothing resets the phase" comment vs `wdc_new_command_reset()` (Astra).  VERIFIED (`dev_wdc.c:1662` vs `:917`);
    pre-existing, outside this diff; noted for the next ATAPI round, not edited here.
K12 The frozen witness's `neg appar` row reads "got 1 want 0 ok" (DeepSeek, GLM).  The artifact is immutable; the
    CHANGELOG says the 19/19 includes that self-test row and the shipped detector dropped it from the score.
K13 `chs c1`'s named channel never built (GLM).  Pre-table corrections name the measured killers (V1/V2/V13r); the CHS
    formula is a must-not-change site, not a fix predicate.
K14 The `#405` sentence, the `&& !d->lba` records with before/after semantics, and the no-claims list (all seats).  The
    CHANGELOG draft carries each.

## Measurements added after pass 2 (`../detector_20261024/`)

* V17v: 30/33 CONTROL=FAIL -> KILLED (`SCORES_V17v.txt`).
* The shipped probe is REVISION 96e5fbc5 (840 lines; the docstring's BLIND list, the V14 note, the V17v CATCHES line and the
  "every want" sentence).  `final_96e5fbc5/ast_equivalence.txt`: its AST with the module docstring excluded differs from
  the kill-table instrument ONLY in the `id geo` predicate and that function's docstring legend -- the same 8-line change
  `rev_equivalence.txt` recorded for 5e4ecd47, so 96e5fbc5 and 5e4ecd47 differ only in the module docstring (5e4ecd47's
  bytes were not preserved; the equivalence is transitive through the instrument).  Its own runs: GATE vs FIX 33/33
  CONTROL=OK (`RESULTS_gate.txt`), two-leg base 33/33 vs HEAD / fix 33/33 vs FIX (`RESULTS_twoleg.txt`), 21:44-21:50.
* Gate 10 end to end (K9): the five `wdc_lba` checks OK, 33/33 CONTROL=OK, sentinel once; the gate's verdict FAIL 1 of 405 on
  the peer's uncommitted GD-ROM probe rows vs HEAD's pin (`GATE10_RUN.txt`, `gate10_wdc_lba.log`).

## Disputes (each side in its own words; ruled here, re-asked in F2)

D1  Row or disclose the head-nibble cell (K3).  Astra and Argon name the variant without a disposition; GLM: "Since adding a
    row re-md5s the probe, disclose the cell alongside V7 instead."  RULED: disclose (empty partition; larger image owed;
    `wdclbaimage` carries it).
D2  Are the pre-table's wrong predictions a defect of the shipped detector?  Astra: "Preserve the historical predictions and
    append explicit corrections.  The measured kills remain valid"; Grok: "an artifact, not a shipped record."  RULED: L4,
    corrected in place; the detector's code unchanged.

## F2 adjudication

TWO FIRINGS, and the first one's texts are LOST -- an apparatus error of the main loop, recorded here rather than hidden.
(1) 21:50:56-22:00:25, a detached `nohup` launch on the packet BEFORE the gate-10 result: `launch_adj2.log` records both seats
answering CONFIRM WITH CHANGES (codex 4,430 b, grok 8,739 b, grok exit 0).  A 2-second check at 21:49 found neither the pointer
file nor the log and declared the launch dead (it had started 90 s later); the answers were never read.  (2) 00:58, the re-fire
on the UPDATED packet (K9's result, section 2, Q3) through the harness: it OVERWROTE the first firing's answer files.  The
surviving answers are the second firing's; the first grok answer's content cannot be recovered.
Astra (`codex_t4adj2.txt`, 4,305 b, refusal 0): ADJUDICATION: CONFIRM WITH CHANGES; WRONG DISPOSITIONS: K3, K4, K8 -- K3's
rationale (a larger image is NOT needed to see a narrowed head mask; corrected above and in the packet), K4's regenerated wiring
text (it said every preserved reading was (16, 63); the dead run's (None, None) is the exception, both predicates reject it --
the hunk regenerated 01:2x), K8 (BUILD_REPORT :46 still said "19:04" -- corrected to the two-leg 19:02-19:04).  D1 and D2
UPHELD; Q3 READY after the record corrections and the same-commit filings; K9 an ADEQUATE discharge provided the records keep
the 1/405 FAIL distinction and the `PMAX` override and claim neither a whole-gate PASS nor validation of the default build
binary -- and describe the clone's provenance as REPORTED unless established: it is now MEASURED (`CLONE_PROVENANCE.txt`).
Grok (`grok_t4adj2.txt`, 9,877 b, exit 0): ADJUDICATION: CONFIRM WITH CHANGES; WRONG DISPOSITIONS: K1, K8, K11.  Every
disposition re-read against the raw mutant logs by file and line.  K1: the CORRECTIONS section's own text named `lba h1` as a
V1/V2 killer; the logs' red row is `lba h1 ctl` (verified: `lba h1` ok, `lba h1 ctl` FAIL in V1.out, V2.out, V13r.out) --
PRETABLE.out amended 01:4x with a dated sub-correction quoting the wrong sentence.  K8: "19:02-19:04" glued RESULTS_fix.txt's
19:02:13 to twoleg/RESULTS.txt's 19:04:46, a different file -- every record now says "dated 19:02:13".  K11: the "noted in the
dated section" half had not been done -- one sentence added to the OUTSTANDING_BUGS section.  Also taken from its Q1/Q3: the
CHANGELOG draft's witness-era anchor sentence replaced by the measured T_m1/T_p1 row lists (seven rows each; verified against
raw_mut/T_m1.out and T_p1.out); the `neg appar` row's pass predicate (`got != want` on constants 1 and 0) stated where the draft
said only "could not fail"; the applicator's manifest text corrected -- V17v was applied by a separate one-edit script, now
preserved as `run_v17v.sh.txt`, not by `mutants572.py`; an apply-and-compile receipt for the four hunks added
(`HUNKS_APPLY_RECEIPT.txt`, since "dry-applied clean" had no log); the wiring hunk's count re-stated at each regeneration.
D1 disclose and D2 L4-in-place UPHELD (GLM's own example shows a narrowed `& 7` is distinguishable on this image: select 0x48,
cylinder 0, sector 5 -- the fix reads zeros past EOF, the narrowed mask serves tag 5).  Q3: no product change, no new row, no
kill-table re-run; K9 adequate with the gate's FAIL 1 of 405 kept in every record.
BOTH: CONFIRM WITH CHANGES, all changes applied before the landing; the chain closes on this pass with zero floor breaches
raised over the fix diff, the detector revision and the four hunks (the denominator: K1-K14 and D1-D2 as enumerated above).
