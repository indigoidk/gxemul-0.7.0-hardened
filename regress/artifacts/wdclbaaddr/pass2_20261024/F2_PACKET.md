# T4 `wdclbaaddr` (-> #572) -- PASS-2 F2 ADJUDICATION PACKET (the panel shares its findings), 2026-10-24 21:5x, main loop 087a90

PROJECT FRAMING.  GXemul is a computer-architecture emulator; this fork is a software-correctness hardening effort on the
emulator's own C device models.  This round corrects a DECODE defect in the IDE/ATA disk model (`src/devices/dev_wdc.c`): an
LBA-mode request was served from the cylinder/head/sector reading of the same taskfile bytes.  Ordinary device-model
correctness review.  Tree: `GXEMUL-SEC/` at HEAD cc1f69cc with the working-tree diff of `dev_wdc.c` (the fix) applied.

YOU ARE ADJUDICATING THE PASS-2 FINDINGS, NOT RE-REVIEWING THE DIFF.  Seven answers on the shipped diff are in this directory:
`codex_t4p2.txt` (Astra), `grok_t4p2.txt`, `argon_agy_t4p2.txt`, `ollama_glm_t4p2_Q12.txt`/`_Q34.txt`, `ollama_deepseek_t4p2_Q12.txt`/
`_Q34.txt`; the packet they answered is `packet.md`.  Verdicts: six LAND WITH CHANGES, DeepSeek Q3-4 READY TO LAND; NO seat found a
product-code defect; every owed change is to records, the detector's documentation, or one unmeasured floor leg -- all now done
and listed below with their artifacts.  Open the files; do not build or run anything.

VERDICT LINE FIRST: `ADJUDICATION: CONFIRM | CONFIRM WITH CHANGES | REJECT`, then `WRONG DISPOSITIONS: <ids or none>`, then the
numbered answers.  Mark each claim READ / DERIVED / NOT CHECKABLE.

## 1. The findings, consolidated (K-numbered), each with the main loop's DISPOSITION

K1  PRE-TABLE PER-ROW KILL PREDICTIONS WRONG (Astra Q2 :15-29; Argon Q2 :46-51; Grok Q2 :28-29; GLM Q12 :19-23): `lba 70` is
    GREEN under V1/V2/V3/V13r (0xe0 keeps the flag set under every decode); the applicator's V14r/V14w suffixes are inverted
    relative to the pre-table text (V14w = READ arm disabled); "lba wr h1 kills V8w" wrong (h1s5 does; lba wr h1 kills V4w);
    "lba wr256b kills V11w" wrong (V11w lands at LBA 255); V8/V15 serve tag 5 at `lba h1`, not 67; no V1w exists; the +1
    translation reds seven rows (lba wr cylhi included).  VERIFIED by the main loop against `raw_mut/*.out`.  DISPOSITION: L4,
    corrected IN PLACE -- `detector_20261024/PRETABLE.out` keeps the pre-table block verbatim and carries a dated CORRECTIONS
    section (appended 21:5x) quoting each wrong prediction with its measured killers.  The shipped contract already followed the
    applicator's labels (Astra :20); a one-line NOTE on the V14 suffix convention was added to the contract.
K2  CLAUSE (b) AT SITE 4 UNMEASURED (Astra Q2 :25-29): V17 only drops reserved bit 5; it is not the verbatim pre-#572 readback
    composition.  DISPOSITION: MEASURED after pass 2 -- V17v (`(d->sdh_resv << 6) + (d->lba << 5) + (d->drive << 4) + d->head` over
    the new decode), single build on the frozen instrument fc878c42, GATE mode vs FIX: **30/33, CONTROL=FAIL, KILLED** by sdh rb
    (0x25 for 0xe5), sdh rb2 (0x13 for 0xb3), sdh rb3 (0x2c for 0x4c) -- `detector_20261024/SCORES_V17v.txt`, `raw_mut/V17v.out`.
    Added to the contract's CATCHES.
K3  A FURTHER SINGLE-EDIT VARIANT NO ROW SEES -- the head mask narrowed to its low bit(s), `& 1` / `& 7` (Astra Q2 :33; Argon Q2
    :53-55; GLM Q12 :25): every LBA-mode command drives head 0 or 1.  Also Grok Q2 :32: `&& d->seccnt != 0` (every command passes
    count 1); DeepSeek Q12 :16: `<< 23` in one arm (covered by the head-shift disclosure); Argon :55: `+ (d->cyl_lo ? 0 :
    d->sector)` (a joint cell the rows never drive).  DISPOSITION: DISCLOSED under clause (e) in the contract's BLIND list (head
    nibble 2..15; sector count 0 and counts above 1; the joint cells of the address fields sampled not exhausted).  Not rowed:
    the DEPENDS-ON closure's body-induced partition of `head`, `sector` and `cyl` is EMPTY (the arm tests none of them), so these
    are coverage debt above the floor.  (CORRECTED 01:2x per Astra's F2 K3: a row on THIS image could see a narrowed head mask --
    it redirects an out-of-image head address into the backed image -- so no larger image is needed for that cell; GLM :25 drew
    that distinction and recommended disclosure because a row re-md5s the instrument.  `wdclbaimage` carries the cyl_hi cells only.)
