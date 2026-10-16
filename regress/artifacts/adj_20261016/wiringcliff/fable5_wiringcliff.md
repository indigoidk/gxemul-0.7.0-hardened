FABLE_WIRINGCLIFF_20261016

VERDICT: A (re-date the IP30 line to 2026-10-30 in the `04f3e7c0` form -- the date, a "a re-date is not a discharge" comment, before/after checker outputs preserved -- because B and C are each a measured harness round and not a housekeeping line; and the re-date unblocks ONLY the unit that carries it: five uncommitted GHOST entries in the working-tree checker red section R for the next unit from this tree whatever the date says)

Seat: Fable 5.1, independent (no other answer in this directory was opened).  Tree: `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`,
HEAD e483d931 (2026-10-09 20:53 -0500).  Every number below is READ from the committed text, MEASURED by a run, or marked
REASONED.  Nothing was written to any project tree; the only writes were scratch copies of the checker in my session
scratchpad and run logs under `/tmp`.

----------------------------------------------------------------------------------------------------------------------
## 1.  Q1 -- A, and why not B or C

**A, today, bounded.**  Three reasons, each resting on something read or measured:

1. **The house form for exactly this situation exists and was used seven days ago.**  `04f3e7c0` (2026-10-09, "probe
   wiring: ppc_rldicl_probe.py's gate-wiring exemption came due 2026-10-08 with its gate_ppc.sh block still owed and
   refused every commit -- re-dated to 2026-10-22 by owner ruling, in its own commit").  Its checker hunk is the date
   `2026-10-08 -> 2026-10-22` plus two comment lines ending *"A re-date is not a discharge."*; the reason tuple is
   UNCHANGED; a CHANGELOG block; and three preserved outputs in `regress/artifacts/probewiring_redate_20261009/`
   (`before_redate.out`, `after_redate.out`, `precheck_562_sectionR_expired.out`).  READ.  That is option A with its
   records discipline already decided; the coordinator's A should copy it rather than invent a second shape.

2. **B is not a line.**  Wiring into gate 14 owes what `#536` (mk48, hpcmips) and `#548` (fbpending) each paid: the exec
   line, a `check` on the complete `IP30ABORT_RESULT=33/33` line so numerator AND denominator are pinned by equality, a
   `IP30ABORT_DONE` sentinel row (a killed run must not read as a run that produced nothing), a negative control showing the
   new rows red (the frozen 18-row EARLY version `ip30_abort_probe.18row_20260917.frozen.py` reds an equality pin on the
   denominator; a reinstatement-mutant binary reds the rows themselves), the two-part clearance on the build tree, an
   end-to-end gate-14 run that is now 568 s longer, and the standing two-pass panel every harness round runs.  `#536` was
   a full nine-seat round (ledger `wiringcliff` entries [15]-[23]); `#548` shipped as its own commit `f4f601c4`.  None of
   that can precede today's blocked commits.

3. **C is a probe change, so it owes its kill table again at the new poll.**  Clause (b) of the floor -- verbatim
   reinstatement at EVERY fixed site must still red -- means four reinstatement builds and four runs of a 568 s instrument
   (the contract header at `ip30_abort_probe.py:20-31` lists the measured kills it would have to re-earn), plus clause (a)
   on the pre-fix build.  That is the `wiringcliff` round, not today's commit.

*Not an option, agreed:* deleting the line without wiring (section R then refuses every commit), and -- not in the packet,
worth saying -- giving precommit a `--today` override, which would make section R a check that cannot fail.

**What the round decides, and in what order (REASONED, from the probe's own text):** `session()` at `:186-254` costs a
SURVIVING session `settle 2.0 s` (`:216`) + `0.35 s` per debugger command (`:222`) + `spin 2.5 s` (`:223`) + the
`12.0 s` death poll (`:233`), and only the poll is skipped by a dying child.  Post-fix every session survives, so the
poll is roughly 12 of ~19 s per session, i.e. about 60 % of the 568 s.  Cutting it to 3 s would bring the run to
roughly 300 s; cutting it to zero leaves a ~200 s floor from the fixed sleeps.  **So C halves B's cost; it does not
remove it.**  The latency the poll guards against was measured ONCE at the probe's birth -- *"a process that SIGABRT'd
0.6 s later"* (`:225-231`) -- and 12 s is a 20x margin on one sample.  The round's first act is therefore ONE
measurement: the death-latency ceiling across the four reinstated-abort mutants (they are the builds clause (b) owes
anyway), and the new poll is set from that ceiling with a stated margin.  That settles B-versus-C by a number rather than
by this adjudication.

**A fourth member the packet's option set lacks, for the round to weigh, not adopted here (option-set-completeness
rule):** D -- wire the block with a battery-only switch that prints a LOUD, pinned `SKIP` row on targeted runs.  Zero
attended cost, weekly coverage, and the checker's `exec_sites()` still scores the detector as RUN (the exemption line is
then deleted, as the STALE EXEMPTION rule at `check_probe_wiring.py:3930-3933` requires).  Its hazard is the one this
tree already names: a conditional gate section is a check that cannot fail on the runs that skip it unless the skip is
loud and its own count is pinned (`gate_skip ... silent coverage loss scored as SKIP`).  The round should say in one line
why it took or refused D.

