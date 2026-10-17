# V5 PASS -- `cxlaunchquotation` / `cxlaunchdaybreak`: the codex launcher `tools/cxlaunch.sh`, v5 = the CONTRACT DERIVED FROM THE FILE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a shell wrapper that launches a read-only
review CLI and classifies its exit, and of the test harness that pins it.  READ-ONLY: write nothing to any project tree.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v5 launcher is `tools/cxlaunch.sh` in the WORKING TREE (uncommitted;
v4 is preserved as `regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v4.sh` -- v5 changes COMMENTS only, and its
executable lines are v3's); the controls and mutant table are `run_controls_v5.sh`, `run_mutants_v5.sh` and
`mut_launcher_v5.py` beside it, the census `census_v5.py` / `CENSUS_v5.txt`; the v4-pass answers are in `v4pass/` (Fable's
measurements copied into `v4pass/fable5_meas/`).  Everything a packet-fed seat needs is inlined below.

**Why v5.**  The v4 pass found the v4 CONTRACT INCOMPLETE: it was derived from the three earlier passes' FINDINGS, not from
the file (Fable 5.1), so decisions no pass had named -- codex's own rc passed through, the fallback's second and third
conjuncts, the header's ANSI strip, the stdin redirect, the output names, the pattern alternatives, both `-eq 0` body tests,
the default codex path -- had one-edit mutants passing all 116 v4 controls.  v5's CONTRACT is derived from the FILE: every
predicate, conjunct, pattern alternative, redirection, constant, exit-cascade order and caller-read log phrase, each asked
"which row goes red if this changes".  **This pass's job is to VERIFY THAT ENUMERATION**: is any decision of
`tools/cxlaunch.sh` missing from the CONTRACT (section 3b's header), or listed with a row whose edge does not really pin it?
The chain closes on the first pass whose zero floor breaches survive adjudication; if you find none, NAME THE DECISIONS YOU
CHECKED (a zero needs its denominator).  Check the premises in 2b; do not ratify them.

**Liveness:** open your answer with the token `GLM_CXLANDV5_20261017` on its own line, then your verdict line.

## 1. The v4-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (7)** (`v4pass/fable5_cxlandv4.md`; the seat ran on claude-fable-5-1 throughout, no
  fallback).  Twelve measured one-edit escapes of the 116 controls, every run carrying its completion sentinel.
* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`v4pass/codex_cxlandv4.txt`).
* **Grok 4.7 -- SHIP WITH CHANGES (5)** (`v4pass/grok_cxlandv4.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (5)** (`v4pass/glm_cxlandv4.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| U1 | Fable, Grok, Astra, GLM | codex's own nonzero rc (`if [ "$rc" -ne 0 ]; then ... exit "$rc"`) is pinned by nothing: `if false` passes all 116, so rc 1 with an answer and no diagnostic exits 0 -- the file's founding defect #2 | **PINNED**: RC1A (rc 1, an answer, a clean header -> 1), RC3A (rc 3 -> 3: the RAW rc, not a 1).  Mutants `m_rcpass`, `m_rcgt1`, `m_rcone` |
| U2 | Fable, Astra | the fallback trigger's third conjunct `AUP_MODEL != MODEL` is pinned by nothing | **PINNED**: D5 (a refusal asked ON Daybreak, the fallback on: exits 7, ONE call).  Mutant `m_samemodel` |
| U3 | Fable, Grok | the override's DISABLE semantics -- `${CX_AUP_MODEL-...}` (the `-`) and the conjunct `-n AUP_MODEL` -- are pinned by nothing, while 24 rows rely on them | **PINNED**: FD (every one of the 56 rows that sets CX_AUP_MODEL empty makes exactly ONE call; count pinned).  Mutants `m_aupcolon`, `m_noempty` |
| U4 | Fable, Grok, Astra | the HEADER's ANSI strip is pinned by nothing (`m_nostrip` was killed only through the `ERROR:` path); 149 of 975 opening blocks on record carry ANSI, 105 of them answered runs | **PINNED**: CH (the real coloured opening block of `fx/R2.stderr`, `ESC[1mmodel:ESC[0m gpt-6-astra`, on an answer asked as gpt-6-other -> 5, the log naming the mismatch).  Mutant `m_hdrnostrip` |
| U5 | Fable | `< /dev/null` on codex's stdin is pinned by nothing (the carrier: "the `< /dev/null` is required") | **PINNED**: SI -- every launcher run is fed a MARKER on stdin and the fake records what it reads; no after run's codex may read it (64 runs).  Mutant `m_nostdin` |
| U6 | Fable, Grok | the output names and redirections are pinned by nothing (`.txt` -> `.out` passes) | **PINNED**: N1F (N1's out dir holds exactly `codex_N1.txt` and `codex_N1.err`, byte-for-byte the fixture's stdout and stderr).  Mutants `m_txtname`, `m_errname`, `m_swapio`, `m_nomkdir` |
| U7 | Fable (DISCLOSE), Astra, Grok (PIN) | six of the eight pattern alternatives (`cannot help with`, `can't help with`, `I won't help`, `quota`, `rate limit`, `not authenticated`) and both `-i` folds are pinned by nothing; 0 instances of each on record | **PINNED**, against Fable's DISCLOSE: RF1-RF3 and WL1-WL3 (one alternative each), RFC and WLC (the case fold) -- synthetic rows pinning constants, as K30/K31 pin the cap.  `CENSUS_v5.txt` names the counts (0 lines of each, of 1,095 column-0 `ERROR:` lines).  Mutants `m_ref1`-`m_ref4`, `m_refcase`, `m_wall1`-`m_wall4`, `m_wallcase`.  **A DISAGREEMENT -- see 2c** |
| U8 | Grok, Astra | both `[ "$body" -eq 0 ]` sites treat 1..39 bytes like 0 (the smallest answer fixture was 40 bytes) | **PINNED**: B1G (a 1-byte rc-0 answer with column-0 wall lines: NOT classified -> 0), B1E (a 1-byte answer, a clean header -> 0, not 6).  Mutants `m_gatele1`, `m_emptyle1` |
| U9 | Grok, Astra | the `.refused.txt` move is pinned by nothing (D1 checked only `-s .refused.err`) | **PINNED**: D1R (`.refused.txt` and `.refused.err` byte-for-byte the first run's -- the empty stdout by existence AND content -- and `.txt`/`.err` the Daybreak run's).  Mutants `m_norefusedtxt`, `m_norefusederr` |
| U10 | Grok, Astra | the default codex path, and the override being honoured at all, are pinned by nothing (every row exported CX_CODEX_BIN; an override-ignoring AFTER run would call the REAL CLI) | **PINNED**: HOME is a scratch dir for EVERY column, holding a second fake at the default path that marks the run; DP (CX_CODEX_BIN unset -> the default fake, called exactly as E1), EO (CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY -> the defaults, both calls exactly as E2), E0b (no other after run reaches the default fake).  Mutants `m_defpath`, `m_binignore`, `m_bincolon`, `m_modelcolon`, `m_effortcolon`, `m_aupeffcolon` |
| U11 | Fable, GLM | the exit cascade's ORDER is pinned only for refusal-before-wall (disclosed); 6-before-5 is unrowed | **PINNED, every adjacent pair**: RW (refusal + wall -> 7), RI (refusal + another model's header -> 7), WI (wall + another header -> 8), EM (empty + another header -> 6), IR (rc 1, an answer, another header -> 5), with P1, P2, X1 for the rest.  Ten mutants `m_ord_*`, each MOVING one block, plus `m_prec` |
| U12 | Fable, Grok | the trims of the model line, the banner's `^`, the case folds and `cd "$PROJ"` are equivalent on record or untestable | **PINNED**: WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>` verifies), BA (a prefixed banner and a rule ABOVE the real banner, asked as gpt-6-other -> 5), CWD (every after run's codex starts in the project root; the fake records its directory).  Mutants `m_trailws`, `m_leadws`, `m_bannerun`, `m_cd`.  `|| exit 9` stays DISCLOSED (a missing project dir is untestable without editing the file) |
| U13 | main loop, reading the file for v5 | the awk's remaining guards and constants: `h == 0 &&`, `h == 1 &&`, `h == 2 &&`, the eight-dash rules, the closing `exit`, `h == 2` as the body test, `-m1` and the `^` of `^model:` | **PINNED**: HB (a banner-shaped line inside the block), R7A (seven dashes after the banner are not the first rule), R7B (seven dashes inside the block do not close it), NM (a block with no model line: one after the close is not read), TM (two model lines: the first), MA (`fallback model:` is not a model line).  Mutants `m_bannerh`, `m_rule1h`, `m_rule7a`, `m_rule1next`, `m_close2h`, `m_rule7b`, `m_exitnext`, `m_bodyh1`, `m_capn`, `m_m2`, `m_modelanchor`, `m_hlt1`, `m_hlt3`.  `-m1` -> `-m2` and `exit` -> `next` were DISCLOSED in v4; they are pinned now |
| U14 | main loop, reading the CALLER | the farm's pack runner (`_scratchpad/codexpack_20260928/run_pack_body.sh`, read 2026-10-17) counts a job done only when the launch log says `seat answered` or `The answer is LOST`, and records `answered by: <model>` -- three log phrases no control read | **PINNED**: PK (over every after run: `seat answered` iff exit 0, `The answer is LOST` iff exit 7, `answered by:` iff an exit 0 whose model verified), N1V and WMT (which model), LOG (the `codex rc=N   stdout=N b ...` line, which the launch-log censuses parse).  Mutants `m_msganswered`, `m_msganswered2`, `m_msglost`, `m_msgby`, `m_rcline`.  The launcher's header now says what the runner reads |
| U15 | Astra | the kill-table driver accepted a mutant run without its completion sentinel or full denominator | **FIXED**: `run_mutants_v5.sh` reports an INCOMPLETE run and fails the table; a red check is read from EVERY check line (v4's parser dropped E0's red -- Grok) |
| U16 | Astra, Grok, GLM | `census_v4.py` omitted the 30-line cap; V10's "0 of 410 classified runs" is a count of EMPTY-OR-ABSENT siblings, not of exit status; the m_sgr disclosure cited one fact at three populations (2,372 / 4,851 / 2,422) | **FIXED**: `census_v5.py` applies the cap, names each population (CODEX 2,425 files, ALLERR 8,590, LAUNCH 466 with a `codex rc=` line) and measures each fact itself; the diagonal is measured on the launch logs (474 rows: 440 rc-0 with stdout, 34 rc-1 empty, nothing else) |
| U17 | GLM | "every other row disables it", beside FB1/FB2, is false: D1-D4 leave the fallback on too | **FIXED**: the comment names which rows leave it on |
| U18 | GLM | its own F1: W12 and K30 set CX_MODEL=gpt-6-other, so their 5 cannot be | **REFUTED by grep**: neither row sets CX_MODEL; they ask the default gpt-6-astra while their blocks name gpt-6-other.  The rows that set it are M1, X13, CH, BA, R7B (gpt-6-other), X5 (gpt-5-astra) and D5 (Daybreak) |
| U19 | Grok, GLM | the K30/K31 cap rows are UNTERMINATED blocks, and the realizable shape (a closed block whose model line falls past body line 30) is neither pinned nor censused | **DISCLOSED** in the CONTRACT as synthetic; `CENSUS_v5.txt`: 0 of 975 opening blocks fail to close within the cap, every model line is file line 5 or 7 |
| U20 | Astra, Grok, Fable | records: "a complete answer is never scored WALLED for quoting a wall line" is false (N4); "every decision's pinned edges" over-claimed; "0 of 410 classified runs"; the unconditional "a different model exits 5"; the panel.sh comment note | **CORRECTED** (section 5): an rc-0 run with a non-empty stdout is never scored by what stderr quotes; the CONTRACT's method is stated, not a completeness slogan; the population named; exit 5 comes after the refusal, wall and empty checks, and a refused first run's header is not compared; the working-tree `panel.sh` carries the comment, uncommitted with its other deltas, HEAD's does not |