K4  THE MANIFEST BLURB "differs only in its module docstring" IS FALSE (Astra Q3 :39; Argon Q3 :67-70; Grok Q3 :41): the shipped
    probe differs from the instrument in the `id geo` predicate (8 executable lines).  DISPOSITION: L4 -- `HUNKS_check_probe_
    wiring.py.diff` REGENERATED from HEAD's file (21:4x) with corrected strings for the frozen instrument (the predicate change,
    the (a)/(b) transfer record) and the applicator (tables 1 and 2, the V12/V7 and V17v single builds); dry-applied clean,
    `py_compile` OK.
K5  "EVERY WANT IS A LITERAL" OVERCLAIMS (Astra Q4 :49): wants derived from H/S exist.  DISPOSITION: docstring corrected
    ("literal or derived at run time from the IDENTIFY geometry ... so a dead or wrong geometry read fails those rows").
K6  WORDS 60-61 CLAIM UNWARRANTED IN THE PACKET (DeepSeek Q12 :13; GLM Q34 :19): DISPOSITION: TRUE of the tree -- `dev_wdc.c`
    stores `total_size / 512` into words 57-58 and 60-61 (HEAD :433-442; Grok Q1 :15 READ it at WT :441-445); the CHANGELOG cites
    the lines; no row owed (a statement of existing code, not an observable consequence of the fix).
K7  THE `wdclbaadvertise` CITATION DANGLES UNTIL THE ROW EXISTS (Grok Q3 :47; GLM Q34 :19): DISPOSITION: the row (with
    `wdcmediastatus` and `wdclbaimage`) is FILED IN THIS LANDING -- `ledger_ops_pass1.json` new_rows and the OUTSTANDING_BUGS
    dated section land in the same commit as the comments that cite it.
K8  RESULTS_fix.txt IS A TWO-LEG RUN DATED 19:02:13 (Grok Q2 :30; GLM Q34 :23; Argon :34): DISPOSITION: records say "the frozen
    instrument's two-leg run dated 19:02:13, RESULTS_fix.txt, fix leg 19/19" rather than "19:04".  (CORRECTED 01:4x per both F2
    adjudicators: the "19:02-19:04" span that stood here glued the witness file's start to `twoleg/RESULTS.txt`'s 19:04:46 start,
    a different file; BUILD_REPORT :46 had also still said "19:04".  Both now say "dated 19:02:13".)
K9  THE GATE-10 SHELL BLOCK IS UNEXECUTED (Astra Q3 :41; Grok Q3 :38, :48; GLM Q34 :15): DISPOSITION: RUN END TO END after
    pass 2, as the gate will be committed -- HEAD's `gate_sh_rounding.sh` + this round's +52 hunk (an LF copy built by
    `git -c core.autocrlf=false apply`, md5 3f932e0f, 1779 lines), `PMAX` overridden to the fix clone `/tmp/gxt2/fix/gxemul`
    (its `dev_wdc.c` cmp CLEAN vs SEC, binary newer than source; provenance MEASURED 01:1x in `CLONE_PROVENANCE.txt`, correcting
    the "HEAD sources" wording that stood here: 496 of 505 tracked src files byte-identical to HEAD plus this round's `dev_wdc.c`;
    `cpu_ppc_instr.c` at its pre-#571 revision cb21331c^; the six declared est-divergence paths in the pmax layout; two generated
    .index files -- every file on the wdc/piix4/malta path is HEAD's or this round's), `LOGDIR=/tmp/gxregress_572`; NO build
    tree touched (`build/` carries the peer session's five uncommitted src files).  RESULT (`GATE10_RUN.txt`, 2026-10-24 23:24:20 ->
    2026-10-25 00:57:00, 93 minutes for the whole gate; `gate10_wdc_lba.log` beside it): the #572
    block's five checks ALL OK -- `wdc_lba result parses yes`, `control: identity rows, encodings, breakpoints OK`,
    `rows run 33`, `rows correct 33`, `probe reached its sentinel 1`; the probe log `WDC_LBA_CONTROL=OK WDC_LBA_RESULT=33/33`,
    sentinel once.  The gate's own verdict is `FAIL (1 of 405 checks)`, and the one red is NOT this round's:
    `gdrom_default rows run got=62 want=60` -- the gate runs the WORKING TREE's `gdrom_default_probe.py`, which carries the
    peer session's uncommitted edits adding two rows (its own docstring says 62/62), against HEAD's pin of 60; `#572` touches
    neither.  The first attempt (21:55) died in 2 s on a CRLF copy: `git apply` run OUTSIDE the repo honours the SYSTEM
    `core.autocrlf=true` (the repo's `false` does not reach a temp dir; HEAD's blob and the WT are LF, 0 CR bytes by
    `tr -cd '\r' | wc -c`); the landing script shared that recipe and now pins `-c core.autocrlf=false` and REFUSES a staged
    copy whose CR count differs from HEAD's blob.
