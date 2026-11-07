# Reading task: oldrec586 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC586-e92a` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #586 qhmutcrashscore (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 1-80 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
    1| # `#586` Records (follow-up, 2026-11-07): `qhmutcrashscore` names its landing commit `d2a6f233`; the committed-tree proofs; the pass-2 receipt
    2| 
    3| `git ls-tree d2a6f233`, md5s hashed from the committed bytes: `regress/selftest_mutation.sh` blob `d353556fdb61`, md5 `abf7b2c7c34d`; `tools/pipeline/check_probe_wiring.py` blob `4042856eb49b`, md5 `0975ad6bd4ee`; the 80 committed files under `regress/artifacts/qhmutcrashscore/`, their md5s hashed in path order, `57fad10e7370`.  The working copy against each: selftest_mutation.sh the same; check_probe_wiring.py differs in 2 hunk(s) (other sessions' uncommitted edits).  `qhmutcrashscore`'s `commits` field and `killdrivercrash`'s (the class's live member shipped in it; the row stays held for the owner's decision, on the Mythos route) name `d2a6f233`.  The `regress/pass2_ledger.tsv` receipt line for `d2a6f233`, the Landed line in OUTSTANDING_BUGS.md's `#586` section and `matrix.html` re-rendered complete this records commit.
    4| 
    5| **One note on the in-situ run (`regress/artifacts/qhmutcrashscore/landing_20261105/INSITU_G3.out`), recorded because the kit asked for the machine alone.**  The landing window paused the session's Gemini-web senders first; the stop-wait timed out with three of the four stopped, so one network-bound send overlapped the run's first ~90 seconds.  Leg H took 704 s and leg S 709 s, consistent with each other, and the summary is PASS with `build/`'s inputs unchanged.
    6| 
    7| # `#586` (2026-11-07) -- `qhmutcrashscore`: gate 3 no longer scores a mutant run that never printed its verdict as a detection; such a run prints NOLOG and its check reds
    8| 
    9| **The defect.**  `regress/selftest_mutation.sh` (gate 3) proves that gate 2's float_emul differential can fail: it builds
   10| `regress/diff_ieee_store.c` against seven mutants of `src/core/float_emul.c` and requires each run to report a failure.
   11| `build_and_run()` ran each binary and printed `grep -c 'DIFF_PASS'` of its output, and a mutant's check wants `0`.  So a
   12| run that crashed, called `exit(1)` or printed nothing counted zero DIFF_PASS lines and passed as `DETECTED (must fail)`
   13| without ever reaching its verdict -- the harness's own rule ("A crash is a FAULT, never a detection", `tools/README.md`)
   14| broken by the gate that proves gate 2 can fail.  Filed as task #55 in OUTSTANDING_BUGS.md's 2026-08-12 #376 residuals,
   15| and by `#555` as `qhmutcrashscore`, a member of the class row `idlesslow`; promoted to its own row by this round.  No
   16| guest path: the subject is the test apparatus, so the witness is `harness:`.
   17| 
   18| **The witness** (the killdrivercrash research, 2026-11-05, preserved as `regress/artifacts/qhmutcrashscore/wkdc_20261105/RECEIPT.txt`).  HEAD's gate 3 and `lib.sh`
   19| (md5 `00ab9a20`, `63b3aa8c`) ran whole in a fake ROOT with a STUB in place of `diff_ieee_store.c`
   20| (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/stub_diff_ieee_store.c`; driver `regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/w2_gate3.sh`).  With all seven mutants raising SIGFPE before
   21| any output the gate printed `selftest-float-emul-can-fail: PASS (15 checks)` (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_HEAD.allcrash.log`);
   22| on a mixed set it scored two SIGFPE endings, an `exit(1)` and an empty log `DETECTED (must fail)` and failed only the
   23| genuine survivor (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_HEAD.mixed.log`).
   24| 
   25| **The fix** (`regress/selftest_mutation.sh`, `build_and_run()` only, +11 -1).  The run's status is kept in `rc`,
   26| and before the count the function requires a line beginning `DIFF_PASS` or `DIFF_FAIL` -- the differential's verdict,
   27| its last line -- else it prints `NOLOG rc=<status>`.  `NOLOG ...` equals neither the control's want (`1`) nor a
   28| mutant's (`0`), so that check reds.  The gate's fifteen checks, their names and its output on completed runs are
   29| unchanged; a run whose log carries its verdict line is scored by that verdict whatever its exit status.  The committed file differs from the
   30| copy the controls ran (md5 `84a0ea37`, `regress/artifacts/qhmutcrashscore/wkdc_20261105/fix/selftest_mutation.diff`) in full-line comments only: the comment is
   31| re-worded and tagged and names the stub log and the row filed for hangs (`regress/artifacts/qhmutcrashscore/landing_20261105/STAGED_DIFF.txt`).
   32| `tools/pipeline/check_probe_wiring.py` gains MANIFEST entries for the 7 preserved scripts.
   33| 
   34| **Controls** (`regress/artifacts/qhmutcrashscore/wkdc_20261105/controls/CONTROLS.txt`: "CONTROLS: 33 of 33 rows as expected"; the expectations are written in
   35| `regress/artifacts/qhmutcrashscore/wkdc_20261105/controls/compare.py`, before the logs were read).  Refused by the fix and scored by HEAD: all-crash, HEAD PASS (15
   36| checks) against the fix's FAIL (7 of 15 checks), every mutant `NOLOG rc=136` (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.allcrash.log`);
   37| mixed, HEAD FAIL (1 of 15 checks) against FAIL (5 of 15 checks), its four dead runs `NOLOG` with rc 136, 136, 1 and 0
   38| (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.mixed.log`).  Unchanged, byte-identical to HEAD: every genuine kill and survivor line, the whole
   39| gate output with every mutant a genuine kill (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.allkill.log`), and the whole gate output on HEAD's
   40| REAL `diff_ieee_store.c` and `float_emul.c` with its seven real mutants -- PASS (15 checks) under both, each real
   41| mutant's log ending `DIFF_FAIL` and the control's `DIFF_PASS` (`regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.real.log`).  In situ at the landing, alone on the machine, on the real `build/` tree (`regress/artifacts/qhmutcrashscore/landing_20261105/INSITU_G3.out`): HEAD's gate and the committed gate printed the same whole output, PASS (15 checks), every mutant's log ending `DIFF_FAIL` and the control's `DIFF_PASS` (its last non-blank line); the committed gate with the all-crash stub printed FAIL (7 of 15 checks), every mutant `NOLOG rc=136`, and with the all-kill stub PASS (15 checks).  The script (`regress/artifacts/qhmutcrashscore/landing_20261105/insitu_gate3.sh`, committed beside its log) also required the crash leg's control row `ok 1` and `build/`'s input md5s unchanged.
   42| 
   43| **Floor.**  Two objects: (a), (b) and (d) grade the W2 CONTROLS, the detector defending this fix, against defective gates; (c) is given for the controls and for gate 3 itself, a detector in its own right.  (a) the pre-fix gate PASSes with every mutant crashed (the witness); (b) HEAD's `build_and_run()` is the
   44| verbatim reinstatement, and it is the HEAD leg of every control -- and it is measured too: the null repair (Floor (d) below) prints HEAD's gate output line for line on all three stub sets -- only the header naming the script, the shell's crash reports (process ids, driver path) and the done tag differ (`regress/artifacts/qhmutcrashscore/landing_20261105/pass2/q2/g3/W2_M_q2b.allcrash.log`, `regress/artifacts/qhmutcrashscore/landing_20261105/pass2/q2/g3/W2_M_q2b.mixed.log`, `regress/artifacts/qhmutcrashscore/landing_20261105/pass2/q2/g3/W2_M_q2b.allkill.log`); (c) for GATE 3 as a detector -- (c): measured at `regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.allcrash.log` and `regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/g3/W2_FIX.mixed.log`: the null medium for a gate that runs a detector is a detector that never answers -- the all-crash stub, and the mixed set's empty log -- and the fixed gate reds every such run, each reading NOLOG; the all-crash stub is (a)'s witness and gate 3's (c) medium at once, and legitimately: the defect was gate 3 reading the null medium green, so the pre-fix GATE is (a)'s object and the stub is the medium the fixed gate must red.  (c) for the W2 CONTROLS, the detector defending this fix -- (c): by construction via `regress/artifacts/qhmutcrashscore/wkdc_20261105/controls/compare.py:100-103`, leg not run (the null gate): a row whose line is not found reds (`:100-101`), and the allkill/real SAME rows red when FIX's text is empty against HEAD's non-empty text (`:103`).  The construction holds against a LIVE HEAD leg: with both legs dead the allkill/real rows pass (`"" == ""`), the `all([])` shape;
   45| (d) MEASURED, on pass 2's Q2: the seat's smallest breaking edit, `|| echo 0` in place of the NOLOG return, and the null repair `|| { echo 0; return; }` -- the guard kept, its effect nulled -- each ran through the research's own W2 control driver on the all-crash, mixed and all-kill stubs (`regress/artifacts/qhmutcrashscore/landing_20261105/pass2/q2/Q2_CONTROLS.txt`; the staged gate reds 0 of the 19 control rows there).  `|| echo 0` reds 11 -- it falls through to the count, so a dead run prints `0` twice and its check fails, while the gate's verdict stays FAIL (7 of 15 checks), so the per-row NOLOG expectations are what catch it, not the verdict -- and the null repair reds 13, its all-crash gate back to PASS (15 checks).  Neither escapes, so no control row was added; (e) the CONTRACT: the guard pins a run that
   46| ends without a verdict line.  It does not pin a hang (no time bound: filed as `gate3runbound`), a verdict printed and
   47| then followed by a crash (scored by its verdict, as designed), or its own presence -- no standing control fails if the
   48| guard is deleted; re-running `regress/artifacts/qhmutcrashscore/wkdc_20261105/witness/w2_gate3.sh` on the committed file is the check (filed as `g3nologselfpin`).
   49| 
   50| **Review (pass 2).**  Gemini 4 Argon, web route, packet-fed, on the brief as sent (`regress/artifacts/qhmutcrashscore/landing_20261105/BRIEF_PASS2.md`, wrapped by the gweb reading task: `regress/artifacts/qhmutcrashscore/landing_20261105/pass2/gemini_web.packet.md`), answered `GWEBKDCP2: 9 ATTACKS 0 BROKEN 8 HOLDS 1 UNSETTLED DRAFTABLE:YES` (`regress/artifacts/qhmutcrashscore/landing_20261105/pass2/argon_kdc_p2.txt`).  Its one UNSETTLED point, P1 -- that the differential prints nothing but its verdict that `^DIFF_(PASS|FAIL)` could match -- is settled by grep at HEAD: `regress/diff_ieee_store.c`'s only `DIFF_` tokens are its lines 1307 and 1309, the final verdict's two printf calls, and `src/core/float_emul.c` has none.  Its Q2 edit, `|| echo 0` in place of the NOLOG return, was claimed to keep the completed sets (`allkill`, `real`) green -- true, measured -- and to score dead runs as detections -- measured false: the edit falls through and prints `0` twice, and 11 of the 19 control rows red (Floor (d) above).  Its Q3 member, requiring exit status 0 beside the verdict, was considered and not adopted: a verdict printed and then followed by a teardown crash is still the run's verdict, which its own P4 table scores as intended.  P2 to P6 and the three Q4 records it found true.  The dispositions are the coordinator's of 2026-11-06; the flagship's ruling on them is the regress review.
   51| 
   52| **Regress review** (the Fable-only stage, before the landing).  Fable 5.1, read-only, on the reviewed unit and the preserved logs (`regress/artifacts/qhmutcrashscore/regress_20261106/RULING.md`, answering the queued question `regress/artifacts/qhmutcrashscore/regress_20261106/FABLE_QUEUE_item7.md`): `FABLEREGKDC: 16 CHECKS 0 FLOOR-BREACHES 1 RECORD-NIT(commit.msg five->seven, pre-FINAL) 1 DEBT-TO-FILE(g3 guard self-pin, LOW) INSITU:OWED-BY-STEP-4 VERDICT:LAND` -- `QHMUTREG: 5 RIGHT 0 WRONG; VERDICT discharge -- owe: commit.msg count (pre-FINAL, one word); INSITU_G3.out by the kit's step 4; filed debt g3nologselfpin (LOW)`.  Of its sixteen checks fourteen read TRUE; the other two were the commit message, which said five MANIFEST entries where the block adds seven (corrected before this commit: the count is now derived from the block), and the in-situ log, which the kit's step 4 produces and the final build requires.  Floor: no breach, and (b) measured as well as by construction (above).  Its question (2): accepting the verdict line anywhere in the log is right for this differential, whose only `DIFF_` lines are its final verdict's two printf calls, followed by `return 0`; the difference from the proposed helper's last-line rule is a design inconsistency, not a false pass, carried as a note in `killdrivercrash`'s question.  (3): the guard has no standing control -- debt, filed LOW as `g3nologselfpin`.  (4): every pass-2 disposition right in substance, with one more reason for Q3: requiring exit status 0 would turn an honest `DIFF_FAIL` that exits nonzero into NOLOG, a false red.  (5): the records true, with the one correction.  Two confirming reviews of the ruling -- GPT-6 Astra's (`regress/artifacts/qhmutcrashscore/regress_20261106/reviews/codex_ASTRACONF_KDC.txt`); Grok 4.7's (`regress/artifacts/qhmutcrashscore/regress_20261106/reviews/grok_KDC.txt`) -- found its prose looser than its checks, and Fable 5.1's adjudication of them (`regress/artifacts/qhmutcrashscore/regress_20261106/ADJ_KDC.md`, answering `regress/artifacts/qhmutcrashscore/regress_20261106/ADJ_KDC.brief.txt`) reads `FABLEADJ_KDC: 10 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS`: all ten points accepted, no floor breach, no code or detector repair, every repair a wrong record corrected in place.  The ruling's eight corrections are in `regress/artifacts/qhmutcrashscore/regress_20261106/RULING_ERRATA.md`, beside it -- the ruling stays the seat's bytes -- each quoting the sentence it refutes; among them, Argon's Q2 claim was two claims (the completed sets stay green, true; dead runs score as detections, false), the in-situ sentence claimed more than the script checked and less, MEASURED was stamped on four cells of (d) that were only read, and floor (c) graded one object where its siblings graded another.  The unit's four were made before this commit: the Review paragraph above, the in-situ script and sentence (the script now tests each run log's last non-blank line), floor (c) on both objects (above), and `g3nologselfpin`'s pin sentence.
   53| 
   54| **The class.**  `killdrivercrash` is the class: drivers that score a run by counting lines or comparing extracted
   55| tokens score a run that died by how far it got.  The research's census (`regress/artifacts/qhmutcrashscore/wkdc_20261105/census/AFFECTED.tsv`) names 20 affected
   56| drivers -- this gate, fixed here, and 19 frozen records under `regress/artifacts/`: the 2026-08-27 wdc compile-and-count
   57| family (nine drivers), killrow5.sh and killrow5c.sh, kill495.sh with its three variants and kill494.sh, and three
   58| others.  They are records of what ran and are not patched; their 89 preserved per-mutant logs all end in their
   59| completion sentinel (`regress/artifacts/qhmutcrashscore/wkdc_20261105/census/RETRO_LOGS.out`), so as far as the preserved logs show no recorded table rests on a
   60| truncated run -- five of the drivers preserved no per-run logs and are not covered by that check.  What stops the NEXT
   61| driver is an OWNER decision, and the row is HELD for it, on the Mythos route: the shared helper
   62| `regress/artifacts/qhmutcrashscore/wkdc_20261105/fix/killscore.sh` (`ks_score`: the log's last non-blank line must be the sentinel, else `NOLOG rc=<status>`;
   63| `regress/artifacts/qhmutcrashscore/wkdc_20261105/controls/ks_unit.out`, 10 of 10) and its trigger -- a brief-template line (`tools/BRIEF_TEMPLATE.md` carries
   64| uncommitted edits and is not committable now) or a precommit check.  Its question also carries the regress review's note on gate 3's anywhere-in-the-log rule against the helper's last-line rule.
   65| 
   66| **Filed** (ledger and OUTSTANDING_BUGS.md's `#586` section): `gate3runbound` (LOW) -- gate 3 runs each differential with
   67| no time bound, so a mutant that hangs wedges the gate and the battery behind it (no false pass, no verdict).  `g3nologselfpin` (LOW, from the regress review) -- the NOLOG guard has no standing control, so deleting it reds no check; the ruling's shape is an eighth gate-3 mutant, a constructor that raises SIGFPE before `main`, whose check wants `NOLOG rc=136`.
   68| 
   69| **Seats.**  One ledger entry per seat in `qhmutcrashscore`'s review stage: 1 answer(s) -- agy (`regress/artifacts/qhmutcrashscore/landing_20261105/pass2/argon_kdc_p2.txt`); the other 8 recorded by name as not fired or seat failures, each with its own reason.  Opus 5.5 built this landing kit, so it is not a review seat for its diff (badge A).  The flagship's regress review and its adjudication are the row's regress entries (above).
   70| 
   71| **Owed:** the owner's decision on `killdrivercrash`, held for the Mythos route.
   72| 
   73| **Of the round's evidence** the commit carries 45 files under `regress/artifacts/qhmutcrashscore/wkdc_20261105/` (`regress/artifacts/qhmutcrashscore/wkdc_20261105/MD5SUMS.txt`: each file's md5 and the
   74| scratch file it was copied from), byte copies of the research directory `_scratchpad/wkdc/` except the receipt
   75| (`regress/artifacts/qhmutcrashscore/wkdc_20261105/RECEIPT.txt`), which gains a header saying what was and was not preserved.  Under `regress/artifacts/qhmutcrashscore/landing_20261105/pass2/` it carries the pass-2 seat's banked files (4: the answer, the packet it saw, its argv and verdict), and under `pass2/q2/` the Q2 measurement (19 files: the two mutants, the driver copy and its one-line difference, the nine leg logs, the comparator and its output).  Under `regress/artifacts/qhmutcrashscore/regress_20261106/` it carries the regress review (seven files: the ruling and the question it answered).
   76| 
   77| **Landing.**  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>`
   78| headings: `citeprefixblind`, filed by `#554`).  Every citation in it is a full repository path, and its own resolver,
   79| run over the block in the pretest clone, resolves each to this commit's files (`regress/artifacts/qhmutcrashscore/landing_20261105/CITE.txt`).
   80| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_586: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC586: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
