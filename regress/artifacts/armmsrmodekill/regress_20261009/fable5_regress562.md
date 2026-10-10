FABLE_SEAT_ALIVE_20261009_R562
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: REGRESS WITH FINDINGS (2) -- the committed detector discriminates exactly as recorded (parent 18/47 with the 29 named reds, commit 47/47, row-for-row and diag-for-diag identical to run_head.out / run_fixed.out on fresh builds of both shas in my own clone); nothing landed that differs from what I ruled on except records I name below; two L4 records corrections owed, no code.

REGRESS seat: Fable 5.1, fired 2026-10-09 14:3x on `4f908ad5` (parent `04f3e7c0`).  Badge: none of #562's product or detector
work is mine; I adjudicated the main loop's nine rulings this afternoon (`fable_adjudication_20261009/`), and this is the
review of what then landed, including my own three requested changes.

## What I READ and what I RAN (kept apart)

READ (repo objects at `4f908ad5`, via `git show` / `git archive` -- no index-writing git command, no plain `git status`):
`git show --stat`, `--name-status` and the full commit message; the landed `src/` diff (`git show --format= 4f908ad5 -- src/`)
against `fable_adjudication_20261009/diff562_src.diff`; the committed `regress/arm_msrmode_probe.py` in full (all 1273
lines); the committed `regress/gate_arm.sh` section (`:1946-1993`) against `gate14_20261009/gate_arm.TESTED.sh.txt`; the
`check_probe_wiring.py` and `precommit_check.sh` hunks; the CHANGELOG block and the OUTSTANDING_BUGS section in full; the
`ledger.json` diff (574 lines) -- the `armmsrmodekill` row's `state`/`witness`/`state_note`/`closure`, all 59 added seat
entries, the five new rows, the `armthumbabortkill` hunk; the `matrix.html` chip lines; `killtable5_20261008/run_head.out`,
`run_fixed.out`, `HEAD.sha`, `SHIPPED_vs_FROZEN.txt`, `PRETABLE5.out`'s head and tail; `gate14_20261009/gate14_run2.out`'s
clearance header and gate-14 tail, `gate_arm_msrmode_run2.log`'s trailer; `regress/artifacts/armmmuvehicle/brief.md` and the
head of `agy_research_20261008.txt`; `src/cpus/cpu_dyntrans.c:260`, `src/include/arm_cpu_types.h`, `machine_test.c:212-215`
(for finding 2).

RAN (nothing written to any project tree; everything under my scratchpad and `/tmp/gxfable562` in WSL Gentoo):
* `git archive 04f3e7c0` and `git archive 4f908ad5` into tarballs; extracted (minus `regress/artifacts/`) to
  `/tmp/gxfable562/{parent,commit}`; `./configure` + `make -j4` in each (CONFIGURE_RC=0, MAKE_RC=0 both); checked
  `[ gxemul -nt src/cpus/cpu_arm.c ]` in each (parent binary 14:35:47 over a 13:22:03 source; commit binary 14:36:55 over a
  14:18:29 source -- both NEWER, both ok).  md5 of the four ARM sources in each tree recorded in `work/build562.log`.
* The COMMITTED probe (`/tmp/gxfable562/commit/regress/arm_msrmode_probe.py`, md5 59b99365 = the committed blob), ONE
  instrument for both runs, sequentially, python3 3.13.12:
  `python3 -u arm_msrmode_probe.py /tmp/gxfable562/parent/gxemul PARENT_04f3e7c0` (14:37:39-14:46:50) and
  `python3 -u arm_msrmode_probe.py /tmp/gxfable562/commit/gxemul COMMIT_4f908ad5` (14:46:50-15:03:40); both logs end in
  `ARMMSRMODE_DONE`; saved as `scratchpad/c562/fable/work/probe_parent.out` and `probe_commit.out` -- a VOLATILE path, so
  if a durable record is to cite these numbers the main loop copies them into `regress/artifacts/` first (I am read-only).
* `ast.dump` (minus the module docstring) of the committed probe against `killtable5_20261008/probe_frozen.py`,
  `gate14_20261009/arm_msrmode_probe.TESTED.py.txt` and `opus_pass2r5_20261009/probe_frozen.py`, plus a docstring diff of
  each against the committed text (`work/astcheck562.py`, run under WSL python3 -I).
