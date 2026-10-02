SURVEY: RESUMABLE WITH FIXES

# #529 `crimewidthkill` -- resumption dossier (read-only survey, 2026-09-25 ~21:30)

HEAD `f4f601c4` (#548).  Tree surveyed: `GXEMUL-SEC/` only.  Nothing under `C:\DocumentNoSnc\cc\GXEMUL` was written;
no build, no emulator.  The only files written are in this `p529/` directory.

**Evidence tags used throughout**
* **[READ]** -- I opened the file, artifact, ledger entry or subagent transcript and quote it.
* **[COMPUTED]** -- I ran a read-only tool (cmp, md5sum, a checker in its non-writing mode, an AST compare, or the
  probe with its `session()` stubbed so no emulator ran) and quote the output.
* **[INFERRED]** -- my reasoning, not settled by a run.  Treat it as a prediction to be measured.

## 0. Bottom line

* **The fix is finished, unchanged since 2026-09-13, and identical in all four trees** [COMPUTED]: working
  `dev_sgi_ip32.c` md5 `8c1d1545` = table 12's `INSTRUMENT.md5` entry = est/, build/, build-asan/ and
  /tmp/gxsec-build.  Part 1 CLEAN everywhere, part 2 FRESH in the three build trees, est/ part 2 N/A (source tree),
  no `.MUTANT` sentinel in any build tree or in any #529 scratch clone.
* **The detector is consistent with its pins**: 204 rows [COMPUTED], gate pins 204 x3 [READ], and the last measured
  base legs read 204/204 [READ].
* **The ledger's `state_note` is STALE.**  It says "NOTHING MEASURED ... Next: fire table 12".  But table 12 ran to
  completion on 09-17 (15/15 legs, each ending `CRIMEP_DONE`) [READ].  The ctl0c discharge also ran, and the gate
  pin was fixed on 09-18.
* **Of the two defects Fable named on 09-18:**
  * The gate pin 188 vs 204 is **FIXED** [READ].
  * "No #529 commit, probe staged but never committed" is **STILL PRESENT, and worse** [COMPUTED].  The probe is now
    untracked (`??`) and the index is empty.  Its current bytes are in no git object.
* **NEW, and it changes what "Fable ruled" means for this round** [READ from the subagent transcripts].  Three of the
  rulings that govern #529 were written by `claude-opus-4-8` after Fable refused:
  * `FABLE_C3_RULING_20260914.md` (repair 11);
  * `FABLE_C5_RULING_20260915.md` (repair 13's "latch is FLOOR", which overturned a TRUE-Fable RA3);
  * `FABLE_RULING_20260917.md` (repair 14's shape, its stop condition, and a new floor clause).

  Ledger entries [75], [96], [133] and [134] still credit them to fable5.  Under the standing rule (memory
  `gxemul-agent-refusal-fallback`) a fallback is a SEAT FAILURE, never a ruling.
* **Still owed before close** (§3):
  * the INTMASK and CONTROL-write label-swap measurements;
  * the TIME and REV decline carriers;
  * the entries-13/17 CHANNEL check;
  * two contract (clause e) items;
  * a full-roster pass 2 plus an §F2 pass (Fable AND Astra);
  * several records fixes;
  * a commit that must carry `check_score_claims.py`'s uncommitted hyphen fix.
* **Timing**: resume only after #549 commits (owner ruling 2026-09-24).  #549 is waiting on Astra; codex is walled
  until 2026-09-26 07:01.

---

## 1. EXACTLY what #529 changes versus HEAD

### 1a. `src/devices/dev_sgi_ip32.c` -- +32/-2, three hunks, ALL #529's [READ `git diff HEAD`]

`git log -- src/devices/dev_sgi_ip32.c` shows only `8dd86b5a` (hardening) and `39748e3c` (import), so no other round
has touched this file.  HEAD md5 `4088baa8`, working md5 `8c1d1545` [COMPUTED].

| hunk | lines (working) | change |
|---|---|---|
| `@@ -82,8 +82,14 @@` | :86-91 | adds `int warned;` to `struct crime_data` (the comment says memset(0) at init clears it) and `#define CRIME_W_LEN (1 << 0)` |
| `@@ -288,8 +294,29 @@` | :296-320 | replaces `fatal("crime access len = %i!\n", len); exit(1);` with a latched announce, `fatal("[ crime: unimplemented len=%i at 0x%x -- declined.  (once) ]\n", ...)` guarded by `if (!(d->warned & CRIME_W_LEN))`, then `goto crime_declined;`.  A 17-line comment says why the switch is skipped and why this is not `return 0` |
| `@@ -381,6 +408,9 @@` | :411-413 | adds the `crime_declined:` label and its comment before the common tail (HARDINT restore, INTSTAT recompute, `memory_writemax64` on reads, `return 1`) |

The disposition is option-set member 3, DECLINE + LATCHED ANNOUNCE (the #498 `sgi_de` shape).  The probe's own
`:293-294`, `:229`, `:231`, `:314`, `:361-379` citations resolve correctly against this working file [READ].

### 1b. `regress/gate_arm.sh` -- +59/-0, ONE hunk, ALL #529's [READ]

The working file equals HEAD plus that single hunk (`@@ -1864,4 +1864,63 @@`), which sits just before `gate_end` at
:1926.  `git show HEAD:regress/gate_arm.sh | grep -c crime_width` = 0 [COMPUTED].  Other rounds' sections in this
file are all at HEAD and untouched.

* :1867-1871: header comment.  :1872: `CRIMELOG=$LOGDIR/gate_crime_width.log`.  It runs
  `python3 -u crime_width_probe.py "$PMAX" gate`, where `PMAX` defaults to `$ROOT/build/gxemul` (:77).
* Parse-before-score requires exactly one each of `CRIMEP_RESULT=n/N`, `CRIMEP_CONTROL=OK|FAIL` and `CRIMEP_DONE`.
* **7 checks** (CHANGELOG `:514` independently counts "#529's seven checks"):
  1. parses
  2. controls == OK
  3. exit status == 0
  4. `crime_width rows run` 204 (:1916)
  5. `crime_width rows correct` "204" (:1921)
  6. `crime_width rows emitted` "204" (:1922)
  7. `crime_width rows failed` "0" (:1923)
* `bash -n` passes [COMPUTED].
* **Stale text inside the hunk** (L4, fix before commit):
  * :1869 says "the **four** kill tables".  There are twelve tables plus the 2-leg ctl0c discharge.
  * :1906-1909 is the ORDER warrant: "crime_width_probe.py is dated 09-17 10:38:08 ... no fresh base leg is owed".
    That is **no longer true**.  The probe's mtime is **2026-09-23 15:25:36**, and its bytes differ from both
    measured instruments (§1c).

### 1c. `regress/crime_width_probe.py` -- UNTRACKED, never committed [COMPUTED]

* `git status` shows `??`, `git ls-files --error-unmatch` fails, `git log` is empty, and the index is empty.
* 1597 lines, 120,015 bytes, md5 `a0af7c92`, git blob `4f76458e`.  **That blob is in NO git object**
  (`git cat-file -t` fails).  Every snapshot ref (`refs/snapshots/crime_width_probe_20260921`,
  `tree_including_untracked_{e8a2bc_20260921,087a90_20260923,087a90_20260923b}`) holds the previous revision
  `97ab2415`.
* A byte-identical out-of-git copy exists at `_scratchpad/census0923/c2_frozen/crime_width_probe.py` (md5 `a0af7c92`).
* **Rows: 204.**  Computed by executing the probe with `session()` stubbed out, so no emulator ran
  (`p529/probe_stubcount.py`): 204 `row()` calls, **all 204 names distinct**, 56 sessions, longest name 15 chars
  (`free imask said`, `free istat said`).  The static `grep -c "^\s*row("` gives 153 because of loop templates,
  which the gate comment itself notes.
* **A line written by ANOTHER round** [READ, COMPUTED]: #546 `hygienecensus` (committed `3e33201d`) re-spelled
  `op.endswith("P")` as `op[-1:] == "P"` in `accept()` (:956-963, with a 7-line comment), on 2026-09-23.
  * The #546 commit records the resulting md5 `a0af7c92`.
  * An AST compare shows this is the **only code difference** from table 12's instrument
    (`crime_width_probe.table12.py`, `fa1da8b8`); everything else is docstring or comments.
  * The two spellings are equivalent for every `str` [INFERRED from Python semantics; the #546 record measured the
    eight op strings].
* Docstring score claims: every N/M carries an era tag (40, 71, 121, 131, 141, 157, 188-row); none sits at /204
  [COMPUTED].  Moving the pin will therefore not trip `check_score_claims`.
* Sentinel `CRIMEP_DONE`, plus `CRIMEP_RESULT=` and `CRIMEP_CONTROL=` (:1595-1597).  The CONTROL set is 17 named
  rows (:1589-1592).

### 1d. `tools/pipeline/check_probe_wiring.py` -- the working diff is SHARED [READ, COMPUTED]

| lines in the working diff | owner |
|---|---|
| MANIFEST `"crime_width_probe.py"` (:873) plus **72** `artifacts/crimewidthkill/...` entries, in hunks at old :870, :890, :992, :1026 | **#529** |
| 5 rung-3 witness entries dated 2026-09-13: `b115/`, `fbclearread/`, `wdcnullxfer/` (x2), `wdcrearmzero/` | NOT #529 by content (other rows).  `commit549.sh` counts them as "#529's parked lines", so they will ride with #529 unless someone moves them |
| `--selftest applies 18` -> `22 mutants` (:103) | **#550** (`stage550/` carries it) |
| the EXEMPT re-dating block and "Seven exemptions remained then" | **#550** |
| `"fbctrl_port_probe.py": (CLASS_DETECTOR, "#549 ...")` | **#549** |

* The **#529 entry's description is stale**: "141 rows ... through killtable8_20260914/ ... pin 141".  The pin is
  204.  L4.
* **Running the working checker now gives `PROBEWIRING_FAIL 79 problem(s)`** [COMPUTED]:
  * 72 GHOST crimewidthkill artifacts and 1 GHOST `crime_width_probe.py` (#529 files neither committed nor staged);
  * 5 GHOST rung-3 entries;
  * 1 GHOST `fbctrl_port_probe.py` (#549).

  This is expected while the work is parked: the check's domain is `git ls-files`.
* **39 #529 artifact `.py` files have NO MANIFEST entry** [COMPUTED].  111 are on disk and 72 are listed.  The
  missing ones:

  | directory | files |
  |---|---|
  | `ctl0c_discharge_20260917/` | 2 |
  | `killtable11_20260916/` | 3 |
  | `opus_close7_20260915/` | 4 |
  | `opus_close8_20260916/` | 13 |
  | `repair14_20260916/` | 17 |

  Staging them without entries turns them UNCLASSIFIED.

### 1e. `tools/precommit_check.sh` -- the working diff is SHARED [READ]

* Hunk `@@ -336,9 +336,15 @@`: `SCORE_CLAIMS_MANIFEST=32` (:347) = HEAD's 30 + #529 (crime_width) + #549
  (fbctrl_port).  The comment re-tells the history as three lines:
  * :339 "29 -> 30 ON 2026-09-13 ... crime_width_probe.py (#529, ... at **188 rows** since repair 13 ...)";
  * :341 "30 -> 31 ... landisk_aux (#533)";
  * :344 "31 -> 32 ... fbctrl_port (#549)".
* **#529's part is one unit of the manifest plus the :339 line, and that line is stale twice**:
  * the pin is **204**, not 188;
  * after #549 commits, HEAD will read "29->30 #533, 30->31 #549, =31" (`stage549/tools/precommit_check.sh`
    :339-343), so #529 must APPEND "31 -> 32 ... crime_width ... 204 rows" rather than re-tell 29->30.
* Hunk `@@ -524,7 +530,8 @@` (the exemption-dispersal note) is **#550's**.
* The working checker agrees with the working manifest: `SCORE_CLAIMS_PINNED=32`, `SCORE_CLAIMS_PASS` [COMPUTED].

### 1f. A dependency OUTSIDE the named files: `tools/pipeline/check_score_claims.py` (uncommitted, +21/-1)

* The working `SCORE` regex (:114) adds `-` to the lookbehind (row `scorehyphenfp`).
* **HEAD's checker, run against this working tree, fails on #529's probe** [COMPUTED: `p529/csc_head.py`]:
  `STALE crime_width_probe.py docstring claims 4/8, pin is 204`.  The cause is the ordinal `entries-4/8` at probe
  :314.
* The ledger marks `scorehyphenfp` **closed with `commits: []`** [READ]: a closure on a fix that exists only in the
  working tree.
* #529 cannot commit without this fix, either in its own commit or committed before it.  Rephrasing `entries-4/8`
  would also avoid it.

### 1g. Adjacent files that are NOT #529's but that #529 depends on or is confused with

* `regress/gate_hygiene.sh`:
  * HEAD (#546) already grandfathers `crime_width_probe.py` by name as promptless (:419; owner ruling 2026-09-23 #3).
    Its comment says a fresh clone reds three gate-6 rows until the three untracked probes are committed [READ].
  * The **working** bump `EXPECT_PTY_PROBES 73->74`, `EXPECT_CONVERTED 24->25` belongs to **#549's**
    `fbctrl_port_probe.py`, which uses `pty.fork` and has an `endswith("GXemul>")` predicate [READ].
  * **But `commit549.sh`'s FILES list omits `gate_hygiene.sh`** [READ] -- worth telling #549's owner [INFERRED risk].
* `tools/pipeline/ledger.json`: the `crimewidthkill` row (155 entries) is **already committed at HEAD** via other
  rounds' ledger commits.  HEAD and working are identical for it and for the filed rows `crimectlflood`,
  `crimeramexit`, `crimesplitwidth` and `macepciwidth` [COMPUTED].
* The artifacts: `regress/artifacts/crimewidthkill/` holds **2483 untracked files, 46 MB**, with only 4 tracked
  (codex witness logs) [COMPUTED].  **It includes three 6,159,904-byte gxemul binaries in
  `ctl0c_discharge_20260917/bin/`**, which are not gitignored.

---

## 2. What "repair 14" is, and where it actually stands

### 2a. The repair [READ `repair14_20260916/PRETABLE.out`, probe :268-338, :1228-1538]

This is the class closure that closing pass 8 forced.  Pass 8 found five escapes at 188/188 [READ ledger [108]/[109]
and `opus_close8_20260916/VERDICT.md`]:
* `G_glm_tim4clear`;
* `G_clr_ist4r`;
* `G_lane_ctl`;
* `K_ctl4w_reset_post`;
* `K_ctl8w_reset_post`.

Probe-only edits, 188 -> **204 rows**:

| rows | cell |
|---|---|
| `c t4w gap`, `c t4r gap`, `c t gap once` | ACCEPTS 32/33, TIME 4W/4R, latch CLEAR, gapped channel.  The control wants `[0, 0]` |
| `acc istat lw`, `p acc istat lw` | entry 21, both latch states, seeded above bit 31 |
| `top8 clear` | entry 46, latch CLEAR |
| `acc ctl4r` + `acc ctl0c`, and their POST twins | the CONTROL 4R PAIR |
| `rst alive`, `rst alive once`, `rst 4w`, `rst 4w once`, `rst 8w`, `rst 8w once` | the HARD_RESET generating-set cells.  The halt oracle wants the SENTINEL, not `absent` |
| `p acc ctl msg` 3 -> 4 | entry 14's `sd 0x0201` width twin (L2) |

* **Mandated order, proven by mtimes**: `PRETABLE.out` 03:16, `check_pred.py` 03:16, `mutants_r14.py` 03:15, then
  driver `kill529r14.sh` 03:25, and the run at 07:38.
* **An L1 fix inside it** [READ ledger [150]]: the ctl0c rows first loaded into `a3`, which `st()` clobbers, so the
  first base read 202/204.  The table was aborted at 4 of 15 (`aborted_t12_20260917_0711/`), the rows were moved to
  `s4`, and the encoding was pinned by assertion (probe :457).

### 2b. Kill table 12 -- COMPLETED, contrary to the ledger's state_note [READ `logs/probe_*.raw`, `POSTTABLE.out`, `check_pred.out`]

Clone `/tmp/gxopus_r14`, re-fire `kill529r14.run-073855.sh`, `KILL529R14_DONE 08:53:26` on 2026-09-17.
**Every one of the 15 logs ends `CRIMEP_DONE`**, and the instrument md5 is `fa1da8b8`.

| leg | score | red rows |
|---|---|---|
| base | **204/204** OK | -- |
| G_glm_tim4clear | 202 | c t4w gap, c t4r gap |
| G_clr_ist4r | 203 | acc istat lw |
| G_lane_ctl | 203 | p acc ctl4r (predicted 4 rows; the sole carrier) |
| K_ctl4w_reset_post | 203 | rst 4w |
| K_ctl8w_reset_post | 203 | rst 8w |
| M2_ld278clr | 203 | top8 clear |
| W_ctl8w (entry 14's (d) mutant) | 202 | p acc ctl msg, rst 8w |
| G_clr_imk4r (control) | 203 CONTROL=FAIL | gate line |
| G_clr_ctl4r (equivalent) | 204/204 | -- |
| **M3_timelatch** | **204/204 -- disclosed escape** | -- |
| **M5_revlatch** | **204/204 -- disclosed escape** | -- |
| M4_timeplain | 200 | time lb/sb/lh/sh |
| M6_istlatch | 201 | istat sb, istat lh, istat sh |
| M1_gotolatch (no prediction) | 194 | sb08 msg, sh08b run, imask sb/lh/sh, istat sb/lh/sh, gate run, mid nodflt |

`check_pred.out` gives `CHECK_PRED12_PASS_WITH_PREDICTION_MISSES`: 14 of 15 match exactly, and the one miss
(`G_lane_ctl`) is an over-prediction.

### 2c. The pass 2 on repair 14, and the ctl0c discharge

* **grok pass 2, 2026-09-17** (`grok_pass2_20260917.txt`, the only seat fired on it) [READ, ledger [151]]:
  * it split KILL from CHANNEL, so a prediction miss is L4 of PRETABLE;
  * G_lane_ctl as sole carrier is not a breach;
  * `acc ctl0c` never reds in 15 legs;
  * the `default:` arm is NOT host-log-only for +0x0c.

  L4 fixes are in `L4_CORRECTIONS_20260917.md` and the probe header (:303-323).  Its verdict: "This pass does not
  close #529: the decline-suppression face stays open."
* **The ctl0c discharge** (`ctl0c_discharge_20260917/`, clone `/tmp/gxctl0c`) [READ `RUN.out`, `VERDICT.md`]:
  base 204/204; `M_ctl0c_decline` 202/204, with exactly `acc ctl0c` and `p acc ctl0c` red, as predicted before the
  run.  The binary differs from base, and the clone was restored cmp-clean, binary-nt-source.
  **The ctl0c L1 is discharged.**
  * CHANGELOG `:2686` (committed) still lists it as OWED; the #529 block should record the discharge.

### 2d. Fable's 2026-09-18 flagship -- "two checkable defects ... ONE WOULD RED THE GATE TODAY"

Ledger [154]; the full answer is in subagent transcript `agent-a2865c082138f4cf6`, extracted to
`p529/flagship_0918_final.txt`.  This run **is genuine Fable**: 87 `claude-fable-5-1` turns, 0 refusals
[COMPUTED from the transcript].

| defect named 09-18 | status today | evidence |
|---|---|---|
| gate pin 188 while legs read /204, which reds three checks | **FIXED** | [READ] gate_arm.sh :1916/:1921/:1922 now say 204; the probe emits 204 [COMPUTED]; both newest base legs read 204/204 [READ] |
| no #529 commit; probe staged `A` but never committed | **STILL PRESENT, WORSE** | [COMPUTED] the probe is untracked `??`; staging "did not survive" (`untrackeddetectors` row: 18 unreachable staged blobs, cause unsettled); the current bytes are in no git object |
| (its premise) "table 12 ... not met until that table completes" | table 12 **had already completed** on 09-17 08:53; the premise was stale when written | [READ] 15 logs with `CRIMEP_DONE` |

Fable's own "measurement that settles" -- fifteen logs with `CRIMEP_DONE` plus a base at 204/204 matching the pin --
**is satisfied by the preserved artifacts**.  The underlying stop condition is NOT met, for the reasons in §3.

Record hygiene: the answer lives only in the transcript, and the ledger EV points at the brief in `_scratchpad/`
(volatile).  Preserve it durably.

### 2e. PROVENANCE: three "fable5" rulings are opus-4-8 fallbacks [READ from subagent transcripts, raw per-message `model`]

Transcripts are in `~/.claude/projects/C--DocumentNoSnc-CC-GXEMUL/8e474f41-.../subagents/`; confirmed by
`_scratchpad/agent_models_now.out`.  The `Write` to each ruling file was made by the model shown:

| file | ledger entries | agent | refusal | file written by |
|---|---|---|---|---|
| `lcaisalane/FABLE_C3_RULING_20260914.md` (repair 11, `ldP` floor) | [75] | `ae169fa9758283eaf` | fable-5-1 16:22:26Z | **claude-opus-4-8** 16:29:48Z |
| `lcaisalane/FABLE_C4_RULING_20260915.md` | [85] | `aa9893713d708ebcd` | none | claude-fable-5-1 (genuine) |
| `lcaisalane/FABLE_C5_RULING_20260915.md` (repair 13: "D7 RULED FLOOR, my prior RA3 OVERTURNED") | [96] | `a06935485cd6d5125` | fable-5-1 2026-09-16 19:35:00Z | **claude-opus-4-8** 19:50:12Z |
| `crimewidthkill/repair14_20260916/FABLE_RULING_20260917.md` (repair 14 + Q3 floor clause + stop condition) | [133], [134] | `a2bba4bc2896433b4` (18 fable / 16 opus-4-8 turns) | fable-5-1 06:17:21Z | **claude-opus-4-8** 06:25:19Z |

* Each opus-4-8 file carries a self-reported `MODEL: claude-fable-5-1` line.  Entry [134]'s "SEAT VERIFIED AS
  FABLE" rested on that identity line: the exact check the memory rule says cannot fail.
* `f685d75c` corrected the #530/#538/#541 fallbacks and **none of #529's** (its scan covered 09-18 onward).
* The C4 file (genuine Fable) was edited in place at 14:52 on 09-16, two minutes after the opus-4-8 C5 file, to
  mark its own RA3 "overturned".  So **a genuine Fable ruling (the latch-keyed shrink is clause-(e) debt) stands
  overturned by a non-Fable answer** in the probe header (:213-216) and the ledger.
* **Mitigation, stated so it is not overstated** [READ]: the genuine-Fable 09-18 flagship RATIFIED "the reshaped
  repair 14 (fable ruling, entry [133])".  So repair 14's SHAPE has a first-hand Fable ratification.
* What has **none** [INFERRED]:
  * the Q3 floor clause ("a suppressing guard's floor axes are the skipped dispatch's labels", adopted with three
    amendments; not in the carrier: `grep` of `CLAUDE.md` finds nothing);
  * the stop condition, including the INTMASK/CONTROL-write "VERIFY, do not derive" requirement;
  * repair 13's D7 grading.
* The rows themselves are measured kills either way, so no code or row needs to change on this account.  Only the
  records and the rulings do.

### 2f. Other records defects found on the way [READ]

* **Phantom filings.**
  * The probe header (:53-56 `crimectllane (filed)`, :141-142 "the filed `crimebankorder`") and gate_arm.sh
    (:1870) cite two rows that exist **nowhere**: not in the ledger, OUTSTANDING_BUGS.md, CHANGELOG.md or
    fable_queue.md [COMPUTED].
  * Their full text exists only in `_scratchpad/os529_draft.md`, which is stale ("SHIPPED as #529 (2026-09-13)").
  * `cl529_draft.md` is also stale: 141 rows, nine tables, `@CLOSE@` placeholder, and it lists
    `crimectllane`/`crimeram48`/`crimebankorder` as filed.
  * `crimectlflood`, `crimeramexit` (which replaces `crimeram48`), `crimesplitwidth` and `macepciwidth` DO exist.
* **The contract names none of repair 14's HARD_RESET rows.**  `rst 4w`/`rst 8w` (K_ctl*w_reset_post) are rowed in
  code (:1499-1538) but absent from the header's "NOW ROWED" list (:273-291).  M1_gotolatch, the general
  decline-suppression form, is also unnamed there.
* The contract header at :17-18 still says the tables run "through killtable10_20260915/".

---

## 3. What is still OWED before #529 can close, in order

Rules applied (CLAUDE.md): the vacuity floor (a)-(d) with DEPENDS-ON; the clause-(e) contract; accept-row
failability; the pre-table check (MANDATORY: `PRETABLE.out` written before table 1, with CHANNEL lines, and a
row-list diff against the prescribed rows); the repair-chain rule (a repair owes its own pass 2, closing on the first
VALID zero-breach pass with its denominator; two consecutive same-class breaches owe class closure in one diff); the
full panel on every stage; the §F2 adjudication pass; and Fable+Astra adjudication (memory, 2026-09-24).

**P0 -- sequencing** [READ owner rulings 09-24 #3 and 09-25 #1/#2; CHECKPOINT]
* Parked work is adopted only **after #549 commits**, one round at a time.
* The morning queue is Astra (after 07:01) -> #550 -> #551 -> #549.
* The `scexempt` harness round is due "after #549, before 09-28".
* The weekly battery runs **Sunday 2026-09-27 18:00**; keep the machine quiet.

Where #529 falls relative to `scexempt` is not ruled; `scexempt` has the hard deadline [INFERRED].

**P1 -- records and provenance** (no machine time; lands in #529's commit)
1. Tag ledger [75], [96], [133] and [134] `[NOT A SEAT ANSWER]` with the transcript evidence above, following the
   `f685d75c` pattern.
2. Get **first-hand** re-rulings from **Fable AND Astra**, neutral wording, verified with `agent_models.py`.  The
   memory says RESUME the refused agent, don't respawn; whether 8-day-old agents resume is unknown.  Scope:
   * (a) repair 14's stop condition, including the INTMASK/CONTROL-write measurement requirement and 13/17;
   * (b) the Q3 skipped-dispatch floor clause (a RULE question);
   * (c) D7, latch-keyed shrink FLOOR vs clause (e), where genuine Fable (C4 RA3) and opus-4-8 (C5) disagree.
3. Rewrite the ledger `state_note` from the artifacts.  Preserve the 09-18 Fable answer at a durable path.
4. File `crimectllane` and `crimebankorder` (text in `os529_draft.md`), or correct the "filed" claims.
5. Correct the stale descriptions:
   * the MANIFEST entry (141 -> 204);
   * the precommit :339 line (append 31->32, 204 rows);
   * gate_arm.sh :1869 and the :1906-1909 ORDER warrant;
   * probe :17-18;
   * add the rst/M1 rows to the contract.

**P2 -- measurement only, no probe or product edit: "table 13a"** (scratch clone rebuilt from SEC, PRETABLE first)
* **Base on the CURRENT probe bytes (`a0af7c92`)**.  Both measured bases ran on older bytes: table 12 `fa1da8b8` and
  ctl0c `38b85465`.  The code delta is only #546's line.  Expected 204/204 [INFERRED], but the gate comment's warrant
  for skipping this is void.
* **`latch_label("CRIME_INTMASK")` and `latch_label("CRIME_CONTROL")`**, built from
  `repair14_20260916/mutants_adj.frozen.py`'s method (the M5/M6 shape with the label swapped).  The ruling's ORDER
  item 2 says "VERIFY, do not derive".
* Predictions for PRETABLE [INFERRED, a derivation to be falsified].  M1_gotolatch is the union of all label swaps,
  and its measured reds partition cleanly by session label:
  * INTMASK -> {imask sb, imask lh, imask sh} (201/204);
  * CONTROL-write -> {sb08 msg, sh08b run, gate run} (201/204).
  * The INTSTAT part of M1's reds equals M6's measured set exactly, which supports the partition.
  * If either escapes, it joins TIME and REV as a floor cell needing a carrier (L2).
* Optional and cheap: `C_ist4r` from `killtable11_20260916/mutants529k.py`.  `p acc istat lw` carries no measured
  kill of its own; the cell's latch-SET mutant was killed only by `istat ctl` in table 11 (187/188).
* Cost: roughly 18-19 minutes per probe run [INFERRED from `ctl0c_discharge_20260917/logs`: build_base.log 12:15:54
  -> probe_base.raw 12:34:27].

**P3 -- "repair 15", one diff** (the class closure the repair-chain amendment demands)
* **TIME and REV decline carriers.**  M3 and M5 escape 204/204 today.
  * Ruling text: "replay `time lb/sb/lh/sh` AFTER a prior refusal" for TIME, and "the REV-window PC-redirect
    equivalent after a prior refusal" for REV (kimi CLI [132]: "REV in-window, TIME with a DOWNSTREAM READ").
  * Carriers for any label table 13a finds open.
  * Adds-only sessions keep the targeting rule simple [INFERRED].
* **Entries 13/17** (`sw`/`sd +0x08 = 0x0200`, DOG mask): run the ruling's CHANNEL check, which was never done
  (`grep` of all repair-14 artifacts and the probe finds no disposition) [READ].  The disposition is either a paired
  row (if a body-tested-partition mutant escapes) or a clause-(e) disclosure.
* **Contract (clause e) items the stop condition names that are missing** [READ probe]:
  * :413 says "widths 3, 5, 6, 7 (no MIPS load/store issues them)" unconditionally.  The ruling (D1) requires it to
    be stated as a CONDITION on `DEV_CRIME_LENGTH == 0x280` (row `crimesplitwidth` is filed);
  * the `+2` and larger translations are disclosed nowhere (`grep translation` = 0).
* A new PRETABLE, `check_pred`, a frozen driver and the table.  Pins move to the new count only **after** the base leg
  (the #462 rule).

**P4 -- the closing chain**
* Repair 14's own pass 2 was **grok alone** (`BRIEF_pass2_20260917.md`; ledger [151]).  It is short of the full-panel
  directive and could not close the chain anyway.
* Repair 15 owes a **full-roster pass 2**: `PANEL_KIMI_CLI=1 PANEL_FIRE_AGY=1 bash GXEMUL-SEC/tools/panel.sh <abs brief>`
  plus Opus plus Fable LAST, plus the dedicated codex and grok jobs (memory).
* Then the **§F2 pass**, adjudicated by **Fable AND Astra**.
* It closes on the first VALID pass with zero surviving breaches **and its denominator**: the five decline labels,
  the accept cells, and entries 14 and 13/17.

**P5 -- gates and commit mechanics**
* Run the two-part clearance again after the three pending commits, then gate 14 (`gate_arm`) targeted, plus gate 6
  and precommit.
* Commit **by name**, never `-A`:
  * `dev_sgi_ip32.c`, `gate_arm.sh` and `crime_width_probe.py` **together** (the `untrackeddetectors` ordering
    constraint);
  * `check_score_claims.py` (the hyphen fix; reconcile `scorehyphenfp`'s "closed");
  * #529's checker and precommit lines, plus 39 new MANIFEST entries;
  * the artifacts **excluding `ctl0c_discharge_20260917/bin/`**;
  * the CHANGELOG block, the OUTSTANDING_BUGS closure, and the ledger (CRLF, `newline=""`).
* Decide what happens to the 5 rung-3 MANIFEST entries: stage their files, or move them out of #529's commit.
* The next commit owes #529's pass-2 receipt in `regress/pass2_ledger.tsv`.

**Pending rulings, summarised**
* the three first-hand re-rulings (P1.2);
* whether the Q3 clause enters the carrier (a rule question, currently unadopted);
* #529's slot relative to `scexempt`.

---

## 4. Is the working-tree #529 material consistent?

| check | result | evidence |
|---|---|---|
| probe rows vs gate pins | **consistent**: 204 = 204 x3 | [COMPUTED] stub run; [READ] gate :1916-1922 |
| last measured base legs vs pin | consistent: table 12 base 204/204, ctl0c base 204/204 | [READ] |
| row-name distinctness (owed by PRETABLE "to the base leg") | all 204 distinct | [COMPUTED] |
| measured instrument vs current probe | **differs**: docstring era tags, plus #546's one equivalent code line | [COMPUTED] diff + AST |
| gate ORDER-warrant comment | **false today** (mtime 09-23 15:25:36) | [COMPUTED] `ls --full-time` |
| SCORE_CLAIMS manifest count | consistent: PINNED 32 = MANIFEST 32, PASS | [COMPUTED] |
| SCORE_CLAIMS manifest note | **stale** (188 rows; history retold) | [READ] precommit :339 |
| check_probe_wiring #529 description | **stale** (141 / pin 141) | [READ] :873 |
| check_score_claims at HEAD vs probe | **FAIL** (4/8) until the hyphen fix commits | [COMPUTED] |
| probe contract vs rows | rows implement items 1-10, the K-class and repair 14's accept cells.  **Gaps**: HARD_RESET rows unnamed; D1 not conditional (:413); `+2` translations undisclosed; "filed" rows that do not exist; tables cited only through killtable10.  The statement "Carriers for TIME and REV, and label-swap mutants for INTMASK and CONTROL-write, are OWED and are not in this file yet" (:337-338) is **accurate** | [READ] |
| dev_sgi_ip32.c across trees | consistent: `8c1d1545` everywhere; p1 CLEAN x4, p2 FRESH x3, est/ N/A | [COMPUTED] |
| divergence set | `dev_sgi_ip32.c` is not in `tools/est_divergence.txt` (6 entries derived), so the clearance applies | [COMPUTED] |

---

## 5. The smallest safe next step, and what would make resuming unsafe

**Smallest safe next step** [INFERRED].  After #549 commits and 087a90's commit scripts have restored the working
files:
1. Re-verify that `gate_arm.sh`, `dev_sgi_ip32.c` (`8c1d1545`) and the probe (`a0af7c92`) are byte-unchanged, and
   that the checker and precommit diffs against the new HEAD hold only #529's lines (plus the 5 rung-3 entries).
2. Re-take the temp-index snapshot, so blob `4f76458e` exists in git.
3. Do the P1 records work, and fire the Fable+Astra re-rulings.
4. **Table 13a**: measurement only, three legs (base, `latch_label(CRIME_INTMASK)`, `latch_label(CRIME_CONTROL)`), in
   a fresh clone, PRETABLE first.

It edits nothing in any project tree and answers the ruling's open "measure, don't derive" item.

**What would make resuming unsafe right now**
* **Before #549 lands**, staging anything breaks 087a90's commit scripts.  They refuse a non-empty index and
  "something else is staged".  The index is FREE today [READ CHECKPOINT; COMPUTED 0 staged].
* **Contention.**  The probe's TIME rows are wall-clock oracles.  Do not run concurrently with the Sunday 09-27 18:00
  battery, any gate or kill table, or panel CPU load.
* **Committing as-is would ship wrong records**, in the precommit history, the MANIFEST description, the gate
  comments and the phantom filings.  It would also fail HEAD's `check_score_claims` without the hyphen fix, and would
  sweep 18 MB of binaries if the artifacts dir is added wholesale.
* **Building repair 15 on `FABLE_RULING_20260917.md`'s stop condition** without a first-hand re-ruling contradicts the
  standing "a fallback is a seat failure" rule.
* **Build trees carry other units' uncommitted `src/` deltas** today (dev_fbctrl, dev_lca, dev_pcc2, dev_sh4,
  cpu_alpha_palcode, mvme_pcctworeg.h).  Name the baseline for table 13a and rebuild it in the clone, per the
  kill-table recipe.  `dev_sgi_ip32.c` itself is clean everywhere.
* **Scratch clones.**  #529's clones (`/tmp/gxopus_r14`, `/tmp/gxctl0c`, `/tmp/gxopusc8`, `/tmp/gxopuscrime`,
  `/tmp/gxopuscrimec7`) are sentinel-free at `8c1d1545` [COMPUTED].  Eleven OTHER rounds' `/tmp` clones hold
  `.MUTANT` sentinels (gx514m, gx514pre, gxasan_m0, gxcensusB, gxfix, gxo496p2_m1/_m2, gxopus540p3i, gxpcc2b,
  gxpcc2b5, gxpio_fix).  They are not #529's; do not reuse them.

---

## Appendix -- how each number here can be re-derived (all read-only)

* **Diffs**: `git -C GXEMUL-SEC diff HEAD -- <file>`; `git diff --numstat HEAD -- ...` gives dev +32/-2, gate +59/-0,
  checker +219/-36, precommit +11/-4, check_score_claims +21/-1.
* **Probe row count**: `p529/probe_stubcount.py FAKEBIN stub` gives `CRIMEP_RESULT=9/204`, `SESSIONS=56`.  The 9 are
  want-zero count rows that pass on an empty transcript; not a measurement.
* **HEAD's score checker against the working tree**: `python p529/csc_head.py` (HEAD's file with ROOT pinned).
* **Wiring**: `python tools/pipeline/check_probe_wiring.py` gives `PROBEWIRING_FAIL 79`; output in `p529/cpw_run.out`.
* **Clearance**:
  * Windows trees: cmp and `-nt` in git-bash;
  * WSL: `p529/clear529_ro.sh` via `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/.../clear529_ro.sh`.
* **Provenance**: the per-message `model` and `stop_reason` in `subagents/agent-<id>.jsonl`; the `Write` tool_use
  file_path shows which model wrote each ruling.
* **Files in `p529/`**: `ledger_crimewidthkill.json`, `ledger_entries_tail.txt` (entries 95-154),
  `flagship_0918_final.txt`, `probe_snap0921.py`, `cpw.diff`, `ledger_HEAD.json`.
