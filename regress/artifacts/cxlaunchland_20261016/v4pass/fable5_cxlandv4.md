FABLE_CXLANDV4_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP WITH CHANGES (7)

**Evidence basis.**  Fable 5.1, the v4 pass, 2026-10-17 02:1x-02:3x.  READ: the whole packet; `tools/cxlaunch.sh` (md5
`ee4f5aec`, the md5 RECEIPT_v4 and KILLTABLE_v4 name; its mtime 01:23:15 precedes both receipts, 01:28:35 and 02:06:07);
`run_controls_v4.sh`; `mut_launcher_v4.py`; `run_mutants_v4.sh`; `census_v4.py`; the fixtures; the tracked (`cb180d9d` on
disk) and before (`3c51a757`) launchers.  MEASURED, in scratch copies OUTSIDE the project (nothing written to any project
tree but this file): the base controls 116/116 (02:15:56; 102 launcher runs in 63 s wall with a second batch running --
about 0.6 s each, so `timeout 120` is two orders of magnitude clear); TWELVE one-edit mutants of my own through the 116
controls, every run carrying its `CXLAND_CONTROLS_DONE` sentinel; a census of my own over 2,425 codex `.err` files, 8,590
`.err` files of any name and 488 launch-log rows; four PROPOSED rows and three content checks run against the three
launchers and against the mutants they are meant to kill.  NOT re-run: the 32-mutant table (37 min; forbidden in the
foreground and not needed -- its receipt names the md5 of the file I read; I checked its red sets by reasoning, Q3a).
The v3 -> v4 launcher diff is 0 non-comment lines (MEASURED).  The scratch receipts sit at a VOLATILE path
(`...\scratchpad\cxv4\SUMMARY*.txt`, `CENSUS_fable.txt`, `run_controls_v4x.sh`, `run_controls_v4y.sh`, `mkmut*.py`); I may
not copy them into the tree, so every number is reproduced here and every mutant is given as its exact edit.

## The finding, before the questions

The CONTRACT's sentence -- *"every decision the file makes is pinned at its edges or disclosed below"* -- is FALSE, and
testing that sentence was this pass's job.  Reading the launcher line by line against the CONTRACT finds decisions it
neither pins nor discloses; one-edit mutants of them pass all 116 controls.  ALL MEASURED:

