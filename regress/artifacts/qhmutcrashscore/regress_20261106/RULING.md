# RULING -- qhmutcrashscore (#585 as built), the REGRESS review -- Fable 5.1, 2026-11-06

FABLE_LIVE_20261106_KDC
# CHECKPOINT -- 2026-11-04 17:0x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

**Scope.**  Read-only, pre-landing.  Repo HEAD is `ab39ba0d` (the owner's exemption re-date); the round is NOT yet
committed, so this rules on the unit as the REVIEWED build stages it (`_scratchpad/wkdc/landing/unit/files/`, 88 files)
and on the preserved logs.  Nothing was built or run: every number below was read from an artifact or from `git show`,
and the three comparisons I made myself were `diff`/`cmp` over existing logs.  Reading seat for the floor and the
records; no gate, no panel, no codex.

## The sixteen checks

| # | check | what was read | result |
|---|---|---|---|
| 1 | the base and the bytes | HEAD gate md5 `00ab9a20` (= the measured base); staged `025b60ff`; the controls' copy `84a0ea37`; `STAGED_DIFF.txt`'s comment-only proof.  **Behaviourally too**: the STAGED gate's whole output in the Q2 legs is byte-identical to the measured copy's W2_FIX output on allcrash, mixed and allkill | TRUE |
| 2 | the diff | +11 -1, every hunk inside `build_and_run()`; `local rc=$?` is the statement after the run; the guard precedes `grep -c`; the signature comment names the new outputs | TRUE |
| 3 | why NOLOG reds (P3) | `regress/lib.sh:82` `check()` compares strings: `NOLOG rc=<n>` equals neither `0` nor `1`; the logs show `got=NOLOG rc=136 want=0` | TRUE |
| 4 | the controls | `controls/CONTROLS.txt`: 33 of 33; expectations live in `compare.py` as regexes written before the logs were read; both directions (refused / byte-identical) | TRUE |
| 5 | HEAD's defect | `W2_HEAD.allcrash.log`: `PASS (15 checks)`, all seven mutants rc 136, each log empty; `W2_HEAD.mixed.log`: `FAIL (1 of 15)` -- only the genuine survivor reds, the two SIGFPE, the `exit(1)` and the empty log all read `DETECTED` | TRUE |
| 6 | the fix on the same media | `W2_FIX.allcrash.log`: `FAIL (7 of 15)`, seven `NOLOG rc=136`, control row `ok 1`; `W2_FIX.mixed.log`: `FAIL (5 of 15)`, the four dead runs `NOLOG` rc 136/136/1/0, kill and survivor lines byte-identical to HEAD's | TRUE |
| 7 | nothing else moved | allkill and real: the gate's whole output identical HEAD vs FIX (my `diff`: only the driver-path header and the `W2_GATE3_DONE` tag differ); real: every mutant's log ends `DIFF_FAIL` at rc 0, the control's `DIFF_PASS` | TRUE |
| 8 | P1 settled | `git show HEAD:regress/diff_ieee_store.c \| grep -n DIFF_` -> 1307, 1309 only; the verdict printf is followed by `return 0;` and nothing else; `float_emul.c` has no `DIFF_` token | TRUE |
| 9 | Q2 as measured | `Q2_CONTROLS.txt`: STAGED 0 of 19 red; `M_q2a` (`\|\| echo 0`) 11 red -- it falls through and prints `0` twice, the gate verdict stays `FAIL (7 of 15)`, so the seat's "keeps every leg green" is false; `M_q2b` (`\|\| { echo 0; return; }`) 13 red, allcrash back to `PASS (15 checks)`.  Driver = the research's `w2_gate3.sh` with one output-path line changed (`driver_vs_input.diff`) | TRUE |
| 10 | **(b) is measured, not only by construction** | my `diff`: `M_q2b`'s gate output is byte-identical to HEAD's on allcrash, mixed AND allkill -- the null repair IS the verbatim reinstatement at the only level the controls see, and it reds 13 rows | TRUE (an upgrade of the record's (b), see below) |
| 11 | records: counts and citations | 45 files under `wkdc_20261105/`, 4 banked pass-2 files, 19 under `pass2/q2/` (counted); the `tools/README.md` quote is real (`:58` "A crash is a **FAULT**, never a detection"); `#555` = `c29a5fd3` filed `qhmutcrashscore` in `idlesslow`; member count 94 kept, member line annotated; `killdrivercrash`'s old witness quoted in the new one; OUTSTANDING_BUGS: four in-place annotations + the `#585` section | TRUE |
| 12 | records: the commit message | `commit.msg` says MANIFEST "entries for the **five** scripts preserved with the research"; the staged diff adds **seven** (five under `wkdc_20261105/`, two under `pass2/q2/`); the CHANGELOG says 7 (`{NMAN}`).  Source: `records_wkdc.py:516` hardcodes "five" | RECORD NIT -- correct before the FINAL build |
| 13 | the in-situ log | `landing/INSITU_G3.out` does not exist; step 4 has not run.  The CHANGELOG carries `[IN SITU PENDING ...]`; `build_kit.py` refuses FINAL without a log ending `INSITU_G3_SUMMARY PASS` / `INSITU_G3_DONE`.  The FINAL sentence it will write (`records_wkdc.py:297-302`) asserts exactly what `insitu_gate3.sh` checks: H = S byte-identical and PASS (15), C FAIL (7 of 15) with seven `NOLOG rc=136`, K PASS (15) | OWED by the kit's own step 4; question (1)'s in-situ half is UNANSWERABLE today |
| 14 | (d) beyond Q2 -- the DEPENDS-ON closure | the guard's operands: the regex, the file it reads, `rc`.  Narrow the regex to `^DIFF_PASS` -> every genuine kill reads NOLOG -> the allkill/real byte-identity rows red; to `^DIFF_FAIL` -> the control row reds; move `local rc=$?` below the grep -> `rc=1` against the seven pinned `rc=136` rows; condition the guard on `rc != 0` -> the mixed set's `maskcarry` row (`NOLOG rc=0`) reds.  Every cell lands on an existing row; none owed | TRUE (by reading; the two measured are Q2's) |
| 15 | the seat record | review stage: 1 answer (agy = Argon, packet-fed, transport named) + 8 named non-answers each with its reason = 9; Opus badge A; regress `[HELD AWAITING SEAT: fable5]` with the question in `hold_question` | TRUE |
| 16 | the gate's own comment | names the stub log the commit adds, the hang gap and its row; "verdict line is its last line, so it is the sentinel" describes the differential (true: `:1307/1309` then `return 0`); the code's test is presence, and clause (e) says so | TRUE |

## The floor, (a)-(f), on the shipped detector (the gate's guard, defended by the W2 controls)

* **(a)** fails on the pre-fix build: HEAD's gate reads the all-crash stub `PASS (15 checks)` while the fix reads
  `FAIL (7 of 15)` -- `W2_HEAD.allcrash.log` / `W2_FIX.allcrash.log`.  MEASURED.
* **(b)** verbatim reinstatement: deleting the guard is HEAD; `M_q2b` reproduces HEAD's gate output byte for byte on
  all three stub sets (check 10) and reds 13 of 19 control rows.  MEASURED at `pass2/q2/Q2_CONTROLS.txt` -- the round
  block states (b) as "the HEAD leg of every control", which is by construction; the measured form is available and
  the block may cite it.  Not a wrong record.
* **(c)** null medium: for a gate that runs a detector, a detector that never answers -- the all-crash stub (every
  session dies, the carrier's runtime-probe form) and the mixed set's empty log.  The FIXED gate reds every such run
  (`W2_FIX.allcrash.log`, `W2_FIX.mixed.log` maskcarry `NOLOG rc=0`).  MEASURED.  Note the dual role and why it is
  legitimate here: the carrier says (a)'s medium is never (c)'s, and the all-crash stub serves both -- because this
  round's DEFECT was precisely gate 3 reading the null medium green.  The pre-fix GATE is (a)'s object; the stub is
  the medium the fixed gate must red.  A clause saying so in the block would preempt the objection; not required.
* **(d)** null repair: `M_q2b` (guard kept, effect nulled) 13 red; `M_q2a` (the seat's literal edit) 11 red; the
  rest of the DEPENDS-ON closure lands on existing rows (check 14).  MEASURED.
* **(e)** contract: stated in the block and in the gate comment -- pins a run ending without a verdict line; does
  not pin a hang (`gate3runbound`), a verdict-then-crash (scored by its verdict, by design), or its own presence.
  STATED.
* **(f)** anchor rule: N/A -- no address decode; the oracle is a verdict token, not a cell.

**Floor breaches: 0.**

## Item 7's five questions

**(1) Do the controls and the in-situ log show what the records say?**  The controls: YES, every number the block,
the row and the commit message quote is in the cited log (checks 4-7).  The in-situ log: NOT YET PRODUCED; it is
step 4 of the kit and gates the FINAL build mechanically.  Its claims are pre-checked (check 13).

**(2) Verdict ANYWHERE (`grep -q`) vs killscore.sh's LAST-LINE rule.**  RIGHT for this differential, and the record
discloses it.  Reasoning: the only two `DIFF_` emitters are the final verdict printfs followed by `return 0`; stdout to
a file is fully buffered, so a verdict reaches the log only by a flush -- a death before the flush loses it (NOLOG,
right), a death after it is a TEARDOWN death of a process whose verdict was computed from the complete row set, and
nothing after that printf can change the differential's answer.  The two rules part only when teardown diagnostics
land after the verdict (stderr is merged): ks_score says NOLOG, the gate scores the verdict.  The gate's reading
answers gate 3's question ("can the differential fail?") correctly.  The disagreement is a DESIGN INCONSISTENCY between
the live gate and the proposed shared helper, not a false pass: when the owner decides `killdrivercrash`, gate 3
either adopts the helper or the helper's header records why gate 3 differs.  Carry it as a line in that decision's
question; no new row.

**(3) No standing control fails if the guard is deleted.**  DEBT TO FILE, LOW -- not a floor breach (the floor asks
the detector to fail, which it does; it does not ask that a gate run it) and not a landing blocker.  But the fix's
only defender is a hand-run artifact, and a round removing the guard by accident would not be told.  The shape is
cheap and in-tree: an EIGHTH gate-3 mutant whose expected result is `NOLOG rc=136` -- `mutate()` appends to a copy of
`float_emul.c` a `__attribute__((constructor))` that `raise(SIGFPE)`s before `main`, and the row wants
`NOLOG rc=136`.  One compile and one run (the nine Q2 stub legs took 156 s in all); the check count moves 15 -> 17
and is pinned nowhere (PRETEST), so nothing else reds.  Name it (e.g. `g3nologselfpin`) and let it compose with
`gate3runbound`.  The MANIFEST's CLASS_TOOL classification of the research scripts is defensible (comparators and stub
writers, `.sh` drivers outside R's domain) and is not what this debt is about.

**(4) The pass-2 dispositions.**  All RIGHT.  P1 settled by grep (check 8, re-derived here).  Q2: the seat's literal
edit measured false; its intended mechanism is `M_q2b`, which the coordinator also built and which was caught -- the
right way to treat a sketch.  Q3: not adopting the `rc == 0` member is right, and one more reason belongs beside the
recorded one -- it would convert an honest `DIFF_FAIL` with a nonzero exit into NOLOG, a false red; today every real
mutant exits 0 (`W2_FIX.real.log` ground truth), so the member's only live effect would be on a future differential.
"Neither escapes, so no control row was added" is right under the floor.  Q4's three records TRUE (verified).

**(5) Are the records true of what shipped?**  YES, with one correction owed before the FINAL build: the commit
message's "five scripts" (check 12) -- seven entries are added; "the seven preserved scripts" or "five with the
research and two with the Q2 measurement".  Everything else I could check against a log or `git show` held (checks
1-11, 15-16).  The in-situ sentence is PENDING by design and its claims match what the script measures.

## Owed, in order

1. **Before the FINAL build:** `records_wkdc.py:516` "five" -> seven (one word; the CHANGELOG already says 7).
2. **The kit's own step 4:** `INSITU_G3.out` ending `INSITU_G3_SUMMARY PASS` / `INSITU_G3_DONE`, alone on the
   machine.  On FAIL the kit's own rule governs: do not land.  Land TODAY or re-date the four peer exemptions dated
   2026-11-06 first (PRETEST step 0).
3. **File after landing (LOW):** the guard's self-pin, shape in (3).
4. **Carry into the `killdrivercrash` decision:** the anywhere-vs-last-line note in (2).
5. **Optional wording, no error:** cite `M_q2b`'s byte-identity to HEAD under (b); one clause on the dual medium under (c).

QHMUTREG: 5 RIGHT 0 WRONG; VERDICT discharge -- owe: commit.msg count (pre-FINAL, one word); INSITU_G3.out by the kit's step 4; filed debt g3nologselfpin (LOW)

FABLEREGKDC: 16 CHECKS 0 FLOOR-BREACHES 1 RECORD-NIT(commit.msg five->seven, pre-FINAL) 1 DEBT-TO-FILE(g3 guard self-pin, LOW) INSITU:OWED-BY-STEP-4 VERDICT:LAND