| U21 | main loop, firing THIS pass | the dashboard pass's Astra seat was launched through a frozen copy of this launcher with RELATIVE paths: the brief's size was read in the caller's directory (787 bytes), then `cd "$PROJ"`, then codex got no brief and the run exited 1, "NOT a clean run" -- correctly failed, nothing laundered, but a relative path silently means two different files | **DISCLOSED, not fixed**: the usage line now says ABSOLUTE paths and why, and the CONTRACT lists it under NOT PINNED.  A fix (resolve both paths before the `cd`) must also accept Windows-style absolute paths (`C:/...`), which a `/*` test would mangle -- new code, a new floor-bound diff.  **Question for this pass: fix it in this landing, or disclose and file?** |
| U22 | `CENSUS_v5.txt` | the v5 CONTRACT first called CSI wholly synthetic; the census finds a `;`-joined SGR in 44 of the 2,425 codex `.err` files on record (non-SGR CSI: 0) | **CORRECTED** in the CONTRACT: CSI's `;` half is on record, so `[0-9;]` is load-bearing (`m_strip_nosemi`) |

## 2b. Premises to CHECK (stated as questions)

* **The CONTRACT's completeness.**  Read the whole of `tools/cxlaunch.sh` (section 3a inlines it whole) for every `if`,
  `[ ... ]`, `&&`/`||`, `grep` and its flags, `sed`/`awk` expression, redirection, `exit` and constant.  Is any decision
  missing from section 3b's header, or listed with a row that does not straddle its edge?
* **Is "a constant's edges are what an edge row is for" a sound reason to PIN synthetic shapes** (U7, U12, U13) rather than
  DISCLOSE them with their zero counts?  The pass-2 ruling disclosed 0-on-record shapes; v5 pins them.
* **The caller contract (U14).**  Is `run_pack_body.sh` the only caller that reads the log, and are those the phrases it reads?
  (The `answered by:` grep in its `reap` records the model; `done_job` decides a re-run.)
* **`HOME` for every column (U10).**  Does a scratch HOME change any launcher's behaviour beyond the default codex path?

## 2c. The disagreement, both sides in their own words

**U7 -- pin or disclose the six alternatives with 0 instances.**
* Fable 5.1 (v4 pass): *"For F7 and the three equivalent-on-record edits I do NOT ask for rows: 0 instances on record is the
  pass-2 ruling's own criterion for DISCLOSE, and a synthetic `ERROR: quota ...` would pin nothing real."*
* GPT-6 Astra (v4 pass): *"Narrow the wall expression at line 137 to `usage limit`.  Every classified positive wall fixture
  contains that phrase.  A sole `quota`, `rate limit` or `not authenticated` diagnostic stops producing exit 8."*
* Grok 4.7 (v4 pass): *"Deleting `quota`, `rate limit`, `not authenticated`, or the three non-flagged refusal phrases stays
  green on this suite."*
* My disposition: PIN.  A deleted alternative changes a real outcome (a sole `not authenticated` would read exit 6, which the
  pack runner retries, instead of 8, which STOPs the pack); the rows cost one fixture each; and K30/K31 already pin a
  0-on-record constant.  **Fable: rule on this, and be harder on the side you argued.**

## 3. The repair, v4 -> v5

### 3a. `tools/cxlaunch.sh` -- WHOLE, as it ships (md5 af18158ed30b740cb13604de64013323)

