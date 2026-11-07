# Records checks of the six remaining HELD rounds that already carry their fix -- Gemini web, every claim checked, 2026-11-07 04:3x

The ledger at `8d9df658` holds 34 rows in state `held` with a non-empty `commits` field: 34 = 19 already covered + 8 here + 7 not
covered.  Already covered (19): 13 by the CLOSED8 / #450-#531 passes, 5 by the OLDEST3 pass (#569-#573: m88kscaledbyte,
m88kbuserrregs, ppcdsformxo, wdclbaaddr, lecsrmask), and `killdrivercrash`, whose commit is #586's d2a6f233.  Here (8 rows, six
rounds): b1w, wdcrearmzero, wdccdbmidxfer, xscaleinten, ppcrlwimiwidth, ppcrldimimask, ppcgateimageskip, mapledmaaddr.  Packets:
`mk_next4.py` (SNAP=CHANGELOG_8d9df658.md = HEAD; v2 defangs a quoted "read the source", which `mk_gweb_job.py` had refused for
#526).  Runner `run_oldrec6.sh`, one sender.  NOT covered (7 harness rows with commits but no `#NNN` round block): constblind
(af40df5), mrwstore2 (0447c2e), optrow (fd0ddef), smdatefmt (6e36943), nulheredoc (25da404), cxlaunchquotation (7aa2c41f),
dashokclass (dd2d4e01).

| round | row | Gemini (contradictions / uncited / overclaims) | checked result |
|---|---|---|---|
| #424 | b1w | 2 / 6 / 8 | **no wrong record** -- numbers RE-DERIVED at the round's own commit (below) |
| #473 | wdcrearmzero (+ wdcringambig) | 1 / 3 / 2 | **no new wrong record** -- the one real mismatch is already corrected in place (2026-11-02) |
| #477 | wdccdbmidxfer | 1 / 5 / 3 | **no wrong record** -- the 44-vs-45 is time-indexed and the 44 is logged |
| #526 | xscaleinten | 2 / 7 / 3 | **no wrong record** -- every table score verified against SCORES.txt |
| #527 | ppcrlwimiwidth (+ ppcrldimimask, ppcgateimageskip) | 1 / 2 / 2 + a CODE claim | **no wrong record; the code claim is REFUTED by the code** |
| #528 | mapledmaaddr | 2 / 4 / 7 | **no wrong record** |

## #424 (b1w) -- CHANGELOG_8d9df658.md:31553-31615

* "Both are adopted" (:31576) vs "the sum idiom is gone" (:31584) -- MISREADING.  "Both" is the paragraph's own "two invariants and
  four edges" (:31571); the first seat's "27 sum rows left alone" half was overruled two lines earlier (:31575, "the objection was
  about diff size, not correctness").
* "the named survivor mutant itself" (:31603) "ambiguous among 5" -- MISREADING.  Gate 2 at 81506bd (`regress/gate_offline.sh`,
  the `absorb control` block) applies exactly ONE mutant: it deletes the newline clause (`"\n" not in rest[i:] and`), the first
  survivor the block names (:31566).  "fails all three" (:31609) = the three `lands in BODY` rows; the gate's comment there says
  "three today".
* Uncited numbers (pre-dates the 08-23 names-its-log rule; the counts rule audits nothing retroactively) -- RE-DERIVED anyway at
  81506bd from the committed scripts, offline under WSL in the session scratchpad (`b1w_81506bd/rerun.sh`): `selftest_absorb.py`
  "52 rows, 0 failures" / SELFTEST_ABSORB_PASS (:31590, :31613 hold); `absorb_census.py` "ABSORB_CENSUS attempted=22 killed=22
  survived=0 faults=0", "Survivors: none" (:31590 holds); `st.out` carries exactly three `lands in BODY` rows (:31609 holds).
  Not re-run: "131 checks (was 122)" (needs gate 2 with cc at that commit), "685 today", "2,575 parser steps".

## #473 (wdcrearmzero) -- :21471-21600

* "closed by one diff" (:21473) vs "Both ledger rows are `held`, NOT closed" (:21593) -- MISREADING: the defects vs the ledger state,
  a distinction the block draws on purpose.
* The kill table (:21548-21555, x/6 scores, 8 mutants) disagrees with `regress/artifacts/wdcchunking/killtable_20260827/TABLE.txt`
  at HEAD (x/9, 10 mutants, baseline 26 rows).  It is EXACTLY `git show 1f1a02b:.../TABLE.txt` (the round's own commit); d894e35d
  (#474, "plus #473's pass-2 corrections") rewrote TABLE.txt and the seven per-mutant logs IN PLACE.  ALREADY CORRECTED: the
  2026-11-02 bracket at :21558 names d894e35d as the last writer and says the archive was not produced from the final detector.
  `PREFIX_RUN.txt` matches the block's pre-edit table (:21494-21500) line for line (5 FAIL rows, "22 rows, 5 failures").

## #477 (wdccdbmidxfer) -- :20767-20944

* "baseline **45 rows**" (:20819) vs "the detector stays 44 rows 0 failures on both sides" (:20882) -- TIME-INDEXED, not a
  contradiction.  :20882 is the ASAN measurement on the detector BEFORE the `occupancy above 12` row existed, and it is logged:
  `regress/artifacts/wdccdbmidxfer/killtable2_20260827/TABLE.txt:54-55` ("LIVE 44 rows, 0 failures ASAN clean" / ">= 12 44 rows,
  0 failures ASAN heap-buffer-overflow, WRITE size 1").  On the shipped 45-row detector `M7_ge12.out` is "45 rows, 1 failures",
  red on `occupancy above 12 does not dispatch`.  The block's own :20822-20828 records the same 44 -> 45 step for :20819.
* Gemini's seven "changed steps" verdicts are all UNSETTLED-for-want-of-source (packet-fed); no claim to check.

## #526 (xscaleinten) -- :8598-8721

* "isteer can only become non-zero through a write that itself exits" (:8685) vs "the isteer row reads S1, so the WRITE was
  redirected" (:8698) -- MISREADING: :8685 is the SHIPPED code (HEAD `src/cpus/cpu_arm_coproc.c:318-323`: the only writer stores
  `r[rd]` and then `fatal(); exit(1)` if it is non-zero); :8698 is mutant M5, which redirects the crn-0 (inten) arm's write onto
  isteer (`mut_xscale_t2.py`).
* "the two survivors ... measured at 29/29" vs "both confirmed LIVE kills" (:8651-8656) -- MISREADING: LIVE = the mutants' added
  exits are reachable host kills, `opus_pass2_20260912/SCORES.txt` "LIVENESS (proves the survivors are reachable host kills, not
  inert edits)": XM_RD0 r0 DIES / r9 survives; XM_MAGICBIT DIES.
* Numbers vs `regress/artifacts/xscaleinten/killtable{,2,3}_*/SCORES.txt`, all HOLD: table 1 7 legs, M1 23/26, M5 25/26, M_OPCODE2
  19/26, M_NREAD 19/26, M_RD15 25/26, all killed; table 2 10 legs, HEAD 12/29, M5 27/29 (:8697); table 3 12 legs, BASE 30/30,
  HEAD 12/30, every mutant below 30, M_RD0 and M_MAGICBIT 29/30 each failing RD0_ALLONES alone (:8664).

## #527 (ppcrlwimiwidth, ppcrldimimask) -- :8483-8597 (the first send got Gemini's "I encountered an error"; re-sent once)

* **CODE CLAIM, REFUTED: "the rlwimi fix inserts the UNROTATED source into the high word".**  HEAD `src/cpus/cpu_ppc_instr.c`
  `X(rlwimi)`: `tmp` is narrowed at :2623, ROTATED at :2631 (`tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;`), and only then
  written to the high word at :2652-2653 (`if (mb > me) ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);`).  Book I's ROTL32
  duplicates the word, so a wrapping MASK(MB+32, ME+32) -- which covers all of bits 0-31 -- owes the high word exactly the
  rotated word, which is what it gets.  Gemini read the CHANGELOG's compressed "BEFORE the insertion loop" (:8494) as "before the
  rotation".  Corroborated: rung-3 witness fix 28/28 (`ppcrlwimiwidth/witness_fix.out`), codex's 32,768-combination RTL check.
* "29 rows" (:8511) / "28/29" (:8538) vs "27/27" (:8507) and "13/27" (:8521) -- TWO INSTRUMENTS: the 27-row rung-3 witness
  (`ppcrldimimask/witness_committed.out` SCORE 17/27, `witness_fix.out` 27/27; null medium 13/27) and the 29-row shipped detector
  (HEAD `regress/ppc_rldimi_probe.py`: 29 `row(` calls; `ppcrlwimiwidth/killtable3_20260912/probe_rldimi_BASE.raw` 29/29,
  `_D_SKIP_FULL_ROT.raw` 28/29, `_D_ALIAS_REREAD.raw` 28/29).  rlwimi witness committed 14/28, fix 28/28, null 12/28 -- all as written.

## #528 (mapledmaaddr) -- :8326-8482

* "The ORACLE ... was replaced six times" (:8383) vs six table rows (:8388-8393) -- CLOSES: the six rows are the six SWEPT oracles;
  :8395-8398 is the seventh, the shipped one (whole transcript + full disassembly, the post-`quit` EOF cap and exit 0), which
  answers the last row's three sweeps.  Seven oracles, six replacements, "every replacement but the last was swept".
* "7/7 scriptable" (:8443) vs six seats named -- the panel's own record, `regress/artifacts/mapledmaaddr/panel_20260912_131634_
  maplepass2/SEATS.txt`: "SEATS: 7/7 scriptable produced output" = codex, kimi, grok, glm, deepseek, minimax, kimi(sub) (seven
  TRANSPORTS; the kimi CLI and its substitute are one seat), agy DELIBERATELY NOT FIRED.  The block names only seats with findings.
* "seven survivors MEASURED 16/16 by Opus" (:8444) -- `mapledmaaddr/opus_pass2_20260912/OPUS_REPORT.md`: M_ALIGNDECLINE,
  M_ENDECLINE, M_ALIGNEXIT, M_ENEXIT, M_NOPREFIX, M_LENEXIT, M_THIRDREAD, each 16/16.  HOLDS.

## Result

**Six rounds, ten claimed contradictions and one claimed code defect: every one refuted or already corrected; NO new wrong record.**
On held rounds Gemini's packet-fed contradiction claims are, as on the closed rounds, almost always compressed sentences or two
instruments read as one -- each took one artifact to settle.  The seat remains useful as a POINTER (it named every number worth
checking) and is not a verdict.  Nothing here goes into the repo; it is input to each row's owed Fable close pass.

# Addendum, 05:3x -- the seven HELD HARNESS rows (no `#NNN` block; the record is the commit message + any CHANGELOG block)

Packets `mk_harnessrec.py` -> `hrec_<row>/` (ledger row title/state_note head/hold_question, the commit message(s), CHANGELOG
blocks whose header names the row).  **Packet gap, mine: the ledger `hold` field was not inlined** -- constblind's "absent quote"
claim came from that gap.  Gemini: constblind 4/1/3, mrwstore2 0/2/1, optrow 2/2/2, smdatefmt 4/3/3, nulheredoc 0/2/3,
cxlaunchquotation 1/2/1, dashokclass 2/3/5 (contradictions / uncited / overclaims) -- 13 claimed contradictions.

* **constblind** (af40df5) -- all 4 refuted: the hold_question "how many are there NOW" is a LATER question asking for a fresh
  count (consistent with "THERE ARE THIRTEEN NOW"); the quoted "AUDITED: diff_timer was the only one exposed" IS in the row's
  `hold` field, quoted by its 2026-08-20 in-place correction (the packet omitted that field); later-dated notes on a row are
  normal; "voted 5-0" with "Seats: 6 of 7" = six answered, five voted DROP, none against.
* **optrow** (fd0ddef) -- both refuted: "memory_rw IS THE ONLY ONE" (the audit's answer about today's differentials) vs "It
  knows the STACK-WATERMARK idiom only ... would all slip past" (the mechanised check's disclosed scope) -- an answer and a
  limitation, not a contradiction; the four "stack" mentions are PROSE the audit read, and "Comments are stripped before
  matching" is the checker's rule so prose "cannot masquerade as a measurement".
* **smdatefmt** (6e36943) -- refuted, ONE QUALIFIER: "all four malformed forms silently never expired" vs `ieee_store:` "the
  ONE case the old loop handled" -- the old loop (`regress/gate_offline.sh:1038-1043` at 6e36943^) is `case "${_e##*:}" in
  "") ;;` -- an explicit branch that does NOTHING, so "handled" = "had a branch for", and the empty tail did silently never
  expire.  TRUE as written; "handled" is the misleading word (qualifier: "had a do-nothing branch for").  "CURRENTLY FIXED IN
  TREE" holds: HEAD `regress/gate_offline.sh:1272-1277` names the malformed forms (`NO-DATE`, `BAD-DATE:`).
* **cxlaunchquotation** (7aa2c41f) -- refuted: "every real wall and refusal on record is rc 1 with an empty stdout" (codex's
  own exit status; the census `CENSUS_v5.txt`, 440 rc 0 + 34 rc 1) vs "a real coloured refusal read exit 6 unstripped"
  (CHANGELOG:3562 -- the LAUNCHER's classification exit before the ANSI strip) -- two processes' exit codes.
* **dashokclass** (dd2d4e01) -- refuted: "181/181" vs "179 + 2 + 2 = 183" double-counts -- `regress/artifacts/
  dashokclass_20261016/KILLTABLE_v7_staged.txt` carries 179 `killed` lines INCLUDING the two design mutants (d_nonote2
  109/123, d_dfold2 115/123) + 2 recorded equivalent escapes (d_notenone, d_isosearch) = "KILL TABLE: 181/181 as recorded".
  The CHANGELOG's bare "witness `harness:`" names the KIND; the ledger witness is the full `harness:regress/artifacts/
  dashokclass_20261016/RECEIPT_v7_on_staged_v5.txt ...`.
* **mrwstore2, nulheredoc** -- no contradiction claimed; uncited/overclaim items not pursued (pre-08-23 records).

**Result: 13 claimed contradictions, all refuted; one qualifier (smdatefmt's "handled").  With this addendum every HELD row that
carries a commit (34 at 8d9df658) has had a records check.**