| # | decision (launcher line) | one-edit mutant (exact edit) | 116 | on record |
|---|---|---|---|---|
| F1 | `if [ "$rc" -ne 0 ]; then ... exit "$rc"; fi` (169): codex's own nonzero rc passed through | `m_rcpass`: that `if [ "$rc" -ne 0 ];  then` (two spaces, unique) -> `if false;  then` | **116/116 ESCAPES** | the shape it guards -- rc != 0 WITH an answer and no refusal/wall text -- is off the diagonal: 0 of 488 launch-log rows (448 rc-0-with-stdout, 40 rc-1-empty, nothing else; same answer as the header's 0 of 387 and Astra's 0 of 394) |
| F2 | the fallback trigger's THIRD conjunct `[ "$AUP_MODEL" != "$MODEL" ]` (148) | `m_samemodel`: delete ` && [ "$AUP_MODEL" != "$MODEL" ]` | **116/116 ESCAPES** | nothing on record sets `CX_MODEL` (grep of `tools/` and `_scratchpad`: only the launcher copies' own defaults); the property it keeps is "re-run ONCE" when the brief was asked on Daybreak itself |
| F3 | the override's DISABLE semantics: `${CX_AUP_MODEL-...}` (78, the `-`) and the conjunct `[ -n "$AUP_MODEL" ]` (148) | `m_aupcolon`: `:-` for `-`; `m_noempty`: delete ` && [ -n "$AUP_MODEL" ]` | **116/116 and 116/116 ESCAPE** | production never sets it empty -- but 24 of the 34 rows rely on `CX_AUP_MODEL=` disabling the fallback and NO check counts their calls.  Under either mutant P2, Q1, A1 and R2X FIRE the fallback (with `-m ""` under `m_noempty`), the fake replays the same fixture, the exit is the same: 11 `AUP FALLBACK` lines in each mutant's log against the base's 7 (D1/D2/D4 before+after, D3 after) |
| F4 | `strip_ansi` on the HEADER path (102): `HDR=$(strip_ansi "$ERR" \| awk` | `m_hdrnostrip`: `cat "$ERR"` there only | **116/116 ESCAPES** | **149 of 975 opening blocks on record carry ANSI inside the block, 105 of them on ANSWERED runs** (panel.sh and cxfarm captures; the real R2 header reads `ESC[1mmodel:ESC[0m gpt-6-astra`); 0 of this launcher's own captures.  Unstripped, `grep '^model:'` misses the line: the run says "model UNVERIFIED" and a MISMATCH exits 0 instead of 5.  The table's `m_nostrip` strips NEITHER path and is killed by A1, Q3, R2X, D3 -- all rc 1, all through the `ERROR:` path -- so the table never tested this half |
| F5 | `< /dev/null` on codex's stdin (94) | `m_nostdin`: delete ` < /dev/null` | **116/116 ESCAPES** | the carrier: "the `< /dev/null` is required (the trailing-`-` stdin form died silently once)"; the fake reads no stdin, so nothing can see it |
| F6 | the output file names `codex_<tag>.txt/.err` (81) | `m_txtname`: `.txt` -> `.out` in `TXT=` | **116/116 ESCAPES** | the pack runner and panel.sh read `codex_<tag>.txt`; no check opens an AFTER row's answer file (D1 opens only `.refused.err`) |
| F7 | the ALTERNATIVES inside the refusal and wall patterns (136-137) | `m_refpat`: keep only `flagged for possible cybersecurity`; `m_wallpat`: keep only `usage limit` | **116/116 and 116/116 ESCAPE** | **six of the eight alternatives have ZERO instances**: `cannot help with`, `can.t help with`, `I won.t help`, `quota`, `rate limit`, `not authenticated` match 0 of the 1,095 column-0 `ERROR:` lines (ANSI-stripped, case-insensitive) in 2,425 codex `.err` files; `flagged for possible cybersecurity` 456 lines / 308 files, `usage limit` 209 / 143; every fixture carries only those two |
| -- | `sed 's/[[:space:]]*$//'` on the model line (107) | `m_trailws`: drop that second `sed` expression | 116/116 escapes | 0 of 975 opening-block `model:` lines carry trailing whitespace or CR -- EQUIVALENT on record |
| -- | the banner anchor `/^OpenAI Codex/` (103) | `m_bannerun`: unanchored | 116/116 escapes | 0 files carry a non-column-0 `OpenAI Codex` before the column-0 banner in their first 12 lines -- equivalent on record |
| -- | `grep -ic` (case) on the refusal pattern (136) | `m_nocase`: `-c` | 116/116 escapes | 0 upper-case variants of any alternative on record -- equivalent on record |