* `cmp` of est/ and the working tree against the commit's four ARM files; `git diff --stat ef577140 04f3e7c0` on them;
  `diff` of the comment-stripped committed gate against the TESTED copy; a per-entry parse of the ledger diff
  (`work/ledgercheck562.py`); greps listed inline below.

## 1. Does the committed detector still discriminate?  YES -- and identically to the records.

| run (my clone, committed probe) | RESULT | SESSIONS | REDS | TALLY_MATCHES_HEAD_EXPECT |
|---|---|---|---|---|
| parent `04f3e7c0` (`probe_parent.out`) | **18/47** | 43 | the 29 named rows | yes |
| commit `4f908ad5` (`probe_commit.out`) | **47/47** | 43 | none | no (correct on the fix) |

CONTROL=OK on both; every control row (`enc ok`, `live`, `pc adv`, `armed`, `no cbit`, `encl`, `grid cov`, `row count`)
green on both.  Stripping the free-text notes and diffing the row lines (name, got, want, status), the `diag` lines and
the trailers: **my parent run is IDENTICAL to the committed `run_head.out`, and my commit run is IDENTICAL to the committed
`run_fixed.out`** -- not just the tallies, every got string and every diagnosis.  The records' premise holds too: the
parent's four ARM sources are byte-identical to `ef577140`'s (`git diff --stat ef577140 04f3e7c0 -- <the four>` is empty),
so "HEAD ef577140: 18/47" transfers to the actual parent.

