# Records checks of the eight closed rounds #579-#586 -- Gemini web, every claim checked by the main loop, 2026-11-07 02:5x

Line numbers: CHANGELOG.md at HEAD `521d136a` (snapshot `CHANGELOG_521d136a.md`, ranges by `mk_next4.py` with SNAP).  Gemini:
RECBLOCK_579 2/1/2, _580 3/3/3, _581 2/3/1, _582 1/2/2, _583 4/3/4, _584 3/7/2, _585 3/1/1, _586 1/1/1 (contradictions /
uncited / overclaims) -- 19 claimed contradictions.  Checked: 11.  **No confirmed wrong record (the one first confirmed here was
WITHDRAWN 04:4x, below), two qualifiers (#581; #584, settled).**

## Withdrawn 2026-11-07 04:4x -- was "Confirmed (L4)"; my confirmation was wrong, the CHANGELOG is right

* **#585 :186 (HEAD 8d9df658 :196) "every one of the block's 30 checks failed on at least one leg"** -- this note said "the block
  has **29**" from the per-leg "of 29 checks" counts and `INSITU_fbs.out`'s "checks=29 fails=0".  **That read the per-leg count
  as the block's size.**  `fbsdrampair/landing_20261105/DRYRUN_fbs.out:2` says "The block carries 30 check calls; 29 run on a log
  with a verdict", and its PIN COVERAGE table (`:62-92`) lists **30** checks, each with a nonzero fail count -- the 30th,
  "footbridge probe completed", fails on the dead-probe leg alone (`:50`, "synthetic Y1 dead probe (empty log) -> 1 of 1 checks
  failed").  The sentence is TRUE as written.  Nothing to change in the repo.

## Qualify

* **#581 :594 "the in-situ 223-check gate run stays owed at landing"** -- a review-stage clause the landing discharged: the same block
  (:532) records "223 checks, 0 FAIL" at `mvme187memcoob/landing_20261105/INSITU_memc.out`.  Mark it discharged, cite that file.

## Settled 2026-11-07 (was unsettled) -- QUALIFY, not a wrong record

* **#584 :230 (HEAD 8d9df658; :220 in the 116c5aa9 snapshot) "127 exact-text edits ... 126 call sites replaced, 2 rejected"** --
  the numbers CLOSE; "126" counts CALL SITES, not edits.  `apply_fmt.py` (`fmtattr/stage_20261105/`) adds `n` to its count when
  one edit's `old` occurs n times and GCC warned in every copy, and SKIPS (counts nowhere) an edit that repeats one already
  applied to every copy.  `WHY.txt` = 125 lines: 118 single-site edits, 4 edits marked `(x2, GCC warned in every copy)`, and 3
  marked `duplicate of an edit already applied to every copy`; `REJECTS.txt` = 2.  Edits 118 + 4 + 3 + 2 = 127 (= the 127 `"old"`
  keys in `drafts_20261105/gemini/fmt_*/reply.txt`); call sites 118 + 2x4 = 126 (= SUMMARY.txt's "126 edits applied", which is
  itself the misnomer).  Qualifier text: "(four edits covered two copies each and three repeated those; 122 distinct edits)".

## Rejected (each checked)

* #580 :856 gate-16 totals "289 / 293 ... the other 161 checks" -- `mipsprimundec/landing_20261104/gate16_final.out`: 293 = mips_primundec
  132 (122 rows + 3 denominators + 7 block checks) + fbctrl_cmd 132 + fold 17 + fbctrl_port 6 + fbctrl 6; the other blocks are 161.
* #580 / #581 seat entries "kimi 1 ... not fired" -- the review-stage entries for kimi, deepseek and minimax are NOT FIRED records.
* #583 :303 "Six test-variant tables (`table1/` .. `table7/`)" -- the dirs are table1-5 and table7; there is no table6.
* #583 :323-324 "27 BREACHES" vs "3 FLOOR 26 DEBT" -- 27 is Codex's breach count, and its same verdict line carries "2 FALSE RECORDS":
  27 + 2 = 29 = 3 + 26.
* #586 :3 "80 committed files under `regress/artifacts/qhmutcrashscore/`" -- `git ls-tree -r d2a6f233` gives 80 (45 + 28 + 7);
  Gemini summed four groups to 75.

## Not checked (low yield on the pattern above)

#579's two (NULL4 15/83 vs 14/83, which the block itself explains; the stwcx./stdcx. mnemonic naming); #580's "29 of 34 red"; #582's
"all four" (five places listed -- the four-trees convention is est/ + the three build trees); #583/#584 "resolves all N citations"
(the resolver counts enforced-form citations only); #585's answer counts (entries include NOT FIRED records).

# Addendum, 03:1x -- six older closed rounds: #562, #564, #565, #566, #567, #568 (HEAD `8d9df658`, `CHANGELOG_8d9df658.md`)

Gemini: RECBLOCK_562 1/7/8, _564 2/2/2, _565 1/4/1, _566 1/3/2, _567 2/2/2, _568 1/1/2 -- 8 claimed contradictions.  **All eight
were rejected on checking:**

* #562 "the three shared-latch mutants escaped" vs "all four ... red" -- the first is Table 1 (`killtable_20261007/`, the 25-row
  probe); the second is a later table.
* #564 "its sgi_mte block 74/74" vs "3 controls + 68 rows" -- `sgirekills/gate2_564_20261018/gate_arm.out` carries exactly 74 sgi_mte
  check lines (the emitted/green/red counters are the other three).
* #564 "`SGIRE_W_MTE_STIPPLE = 1 << 10`" vs "`1 << 13`" -- the 1 << 10 is a mutant's value (a new bit moved onto a pre-existing
  one); `dev_sgi_re.c:182` at HEAD is `1 << 13`, as the block says.