**Grading.**  F2 and F3 are conjuncts of the PREDICATE THE LANDING INTRODUCED -- the fallback trigger; the tracked file has
no fallback -- left unpinned: clause (d) by the floor's own letter, L2, repair in-round, and the repair owes its own scoped
pass.  F4 is the sharpest: a one-edit mutant that breaks a RULED property ("a different model named by codex's OPENING
header exits 5") on a stderr shape on record in 105 answered runs; the strip was added by this very landing BECAUSE a
panel-transport file (R2) was coloured, so "0 on this launcher's own captures" does not make the shape foreign -- L2.  F1
is the site of the file's founding defect #2 ("exited 0 while holding codex rc=1"); its shape is 0 on record like
`m_eq1`'s, so DISCLOSE is consistent with the pass-2 ruling -- but the fixture that pins it is N4's shape without the
quoted wall (N4 is already rowed at rc 1 with an answer), no realism objection N4 does not carry, one row: I say PIN.
F5-F7 are completeness: the CONTRACT claims each decision and these are decisions.  The launcher's CODE is right on every
on-record shape; what is wrong is the RECORD of what the controls cover.  So: SHIP WITH the rows below added, not DO NOT
SHIP -- and the chain does NOT close on this pass (seven breaches of its own sentence, three of them floor-shaped).

**The rows, MEASURED in scratch copies of `run_controls_v4.sh`** (`run_controls_v4x.sh`: +RC1A, D5, SI and three checks =
37 rows, 129 checks, BASE 129/129 in 97 s; `run_controls_v4y.sh`: +CH = 38 rows, 133 checks, BASE 133/133).  Every proposed
expectation holds on the tracked, before AND landed launchers, and each kills its mutant:

| row / check | fixture | tracked / before / after | kills |
|---|---|---|---|
| RC1A | rc 1, an answer (`ans_verdict.txt`), ANS's clean header, fallback off | 1 / 1 / 1 | `m_rcpass` 128/129 (RC1A after exit 0, want 1) |
| D5 | P2 (a refusal) asked as `CX_MODEL=gpt-daybreak-blue-latest`, fallback ON; check `args_D5_after` = ONE call | 7 / 7 / 7 | `m_samemodel` 128/129 (two calls) |
| P2 one-call check | `grep -c '^CALL$' args_P2_after` = 1 -- the fallback DISABLED by `CX_AUP_MODEL=` | content check | `m_aupcolon` 128/129, `m_noempty` 128/129 |
| CH | ANS's header with its `model:` label coloured exactly as R2's (`sed "s/^model:/${ESC}[1mmodel:${ESC}[0m/"`), rc 0, asked gpt-6-other; check: the log names the mismatch | 0 / 0 / 5 | `m_hdrnostrip` 131/133 (CH after exit 0, want 5; UNVERIFIED instead of the named mismatch) |
| SI | ANS, with the launcher's OWN stdin fed a marker file (the harness gives every other row `/dev/null`: `< "${STDIN_OVERRIDE:-/dev/null}"` in `run()`); the fake writes `head -c 60` of its stdin to `$FX_ARGS.stdin`; check: the marker does not reach it | 0 / 0 / 0 | `m_nostdin` 128/129 |
| N1 file check | `out_N1_after/codex_N1.txt` and `.err` exist and are non-empty | content check | `m_txtname` 128/129 |

For F7 and the three equivalent-on-record edits I do NOT ask for rows: 0 instances on record is the pass-2 ruling's own
criterion for DISCLOSE, and a synthetic `ERROR: quota ...` would pin nothing real.  I ask that the CONTRACT disclose them
WITH THE DERIVER (`census_v4.py` can carry the per-alternative count), because a reader of the pattern today believes
eight shapes are covered and the fixtures cover two.

## Q1 -- my own findings in section 2

I have none: the Fable seat STALLED on the v3 pass (confirmed -- `v3pass/` holds no `fable5_*` file), so no V-row is
mine.  I reviewed all sixteen anyway; that is Q5.  The packet's attribution of the two stalls to "the whole kill table run
as ONE foreground command" is a guess labelled as one ("most likely"); the hazard is real (37 min against a 600 s
watchdog), and this run put every long thing in the background and lost nothing.

## Q2 -- the enumeration: every decision I checked, by launcher line