----------------------------------------------------------------------------------------------------------------------
## 2.  Q2 -- the date and the text

**2026-10-30: yes, as a BACKSTOP, with its reasoning written down.**  The owed work is the `wiringcliff` round, which the
disposition makes the next single task; if that holds, the line is DELETED with the wiring and the date never fires.  The
date matters only on a slip: 10-30 allows one slip of about a week, it does NOT stack on any other expiry (the next ones
are 10-22, 10-22, 10-23, 10-26, 10-27, then 11-05 -- `exemptcliff`'s own lesson was never to align two debts on one
day), and it spans two Sunday batteries (10-18, 10-25).  Aligning it to 10-22 instead was considered and rejected: it
re-creates a block cliff in six days if the round slips, against the 09-24 owner ruling's per-entry owed-work dates.

**The text: keep `04f3e7c0`'s two-part form.**

* A COMMENT above the entry, the precedent's wording with the dates changed: *"Re-dated 2026-10-15 -> 2026-10-30 on
  2026-10-16 by the owner's four-adjudicator roster (regress/artifacts/adj_20261016/wiringcliff/), in its own commit: it
  came due with the gate_arm.sh block still owed and refused every commit.  A re-date is not a discharge."*
* The reason tuple: the coordinator's text is right in substance -- it names the home, the measured cost, and the
  owing row -- with four edits:
  1. **Do not write "four-seat ruling" until four seats have answered.**  Write the count the completed panel measured and
     name the seats; a seat that did not answer is a seat failure, never a vote (the tally-before-the-panel-finished class
     in the carrier).  When I wrote this, the directory held answers from codex, glm and grok plus this one -- but their
     content was not opened, so I do not know which of them are REAL answers.
  2. Cite the 568 s by its exact artifact, `regress/artifacts/exemptredate_20260925/opus550_measured_p2/keep_p1_logs.out`
     ("ip30 wall from file mtimes: 568 s"), which the comment block above the entry (`:3091-3096`) already carries; the
     proposed `regress/artifacts/exemptredate_20260925/` is a second, vaguer citation of the same number.
  3. Keep the existing `(gate_asan_sweep.sh constructs only)` and `with #518/#520/#530` -- both still true and
     cross-referenced from the Alpha entries; a one-line commit should not also delete text.
  4. Add "33 rows" beside the 568 s: that is the denominator a gate will pin (see fact 3).

----------------------------------------------------------------------------------------------------------------------
## 3.  Q3 -- the facts, checked