K10 BUILD_REPORT NAME AND HUNK COUNT (Astra Q4 :50): DISPOSITION: the report is `BUILD_REPORT_mainloop.md` (written by the main
    loop from the artifacts; the builder sub-agent never delivered its own) and now says +25/regenerated; records cite it by name.
K11 "NOTHING RESETS THE PHASE" COMMENT vs `wdc_new_command_reset()` clearing `atapi_phase` (Astra Q4 :51): VERIFIED --
    `dev_wdc.c:1662` says it, `:917` clears it.  DISPOSITION: a pre-existing stale comment outside this diff; noted in the
    OUTSTANDING_BUGS dated section as a records nit for the next round that touches the ATAPI path; not edited here (R23).
K12 THE FROZEN WITNESS'S `neg appar` ROW READS "got 1 want 0 ok" (DeepSeek Q34 :37; GLM Q34 :23): DISPOSITION: the frozen artifact
    is immutable by design; the CHANGELOG says the 19/19 includes that one negative-mode self-test row, and the shipped detector
    removed it from the score.
K13 `chs c1`'s NAMED CHANNEL WAS NEVER BUILT (GLM Q12 :23): DISPOSITION: amended in the pre-table corrections to the measured
    killers V1/V2/V13r (the CHS formula is a must-not-change site, not a fix predicate).
K14 The `#405` sentence, the `&& !d->lba` records with before/after semantics, no claim of advertised LBA / LBA48 / portable V15
    detection / an executed gate block unless it ran (all seats): DISPOSITION: the CHANGELOG draft carries each.

## 2. Measurements added after pass 2 (all under `regress/artifacts/wdclbaaddr/detector_20261024/`)

* V17v: 30/33 CONTROL=FAIL KILLED (SCORES_V17v.txt).
* The docstring-revised shipped probe is revision 96e5fbc5 (840 lines, 35,862 b): `final_96e5fbc5/ast_equivalence.txt` -- its AST
  with the module docstring excluded differs from the kill-table instrument ONLY in the `id geo` predicate and that function's
  docstring legend, the same 8-line change `rev_equivalence.txt` recorded for 5e4ecd47 (whose bytes were not preserved; the
  equivalence is transitive through the instrument); its own runs `RESULTS_gate.txt` GATE vs FIX 33/33 CONTROL=OK and
  `RESULTS_twoleg.txt` base 33/33 vs HEAD / fix 33/33 vs FIX (21:44-21:50).
* Gate 10 run end to end with the block in place (K9): the five `wdc_lba` checks OK, 33/33 CONTROL=OK, sentinel once; the gate's
  verdict FAIL 1 of 405 on the peer's uncommitted 62-row GD-ROM probe vs HEAD's 60 pin (`GATE10_RUN.txt`, `gate10_wdc_lba.log`).
* Builder sub-agent: STOPPED at 21:5x (it never delivered its report and was about to regenerate the four hunks over the
  corrected ones); the four `HUNKS_*.diff` are the main loop's, each dry-applied to HEAD with its CR count unchanged.

## 3. DISAGREEMENTS between seats (each side in its own words)

D1  Whether the K3 head-nibble cell should be ROWED now or DISCLOSED.  Argon (:54) and Astra (:33) name the variant without a
    disposition; GLM (:25): "Since adding a row re-md5s the probe, disclose the cell alongside V7 instead."  MAIN LOOP: disclose
    (the partition is empty; a new row needs a larger image; `wdclbaimage` carries it).
D2  Whether the pre-table's wrong predictions are a defect of the shipped detector.  Astra (:29): "Preserve the historical
    predictions and append explicit corrections.  The measured kills remain valid"; Grok (:54): "an artifact, not a shipped
    record."  MAIN LOOP: L4 in place (done); the detector ships unchanged in code.

## 4. QUESTIONS

Q1 WHICH OF K1-K14'S DISPOSITIONS IS WRONG?  Name the id and the refuting fact.
Q2 Rule D1 and D2.
Q3 Is the round READY TO LAND -- or does any item above require a product-code change, a new row, or a re-run of the kill
   tables on the docstring-revised probe (the main loop holds that the AST check plus the GATE and two-leg re-runs discharge a
   docstring-only revision, as #571's precedent did)?  Is K9's disposition -- the gate run on the fix CLONE with `PMAX`
   overridden, its one red attributed to the peer's uncommitted probe -- an adequate discharge, or must the records say more?