| line | decision | CONTRACT | my check |
|---|---|---|---|
| 73 | `set -u`; `$1 $2 $3` | not listed | not a decision: a missing argument is a bash error (exit 1); apparatus-level |
| 74, 88 | `PROJ` hardcoded; `cd "$PROJ" \|\| exit 9` | DISCLOSED | agreed: untestable without editing the file |
| 75 | `CX_CODEX_BIN` override | E0 (an override-ignoring AFTER runs the REAL CLI and leaves no args log) | note: for the AFTER column HOME is not redirected, so that detection COSTS 34 real codex calls; a `HOME="$T/home"` for all three columns would let the fake absorb it.  A design note, not a change |
| 76-77 | `MODEL` default `gpt-6-astra`, `EFFORT` default `ultra` | E1/E2 (the whole argument sequence), N1's identity compare | pinned |
| 78 | `AUP_MODEL` default; the `-` (empty disables) | the default by E2; **the `-` by nothing** | F3 |
| 79 | `AUP_EFFORT` default `ultra` | E2 | pinned |
| 81 | `codex_<tag>.txt/.err` | **not listed** | F6 (the `.refused.err` rename IS pinned, D1) |
| 84-86 | `wc -c`; the argv cap `-gt 30000` | X14/X15 | pinned at both edges.  A MISSING brief file is unhandled (`sz` empty, `[ "" -gt ... ]` errors, codex gets an empty brief) -- apparatus-level, no row asked |
| 90 | `strip_ansi` = `ESC [ [0-9;]* [A-Za-z]` | A1, Q3 through `CXERR`; `m_sgr` disclosed | **the HEADER use is unpinned** -- F4.  The `m_sgr` disclosure's premise re-derived: 8,590 `.err` files of any name, 198 carry ESC, 0 carry a non-SGR CSI or an OSC; 2 (`lcabadval/codex_audit*_20260910.err`) carry a bare `ESC`+space that neither strip touches -- consistent with "0 non-SGR CSI or OSC in 4,851" at a larger scope |
| 93-94 | the argument list; `> $TXT 2> $ERR < /dev/null` | E1/E2 whole | `< /dev/null` unpinned -- F5 |
| 102 | window `NR > 12 && h < 2` | W12/W13, X13, X9/X10 | pinned at both edges.  Banner histogram on record {line 2: 974, line 4: 1} -- X13 is the one; the launcher's "line 5 in 599 of 600 and line 7 in one" holds at 975 (model at 5: 974, at 7: 1) |
| 103 | `/^OpenAI Codex/` | not listed | equivalent on record (`m_bannerun`); one disclosure line |
| 104-105 | the rules `/^--------/`; the closing `exit` | M1/X5; `exit -> next` disclosed with the census | agreed; my census agrees with CENSUS_v4 at +3 files (975 blocks of 2,425, 0 without exactly one model line, 0 unclosed) |
| 106 | cap `++n > 30` | K30/K31 | pinned at both edges; unclosed blocks 0 on record -- the cap exists for a 0-instance shape and pinning its constant is still right (v3's `m_nocap` escaped) |
| 107 | first `model:` (`-m1`); the two `sed` trims | `-m1 -> -m2` disclosed; **the trims not listed** | `m_trailws` equivalent on record |
| 131 | `^ERROR:` anchor, `grep -a` | X1, X8 | pinned |
| 132 | `verd` | -- | computed and PRINTED only; no decision reads it (which is why X2 pins `body`, not `verd`) |
| 135 | gate `rc -ne 0 \|\| body -eq 0` | N1, N2, X2, N4; `m_eq1` disclosed | agreed; the `m_eq1` shape is 0 of 488 launch-log rows (MEASURED) |
| 136-137 | the patterns' alternatives; `-ic` | **not listed** | F7; case equivalent on record |
| 148 | the fallback trigger: `refus -gt 0` AND `-n AUP_MODEL` AND `AUP_MODEL != MODEL` | first conjunct: D1-D4, FB1/FB2; **second and third: nothing** | F3, F2 |
| 151 | the two `mv -f` renames | D1 (`.refused.err`), FB1 (nothing renamed) | `.refused.txt` unpinned but empty on every refusal -- no change |
| 153-154 | the Daybreak run; `ANSWERED_BY=$AUP_MODEL` | D1 (credited), D2 (compared against Daybreak) | pinned |
| 157-162 | refusal -> 7, `-gt 0` | P2, Q1, A1 (1), R2X (2) | pinned at both edges |
| 163 | wall -> 8 | W1L (1), P1 etc. (2), N4 (6) | pinned |
| 164 | empty -> 6 | N3, X1 | pinned |
| 165-168 | identity -> 5 | M1, D2, X5, W12, K30, X13; UNVERIFIED by M2, X6, X9, W13, K31 | pinned -- for an UNCOLOURED header (F4) |
| 169 | `rc -ne 0 -> exit rc` | **not listed** | F1 |
| 170-174 | the two final messages | M2/X6 (`m_claimmodel`) | pinned |
| order | 7 before 8 before 6 before 5 before rc | refusal-before-wall DISCLOSED (`m_prec`: "0 of 410" -- MEASURED 0 of 411 at +1 file) | 6-before-5 (an empty stdout AND a mismatching header) is unrowed and undisclosed: REASONED only, not built; 0 on record is likely, since every rc-1 run on record is a refusal or a wall.  One disclosure line |

Premises of 2b: W12/W13 and K30/K31 are synthetic shapes real runs do not produce (975 blocks: banner at 2 or 4, 0
unclosed) -- they pin CONSTANTS, which is what an edge row is for, and the packet says so.  X13 and R2X are real: R2 is
BYTE-IDENTICAL to `_scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err` (`cmp`), 0 column-0 `ERROR:` lines
unstripped and 2 stripped; and the real fallback receipt (`dossier_gdromdma.launch.log`, read whole) shows `refusal: 2` on
Astra, then Daybreak credited -- so the doubled refusal is PRODUCTION's shape and V4's `-eq 1` mutant would have broken
the real fallback, not only the table.  `timeout 120`: MEASURED about 0.6 s per launcher run under load.

## Q3 -- the kill table and the floor

(a) *Killed for a reason other than the one named?*  READ against the red sets: every named control is in its mutant's
red set (the runner enforces that), and each red set is what the named mechanism predicts -- `m_fbge0` 113 = FB1 exit
(the fallback fires on an answer, the replayed N1 is credited to Daybreak and its astra header exits 5) + FB1 content +
FB2 content; `m_twice` 113 = D3, D4, E2 call counts; `m_argv1` 113 = X15 exit, X15 content, E0's `extra`;
`m_nofallback`'s D4 red is its call count (1, not 2); `m_nogate`'s M1/X5 reds are N1's quoted walls read under other
model names.  One caveat the table cannot show and the CONTRACT turns into a false record: **`m_nostrip` is killed
entirely through the `ERROR:` path** (A1, Q3, R2X, D3: all rc 1), so its kill says nothing about the header path -- F4.
I did not re-run the 32.

(b) *A one-edit mutant not in the table that passes all 116 and breaks a ruled property?*  YES -- twelve measured
escapes above, nine of them at decisions the CONTRACT does not mention.  Ruled properties broken: "re-run ONCE" (F2: asked
on Daybreak and refused, the mutant re-runs Daybreak); the controls' own "fallback disabled" premise (F3); "a different
model exits 5" on a coloured header (F4); "otherwise codex's own nonzero rc" (F1).  Shapes swept and NOT found escaping,
or equivalent on record: the window and cap constants (pinned), the first-`model:` rule, the gate's two operands, the
anchor and `-a`, the multiplicity guards at both sites, the identity compare and its UNVERIFIED branch, the argument list,
the renames, the exit ORDER (6-before-5 unbuilt, Q2), the `verd` count (no decision reads it).

## Q4 -- the records (section 5)

TRUE, checked: 5a's bracket on the "greps stdout freely" lines (the tracked file's line 44 greps `$TXT` -- READ); 5a's
`cxlaunchdaybreak` closure's real-run receipt (`dossier_gdromdma.launch.log` carries `refusal: 2`, `AUP FALLBACK:
re-running ONCE`, `answered by: gpt-daybreak-blue-latest` -- READ whole); 5a's "this filing never had a ledger row"
(`cxlaunchwallfp`: 0 ids in `ledger.json` -- MEASURED); 5b's witnesses (N1/N2 8 -> 0, D1 7 -> 0: RECEIPT_v4 lines, and the
receipt's three md5s match the three files on disk -- MEASURED); 5c's V12 bracket (MEASURED at `c64445fa`: OB:22494-22503
is `asanfifteen`'s body into `cxlaunchwallfp`'s heading at 22502; :24714-24716 is `stagetokenscontrols`; ledger :62489
is `"id": "armvecrecurse"`); 5d's "every real wall and refusal on record is rc 1 with an empty stdout, and every rc-0 run
carries an answer" (MEASURED: 448 + 40 of 488, nothing off the diagonal); 5d's "29 ... killed, the three escapes filed"
(29 + 3 = 32); V10's "0 of 410" (MEASURED 0 of 411; the rc-0 runs that quote both are `pass2/codex_cxland.err`,
`adj_20261016/astra/C_records/codex_adjC.err` and `v3pass/codex_cxlandv3.err` -- the packet names one and says
"exist", which is true).

FALSE, one sentence in three places: **"its header is the CONTRACT -- which edge of EACH decision this file makes is
pinned, and which is deliberately not"** (the launcher header, lines 67-69); **"every decision the file makes is pinned
at its edges or disclosed below"** (`run_controls_v4.sh` line 33); **"Its header is the CONTRACT: each decision the
launcher makes, the rows that pin its edges, and what is deliberately not pinned"** (the 5d CHANGELOG draft).  Seven
decisions are neither.  Correct all three after the rows land, or soften "each/every" to the enumerated list.  Also:
`cxlaunchunpinned`'s title says "three one-edit escapes are unpinned by ruling" -- after this pass the DISCLOSED escapes
are more (F7's six alternatives; the three equivalent-on-record edits; the 6-before-5 order); carry them in the row or in
the CONTRACT, and the CHANGELOG's "[to be written]" V4-pass sentence must say the pass found the CONTRACT INCOMPLETE,
not that it verified it.  Not checked: the "0 of 394 launcher rows" scope (Astra's; mine is 0 of 488), the "0 of 330
launcher-captured answered runs lack a header" count, and the pack runner "special-cases 7 and 8 only" (no runner under
`_scratchpad/codexpack_20260928/` or `tools/` reads `LAUNCH_RC` by that name; READ as the packet states it).

## Q5 -- which of the 16 accepted dispositions is wrong?

Checked: 16 of 16.  Wrong as stated: NONE.  V1-V7 hold against the awk/shell semantics and the table's red sets (e.g.
`m_win11` reds only W12 because X13's rule is at line 5; `m_cap29` reds K30 because `++n > 29` exits before printing body
line 30; `m_fbeq1` reds D3 because the real doubled refusal is count 2); V8, V9, V13, V14 are in the files; V10, V11, V12
MEASURED above; V15's census agrees with mine; V16's `d` marks sit only on answered seats.  What is wrong is one level
up: v4's claim to be the CLASS CLOSURE.  The class -- a decision of the launcher whose edge no fixture straddles -- has
further members the enumeration missed, because it was derived from the three passes' FINDINGS rather than from the
file's PREDICATES.  The derivation that finds them is Q2: every `if`, `[ ]`, conjunct, pattern alternative, redirect and
constant, each asked "which row goes red if this changes".

## The changes, ranked

1. **F3** (L2): the P2 one-call check -- pins the disable (`-` and `-n`) that 24 rows silently depend on.  One line.
2. **F2** (L2): row D5 (7/7/7, one call) and a CONTRACT line for the third conjunct.
3. **F4** (L2): row CH (0/0/5) and the CONTRACT's strip line split into its two uses (`CXERR`: A1/Q3; `HDR`: CH).
4. **F1** (L4 + pin): row RC1A (1/1/1) and a CONTRACT line for `rc -ne 0 -> exit rc` -- or disclose it with the 0-of-488
   census, but the CONTRACT must carry it either way.
5. **F5**: row SI, with the harness giving every row an explicit stdin and the fake recording its own.
6. **F6**: the N1 file-name check.
7. **F7 + the three equivalent-on-record edits + the 6-before-5 order**: DISCLOSE in the CONTRACT with the deriver
   (six dead alternatives, 0 of 1,095 column-0 lines; trailing-space trim, banner anchor, case: equivalent on 975 blocks).
And the three "each/every decision" sentences corrected (Q4).  The repair owes ONE pass scoped to its diff; the stop
condition is the Q2 enumeration verified against the new rows, not another hunt.

## What I could not check

The 32-mutant table was not re-run (its receipt is of the same md5).  Astra's two census scopes (394 rows; 4,851 files)
were not reproduced at their scope -- mine are larger and give the same answers.  The pack runner's exit-code handling
was not found.  The scratch receipts for every number above live at a volatile path I may not copy into the tree; the
main loop should re-derive them from the exact edits given here or copy them before the record cites them.
