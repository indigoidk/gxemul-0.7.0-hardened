# mvme187memcoob -- test-variant TABLE 5 (repair 5, 206 rows; the consolidated ruling's L-walk), 2026-11-05 ~10:5x-12:2xZ

Driver `../table5_memc.run.sh` (frozen copy of table5_memc.sh, written by the local Mythos 5.1 preparer), WSL scratch clone /tmp/gxmemc6
under a clone-local .MUTANT; restored to GXEMUL-SEC and rebuilt fresh, sentinel cleared (../table5_run.log).  Instrument
`probe206_frozen.py`, cmp-identical to the in-tree probe; `../PRETABLE_5.out` (02:32:32 local) and its machine form PRED_MAP.txt predate
every table output; `check4.out` re-verified the preparer's device model against all 60 table-4 measurements before the variants ran.
Scores: SCORES.txt; tally: TALLY.txt.

* base 206/206 CONTROL=OK SYMPTOM=ABSENT; HEAD 29/206 SYMPTOM=PRESENT; null media /bin/true 27/206, an absent binary 4/206, /bin/false
  5/206 -- each CONTROL=FAIL; every leg as predicted.
* 3,575 variants (112 from table 4 + 3,463 L-walk representatives): PRED=match 3,523, PRED=atleast-ok 56, PRED=MISS 1, build failures 0,
  text-not-found 0.
* The one MISS, `D7_fold`, is DETECTED (175/206, 31 rows red); its carried-forward "at least" set from table 4 included `R7_lines`, which
  stays green under D7 now that repair 5 extended the R7 session (IMPL_NOTE.md: "R7 EXTENDED ... lines stays 2").  A carry-forward
  error in the prediction, not an escape.
* 665 variants score 206/206, and EVERY ONE was predicted green: the representatives of the 517 predicted SURVIVOR groups inside the
  ruling's own denominator (UNFIRED 106, of which 58 in-bound; UNOBSERVED 411) and of the 148 NOCHANGE statements.  So the measurement
  CONFIRMS T5_PREP's finding: the 206 rows do not close the L-walk as the consolidated ruling defined it.  Whether those cells are floor
  cells owed rows, or clause-(e) coverage debt under the 09-04 floor bound, is the question pass 5 and the next ruling must answer.
* Carried into pass 5 BY NAME (from LATE_REPLICATIONS_20261105.md): NB3 -- a `|=`/`^=` keep into chipid/chiprev in the memconf-latch
  arm, controller-gated (predicted and measured a survivor); NB4 -- an `&=` keep under !controller, which PRETABLE_5 classes NOCHANGE,
  so the tally does not report it as a survivor although it passes every row.