* #565 Fable "upheld ... 2026-10-16" vs "NOT FIRED -- held by the 2026-10-17 directive" -- two dates, no conflict.
* #566 "six statements corrected (four announce sites and three ISR sites, not six and five; ...)" -- six statements, and the
  parenthesis lists what they now say; it is not a sum.
* #567 "44" mutants vs "48 table-4 logs" -- 44 + the fix + HEAD + two null media; #567's battery-vs-shipped note is a disclosure.
* #568 38 probe rows vs a 45-check gate block -- rows are a subset of a block's checks.

**Across fourteen closed rounds (#562-#586): NO confirmed wrong record (#585's "30 checks" was confirmed here at 02:5x and
WITHDRAWN at 04:4x -- the block does carry 30), two qualifiers (#581; #584, settled 2026-11-07 -- its numbers close, see above),
against 27 claimed contradictions.**  The nine held rounds checked first carried twelve; these later, closed blocks are
markedly cleaner, and on them Gemini's packet-fed contradiction claims are mostly misreadings of compressed sentences.  The seat
is still useful as a pointer -- each claim took one grep to settle -- but not as a verdict.

# Addendum 2, 03:3x -- seven HELD rows that already carry their fix (their flagship close pass is owed): #450 arcbiosubsan,
# #452 sh4tlbda2, #472 b115, #513 sgirekills, #519 sgirandomcolour, #524 armbdt, #531 ip30abortkill

Gemini: RECBLOCK_452 1/2/2, _472 1/3/4, _513 1/4/5, _519 2/2/2, _524 1/6/2, _531 1/6/2 (#450's reply carries the analysis but no
verdict line).  Ranges: the three oldest use the `## R19 (#450)` / `## Round 472 (#472)` header forms (mk_next4.py spans them to
the next header of any level).  **No confirmed wrong record; one candidate qualifier for the close pass:**

* **CANDIDATE (judgement) -- #513's headline "four adversarial passes, three of which found something":** PASS 4 (at the block's
  "**PASS 4** split 3-2 to close") found that only 2 of 11 aliases had a logged kill against the FINAL row -- "Hence the sweep below."
  That is a finding about the evidence; the headline undercounts unless "found something" means a code or detector defect.

Rejected (each checked): #519 "frozen BASE 14/14" vs "M14 ... 19/19" -- `sgirandomcolour/killtable_20260910/` holds two instruments
(`BASE.raw`, and `BASE19.raw` / `M14l_lineardecline_vs19.raw`); #519 "at most four concern position" is consistent with three;
#524 "six of seven scriptable seats" -- agy is one of the seven, Opus is an Agent seat; #531 "FOURTEEN cells to TEN" -- with one
non-ISR announce site, (5+1) x 2 + 2 = 14 and (3+1) x 2 + 2 = 10; #472 "six rows" + "ONE row" vs "53 rows" -- 53 is the whole
differential's run.  Not checked: #450's two (a census comment false-positive; C integer conversion), #452's register-flow reading.
