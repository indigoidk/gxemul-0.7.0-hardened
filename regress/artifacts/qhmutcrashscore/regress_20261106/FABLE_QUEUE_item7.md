### 7. `qhmutcrashscore` -- the REGRESS review of the gate 3 crash-scoring round (#585 as built; take the round number from the landing commit), held on the row's regress stage

**Fable 5.1, the regress-is-fable-only review of the round as committed, read-only, after its landing.**  The round
changed one function of one harness script, `regress/selftest_mutation.sh`'s `build_and_run()` (+11 -1): a mutant run
whose log has no line beginning `DIFF_PASS` or `DIFF_FAIL` now prints `NOLOG rc=<status>` instead of a zero
DIFF_PASS count, so its check reds instead of scoring `DETECTED (must fail)`.  It also promoted `qhmutcrashscore` out of
`idlesslow` and closed it, held the class row `killdrivercrash` for the owner, and filed `gate3runbound` LOW.  **Inputs**,
all under `regress/artifacts/qhmutcrashscore/`: the diff and its comment-only proof against the measured copy
(`landing_20261105/STAGED_DIFF.txt`); the research's controls, 33 of 33 (`wkdc_20261105/controls/CONTROLS.txt`, its
expectations in `controls/compare.py`) and the gate legs behind them (`wkdc_20261105/witness/g3/W2_{HEAD,FIX}.{allcrash,
mixed,allkill,real}.log` -- HEAD PASS (15 checks) with every mutant crashed, the fix FAIL (7 of 15)); the in-situ run on
the real `build/` tree (`landing_20261105/INSITU_G3.out`, made in the landing window); pass 2 -- Gemini 4 Argon's
answer `GWEBKDCP2: 9 ATTACKS 0 BROKEN 8 HOLDS 1 UNSETTLED DRAFTABLE:YES` (`landing_20261105/pass2/argon_kdc_p2.txt`, on
the packet `pass2/gemini_web.packet.md`) and the coordinator's dispositions, recorded per seat in the row's review stage
(P1 settled by grep: `diff_ieee_store.c`'s only `DIFF_` tokens are its lines 1307 and 1309; Q2's `|| echo 0` MEASURED
to red 11 of 19 control rows and the null repair `|| { echo 0; return; }` 13, `landing_20261105/pass2/q2/Q2_CONTROLS.txt`,
so no row was added; Q3's exit-status-0 member considered and not adopted, because a verdict printed and then followed
by a teardown crash is still the run's verdict); and the records (the round's CHANGELOG block, OUTSTANDING_BUGS.md's
section, the ledger rows `qhmutcrashscore`, `killdrivercrash`, `gate3runbound`).  **The question** (the row's
`hold_question`, verbatim there): (1) do the controls and the in-situ log show what the records say; (2) is accepting the
verdict line ANYWHERE in the log (`grep -q`) right for this differential, where the proposed shared helper
`wkdc_20261105/fix/killscore.sh` requires it LAST -- a run whose log carries `DIFF_FAIL` and then dies scores as a kill;
(3) is the guard's lack of a standing control (nothing fails if it is deleted; `wkdc_20261105/witness/w2_gate3.sh`
re-run on the committed file is the check) debt to file, or adequately carried; (4) is each pass-2 disposition right;
(5) are the records true of what shipped?  Answer with `QHMUTREG: <n> RIGHT <w> WRONG; VERDICT discharge | owe <what>`;
under the late-dissent rule a measured false pass found here is repaired in a follow-up commit (never under this
round's number), a wrong record is corrected in place, and a design dissent is filed as its own row.  The owner's
separate decision on `killdrivercrash` (the shared helper and its trigger) is NOT this item.