| # | status | what the file says |
|---|---|---|
| 1 | **READ, true** | `precommit_check.sh:541-553` at HEAD: `PWCHK=$_HERE/pipeline/check_probe_wiring.py` (`:542`), `if out=$(python "$PWCHK" 2>&1)` (`:546`, no `--today`), `bad "A COMMITTED DETECTOR IS RUN BY NO GATE ..."` (`:550`); `bad()` at `:37` increments `fail`, and the tail exits 1 on `fail > 0` (`PRECOMMIT_FAIL`).  Checker: `--today` parsed at `:3869-3870`, default `datetime.date.today()` at `:3871-3873`, `elif d < today:` at `:3941` (EXPIRED branch `:3941-3944`).  And `:559-561` makes a TOUCHED checker (diff, cached diff, or untracked) run `--selftest` with the mutant count pinned at 22 (`:583-586`). |
| 2 | **READ, true but INCOMPLETE -- the consequential correction** | HEAD `:3097-3100`, date `2026-10-15` at `:3098`; working tree `:3112-3115` (the packet's `3112-3114` is one line short; the date is at `:3113`).  MEASURED today: the HEAD checker against the real index -> **1 problem** (EXPIRED EXEMPTION, ip30).  The WORKING-TREE checker, which is what precommit runs -> **6 problems**: the expiry PLUS **five GHOST** entries; with `--today 2026-10-15` -> **5 problems**.  See section 4, item 1. |
| 3 | READ; **row count stale** | `686d179c` 2026-09-18 06:09 -0500, subject `#531 ip30abortkill + #532 stagetokens ...`; probe +718 lines there, 721 at HEAD; header `:9-12` says 8/21 -> 21/21 -> "27 rows after the pass-2 class closure".  But the shipped instrument reports **`IP30ABORT_RESULT=33/33`** (the 09-25 log, `p1_runs/ip30_out_ip30.txt`), and the only commit to the probe since, `ef577140` (#561, 2026-10-06), is docstring-only (READ: its diff is the `session()` docstring) -- so **33 is HEAD's denominator; 27 is the 09-18 figure.**  Facts 3 and 4 disagree and fact 4 is current. |
| 4 | **READ, true** (one provenance nit) | `04500deb` is dated **2026-09-26**; the measurement is 09-25 (`p1_runs/` mtimes 2026-09-25 16:18:43) -- "re-dated on 2026-09-25" is the work date, not the commit date.  `#550`'s message set the IP30 date "in owed-work order (ppc_rldicl 10-08; ip30_abort 10-15; the four Alpha probes 10-22..10-27 ...)".  `gate_arm.sh` is GATE 14 (`:2`) and runs **seven `sgi_*_probe.py`** (`:1318,1402,1492,1529,1573,1611,1660`) plus `crime_width_probe.py` (`:1887`), an eighth SGI-machine probe; **all eight exec `-e ip32`** (grep of each probe), the IP30 probe execs `-V -x -E sgi -e ip30 -M 64` (`:193`) -- so "no gate runs an SGI IP30 guest session" is true as written.  The 12 s poll is `deadline = time.time() + 12.0` at `:233`, per session, paid in full only by survivors. |
| 5 | **READ, true** | The ten EXEMPT entries at HEAD (`:2978-3101`): wdc_altoffset 11-05, _sig 11-19, _4bit 11-12, wdc_addtoinbuf 12-03, ppc_rldicl 10-22, alpha_tbi 10-22, lca_badval 10-23, lca_widewrite 10-26, lca_isalane 10-27, ip30 10-15.  The alpha/lca reasons all name `gate_crossfamily.sh` as the home.  "The three LCA ones belong to the other session" is REASONED from the standing note that lca*/alpha* holds are the peer's, not from any file. |
| 6 | **READ, true** | ledger `wiringcliff`: state "in work", sev med, opened 2026-08-30, commits `8404520 eec0f4a`.  `exemptcliff` (the one-day alignment hazard) is CLOSED at `04500deb`, so `wiringcliff` is the right owing row.  Its 09-09 ruling is the standard this re-date must meet: *"an EXEMPTION naming the round that owes it -- debt that expires, not debt that disappears"*. |

**The per-commit / weekly question, answered from the files.**  `precommit_check.sh` runs NO gate (its only `gate_arm`
mentions are comments); section R runs the checker alone.  Gate 14 runs (a) in the FULL battery -- `run.sh:10` lists it
at position 14 of 16, `nightly_battery.sh:70` runs `./run.sh`, and the last battery (`_scratchpad/nightly/
verdict_20261011_180002.txt`) ran **18:02:24 -> 22:02:45, four hours**, REGRESS_PASS 16/16 -- and (b) as the ATTENDED,
serialized targeted gate of any round whose probe lives in it: **seven commits touched `gate_arm.sh` in the four weeks
since 09-18** (#536, #539, #545, #548, #529, #556, #562), i.e. about two attended runs a week, each run while nothing
else may use the machine.  So B's 568 s is ~4 % of an unattended Sunday battery AND ~9.5 min of serialized attended time
about twice a week, recurring until C lands (which halves it).  (Context, not the packet's claim: the carrier's "~45 min"
battery figure is stale by this verdict.)

**The after-state, measured on scratch copies, the way `04f3e7c0` preserved `after_redate.out`:** HEAD's checker with
only the date changed to 2026-10-30, run against the real index with today's clock -> `PROBEWIRING_PASS  74/84 detectors
run by a gate, 10 dated-exempt, 43 witnesses correctly ungated` (rc 0).  Its `--selftest` -> `PROBEWIRING_SELFTEST_PASS
22/22` (the precommit pin).  The AS-IS working-tree checker's selftest today -> **`SELFTEST_FAIL 20/22`**: `M0 unmutated
copy is GREEN rc=1` and `M2b`, because the expired entry reds the selftest's own baseline -- the same thing `04f3e7c0`
recorded on 10-08.  So any unit that touches the checker today fails TWICE (section R and the touched-checker selftest),
and the re-date clears both.  These runs must be re-done at commit time from the real file; mine are scratch copies.

----------------------------------------------------------------------------------------------------------------------
## 4.  Q4 -- the coordinator's dispositions I would change

1. **"stages HEAD's file plus this one line only" is right for THIS commit and silent about the NEXT one.**  The working
   tree's checker carries 15 uncommitted lines (mtime 2026-10-09 21:09:42, sixteen minutes AFTER HEAD landed): a records
   comment at `:1533-1537` and a MANIFEST hunk at `:1408-1417` naming five files under
   `regress/artifacts/{wdcnullxfer,wdcrearmzero,fbclearread,b115}/rung3_20260913/` (four CLASS_RESEARCH, one CLASS_TOOL).
   All five exist on disk, dated 2026-09-13, and are `??` -- neither committed nor staged -- and `domain()` reads
   `git ls-files` (`:3323-3358`), so the checker reports five `GHOST` failures **independent of any date** (MEASURED:
   5 problems with `--today 2026-10-15`; 5 with the re-date applied to the working copy).  The commit tool's precheck swaps
   the unit's files to the unit's content and merges the rest back afterwards (its 10-09 run log: "backed up ... staged
   19 paths ... COMMITTED ... merged CHANGELOG.md"), so a unit carrying HEAD+1 line passes section R -- and the moment the
   15 lines are merged back, the next unit that does not carry the checker is refused by section R for a reason this packet
   never names.  **Add to the disposition:** before or with the next unit, either land the parked `rung3_20260913` unit
   (its five files WITH their MANIFEST lines -- no wiring is owed, they are research/tool classes) or drop that hunk from
   the working copy; say which session owns it.  Section R is not "unblocked" until that is done.

2. **"decided on their own dates" is off by one in the dangerous direction.**  `d < today` makes the stamped date the LAST
   green day (the checker's own comment at `:3687-3689`): the 10-22 pair reds every commit, for both sessions, on the
   morning of **10-23**; lca_badval on 10-24, lca_widewrite on 10-27, lca_isalane on 10-28.  Write "on or before", and put
   the five dates with an OWNER each into the re-date's CHANGELOG block (ppc_rldicl: this session's PowerPC work, per
   `04f3e7c0`/`a05660af`; alpha_tbi and the three lca_*: the peer's) so the next cliff is a scheduled decision, not a
   surprise.  The `wiringcliff` round, if it is genuinely next, should either take `ppc_rldicl`'s owed `gate_ppc.sh` block
   with it or say in one line that it does not.

3. **"four-seat ruling" -- write the measured count after the panel completes**, naming the seats that answered (section 2,
   edit 1).  A ruling issued short of the roster is provisional on its face.

4. **"B or C" is the wrong decision shape for the round:** the choice is settled FIRST by the death-latency measurement
   (section 1), with the arithmetic that C halves rather than removes the cost, and the option set carries D (section 1).
   The round record should state the cost of whichever it ships in the unit the files use: seconds per attended gate-14
   run, from a timed run, not from this estimate.

5. **Copy `04f3e7c0`'s records discipline, which the disposition omits:** the "a re-date is not a discharge" comment; the
   before/after/precheck outputs preserved at a durable path (this directory, or `regress/artifacts/
   probewiring_redate_20261016/`); the CHANGELOG block.  Do NOT put a `ledger.json` edit in the re-date unit:
   `ledger.json` and `matrix.html` are among the **20 modified tracked files** (with 652 untracked paths) the two sessions
   hold uncommitted, and the precedent for this exact change touched neither -- the round writes its own ledger entries.

6. **Execution hazard, not a disposition change:** the unit touches the checker, so precommit's touched-checker branch runs
   the 31 s selftest (pin 22; measured 22/22 on the re-dated copy); and the commit tool must be launched in the background
   with no timeout wrapper -- its killed-precheck failure on 2026-10-09 left 77 staged paths and swapped files.

7. **Filed, not adopted (a checker change owes its selftest pin bump and two negative controls, and is the owner's call):**
   a `note` line, not a FAIL, when an exemption is within N days of its date, so a cliff is announced before it blocks both
   sessions.  This is the third expiry-driven block in four weeks (09-27 block, 10-08 ppc_rldicl, 10-15 ip30), and at least
   the IP30 line's third date (#536 -> 09-27, #550 -> 10-15, now 10-30).  It can ride with `exemptcal` (open), which
   already owns a `DATE_RE` change to the same table.

**Dispositions upheld:** A now; re-date nothing else today (the 09-09 ruling refused blanket re-dates and the 09-24 owner
ruling chose per-entry owed-work dates); the `wiringcliff` round as the next single task; the reason naming the measured
cost and the owing row; HEAD's file plus one line as the unit.

----------------------------------------------------------------------------------------------------------------------
## 5.  Re-derive every number here (run from `GXEMUL-SEC/`; nothing writes to the tree)

    python tools/pipeline/check_probe_wiring.py                      # working tree: 6 problems (5 GHOST + EXPIRED)
    python tools/pipeline/check_probe_wiring.py --today 2026-10-15   # working tree: 5 problems (GHOST only)
    git show e483d931:tools/pipeline/check_probe_wiring.py > /tmp/chk_head.py
    python /tmp/chk_head.py --regress "$PWD/regress"                 # HEAD: 1 problem (EXPIRED)
    sed 's/("2026-10-15",/("2026-10-30",/' /tmp/chk_head.py > /tmp/chk_head_red.py
    python /tmp/chk_head_red.py --regress "$PWD/regress"             # HEAD+re-date: PROBEWIRING_PASS 74/84, 10 exempt
    python tools/pipeline/check_probe_wiring.py --selftest           # today: SELFTEST_FAIL 20/22 (M0, M2b)
    git status --short -- regress/artifacts/*/rung3_20260913/        # the five ?? files the MANIFEST hunk names
    git show --format= 04f3e7c0 -- tools/pipeline/check_probe_wiring.py   # the precedent's hunk
    cat regress/artifacts/exemptredate_20260925/opus550_measured_p2/keep_p1_logs.out   # "ip30 wall ... 568 s"
    tail -2 regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/ip30_out_ip30.txt   # 33/33
    for p in sgi_de_width sgi_re_width sgi_re_unmapped sgi_re_randompixel sgi_re_colourdefault sgi_re_rgb \
             sgi_de_primop crime_width; do grep -ho 'ip3[0-9]' regress/${p}_probe.py | sort -u; done   # all ip32
    git log --since=2026-09-18 --format='%h %ad %s' --date=short -- regress/gate_arm.sh | wc -l    # 7
    sed -n '1,12p' ../_scratchpad/nightly/verdict_20261011_180002.txt   # START 18:02:24, END 22:02:45