**Is every red on the parent red for the reason its row names?**  Every one of the 29 reds is `got=dead` -- EOF, the
probe's own oracle -- and where the probe diagnoses the death, the text it finds is the one the row's reason requires:
`kill 14` / `kill 15` "load mode 20 / 21 seen" (Load's `default:` with the driven value); `kill 1e` load mode 30, `kill 03`
load mode 3 (the two helper-domain rows die on exactly their values); `rst movs` / `rst ldm` / `latch ind` / `latch rpt` /
`msr lbl` / `msr wide` load mode 20; `zero spsr` load mode 0 (the never-written SPSR -- the no-MSR route); `dbg save` SAVE
mode 20 (the row is about Save's arm); `dbg both` save mode 20 only -- which is what the docstring says a HEAD run must
show ("HEAD dies in Save first"; it is not a HEAD reproduction of Load, and the docstring says so); `save 2s`
load=yes save=no, again as its note predicts ("dies on the FIRST MSR, the same Load death as kill 14"); the ten `src *` rows
load mode 15 (the first decline of SPSR_c 0xcf, mode 0x0f, through the restore); the three `grid *` rows load mode 14
(0x11 ^ 0x1f = 0x0e, the first G2 decline).  Two reds carry NO diag line because those rows never call `diag_unimpl()`:
`tbit` and `encl2`.  Their HEAD reason is attributed by reading, not by the probe -- `tbit`'s first unmodelled value is
`c_34` at T4 after three T-set ACCEPTS (0x3f is SYS32 + T), and `encl2`'s is `s_14` + `subs pc,lr`.  That is a
diag-coverage gap, not a detection gap (the rows red, and on the fix they want the exact T/mode words); adding
`diag_unimpl` to both is an AST change and belongs with `armmsrmodedebt`, not in-round.

## 2. Did anything land that the review did not see?  NO product or detector material; three records items I name.

* **`src/`** -- the four landed hunks are IDENTICAL to `diff562_src.diff` (the only differences are `@@` hunk-header
  function names and one `/*` line attributed to context instead of `+`, i.e. diff rendering of the same bytes).
  `est/` == commit and the working tree == commit on all four files (`cmp`).
* **The probe** -- the committed blob is md5 59b99365, the SAME file I adjudicated this afternoon.  AST minus the
  module docstring, re-derived this session: **412a7157 for the committed probe, `killtable5_20261008/probe_frozen.py`
  (8a9a9cac), the gate-TESTED copy (5ddc3242) and `opus_pass2r5_20261009/probe_frozen.py` (97555f3a) alike**.  So every
  kill table and both gate runs transfer to what landed.  The docstring diff TESTED -> committed is 7 lines, exactly the two
  sentences the commit message names (the probe48 loop row "pins it -- measured in the filed prototype", and the
  `KTR5_LANE4.out` citation).
* **Gate 14's section** (`gate_arm.sh:1946-1988`, `gate_end` at `:1990`) -- comment-stripped, IDENTICAL to
  `gate_arm.TESTED.sh.txt`; the only text change is the one comment the commit message names (lines 1952-1954, the
  "checked twice ... neither establishes row IDENTITY" sentence).  The committed `gate14_run2.out` carries the section at
  `ok` x 8 and "gate 14 ... PASS (1110 checks)"; its msrmode log is 47/47, REDS none, 43 sessions, zero ` FAIL ` row lines.
* **My three changes, verified in the landed text:** (1) `armmsrmodekill.state_note` now opens "[2026-10-09] #562 SHIPPED
  ... CORRECTION (GPT-6 Astra item 4, Fable 5.1 R9): ... 'which NO stepping row can see' -- FALSE: none of the SHIPPED 47
  rows sees it, but the filed loop prototype does (... probe48.py, KTR5_LANE5.out 47/48); the old text is kept below" --
  correct in place, old segment kept.  (2) The CHANGELOG block (the panel paragraph), the commit message and the
  closure note each carry the "After the owner lifted that hold, Fable 5.1 adjudicated ... RATIFY WITH CHANGES (3), all nine
  upheld ... corrections applied" sentence, with the durable path, and my adjudication sits at that path
  (`fable_adjudication_20261009/fable5_adjudication562.md`, with the brief and `diff562_src.diff` beside it).  (3)
  `PRETABLE5.out`'s CORRECTIONS section ends with the dated clause voiding the first line's mtime-order claim and the
  sibling-file rule.  Also taken: the kimi-k3 "new default: behaviour" ELSE is recorded FALSE in the CHANGELOG (R4), and the
  `rows failed` fragility is in `armmsrmodedebt`.
* **The 59 seat entries** -- 7 panels x 7 scriptable seats (agy, codex, deepseek, glm, grok, kimi, minimax) = 49, plus 7
  `opus5` entries (one per pass, `ev` = the `opus_*` or `witness_20261007` file), plus 3 `fable5` entries: a
  "[NOT A SEAT ANSWER] ... DELIBERATELY NOT FIRED" annotation for the held passes, a `design` CONFIRMED and a `review`
  CONFIRMED, both pointing at my adjudication file and summarising it accurately (I read all three in full).  Every one
  of the 56 non-fable5 entries names its panel dir (`panel_pass1_20261007` .. `panel_pass2r5_20261009`) or its opus dir --
  parsed, zero without.  The kimi entries record the transport (`kimi-k3:cloud`, CLI 403 on the last four) as a seat
  failure of that transport, not agreement.  `matrix.html`'s chips moved 709/149 -> 713/150 in-work/closed and 1906 ->
  1965 entries, which is +5 rows filed, -1/+1 for the closure, +59 entries -- consistent.
* **Wiring and precommit** -- `check_probe_wiring.py` gains the DETECTOR entry plus 35 artifact lines, and the commit
  holds exactly 35 `.py` files under `regress/artifacts/armmsrmodekill/` (`git ls-tree`), none missing from the diff;
  `SCORE_CLAIMS_MANIFEST` 32 -> 33 with its dated comment.
* **Not individually in the package I ruled on, all records/research, named here so nothing reads as hidden:**
  (a) `armthumbabortkill`'s `state_note` gained a prefixed "2026-10-07 pre-brief READING (Opus 5.5 ...)" segment, old
  text kept after `||` -- named in the commit message ("armthumbabortkill's pre-brief reading"); see finding 2.
  (b) Two files under `regress/artifacts/armmmuvehicle/` (`brief.md`, `agy_research_20261008.txt`) -- the agy research the
  filed `armmmuvehicle` row cites; the `stage562/` manifest I read at adjudication is no longer on disk, so I cannot
  re-confirm they were listed there, but the OUTSTANDING_BUGS text I ruled on cites the research path, so their landing
  is expected.  (c) `astra_confirm_20261009/codex_confirm562.err`, 7889 lines / 849 KB of codex stderr -- large, but the
  same practice as every committed `codex.txt`.

## 3. What the gate would not catch

**Finding 1 (L4, records): `killtable5_20261008/SHIPPED_vs_FROZEN.txt` is one edit behind the commit.**  Its last UPDATE
says "Installed probe md5 5ddc3242; AST minus the module docstring IDENTICAL to probe_frozen.py (8a9a9cac)".  5ddc3242 is
the gate-TESTED copy; the COMMITTED probe is 59b99365 -- Astra's post-gate two-sentence docstring edit came after that
note and the file was not appended again.  The identity claim is TRUE of the committed file (my AST check above:
412a7157 for both), but the file whose job is to record shipped-vs-frozen names a blob that did not ship, and the gate
comment at `gate_arm.sh:1980` sends a reader there.  One appended line: "UPDATE 2026-10-09 (after GPT-6 Astra's
confirmation): two more docstring sentences; committed probe md5 59b99365, AST minus docstring IDENTICAL to 8a9a9cac
(re-checked by the REGRESS seat)".  No gate reads the md5, so nothing is red; it is a wrong record waiting for a reader.

**Finding 2 (L4, records): `armthumbabortkill`'s new pre-brief note carries an "unchecked" claim the tree refutes, and
the refutation is in the same commit.**  Item (3) of the prefixed segment says "testarm's default SA1110 is ARMv4 with no
Thumb (seat's recollection, unchecked)".  Measured by grep: `arm_cpu_types.h` has no Thumb capability field at all
(`grep -i thumb` is empty; the SA1110 row is `{ "SA1110", CPU_ID_SA1110, 0, 14, 1, 14, 1 }`), and `cpu_dyntrans.c:260`
selects `arm_cpu_interpret_thumb_SLOW` on `ARM_FLAG_T` alone -- which is exactly what the committed `armmmuvehicle`
OUTSTANDING_BUGS entry records from agy's research ("no per-CPU Thumb capability flag -- the T bit alone selects the Thumb
interpreter -- which answers this row's open question").  The note labels the item unchecked, so it is honest; but a
reader of the `armthumbabortkill` row sees the recollection and not the answer.  One clause in that `state_note` ("(3)'s
Thumb question is ANSWERED in armmmuvehicle: T alone selects the interpreter") closes it.

**Notes, no change owed:**
* The `rows failed` check is still `grep -E ' want=' | grep -cE ' FAIL '` over whole row lines (`gate_arm.sh:1987`).  The
  new comment ("no row line may carry ` FAIL ' after its `want='") is literally true of what the code tests, but it does
  not say what my adjudication item 4 said: the check is green only because `note[:64]` cuts the `kill 14` note before
  its " FAIL " text, so a note edit can red the gate falsely.  That hazard IS recorded, in `armmsrmodedebt`'s gate-parser
  bullet, with the remedy (key on the verdict column).  Loud, the safe direction; filed; nothing further.
* Docstring vs rows, cross-checked by reading the committed probe: the NAMED-RED tally lists exactly the 29 rows the
  `EXPECT` constant builds (same order: labels outer, path inner, so `src dpi fiq, src pop fiq, ...`); "Rows added by #562"
  is 30 names and 17 + 30 = 47; 43 sessions re-derived from the session calls (one per scored dynamic row, `live`/`pc adv`
  sharing one, three static rows); `tbit`'s want `3f 3f 3f 33 33 33 n=3`, `latch rpt`'s want, `msr wide`'s 0xffffffd1
  ("bits 31:6, 4 and 0 only") and the grid counts 56/52/58 (computed from `len(obs)`) all agree with the code.  No row's
  expected value disagrees with the docstring.
* `tbit` and `encl2` have no `diag` line (above); a `diag_unimpl` call on each is a cheap addition for the `armmsrmodedebt`
  repair, not for this commit (AST change).
* `regress/arm_bfx_stub.bin` is untracked and not git-ignored in the working tree (dated Sep 7, from the earlier ARM
  probes); the probe creates it if absent, so the gate does not depend on it being committed.  Pre-existing, not #562's.
* Timing, for whoever schedules the battery: the parent run took 9 min 11 s (29 EOF deaths each waiting the 12 s reap) and
  the fixed run 16 min 50 s (the three grid sessions carry 56/52/58 debugger interactions each), alone on the machine.

## Something else?

Nothing in product code, the detector or the gate.  The two findings are records, both L4, both one clause.  I did not
re-run gate 14 (no gates, per the brief) and did not touch `build/`, `build-asan/`, `/tmp/gxsec-build` or `est/`; the
clearance claims in `gate14_run2.out`'s header are read, not regenerated.

Artifacts of this review (volatile, my scratchpad `c562/fable/work/`): `build562.sh`/`.log`, `runprobe562.sh`/`.log`,
`probe_parent.out`, `probe_commit.out`, `astcheck562.py`, `ledgercheck562.py`, the extracted diffs.