```bash
     1	#!/bin/bash
     2	#  A codex launcher that CANNOT report a refused seat as a clean run.
     3	#
     4	#  *** THE TWO DEFECTS THIS REPLACES, both mine, both measured 2026-09-07 on the lcaconfwidth
     5	#  census. ***
     6	#    1. The content check grepped the .txt for refusal text.  A codex CONTENT-FILTER REFUSAL writes
     7	#       NOTHING to stdout and puts "ERROR: This content was flagged..." on STDERR -- so the check
     8	#       reported `refusal hits: 0` on a refusal.  A check that looks in the wrong stream answers the
     9	#       same whether or not the thing it tests is true.
    10	#    2. The script ended on a successful command, so it exited 0 while holding `codex rc=1`.  The
    11	#       harness then reported the task as COMPLETED.  A failure laundered into a clean completion.
    12	#
    13	#  *** LANDED HERE 2026-10-16 (ledger `cxlaunchquotation`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 in
    14	#  regress/artifacts/adj_20261016/RULINGS_C_records.md, F1).  Until then THIS file ran Astra at `max` with the
    15	#  2026-09-07 classifier, while most farm jobs ran an UNTRACKED scratchpad copy (cxlaunch_u.sh) carrying the two
    16	#  owner directives of 2026-09-26 -- and the carrier described the copy's behaviour as this file's.  Not every job
    17	#  ran the copy: the 2026-10-09 asicconverge confirm used the old classifier and reported an rc-0, 10,466-byte answer
    18	#  as WALLED (fablequeue8n_20261009/astra_confirm/cxlaunch_asicconverge_stdout.txt). ***
    19	#    1. "Astra (ultra) can replace codex 5.6 sol" -- the effort is `ultra`.  MEASURED 2026-09-26 before use: the
    20	#       server's enum lists 'none'..'xhigh','max' and rejects a bogus value with 400 invalid_enum_value; `ultra` is
    21	#       accepted (rc 0, header `reasoning effort: ultra`, liveness token and a verbatim CHECKPOINT.md quote returned).
    22	#       The CLI's own model cache describes it as "Maximum reasoning with automatic task delegation" -- max plus
    23	#       delegation, so it is a CLI tier above max, not a server one.
    24	#    2. "use daybreak ... if encountering AUP error" -- on a content-filter refusal (codex's own `ERROR: This content
    25	#       was flagged for possible cybersecurity risk` on stderr) the brief is re-run ONCE on the Daybreak model
    26	#       (gpt-daybreak-blue-latest, the CLI's only Daybreak slug: "frontier agentic coding model for broad defensive
    27	#       cybersecurity work"; liveness-verified 2026-09-26).  The refused run's files are KEPT as
    28	#       codex_<tag>.refused.{txt,err}, and the log names which model answered -- a Daybreak answer is recorded as
    29	#       Daybreak's, never as Astra's.  The receipt of the fallback firing on a REAL refusal is
    30	#       regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log; the controls below test
    31	#       the classifier on fixtures, which is a different claim.
    32	#    3. (2026-10-16, Fable 5.1) codex's diagnostics are matched AFTER ANSI colour is stripped.  7 of 453 panel.sh
    33	#       codex.txt files carry a column-0 `ERROR:` coloured as ESC[1m ESC[31m ERROR: ESC[0m
    34	#       (adj_20261016/fable5/meas_C/ansi_census.txt; 0 of 593 launcher .err files), and one is a REAL codex refusal:
    35	#       _scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err, where `grep '^ERROR:'` finds 0 lines unstripped
    36	#       and 2 stripped.  Unstripped, such a run reads exit 6 "seat down" (Fable's Q3 is the wall-shaped twin).
    37	#    4. (2026-10-16, GPT-6 Astra) the `model:` line of codex's HEADER BLOCK is COMPARED to the model asked for.  This
    38	#       file printed both and compared neither, so "a wrong name is a SEAT FAILURE" was unenforced.  On record: 322
    39	#       asked/ran pairs across 519 launch logs under the project root, 319 across 493 inside GXEMUL-SEC (Astra), no
    40	#       header absent and no mismatch -- so a mismatch is new, and it exits 5.  Only the OPENING header block is read
    41	#       (pass 2 and the adjudication pass, Astra): a `model:` line anywhere else in stderr is streamed source or the
    42	#       brief -- it can name a model, and it is never READ (GLM 5.3 and Grok 4.7, v3 pass).
    43	#
    44	#  KNOWN RESIDUALS -- recorded, NOT fixed (the ruling's own wording; no real run has either shape, 0 of 387 launch
    45	#  lines are off the diagonal of {rc 0 with stdout, rc 1 with empty stdout} -- adj_20261016/fable5/meas_C/
    46	#  launchlog_census.txt):
    47	#    * rc != 0 WITH an answer AND column-0 quoted wall text -> exit 8 (fixture N4).  Reading only codex's LAST
    48	#      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
    49	#    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
    50	#      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
    51	#    * a run whose stderr carries NO opening codex header block is reported "model UNVERIFIED" and is not failed -- 0 of
    52	#      330 launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
    53	#      CLI format change.  A block whose closing rule never comes is read for 30 lines at most.
    54	#    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
    55	#      pass 2): a quoted line whose only prefix was colour becomes column-0 -- still inside the classify-on-failure gate.
    56	#    * a REFUSED first run's header is printed (`ran:`) but not compared; its answer is discarded, and the fallback's
    57	#      own run is the one compared (GLM 5.3, pass 2).
    58	#    * exit 5 is new to callers: the farm's pack runner special-cases 7 and 8 only, so it RETRIES a 5 rather than
    59	#      recording an answer (Grok 4.7, pass 2) -- a different model having answered is not an answer from this seat.
    60	#      The mechanism (_scratchpad/codexpack_20260928/run_pack_body.sh, read 2026-10-17): it reports a 7, STOPs the pack
    61	#      on an 8, and its done_job counts a job done only when the launch log says `seat answered` or `The answer is
    62	#      LOST` -- so a 5 or a 6 is left not done and the next pack run fires it again.  Those two phrases, and the
    63	#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5).
    64	#
    65	#  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
    66	#  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
    67	#
    68	#  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
    69	#  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
    70	#  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
    71	#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh (RECEIPT_v5.txt; the kill table is
    72	#  KILLTABLE_v5.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
    73	#  redirection, constant and caller-read log phrase of this file, each with the rows that pin its edges or the reason
    74	#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v4.txt are the receipts of the earlier versions.
    75	#
    76	#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>   -- ABSOLUTE paths.  The brief's size and `mkdir` resolve in the caller's
    77	#  directory, codex's files after `cd "$PROJ"`, so a relative path breaks: measured 2026-10-17, a relative pointer read 787
    78	#  bytes, then codex got no brief and the run exited 1, NOT a clean run.  Every caller on record passes absolute paths.
    79	set -u
    80	BRIEF="$1"; OUT="$2"; TAG="$3"
    81	PROJ=/c/DocumentNoSnc/CC/GXEMUL
    82	CODEX="${CX_CODEX_BIN:-$HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex}"
    83	MODEL="${CX_MODEL:-gpt-6-astra}"
    84	EFFORT="${CX_EFFORT:-ultra}"
    85	AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"
    86	AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"
    87	mkdir -p "$OUT"
    88	TXT="$OUT/codex_${TAG}.txt"; ERR="$OUT/codex_${TAG}.err"
    89	ESC=$(printf '\033')
    90	
    91	sz=$(wc -c < "$BRIEF")
    92	echo "brief bytes: $sz"
    93	[ "$sz" -gt 30000 ] && { echo "*** above the argv cap -- use the pointer form"; exit 9; }
    94	
    95	cd "$PROJ" || exit 9
    96	
    97	strip_ansi() { sed "s/${ESC}\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }
    98	
    99	run_codex() {    # $1 model, $2 effort
   100	    "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
   101	        -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
   102	    rc=$?
   103	    #  codex's OPENING header block -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the
   104	    #  model and effort it actually ran.  Read only that block, and only at the TOP of stderr: the banner and its first
   105	    #  rule must appear by line 12 and the block is read for at most 30 lines.  On record the block's `model:` line is
   106	    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra).  A `model:` line
   107	    #  anywhere else is streamed source or the brief and is never READ -- including a complete QUOTED header block, which
   108	    #  N1's own stderr carries at line 5528 (GPT-6 Astra, adjudication pass: v2 matched the banner anywhere).
   109	    HDR=$(strip_ansi "$ERR" | awk 'NR > 12 && h < 2 { exit }
   110	        h == 0 && /^OpenAI Codex/ { h = 1; next }
   111	        h == 1 && /^--------/ { h = 2; next }
   112	        h == 2 && /^--------/ { exit }
   113	        h == 2 { if (++n > 30) exit; print }')
   114	    RAN=$(printf '%s\n' "$HDR" | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
   115	    echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
   116	    echo "  ran: ${RAN:+model: $RAN} / $(printf '%s\n' "$HDR" | grep -m1 '^reasoning effort:')"
   117	}
   118	
   119	#  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
   120	#
   121	#  *** MEASURED 2026-09-07, on the run that installed this file: codex STREAMS THE SOURCE IT READS into stderr, so a
   122	#  bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
   123	#
   124	#  *** AND THE ANCHOR IS NOT ENOUGH.  MEASURED 2026-09-26: THREE REAL ANSWERS WERE REPORTED "SEAT WALLED" -- astra549
   125	#  (rc 0, 11,472 b), astra550 (rc 0, 4,265 b), rec529audit (rc 0, 13,442 b) -- because each read an old panel file
   126	#  whose lines BEGIN with a codex wall message ("ERROR: You've hit your usage limit ... 7:01 AM"), and codex streamed
   127	#  those lines into stderr at column 0.  A quoted marker re-arms the tool that reads it (the carrier's own rule). ***
   128	#
   129	#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge.  stderr's `ERROR:` lines are
   130	#  classified ONLY WHEN rc != 0 OR stdout IS EMPTY; rc 0 with a non-empty stdout is an ANSWER, whatever stderr quotes.
   131	#  Every real wall and refusal on record is rc 1 with an EMPTY stdout, and every rc-0 run carries an answer: 362 + 25
   132	#  of 387 launch lines, nothing off that diagonal (launchlog_census.txt) -- the residuals above are the off-diagonal.
   133	classify() {
   134	    #  `grep -a`: a stderr carrying a NUL byte is "binary" to grep, which then prints `Binary file (standard input)
   135	    #  matches` instead of the lines.  A real wall was recorded exit 6 "seat down" that way:
   136	    #  _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err (rc 1, empty stdout, 1,449 NULs from byte 2,318,517;
   137	    #  its two column-0 `ERROR: You've hit your usage limit` lines come after them) -- Grok 4.7, pass 2, re-run here.
   138	    CXERR=$(strip_ansi "$ERR" | grep -a '^ERROR:')
   139	    verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
   140	    body=$(wc -c < "$TXT")
   141	    refus=0; wall=0
   142	    if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then
   143	        refus=$(printf '%s' "$CXERR" | grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help')
   144	        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')
   145	    else
   146	        q=$(printf '%s' "$CXERR" | grep -c .)
   147	        [ "$q" -gt 0 ] && echo "  note: $q ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source"
   148	    fi
   149	    echo "  verdict-in-stdout: $verd   refusal: $refus   wall: $wall   (classified only when rc != 0 or stdout is empty)"
   150	}
   151	
   152	run_codex "$MODEL" "$EFFORT"; classify
   153	ANSWERED_BY="$MODEL"
   154	
   155	if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then
   156	    echo "  *** SEAT REFUSED on $MODEL (content filter):"
   157	    printf '%s\n' "$CXERR" | grep -m1 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
   158	    mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"
   159	    echo "  *** AUP FALLBACK: re-running ONCE on $AUP_MODEL / $AUP_EFFORT (the refused run is kept as codex_${TAG}.refused.*)"
   160	    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify
   161	    ANSWERED_BY="$AUP_MODEL"
   162	fi
   163	
   164	if [ "$refus" -gt 0 ]; then
   165	    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."
   166	    printf '%s\n' "$CXERR" | grep -m2 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
   167	    echo "  *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK."
   168	    exit 7
   169	fi
   170	if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED ($ANSWERED_BY)."; exit 8; fi
   171	if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
   172	if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then
   173	    echo "  *** A DIFFERENT MODEL RAN: asked $ANSWERED_BY, codex's header says $RAN -- a SEAT FAILURE; the answer is not $ANSWERED_BY's."
   174	    exit 5
   175	fi
   176	if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
   177	if [ -z "$RAN" ]; then
   178	    echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"
   179	else
   180	    echo "  seat answered. (answered by: $ANSWERED_BY)"
   181	fi
```

### 3a'. its v4 -> v5 diff -- comments only (15 changed lines)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v4.sh	2026-10-17 01:23:15.224968700 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh	2026-10-17 03:31:55.562960900 -0500
@@ -57,6 +57,10 @@
 #      own run is the one compared (GLM 5.3, pass 2).
 #    * exit 5 is new to callers: the farm's pack runner special-cases 7 and 8 only, so it RETRIES a 5 rather than
 #      recording an answer (Grok 4.7, pass 2) -- a different model having answered is not an answer from this seat.
+#      The mechanism (_scratchpad/codexpack_20260928/run_pack_body.sh, read 2026-10-17): it reports a 7, STOPs the pack
+#      on an 8, and its done_job counts a job done only when the launch log says `seat answered` or `The answer is
+#      LOST` -- so a 5 or a 6 is left not done and the next pack run fires it again.  Those two phrases, and the
+#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5).
 #
 #  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
 #  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
@@ -64,11 +68,14 @@
 #  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
 #  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
 #  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
-#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v4.sh (RECEIPT_v4.txt; the kill table is
-#  KILLTABLE_v4.txt; its header is the CONTRACT -- which edge of each decision this file makes is pinned, and which is
-#  deliberately not).  RECEIPT.txt, RECEIPT_v2.txt and RECEIPT_v3.txt are the receipts of the earlier versions.
+#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh (RECEIPT_v5.txt; the kill table is
+#  KILLTABLE_v5.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
+#  redirection, constant and caller-read log phrase of this file, each with the rows that pin its edges or the reason
+#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v4.txt are the receipts of the earlier versions.
 #
-#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>
+#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>   -- ABSOLUTE paths.  The brief's size and `mkdir` resolve in the caller's
+#  directory, codex's files after `cd "$PROJ"`, so a relative path breaks: measured 2026-10-17, a relative pointer read 787
+#  bytes, then codex got no brief and the run exited 1, NOT a clean run.  Every caller on record passes absolute paths.
 set -u
 BRIEF="$1"; OUT="$2"; TAG="$3"
 PROJ=/c/DocumentNoSnc/CC/GXEMUL
```

### 3b. the controls, `run_controls_v5.sh`, WHOLE (the CONTRACT is its header)

```bash
     1	#!/bin/bash
     2	#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
     3	#  F1), v5 after the four-seat pass 2, the adjudication pass, the v3 pass and the v4 pass.  Every row runs a launcher against a FAKE
     4	#  codex that replays a fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the
     5	#  expected one:
     6	#
     7	#    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
     8	#             landing REPLACES -- it names its codex binary under $HOME and has no override
     9	#    before   cxlaunch_before.sh   = the untracked production copy the farm ran (md5 3c51a757...)
    10	#    after    tools/cxlaunch.sh    = the landed file (or $CXL_AFTER, which the mutant table uses)
    11	#
    12	#  The tracked column is the PRE-FIX state (Fable 5.1's pass-2 C1, via its Opus 4.8 fallback): N1 and N2 are the
    13	#  `cxlaunchquotation' false wall (exit 8 there, 0 after), D1 the missing Daybreak fallback (7 there, 0 after).  The tracked and
    14	#  before expectations RECORD what the two old files do; only the after column is a claim.  Those of the rows v5 added were
    15	#  recorded from a calibration run of this file (RECEIPT_v5_calibration.txt); every after expectation was written before it.
    16	#
    17	#  v5 -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3) measured one-edit mutants passing all 116 v4 controls at
    18	#  decisions the v4 CONTRACT did not list -- codex's own rc passed through, the fallback's second and third conjuncts, the
    19	#  header's ANSI strip, the stdin redirect, the output names, the pattern alternatives, the two `-eq 0` body tests, the default
    20	#  codex path.  The v4 CONTRACT was derived from the three passes' FINDINGS, not from the file (Fable 5.1).  v5's is derived from
    21	#  the file: every predicate, conjunct, pattern alternative, redirection, constant, exit-cascade order and caller-read log
    22	#  phrase, each asked "which row goes red if this changes".  Every launcher run is under `timeout 120' (a looping mutant exits
    23	#  124 and reds; an honest run takes about 0.6 s -- Fable 5.1, v4 pass) and is fed a MARKER file on stdin; HOME is a scratch
    24	#  dir holding a second fake at the launcher's default codex path, which marks the runs that reach it.
    25	#
    26	#  THE CONTRACT -- each decision of the landed launcher (by construct), the rows that pin its edges, and what is not pinned:
    27	#  configuration
    28	#    CX_CODEX_BIN honoured, its `:-'      E0b (no after run but DP's and EO's reaches the default-path fake); EO (set EMPTY)
    29	#    the default codex path               DP (CX_CODEX_BIN unset: the run reaches $HOME/AppData/Local/Programs/.../codex)
    30	#    CX_MODEL, CX_EFFORT, CX_AUP_EFFORT, their `:-' and defaults
    31	#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default)
    32	#    CX_AUP_MODEL, its default and `-' (EMPTY disables the fallback)
    33	#                                         E2; FD (every row that sets it empty makes exactly one call)
    34	#    the output names and the stdout/stderr redirections, `mkdir -p "$OUT"'
    35	#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written)
    36	#    `< /dev/null' on codex's stdin       SI (no after run's codex reads the marker the launcher is fed)
    37	#    `cd "$PROJ"'                         CWD (every after run's codex starts in the project root)
    38	#    the argv cap `sz -gt 30000', exit 9  X14 (30,000 accepted) / X15 (30,001: exit 9, codex never called)
    39	#  the call
    40	#    the argument sequence                E1 (one call), E2 and EO (Astra, then Daybreak), DP -- each compared whole
    41	#  the opening header
    42	#    ANSI strip on the header             CH (the real coloured header of fx/R2.stderr, asked as gpt-6-other -> 5)
    43	#    the window `NR > 12 && h < 2'        W12 / W13 (first rule at line 12 read, at 13 not); X13 (the real banner-at-4 header);
    44	#                                         X9, X10 (no opening block, a quoted one at line 21)
    45	#    the banner: `h == 0 &&', `/^OpenAI Codex/'
    46	#                                         HB (a banner-shaped line inside the block does not restart it); BA (a banner with a
    47	#                                         prefix, above the real one, is not a banner); every header row (the text)
    48	#    the first rule: `h == 1 &&', 8 dashes, `next'
    49	#                                         BA (a rule before any banner is not the first rule); R7A (seven dashes are not a
    50	#                                         rule; nine find no block anywhere); every header row (`next')
    51	#    the closing rule: `h == 2 &&', 8 dashes, `exit'
    52	#                                         BA (a rule before any banner closes nothing); R7B (seven dashes do not close the
    53	#                                         block); NM (no model line in the block: a model line after the close is not read)
    54	#    the body: `h == 2', the cap `++n > 30'
    55	#                                         R7A (the lines between banner and first rule are not body); K30 / K31 (a model at
    56	#                                         body line 30 read, at 31 not)
    57	#    the first `model:' line, anchored    TM (two model lines: the first is read); MA (`fallback model:' is not a model line);
    58	#                                         M1, X5
    59	#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies)
    60	#  classification
    61	#    the gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4; RC2W (rc 2 with an answer IS classified); B1G (a 1-byte rc-0
    62	#                                         answer is NOT)
    63	#    `^ERROR:', `grep -a'                 X1; X8
    64	#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR)
    65	#    the refusal alternatives, `-i'       P2, Q1, A1 (`flagged for possible cybersecurity'); RF1 (`cannot help with');
    66	#                                         RF2 (`can't help with'); RF3 (`I won't help'); RFC (the first, upper case)
    67	#    the wall alternatives, `-i'          P1, Q2, Q3, X8 (`usage limit'); WL1 (`quota'); WL2 (`rate limit');
    68	#                                         WL3 (`not authenticated'); WLC (the first, upper case)
    69	#    refusal count `refus -gt 0', at BOTH guards
    70	#                                         P2, Q1, A1, D1 (count 1); R2X (2, the final guard); D3 (2, the fallback)
    71	#    wall count `wall -gt 0'              W1L (count 1); P1, Q2, Q3, X8 (2); N4 (6)
    72	#  the fallback
    73	#    trigger `refus -gt 0 && -n AUP_MODEL && AUP_MODEL != MODEL'
    74	#                                         D1, D2, D3 fire; FB1, FB2 do not (an answer, a wall; the fallback on); FD (empty:
    75	#                                         never); D5 (asked ON Daybreak and refused: no second run)
    76	#    once                                 D4 (refused, then refused on Daybreak: exactly two calls)
    77	#    the refused run's files kept         D1R (codex_D1.refused.txt and .refused.err byte-for-byte the first run's; codex_D1.txt
    78	#                                         and .err the Daybreak run's)
    79	#    the answer credited to the fallback  D1, D3 (Daybreak credited); D2 (Daybreak compared -> 5)
    80	#  the exit cascade: refused 7, walled 8, empty 6, a different model 5, codex's own rc
    81	#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1)
    82	#    the order, each adjacent pair        RW (refusal + wall -> 7); P2 (refusal + empty + rc 1 -> 7); RI (refusal + another
    83	#                                         model's header -> 7); P1 (wall + empty -> 8); WI (wall + another header -> 8);
    84	#                                         EM (empty + another header -> 6); X1 (empty + rc 1 -> 6); IR (rc 1, an answer,
    85	#                                         another header -> 5)
    86	#    the empty test `body -eq 0'          N3, X1 (0 bytes -> 6); B1E (1 byte -> 0)
    87	#    identity `-n RAN && RAN != ANSWERED_BY'
    88	#                                         M1, D2, X5, W12, K30, X13, CH, IR, BA -> 5; M2, X6, X9, W13, K31, NM, HB -> UNVERIFIED, 0
    89	#  the log phrases a caller reads (_scratchpad/codexpack_20260928/run_pack_body.sh: done_job and reap)
    90	#    `seat answered' iff exit 0; `The answer is LOST' iff exit 7; `answered by: <model>' iff an exit 0 whose model verified
    91	#                                         PK (every after run); N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB (none)
    92	#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, which the launch-log censuses this file cites parse
    93	#                                         LOG (N1)
    94	#  NOT PINNED, each with its reason:
    95	#    `|| exit 9' after `cd'               needs a missing project dir -- untestable without editing the file
    96	#    `set -u'                             reached only by a missing positional argument (a usage error, exit 1); every caller
    97	#                                         passes three, and a row without them would write outside the scratch dir under a
    98	#                                         mutant that drops it
    99	#    the banner rule's `next'             equivalent: the banner line matches no later rule
   100	#    RELATIVE paths                       the brief's size and `mkdir' resolve in the caller's directory, codex's files after
   101	#                                         `cd "$PROJ"', so a relative brief or out path breaks (measured 2026-10-17: a relative
   102	#                                         pointer read 787 bytes, codex got no brief, exit 1 -- NOT a clean run, nothing
   103	#                                         laundered).  Disclosed in the usage line; every caller on record, and every row here,
   104	#                                         passes absolute paths
   105	#    display only -- printed, read by no decision and no caller: `brief bytes'; the `ran:' line (the header's effort is
   106	#                                         printed, never compared); `verdict-in-stdout' (verd exists for that line alone); the
   107	#                                         IGNORED note; the refusal excerpts (`-m1'/`-m2', `cut -c1-160'); the REPHRASE line;
   108	#                                         the wording of the 5, 6, 8 and rc messages beyond the phrases above
   109	#  SYNTHETIC SHAPES, pinned because a constant's edges are what an edge row is for: RF1-RF3, RFC, WL1-WL3, WLC, RW, BA, HB,
   110	#  R7A, R7B, NM, TM, MA, WS, K30, K31 and W12/W13 have 0 instances on record, and so does CSI's non-SGR half (CENSUS_v5.txt,
   111	#  which names each count).  CSI's other half is NOT synthetic: a `;'-joined SGR sits in 44 of the 2,425 codex .err files on
   112	#  record, so the strip's `;' is load-bearing.
   113	#
   114	#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
   115	#  Usage: bash run_controls_v5.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
   116	#  the mutant table uses; writes only to a scratch dir it removes)
   117	set -u
   118	HERE=$(cd "$(dirname "$0")" && pwd)
   119	REPO=$(cd "$HERE/../../.." && pwd)
   120	TRACKED="$HERE/cxlaunch_tracked.sh"
   121	BEFORE="$HERE/cxlaunch_before.sh"
   122	AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
   123	ONLY="${CXL_AFTER_ONLY:-}"
   124	N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
   125	QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
   126	NROWS=65
   127	NFD=56
   128	for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
   129	         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout" "$HERE/fx/R2.stderr"; do
   130	    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
   131	done
   132	T=$(mktemp -d)
   133	trap 'rm -rf "$T"' EXIT
   134	ESC=$(printf '\033')
   135	
   136	mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr from stdin)
   137	    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
   138	    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
   139	    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
   140	}
   141	printf 'A complete review answer.\nVERDICT: SHIP\n' > "$T/ans_verdict.txt"
   142	#  NOT the word "verdict" in any case: the launcher counts it case-insensitively, and a first draft of this fixture said
   143	#  "no verdict line" -- so it HAD one, and the kill table measured X2 blind to the mutant it exists for.
   144	printf 'A complete review answer that ends without its summary line.\n' > "$T/ans_noverdict.txt"
   145	printf 'x' > "$T/ans_1byte.txt"
   146	hdr() {    # $1 the model -- a minimal closed opening header block
   147	    printf 'OpenAI Codex v0.153.4\n--------\nmodel: %s\nreasoning effort: ultra\n--------\n' "$1"
   148	}
   149	hdr gpt-6-astra > "$T/hdr_astra.txt"
   150	hdr gpt-6-other > "$T/hdr_other.txt"
   151	grep -m1 '^ERROR:' "$HERE/fx/P2.stderr" > "$T/refusal_line.txt"
   152	grep -m1 '^ERROR:' "$HERE/fx/P1.stderr" > "$T/wall_line.txt"
   153	[ -s "$T/refusal_line.txt" ] && [ -s "$T/wall_line.txt" ] || { echo "APPARATUS FAIL: no column-0 ERROR line in P1 or P2"; exit 9; }
   154	mkfx P1 1 "" "$HERE/fx/P1.stderr"
   155	mkfx P2 1 "" "$HERE/fx/P2.stderr"
   156	mkfx N1 0 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
   157	mkfx N2 0 "$HERE/fx/N2.stdout" ""
   158	mkfx N3 0 "" ""
   159	mkfx N4 1 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
   160	mkfx Q1 1 "" "$QD/Q1.stderr"
   161	mkfx Q2 0 "" "$QD/Q2.stderr"
   162	mkfx Q3 1 "" "$QD/Q3.stderr"
   163	sed "s/^ERROR:/${ESC}[1m${ESC}[31mERROR:${ESC}[0m${ESC}[0m/" "$HERE/fx/P2.stderr" | mkfx A1 1 "" -
   164	hdr gpt-daybreak-blue-latest | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
   165	mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" "$T/hdr_astra.txt"
   166	sed 's/^/regress\/artifacts\/old_panel\/codex.txt:17:/' "$HERE/fx/P2.stderr" | mkfx X1 1 "" -
   167	mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
   168	printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
   169	{ printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -
   170	#  X9/X10: twenty lines of streamed text, then a complete codex header block QUOTED from a file the review read (the shape
   171	#  N1's stderr carries from line 5528) -- and no opening header at all
   172	latehdr() {    # $1 the quoted block's model
   173	    i=1; while [ $i -le 20 ]; do printf 'streamed line %d of a file the review read\n' $i; i=$((i + 1)); done
   174	    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$1"
   175	    printf 'reasoning effort: ultra\n--------\nuser\nthe quoted session brief\n'
   176	}
   177	latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
   178	latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -
   179	#  v4 (the v3 pass): the window's and the cap's EDGES, the real warning-prefixed header, a real doubled refusal, one wall line
   180	hdrat() {    # $1 lines before the banner, $2 the block's model -- a CLOSED opening block whose banner is line $1+1
   181	    i=1; while [ $i -le "$1" ]; do printf 'startup line %d\n' $i; i=$((i + 1)); done
   182	    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$2"
   183	    printf 'reasoning effort: ultra\n--------\nuser\nthe session brief\n'
   184	}
   185	hdrat 10 gpt-6-other | mkfx W12 0 "$T/ans_verdict.txt" -      # banner line 11, first rule line 12: inside the window
   186	hdrat 11 gpt-6-other | mkfx W13 0 "$T/ans_verdict.txt" -      # banner line 12, first rule line 13: outside it
   187	head -14 "$REPO/regress/artifacts/ppcrldimimask/codex_book1check_20260910.err" | mkfx X13 0 "$T/ans_verdict.txt" -
   188	capat() {    # $1 body lines before the block's `model:' line -- an UNTERMINATED opening block
   189	    printf 'OpenAI Codex v0.153.4\n--------\n'
   190	    i=1; while [ $i -le "$1" ]; do printf 'body line %d\n' $i; i=$((i + 1)); done
   191	    printf 'model: gpt-6-other\nreasoning effort: ultra\n'
   192	    i=1; while [ $i -le 20 ]; do printf 'streamed line %d\n' $i; i=$((i + 1)); done
   193	}
   194	capat 29 | mkfx K30 0 "$T/ans_verdict.txt" -                  # the model is body line 30: read
   195	capat 30 | mkfx K31 0 "$T/ans_verdict.txt" -                  # the model is body line 31: not read
   196	mkfx R2 1 "" "$HERE/fx/R2.stderr"
   197	mkfx W1L 1 "" "$T/wall_line.txt"
   198	mkfx ANS 0 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   199	#  v5 (the v4 pass): the rc pass-through, the gate's and the empty test's 1-byte edge, the real coloured header, each pattern
   200	#  alternative and the case fold, a non-SGR strip, each adjacent pair of the exit cascade, and every awk guard and constant
   201	mkfx RC1A 1 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   202	mkfx RC3A 3 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   203	mkfx RC2W 2 "$T/ans_verdict.txt" "$HERE/fx/P1.stderr"
   204	mkfx B1G 0 "$T/ans_1byte.txt" "$HERE/fx/P1.stderr"
   205	mkfx B1E 0 "$T/ans_1byte.txt" "$T/hdr_astra.txt"
   206	head -12 "$HERE/fx/R2.stderr" | mkfx CH 0 "$T/ans_verdict.txt" -      # its opening block only: `ESC[1mmodel:ESC[0m gpt-6-astra'
   207	printf 'ERROR: I cannot help with that request.\n' | mkfx RF1 1 "" -
   208	printf "ERROR: I can't help with that request.\n" | mkfx RF2 1 "" -
   209	printf "ERROR: I won't help with that request.\n" | mkfx RF3 1 "" -
   210	printf 'ERROR: THIS CONTENT WAS FLAGGED FOR POSSIBLE CYBERSECURITY RISK.\n' | mkfx RFC 1 "" -
   211	printf 'ERROR: quota exceeded for this workspace.\n' | mkfx WL1 1 "" -
   212	printf 'ERROR: rate limit reached; retry in 60s.\n' | mkfx WL2 1 "" -
   213	printf 'ERROR: not authenticated -- run codex login.\n' | mkfx WL3 1 "" -
   214	printf "ERROR: You've hit your USAGE LIMIT.\n" | mkfx WLC 1 "" -
   215	printf '%s\n' "${ESC}[2K${ESC}[1;31mERROR:${ESC}[0m This content was flagged for possible cybersecurity risk." | mkfx CSI 1 "" -
   216	cat "$T/refusal_line.txt" "$T/wall_line.txt" | mkfx RW 1 "" -
   217	cat "$T/hdr_other.txt" "$T/refusal_line.txt" | mkfx RI 1 "" -
   218	cat "$T/hdr_other.txt" "$T/wall_line.txt" | mkfx WI 1 "" -
   219	mkfx EM 0 "" "$T/hdr_other.txt"
   220	mkfx IR 1 "$T/ans_verdict.txt" "$T/hdr_other.txt"
   221	printf 'OpenAI Codex v0.153.4\n--------\nmodel:\t  gpt-6-astra \r\nreasoning effort: ultra\n--------\n' | mkfx WS 0 "$T/ans_verdict.txt" -
   222	printf 'OpenAI Codex v0.153.4\n--------\nfallback model: gpt-6-other\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   223	    | mkfx MA 0 "$T/ans_verdict.txt" -
   224	printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
   225	    | mkfx TM 0 "$T/ans_verdict.txt" -
   226	printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nreasoning effort: ultra\n--------\nuser\nmodel: gpt-6-other\n' \
   227	    | mkfx NM 0 "$T/ans_verdict.txt" -
   228	printf '> OpenAI Codex v0.1 (a quoted transcript)\n--------\nmodel: gpt-6-other\n--------\n' > "$T/ba_pre.txt"
   229	cat "$T/ba_pre.txt" "$T/hdr_astra.txt" | mkfx BA 0 "$T/ans_verdict.txt" -
   230	printf 'OpenAI Codex v0.153.4\n--------\nOpenAI Codex v0.1 (quoted)\n--------\nmodel: gpt-6-other\n--------\n' \
   231	    | mkfx HB 0 "$T/ans_verdict.txt" -
   232	printf 'OpenAI Codex v0.153.4\n-------\nmodel: gpt-6-other\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   233	    | mkfx R7A 0 "$T/ans_verdict.txt" -
   234	printf 'OpenAI Codex v0.153.4\n--------\n-------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   235	    | mkfx R7B 0 "$T/ans_verdict.txt" -
   236	
   237	#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL); logs its arguments to $FX_ARGS, its working
   238	#  directory to $FX_ARGS.cwd and the first 60 bytes of its stdin to $FX_ARGS.stdin
   239	cat > "$T/fakecodex.sh" <<'EOF'
   240	#!/bin/bash
   241	D="$FX"; prev=""
   242	for a in "$@"; do
   243	    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
   244	    prev="$a"
   245	done
   246	if [ -n "${FX_ARGS:-}" ]; then
   247	    { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
   248	    pwd >> "$FX_ARGS.cwd"
   249	    head -c 60 >> "$FX_ARGS.stdin"
   250	fi
   251	cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
   252	EOF
   253	chmod +x "$T/fakecodex.sh"
   254	#  the default-path fake under the scratch HOME: it marks the run, then is the same fake (the tracked launcher names only this
   255	#  path; the after launcher reaches it only when CX_CODEX_BIN is unset or empty)
   256	DEFBIN="$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
   257	mkdir -p "$DEFBIN"
   258	printf '#!/bin/bash\n[ -n "${FX_ARGS:-}" ] && echo DEFAULT >> "$FX_ARGS.default"\nexec bash "%s" "$@"\n' "$T/fakecodex.sh" > "$DEFBIN/codex"
   259	chmod +x "$DEFBIN/codex"
   260	printf 'control brief\n' > "$T/brief.md"
   261	printf '%30000s' '' | tr ' ' b > "$T/brief30000.md"
   262	printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"
   263	printf 'STDIN MARKER -- codex must never read this\n' > "$T/stdin_marker"
   264	
   265	pass=0; total=0
   266	run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit (? = record only, counted as a failure), then env
   267	    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
   268	    local out="$T/out_${row}_${lab}"
   269	    case " $* " in *" CX_AUP_MODEL= "*) : > "$T/disabled_${row}_${lab}" ;; esac
   270	    ( export HOME="$T/home" CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
   271	      for kv in "$@"; do export "$kv"; done
   272	      [ "${UNSET_CODEX_BIN:-}" = 1 ] && unset CX_CODEX_BIN
   273	      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" < "$T/stdin_marker" ) > "$T/log_${row}_${lab}.txt" 2>&1
   274	    local got=$?
   275	    echo "$got" > "$T/exit_${row}_${lab}"
   276	    total=$((total + 1))
   277	    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
   278	    printf '%-4s %-7s exit=%-3s want=%-3s %s\n' "$row" "$lab" "$got" "$want" "$ok"
   279	    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
   280	}
   281	three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
   282	    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
   283	    if [ "$ONLY" != 1 ]; then
   284	        run "$row" tracked "$TRACKED" "$wt" "$@"
   285	        run "$row" before "$BEFORE" "$wb" "$@"
   286	    fi
   287	    run "$row" after "$AFTER" "$wa" "$@"
   288	}
   289	check() {    # $1 label, $2 0/1 result
   290	    total=$((total + 1))
   291	    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
   292	}
   293	
   294	echo "# cxlaunch landing controls (v5), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
   295	echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
   296	echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
   297	echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
   298	three P1 8 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
   299	three P2 7 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
   300	three N1 8 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
   301	three N2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
   302	three N3 6 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
   303	three N4 8 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
   304	three Q1 7 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
   305	three Q2 8 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
   306	three Q3 6 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
   307	three A1 6 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
   308	three M1 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   309	three M2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
   310	three D1 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
   311	three D2 7 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
   312	three X1 6 6 6 FX="$T/fx/X1" CX_AUP_MODEL=
   313	three X2 8 0 0 FX="$T/fx/X2" CX_AUP_MODEL=
   314	three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
   315	three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
   316	three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
   317	three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
   318	three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
   319	three W12 0 0 5 FX="$T/fx/W12" CX_AUP_MODEL=
   320	three W13 0 0 0 FX="$T/fx/W13" CX_AUP_MODEL=
   321	three X13 0 0 5 FX="$T/fx/X13" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   322	three K30 0 0 5 FX="$T/fx/K30" CX_AUP_MODEL=
   323	three K31 0 0 0 FX="$T/fx/K31" CX_AUP_MODEL=
   324	three R2X 6 6 7 FX="$T/fx/R2" CX_AUP_MODEL=
   325	three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
   326	three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
   327	three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
   328	#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5 and EO
   329	#  (refusals), and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
   330	#  GLM 5.3, v4 pass.)
   331	three FB1 8 0 0 FX="$T/fx/N1"
   332	three FB2 8 8 8 FX="$T/fx/P1"
   333	three X14 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30000.md"
   334	three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"
   335	#  v5 rows
   336	three RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=
   337	three RC3A 3 3 3 FX="$T/fx/RC3A" CX_AUP_MODEL=
   338	three RC2W 8 8 8 FX="$T/fx/RC2W" CX_AUP_MODEL=
   339	three B1G 8 0 0 FX="$T/fx/B1G" CX_AUP_MODEL=
   340	three B1E 0 0 0 FX="$T/fx/B1E" CX_AUP_MODEL=
   341	three D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest
   342	three CH 0 0 5 FX="$T/fx/CH" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   343	three DP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= UNSET_CODEX_BIN=1
   344	three EO 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest CX_CODEX_BIN= CX_MODEL= CX_EFFORT= CX_AUP_EFFORT=
   345	three RF1 7 7 7 FX="$T/fx/RF1" CX_AUP_MODEL=
   346	three RF2 7 7 7 FX="$T/fx/RF2" CX_AUP_MODEL=
   347	three RF3 7 7 7 FX="$T/fx/RF3" CX_AUP_MODEL=
   348	three RFC 7 7 7 FX="$T/fx/RFC" CX_AUP_MODEL=
   349	three WL1 8 8 8 FX="$T/fx/WL1" CX_AUP_MODEL=
   350	three WL2 8 8 8 FX="$T/fx/WL2" CX_AUP_MODEL=
   351	three WL3 8 8 8 FX="$T/fx/WL3" CX_AUP_MODEL=
   352	three WLC 8 8 8 FX="$T/fx/WLC" CX_AUP_MODEL=
   353	three CSI 6 6 7 FX="$T/fx/CSI" CX_AUP_MODEL=
   354	three RW 7 7 7 FX="$T/fx/RW" CX_AUP_MODEL=
   355	three RI 7 7 7 FX="$T/fx/RI" CX_AUP_MODEL=
   356	three WI 8 8 8 FX="$T/fx/WI" CX_AUP_MODEL=
   357	three EM 6 6 6 FX="$T/fx/EM" CX_AUP_MODEL=
   358	three IR 1 1 5 FX="$T/fx/IR" CX_AUP_MODEL=
   359	three WS 0 0 0 FX="$T/fx/WS" CX_AUP_MODEL=
   360	three MA 0 0 0 FX="$T/fx/MA" CX_AUP_MODEL=
   361	three TM 0 0 0 FX="$T/fx/TM" CX_AUP_MODEL=
   362	three NM 0 0 0 FX="$T/fx/NM" CX_AUP_MODEL=
   363	three BA 0 0 5 FX="$T/fx/BA" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   364	three HB 0 0 0 FX="$T/fx/HB" CX_AUP_MODEL=
   365	three R7A 0 0 0 FX="$T/fx/R7A" CX_AUP_MODEL=
   366	three R7B 0 0 5 FX="$T/fx/R7B" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   367	
   368	#  E0: the fake ran for every row of every column but X15's, and never for X15's (it must exit 9 BEFORE codex); the run count is
   369	#  pinned, so a deleted row is visible.  The other aggregate checks read the AFTER runs; each pins its own denominator.
   370	cols=3; [ "$ONLY" = 1 ] && cols=1
   371	nruns=$(ls "$T"/log_* 2>/dev/null | wc -l)
   372	miss=""; extra=""
   373	for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}
   374	    case "$b" in X15_*) [ -e "$T/args_$b" ] && extra="$extra $b" ;; *) [ -s "$T/args_$b" ] || miss="$miss $b" ;; esac
   375	done
   376	[ "$nruns" = $((NROWS * cols)) ] && [ -z "$miss" ] && [ -z "$extra" ]; check "E0  all  the fake codex was reached by every run but X15's, and by none of X15's ($NROWS rows x $cols = $nruns of $((NROWS * cols)), pinned)${miss:+ -- NOT reached:$miss}${extra:+ -- X15 REACHED it:$extra}" $?
   377	nafter=0; dbad=""; sbad=""; ns=0; cbad=""; nc=0; pbad=""; fbad=""; nfd=0
   378	for f in "$T"/exit_*_after; do r=${f##*/exit_}; r=${r%_after}; nafter=$((nafter + 1))
   379	    case "$r" in
   380	        DP|EO) [ -e "$T/args_${r}_after.default" ] || dbad="$dbad $r(not reached)" ;;
   381	        *) [ -e "$T/args_${r}_after.default" ] && dbad="$dbad $r" ;;
   382	    esac
   383	    if [ -e "$T/args_${r}_after.stdin" ]; then ns=$((ns + 1)); [ -s "$T/args_${r}_after.stdin" ] && sbad="$sbad $r"; fi
   384	    if [ -e "$T/args_${r}_after.cwd" ]; then nc=$((nc + 1))
   385	        while IFS= read -r d; do [ "$(printf '%s' "$d" | tr 'A-Z' 'a-z')" = /c/documentnosnc/cc/gxemul ] || cbad="$cbad $r"; done < "$T/args_${r}_after.cwd"
   386	    fi
   387	    e=$(cat "$f"); L="$T/log_${r}_after.txt"
   388	    a=$(grep -c 'seat answered' "$L"); l=$(grep -c 'The answer is LOST' "$L"); b=$(grep -c 'answered by: ' "$L"); u=$(grep -c 'model UNVERIFIED' "$L")
   389	    case "$e" in
   390	        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
   391	        7) { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
   392	        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
   393	    esac
   394	    if [ -e "$T/disabled_${r}_after" ] && [ "$r" != X15 ]; then nfd=$((nfd + 1))
   395	        [ "$(grep -c '^CALL$' "$T/args_${r}_after" 2>/dev/null)" = 1 ] || fbad="$fbad $r"
   396	    fi
   397	done
   398	[ "$nafter" = "$NROWS" ] && [ -z "$dbad" ]; check "E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of $nafter)${dbad:+ -- wrong:$dbad}" $?
   399	[ "$ns" = $((NROWS - 1)) ] && [ -z "$sbad" ]; check "SI  after  no after run's codex read the stdin the launcher was fed ($ns runs that reached codex, of $((NROWS - 1)))${sbad:+ -- READ IT:$sbad}" $?
   400	[ "$nc" = $((NROWS - 1)) ] && [ -z "$cbad" ]; check "CWD after  every after run's codex started in the project root ($nc of $((NROWS - 1)))${cbad:+ -- elsewhere:$cbad}" $?
   401	[ "$nfd" = "$NFD" ] && [ -z "$fbad" ]; check "FD  after  every row that sets CX_AUP_MODEL empty made exactly one call ($nfd rows, $NFD pinned)${fbad:+ -- more:$fbad}" $?
   402	[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff exit 7, 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
   403	grep -qE '^codex rc=0   stdout=[0-9]+ b   stderr=[0-9]+ b   asked: gpt-6-astra / ultra$' "$T/log_N1_after.txt"; check "LOG after  N1's 'codex rc=0   stdout=N b   stderr=N b   asked: gpt-6-astra / ultra' line, as the launch-log censuses parse it" $?
   404	[ "$(ls "$T/out_N1_after" | wc -l)" = 2 ] && cmp -s "$T/out_N1_after/codex_N1.txt" "$T/fx/N1/stdout" && cmp -s "$T/out_N1_after/codex_N1.err" "$T/fx/N1/stderr"; check "N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr" $?
   405	grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_N1_after.txt"; check "N1V after  N1 is credited to gpt-6-astra" $?
   406	grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_WS_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_MA_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_TM_after.txt"; check "WMT after  WS, MA and TM verify gpt-6-astra (not UNVERIFIED)" $?
   407	#  content, not exit status -- on the AFTER logs
   408	for r in M2 X6 X9 W13 K31 NM HB; do
   409	    grep -q 'model UNVERIFIED' "$T/log_${r}_after.txt" && ! grep -q 'answered by:' "$T/log_${r}_after.txt"; check "$r  after  says model UNVERIFIED and names no model" $?
   410	done
   411	cmp -s "$T/out_D1_after/codex_D1.refused.txt" "$T/fx/P2/stdout" && cmp -s "$T/out_D1_after/codex_D1.refused.err" "$T/fx/P2/stderr" \
   412	    && cmp -s "$T/out_D1_after/codex_D1.txt" "$T/fx/DB_OK/stdout" && cmp -s "$T/out_D1_after/codex_D1.err" "$T/fx/DB_OK/stderr" \
   413	    && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1R after  refused run kept byte-for-byte as .refused.txt/.err, Daybreak's run as .txt/.err, Daybreak credited" $?
   414	[ "$(grep -c '^CALL$' "$T/args_FB1_after" 2>/dev/null)" = 1 ] && ! ls "$T/out_FB1_after"/*.refused.* >/dev/null 2>&1; check "FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused" $?
   415	[ "$(grep -c '^CALL$' "$T/args_FB2_after" 2>/dev/null)" = 1 ]; check "FB2 after  the fallback on, a wall: ONE call" $?
   416	[ "$(grep -c '^CALL$' "$T/args_D4_after" 2>/dev/null)" = 2 ]; check "D4  after  refused, then refused on Daybreak: EXACTLY two calls" $?
   417	[ "$(grep -c '^CALL$' "$T/args_D3_after" 2>/dev/null)" = 2 ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D3_after.txt"; check "D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited" $?
   418	[ "$(grep -c '^CALL$' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked ON Daybreak and refused: ONE call, no re-run on the same model" $?
   419	[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?
   420	grep -qF "codex's header says gpt-6-astra" "$T/log_CH_after.txt"; check "CH  after  the coloured header is read: the log names gpt-6-astra as the model that ran" $?
   421	#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
   422	callseq() {    # $1 model -- the sequence one call must receive
   423	    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
   424	    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
   425	}
   426	callseq gpt-6-astra > "$T/want_E1"
   427	{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
   428	cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
   429	cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
   430	cmp -s "$T/want_E2" "$T/args_EO_after"; check "EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2" $?
   431	cmp -s "$T/want_E1" "$T/args_DP_after"; check "DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1" $?
   432	echo "CONTROLS: $pass/$total as expected"
   433	echo "CXLAND_CONTROLS_DONE"
   434	[ "$pass" = "$total" ]
```

### 3c. the mutant list, `mut_launcher_v5.py`, WHOLE (each mutant's exact edit and the controls named to kill it)

```python
     1	#!/usr/bin/env python3
     2	"""mut_launcher_v5.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-17 landing, v5) for the
     3	controls' kill table (run_mutants_v5.sh).  Each mutant names the controls expected to catch it; v5 pins every decision its
     4	CONTRACT lists, so no mutant is UNPINNED (v4's three -- m_eq1, m_sgr, m_prec -- are pinned by RC2W, CSI and RW).  The v4 list is
     5	kept whole; v5 adds one mutant per decision the v4 pass found unpinned and per decision the v5 enumeration reads off the file
     6	(run_controls_v5.sh's CONTRACT).  m_twice inserts a line and the m_ord_* mutants MOVE one block of the exit cascade: each is
     7	still one edit.  A find-text that is absent, or present more than once, is an apparatus failure, never a silent skip."""
     8	import io, os, sys
     9	
    10	src, out = sys.argv[1], sys.argv[2]
    11	t = io.open(src, encoding="utf-8", newline="").read()
    12	#  the opening-header awk, as v3/v4 read it, so the find-text cannot drift
    13	AWK = ('HDR=$(strip_ansi "$ERR" | awk \'NR > 12 && h < 2 { exit }\n        h == 0 && /^OpenAI Codex/ { h = 1; next }\n'
    14	       '        h == 1 && /^--------/ { h = 2; next }\n        h == 2 && /^--------/ { exit }\n'
    15	       '        h == 2 { if (++n > 30) exit; print }\')')
    16	STRIP = 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }'
    17	REF = r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help'"
    18	WAL = r"grep -ic 'usage limit\|quota\|rate limit\|not authenticated'"
    19	GATE = 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then'
    20	TRIG = 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then'
    21	
    22	#  the exit cascade, cut from the launcher itself into its five blocks: refusal 7, wall 8, empty 6, identity 5, codex's rc
    23	R0 = 'if [ "$refus" -gt 0 ]; then\n    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.'
    24	W0 = 'if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED'
    25	E0 = 'if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT'
    26	I0 = 'if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then'
    27	C0 = 'if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc'
    28	C1 = 'exit "$rc"; fi\n'
    29	starts = [t.find(x) for x in (R0, W0, E0, I0, C0)]
    30	cend = t.find(C1, starts[4]) + len(C1) if starts[4] >= 0 else -1
    31	if min(starts) < 0 or cend < 0 or starts != sorted(starts) or any(t.count(x) != 1 for x in (R0, W0, E0, I0, C0)):
    32	    print("CASCADE_NOT_FOUND (starts %s)" % starts); sys.exit(1)
    33	B = dict(zip("RWEIC", [t[starts[i]:(starts[i + 1] if i < 4 else cend)] for i in range(5)]))
    34	CASCADE = "".join(B[k] for k in "RWEIC")
    35	
    36	def order(seq):
    37	    return (CASCADE, "".join(B[k] for k in seq))
    38	
    39	MUTANTS = [
    40	    #  v4's table, unchanged
    41	    ("m_anchor", "X1", "grep -a '^ERROR:'", "grep -a 'ERROR:'"),
    42	    ("m_bodyverd", "X2", GATE, 'if [ "$rc" -ne 0 ] || [ "$verd" -eq 0 ]; then'),
    43	    ("m_suffix", "X5", '[ "$RAN" != "$ANSWERED_BY" ]', '[ "${RAN##*-}" != "${ANSWERED_BY##*-}" ]'),
    44	    ("m_effort", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$1"'),
    45	    ("m_head40", "X6", AWK, 'HDR=$(strip_ansi "$ERR" | head -n 40)'),
    46	    ("m_v2awk", "X9 X10", AWK,
    47	     """HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')"""),
    48	    ("m_effortx", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$2x"'),
    49	    ("m_sandbox", "E1 E2", "--sandbox read-only", "--sandbox workspace-write"),
    50	    ("m_brief", "E1 E2", '"$(cat "$BRIEF")"', '"$BRIEF"'),
    51	    ("m_noa", "X8", "grep -a '^ERROR:'", "grep '^ERROR:'"),
    52	    ("m_nostrip", "Q3 A1 CH", STRIP, 'strip_ansi() { cat "$1" 2>/dev/null; }'),
    53	    ("m_noident", "M1 D2 X5", I0, "if false; then"),
    54	    ("m_nofallback", "D1 D2 E2", 'AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"', 'AUP_MODEL=""'),
    55	    ("m_nogate", "N1 X2", GATE, "if true; then"),
    56	    ("m_claimmodel", "M2 X6", 'echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"',
    57	     'echo "  seat answered. (answered by: $ANSWERED_BY)"'),
    58	    ("m_eq1", "RC2W", GATE, 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
    59	    ("m_sgr", "CSI", STRIP, 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
    60	    ("m_prec", "RW", "        wall=$(printf '%s' \"$CXERR\" | " + WAL + ")",
    61	     "        wall=$(printf '%s' \"$CXERR\" | " + WAL + "); [ \"$wall\" -gt 0 ] && refus=0"),
    62	    ("m_win11", "W12", "NR > 12 && h < 2", "NR > 11 && h < 2"),
    63	    ("m_win13", "W13", "NR > 12 && h < 2", "NR > 13 && h < 2"),
    64	    ("m_win3", "W12 X13", "NR > 12 && h < 2", "NR > 3 && h < 2"),
    65	    ("m_cap29", "K30", "if (++n > 30) exit", "if (++n > 29) exit"),
    66	    ("m_cap31", "K31", "if (++n > 30) exit", "if (++n > 31) exit"),
    67	    ("m_nocap", "K31", "h == 2 { if (++n > 30) exit; print }", "h == 2 { print }"),
    68	    ("m_fbeq1", "D3", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -eq 1 ] && [ -n "$AUP_MODEL" ]'),
    69	    ("m_refeq1", "R2X", 'if [ "$refus" -gt 0 ]; then\n    echo', 'if [ "$refus" -eq 1 ]; then\n    echo'),
    70	    ("m_wallgt1", "W1L", 'if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 1 ]; then'),
    71	    ("m_fbge0", "FB1", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -ge 0 ] && [ -n "$AUP_MODEL" ]'),
    72	    ("m_fbwall", "FB2", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]',
    73	     'if { [ "$refus" -gt 0 ] || [ "$wall" -gt 0 ]; } && [ -n "$AUP_MODEL" ]'),
    74	    ("m_twice", "D4 E2", '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n',
    75	     '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n'),
    76	    ("m_argv1", "X15", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 30001 ]'),
    77	    ("m_argv2", "X14", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 29999 ]'),
    78	    #  v5 -- configuration
    79	    ("m_defpath", "DP", 'Codex/bin/codex}"', 'Codex/bin/codex2}"'),
    80	    ("m_binignore", "E0b", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BINX:-'),
    81	    ("m_bincolon", "EO", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BIN-'),
    82	    ("m_modelcolon", "EO", '"${CX_MODEL:-', '"${CX_MODEL-'),
    83	    ("m_effortcolon", "EO", '"${CX_EFFORT:-', '"${CX_EFFORT-'),
    84	    ("m_aupeffcolon", "EO", '"${CX_AUP_EFFORT:-', '"${CX_AUP_EFFORT-'),
    85	    ("m_aupcolon", "FD", '"${CX_AUP_MODEL-', '"${CX_AUP_MODEL:-'),
    86	    ("m_nomkdir", "N1", 'mkdir -p "$OUT"', ': mkdir -p "$OUT"'),
    87	    ("m_txtname", "N1F", 'TXT="$OUT/codex_${TAG}.txt"', 'TXT="$OUT/codex_${TAG}.out"'),
    88	    ("m_errname", "N1F", 'ERR="$OUT/codex_${TAG}.err"', 'ERR="$OUT/codex_${TAG}.log"'),
    89	    ("m_swapio", "N1F", '> "$TXT" 2> "$ERR" < /dev/null', '> "$ERR" 2> "$TXT" < /dev/null'),
    90	    ("m_nostdin", "SI", '2> "$ERR" < /dev/null', '2> "$ERR"'),
    91	    ("m_cd", "CWD", 'cd "$PROJ" || exit 9', 'cd "$HOME" || exit 9'),
    92	    ("m_noskip", "E1", ' --skip-git-repo-check', ''),
    93	    #  v5 -- the opening header
    94	    ("m_hdrnostrip", "CH", 'HDR=$(strip_ansi "$ERR" | awk', 'HDR=$(cat "$ERR" | awk'),
    95	    ("m_hlt1", "W13", "NR > 12 && h < 2", "NR > 12 && h < 1"),
    96	    ("m_hlt3", "K30 W12", "NR > 12 && h < 2", "NR > 12 && h < 3"),
    97	    ("m_bannerun", "BA", "h == 0 && /^OpenAI Codex/", "h == 0 && /OpenAI Codex/"),
    98	    ("m_bannerh", "HB", "h == 0 && /^OpenAI Codex/", "/^OpenAI Codex/"),
    99	    ("m_rule1h", "BA", "h == 1 && /^--------/ { h = 2; next }", "/^--------/ { h = 2; next }"),
   100	    ("m_rule7a", "R7A", "h == 1 && /^--------/", "h == 1 && /^-------/"),
   101	    ("m_rule1next", "M1", "{ h = 2; next }", "{ h = 2 }"),
   102	    ("m_close2h", "BA", "h == 2 && /^--------/ { exit }", "/^--------/ { exit }"),
   103	    ("m_rule7b", "R7B", "h == 2 && /^--------/ { exit }", "h == 2 && /^-------/ { exit }"),
   104	    ("m_exitnext", "NM", "h == 2 && /^--------/ { exit }", "h == 2 && /^--------/ { next }"),
   105	    ("m_bodyh1", "R7A", "h == 2 { if (++n > 30) exit; print }", "h >= 1 { if (++n > 30) exit; print }"),
   106	    ("m_capn", "K31", "if (++n > 30) exit", "if (n++ > 30) exit"),
   107	    ("m_m2", "TM", "grep -m1 '^model:'", "grep -m2 '^model:'"),
   108	    ("m_modelanchor", "MA", "grep -m1 '^model:'", "grep -m1 'model:'"),
   109	    ("m_trailws", "WS", "s/^model:[[:space:]]*//; s/[[:space:]]*$//'", "s/^model:[[:space:]]*//'"),
   110	    ("m_leadws", "WS", "s/^model:[[:space:]]*//", "s/^model: //"),
   111	    ("m_nomodelsed", "N1", "sed 's/^model:[[:space:]]*//; s/", "sed 's/"),
   112	    #  v5 -- classification
   113	    ("m_strip_nog", "A1 CSI", '[A-Za-z]//g" "$1"', '[A-Za-z]//" "$1"'),
   114	    ("m_strip_nosemi", "CSI", '\\[[0-9;]*[A-Za-z]', '\\[[0-9]*[A-Za-z]'),
   115	    ("m_noinit", "N1", "refus=0; wall=0", ":"),
   116	    ("m_gateand", "N4 RC2W", GATE, 'if [ "$rc" -ne 0 ] && [ "$body" -eq 0 ]; then'),
   117	    ("m_gatele1", "B1G", GATE, 'if [ "$rc" -ne 0 ] || [ "$body" -le 1 ]; then'),
   118	    ("m_ref1", "P2", REF, r"grep -ic 'cannot help with\|can.t help with\|I won.t help'"),
   119	    ("m_ref2", "RF1", REF, r"grep -ic 'flagged for possible cybersecurity\|can.t help with\|I won.t help'"),
   120	    ("m_ref3", "RF2", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|I won.t help'"),
   121	    ("m_ref4", "RF3", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with'"),
   122	    ("m_refcase", "RFC", REF, REF.replace("grep -ic", "grep -c")),
   123	    ("m_wall1", "P1", WAL, r"grep -ic 'quota\|rate limit\|not authenticated'"),
   124	    ("m_wall2", "WL1", WAL, r"grep -ic 'usage limit\|rate limit\|not authenticated'"),
   125	    ("m_wall3", "WL2", WAL, r"grep -ic 'usage limit\|quota\|not authenticated'"),
   126	    ("m_wall4", "WL3", WAL, r"grep -ic 'usage limit\|quota\|rate limit'"),
   127	    ("m_wallcase", "WLC", WAL, WAL.replace("grep -ic", "grep -c")),
   128	    #  v5 -- the fallback
   129	    ("m_samemodel", "D5", TRIG, 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]; then'),
   130	    ("m_noempty", "FD", TRIG, 'if [ "$refus" -gt 0 ] && [ "$AUP_MODEL" != "$MODEL" ]; then'),
   131	    ("m_norefusedtxt", "D1R", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; ', ''),
   132	    ("m_norefusederr", "D1R", '; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"', ''),
   133	    ("m_ansby", "D1 D2", '    ANSWERED_BY="$AUP_MODEL"', '    ANSWERED_BY="$MODEL"'),
   134	    #  v5 -- the exit cascade
   135	    ("m_emptyle1", "B1E", E0, 'if [ "$body" -le 1 ]; then echo "  *** EMPTY STDOUT'),
   136	    ("m_noransep", "M2", I0, 'if [ "$RAN" != "$ANSWERED_BY" ]; then'),
   137	    ("m_zflip", "M2 N1V", 'if [ -z "$RAN" ]; then', 'if [ -n "$RAN" ]; then'),
   138	    ("m_rcpass", "RC1A RC3A", 'if [ "$rc" -ne 0 ];  then', 'if false;  then'),
   139	    ("m_rcgt1", "RC1A", 'if [ "$rc" -ne 0 ];  then', 'if [ "$rc" -gt 1 ];  then'),
   140	    ("m_rcone", "RC3A", C1, 'exit 1; fi\n'),
   141	    ("m_ord_wr", "RW",) + order("WREIC"),
   142	    ("m_ord_re", "P2",) + order("ERWIC"),
   143	    ("m_ord_ri", "RI",) + order("IRWEC"),
   144	    ("m_ord_rc", "P2",) + order("CRWEI"),
   145	    ("m_ord_we", "P1",) + order("REWIC"),
   146	    ("m_ord_wi", "WI",) + order("RIWEC"),
   147	    ("m_ord_wc", "P1",) + order("RCWEI"),
   148	    ("m_ord_ei", "EM",) + order("RWIEC"),
   149	    ("m_ord_ec", "X1",) + order("RWCEI"),
   150	    ("m_ord_ic", "IR",) + order("RWECI"),
   151	    #  v5 -- the log phrases a caller reads
   152	    ("m_msganswered", "PK", 'echo "  seat answered. (answered by:', 'echo "  seat replied. (answered by:'),
   153	    ("m_msganswered2", "PK", 'echo "  seat answered -- model UNVERIFIED', 'echo "  seat replied -- model UNVERIFIED'),
   154	    ("m_msglost", "PK", "The answer is LOST, whatever", "The answer is gone, whatever"),
   155	    ("m_msgby", "PK N1V", "(answered by: $ANSWERED_BY)", "(by: $ANSWERED_BY)"),
   156	    ("m_rcline", "LOG", 'echo "codex rc=$rc   stdout=', 'echo "codex rc=$rc stdout='),
   157	]
   158	os.makedirs(out, exist_ok=True)
   159	bad = 0
   160	names = set()
   161	with io.open(os.path.join(out, "MUTANTS.list"), "w", encoding="utf-8", newline="\n") as lst:
   162	    for name, catches, find, repl in MUTANTS:
   163	        n = t.count(find)
   164	        if n != 1 or name in names or find == repl:
   165	            print("MUTANT_TEXT_NOT_FOUND %s (found %d)" % (name, n)); bad += 1; continue
   166	        names.add(name)
   167	        io.open(os.path.join(out, name + ".sh"), "w", encoding="utf-8", newline="").write(t.replace(find, repl))
   168	        lst.write("%s\t%s\n" % (name, catches))
   169	print("mutants written: %d of %d" % (len(MUTANTS) - bad, len(MUTANTS)))
   170	sys.exit(1 if bad else 0)
```

### 3d. `CENSUS_v5.txt` (`census_v5.py`)

```
roots: C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC C:\DocumentNoSnc\cc\GXEMUL\_scratchpad
POPULATIONS: CODEX 2425 files | ALLERR 8590 files | LAUNCH 699 files (466 carrying a `codex rc=' line)
1. CODEX opening blocks by the landed rule (window 12, cap 30): 975 of 2425 files | no model line: 0 | two or more: 0 | not closed within the cap: 0
   banner line: {2: 974, 4: 1}
   first rule line: {3: 974, 5: 1}
   model line (file line): {5: 974, 7: 1}
   blocks carrying ANSI escapes: 149 of 975 (answered runs -- sibling .txt non-empty: 105)
   synthetic row shapes, blocks (R7: files): WS 0 | MA 0 | HB 0 | NM 0 | BA 0 | R7 0 (of 2425 files)
2. CODEX escapes: 2425 files read | with ESC 198 | non-SGR CSI 0 | `;'-joined SGR 44 | OSC 0 | other ESC 2
2. ALLERR escapes: 8590 files read | with ESC 198 | non-SGR CSI 0 | `;'-joined SGR 44 | OSC 0 | other ESC 2
3. CODEX column-0 ERROR lines (after the strip): 1095 lines in 498 files
   refusal: flagged for possible cybersecurity case-insensitive   456 lines /  308 files | case-sensitive   456 | case-only 0
   refusal: cannot help with            case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
   refusal: can.t help with             case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
   refusal: I won.t help                case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
   wall: usage limit                    case-insensitive   209 lines /  143 files | case-sensitive   209 | case-only 0
   wall: quota                          case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
   wall: rate limit                     case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
   wall: not authenticated              case-insensitive     0 lines /    0 files | case-sensitive     0 | case-only 0
4. the empty-or-absent-sibling subset of CODEX: 410 of 2425 files | carrying BOTH a refusal and a wall ERROR line: 0
5. LAUNCH `codex rc=' lines: 474 | rc 0 stdout: 440, rc 1 empty: 34
CENSUS_V5_DONE
```

## 4. The receipts

### 4a. `RECEIPT_v5.txt` -- the AFTER rows and every content check (the tracked and before rows, which record the old
files, and the indented per-run output are in the file)

```
# cxlaunch landing controls (v5), 2026-10-17 04:02:07
# tracked: cb180d9d58da2c0b05defe48c65b7ad0  cxlaunch_tracked.sh
# before:  3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:   af18158ed30b740cb13604de64013323  /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
P1   after   exit=8   want=8   ok
P2   after   exit=7   want=7   ok
N1   after   exit=0   want=0   ok
N2   after   exit=0   want=0   ok
N3   after   exit=6   want=6   ok
N4   after   exit=8   want=8   ok
Q1   after   exit=7   want=7   ok
Q2   after   exit=8   want=8   ok
Q3   after   exit=8   want=8   ok
A1   after   exit=7   want=7   ok
M1   after   exit=5   want=5   ok
M2   after   exit=0   want=0   ok
D1   after   exit=0   want=0   ok
D2   after   exit=5   want=5   ok
X1   after   exit=6   want=6   ok
X2   after   exit=0   want=0   ok
X5   after   exit=5   want=5   ok
X6   after   exit=0   want=0   ok
X8   after   exit=8   want=8   ok
X9   after   exit=0   want=0   ok
X10  after   exit=0   want=0   ok
W12  after   exit=5   want=5   ok
W13  after   exit=0   want=0   ok
X13  after   exit=5   want=5   ok
K30  after   exit=5   want=5   ok
K31  after   exit=0   want=0   ok
R2X  after   exit=7   want=7   ok
D3   after   exit=0   want=0   ok
D4   after   exit=7   want=7   ok
W1L  after   exit=8   want=8   ok
FB1  after   exit=0   want=0   ok
FB2  after   exit=8   want=8   ok
X14  after   exit=0   want=0   ok
X15  after   exit=9   want=9   ok
RC1A after   exit=1   want=1   ok
RC3A after   exit=3   want=3   ok
RC2W after   exit=8   want=8   ok
B1G  after   exit=0   want=0   ok
B1E  after   exit=0   want=0   ok
D5   after   exit=7   want=7   ok
CH   after   exit=5   want=5   ok
DP   after   exit=0   want=0   ok
EO   after   exit=0   want=0   ok
RF1  after   exit=7   want=7   ok
RF2  after   exit=7   want=7   ok
RF3  after   exit=7   want=7   ok
RFC  after   exit=7   want=7   ok
WL1  after   exit=8   want=8   ok
WL2  after   exit=8   want=8   ok
WL3  after   exit=8   want=8   ok
WLC  after   exit=8   want=8   ok
CSI  after   exit=7   want=7   ok
RW   after   exit=7   want=7   ok
RI   after   exit=7   want=7   ok
WI   after   exit=8   want=8   ok
EM   after   exit=6   want=6   ok
IR   after   exit=5   want=5   ok
WS   after   exit=0   want=0   ok
MA   after   exit=0   want=0   ok
TM   after   exit=0   want=0   ok
NM   after   exit=0   want=0   ok
BA   after   exit=5   want=5   ok
HB   after   exit=0   want=0   ok
R7A  after   exit=0   want=0   ok
R7B  after   exit=5   want=5   ok
E0  all  the fake codex was reached by every run but X15's, and by none of X15's (65 rows x 3 = 195 of 195, pinned)  ok
E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of 65)  ok
SI  after  no after run's codex read the stdin the launcher was fed (64 runs that reached codex, of 64)  ok
CWD after  every after run's codex started in the project root (64 of 64)  ok
FD  after  every row that sets CX_AUP_MODEL empty made exactly one call (56 rows, 56 pinned)  ok
PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff exit 7, 'answered by:' iff a verified exit 0 (65 runs)  ok
LOG after  N1's 'codex rc=0   stdout=N b   stderr=N b   asked: gpt-6-astra / ultra' line, as the launch-log censuses parse it  ok
N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr  ok
N1V after  N1 is credited to gpt-6-astra  ok
WMT after  WS, MA and TM verify gpt-6-astra (not UNVERIFIED)  ok
M2  after  says model UNVERIFIED and names no model  ok
X6  after  says model UNVERIFIED and names no model  ok
X9  after  says model UNVERIFIED and names no model  ok
W13  after  says model UNVERIFIED and names no model  ok
K31  after  says model UNVERIFIED and names no model  ok
NM  after  says model UNVERIFIED and names no model  ok
HB  after  says model UNVERIFIED and names no model  ok
D1R after  refused run kept byte-for-byte as .refused.txt/.err, Daybreak's run as .txt/.err, Daybreak credited  ok
FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused  ok
FB2 after  the fallback on, a wall: ONE call  ok
D4  after  refused, then refused on Daybreak: EXACTLY two calls  ok
D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited  ok
D5  after  asked ON Daybreak and refused: ONE call, no re-run on the same model  ok
X15 after  a 30,001-byte brief never reaches codex  ok
CH  after  the coloured header is read: the log names gpt-6-astra as the model that ran  ok
E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief  ok
E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each  ok
EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2  ok
DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1  ok
CONTROLS: 224/224 as expected
CXLAND_CONTROLS_DONE
```

### 4b. `KILLTABLE_v5_md5_236cda5f.txt`, whole (`run_mutants_v5.sh`: each mutant through the after column; the base run is all three)

It ran at 03:00 on launcher md5 236cda5f and controls md5 362c8a93.  Since then the launcher gained the three-line usage
comment of U21 and the controls the two disclosures of U21/U22 -- comments only (section 3a' carries the launcher's
diff).  The receipt in 4a is of the FINAL files (af18158e); the table's re-run on them is in progress and is the one the
record will cite.

```
mutants written: 105 of 105
# kill table for /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh (236cda5fc25147cd427c1dfb328a1416), 2026-10-17 03:00:25, 4 at a time; controls 362c8a93095ca2cc8b38fe65c97583e6
BASE      CONTROLS: 224/224 as expected
BASE      65 rows; a mutant's after-only run must total 94
m_anchor        93/94    killed by: X1                                                  [X1]
m_bodyverd      92/94    killed by: B1G X2                                              [X2]
m_suffix        93/94    killed by: X5                                                  [X5]
m_effort        90/94    killed by: DP E1 E2 EO                                         [E1 E2]
m_head40        80/94    killed by: BA HB K31 NM R7A W13 X10 X6 X9                      [X6]
m_v2awk         86/94    killed by: HB K31 W13 X10 X9                                   [X9 X10]
m_effortx       90/94    killed by: DP E1 E2 EO                                         [E1 E2]
m_sandbox       90/94    killed by: DP E1 E2 EO                                         [E1 E2]
m_brief         90/94    killed by: DP E1 E2 EO                                         [E1 E2]
m_noa           93/94    killed by: X8                                                  [X8]
m_nostrip       86/94    killed by: A1 CH CSI D3 Q3 R2X                                 [Q3 A1 CH]
m_noident       83/94    killed by: BA CH D2 IR K30 M1 R7B W12 X13 X5                   [M1 D2 X5]
m_nofallback    85/94    killed by: D1 D1R D2 D3 D4 E2 EO                               [D1 D2 E2]
m_nogate        87/94    killed by: B1G FB1 M1 N1 N1V X2 X5                             [N1 X2]
m_claimmodel    87/94    killed by: HB K31 M2 NM W13 X6 X9                              [M2 X6]
m_eq1           93/94    killed by: RC2W                                                [RC2W]
m_sgr           93/94    killed by: CSI                                                 [CSI]
m_prec          93/94    killed by: RW                                                  [RW]
m_win11         93/94    killed by: W12                                                 [W12]
m_win13         92/94    killed by: W13                                                 [W13]
m_win3          91/94    killed by: BA W12 X13                                          [W12 X13]
m_cap29         93/94    killed by: K30                                                 [K30]
m_cap31         92/94    killed by: K31                                                 [K31]
m_nocap         92/94    killed by: K31                                                 [K31]
m_fbeq1         92/94    killed by: D3                                                  [D3]
m_refeq1        93/94    killed by: R2X                                                 [R2X]
m_wallgt1       88/94    killed by: W1L WI WL1 WL2 WL3 WLC                              [W1L]
m_fbge0         91/94    killed by: FB1 FB2                                             [FB1]
m_fbwall        93/94    killed by: FB2                                                 [FB2]
m_twice         90/94    killed by: D3 D4 E2 EO                                         [D4 E2]
m_argv1         89/94    killed by: CWD E0 SI X15                                       [X15]
m_argv2         89/94    killed by: CWD E0 FD SI X14                                    [X14]
m_defpath       85/94    killed by: CWD DP E0 E0b EO FD SI                              [DP]
m_binignore     93/94    killed by: E0b                                                 [E0b]
m_bincolon      88/94    killed by: CWD E0 E0b EO SI                                    [EO]
m_modelcolon    93/94    killed by: EO                                                  [EO]
m_effortcolon   93/94    killed by: EO                                                  [EO]
m_aupeffcolon   93/94    killed by: EO                                                  [EO]
m_aupcolon      93/94    killed by: FD                                                  [FD]
m_nomkdir       4/94     killed by: A1 B1E B1G BA CH CSI CWD D1 D1R D2 D3 D4 D5 DP E0 E0b E1 E2 EM EO FB1 FB2 FD HB IR K30 K31 LOG M1 M2 MA N1 N1F N1V N2 N3 N4 NM P1 P2 Q1 Q2 Q3 R2X R7A R7B RC2W RC3A RF1 RF2 RF3 RFC RI RW SI TM W12 W13 W1L WI WL1 WL2 WL3 WLC WMT WS X1 X10 X13 X14 X2 X5 X6 X8 X9  [N1]
m_txtname       92/94    killed by: D1R N1F                                             [N1F]
m_errname       92/94    killed by: D1R N1F                                             [N1F]
m_swapio        41/94    killed by: A1 BA CH CSI D1 D1R D2 D3 D4 D5 E2 EM EO FB2 IR K30 M1 M2 N1F N1V N2 N4 P1 P2 Q1 Q2 Q3 R2X R7B RC2W RF1 RF2 RF3 RFC RI RW W12 W1L WI WL1 WL2 WL3 WLC WMT X1 X13 X5 X8  [N1F]
m_nostdin       93/94    killed by: SI                                                  [SI]
m_cd            93/94    killed by: CWD                                                 [CWD]
m_noskip        90/94    killed by: DP E1 E2 EO                                         [E1]
m_hdrnostrip    92/94    killed by: CH                                                  [CH]
m_hlt1          92/94    killed by: W13                                                 [W13]
m_hlt3          92/94    killed by: K30 W12                                             [K30 W12]
m_bannerun      93/94    killed by: BA                                                  [BA]
m_bannerh       92/94    killed by: HB                                                  [HB]
m_rule1h        89/94    killed by: BA HB NM                                            [BA]
m_rule7a        93/94    killed by: R7A                                                 [R7A]
m_rule1next     79/94    killed by: BA CH D1R D2 D3 IR K30 M1 N1V R7B W12 WMT X13 X5    [M1]
m_close2h       93/94    killed by: BA                                                  [BA]
m_rule7b        93/94    killed by: R7B                                                 [R7B]
m_exitnext      90/94    killed by: HB NM                                               [NM]
m_bodyh1        93/94    killed by: R7A                                                 [R7A]
m_capn          92/94    killed by: K31                                                 [K31]
m_m2            92/94    killed by: TM WMT                                              [TM]
m_modelanchor   92/94    killed by: MA WMT                                              [MA]
m_trailws       92/94    killed by: WMT WS                                              [WS]
m_leadws        92/94    killed by: WMT WS                                              [WS]
m_nomodelsed    75/94    killed by: B1E CH D1 D1R D3 DP EO FB1 MA N1 N1V R7A RC1A RC3A TM WMT WS X14  [N1]
m_strip_nog     87/94    killed by: A1 CH CSI D3 Q3 R2X                                 [A1 CSI]
m_strip_nosemi  93/94    killed by: CSI                                                 [CSI]
m_noinit        50/94    killed by: B1E B1G BA CH D1 D1R D2 D3 DP EO FB1 HB K30 K31 M1 M2 MA N1 N1V N2 NM R7A R7B TM W12 W13 WMT WS X10 X13 X14 X2 X5 X6 X9  [N1]
m_gateand       91/94    killed by: N4 Q2 RC2W                                          [N4 RC2W]
m_gatele1       93/94    killed by: B1G                                                 [B1G]
m_ref1          75/94    killed by: A1 CSI D1 D1R D2 D3 D4 D5 E2 EO P2 Q1 R2X RFC RI RW  [P2]
m_ref2          93/94    killed by: RF1                                                 [RF1]
m_ref3          93/94    killed by: RF2                                                 [RF2]
m_ref4          93/94    killed by: RF3                                                 [RF3]
m_refcase       93/94    killed by: RFC                                                 [RFC]
m_wall1         84/94    killed by: FB2 N4 P1 Q2 Q3 RC2W W1L WI WLC X8                  [P1]
m_wall2         93/94    killed by: WL1                                                 [WL1]
m_wall3         93/94    killed by: WL2                                                 [WL2]
m_wall4         93/94    killed by: WL3                                                 [WL3]
m_wallcase      93/94    killed by: WLC                                                 [WLC]
m_samemodel     93/94    killed by: D5                                                  [D5]
m_noempty       93/94    killed by: FD                                                  [FD]
m_norefusedtxt  93/94    killed by: D1R                                                 [D1R]
m_norefusederr  93/94    killed by: D1R                                                 [D1R]
m_ansby         88/94    killed by: D1 D1R D2 D3 EO                                     [D1 D2]
m_emptyle1      92/94    killed by: B1E B1G                                             [B1E]
m_noransep      76/94    killed by: B1G HB K31 M2 N2 NM W13 X10 X2 X6 X9                [M2]
m_zflip         83/94    killed by: D1R D3 HB K31 M2 N1V NM W13 WMT X6 X9               [M2 N1V]
m_rcpass        92/94    killed by: RC1A RC3A                                           [RC1A RC3A]
m_rcgt1         93/94    killed by: RC1A                                                [RC1A]
m_rcone         93/94    killed by: RC3A                                                [RC3A]
m_ord_wr        93/94    killed by: RW                                                  [RW]
m_ord_re        70/94    killed by: A1 CSI D4 D5 FB2 P1 P2 Q1 Q2 Q3 R2X RF1 RF2 RF3 RFC RI RW W1L WI WL1 WL2 WL3 WLC X8  [P2]
m_ord_ri        91/94    killed by: EM RI WI                                            [RI]
m_ord_rc        67/94    killed by: A1 CSI D4 D5 FB2 IR N4 P1 P2 Q1 Q3 R2X RC2W RF1 RF2 RF3 RFC RI RW W1L WI WL1 WL2 WL3 WLC X1 X8  [P2]
m_ord_we        83/94    killed by: FB2 P1 Q2 Q3 W1L WI WL1 WL2 WL3 WLC X8              [P1]
m_ord_wi        92/94    killed by: EM WI                                               [WI]
m_ord_wc        80/94    killed by: FB2 IR N4 P1 Q3 RC2W W1L WI WL1 WL2 WL3 WLC X1 X8   [P1]
m_ord_ei        93/94    killed by: EM                                                  [EM]
m_ord_ec        92/94    killed by: IR X1                                               [X1]
m_ord_ic        93/94    killed by: IR                                                  [IR]
m_msganswered   91/94    killed by: N1V PK WMT                                          [PK]
m_msganswered2  93/94    killed by: PK                                                  [PK]
m_msglost       93/94    killed by: PK                                                  [PK]
m_msgby         89/94    killed by: D1R D3 N1V PK WMT                                   [PK N1V]
m_rcline        93/94    killed by: LOG                                                 [LOG]
KILL TABLE: 105/105 as recorded
CXLAND_MUTANTS_DONE
```

## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A.

## 6. Questions

1. **Your own v4 findings** (the U-rows naming you): is my disposition right, AND is the fix right -- does the named row go
   red under the named mutant FOR THE REASON NAMED?  Be harder on the ones you raised than on anyone else's.
2. **The enumeration.**  List every decision of `tools/cxlaunch.sh` you checked against the CONTRACT, by construct.  For a
   decision that is missing, or a listed row that does not straddle its edge, give the exact one-edit mutant, which of the
   224 controls it passes, and the property it breaks.  A zero is evidence only with its denominator.
3. **The kill table** (section 4b).  Is any mutant killed for a reason other than the one its line names?  Is there a one-edit
   mutant OUTSIDE the table that passes all 224 controls and breaks a line of the CONTRACT?  Name the shapes you swept.
4. **The records** (section 5).  Which sentences are false of what ships?
5. **U7** (section 2c): pin or disclose -- rule on it.  And **U21**: fix the relative-path behaviour in this landing, or disclose and file?
6. **Which of my 22 dispositions is WRONG?**  Name the count you checked.

Open with your verdict line: `VERDICT: SHIP` / `VERDICT: SHIP WITH CHANGES (n)` / `VERDICT: DO NOT SHIP`.  Label each claim
MEASURED (you ran it), READ (you opened the file) or REASONED.  Write nothing to any project tree.
