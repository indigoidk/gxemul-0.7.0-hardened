# V6 PASS -- `cxlaunchquotation` / `cxlaunchdaybreak`: the codex launcher `tools/cxlaunch.sh`, v6 = EACH DECISION'S VALUES, NOT ITS DEFAULTS

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a shell wrapper that launches a read-only
review CLI and classifies its exit, and of the test harness that pins it.  READ-ONLY: write nothing to any project tree.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v6 launcher is `tools/cxlaunch.sh` in the WORKING TREE (uncommitted;
v5 is preserved as `regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v5.sh`, md5 af18158e -- v6 changes ONE
executable line, the UNVERIFIED message's wording, and comments); the controls and mutant table are `run_controls_v6.sh`,
`run_mutants_v6.sh` and `mut_launcher_v6.py` beside it; the v5-pass answers are in `v5pass/`, with the main loop's
measurement of every claimed escape in `v5pass/main_meas.txt` (one `.out` per mutant in `v5pass/main_meas/`).  Everything a
packet-fed seat needs is inlined below.

**Why v6.**  The v5 pass -- all four seats -- found the v5 CONTRACT's enumeration right in kind and short in one shape: **a
row pinned the DEFAULT of a value, not the value; a FRESH state, not a used one.**  Every override was honoured only as
empty or default (CX_EFFORT=ultra, the fallback's effort and model, the main call's model); `>` and `2>` never met a used
out dir; `mkdir -p` never met a missing parent; the refused run's stdout was always empty; the fallback's own rc was never
nonzero with an answer; the rule patterns met no separator off column 0 and no nine-dash rule; the strip met no
parameterless CSI; the trims met no `model:` without a space; the banner met no near-miss; the `codex rc=` line's numbers
were never compared.  **The main loop MEASURED every claimed escape before acting on it: 18 of 18 pass all 94 after-column
checks of the v5 controls** (`v5pass/main_meas.txt`), and Fable 5.1 measured 19 more forms of the same shapes.  The records
had five false sentences (section 2, Y11-Y17).  v6 rows each value, each used state and each edge: the controls grew from
65 rows / 224 checks to 78 rows / 269 checks, the kill table from 105 to 133 mutants.

**All four seats graded the v5 pass ZERO floor breaches; v6 is run anyway, for the material:** thirteen new rows, a
rewritten PK and LOG, a flake re-run in the table driver, and one changed message line.  **If this pass finds zero floor
breaches that survive adjudication, the chain closes here.**  Check the premises in 2b; do not ratify them.

**Liveness:** open your answer with the token `ASTRA_CXLANDV6_20261017` on its own line, then your verdict line.

## 1. The v5-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (5)** (`v5pass/fable5_cxlandv5.md`; claude-fable-5-1 throughout, verified).  Measured in a
  mirror: 224/224 reproduced; 53 decision constructs read off the file; 21 one-edit mutants -- 19 valid escapes, 11 killed by
  five rows it built and measured (OV, SO, NP, ESCM, LOG2 = v6's OV, RS, MP, CZ, LOG); U21's disclosure a WRONG RECORD.
* **GPT-6 Astra -- SHIP WITH CHANGES (5)** (`v5pass/codex_cxlandv5.txt`).  Fifteen one-edit survivors reasoned; five record
  corrections; the 44-file provenance.
* **Grok 4.7 -- SHIP WITH CHANGES (2)** (`v5pass/grok_cxlandv5.txt`).  The truncation edge with its production path (the
  pack runner retries into the same out dir); two false sentences.
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`v5pass/glm_cxlandv5.txt`).  The truncation and effort edges; five unnamed items.

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| Y1 | all four | the override VALUES: `CX_EFFORT`, `CX_AUP_EFFORT`, a non-default `CX_MODEL` / `CX_AUP_MODEL` -- each honoured only as empty or default, so hardcoding any of them passes all 224 | **PINNED**: row OV (`CX_MODEL=m-primary CX_EFFORT=low CX_AUP_MODEL=m-fallback CX_AUP_EFFORT=high`, a refusal then an answer whose header names m-fallback) and check OVA (both calls' argument sequences compared WHOLE, the fallback credited).  Mutants `m_effortfix`, `m_aupeffortfix`, `m_aupcalleff`, `m_mainmodelfix`, `m_aupmodelfix` (the main loop's), `m_effortignore`, `m_aupeffignore`, `m_effortglobal`, `m_ansbyhard` (Fable's) |
| Y2 | all four | the redirections TRUNCATE: `>>` and `2>>` pass (every out dir fresh), while the pack runner retries a 5 or a 6 into the SAME out dir (Grok, Fable: `run_pack_body.sh`) | **PINNED**: row RS (the out dir pre-seeded with a stale answer and a stale header naming another model) and check RSF (both files byte-for-byte the new run's); `2>>` also exits 5 (the stale header is read first).  Mutants `m_append`, `m_appenderr` |
| Y3 | Astra, GLM, Fable (Grok: disclose) | `mkdir -p` -> `mkdir` passes (every out dir's parent exists) | **PINNED** (three of four; one row is cheaper than the argument): row MP (the out dir two levels below a missing parent) and check MPF.  Mutant `m_mkdirnop` |
| Y4 | Astra | the FALLBACK run's own rc: `rc=$?` after `run_codex ...; ` resets it to the echo's 0, so a fallback answer with rc 3 becomes success | **PINNED**: row FR (a refusal, then a Daybreak answer with rc 3 -> 3).  Mutant `m_fbrc` |
| Y5 | Astra | the refused run's stdout was always EMPTY, so replacing its move with `: > .refused.txt` passes | **PINNED**: row RN (a refusal whose stdout holds a partial answer) and check RNF (`.refused.txt` byte-for-byte that answer).  Mutant `m_refusedempty` |
| Y6 | Astra | the rule patterns' `^`: unanchored first-rule and closing-rule patterns pass | **PINNED**: rows SP1 (`x --------` before the first rule) and SP2 (`note: a -------- b` inside the body).  Mutants `m_rule1unanch`, `m_rule2unanch` |
| Y7 | Grok (Fable read it the other way) | "nine find no block anywhere" is false of the PATTERN -- `^--------` has no end anchor, so nine dashes ARE a rule | **CORRECTED and PINNED**: the CONTRACT says nine dashes are a rule; rows R9A (nine-dash rules read) and R9B (a nine-dash close: a model after it not read) pin the pattern's own edge.  MEASURED: every line opening with eight dashes in the first 42 lines of 2,427 codex `.err` files is exactly eight (1,954 lines, `v5pass/RULELEN_CENSUS.txt`) -- Fable's reading, true of the record.  Mutants `m_rule1end`, `m_rule2end` |
| Y8 | Astra, Fable | a parameterless CSI (`ESC[m`): the strip's `*` narrowed to one-or-more passes | **PINNED**: row CZ (`ESC[mERROR: ...flagged...`, rc 1 -> 7).  Mutants `m_csi1`, `m_stripplus` |
| Y9 | Astra | `model:gpt-6-astra` (no whitespace): the trim's `*` narrowed passes | **PINNED**: row WZ, and WMT now names it.  Mutant `m_ws1` |
| Y10 | GLM | the banner's TEXT: `/^OpenAI Codex/` widened to `/^OpenAI/` passes | **PINNED**: row BN (`OpenAI notice:` and a block above the real banner).  Mutant `m_bannercodex` |
| Y11 | Astra | the CONTRACT said no caller reads the wall wording; `_scratchpad/codexpack_20260928/status.sh:16` counts `SEAT WALLED` | **CORRECTED and PINNED**: the caller set re-derived by grep (the two pack scripts and census_v5.py, named in the CONTRACT with the command); PK asserts `SEAT WALLED` iff exit 8.  Mutant `m_wallmsg` |
| Y12 | Astra, Fable | LOG read the line's FORMAT, not its numbers: `stdout=$(wc -c < "$ERR")` passes; the fallback line's `asked:` unread | **PINNED**: LOG compares N1's line, BOTH of D1's and RC3A's WHOLE, each number the fixture's own.  Mutants `m_stdoutcnt`, `m_stderrcnt`, `m_logrc`, `m_askedglobal` |
| Y13 | Astra | "`The answer is LOST` iff exit 7" is false: codex's own rc 7 also exits 7, printing `codex exited 7` | **CORRECTED and PINNED**: PK reads LOST as the REFUSAL exit's; row R7X and check R7XL (rc 7 with an answer: `codex exited 7`, neither LOST nor answered); the launcher's exit list says so.  Mutant `m_lost7` |
| Y14 | Astra | the UNVERIFIED message says "no codex header block in stderr", false of NM (a block with no model line) | **FIXED** -- v6's ONE executable change: "no model line in an opening codex header block"; the KNOWN RESIDUALS bullet likewise |
| Y15 | Astra (U22) | 42 of the 44 `;`-SGR files are the #544 control stub's own output | **MEASURED TRUE** (`v5pass/SEMISGR_WHERE.txt`: 42 stub outputs, 2 mid-line quotations of a coloured GXemul prompt at lines 1,581 and 1,650); the CONTRACT now calls CSI synthetic in BOTH halves |
| Y16 | Fable (all four: disclose and file) | U21's disclosure was a WRONG RECORD: a missing or relative brief reaches codex as an EMPTY prompt, and an answer to it is reported `seat answered`, exit 0 (measured with the fake) -- the 2026-10-17 exit 1 was codex's | **CORRECTED** in the usage line and the CONTRACT; **FILED on `cxlaunchempty`**, the open row whose defect this is (an empty prompt reaching codex) by a second road, with the relative OUT dir and Fable's one-change shape -- no duplicate row.  Its NUL half is recorded closed by this landing (X8) |
| Y17 | Grok, Astra | "every caller on record passes absolute paths" -- the main loop's own relative launch is on record | **CORRECTED**: "every caller in the tree" (the pack runner's ARTS defaults to an absolute path, and it skips a missing brief) |
| Y18 | Fable, GLM, Grok | equivalents and display-only edges unnamed | **DISCLOSED** in NOT PINNED, each with its reason: `mv -f`; `2>/dev/null` (strip and verdict grep); the cap's and the window's `exit`; the `model:` label's and the identity compare's case; `wc -c` against `wc -m`; the banner narrowed to `OpenAI Codex v`; the closing rule's form; the `.` of `can.t`/`won.t` (the quoting form of an apostrophe); `set -u` sharpened (load-bearing for `m_noinit`'s kill).  The ESC byte is listed as PINNED (every strip row) |
| Y19 | Fable (withdrew DISCLOSE), Astra, Grok, GLM | U7: pin the six 0-on-record alternatives | **PINNED, all four agreeing**, and Fable's BOUNDARY written into the CONTRACT: a synthetic edge is pinned when its constant selects an exit status, a call argument or a caller-read phrase on an input codex can produce through its documented interface; disclosed when the edge needs the harness environment, an encoding the file does not claim, an unreachable flag value, or a display line.  The synthetic list now names every rc row and every Daybreak answer too |
| Y20 | Fable | a FLAKE under heavy load: a run's first redirect fails after `mkdir -p` (the log's `stdout= b`, counts empty) -- two in ~2,570 runs, cause not established; it only ADDS reds | **HANDLED in the driver**: a mutant run carrying the signature is re-run ONCE, alone, and the re-run is scored (`m_mkdirnop`'s MP shows it deterministically) |
| Y21 | Fable | "KILLTABLE_v5.txt kills each" was a precondition: the re-run on af18158e had printed only its base lines | **SUPERSEDED**: that re-run was stopped when v6 changed the files; the record cites `KILLTABLE_v6.txt`, which re-runs all 105 v5 mutants with the 28 new ones |
| Y22 | Fable | the header's "line 5 in 599 of 600" is an older count | **RE-CITED**: the census's 974 of 975 / 1 added beside it |
| Y23 | Astra, Grok | 5a's unconditional "exits 5 when codex's OPENING header block names a different model"; "every decision pinned or disclosed" while escapes stood | **CORRECTED**: the OB bracket says the identity test runs after the refusal, wall and empty-stdout tests, on the run that answered; the pinning sentences are written of v6 |
| Y24 | main loop | the claimed escapes, measured before acting | `v5pass/main_meas.txt`: g_append, g_appenderr, g_effort, g_aupeffort, g_aupcall, g_banner, g_mkdirp, g_mvf, a_mainmodel, a_aupmodel, a_fbrc, a_refusedempty, a_rule1anchor, a_rule2anchor, a_csi1, a_ws0, a_wallmsg, a_stdoutcnt -- 94/94 each, with the sentinel |
| Y25 | Fable | DW, DE, DR (the fallback run walled, empty, or another model): composition receipts that kill nothing new | **NOT ADDED** -- no mutant needs them; the cascade is one code path on the LAST run's counts, and D4 pins that `classify` re-runs |
| Y26 | GLM | U14's caller premise was not checkable from the packet | **SETTLED by grep** (Y11): the readers are `run_pack_body.sh`, `status.sh` and `census_v5.py`; the agy launchers print their own phrases |

## 2b. Premises to CHECK (stated as questions)

* **Each v6 row straddles its edge.**  Does OV/OVA see each override's VALUE at its own call (a hardcoded effort or model at
  EITHER call)?  Does RS/RSF see truncation on BOTH streams?  Do SP1/SP2 and R9A/R9B pin both ends of BOTH rule patterns?
  Does PK's new form make `The answer is LOST` the refusal exit's and nothing else's?
* **The BOUNDARY** (Y19).  Is it sound, and does every NOT PINNED item sit on its correct side of it?
* **U21's filing on `cxlaunchempty`** (Y16) rather than a new row: is that the right home, and is the measured shape right?
* **Anything else in the file** -- after v6, is there a decision of `tools/cxlaunch.sh` whose edge no row straddles and no
  disclosure names?

## 3. The repair, v5 -> v6

### 3a. `tools/cxlaunch.sh` -- WHOLE, as it ships (md5 c53b99abf57f7faf8aadfe2a89294af6)

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
    51	#    * a run whose stderr carries NO opening codex header block, or one with no `model:` line (fixture NM -- GPT-6 Astra,
    52	#      v5 pass), is reported "model UNVERIFIED" and is not failed -- 0 of
    53	#      330 launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
    54	#      CLI format change.  A block whose closing rule never comes is read for 30 lines at most.
    55	#    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
    56	#      pass 2): a quoted line whose only prefix was colour becomes column-0 -- still inside the classify-on-failure gate.
    57	#    * a REFUSED first run's header is printed (`ran:`) but not compared; its answer is discarded, and the fallback's
    58	#      own run is the one compared (GLM 5.3, pass 2).
    59	#    * exit 5 is new to callers: the farm's pack runner special-cases 7 and 8 only, so it RETRIES a 5 rather than
    60	#      recording an answer (Grok 4.7, pass 2) -- a different model having answered is not an answer from this seat.
    61	#      The mechanism (_scratchpad/codexpack_20260928/run_pack_body.sh, read 2026-10-17): it reports a 7, STOPs the pack
    62	#      on an 8, and its done_job counts a job done only when the launch log says `seat answered` or `The answer is
    63	#      LOST` -- so a 5 or a 6 is left not done and the next pack run fires it again.  Those two phrases, and the
    64	#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5); so is
    65	#      `SEAT WALLED`, which status.sh beside the runner counts (GPT-6 Astra, v5 pass -- PK pins it from v6).
    66	#
    67	#  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
    68	#  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
    69	#
    70	#  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
    71	#  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
    72	#  codex's own nonzero rc -- so codex's own rc 7 also exits 7, printing `codex exited 7` and not `The answer is LOST`,
    73	#  and the runner retries it (GPT-6 Astra, v5 pass; controls row R7X).  An answered run whose model is unverified still exits 0, and says so instead of naming
    74	#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v6.sh (RECEIPT_v6.txt; the kill table is
    75	#  KILLTABLE_v6.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
    76	#  redirection, constant and caller-read log phrase of this file, each with the rows that pin its edges or the reason
    77	#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v5.txt are the receipts of the earlier versions.
    78	#
    79	#  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>   -- ABSOLUTE paths.  The brief's size and `mkdir` resolve in the caller's
    80	#  directory, codex's files after `cd "$PROJ"`, and the brief is not checked: a missing or relative brief reaches codex as
    81	#  an EMPTY prompt, and whatever codex does is what is reported.  On 2026-10-17 a relative launch -- the main loop's own --
    82	#  exited 1 because codex refused the empty prompt; a codex that answered it would have been reported `seat answered`
    83	#  (Fable 5.1, v5 pass, measured with the fake).  Every caller in the tree passes absolute paths (the pack runner's ARTS
    84	#  defaults to one, and it skips a missing brief).  Filed on `cxlaunchempty`, the same defect by a second road.
    85	set -u
    86	BRIEF="$1"; OUT="$2"; TAG="$3"
    87	PROJ=/c/DocumentNoSnc/CC/GXEMUL
    88	CODEX="${CX_CODEX_BIN:-$HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex}"
    89	MODEL="${CX_MODEL:-gpt-6-astra}"
    90	EFFORT="${CX_EFFORT:-ultra}"
    91	AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"
    92	AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"
    93	mkdir -p "$OUT"
    94	TXT="$OUT/codex_${TAG}.txt"; ERR="$OUT/codex_${TAG}.err"
    95	ESC=$(printf '\033')
    96	
    97	sz=$(wc -c < "$BRIEF")
    98	echo "brief bytes: $sz"
    99	[ "$sz" -gt 30000 ] && { echo "*** above the argv cap -- use the pointer form"; exit 9; }
   100	
   101	cd "$PROJ" || exit 9
   102	
   103	strip_ansi() { sed "s/${ESC}\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }
   104	
   105	run_codex() {    # $1 model, $2 effort
   106	    "$CODEX" exec --sandbox read-only --skip-git-repo-check -m "$1" \
   107	        -c model_reasoning_effort="$2" "$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null
   108	    rc=$?
   109	    #  codex's OPENING header block -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the
   110	    #  model and effort it actually ran.  Read only that block, and only at the TOP of stderr: the banner and its first
   111	    #  rule must appear by line 12 and the block is read for at most 30 lines.  On record the block's `model:` line is
   112	    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra) -- re-counted at the
   113	    #  landing: the first rule is line 3 in 974 of 975 opening blocks and line 5 in one (CENSUS_v5.txt).  A `model:` line
   114	    #  anywhere else is streamed source or the brief and is never READ -- including a complete QUOTED header block, which
   115	    #  N1's own stderr carries at line 5528 (GPT-6 Astra, adjudication pass: v2 matched the banner anywhere).
   116	    HDR=$(strip_ansi "$ERR" | awk 'NR > 12 && h < 2 { exit }
   117	        h == 0 && /^OpenAI Codex/ { h = 1; next }
   118	        h == 1 && /^--------/ { h = 2; next }
   119	        h == 2 && /^--------/ { exit }
   120	        h == 2 { if (++n > 30) exit; print }')
   121	    RAN=$(printf '%s\n' "$HDR" | grep -m1 '^model:' | sed 's/^model:[[:space:]]*//; s/[[:space:]]*$//')
   122	    echo "codex rc=$rc   stdout=$(wc -c < "$TXT") b   stderr=$(wc -c < "$ERR") b   asked: $1 / $2"
   123	    echo "  ran: ${RAN:+model: $RAN} / $(printf '%s\n' "$HDR" | grep -m1 '^reasoning effort:')"
   124	}
   125	
   126	#  CONTENT CHECK.  Verify by content, never by size -- and NOT by grepping stderr for codex's diagnostics alone.
   127	#
   128	#  *** MEASURED 2026-09-07, on the run that installed this file: codex STREAMS THE SOURCE IT READS into stderr, so a
   129	#  bare grep over stderr matches any file containing the words -- hence the `^ERROR:` anchor. ***
   130	#
   131	#  *** AND THE ANCHOR IS NOT ENOUGH.  MEASURED 2026-09-26: THREE REAL ANSWERS WERE REPORTED "SEAT WALLED" -- astra549
   132	#  (rc 0, 11,472 b), astra550 (rc 0, 4,265 b), rec529audit (rc 0, 13,442 b) -- because each read an old panel file
   133	#  whose lines BEGIN with a codex wall message ("ERROR: You've hit your usage limit ... 7:01 AM"), and codex streamed
   134	#  those lines into stderr at column 0.  A quoted marker re-arms the tool that reads it (the carrier's own rule). ***
   135	#
   136	#  So the discriminator is the EXIT STATUS and the ANSWER, which quoted text cannot forge.  stderr's `ERROR:` lines are
   137	#  classified ONLY WHEN rc != 0 OR stdout IS EMPTY; rc 0 with a non-empty stdout is an ANSWER, whatever stderr quotes.
   138	#  Every real wall and refusal on record is rc 1 with an EMPTY stdout, and every rc-0 run carries an answer: 362 + 25
   139	#  of 387 launch lines, nothing off that diagonal (launchlog_census.txt) -- the residuals above are the off-diagonal.
   140	classify() {
   141	    #  `grep -a`: a stderr carrying a NUL byte is "binary" to grep, which then prints `Binary file (standard input)
   142	    #  matches` instead of the lines.  A real wall was recorded exit 6 "seat down" that way:
   143	    #  _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err (rc 1, empty stdout, 1,449 NULs from byte 2,318,517;
   144	    #  its two column-0 `ERROR: You've hit your usage limit` lines come after them) -- Grok 4.7, pass 2, re-run here.
   145	    CXERR=$(strip_ansi "$ERR" | grep -a '^ERROR:')
   146	    verd=$(grep -ic 'VERDICT' "$TXT" 2>/dev/null)
   147	    body=$(wc -c < "$TXT")
   148	    refus=0; wall=0
   149	    if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then
   150	        refus=$(printf '%s' "$CXERR" | grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help')
   151	        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')
   152	    else
   153	        q=$(printf '%s' "$CXERR" | grep -c .)
   154	        [ "$q" -gt 0 ] && echo "  note: $q ERROR:-shaped line(s) in stderr IGNORED -- rc 0 with an answer, so they are quoted source"
   155	    fi
   156	    echo "  verdict-in-stdout: $verd   refusal: $refus   wall: $wall   (classified only when rc != 0 or stdout is empty)"
   157	}
   158	
   159	run_codex "$MODEL" "$EFFORT"; classify
   160	ANSWERED_BY="$MODEL"
   161	
   162	if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then
   163	    echo "  *** SEAT REFUSED on $MODEL (content filter):"
   164	    printf '%s\n' "$CXERR" | grep -m1 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
   165	    mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"
   166	    echo "  *** AUP FALLBACK: re-running ONCE on $AUP_MODEL / $AUP_EFFORT (the refused run is kept as codex_${TAG}.refused.*)"
   167	    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify
   168	    ANSWERED_BY="$AUP_MODEL"
   169	fi
   170	
   171	if [ "$refus" -gt 0 ]; then
   172	    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."
   173	    printf '%s\n' "$CXERR" | grep -m2 -i 'flagged for possible cybersecurity' | cut -c1-160 | sed 's/^/    /'
   174	    echo "  *** REPHRASE (neutral test-coverage wording) or ROUTE THIS BRIEF TO GROK."
   175	    exit 7
   176	fi
   177	if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED ($ANSWERED_BY)."; exit 8; fi
   178	if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT with no refusal/wall text -- seat down, cause NOT established."; exit 6; fi
   179	if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then
   180	    echo "  *** A DIFFERENT MODEL RAN: asked $ANSWERED_BY, codex's header says $RAN -- a SEAT FAILURE; the answer is not $ANSWERED_BY's."
   181	    exit 5
   182	fi
   183	if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
   184	if [ -z "$RAN" ]; then
   185	    echo "  seat answered -- model UNVERIFIED: no model line in an opening codex header block (requested: $ANSWERED_BY)"
   186	else
   187	    echo "  seat answered. (answered by: $ANSWERED_BY)"
   188	fi
```

### 3a'. its v5 -> v6 diff (27 changed lines; ONE executable, the UNVERIFIED message)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v5.sh	2026-10-17 05:09:06.309442600 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh	2026-10-17 05:09:06.501230800 -0500
@@ -48,7 +48,8 @@
 #      `ERROR:` line does not fix it: in N4 that line is itself a quotation.
 #    * its refusal twin: a quoted `flagged for possible cybersecurity` line on rc != 0 -> the Daybreak re-run fires
 #      and the first answer is renamed codex_<tag>.refused.* (Grok 4.7).
-#    * a run whose stderr carries NO opening codex header block is reported "model UNVERIFIED" and is not failed -- 0 of
+#    * a run whose stderr carries NO opening codex header block, or one with no `model:` line (fixture NM -- GPT-6 Astra,
+#      v5 pass), is reported "model UNVERIFIED" and is not failed -- 0 of
 #      330 launcher-captured answered runs on record lack it (counted on pass 2); failing it would lose every answer to a
 #      CLI format change.  A block whose closing rule never comes is read for 30 lines at most.
 #    * the ANSI strip widens both residuals above to colour-prefixed quoted lines on a failed or empty run (GLM 5.3,
@@ -60,22 +61,27 @@
 #      The mechanism (_scratchpad/codexpack_20260928/run_pack_body.sh, read 2026-10-17): it reports a 7, STOPs the pack
 #      on an 8, and its done_job counts a job done only when the launch log says `seat answered` or `The answer is
 #      LOST` -- so a 5 or a 6 is left not done and the next pack run fires it again.  Those two phrases, and the
-#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5).
+#      `answered by: <model>` the runner records, are therefore part of this file's contract (controls row PK, v5); so is
+#      `SEAT WALLED`, which status.sh beside the runner counts (GPT-6 Astra, v5 pass -- PK pins it from v6).
 #
 #  Overrides, each only so the branches are testable without the network: CX_MODEL, CX_EFFORT, CX_AUP_MODEL (set it
 #  EMPTY to disable the fallback), CX_AUP_EFFORT, CX_CODEX_BIN.
 #
 #  Exit status: 0 answered; 5 a different model ran; 6 empty stdout with no refusal or wall text; 7 refused (after
 #  the fallback, if any); 8 walled; 9 the brief is above the argv cap or the project dir is missing; otherwise
-#  codex's own nonzero rc.  An answered run whose model is unverified still exits 0, and says so instead of naming
-#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh (RECEIPT_v5.txt; the kill table is
-#  KILLTABLE_v5.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
+#  codex's own nonzero rc -- so codex's own rc 7 also exits 7, printing `codex exited 7` and not `The answer is LOST`,
+#  and the runner retries it (GPT-6 Astra, v5 pass; controls row R7X).  An answered run whose model is unverified still exits 0, and says so instead of naming
+#  a model.  Controls: regress/artifacts/cxlaunchland_20261016/run_controls_v6.sh (RECEIPT_v6.txt; the kill table is
+#  KILLTABLE_v6.txt).  Its header is the CONTRACT: the decisions found by reading every predicate, pattern alternative,
 #  redirection, constant and caller-read log phrase of this file, each with the rows that pin its edges or the reason
-#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v4.txt are the receipts of the earlier versions.
+#  it is not pinned.  RECEIPT.txt and RECEIPT_v2.txt to RECEIPT_v5.txt are the receipts of the earlier versions.
 #
 #  Usage: cxlaunch.sh <brief-path> <out-dir> <tag>   -- ABSOLUTE paths.  The brief's size and `mkdir` resolve in the caller's
-#  directory, codex's files after `cd "$PROJ"`, so a relative path breaks: measured 2026-10-17, a relative pointer read 787
-#  bytes, then codex got no brief and the run exited 1, NOT a clean run.  Every caller on record passes absolute paths.
+#  directory, codex's files after `cd "$PROJ"`, and the brief is not checked: a missing or relative brief reaches codex as
+#  an EMPTY prompt, and whatever codex does is what is reported.  On 2026-10-17 a relative launch -- the main loop's own --
+#  exited 1 because codex refused the empty prompt; a codex that answered it would have been reported `seat answered`
+#  (Fable 5.1, v5 pass, measured with the fake).  Every caller in the tree passes absolute paths (the pack runner's ARTS
+#  defaults to one, and it skips a missing brief).  Filed on `cxlaunchempty`, the same defect by a second road.
 set -u
 BRIEF="$1"; OUT="$2"; TAG="$3"
 PROJ=/c/DocumentNoSnc/CC/GXEMUL
@@ -103,7 +109,8 @@
     #  codex's OPENING header block -- `OpenAI Codex vX`, then the lines between the next two `--------` rules -- names the
     #  model and effort it actually ran.  Read only that block, and only at the TOP of stderr: the banner and its first
     #  rule must appear by line 12 and the block is read for at most 30 lines.  On record the block's `model:` line is
-    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra).  A `model:` line
+    #  line 5 of stderr in 599 of 600 codex .err files and line 7 in one (two pre-header lines; Astra) -- re-counted at the
+    #  landing: the first rule is line 3 in 974 of 975 opening blocks and line 5 in one (CENSUS_v5.txt).  A `model:` line
     #  anywhere else is streamed source or the brief and is never READ -- including a complete QUOTED header block, which
     #  N1's own stderr carries at line 5528 (GPT-6 Astra, adjudication pass: v2 matched the banner anywhere).
     HDR=$(strip_ansi "$ERR" | awk 'NR > 12 && h < 2 { exit }
@@ -175,7 +182,7 @@
 fi
 if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc -- NOT a clean run."; exit "$rc"; fi
 if [ -z "$RAN" ]; then
-    echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"
+    echo "  seat answered -- model UNVERIFIED: no model line in an opening codex header block (requested: $ANSWERED_BY)"
 else
     echo "  seat answered. (answered by: $ANSWERED_BY)"
 fi
```

### 3b. the controls, `run_controls_v6.sh`, WHOLE (the CONTRACT is its header)

```bash
     1	#!/bin/bash
     2	#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
     3	#  F1), v6 after the four-seat pass 2, the adjudication pass and the v3, v4 and v5 passes.  Every row runs a launcher against a FAKE
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
    26	#  v6 -- the v5 pass measured one-edit mutants passing all 224 v5 controls at decisions the v5 CONTRACT listed as pinned, one
    27	#  shape again: a row pinned the DEFAULT of a value and not the value itself, or a fresh state and not a used one.  Each
    28	#  override honoured only as empty or default (CX_EFFORT=ultra, the fallback's effort and model, the main call's model --
    29	#  GLM 5.3, GPT-6 Astra, Fable 5.1); `>' and `2>' never met a used out dir (`>>' passes -- all four seats); `mkdir -p' never
    30	#  met a missing parent; the refused run's stdout was always empty; the fallback's own rc never nonzero with an answer; the
    31	#  rule patterns' anchors, a parameterless CSI, `model:' with no space, the banner text's `Codex', a nine-dash rule; and the
    32	#  `codex rc=' line's numbers, never compared.  The CONTRACT also said no caller reads the wall wording (status.sh does),
    33	#  `The answer is LOST' iff exit 7 (codex's own rc 7 exits 7 without it), and that nine dashes are not a rule (they are --
    34	#  the pattern has no end anchor; Grok 4.7), and that a relative brief makes the LAUNCHER exit 1 (it does not: an empty
    35	#  prompt reaches codex, and codex decided -- Fable 5.1, measured).  Each is now a row, a check or a corrected sentence.
    36	#
    37	#  THE CONTRACT -- each decision of the landed launcher (by construct), the rows that pin its edges, and what is not pinned:
    38	#  configuration
    39	#    CX_CODEX_BIN honoured, its `:-'      E0b (no after run but DP's and EO's reaches the default-path fake); EO (set EMPTY)
    40	#    the default codex path               DP (CX_CODEX_BIN unset: the run reaches $HOME/AppData/Local/Programs/.../codex)
    41	#    CX_MODEL, CX_EFFORT, CX_AUP_EFFORT, their `:-' and defaults
    42	#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default); OVA (each
    43	#                                         set to a NON-default value: each reaches its own call, both compared whole)
    44	#    CX_AUP_MODEL, its default and `-' (EMPTY disables the fallback)
    45	#                                         E2; FD (every row that sets it empty makes exactly one call); OVA (a non-default
    46	#                                         fallback model is the second call's)
    47	#    the output names and the stdout/stderr redirections
    48	#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written); RSF
    49	#                                         (a re-run into a dir holding a stale answer and a stale header: both TRUNCATED)
    50	#    `mkdir -p "$OUT"'                    MPF (an out dir two levels below a missing parent is created)
    51	#    `< /dev/null' on codex's stdin       SI (no after run's codex reads the marker the launcher is fed)
    52	#    `cd "$PROJ"'                         CWD (every after run's codex starts in the project root)
    53	#    the argv cap `sz -gt 30000', exit 9  X14 (30,000 accepted) / X15 (30,001: exit 9, codex never called)
    54	#  the call
    55	#    the argument sequence                E1 (one call), E2 and EO (Astra, then Daybreak), DP -- each compared whole
    56	#  the opening header
    57	#    ANSI strip on the header             CH (the real coloured header of fx/R2.stderr, asked as gpt-6-other -> 5)
    58	#    the window `NR > 12 && h < 2'        W12 / W13 (first rule at line 12 read, at 13 not); X13 (the real banner-at-4 header);
    59	#                                         X9, X10 (no opening block, a quoted one at line 21)
    60	#    the banner: `h == 0 &&', `/^OpenAI Codex/'
    61	#                                         HB (a banner-shaped line inside the block does not restart it); BA (a banner with a
    62	#                                         prefix, above the real one, is not a banner); BN (`OpenAI notice:', a near-miss
    63	#                                         above the real banner, is not one: the text's `Codex'); every header row
    64	#    the first rule: `h == 1 &&', 8 dashes, `next'
    65	#                                         BA (a rule before any banner is not the first rule); R7A (seven dashes are not a
    66	#                                         rule); R9A (nine dashes ARE one -- the pattern has no end anchor; the v5 gloss
    67	#                                         "nine find no block anywhere" was false, Grok 4.7); SP1 (a separator not at column
    68	#                                         0, before the first rule, is not one: the `^'); every header row (`next')
    69	#    the closing rule: `h == 2 &&', 8 dashes, `exit'
    70	#                                         BA (a rule before any banner closes nothing); R7B (seven dashes do not close the
    71	#                                         block); R9B (nine dashes DO close it: a model after them is not read); SP2 (a
    72	#                                         separator not at column 0, inside the body, does not close it: the `^'); NM (no
    73	#                                         model line in the block: a model line after the close is not read)
    74	#    the body: `h == 2', the cap `++n > 30'
    75	#                                         R7A (the lines between banner and first rule are not body); K30 / K31 (a model at
    76	#                                         body line 30 read, at 31 not)
    77	#    the first `model:' line, anchored    TM (two model lines: the first is read); MA (`fallback model:' is not a model line);
    78	#                                         M1, X5
    79	#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies); WZ (`model:gpt-6-astra',
    80	#                                         NO whitespace, verifies: the trims' `*', zero or more)
    81	#  classification
    82	#    the gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4; RC2W (rc 2 with an answer IS classified); B1G (a 1-byte rc-0
    83	#                                         answer is NOT)
    84	#    `^ERROR:', `grep -a'                 X1; X8
    85	#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR);
    86	#                                         CZ (`ESC[m', a CSI with NO parameter: the class's `*')
    87	#    the ESC byte, `printf '\033''        A1, CH, CSI, CZ, Q3, R2X -- each needs the strip, and a wrong ESC strips nothing
    88	#    the refusal alternatives, `-i'       P2, Q1, A1 (`flagged for possible cybersecurity'); RF1 (`cannot help with');
    89	#                                         RF2 (`can't help with'); RF3 (`I won't help'); RFC (the first, upper case)
    90	#    the wall alternatives, `-i'          P1, Q2, Q3, X8 (`usage limit'); WL1 (`quota'); WL2 (`rate limit');
    91	#                                         WL3 (`not authenticated'); WLC (the first, upper case)
    92	#    refusal count `refus -gt 0', at BOTH guards
    93	#                                         P2, Q1, A1, D1 (count 1); R2X (2, the final guard); D3 (2, the fallback)
    94	#    wall count `wall -gt 0'              W1L (count 1); P1, Q2, Q3, X8 (2); N4 (6)
    95	#  the fallback
    96	#    trigger `refus -gt 0 && -n AUP_MODEL && AUP_MODEL != MODEL'
    97	#                                         D1, D2, D3 fire; FB1, FB2 do not (an answer, a wall; the fallback on); FD (empty:
    98	#                                         never); D5 (asked ON Daybreak and refused: no second run)
    99	#    once                                 D4 (refused, then refused on Daybreak: exactly two calls)
   100	#    the refused run's files kept         D1R (codex_D1.refused.txt and .refused.err byte-for-byte the first run's; codex_D1.txt
   101	#                                         and .err the Daybreak run's); RNF (a NON-EMPTY refused stdout, byte-for-byte)
   102	#    the answer credited to the fallback  D1, D3 (Daybreak credited); D2 (Daybreak compared -> 5)
   103	#  the exit cascade: refused 7, walled 8, empty 6, a different model 5, codex's own rc
   104	#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1); FR (3:
   105	#                                         the FALLBACK run's raw rc, with an answer); R7X (codex's own rc 7 with an answer)
   106	#    the order, each adjacent pair        RW (refusal + wall -> 7); P2 (refusal + empty + rc 1 -> 7); RI (refusal + another
   107	#                                         model's header -> 7); P1 (wall + empty -> 8); WI (wall + another header -> 8);
   108	#                                         EM (empty + another header -> 6); X1 (empty + rc 1 -> 6); IR (rc 1, an answer,
   109	#                                         another header -> 5)
   110	#    the empty test `body -eq 0'          N3, X1 (0 bytes -> 6); B1E (1 byte -> 0)
   111	#    identity `-n RAN && RAN != ANSWERED_BY'
   112	#                                         M1, D2, X5, W12, K30, X13, CH, IR, BA -> 5; M2, X6, X9, W13, K31, NM, HB -> UNVERIFIED, 0
   113	#  the log phrases a caller reads -- _scratchpad/codexpack_20260928/run_pack_body.sh (done_job and reap) AND status.sh beside
   114	#  it, which counts `SEAT WALLED' (GPT-6 Astra, v5 pass: the v5 CONTRACT said no caller read the wall wording); derived by
   115	#  `grep -rlE "SEAT WALLED|The answer is LOST|seat answered|answered by: "' over _scratchpad and GXEMUL-SEC/tools, the
   116	#  launcher copies and the agy pack excluded -- the two pack scripts above and census_v5.py are the readers
   117	#    `seat answered' iff exit 0; `The answer is LOST' iff the REFUSAL exit (codex's own rc 7 also exits 7 and prints `codex
   118	#    exited 7' instead, so the runner retries it -- R7X); `SEAT WALLED' iff exit 8; `answered by: <model>' iff an exit 0
   119	#    whose model verified
   120	#                                         PK (every after run); R7XL; N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB,
   121	#                                         R9B (none)
   122	#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, which the launch-log censuses this file cites parse --
   123	#    its FORMAT and its NUMBERS (the fixture's own rc and byte counts; v5 read the format only, GPT-6 Astra)
   124	#                                         LOG (N1, both of D1's calls, RC3A: each line compared whole)
   125	#  NOT PINNED, each with its reason:
   126	#    `|| exit 9' after `cd'               needs a missing project dir -- untestable without editing the file
   127	#    `set -u'                             reached only by a missing positional argument (a usage error, exit 1); every caller
   128	#                                         passes three, and a row without them would write outside the scratch dir under a
   129	#                                         mutant that drops it.  Load-bearing for one kill: under it `m_noinit''s unbound
   130	#                                         `$refus' errors every rc-0 row (Fable 5.1, v5 pass)
   131	#    the banner rule's `next'             equivalent: the banner line matches no later rule
   132	#    the body cap's and the window guard's `exit' (not `next')
   133	#                                         equivalent: past the cap every later line also fails `++n > 30' and is not
   134	#                                         printed, and past line 12 with no block every later line is skipped either way
   135	#    `mv -f' (both moves)                 equivalent off a terminal: mv prompts only with a terminal on stdin AND an
   136	#                                         unwritable destination; no caller runs the launcher on a terminal
   137	#    `2>/dev/null' on strip_ansi and on the verdict grep
   138	#                                         display only: each reads a file that exists whenever it runs ($ERR after codex
   139	#                                         wrote it; $TXT), and the suppressed text changes no decision
   140	#    RELATIVE or MISSING paths            the brief's size and `mkdir' resolve in the caller's directory, codex's files after
   141	#                                         `cd "$PROJ"', and the brief is not checked: a missing or relative brief reaches codex
   142	#                                         as an EMPTY prompt, and what codex does is what is reported -- on 2026-10-17 codex
   143	#                                         refused it and exited 1, while a fake that answers it is reported `seat answered',
   144	#                                         exit 0 (Fable 5.1, v5 pass, measured; the v5 text called the exit 1 the launcher's).
   145	#                                         It is `cxlaunchempty''s defect -- an empty prompt reaches codex -- by a second road,
   146	#                                         and is FILED on that row with the relative OUT dir.  Every caller in the tree passes
   147	#                                         absolute paths (the pack runner's ARTS defaults to one, and it skips a missing
   148	#                                         brief); so does every row here
   149	#    the `model:' label's case, and the identity compare's case
   150	#                                         equivalent on record: codex's header is lower-case by its format (all 975 opening
   151	#                                         blocks match `^model:'), and a case-folded compare is a policy change, not a drift
   152	#    `wc -c' (bytes) for the argv cap     equivalent here: under the C locale the harness and the farm run in `wc -m' counts
   153	#                                         bytes too, and every brief on record is ASCII
   154	#    the banner past `OpenAI Codex' (narrowed to `OpenAI Codex v')
   155	#                                         equivalent on record: every banner is `OpenAI Codex v...' (BN pins the widening)
   156	#    the closing rule's `exit' against another way to end the block (`h = 3; next')
   157	#                                         equivalent by construction: nothing matches past the close either way; the edge
   158	#                                         that matters, `exit' against `next', is NM's
   159	#    the `.' of `can.t' and `won.t'       the quoting form of an apostrophe inside a single-quoted pattern, not a decision:
   160	#                                         an ASCII `'' cannot be written there, and 0 column-0 ERROR lines on record carry a
   161	#                                         curly apostrophe or any non-ASCII byte (Fable 5.1, v5 pass)
   162	#    display only -- printed, read by no decision and no caller: `brief bytes'; the `ran:' line (the header's effort is
   163	#                                         printed, never compared); `verdict-in-stdout' (verd exists for that line alone); the
   164	#                                         IGNORED note; the refusal excerpts (`-m1'/`-m2', `cut -c1-160'); the REPHRASE line;
   165	#                                         the wording of the 5, 6, 8 and rc messages beyond the phrases above (the 8's `SEAT
   166	#                                         WALLED' and the rc message's `codex exited N' ARE pinned, by PK and R7XL)
   167	#  SYNTHETIC SHAPES, and THE BOUNDARY of what is pinned without an instance on record (Fable 5.1, v5 pass, with GLM 5.3's and
   168	#  Grok 4.7's criterion; pass 2's "0 on record, so disclose" is superseded): a synthetic edge is PINNED when its constant
   169	#  selects an exit status, a call argument or a log phrase a caller reads, on an input codex can produce through its
   170	#  documented interface -- a diagnostic line, a header line, an escape sequence, a status, an answer; it is DISCLOSED as
   171	#  equivalent when the edge is reachable only through the harness environment (a locale), an input encoding the file does
   172	#  not claim, a flag whose other value is unreachable here, or a display line (the NOT PINNED list).  Pinned under it, each
   173	#  with 0 instances on record (CENSUS_v5.txt names each count): RF1-RF3, RFC, WL1-WL3, WLC, RW, RI, WI, EM, IR, BA, BN, HB,
   174	#  R7A, R7B, R9A, R9B, SP1, SP2, NM, TM, MA, WS, WZ, K30, K31, W12/W13, CZ, R7X, RC1A, RC3A, RC2W, B1G, B1E, D5, FR, RN, RS, MP,
   175	#  OV and the fallback rows' Daybreak answers -- every rc row and every Daybreak answer sits off CENSUS_v5's diagonal (0
   176	#  launch lines off rc 0 with stdout / rc 1 empty) -- and CSI, in BOTH halves.  The v5 CONTRACT called its `;'-joined half load-bearing because 44 of the codex .err files carry
   177	#  one; 42 of the 44 are the #544 control stub's own output and the other 2 quote a coloured GXemul prompt mid-line, never a
   178	#  codex diagnostic (v5pass/SEMISGR_WHERE.txt; GPT-6 Astra, v5 pass).  Every line opening with eight dashes in the first 42
   179	#  lines of the 2,427 codex .err files is exactly eight dashes (1,954 lines, v5pass/RULELEN_CENSUS.txt), so R9A/R9B pin the
   180	#  pattern's own edge, not a shape seen.
   181	#
   182	#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
   183	#  Usage: bash run_controls_v6.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
   184	#  the mutant table uses; writes only to a scratch dir it removes)
   185	set -u
   186	HERE=$(cd "$(dirname "$0")" && pwd)
   187	REPO=$(cd "$HERE/../../.." && pwd)
   188	TRACKED="$HERE/cxlaunch_tracked.sh"
   189	BEFORE="$HERE/cxlaunch_before.sh"
   190	AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
   191	ONLY="${CXL_AFTER_ONLY:-}"
   192	N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
   193	QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
   194	NROWS=78
   195	NFD=66
   196	for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
   197	         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout" "$HERE/fx/R2.stderr"; do
   198	    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
   199	done
   200	T=$(mktemp -d)
   201	trap 'rm -rf "$T"' EXIT
   202	ESC=$(printf '\033')
   203	
   204	mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr from stdin)
   205	    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
   206	    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
   207	    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
   208	}
   209	printf 'A complete review answer.\nVERDICT: SHIP\n' > "$T/ans_verdict.txt"
   210	#  NOT the word "verdict" in any case: the launcher counts it case-insensitively, and a first draft of this fixture said
   211	#  "no verdict line" -- so it HAD one, and the kill table measured X2 blind to the mutant it exists for.
   212	printf 'A complete review answer that ends without its summary line.\n' > "$T/ans_noverdict.txt"
   213	printf 'x' > "$T/ans_1byte.txt"
   214	hdr() {    # $1 the model -- a minimal closed opening header block
   215	    printf 'OpenAI Codex v0.153.4\n--------\nmodel: %s\nreasoning effort: ultra\n--------\n' "$1"
   216	}
   217	hdr gpt-6-astra > "$T/hdr_astra.txt"
   218	hdr gpt-6-other > "$T/hdr_other.txt"
   219	grep -m1 '^ERROR:' "$HERE/fx/P2.stderr" > "$T/refusal_line.txt"
   220	grep -m1 '^ERROR:' "$HERE/fx/P1.stderr" > "$T/wall_line.txt"
   221	[ -s "$T/refusal_line.txt" ] && [ -s "$T/wall_line.txt" ] || { echo "APPARATUS FAIL: no column-0 ERROR line in P1 or P2"; exit 9; }
   222	mkfx P1 1 "" "$HERE/fx/P1.stderr"
   223	mkfx P2 1 "" "$HERE/fx/P2.stderr"
   224	mkfx N1 0 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
   225	mkfx N2 0 "$HERE/fx/N2.stdout" ""
   226	mkfx N3 0 "" ""
   227	mkfx N4 1 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
   228	mkfx Q1 1 "" "$QD/Q1.stderr"
   229	mkfx Q2 0 "" "$QD/Q2.stderr"
   230	mkfx Q3 1 "" "$QD/Q3.stderr"
   231	sed "s/^ERROR:/${ESC}[1m${ESC}[31mERROR:${ESC}[0m${ESC}[0m/" "$HERE/fx/P2.stderr" | mkfx A1 1 "" -
   232	hdr gpt-daybreak-blue-latest | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
   233	mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" "$T/hdr_astra.txt"
   234	sed 's/^/regress\/artifacts\/old_panel\/codex.txt:17:/' "$HERE/fx/P2.stderr" | mkfx X1 1 "" -
   235	mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
   236	printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
   237	{ printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -
   238	#  X9/X10: twenty lines of streamed text, then a complete codex header block QUOTED from a file the review read (the shape
   239	#  N1's stderr carries from line 5528) -- and no opening header at all
   240	latehdr() {    # $1 the quoted block's model
   241	    i=1; while [ $i -le 20 ]; do printf 'streamed line %d of a file the review read\n' $i; i=$((i + 1)); done
   242	    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$1"
   243	    printf 'reasoning effort: ultra\n--------\nuser\nthe quoted session brief\n'
   244	}
   245	latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
   246	latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -
   247	#  v4 (the v3 pass): the window's and the cap's EDGES, the real warning-prefixed header, a real doubled refusal, one wall line
   248	hdrat() {    # $1 lines before the banner, $2 the block's model -- a CLOSED opening block whose banner is line $1+1
   249	    i=1; while [ $i -le "$1" ]; do printf 'startup line %d\n' $i; i=$((i + 1)); done
   250	    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$2"
   251	    printf 'reasoning effort: ultra\n--------\nuser\nthe session brief\n'
   252	}
   253	hdrat 10 gpt-6-other | mkfx W12 0 "$T/ans_verdict.txt" -      # banner line 11, first rule line 12: inside the window
   254	hdrat 11 gpt-6-other | mkfx W13 0 "$T/ans_verdict.txt" -      # banner line 12, first rule line 13: outside it
   255	head -14 "$REPO/regress/artifacts/ppcrldimimask/codex_book1check_20260910.err" | mkfx X13 0 "$T/ans_verdict.txt" -
   256	capat() {    # $1 body lines before the block's `model:' line -- an UNTERMINATED opening block
   257	    printf 'OpenAI Codex v0.153.4\n--------\n'
   258	    i=1; while [ $i -le "$1" ]; do printf 'body line %d\n' $i; i=$((i + 1)); done
   259	    printf 'model: gpt-6-other\nreasoning effort: ultra\n'
   260	    i=1; while [ $i -le 20 ]; do printf 'streamed line %d\n' $i; i=$((i + 1)); done
   261	}
   262	capat 29 | mkfx K30 0 "$T/ans_verdict.txt" -                  # the model is body line 30: read
   263	capat 30 | mkfx K31 0 "$T/ans_verdict.txt" -                  # the model is body line 31: not read
   264	mkfx R2 1 "" "$HERE/fx/R2.stderr"
   265	mkfx W1L 1 "" "$T/wall_line.txt"
   266	mkfx ANS 0 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   267	#  v5 (the v4 pass): the rc pass-through, the gate's and the empty test's 1-byte edge, the real coloured header, each pattern
   268	#  alternative and the case fold, a non-SGR strip, each adjacent pair of the exit cascade, and every awk guard and constant
   269	mkfx RC1A 1 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   270	mkfx RC3A 3 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   271	mkfx RC2W 2 "$T/ans_verdict.txt" "$HERE/fx/P1.stderr"
   272	mkfx B1G 0 "$T/ans_1byte.txt" "$HERE/fx/P1.stderr"
   273	mkfx B1E 0 "$T/ans_1byte.txt" "$T/hdr_astra.txt"
   274	head -12 "$HERE/fx/R2.stderr" | mkfx CH 0 "$T/ans_verdict.txt" -      # its opening block only: `ESC[1mmodel:ESC[0m gpt-6-astra'
   275	printf 'ERROR: I cannot help with that request.\n' | mkfx RF1 1 "" -
   276	printf "ERROR: I can't help with that request.\n" | mkfx RF2 1 "" -
   277	printf "ERROR: I won't help with that request.\n" | mkfx RF3 1 "" -
   278	printf 'ERROR: THIS CONTENT WAS FLAGGED FOR POSSIBLE CYBERSECURITY RISK.\n' | mkfx RFC 1 "" -
   279	printf 'ERROR: quota exceeded for this workspace.\n' | mkfx WL1 1 "" -
   280	printf 'ERROR: rate limit reached; retry in 60s.\n' | mkfx WL2 1 "" -
   281	printf 'ERROR: not authenticated -- run codex login.\n' | mkfx WL3 1 "" -
   282	printf "ERROR: You've hit your USAGE LIMIT.\n" | mkfx WLC 1 "" -
   283	printf '%s\n' "${ESC}[2K${ESC}[1;31mERROR:${ESC}[0m This content was flagged for possible cybersecurity risk." | mkfx CSI 1 "" -
   284	cat "$T/refusal_line.txt" "$T/wall_line.txt" | mkfx RW 1 "" -
   285	cat "$T/hdr_other.txt" "$T/refusal_line.txt" | mkfx RI 1 "" -
   286	cat "$T/hdr_other.txt" "$T/wall_line.txt" | mkfx WI 1 "" -
   287	mkfx EM 0 "" "$T/hdr_other.txt"
   288	mkfx IR 1 "$T/ans_verdict.txt" "$T/hdr_other.txt"
   289	printf 'OpenAI Codex v0.153.4\n--------\nmodel:\t  gpt-6-astra \r\nreasoning effort: ultra\n--------\n' | mkfx WS 0 "$T/ans_verdict.txt" -
   290	printf 'OpenAI Codex v0.153.4\n--------\nfallback model: gpt-6-other\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   291	    | mkfx MA 0 "$T/ans_verdict.txt" -
   292	printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
   293	    | mkfx TM 0 "$T/ans_verdict.txt" -
   294	printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nreasoning effort: ultra\n--------\nuser\nmodel: gpt-6-other\n' \
   295	    | mkfx NM 0 "$T/ans_verdict.txt" -
   296	printf '> OpenAI Codex v0.1 (a quoted transcript)\n--------\nmodel: gpt-6-other\n--------\n' > "$T/ba_pre.txt"
   297	cat "$T/ba_pre.txt" "$T/hdr_astra.txt" | mkfx BA 0 "$T/ans_verdict.txt" -
   298	printf 'OpenAI Codex v0.153.4\n--------\nOpenAI Codex v0.1 (quoted)\n--------\nmodel: gpt-6-other\n--------\n' \
   299	    | mkfx HB 0 "$T/ans_verdict.txt" -
   300	printf 'OpenAI Codex v0.153.4\n-------\nmodel: gpt-6-other\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   301	    | mkfx R7A 0 "$T/ans_verdict.txt" -
   302	printf 'OpenAI Codex v0.153.4\n--------\n-------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
   303	    | mkfx R7B 0 "$T/ans_verdict.txt" -
   304	#  v6 (the v5 pass): each override's VALUE honoured at its own call, the fallback's own rc, a re-run into a used dir, a missing
   305	#  parent, a non-empty refused stdout, separators off column 0, a parameterless CSI, `model:' with no space, codex's own rc 7, a
   306	#  near-miss banner, nine-dash rules
   307	hdr m-fallback | mkfx OV2 0 "$T/ans_verdict.txt" -
   308	hdr gpt-daybreak-blue-latest | mkfx FR3 3 "$T/ans_verdict.txt" -
   309	printf 'STALE ANSWER from an earlier run of this tag\n' > "$T/seed_stdout"
   310	hdr gpt-6-stale > "$T/seed_stderr"
   311	printf 'A partial answer the content filter cut off.\n' > "$T/ans_partial.txt"
   312	mkfx RN1 1 "$T/ans_partial.txt" "$HERE/fx/P2.stderr"
   313	printf 'OpenAI Codex v0.153.4\nx --------\n--------\nworkdir: x\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
   314	    | mkfx SP1 0 "$T/ans_verdict.txt" -
   315	printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nnote: a -------- b\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
   316	    | mkfx SP2 0 "$T/ans_verdict.txt" -
   317	printf '%s\n' "${ESC}[mERROR: This content was flagged for possible cybersecurity risk." | mkfx CZ 1 "" -
   318	printf 'OpenAI Codex v0.153.4\n--------\nmodel:gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx WZ 0 "$T/ans_verdict.txt" -
   319	mkfx R7X 7 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
   320	{ printf 'OpenAI notice: a deprecation warning\n--------\nmodel: gpt-6-other\n--------\n'; cat "$T/hdr_astra.txt"; } \
   321	    | mkfx BN 0 "$T/ans_verdict.txt" -
   322	printf 'OpenAI Codex v0.153.4\n---------\nmodel: gpt-6-other\nreasoning effort: ultra\n---------\n' | mkfx R9A 0 "$T/ans_verdict.txt" -
   323	printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\n---------\nmodel: gpt-6-other\n' | mkfx R9B 0 "$T/ans_verdict.txt" -
   324	
   325	#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL); logs its arguments to $FX_ARGS, its working
   326	#  directory to $FX_ARGS.cwd and the first 60 bytes of its stdin to $FX_ARGS.stdin
   327	cat > "$T/fakecodex.sh" <<'EOF'
   328	#!/bin/bash
   329	D="$FX"; prev=""
   330	for a in "$@"; do
   331	    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
   332	    prev="$a"
   333	done
   334	if [ -n "${FX_ARGS:-}" ]; then
   335	    { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
   336	    pwd >> "$FX_ARGS.cwd"
   337	    head -c 60 >> "$FX_ARGS.stdin"
   338	fi
   339	cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
   340	EOF
   341	chmod +x "$T/fakecodex.sh"
   342	#  the default-path fake under the scratch HOME: it marks the run, then is the same fake (the tracked launcher names only this
   343	#  path; the after launcher reaches it only when CX_CODEX_BIN is unset or empty)
   344	DEFBIN="$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
   345	mkdir -p "$DEFBIN"
   346	printf '#!/bin/bash\n[ -n "${FX_ARGS:-}" ] && echo DEFAULT >> "$FX_ARGS.default"\nexec bash "%s" "$@"\n' "$T/fakecodex.sh" > "$DEFBIN/codex"
   347	chmod +x "$DEFBIN/codex"
   348	printf 'control brief\n' > "$T/brief.md"
   349	printf '%30000s' '' | tr ' ' b > "$T/brief30000.md"
   350	printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"
   351	printf 'STDIN MARKER -- codex must never read this\n' > "$T/stdin_marker"
   352	
   353	pass=0; total=0
   354	run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit (? = record only, counted as a failure), then env
   355	    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
   356	    local out="$T/out_${row}_${lab}"
   357	    case " $* " in *" CX_AUP_MODEL= "*) : > "$T/disabled_${row}_${lab}" ;; esac
   358	    #  v6: SEED=1 pre-seeds the out dir with a stale answer and a stale header (RS); NEST=1 puts it two levels below a
   359	    #  missing parent (MP).  Both reach the launcher's environment too, where nothing reads them.
   360	    case " $* " in *" SEED=1 "*) mkdir -p "$out"; cp "$T/seed_stdout" "$out/codex_${row}.txt"; cp "$T/seed_stderr" "$out/codex_${row}.err" ;; esac
   361	    case " $* " in *" NEST=1 "*) out="$out/nest/ed" ;; esac
   362	    ( export HOME="$T/home" CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
   363	      for kv in "$@"; do export "$kv"; done
   364	      [ "${UNSET_CODEX_BIN:-}" = 1 ] && unset CX_CODEX_BIN
   365	      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" < "$T/stdin_marker" ) > "$T/log_${row}_${lab}.txt" 2>&1
   366	    local got=$?
   367	    echo "$got" > "$T/exit_${row}_${lab}"
   368	    total=$((total + 1))
   369	    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
   370	    printf '%-4s %-7s exit=%-3s want=%-3s %s\n' "$row" "$lab" "$got" "$want" "$ok"
   371	    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
   372	}
   373	three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
   374	    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
   375	    if [ "$ONLY" != 1 ]; then
   376	        run "$row" tracked "$TRACKED" "$wt" "$@"
   377	        run "$row" before "$BEFORE" "$wb" "$@"
   378	    fi
   379	    run "$row" after "$AFTER" "$wa" "$@"
   380	}
   381	check() {    # $1 label, $2 0/1 result
   382	    total=$((total + 1))
   383	    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
   384	}
   385	
   386	echo "# cxlaunch landing controls (v6), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
   387	echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
   388	echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
   389	echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
   390	three P1 8 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
   391	three P2 7 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
   392	three N1 8 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
   393	three N2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
   394	three N3 6 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
   395	three N4 8 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
   396	three Q1 7 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
   397	three Q2 8 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
   398	three Q3 6 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
   399	three A1 6 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
   400	three M1 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   401	three M2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
   402	three D1 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
   403	three D2 7 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
   404	three X1 6 6 6 FX="$T/fx/X1" CX_AUP_MODEL=
   405	three X2 8 0 0 FX="$T/fx/X2" CX_AUP_MODEL=
   406	three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
   407	three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
   408	three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
   409	three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
   410	three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
   411	three W12 0 0 5 FX="$T/fx/W12" CX_AUP_MODEL=
   412	three W13 0 0 0 FX="$T/fx/W13" CX_AUP_MODEL=
   413	three X13 0 0 5 FX="$T/fx/X13" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   414	three K30 0 0 5 FX="$T/fx/K30" CX_AUP_MODEL=
   415	three K31 0 0 0 FX="$T/fx/K31" CX_AUP_MODEL=
   416	three R2X 6 6 7 FX="$T/fx/R2" CX_AUP_MODEL=
   417	three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
   418	three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
   419	three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
   420	#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5, EO, FR and
   421	#  RN (refusals), set to a NON-default model by OV, and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
   422	#  GLM 5.3, v4 pass.)
   423	three FB1 8 0 0 FX="$T/fx/N1"
   424	three FB2 8 8 8 FX="$T/fx/P1"
   425	three X14 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30000.md"
   426	three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"
   427	#  v5 rows
   428	three RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=
   429	three RC3A 3 3 3 FX="$T/fx/RC3A" CX_AUP_MODEL=
   430	three RC2W 8 8 8 FX="$T/fx/RC2W" CX_AUP_MODEL=
   431	three B1G 8 0 0 FX="$T/fx/B1G" CX_AUP_MODEL=
   432	three B1E 0 0 0 FX="$T/fx/B1E" CX_AUP_MODEL=
   433	three D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest
   434	three CH 0 0 5 FX="$T/fx/CH" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   435	three DP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= UNSET_CODEX_BIN=1
   436	three EO 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest CX_CODEX_BIN= CX_MODEL= CX_EFFORT= CX_AUP_EFFORT=
   437	three RF1 7 7 7 FX="$T/fx/RF1" CX_AUP_MODEL=
   438	three RF2 7 7 7 FX="$T/fx/RF2" CX_AUP_MODEL=
   439	three RF3 7 7 7 FX="$T/fx/RF3" CX_AUP_MODEL=
   440	three RFC 7 7 7 FX="$T/fx/RFC" CX_AUP_MODEL=
   441	three WL1 8 8 8 FX="$T/fx/WL1" CX_AUP_MODEL=
   442	three WL2 8 8 8 FX="$T/fx/WL2" CX_AUP_MODEL=
   443	three WL3 8 8 8 FX="$T/fx/WL3" CX_AUP_MODEL=
   444	three WLC 8 8 8 FX="$T/fx/WLC" CX_AUP_MODEL=
   445	three CSI 6 6 7 FX="$T/fx/CSI" CX_AUP_MODEL=
   446	three RW 7 7 7 FX="$T/fx/RW" CX_AUP_MODEL=
   447	three RI 7 7 7 FX="$T/fx/RI" CX_AUP_MODEL=
   448	three WI 8 8 8 FX="$T/fx/WI" CX_AUP_MODEL=
   449	three EM 6 6 6 FX="$T/fx/EM" CX_AUP_MODEL=
   450	three IR 1 1 5 FX="$T/fx/IR" CX_AUP_MODEL=
   451	three WS 0 0 0 FX="$T/fx/WS" CX_AUP_MODEL=
   452	three MA 0 0 0 FX="$T/fx/MA" CX_AUP_MODEL=
   453	three TM 0 0 0 FX="$T/fx/TM" CX_AUP_MODEL=
   454	three NM 0 0 0 FX="$T/fx/NM" CX_AUP_MODEL=
   455	three BA 0 0 5 FX="$T/fx/BA" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   456	three HB 0 0 0 FX="$T/fx/HB" CX_AUP_MODEL=
   457	three R7A 0 0 0 FX="$T/fx/R7A" CX_AUP_MODEL=
   458	three R7B 0 0 5 FX="$T/fx/R7B" CX_AUP_MODEL= CX_MODEL=gpt-6-other
   459	#  v6 rows (the tracked and before expectations recorded from RECEIPT_v6_calibration.txt; the after ones written first)
   460	three OV 7 0 0 FX="$T/fx/P2" FX2="$T/fx/OV2" FX2_MODEL=m-fallback CX_MODEL=m-primary CX_EFFORT=low CX_AUP_MODEL=m-fallback CX_AUP_EFFORT=high
   461	three FR 7 3 3 FX="$T/fx/P2" FX2="$T/fx/FR3" FX2_MODEL=gpt-daybreak-blue-latest
   462	three RS 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= SEED=1
   463	three MP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= NEST=1
   464	three RN 7 0 0 FX="$T/fx/RN1" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
   465	three SP1 0 0 5 FX="$T/fx/SP1" CX_AUP_MODEL=
   466	three SP2 0 0 5 FX="$T/fx/SP2" CX_AUP_MODEL=
   467	three CZ 6 6 7 FX="$T/fx/CZ" CX_AUP_MODEL=
   468	three WZ 0 0 0 FX="$T/fx/WZ" CX_AUP_MODEL=
   469	three R7X 7 7 7 FX="$T/fx/R7X" CX_AUP_MODEL=
   470	three BN 0 0 0 FX="$T/fx/BN" CX_AUP_MODEL=
   471	three R9A 0 0 5 FX="$T/fx/R9A" CX_AUP_MODEL=
   472	three R9B 0 0 0 FX="$T/fx/R9B" CX_AUP_MODEL=
   473	
   474	#  E0: the fake ran for every row of every column but X15's, and never for X15's (it must exit 9 BEFORE codex); the run count is
   475	#  pinned, so a deleted row is visible.  The other aggregate checks read the AFTER runs; each pins its own denominator.
   476	cols=3; [ "$ONLY" = 1 ] && cols=1
   477	nruns=$(ls "$T"/log_* 2>/dev/null | wc -l)
   478	miss=""; extra=""
   479	for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}
   480	    case "$b" in X15_*) [ -e "$T/args_$b" ] && extra="$extra $b" ;; *) [ -s "$T/args_$b" ] || miss="$miss $b" ;; esac
   481	done
   482	[ "$nruns" = $((NROWS * cols)) ] && [ -z "$miss" ] && [ -z "$extra" ]; check "E0  all  the fake codex was reached by every run but X15's, and by none of X15's ($NROWS rows x $cols = $nruns of $((NROWS * cols)), pinned)${miss:+ -- NOT reached:$miss}${extra:+ -- X15 REACHED it:$extra}" $?
   483	nafter=0; dbad=""; sbad=""; ns=0; cbad=""; nc=0; pbad=""; fbad=""; nfd=0
   484	for f in "$T"/exit_*_after; do r=${f##*/exit_}; r=${r%_after}; nafter=$((nafter + 1))
   485	    case "$r" in
   486	        DP|EO) [ -e "$T/args_${r}_after.default" ] || dbad="$dbad $r(not reached)" ;;
   487	        *) [ -e "$T/args_${r}_after.default" ] && dbad="$dbad $r" ;;
   488	    esac
   489	    if [ -e "$T/args_${r}_after.stdin" ]; then ns=$((ns + 1)); [ -s "$T/args_${r}_after.stdin" ] && sbad="$sbad $r"; fi
   490	    if [ -e "$T/args_${r}_after.cwd" ]; then nc=$((nc + 1))
   491	        while IFS= read -r d; do [ "$(printf '%s' "$d" | tr 'A-Z' 'a-z')" = /c/documentnosnc/cc/gxemul ] || cbad="$cbad $r"; done < "$T/args_${r}_after.cwd"
   492	    fi
   493	    e=$(cat "$f"); L="$T/log_${r}_after.txt"
   494	    a=$(grep -c 'seat answered' "$L"); l=$(grep -c 'The answer is LOST' "$L"); b=$(grep -c 'answered by: ' "$L"); u=$(grep -c 'model UNVERIFIED' "$L")
   495	    w=$(grep -c 'SEAT WALLED' "$L")    # v6: status.sh counts it (GPT-6 Astra, v5 pass)
   496	    case "$e" in
   497	        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ "$w" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
   498	        #  v6: LOST is the REFUSAL exit's; codex's own rc 7 prints `codex exited 7' and no LOST (GPT-6 Astra, v5 pass)
   499	        7) if grep -qF '*** codex exited 7 ' "$L"; then { [ "$l" = 0 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"
   500	           else { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"; fi ;;
   501	        8) { [ "$w" -ge 1 ] && [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
   502	        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r" ;;
   503	    esac
   504	    if [ -e "$T/disabled_${r}_after" ] && [ "$r" != X15 ]; then nfd=$((nfd + 1))
   505	        [ "$(grep -c '^CALL$' "$T/args_${r}_after" 2>/dev/null)" = 1 ] || fbad="$fbad $r"
   506	    fi
   507	done
   508	[ "$nafter" = "$NROWS" ] && [ -z "$dbad" ]; check "E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of $nafter)${dbad:+ -- wrong:$dbad}" $?
   509	[ "$ns" = $((NROWS - 1)) ] && [ -z "$sbad" ]; check "SI  after  no after run's codex read the stdin the launcher was fed ($ns runs that reached codex, of $((NROWS - 1)))${sbad:+ -- READ IT:$sbad}" $?
   510	[ "$nc" = $((NROWS - 1)) ] && [ -z "$cbad" ]; check "CWD after  every after run's codex started in the project root ($nc of $((NROWS - 1)))${cbad:+ -- elsewhere:$cbad}" $?
   511	[ "$nfd" = "$NFD" ] && [ -z "$fbad" ]; check "FD  after  every row that sets CX_AUP_MODEL empty made exactly one call ($nfd rows, $NFD pinned)${fbad:+ -- more:$fbad}" $?
   512	[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff the refusal exit 7, 'SEAT WALLED' iff exit 8, 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
   513	#  v6: the NUMBERS too -- v5 read only the format, and `stdout=$(wc -c < "$ERR")' passed (GPT-6 Astra, v5 pass)
   514	logline() {    # $1 fixture dir, $2 model -- the exact line the launcher must log for one call replaying it
   515	    printf 'codex rc=%s   stdout=%s b   stderr=%s b   asked: %s / ultra\n' "$(cat "$1/rc")" "$(wc -c < "$1/stdout")" "$(wc -c < "$1/stderr")" "$2"
   516	}
   517	logline "$T/fx/N1" gpt-6-astra > "$T/want_LOG_N1"; { logline "$T/fx/P2" gpt-6-astra; logline "$T/fx/DB_OK" gpt-daybreak-blue-latest; } > "$T/want_LOG_D1"
   518	logline "$T/fx/RC3A" gpt-6-astra > "$T/want_LOG_RC3A"
   519	lbad=""; for r in N1 D1 RC3A; do grep '^codex rc=' "$T/log_${r}_after.txt" | cmp -s - "$T/want_LOG_$r" || lbad="$lbad $r"; done
   520	[ -z "$lbad" ]; check "LOG after  the 'codex rc=N   stdout=N b   stderr=N b   asked: M / E' lines of N1, D1 (both calls) and RC3A, WHOLE: the format the censuses parse and each number the fixture's own${lbad:+ -- wrong:$lbad}" $?
   521	[ "$(ls "$T/out_N1_after" | wc -l)" = 2 ] && cmp -s "$T/out_N1_after/codex_N1.txt" "$T/fx/N1/stdout" && cmp -s "$T/out_N1_after/codex_N1.err" "$T/fx/N1/stderr"; check "N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr" $?
   522	grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_N1_after.txt"; check "N1V after  N1 is credited to gpt-6-astra" $?
   523	wbad=""; for r in WS MA TM WZ BN; do grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_${r}_after.txt" || wbad="$wbad $r"; done
   524	[ -z "$wbad" ]; check "WMT after  WS, MA, TM, WZ and BN verify gpt-6-astra (not UNVERIFIED)${wbad:+ -- wrong:$wbad}" $?
   525	#  content, not exit status -- on the AFTER logs
   526	for r in M2 X6 X9 W13 K31 NM HB R9B; do
   527	    grep -q 'model UNVERIFIED' "$T/log_${r}_after.txt" && ! grep -q 'answered by:' "$T/log_${r}_after.txt"; check "$r  after  says model UNVERIFIED and names no model" $?
   528	done
   529	cmp -s "$T/out_D1_after/codex_D1.refused.txt" "$T/fx/P2/stdout" && cmp -s "$T/out_D1_after/codex_D1.refused.err" "$T/fx/P2/stderr" \
   530	    && cmp -s "$T/out_D1_after/codex_D1.txt" "$T/fx/DB_OK/stdout" && cmp -s "$T/out_D1_after/codex_D1.err" "$T/fx/DB_OK/stderr" \
   531	    && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1R after  refused run kept byte-for-byte as .refused.txt/.err, Daybreak's run as .txt/.err, Daybreak credited" $?
   532	[ "$(grep -c '^CALL$' "$T/args_FB1_after" 2>/dev/null)" = 1 ] && ! ls "$T/out_FB1_after"/*.refused.* >/dev/null 2>&1; check "FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused" $?
   533	[ "$(grep -c '^CALL$' "$T/args_FB2_after" 2>/dev/null)" = 1 ]; check "FB2 after  the fallback on, a wall: ONE call" $?
   534	[ "$(grep -c '^CALL$' "$T/args_D4_after" 2>/dev/null)" = 2 ]; check "D4  after  refused, then refused on Daybreak: EXACTLY two calls" $?
   535	[ "$(grep -c '^CALL$' "$T/args_D3_after" 2>/dev/null)" = 2 ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D3_after.txt"; check "D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited" $?
   536	[ "$(grep -c '^CALL$' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked ON Daybreak and refused: ONE call, no re-run on the same model" $?
   537	[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?
   538	grep -qF "codex's header says gpt-6-astra" "$T/log_CH_after.txt"; check "CH  after  the coloured header is read: the log names gpt-6-astra as the model that ran" $?
   539	#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
   540	callseq() {    # $1 model -- the sequence one call must receive
   541	    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
   542	    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
   543	}
   544	callseq gpt-6-astra > "$T/want_E1"
   545	{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
   546	cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
   547	cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
   548	cmp -s "$T/want_E2" "$T/args_EO_after"; check "EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2" $?
   549	cmp -s "$T/want_E1" "$T/args_DP_after"; check "DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1" $?
   550	#  v6 content checks
   551	callseq2() {    # $1 model, $2 effort
   552	    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
   553	    printf 'ARG model_reasoning_effort=%s\nARG control brief\n' "$2"
   554	}
   555	{ callseq2 m-primary low; callseq2 m-fallback high; } > "$T/want_OV"
   556	cmp -s "$T/want_OV" "$T/args_OV_after" && grep -qF 'seat answered. (answered by: m-fallback)' "$T/log_OV_after.txt"; check "OVA after  CX_MODEL, CX_EFFORT, CX_AUP_MODEL, CX_AUP_EFFORT set to NON-default values: each reaches its own call, both compared whole; the fallback credited" $?
   557	[ "$(ls "$T/out_RS_after" | wc -l)" = 2 ] && cmp -s "$T/out_RS_after/codex_RS.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_RS_after/codex_RS.err" "$T/fx/ANS/stderr"; check "RSF after  a re-run into a dir holding a stale answer and a stale header: both files TRUNCATED, byte-for-byte the new run's" $?
   558	cmp -s "$T/out_MP_after/nest/ed/codex_MP.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_MP_after/nest/ed/codex_MP.err" "$T/fx/ANS/stderr"; check "MPF after  an out dir two levels below a missing parent is created, and the run lands in it" $?
   559	cmp -s "$T/out_RN_after/codex_RN.refused.txt" "$T/fx/RN1/stdout" && cmp -s "$T/out_RN_after/codex_RN.refused.err" "$T/fx/RN1/stderr" \
   560	    && cmp -s "$T/out_RN_after/codex_RN.txt" "$T/fx/DB_OK/stdout"; check "RNF after  a NON-EMPTY refused stdout is kept byte-for-byte as .refused.txt; Daybreak's answer is .txt" $?
   561	grep -qF '*** codex exited 7 ' "$T/log_R7X_after.txt" && ! grep -q 'The answer is LOST' "$T/log_R7X_after.txt" && ! grep -q 'seat answered' "$T/log_R7X_after.txt"; check "R7XL after  codex's own rc 7 with an answer: 'codex exited 7', and neither LOST nor answered" $?
   562	echo "CONTROLS: $pass/$total as expected"
   563	echo "CXLAND_CONTROLS_DONE"
   564	[ "$pass" = "$total" ]
```

### 3b'. their v5 -> v6 diff (212 changed lines)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh	2026-10-17 03:32:05.885995700 -0500
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/cxlaunchland_20261016/run_controls_v6.sh	2026-10-17 05:08:15.140382700 -0500
@@ -1,6 +1,6 @@
 #!/bin/bash
 #  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
-#  F1), v5 after the four-seat pass 2, the adjudication pass, the v3 pass and the v4 pass.  Every row runs a launcher against a FAKE
+#  F1), v6 after the four-seat pass 2, the adjudication pass and the v3, v4 and v5 passes.  Every row runs a launcher against a FAKE
 #  codex that replays a fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the
 #  expected one:
 #
@@ -23,16 +23,31 @@
 #  124 and reds; an honest run takes about 0.6 s -- Fable 5.1, v4 pass) and is fed a MARKER file on stdin; HOME is a scratch
 #  dir holding a second fake at the launcher's default codex path, which marks the runs that reach it.
 #
+#  v6 -- the v5 pass measured one-edit mutants passing all 224 v5 controls at decisions the v5 CONTRACT listed as pinned, one
+#  shape again: a row pinned the DEFAULT of a value and not the value itself, or a fresh state and not a used one.  Each
+#  override honoured only as empty or default (CX_EFFORT=ultra, the fallback's effort and model, the main call's model --
+#  GLM 5.3, GPT-6 Astra, Fable 5.1); `>' and `2>' never met a used out dir (`>>' passes -- all four seats); `mkdir -p' never
+#  met a missing parent; the refused run's stdout was always empty; the fallback's own rc never nonzero with an answer; the
+#  rule patterns' anchors, a parameterless CSI, `model:' with no space, the banner text's `Codex', a nine-dash rule; and the
+#  `codex rc=' line's numbers, never compared.  The CONTRACT also said no caller reads the wall wording (status.sh does),
+#  `The answer is LOST' iff exit 7 (codex's own rc 7 exits 7 without it), and that nine dashes are not a rule (they are --
+#  the pattern has no end anchor; Grok 4.7), and that a relative brief makes the LAUNCHER exit 1 (it does not: an empty
+#  prompt reaches codex, and codex decided -- Fable 5.1, measured).  Each is now a row, a check or a corrected sentence.
+#
 #  THE CONTRACT -- each decision of the landed launcher (by construct), the rows that pin its edges, and what is not pinned:
 #  configuration
 #    CX_CODEX_BIN honoured, its `:-'      E0b (no after run but DP's and EO's reaches the default-path fake); EO (set EMPTY)
 #    the default codex path               DP (CX_CODEX_BIN unset: the run reaches $HOME/AppData/Local/Programs/.../codex)
 #    CX_MODEL, CX_EFFORT, CX_AUP_EFFORT, their `:-' and defaults
-#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default)
+#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default); OVA (each
+#                                         set to a NON-default value: each reaches its own call, both compared whole)
 #    CX_AUP_MODEL, its default and `-' (EMPTY disables the fallback)
-#                                         E2; FD (every row that sets it empty makes exactly one call)
-#    the output names and the stdout/stderr redirections, `mkdir -p "$OUT"'
-#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written)
+#                                         E2; FD (every row that sets it empty makes exactly one call); OVA (a non-default
+#                                         fallback model is the second call's)
+#    the output names and the stdout/stderr redirections
+#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written); RSF
+#                                         (a re-run into a dir holding a stale answer and a stale header: both TRUNCATED)
+#    `mkdir -p "$OUT"'                    MPF (an out dir two levels below a missing parent is created)
 #    `< /dev/null' on codex's stdin       SI (no after run's codex reads the marker the launcher is fed)
 #    `cd "$PROJ"'                         CWD (every after run's codex starts in the project root)
 #    the argv cap `sz -gt 30000', exit 9  X14 (30,000 accepted) / X15 (30,001: exit 9, codex never called)
@@ -44,24 +59,32 @@
 #                                         X9, X10 (no opening block, a quoted one at line 21)
 #    the banner: `h == 0 &&', `/^OpenAI Codex/'
 #                                         HB (a banner-shaped line inside the block does not restart it); BA (a banner with a
-#                                         prefix, above the real one, is not a banner); every header row (the text)
+#                                         prefix, above the real one, is not a banner); BN (`OpenAI notice:', a near-miss
+#                                         above the real banner, is not one: the text's `Codex'); every header row
 #    the first rule: `h == 1 &&', 8 dashes, `next'
 #                                         BA (a rule before any banner is not the first rule); R7A (seven dashes are not a
-#                                         rule; nine find no block anywhere); every header row (`next')
+#                                         rule); R9A (nine dashes ARE one -- the pattern has no end anchor; the v5 gloss
+#                                         "nine find no block anywhere" was false, Grok 4.7); SP1 (a separator not at column
+#                                         0, before the first rule, is not one: the `^'); every header row (`next')
 #    the closing rule: `h == 2 &&', 8 dashes, `exit'
 #                                         BA (a rule before any banner closes nothing); R7B (seven dashes do not close the
-#                                         block); NM (no model line in the block: a model line after the close is not read)
+#                                         block); R9B (nine dashes DO close it: a model after them is not read); SP2 (a
+#                                         separator not at column 0, inside the body, does not close it: the `^'); NM (no
+#                                         model line in the block: a model line after the close is not read)
 #    the body: `h == 2', the cap `++n > 30'
 #                                         R7A (the lines between banner and first rule are not body); K30 / K31 (a model at
 #                                         body line 30 read, at 31 not)
 #    the first `model:' line, anchored    TM (two model lines: the first is read); MA (`fallback model:' is not a model line);
 #                                         M1, X5
-#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies)
+#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies); WZ (`model:gpt-6-astra',
+#                                         NO whitespace, verifies: the trims' `*', zero or more)
 #  classification
 #    the gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4; RC2W (rc 2 with an answer IS classified); B1G (a 1-byte rc-0
 #                                         answer is NOT)
 #    `^ERROR:', `grep -a'                 X1; X8
-#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR)
+#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR);
+#                                         CZ (`ESC[m', a CSI with NO parameter: the class's `*')
+#    the ESC byte, `printf '\033''        A1, CH, CSI, CZ, Q3, R2X -- each needs the strip, and a wrong ESC strips nothing
 #    the refusal alternatives, `-i'       P2, Q1, A1 (`flagged for possible cybersecurity'); RF1 (`cannot help with');
 #                                         RF2 (`can't help with'); RF3 (`I won't help'); RFC (the first, upper case)
 #    the wall alternatives, `-i'          P1, Q2, Q3, X8 (`usage limit'); WL1 (`quota'); WL2 (`rate limit');
@@ -75,10 +98,11 @@
 #                                         never); D5 (asked ON Daybreak and refused: no second run)
 #    once                                 D4 (refused, then refused on Daybreak: exactly two calls)
 #    the refused run's files kept         D1R (codex_D1.refused.txt and .refused.err byte-for-byte the first run's; codex_D1.txt
-#                                         and .err the Daybreak run's)
+#                                         and .err the Daybreak run's); RNF (a NON-EMPTY refused stdout, byte-for-byte)
 #    the answer credited to the fallback  D1, D3 (Daybreak credited); D2 (Daybreak compared -> 5)
 #  the exit cascade: refused 7, walled 8, empty 6, a different model 5, codex's own rc
-#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1)
+#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1); FR (3:
+#                                         the FALLBACK run's raw rc, with an answer); R7X (codex's own rc 7 with an answer)
 #    the order, each adjacent pair        RW (refusal + wall -> 7); P2 (refusal + empty + rc 1 -> 7); RI (refusal + another
 #                                         model's header -> 7); P1 (wall + empty -> 8); WI (wall + another header -> 8);
 #                                         EM (empty + another header -> 6); X1 (empty + rc 1 -> 6); IR (rc 1, an answer,
@@ -86,33 +110,77 @@
 #    the empty test `body -eq 0'          N3, X1 (0 bytes -> 6); B1E (1 byte -> 0)
 #    identity `-n RAN && RAN != ANSWERED_BY'
 #                                         M1, D2, X5, W12, K30, X13, CH, IR, BA -> 5; M2, X6, X9, W13, K31, NM, HB -> UNVERIFIED, 0
-#  the log phrases a caller reads (_scratchpad/codexpack_20260928/run_pack_body.sh: done_job and reap)
-#    `seat answered' iff exit 0; `The answer is LOST' iff exit 7; `answered by: <model>' iff an exit 0 whose model verified
-#                                         PK (every after run); N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB (none)
-#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, which the launch-log censuses this file cites parse
-#                                         LOG (N1)
+#  the log phrases a caller reads -- _scratchpad/codexpack_20260928/run_pack_body.sh (done_job and reap) AND status.sh beside
+#  it, which counts `SEAT WALLED' (GPT-6 Astra, v5 pass: the v5 CONTRACT said no caller read the wall wording); derived by
+#  `grep -rlE "SEAT WALLED|The answer is LOST|seat answered|answered by: "' over _scratchpad and GXEMUL-SEC/tools, the
+#  launcher copies and the agy pack excluded -- the two pack scripts above and census_v5.py are the readers
+#    `seat answered' iff exit 0; `The answer is LOST' iff the REFUSAL exit (codex's own rc 7 also exits 7 and prints `codex
+#    exited 7' instead, so the runner retries it -- R7X); `SEAT WALLED' iff exit 8; `answered by: <model>' iff an exit 0
+#    whose model verified
+#                                         PK (every after run); R7XL; N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB,
+#                                         R9B (none)
+#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, which the launch-log censuses this file cites parse --
+#    its FORMAT and its NUMBERS (the fixture's own rc and byte counts; v5 read the format only, GPT-6 Astra)
+#                                         LOG (N1, both of D1's calls, RC3A: each line compared whole)
 #  NOT PINNED, each with its reason:
 #    `|| exit 9' after `cd'               needs a missing project dir -- untestable without editing the file
 #    `set -u'                             reached only by a missing positional argument (a usage error, exit 1); every caller
 #                                         passes three, and a row without them would write outside the scratch dir under a
-#                                         mutant that drops it
+#                                         mutant that drops it.  Load-bearing for one kill: under it `m_noinit''s unbound
+#                                         `$refus' errors every rc-0 row (Fable 5.1, v5 pass)
 #    the banner rule's `next'             equivalent: the banner line matches no later rule
-#    RELATIVE paths                       the brief's size and `mkdir' resolve in the caller's directory, codex's files after
-#                                         `cd "$PROJ"', so a relative brief or out path breaks (measured 2026-10-17: a relative
-#                                         pointer read 787 bytes, codex got no brief, exit 1 -- NOT a clean run, nothing
-#                                         laundered).  Disclosed in the usage line; every caller on record, and every row here,
-#                                         passes absolute paths
+#    the body cap's and the window guard's `exit' (not `next')
+#                                         equivalent: past the cap every later line also fails `++n > 30' and is not
+#                                         printed, and past line 12 with no block every later line is skipped either way
+#    `mv -f' (both moves)                 equivalent off a terminal: mv prompts only with a terminal on stdin AND an
+#                                         unwritable destination; no caller runs the launcher on a terminal
+#    `2>/dev/null' on strip_ansi and on the verdict grep
+#                                         display only: each reads a file that exists whenever it runs ($ERR after codex
+#                                         wrote it; $TXT), and the suppressed text changes no decision
+#    RELATIVE or MISSING paths            the brief's size and `mkdir' resolve in the caller's directory, codex's files after
+#                                         `cd "$PROJ"', and the brief is not checked: a missing or relative brief reaches codex
+#                                         as an EMPTY prompt, and what codex does is what is reported -- on 2026-10-17 codex
+#                                         refused it and exited 1, while a fake that answers it is reported `seat answered',
+#                                         exit 0 (Fable 5.1, v5 pass, measured; the v5 text called the exit 1 the launcher's).
+#                                         It is `cxlaunchempty''s defect -- an empty prompt reaches codex -- by a second road,
+#                                         and is FILED on that row with the relative OUT dir.  Every caller in the tree passes
+#                                         absolute paths (the pack runner's ARTS defaults to one, and it skips a missing
+#                                         brief); so does every row here
+#    the `model:' label's case, and the identity compare's case
+#                                         equivalent on record: codex's header is lower-case by its format (all 975 opening
+#                                         blocks match `^model:'), and a case-folded compare is a policy change, not a drift
+#    `wc -c' (bytes) for the argv cap     equivalent here: under the C locale the harness and the farm run in `wc -m' counts
+#                                         bytes too, and every brief on record is ASCII
+#    the banner past `OpenAI Codex' (narrowed to `OpenAI Codex v')
+#                                         equivalent on record: every banner is `OpenAI Codex v...' (BN pins the widening)
+#    the closing rule's `exit' against another way to end the block (`h = 3; next')
+#                                         equivalent by construction: nothing matches past the close either way; the edge
+#                                         that matters, `exit' against `next', is NM's
+#    the `.' of `can.t' and `won.t'       the quoting form of an apostrophe inside a single-quoted pattern, not a decision:
+#                                         an ASCII `'' cannot be written there, and 0 column-0 ERROR lines on record carry a
+#                                         curly apostrophe or any non-ASCII byte (Fable 5.1, v5 pass)
 #    display only -- printed, read by no decision and no caller: `brief bytes'; the `ran:' line (the header's effort is
 #                                         printed, never compared); `verdict-in-stdout' (verd exists for that line alone); the
 #                                         IGNORED note; the refusal excerpts (`-m1'/`-m2', `cut -c1-160'); the REPHRASE line;
-#                                         the wording of the 5, 6, 8 and rc messages beyond the phrases above
-#  SYNTHETIC SHAPES, pinned because a constant's edges are what an edge row is for: RF1-RF3, RFC, WL1-WL3, WLC, RW, BA, HB,
-#  R7A, R7B, NM, TM, MA, WS, K30, K31 and W12/W13 have 0 instances on record, and so does CSI's non-SGR half (CENSUS_v5.txt,
-#  which names each count).  CSI's other half is NOT synthetic: a `;'-joined SGR sits in 44 of the 2,425 codex .err files on
-#  record, so the strip's `;' is load-bearing.
+#                                         the wording of the 5, 6, 8 and rc messages beyond the phrases above (the 8's `SEAT
+#                                         WALLED' and the rc message's `codex exited N' ARE pinned, by PK and R7XL)
+#  SYNTHETIC SHAPES, and THE BOUNDARY of what is pinned without an instance on record (Fable 5.1, v5 pass, with GLM 5.3's and
+#  Grok 4.7's criterion; pass 2's "0 on record, so disclose" is superseded): a synthetic edge is PINNED when its constant
+#  selects an exit status, a call argument or a log phrase a caller reads, on an input codex can produce through its
+#  documented interface -- a diagnostic line, a header line, an escape sequence, a status, an answer; it is DISCLOSED as
+#  equivalent when the edge is reachable only through the harness environment (a locale), an input encoding the file does
+#  not claim, a flag whose other value is unreachable here, or a display line (the NOT PINNED list).  Pinned under it, each
+#  with 0 instances on record (CENSUS_v5.txt names each count): RF1-RF3, RFC, WL1-WL3, WLC, RW, RI, WI, EM, IR, BA, BN, HB,
+#  R7A, R7B, R9A, R9B, SP1, SP2, NM, TM, MA, WS, WZ, K30, K31, W12/W13, CZ, R7X, RC1A, RC3A, RC2W, B1G, B1E, D5, FR, RN, RS, MP,
+#  OV and the fallback rows' Daybreak answers -- every rc row and every Daybreak answer sits off CENSUS_v5's diagonal (0
+#  launch lines off rc 0 with stdout / rc 1 empty) -- and CSI, in BOTH halves.  The v5 CONTRACT called its `;'-joined half load-bearing because 44 of the codex .err files carry
+#  one; 42 of the 44 are the #544 control stub's own output and the other 2 quote a coloured GXemul prompt mid-line, never a
+#  codex diagnostic (v5pass/SEMISGR_WHERE.txt; GPT-6 Astra, v5 pass).  Every line opening with eight dashes in the first 42
+#  lines of the 2,427 codex .err files is exactly eight dashes (1,954 lines, v5pass/RULELEN_CENSUS.txt), so R9A/R9B pin the
+#  pattern's own edge, not a shape seen.
 #
 #  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
-#  Usage: bash run_controls_v5.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
+#  Usage: bash run_controls_v6.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
 #  the mutant table uses; writes only to a scratch dir it removes)
 set -u
 HERE=$(cd "$(dirname "$0")" && pwd)
@@ -123,8 +191,8 @@
 ONLY="${CXL_AFTER_ONLY:-}"
 N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
 QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
-NROWS=65
-NFD=56
+NROWS=78
+NFD=66
 for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
          "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout" "$HERE/fx/R2.stderr"; do
     [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
@@ -233,6 +301,26 @@
     | mkfx R7A 0 "$T/ans_verdict.txt" -
 printf 'OpenAI Codex v0.153.4\n--------\n-------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
     | mkfx R7B 0 "$T/ans_verdict.txt" -
+#  v6 (the v5 pass): each override's VALUE honoured at its own call, the fallback's own rc, a re-run into a used dir, a missing
+#  parent, a non-empty refused stdout, separators off column 0, a parameterless CSI, `model:' with no space, codex's own rc 7, a
+#  near-miss banner, nine-dash rules
+hdr m-fallback | mkfx OV2 0 "$T/ans_verdict.txt" -
+hdr gpt-daybreak-blue-latest | mkfx FR3 3 "$T/ans_verdict.txt" -
+printf 'STALE ANSWER from an earlier run of this tag\n' > "$T/seed_stdout"
+hdr gpt-6-stale > "$T/seed_stderr"
+printf 'A partial answer the content filter cut off.\n' > "$T/ans_partial.txt"
+mkfx RN1 1 "$T/ans_partial.txt" "$HERE/fx/P2.stderr"
+printf 'OpenAI Codex v0.153.4\nx --------\n--------\nworkdir: x\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
+    | mkfx SP1 0 "$T/ans_verdict.txt" -
+printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nnote: a -------- b\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
+    | mkfx SP2 0 "$T/ans_verdict.txt" -
+printf '%s\n' "${ESC}[mERROR: This content was flagged for possible cybersecurity risk." | mkfx CZ 1 "" -
+printf 'OpenAI Codex v0.153.4\n--------\nmodel:gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx WZ 0 "$T/ans_verdict.txt" -
+mkfx R7X 7 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
+{ printf 'OpenAI notice: a deprecation warning\n--------\nmodel: gpt-6-other\n--------\n'; cat "$T/hdr_astra.txt"; } \
+    | mkfx BN 0 "$T/ans_verdict.txt" -
+printf 'OpenAI Codex v0.153.4\n---------\nmodel: gpt-6-other\nreasoning effort: ultra\n---------\n' | mkfx R9A 0 "$T/ans_verdict.txt" -
+printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\n---------\nmodel: gpt-6-other\n' | mkfx R9B 0 "$T/ans_verdict.txt" -
 
 #  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL); logs its arguments to $FX_ARGS, its working
 #  directory to $FX_ARGS.cwd and the first 60 bytes of its stdin to $FX_ARGS.stdin
@@ -267,6 +355,10 @@
     local row="$1" lab="$2" sh="$3" want="$4"; shift 4
     local out="$T/out_${row}_${lab}"
     case " $* " in *" CX_AUP_MODEL= "*) : > "$T/disabled_${row}_${lab}" ;; esac
+    #  v6: SEED=1 pre-seeds the out dir with a stale answer and a stale header (RS); NEST=1 puts it two levels below a
+    #  missing parent (MP).  Both reach the launcher's environment too, where nothing reads them.
+    case " $* " in *" SEED=1 "*) mkdir -p "$out"; cp "$T/seed_stdout" "$out/codex_${row}.txt"; cp "$T/seed_stderr" "$out/codex_${row}.err" ;; esac
+    case " $* " in *" NEST=1 "*) out="$out/nest/ed" ;; esac
     ( export HOME="$T/home" CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
       for kv in "$@"; do export "$kv"; done
       [ "${UNSET_CODEX_BIN:-}" = 1 ] && unset CX_CODEX_BIN
@@ -291,7 +383,7 @@
     if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
 }
 
-echo "# cxlaunch landing controls (v5), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
+echo "# cxlaunch landing controls (v6), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
 echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
 echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
 echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
@@ -325,8 +417,8 @@
 three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
 three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
 three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
-#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5 and EO
-#  (refusals), and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
+#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5, EO, FR and
+#  RN (refusals), set to a NON-default model by OV, and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
 #  GLM 5.3, v4 pass.)
 three FB1 8 0 0 FX="$T/fx/N1"
 three FB2 8 8 8 FX="$T/fx/P1"
@@ -364,6 +456,20 @@
 three HB 0 0 0 FX="$T/fx/HB" CX_AUP_MODEL=
 three R7A 0 0 0 FX="$T/fx/R7A" CX_AUP_MODEL=
 three R7B 0 0 5 FX="$T/fx/R7B" CX_AUP_MODEL= CX_MODEL=gpt-6-other
+#  v6 rows (the tracked and before expectations recorded from RECEIPT_v6_calibration.txt; the after ones written first)
+three OV 7 0 0 FX="$T/fx/P2" FX2="$T/fx/OV2" FX2_MODEL=m-fallback CX_MODEL=m-primary CX_EFFORT=low CX_AUP_MODEL=m-fallback CX_AUP_EFFORT=high
+three FR 7 3 3 FX="$T/fx/P2" FX2="$T/fx/FR3" FX2_MODEL=gpt-daybreak-blue-latest
+three RS 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= SEED=1
+three MP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= NEST=1
+three RN 7 0 0 FX="$T/fx/RN1" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
+three SP1 0 0 5 FX="$T/fx/SP1" CX_AUP_MODEL=
+three SP2 0 0 5 FX="$T/fx/SP2" CX_AUP_MODEL=
+three CZ 6 6 7 FX="$T/fx/CZ" CX_AUP_MODEL=
+three WZ 0 0 0 FX="$T/fx/WZ" CX_AUP_MODEL=
+three R7X 7 7 7 FX="$T/fx/R7X" CX_AUP_MODEL=
+three BN 0 0 0 FX="$T/fx/BN" CX_AUP_MODEL=
+three R9A 0 0 5 FX="$T/fx/R9A" CX_AUP_MODEL=
+three R9B 0 0 0 FX="$T/fx/R9B" CX_AUP_MODEL=
 
 #  E0: the fake ran for every row of every column but X15's, and never for X15's (it must exit 9 BEFORE codex); the run count is
 #  pinned, so a deleted row is visible.  The other aggregate checks read the AFTER runs; each pins its own denominator.
@@ -386,10 +492,14 @@
     fi
     e=$(cat "$f"); L="$T/log_${r}_after.txt"
     a=$(grep -c 'seat answered' "$L"); l=$(grep -c 'The answer is LOST' "$L"); b=$(grep -c 'answered by: ' "$L"); u=$(grep -c 'model UNVERIFIED' "$L")
+    w=$(grep -c 'SEAT WALLED' "$L")    # v6: status.sh counts it (GPT-6 Astra, v5 pass)
     case "$e" in
-        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
-        7) { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
-        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
+        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ "$w" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
+        #  v6: LOST is the REFUSAL exit's; codex's own rc 7 prints `codex exited 7' and no LOST (GPT-6 Astra, v5 pass)
+        7) if grep -qF '*** codex exited 7 ' "$L"; then { [ "$l" = 0 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"
+           else { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"; fi ;;
+        8) { [ "$w" -ge 1 ] && [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
+        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r" ;;
     esac
     if [ -e "$T/disabled_${r}_after" ] && [ "$r" != X15 ]; then nfd=$((nfd + 1))
         [ "$(grep -c '^CALL$' "$T/args_${r}_after" 2>/dev/null)" = 1 ] || fbad="$fbad $r"
@@ -399,13 +509,21 @@
 [ "$ns" = $((NROWS - 1)) ] && [ -z "$sbad" ]; check "SI  after  no after run's codex read the stdin the launcher was fed ($ns runs that reached codex, of $((NROWS - 1)))${sbad:+ -- READ IT:$sbad}" $?
 [ "$nc" = $((NROWS - 1)) ] && [ -z "$cbad" ]; check "CWD after  every after run's codex started in the project root ($nc of $((NROWS - 1)))${cbad:+ -- elsewhere:$cbad}" $?
 [ "$nfd" = "$NFD" ] && [ -z "$fbad" ]; check "FD  after  every row that sets CX_AUP_MODEL empty made exactly one call ($nfd rows, $NFD pinned)${fbad:+ -- more:$fbad}" $?
-[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff exit 7, 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
-grep -qE '^codex rc=0   stdout=[0-9]+ b   stderr=[0-9]+ b   asked: gpt-6-astra / ultra$' "$T/log_N1_after.txt"; check "LOG after  N1's 'codex rc=0   stdout=N b   stderr=N b   asked: gpt-6-astra / ultra' line, as the launch-log censuses parse it" $?
+[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff the refusal exit 7, 'SEAT WALLED' iff exit 8, 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
+#  v6: the NUMBERS too -- v5 read only the format, and `stdout=$(wc -c < "$ERR")' passed (GPT-6 Astra, v5 pass)
+logline() {    # $1 fixture dir, $2 model -- the exact line the launcher must log for one call replaying it
+    printf 'codex rc=%s   stdout=%s b   stderr=%s b   asked: %s / ultra\n' "$(cat "$1/rc")" "$(wc -c < "$1/stdout")" "$(wc -c < "$1/stderr")" "$2"
+}
+logline "$T/fx/N1" gpt-6-astra > "$T/want_LOG_N1"; { logline "$T/fx/P2" gpt-6-astra; logline "$T/fx/DB_OK" gpt-daybreak-blue-latest; } > "$T/want_LOG_D1"
+logline "$T/fx/RC3A" gpt-6-astra > "$T/want_LOG_RC3A"
+lbad=""; for r in N1 D1 RC3A; do grep '^codex rc=' "$T/log_${r}_after.txt" | cmp -s - "$T/want_LOG_$r" || lbad="$lbad $r"; done
+[ -z "$lbad" ]; check "LOG after  the 'codex rc=N   stdout=N b   stderr=N b   asked: M / E' lines of N1, D1 (both calls) and RC3A, WHOLE: the format the censuses parse and each number the fixture's own${lbad:+ -- wrong:$lbad}" $?
 [ "$(ls "$T/out_N1_after" | wc -l)" = 2 ] && cmp -s "$T/out_N1_after/codex_N1.txt" "$T/fx/N1/stdout" && cmp -s "$T/out_N1_after/codex_N1.err" "$T/fx/N1/stderr"; check "N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr" $?
 grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_N1_after.txt"; check "N1V after  N1 is credited to gpt-6-astra" $?
-grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_WS_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_MA_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_TM_after.txt"; check "WMT after  WS, MA and TM verify gpt-6-astra (not UNVERIFIED)" $?
+wbad=""; for r in WS MA TM WZ BN; do grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_${r}_after.txt" || wbad="$wbad $r"; done
+[ -z "$wbad" ]; check "WMT after  WS, MA, TM, WZ and BN verify gpt-6-astra (not UNVERIFIED)${wbad:+ -- wrong:$wbad}" $?
 #  content, not exit status -- on the AFTER logs
-for r in M2 X6 X9 W13 K31 NM HB; do
+for r in M2 X6 X9 W13 K31 NM HB R9B; do
     grep -q 'model UNVERIFIED' "$T/log_${r}_after.txt" && ! grep -q 'answered by:' "$T/log_${r}_after.txt"; check "$r  after  says model UNVERIFIED and names no model" $?
 done
 cmp -s "$T/out_D1_after/codex_D1.refused.txt" "$T/fx/P2/stdout" && cmp -s "$T/out_D1_after/codex_D1.refused.err" "$T/fx/P2/stderr" \
@@ -429,6 +547,18 @@
 cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
 cmp -s "$T/want_E2" "$T/args_EO_after"; check "EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2" $?
 cmp -s "$T/want_E1" "$T/args_DP_after"; check "DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1" $?
+#  v6 content checks
+callseq2() {    # $1 model, $2 effort
+    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
+    printf 'ARG model_reasoning_effort=%s\nARG control brief\n' "$2"
+}
+{ callseq2 m-primary low; callseq2 m-fallback high; } > "$T/want_OV"
+cmp -s "$T/want_OV" "$T/args_OV_after" && grep -qF 'seat answered. (answered by: m-fallback)' "$T/log_OV_after.txt"; check "OVA after  CX_MODEL, CX_EFFORT, CX_AUP_MODEL, CX_AUP_EFFORT set to NON-default values: each reaches its own call, both compared whole; the fallback credited" $?
+[ "$(ls "$T/out_RS_after" | wc -l)" = 2 ] && cmp -s "$T/out_RS_after/codex_RS.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_RS_after/codex_RS.err" "$T/fx/ANS/stderr"; check "RSF after  a re-run into a dir holding a stale answer and a stale header: both files TRUNCATED, byte-for-byte the new run's" $?
+cmp -s "$T/out_MP_after/nest/ed/codex_MP.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_MP_after/nest/ed/codex_MP.err" "$T/fx/ANS/stderr"; check "MPF after  an out dir two levels below a missing parent is created, and the run lands in it" $?
+cmp -s "$T/out_RN_after/codex_RN.refused.txt" "$T/fx/RN1/stdout" && cmp -s "$T/out_RN_after/codex_RN.refused.err" "$T/fx/RN1/stderr" \
+    && cmp -s "$T/out_RN_after/codex_RN.txt" "$T/fx/DB_OK/stdout"; check "RNF after  a NON-EMPTY refused stdout is kept byte-for-byte as .refused.txt; Daybreak's answer is .txt" $?
+grep -qF '*** codex exited 7 ' "$T/log_R7X_after.txt" && ! grep -q 'The answer is LOST' "$T/log_R7X_after.txt" && ! grep -q 'seat answered' "$T/log_R7X_after.txt"; check "R7XL after  codex's own rc 7 with an answer: 'codex exited 7', and neither LOST nor answered" $?
 echo "CONTROLS: $pass/$total as expected"
 echo "CXLAND_CONTROLS_DONE"
 [ "$pass" = "$total" ]
```

### 3c. the mutant list, `mut_launcher_v6.py`, WHOLE (each mutant's exact edit and the controls named to kill it)

```python
     1	#!/usr/bin/env python3
     2	"""mut_launcher_v6.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-17 landing, v6) for the
     3	controls' kill table (run_mutants_v6.sh).  Each mutant names the controls expected to catch it; v5 pins every decision its
     4	CONTRACT lists, so no mutant is UNPINNED (v4's three -- m_eq1, m_sgr, m_prec -- are pinned by RC2W, CSI and RW).  The v4 list is
     5	kept whole; v5 adds one mutant per decision the v4 pass found unpinned and per decision the v5 enumeration reads off the file
     6	(run_controls_v5.sh's CONTRACT); v6 appends one per escape the v5 pass MEASURED (GLM 5.3, GPT-6 Astra, Grok 4.7, Fable 5.1)
     7	and per edge v6 rows.  m_twice inserts a line and the m_ord_* mutants MOVE one block of the exit cascade: each is
     8	still one edit.  A find-text that is absent, or present more than once, is an apparatus failure, never a silent skip."""
     9	import io, os, sys
    10	
    11	src, out = sys.argv[1], sys.argv[2]
    12	t = io.open(src, encoding="utf-8", newline="").read()
    13	#  the opening-header awk, as v3/v4 read it, so the find-text cannot drift
    14	AWK = ('HDR=$(strip_ansi "$ERR" | awk \'NR > 12 && h < 2 { exit }\n        h == 0 && /^OpenAI Codex/ { h = 1; next }\n'
    15	       '        h == 1 && /^--------/ { h = 2; next }\n        h == 2 && /^--------/ { exit }\n'
    16	       '        h == 2 { if (++n > 30) exit; print }\')')
    17	STRIP = 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }'
    18	REF = r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help'"
    19	WAL = r"grep -ic 'usage limit\|quota\|rate limit\|not authenticated'"
    20	GATE = 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then'
    21	TRIG = 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then'
    22	
    23	#  the exit cascade, cut from the launcher itself into its five blocks: refusal 7, wall 8, empty 6, identity 5, codex's rc
    24	R0 = 'if [ "$refus" -gt 0 ]; then\n    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.'
    25	W0 = 'if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED'
    26	E0 = 'if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT'
    27	I0 = 'if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then'
    28	C0 = 'if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc'
    29	C1 = 'exit "$rc"; fi\n'
    30	starts = [t.find(x) for x in (R0, W0, E0, I0, C0)]
    31	cend = t.find(C1, starts[4]) + len(C1) if starts[4] >= 0 else -1
    32	if min(starts) < 0 or cend < 0 or starts != sorted(starts) or any(t.count(x) != 1 for x in (R0, W0, E0, I0, C0)):
    33	    print("CASCADE_NOT_FOUND (starts %s)" % starts); sys.exit(1)
    34	B = dict(zip("RWEIC", [t[starts[i]:(starts[i + 1] if i < 4 else cend)] for i in range(5)]))
    35	CASCADE = "".join(B[k] for k in "RWEIC")
    36	
    37	def order(seq):
    38	    return (CASCADE, "".join(B[k] for k in seq))
    39	
    40	MUTANTS = [
    41	    #  v4's table, unchanged
    42	    ("m_anchor", "X1", "grep -a '^ERROR:'", "grep -a 'ERROR:'"),
    43	    ("m_bodyverd", "X2", GATE, 'if [ "$rc" -ne 0 ] || [ "$verd" -eq 0 ]; then'),
    44	    ("m_suffix", "X5", '[ "$RAN" != "$ANSWERED_BY" ]', '[ "${RAN##*-}" != "${ANSWERED_BY##*-}" ]'),
    45	    ("m_effort", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$1"'),
    46	    ("m_head40", "X6", AWK, 'HDR=$(strip_ansi "$ERR" | head -n 40)'),
    47	    ("m_v2awk", "X9 X10", AWK,
    48	     """HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')"""),
    49	    ("m_effortx", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$2x"'),
    50	    ("m_sandbox", "E1 E2", "--sandbox read-only", "--sandbox workspace-write"),
    51	    ("m_brief", "E1 E2", '"$(cat "$BRIEF")"', '"$BRIEF"'),
    52	    ("m_noa", "X8", "grep -a '^ERROR:'", "grep '^ERROR:'"),
    53	    ("m_nostrip", "Q3 A1 CH", STRIP, 'strip_ansi() { cat "$1" 2>/dev/null; }'),
    54	    ("m_noident", "M1 D2 X5", I0, "if false; then"),
    55	    ("m_nofallback", "D1 D2 E2", 'AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"', 'AUP_MODEL=""'),
    56	    ("m_nogate", "N1 X2", GATE, "if true; then"),
    57	    ("m_claimmodel", "M2 X6", 'echo "  seat answered -- model UNVERIFIED: no model line in an opening codex header block (requested: $ANSWERED_BY)"',
    58	     'echo "  seat answered. (answered by: $ANSWERED_BY)"'),
    59	    ("m_eq1", "RC2W", GATE, 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
    60	    ("m_sgr", "CSI", STRIP, 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
    61	    ("m_prec", "RW", "        wall=$(printf '%s' \"$CXERR\" | " + WAL + ")",
    62	     "        wall=$(printf '%s' \"$CXERR\" | " + WAL + "); [ \"$wall\" -gt 0 ] && refus=0"),
    63	    ("m_win11", "W12", "NR > 12 && h < 2", "NR > 11 && h < 2"),
    64	    ("m_win13", "W13", "NR > 12 && h < 2", "NR > 13 && h < 2"),
    65	    ("m_win3", "W12 X13", "NR > 12 && h < 2", "NR > 3 && h < 2"),
    66	    ("m_cap29", "K30", "if (++n > 30) exit", "if (++n > 29) exit"),
    67	    ("m_cap31", "K31", "if (++n > 30) exit", "if (++n > 31) exit"),
    68	    ("m_nocap", "K31", "h == 2 { if (++n > 30) exit; print }", "h == 2 { print }"),
    69	    ("m_fbeq1", "D3", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -eq 1 ] && [ -n "$AUP_MODEL" ]'),
    70	    ("m_refeq1", "R2X", 'if [ "$refus" -gt 0 ]; then\n    echo', 'if [ "$refus" -eq 1 ]; then\n    echo'),
    71	    ("m_wallgt1", "W1L", 'if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 1 ]; then'),
    72	    ("m_fbge0", "FB1", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -ge 0 ] && [ -n "$AUP_MODEL" ]'),
    73	    ("m_fbwall", "FB2", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]',
    74	     'if { [ "$refus" -gt 0 ] || [ "$wall" -gt 0 ]; } && [ -n "$AUP_MODEL" ]'),
    75	    ("m_twice", "D4 E2", '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n',
    76	     '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n'),
    77	    ("m_argv1", "X15", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 30001 ]'),
    78	    ("m_argv2", "X14", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 29999 ]'),
    79	    #  v5 -- configuration
    80	    ("m_defpath", "DP", 'Codex/bin/codex}"', 'Codex/bin/codex2}"'),
    81	    ("m_binignore", "E0b", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BINX:-'),
    82	    ("m_bincolon", "EO", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BIN-'),
    83	    ("m_modelcolon", "EO", '"${CX_MODEL:-', '"${CX_MODEL-'),
    84	    ("m_effortcolon", "EO", '"${CX_EFFORT:-', '"${CX_EFFORT-'),
    85	    ("m_aupeffcolon", "EO", '"${CX_AUP_EFFORT:-', '"${CX_AUP_EFFORT-'),
    86	    ("m_aupcolon", "FD", '"${CX_AUP_MODEL-', '"${CX_AUP_MODEL:-'),
    87	    ("m_nomkdir", "N1", 'mkdir -p "$OUT"', ': mkdir -p "$OUT"'),
    88	    ("m_txtname", "N1F", 'TXT="$OUT/codex_${TAG}.txt"', 'TXT="$OUT/codex_${TAG}.out"'),
    89	    ("m_errname", "N1F", 'ERR="$OUT/codex_${TAG}.err"', 'ERR="$OUT/codex_${TAG}.log"'),
    90	    ("m_swapio", "N1F", '> "$TXT" 2> "$ERR" < /dev/null', '> "$ERR" 2> "$TXT" < /dev/null'),
    91	    ("m_nostdin", "SI", '2> "$ERR" < /dev/null', '2> "$ERR"'),
    92	    ("m_cd", "CWD", 'cd "$PROJ" || exit 9', 'cd "$HOME" || exit 9'),
    93	    ("m_noskip", "E1", ' --skip-git-repo-check', ''),
    94	    #  v5 -- the opening header
    95	    ("m_hdrnostrip", "CH", 'HDR=$(strip_ansi "$ERR" | awk', 'HDR=$(cat "$ERR" | awk'),
    96	    ("m_hlt1", "W13", "NR > 12 && h < 2", "NR > 12 && h < 1"),
    97	    ("m_hlt3", "K30 W12", "NR > 12 && h < 2", "NR > 12 && h < 3"),
    98	    ("m_bannerun", "BA", "h == 0 && /^OpenAI Codex/", "h == 0 && /OpenAI Codex/"),
    99	    ("m_bannerh", "HB", "h == 0 && /^OpenAI Codex/", "/^OpenAI Codex/"),
   100	    ("m_rule1h", "BA", "h == 1 && /^--------/ { h = 2; next }", "/^--------/ { h = 2; next }"),
   101	    ("m_rule7a", "R7A", "h == 1 && /^--------/", "h == 1 && /^-------/"),
   102	    ("m_rule1next", "M1", "{ h = 2; next }", "{ h = 2 }"),
   103	    ("m_close2h", "BA", "h == 2 && /^--------/ { exit }", "/^--------/ { exit }"),
   104	    ("m_rule7b", "R7B", "h == 2 && /^--------/ { exit }", "h == 2 && /^-------/ { exit }"),
   105	    ("m_exitnext", "NM", "h == 2 && /^--------/ { exit }", "h == 2 && /^--------/ { next }"),
   106	    ("m_bodyh1", "R7A", "h == 2 { if (++n > 30) exit; print }", "h >= 1 { if (++n > 30) exit; print }"),
   107	    ("m_capn", "K31", "if (++n > 30) exit", "if (n++ > 30) exit"),
   108	    ("m_m2", "TM", "grep -m1 '^model:'", "grep -m2 '^model:'"),
   109	    ("m_modelanchor", "MA", "grep -m1 '^model:'", "grep -m1 'model:'"),
   110	    ("m_trailws", "WS", "s/^model:[[:space:]]*//; s/[[:space:]]*$//'", "s/^model:[[:space:]]*//'"),
   111	    ("m_leadws", "WS", "s/^model:[[:space:]]*//", "s/^model: //"),
   112	    ("m_nomodelsed", "N1", "sed 's/^model:[[:space:]]*//; s/", "sed 's/"),
   113	    #  v5 -- classification
   114	    ("m_strip_nog", "A1 CSI", '[A-Za-z]//g" "$1"', '[A-Za-z]//" "$1"'),
   115	    ("m_strip_nosemi", "CSI", '\\[[0-9;]*[A-Za-z]', '\\[[0-9]*[A-Za-z]'),
   116	    ("m_noinit", "N1", "refus=0; wall=0", ":"),
   117	    ("m_gateand", "N4 RC2W", GATE, 'if [ "$rc" -ne 0 ] && [ "$body" -eq 0 ]; then'),
   118	    ("m_gatele1", "B1G", GATE, 'if [ "$rc" -ne 0 ] || [ "$body" -le 1 ]; then'),
   119	    ("m_ref1", "P2", REF, r"grep -ic 'cannot help with\|can.t help with\|I won.t help'"),
   120	    ("m_ref2", "RF1", REF, r"grep -ic 'flagged for possible cybersecurity\|can.t help with\|I won.t help'"),
   121	    ("m_ref3", "RF2", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|I won.t help'"),
   122	    ("m_ref4", "RF3", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with'"),
   123	    ("m_refcase", "RFC", REF, REF.replace("grep -ic", "grep -c")),
   124	    ("m_wall1", "P1", WAL, r"grep -ic 'quota\|rate limit\|not authenticated'"),
   125	    ("m_wall2", "WL1", WAL, r"grep -ic 'usage limit\|rate limit\|not authenticated'"),
   126	    ("m_wall3", "WL2", WAL, r"grep -ic 'usage limit\|quota\|not authenticated'"),
   127	    ("m_wall4", "WL3", WAL, r"grep -ic 'usage limit\|quota\|rate limit'"),
   128	    ("m_wallcase", "WLC", WAL, WAL.replace("grep -ic", "grep -c")),
   129	    #  v5 -- the fallback
   130	    ("m_samemodel", "D5", TRIG, 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]; then'),
   131	    ("m_noempty", "FD", TRIG, 'if [ "$refus" -gt 0 ] && [ "$AUP_MODEL" != "$MODEL" ]; then'),
   132	    ("m_norefusedtxt", "D1R", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; ', ''),
   133	    ("m_norefusederr", "D1R", '; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"', ''),
   134	    ("m_ansby", "D1 D2", '    ANSWERED_BY="$AUP_MODEL"', '    ANSWERED_BY="$MODEL"'),
   135	    #  v5 -- the exit cascade
   136	    ("m_emptyle1", "B1E", E0, 'if [ "$body" -le 1 ]; then echo "  *** EMPTY STDOUT'),
   137	    ("m_noransep", "M2", I0, 'if [ "$RAN" != "$ANSWERED_BY" ]; then'),
   138	    ("m_zflip", "M2 N1V", 'if [ -z "$RAN" ]; then', 'if [ -n "$RAN" ]; then'),
   139	    ("m_rcpass", "RC1A RC3A", 'if [ "$rc" -ne 0 ];  then', 'if false;  then'),
   140	    ("m_rcgt1", "RC1A", 'if [ "$rc" -ne 0 ];  then', 'if [ "$rc" -gt 1 ];  then'),
   141	    ("m_rcone", "RC3A", C1, 'exit 1; fi\n'),
   142	    ("m_ord_wr", "RW",) + order("WREIC"),
   143	    ("m_ord_re", "P2",) + order("ERWIC"),
   144	    ("m_ord_ri", "RI",) + order("IRWEC"),
   145	    ("m_ord_rc", "P2",) + order("CRWEI"),
   146	    ("m_ord_we", "P1",) + order("REWIC"),
   147	    ("m_ord_wi", "WI",) + order("RIWEC"),
   148	    ("m_ord_wc", "P1",) + order("RCWEI"),
   149	    ("m_ord_ei", "EM",) + order("RWIEC"),
   150	    ("m_ord_ec", "X1",) + order("RWCEI"),
   151	    ("m_ord_ic", "IR",) + order("RWECI"),
   152	    #  v5 -- the log phrases a caller reads
   153	    ("m_msganswered", "PK", 'echo "  seat answered. (answered by:', 'echo "  seat replied. (answered by:'),
   154	    ("m_msganswered2", "PK", 'echo "  seat answered -- model UNVERIFIED', 'echo "  seat replied -- model UNVERIFIED'),
   155	    ("m_msglost", "PK", "The answer is LOST, whatever", "The answer is gone, whatever"),
   156	    ("m_msgby", "PK N1V", "(answered by: $ANSWERED_BY)", "(by: $ANSWERED_BY)"),
   157	    ("m_rcline", "LOG", 'echo "codex rc=$rc   stdout=', 'echo "codex rc=$rc stdout='),
   158	    #  v6 -- each override's VALUE (GLM 5.3, GPT-6 Astra, Fable 5.1: each escaped 94/94, measured)
   159	    ("m_effortfix", "OVA", '\nEFFORT="${CX_EFFORT:-ultra}"', '\nEFFORT=ultra'),
   160	    ("m_aupeffortfix", "OVA", 'AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"', 'AUP_EFFORT=ultra'),
   161	    ("m_aupcalleff", "OVA", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex "$AUP_MODEL" "$EFFORT"; classify'),
   162	    ("m_mainmodelfix", "OVA", 'run_codex "$MODEL" "$EFFORT"; classify', 'run_codex gpt-6-astra "$EFFORT"; classify'),
   163	    ("m_aupmodelfix", "OV OVA", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex gpt-daybreak-blue-latest "$AUP_EFFORT"; classify'),
   164	    #  v6 -- the fallback's own rc (GPT-6 Astra)
   165	    ("m_fbrc", "FR", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; rc=$?; classify'),
   166	    #  v6 -- a used out dir, a missing parent, a non-empty refused stdout (all four seats; GLM 5.3; GPT-6 Astra)
   167	    ("m_append", "RSF", '"$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null', '"$(cat "$BRIEF")" >> "$TXT" 2> "$ERR" < /dev/null'),
   168	    ("m_appenderr", "RS RSF", '"$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null', '"$(cat "$BRIEF")" > "$TXT" 2>> "$ERR" < /dev/null'),
   169	    ("m_mkdirnop", "MP MPF", 'mkdir -p "$OUT"', 'mkdir "$OUT"'),
   170	    ("m_refusedempty", "RNF", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt";', ': > "$OUT/codex_${TAG}.refused.txt";'),
   171	    #  v6 -- the opening header: the rules' anchors at both ends, the banner's text, the trims' `*' (GPT-6 Astra, GLM 5.3, Grok 4.7)
   172	    ("m_rule1unanch", "SP1", "h == 1 && /^--------/ { h = 2; next }", "h == 1 && /--------/ { h = 2; next }"),
   173	    ("m_rule2unanch", "SP2", "h == 2 && /^--------/ { exit }", "h == 2 && /--------/ { exit }"),
   174	    ("m_rule1end", "R9A", "h == 1 && /^--------/ { h = 2; next }", "h == 1 && /^--------$/ { h = 2; next }"),
   175	    ("m_rule2end", "R9B", "h == 2 && /^--------/ { exit }", "h == 2 && /^--------$/ { exit }"),
   176	    ("m_bannercodex", "BN WMT", "h == 0 && /^OpenAI Codex/", "h == 0 && /^OpenAI/"),
   177	    ("m_ws1", "WZ WMT", "s/^model:[[:space:]]*//", "s/^model:[[:space:]][[:space:]]*//"),
   178	    #  v6 -- a parameterless CSI (GPT-6 Astra)
   179	    ("m_csi1", "CZ", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-9;][0-9;]*[A-Za-z]")),
   180	    #  v6 -- the phrases and numbers a caller reads (GPT-6 Astra: status.sh reads SEAT WALLED; LOG read the format only)
   181	    ("m_wallmsg", "PK", '*** SEAT WALLED ($ANSWERED_BY).', '*** SEAT BLOCKED ($ANSWERED_BY).'),
   182	    ("m_stdoutcnt", "LOG", 'stdout=$(wc -c < "$TXT") b', 'stdout=$(wc -c < "$ERR") b'),
   183	    ("m_stderrcnt", "LOG", 'stderr=$(wc -c < "$ERR") b', 'stderr=$(wc -c < "$TXT") b'),
   184	    ("m_logrc", "LOG", 'echo "codex rc=$rc   stdout=', 'echo "codex rc=0   stdout='),
   185	    ("m_lost7", "R7XL", R0, R0.replace('if [ "$refus" -gt 0 ]; then', 'if [ "$refus" -gt 0 ] || [ "$rc" -eq 7 ]; then')),
   186	    #  v6 -- Fable 5.1's v5-pass escapes in the forms the list above lacked (each measured 94/94 on the v5 controls)
   187	    ("m_effortignore", "OVA", '"${CX_EFFORT:-ultra}"', '"${CX_EFFORTX:-ultra}"'),
   188	    ("m_aupeffignore", "OVA", '"${CX_AUP_EFFORT:-ultra}"', '"${CX_AUP_EFFORTX:-ultra}"'),
   189	    ("m_effortglobal", "OVA", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$EFFORT"'),
   190	    ("m_ansbyhard", "OV OVA", '    ANSWERED_BY="$AUP_MODEL"', '    ANSWERED_BY=gpt-daybreak-blue-latest'),
   191	    ("m_askedglobal", "LOG", 'asked: $1 / $2"', 'asked: $MODEL / $EFFORT"'),
   192	    ("m_stripplus", "CZ", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-9;]\\{1,\\}[A-Za-z]")),
   193	]
   194	os.makedirs(out, exist_ok=True)
   195	bad = 0
   196	names = set()
   197	with io.open(os.path.join(out, "MUTANTS.list"), "w", encoding="utf-8", newline="\n") as lst:
   198	    for name, catches, find, repl in MUTANTS:
   199	        n = t.count(find)
   200	        if n != 1 or name in names or find == repl:
   201	            print("MUTANT_TEXT_NOT_FOUND %s (found %d)" % (name, n)); bad += 1; continue
   202	        names.add(name)
   203	        io.open(os.path.join(out, name + ".sh"), "w", encoding="utf-8", newline="").write(t.replace(find, repl))
   204	        lst.write("%s\t%s\n" % (name, catches))
   205	print("mutants written: %d of %d" % (len(MUTANTS) - bad, len(MUTANTS)))
   206	sys.exit(1 if bad else 0)
```

### 3d. the censuses: `CENSUS_v5.txt`, `v5pass/RULELEN_CENSUS.txt`, `v5pass/SEMISGR_WHERE.txt`

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

files read: 2427
lengths of lines opening with 8 dashes, in the first 42 lines: [(8, 1954)]
files with such a line longer than 8 or carrying other text: 0
RULELEN_CENSUS_DONE

files: 44
    1  GXEMUL-SEC\_scratchpad\panel_514p5_20260908
    1  GXEMUL-SEC\_scratchpad\panel_514p6_20260908
    1  _scratchpad\w544\out_FIX_C9_combined_sgr
    1  _scratchpad\w544\out_HEAD_C9_combined_sgr
    1  _scratchpad\w544\out_MUTNOANCHOR_C9_combined_sgr
    1  _scratchpad\w544\out_MUTNOA_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_dashlws_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_dashnospace_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_dashtws_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_floor35_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_floor65_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_lead80_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_letteronly_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noanchor_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noa_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nocase_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nodash_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noemdash_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noemph_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noendash_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nofinalonly_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nofinal_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nofloor_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nogate_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nohat_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nohyphen_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nolead_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noletter_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nonum_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nooverall_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noprecedence_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noprefix_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_norc_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_noseat_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nosep_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nosgr_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_nowalltxt_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_numprefix2_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_sgrnoparam_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_v4regex_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_valueany_C9_combined_sgr
    1  _scratchpad\w544\out_MUT_walltxt_C9_combined_sgr
    1  _scratchpad\w544_review_mine\out_FIX2_C9_combined_sgr
    1  _scratchpad\w544_review_mine\out_HEAD2_C9_combined_sgr
non-w544 files:
  GXEMUL-SEC\_scratchpad\panel_514p5_20260908\codex.err  line 1581  col0 False  '\x1b[34;1mGXemul> \x1b[0m... and no ^GXemul> anchor matches.  I ha'
  GXEMUL-SEC\_scratchpad\panel_514p6_20260908\codex.err  line 1650  col0 False  '\x1b[34;1mGXemul> \x1b[0m... and no ^GXemul> anchor matches.  I ha'
w544 lines of first match: [(1, 42)]
SEMISGR_WHERE_DONE
```

### 3e. `v5pass/main_meas.txt` -- the v5 pass's claimed escapes, MEASURED on the v5 controls before v6 was built

```
wrote 18 mutants
# claimed-escape measurement: launcher af18158e, controls 12effca6, 2026-10-17 04:14:02
g_append         94/94    sentinel=1  ESCAPES (passes every after check)
g_appenderr      94/94    sentinel=1  ESCAPES (passes every after check)
g_effort         94/94    sentinel=1  ESCAPES (passes every after check)
g_aupeffort      94/94    sentinel=1  ESCAPES (passes every after check)
g_aupcall        94/94    sentinel=1  ESCAPES (passes every after check)
g_banner         94/94    sentinel=1  ESCAPES (passes every after check)
g_mkdirp         94/94    sentinel=1  ESCAPES (passes every after check)
g_mvf            94/94    sentinel=1  ESCAPES (passes every after check)
a_mainmodel      94/94    sentinel=1  ESCAPES (passes every after check)
a_aupmodel       94/94    sentinel=1  ESCAPES (passes every after check)
a_fbrc           94/94    sentinel=1  ESCAPES (passes every after check)
a_refusedempty   94/94    sentinel=1  ESCAPES (passes every after check)
a_rule1anchor    94/94    sentinel=1  ESCAPES (passes every after check)
a_rule2anchor    94/94    sentinel=1  ESCAPES (passes every after check)
a_csi1           94/94    sentinel=1  ESCAPES (passes every after check)
a_ws0            94/94    sentinel=1  ESCAPES (passes every after check)
a_wallmsg        94/94    sentinel=1  ESCAPES (passes every after check)
a_stdoutcnt      94/94    sentinel=1  ESCAPES (passes every after check)
frozen copy removed (cmp clean)
MEAS_V5PASS_DONE
```

## 4. The receipts

### 4a. `RECEIPT_v6.txt` -- the AFTER rows and every content check (the tracked and before rows, which record the old
files, and the indented per-run output are in the file; the new rows' tracked and before values were recorded by
`RECEIPT_v6_calibration.txt`, every after expectation written first)

```
# controls md5 c87796c04c1343a16156281e47b76d09
# cxlaunch landing controls (v6), 2026-10-17 05:10:07
# tracked: cb180d9d58da2c0b05defe48c65b7ad0  cxlaunch_tracked.sh
# before:  3c51a7579065c5e6bebd5fd59d32b3ed  cxlaunch_before.sh
# after:   c53b99abf57f7faf8aadfe2a89294af6  /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh
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
OV   after   exit=0   want=0   ok
FR   after   exit=3   want=3   ok
RS   after   exit=0   want=0   ok
MP   after   exit=0   want=0   ok
RN   after   exit=0   want=0   ok
SP1  after   exit=5   want=5   ok
SP2  after   exit=5   want=5   ok
CZ   after   exit=7   want=7   ok
WZ   after   exit=0   want=0   ok
R7X  after   exit=7   want=7   ok
BN   after   exit=0   want=0   ok
R9A  after   exit=5   want=5   ok
R9B  after   exit=0   want=0   ok
E0  all  the fake codex was reached by every run but X15's, and by none of X15's (78 rows x 3 = 234 of 234, pinned)  ok
E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of 78)  ok
SI  after  no after run's codex read the stdin the launcher was fed (77 runs that reached codex, of 77)  ok
CWD after  every after run's codex started in the project root (77 of 77)  ok
FD  after  every row that sets CX_AUP_MODEL empty made exactly one call (66 rows, 66 pinned)  ok
PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff the refusal exit 7, 'SEAT WALLED' iff exit 8, 'answered by:' iff a verified exit 0 (78 runs)  ok
LOG after  the 'codex rc=N   stdout=N b   stderr=N b   asked: M / E' lines of N1, D1 (both calls) and RC3A, WHOLE: the format the censuses parse and each number the fixture's own  ok
N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr  ok
N1V after  N1 is credited to gpt-6-astra  ok
WMT after  WS, MA, TM, WZ and BN verify gpt-6-astra (not UNVERIFIED)  ok
M2  after  says model UNVERIFIED and names no model  ok
X6  after  says model UNVERIFIED and names no model  ok
X9  after  says model UNVERIFIED and names no model  ok
W13  after  says model UNVERIFIED and names no model  ok
K31  after  says model UNVERIFIED and names no model  ok
NM  after  says model UNVERIFIED and names no model  ok
HB  after  says model UNVERIFIED and names no model  ok
R9B  after  says model UNVERIFIED and names no model  ok
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
OVA after  CX_MODEL, CX_EFFORT, CX_AUP_MODEL, CX_AUP_EFFORT set to NON-default values: each reaches its own call, both compared whole; the fallback credited  ok
RSF after  a re-run into a dir holding a stale answer and a stale header: both files TRUNCATED, byte-for-byte the new run's  ok
MPF after  an out dir two levels below a missing parent is created, and the run lands in it  ok
RNF after  a NON-EMPTY refused stdout is kept byte-for-byte as .refused.txt; Daybreak's answer is .txt  ok
R7XL after  codex's own rc 7 with an answer: 'codex exited 7', and neither LOST nor answered  ok
CONTROLS: 269/269 as expected
CXLAND_CONTROLS_DONE
```

### 4b. `KILLTABLE_v6.txt`, whole (`run_mutants_v6.sh`: each mutant through the after column; the base run is all three)

```
# controls md5 c87796c04c1343a16156281e47b76d09
# driver md5 9ce15b2d491f37fb7d65eb8578df4358
mutants written: 133 of 133
# kill table for /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh (c53b99abf57f7faf8aadfe2a89294af6), 2026-10-17 05:13:25, 2 at a time; controls c87796c04c1343a16156281e47b76d09
BASE      CONTROLS: 269/269 as expected
BASE      78 rows; a mutant's after-only run must total 113
RERUN     m_nomkdir (the flake signature in its first run)
RERUN     m_fbrc (the flake signature in its first run)
RERUN     m_append (the flake signature in its first run)
RERUN     m_mkdirnop (the flake signature in its first run)
m_anchor        112/113  killed by: X1                                                  [X1]
m_bodyverd      111/113  killed by: B1G X2                                              [X2]
m_suffix        112/113  killed by: X5                                                  [X5]
m_effort        108/113  killed by: DP E1 E2 EO OVA                                     [E1 E2]
m_head40        95/113   killed by: BA BN HB K31 NM R7A R9B W13 WMT X10 X6 X9           [X6]
m_v2awk         105/113  killed by: HB K31 W13 X10 X9                                   [X9 X10]
m_effortx       108/113  killed by: DP E1 E2 EO OVA                                     [E1 E2]
m_sandbox       108/113  killed by: DP E1 E2 EO OVA                                     [E1 E2]
m_brief         108/113  killed by: DP E1 E2 EO OVA                                     [E1 E2]
m_noa           112/113  killed by: X8                                                  [X8]
m_nostrip       104/113  killed by: A1 CH CSI CZ D3 Q3 R2X                              [Q3 A1 CH]
m_noident       99/113   killed by: BA CH D2 IR K30 M1 R7B R9A SP1 SP2 W12 X13 X5       [M1 D2 X5]
m_nofallback    98/113   killed by: D1 D1R D2 D3 D4 E2 EO FR LOG OV OVA RN RNF          [D1 D2 E2]
m_nogate        106/113  killed by: B1G FB1 M1 N1 N1V X2 X5                             [N1 X2]
m_claimmodel    105/113  killed by: HB K31 M2 NM R9B W13 X6 X9                          [M2 X6]
m_eq1           112/113  killed by: RC2W                                                [RC2W]
m_sgr           112/113  killed by: CSI                                                 [CSI]
m_prec          112/113  killed by: RW                                                  [RW]
m_win11         112/113  killed by: W12                                                 [W12]
m_win13         111/113  killed by: W13                                                 [W13]
m_win3          109/113  killed by: BA W12 WMT X13                                      [W12 X13]
m_cap29         112/113  killed by: K30                                                 [K30]
m_cap31         111/113  killed by: K31                                                 [K31]
m_nocap         111/113  killed by: K31                                                 [K31]
m_fbeq1         111/113  killed by: D3                                                  [D3]
m_refeq1        112/113  killed by: R2X                                                 [R2X]
m_wallgt1       107/113  killed by: W1L WI WL1 WL2 WL3 WLC                              [W1L]
m_fbge0         110/113  killed by: FB1 FB2                                             [FB1]
m_fbwall        112/113  killed by: FB2                                                 [FB2]
m_twice         107/113  killed by: D3 D4 E2 EO LOG OVA                                 [D4 E2]
m_argv1         108/113  killed by: CWD E0 SI X15                                       [X15]
m_argv2         108/113  killed by: CWD E0 FD SI X14                                    [X14]
m_defpath       104/113  killed by: CWD DP E0 E0b EO FD SI                              [DP]
m_binignore     112/113  killed by: E0b                                                 [E0b]
m_bincolon      107/113  killed by: CWD E0 E0b EO SI                                    [EO]
m_modelcolon    112/113  killed by: EO                                                  [EO]
m_effortcolon   112/113  killed by: EO                                                  [EO]
m_aupeffcolon   112/113  killed by: EO                                                  [EO]
m_aupcolon      112/113  killed by: FD                                                  [FD]
m_nomkdir       6/113    killed by: A1 B1E B1G BA BN CH CSI CWD CZ D1 D1R D2 D3 D4 D5 DP E0 E0b E1 E2 EM EO FB1 FB2 FD FR HB IR K30 K31 LOG M1 M2 MA MP MPF N1 N1F N1V N2 N3 N4 NM OV OVA P1 P2 Q1 Q2 Q3 R2X R7A R7B R7X R7XL R9A R9B RC2W RC3A RF1 RF2 RF3 RFC RI RN RNF RW SI SP1 SP2 TM W12 W13 W1L WI WL1 WL2 WL3 WLC WMT WS WZ X1 X10 X13 X14 X2 X5 X6 X8 X9  [N1]
m_txtname       108/113  killed by: D1R MPF N1F RNF RSF                                 [N1F]
m_errname       109/113  killed by: D1R MPF N1F RSF                                     [N1F]
m_swapio        48/113   killed by: A1 BA CH CSI CZ D1 D1R D2 D3 D4 D5 E2 EM EO FB2 FR IR K30 LOG M1 M2 MPF N1F N1V N2 N4 OV OVA P1 P2 Q1 Q2 Q3 R2X R7B R9A RC2W RF1 RF2 RF3 RFC RI RN RNF RSF RW SP1 SP2 W12 W1L WI WL1 WL2 WL3 WLC WMT X1 X13 X5 X8  [N1F]
m_nostdin       112/113  killed by: SI                                                  [SI]
m_cd            112/113  killed by: CWD                                                 [CWD]
m_noskip        108/113  killed by: DP E1 E2 EO OVA                                     [E1]
m_hdrnostrip    111/113  killed by: CH                                                  [CH]
m_hlt1          111/113  killed by: W13                                                 [W13]
m_hlt3          111/113  killed by: K30 W12                                             [K30 W12]
m_bannerun      112/113  killed by: BA                                                  [BA]
m_bannerh       111/113  killed by: HB                                                  [HB]
m_rule1h        104/113  killed by: BA BN HB NM R9B WMT                                 [BA]
m_rule7a        112/113  killed by: R7A                                                 [R7A]
m_rule1next     94/113   killed by: BA CH D1R D2 D3 IR K30 M1 N1V OVA R7B R9A SP1 SP2 W12 WMT X13 X5  [M1]
m_close2h       111/113  killed by: BA WMT                                              [BA]
m_rule7b        112/113  killed by: R7B                                                 [R7B]
m_exitnext      107/113  killed by: HB NM R9B                                           [NM]
m_bodyh1        112/113  killed by: R7A                                                 [R7A]
m_capn          111/113  killed by: K31                                                 [K31]
m_m2            111/113  killed by: TM WMT                                              [TM]
m_modelanchor   111/113  killed by: MA WMT                                              [MA]
m_trailws       111/113  killed by: WMT WS                                              [WS]
m_leadws        110/113  killed by: WMT WS WZ                                           [WS]
m_nomodelsed    84/113   killed by: B1E BN CH D1 D1R D3 DP EO FB1 FR MA MP N1 N1V OV OVA R7A R7X R7XL RC1A RC3A RN RS TM WMT WS WZ X14  [N1]
m_strip_nog     106/113  killed by: A1 CH CSI D3 Q3 R2X                                 [A1 CSI]
m_strip_nosemi  112/113  killed by: CSI                                                 [CSI]
m_noinit        57/113   killed by: B1E B1G BA BN CH D1 D1R D2 D3 DP EO FB1 HB K30 K31 M1 M2 MA MP N1 N1V N2 NM OV OVA R7A R7B R9A R9B RN RS SP1 SP2 TM W12 W13 WMT WS WZ X10 X13 X14 X2 X5 X6 X9  [N1]
m_gateand       108/113  killed by: N4 Q2 RC2W RN RNF                                   [N4 RC2W]
m_gatele1       112/113  killed by: B1G                                                 [B1G]
m_ref1          87/113   killed by: A1 CSI CZ D1 D1R D2 D3 D4 D5 E2 EO FR LOG OV OVA P2 Q1 R2X RFC RI RN RNF RW  [P2]
m_ref2          112/113  killed by: RF1                                                 [RF1]
m_ref3          112/113  killed by: RF2                                                 [RF2]
m_ref4          112/113  killed by: RF3                                                 [RF3]
m_refcase       112/113  killed by: RFC                                                 [RFC]
m_wall1         103/113  killed by: FB2 N4 P1 Q2 Q3 RC2W W1L WI WLC X8                  [P1]
m_wall2         112/113  killed by: WL1                                                 [WL1]
m_wall3         112/113  killed by: WL2                                                 [WL2]
m_wall4         112/113  killed by: WL3                                                 [WL3]
m_wallcase      112/113  killed by: WLC                                                 [WLC]
m_samemodel     112/113  killed by: D5                                                  [D5]
m_noempty       112/113  killed by: FD                                                  [FD]
m_norefusedtxt  111/113  killed by: D1R RNF                                             [D1R]
m_norefusederr  111/113  killed by: D1R RNF                                             [D1R]
m_ansby         103/113  killed by: D1 D1R D2 D3 EO FR OV OVA RN                        [D1 D2]
m_emptyle1      111/113  killed by: B1E B1G                                             [B1E]
m_noransep      93/113   killed by: B1G HB K31 M2 N2 NM R9B W13 X10 X2 X6 X9            [M2]
m_zflip         100/113  killed by: D1R D3 HB K31 M2 N1V NM OVA R9B W13 WMT X6 X9       [M2 N1V]
m_rcpass        108/113  killed by: FR R7X R7XL RC1A RC3A                               [RC1A RC3A]
m_rcgt1         112/113  killed by: RC1A                                                [RC1A]
m_rcone         110/113  killed by: FR R7X RC3A                                         [RC3A]
m_ord_wr        112/113  killed by: RW                                                  [RW]
m_ord_re        88/113   killed by: A1 CSI CZ D4 D5 FB2 P1 P2 Q1 Q2 Q3 R2X RF1 RF2 RF3 RFC RI RW W1L WI WL1 WL2 WL3 WLC X8  [P2]
m_ord_ri        110/113  killed by: EM RI WI                                            [RI]
m_ord_rc        85/113   killed by: A1 CSI CZ D4 D5 FB2 IR N4 P1 P2 Q1 Q3 R2X RC2W RF1 RF2 RF3 RFC RI RW W1L WI WL1 WL2 WL3 WLC X1 X8  [P2]
m_ord_we        102/113  killed by: FB2 P1 Q2 Q3 W1L WI WL1 WL2 WL3 WLC X8              [P1]
m_ord_wi        111/113  killed by: EM WI                                               [WI]
m_ord_wc        99/113   killed by: FB2 IR N4 P1 Q3 RC2W W1L WI WL1 WL2 WL3 WLC X1 X8   [P1]
m_ord_ei        112/113  killed by: EM                                                  [EM]
m_ord_ec        111/113  killed by: IR X1                                               [X1]
m_ord_ic        112/113  killed by: IR                                                  [IR]
m_msganswered   109/113  killed by: N1V OVA PK WMT                                      [PK]
m_msganswered2  112/113  killed by: PK                                                  [PK]
m_msglost       112/113  killed by: PK                                                  [PK]
m_msgby         107/113  killed by: D1R D3 N1V OVA PK WMT                               [PK N1V]
m_rcline        112/113  killed by: LOG                                                 [LOG]
m_effortfix     112/113  killed by: OVA                                                 [OVA]
m_aupeffortfix  112/113  killed by: OVA                                                 [OVA]
m_aupcalleff    112/113  killed by: OVA                                                 [OVA]
m_mainmodelfix  112/113  killed by: OVA                                                 [OVA]
m_aupmodelfix   111/113  killed by: OV OVA                                              [OV OVA]
m_fbrc          112/113  killed by: FR                                                  [FR]
m_append        112/113  killed by: RSF                                                 [RSF]
m_appenderr     111/113  killed by: RS RSF                                              [RS RSF]
m_mkdirnop      107/113  killed by: CWD E0 FD MP MPF SI                                 [MP MPF]
m_refusedempty  112/113  killed by: RNF                                                 [RNF]
m_rule1unanch   112/113  killed by: SP1                                                 [SP1]
m_rule2unanch   112/113  killed by: SP2                                                 [SP2]
m_rule1end      112/113  killed by: R9A                                                 [R9A]
m_rule2end      111/113  killed by: R9B                                                 [R9B]
m_bannercodex   111/113  killed by: BN WMT                                              [BN WMT]
m_ws1           111/113  killed by: WMT WZ                                              [WZ WMT]
m_csi1          112/113  killed by: CZ                                                  [CZ]
m_wallmsg       112/113  killed by: PK                                                  [PK]
m_stdoutcnt     112/113  killed by: LOG                                                 [LOG]
m_stderrcnt     112/113  killed by: LOG                                                 [LOG]
m_logrc         112/113  killed by: LOG                                                 [LOG]
m_lost7         112/113  killed by: R7XL                                                [R7XL]
m_effortignore  112/113  killed by: OVA                                                 [OVA]
m_aupeffignore  112/113  killed by: OVA                                                 [OVA]
m_effortglobal  112/113  killed by: OVA                                                 [OVA]
m_ansbyhard     111/113  killed by: OV OVA                                              [OV OVA]
m_askedglobal   112/113  killed by: LOG                                                 [LOG]
m_stripplus     112/113  killed by: CZ                                                  [CZ]
KILL TABLE: 133/133 as recorded
CXLAND_MUTANTS_DONE
```

## 5. The records this landing writes AT COMMIT (previews against HEAD)

### 5a. OUTSTANDING_BUGS.md

```diff
--- OUTSTANDING_BUGS.md@HEAD
+++ OUTSTANDING_BUGS.md@preview
@@ -16561,6 +16561,12 @@
 
 `tools/cxlaunch.sh` anchors stderr tests on codex's own `^ERROR:` lines and greps stdout freely;
 exit 7 refusal, 8 wall, 6 empty-with-neither, else `rc`. Controlled in four states.
+*[2026-10-17, the `cxlaunchquotation` landing: the two lines above are kept as written and are NO LONGER TRUE -- "greps
+stdout freely" was the very defect `cxlaunchquotation` was filed for.  The landed file classifies codex's `^ERROR:` lines
+(ANSI-stripped, read with `grep -a`) ONLY when rc != 0 or stdout is empty, never greps stdout for wall words, re-runs a
+refused brief once on Daybreak, and exits 5 when codex's OPENING header block names a different model -- tested after
+the refusal, wall and empty-stdout checks, on the run that answered (a refused first run's header is not compared).
+Controls: `regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt`.]*
 
 *`panel.sh` already had a better, POSITION-based discriminator (head/tail 400 bytes) with the
 incident that taught it recorded in its own comment. A claim here that it did not was false and is
@@ -22068,6 +22074,17 @@
 Four heredoc-written briefs came out 0 bytes and were launched (2026-09-19 01:25).  Refuse `sz < 200`; require a verdict
 line.  Its wall detector also missed a walled job whose multi-MB `.err` carried NUL bytes: `grep` called it BINARY and
 dropped the usage-limit lines (the peer session's `grep -a` diagnosis, #544 control C18).  Joins #544.
+*[2026-10-17, the `tools/cxlaunch.sh` landing: the NUL half above is CLOSED -- the landed file reads stderr with `grep
+-a` (controls X8, a real NUL-bearing wall: 6 -> 8).  The empty-brief half is OPEN and gains a second road, measured on
+the landing's v5 pass (Fable 5.1, with the fake codex): a MISSING or RELATIVE brief also reaches codex as an EMPTY
+prompt -- the launcher reads the brief after `cd "$PROJ"` and checks neither its existence nor its size -- and a codex
+that answers is reported `seat answered`, exit 0.  On 2026-10-17 a relative launch, the main loop's own, exited 1 only
+because codex refused the empty prompt.  A relative OUT dir breaks too (`mkdir` in the caller's directory, the files
+after the `cd`).  Every caller in the tree passes absolute paths, and the pack runner skips a missing brief.  The FIX
+is `#544`'s -- the peer session's round (e8a2bc), in work since 2026-09-19 and staged in `_scratchpad/w544/` (a 64-byte
+floor and a verdict-line gate) -- and it now rebases on the landed file.  Offered to it (Fable 5.1): reading the brief
+BEFORE the `cd` into a variable and refusing an empty one, `BODY=$(cat "$BRIEF") && [ -n "$BODY" ] || exit 9`,
+closes the missing and relative roads with the empty one; a `case` on `/*|?:*` resolves a relative OUT.]*
 
 ### `brieftplstale` (LOW, records; never-commit file) — the template's tree warning names copies that do not exist
 `./src/` and `_archive/` copies of `dev_footbridge.c` are absent; `_scratchpad/r6pass2_fb/` (744-line stale fork copy)
@@ -22509,6 +22526,10 @@
 tool that reads it).  Fix shape: key the stderr test on codex's own error block at the END of the stream, and give the
 stdout patterns word boundaries; negative-control both directions (a real wall still reds; these two runs do not).
 Found while confirming `#550`.
+**MERGED 2026-10-17 into the `cxlaunchquotation` landing, with its fix shape WITHDRAWN** (the three-seat ruling,
+regress/artifacts/adj_20261016/RULINGS_C_records.md F1): keying on codex's LAST `ERROR:` line does not work -- in fixture
+N4 that line is itself a quotation -- so the landed rule keys on the exit status and an empty stdout instead.  This filing
+never had a ledger row; both of its false positives are controlled in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt` (N1, N2).
 
 ## 2026-09-25 — GXEMUL [087a90]: `#551` wdcidselfcheck; what its review files
 
@@ -24674,6 +24695,12 @@
 once".  The fallback the owner ruled (2026-10-01: `gpt-daybreak-blue-latest` on an Astra AUP refusal) exists only in
 `_scratchpad/codexpack_20260928/cxlaunch_pack.run-*.sh`.  Fix: give `cxlaunch.sh` the pack runner's fallback, and
 correct the comment when `panel.sh` is next reviewed (it carries unreviewed deltas).
+**CLOSED 2026-10-17** (the landing; the heading above is kept as written -- it was true of the tracked file until then).
+The fallback is controlled in `regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt` by D1, D2, D3 (a real doubled refusal) and D4 (fires ONCE on a second
+refusal), by FB1/FB2 (it does not fire on an answer or a wall), and by E1/E2 (the exact arguments of both calls); the
+real-run receipt of it firing is `regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log`.
+The working-tree `panel.sh` already carries the corrected comment beside `CODEX_EFFORT`, uncommitted with that file's
+other unreviewed deltas; HEAD's `panel.sh` does not yet.
 
 ### 2026-10-09 -- `ppcrlwhighhalf` / `ppcwitnessmaskoracle`: the oracle repair committed alone, the rung-3 witness on committed HEAD
 
@@ -24722,6 +24749,10 @@
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
+  **CLOSED 2026-10-17 by the landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F1): stdout is
+  never grepped for wall words; codex's `^ERROR:` lines are classified only when rc != 0 or stdout is empty.  The tracked
+  file the landing replaced exits 8 on N1 (a captured real answer whose stderr quotes a codex wall line) and N2 (a
+  synthetic answer carrying the four wall words), and the landed one 0 (`regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt`).
 * **`fablequeueregress` (MEDIUM, open)** gains Fable 5.1's stagetokens finding 5: section I's regress guarantee is
   narrower than its docstring -- precommit I2 (the codex wall), not I, forces a held regress review into the queue.
 
@@ -24761,3 +24792,16 @@
   supervisor trap in a slot naming a residual vector (11..113, 116..127) or 114/115 -- is unrowed.  `&& !(cpu->delay_slot
   && is_trap)` at :799 is a PREDICTED 84/84 escape, not measured (Fable 5.1, pass 16, `pass16/fable5_m88kp16.md` section
   4).  Pin if ever rowed: `residtbdslot` = `[BR_N_PLUS16, TB1_0_R3_50]`, r3 = 1, expected HALT naming 0x032.
+
+### 2026-10-17 -- the codex launcher landed in `tools/cxlaunch.sh` (`cxlaunchquotation`, `cxlaunchdaybreak` closed)
+
+* No row filed.  The relative-path defect the v5 pass ruled disclose-and-FILE (GPT-6 Astra, GLM 5.3, Grok 4.7, Fable
+  5.1) is FILED ON `cxlaunchempty` -- a missing or relative brief reaches codex as an EMPTY prompt, that row's defect by
+  a second road (Fable 5.1, measured); see the bracket under its entry, which also records its NUL half closed (X8).
+* The three one-edit escapes pass 2 left UNPINNED BY RULING -- `-ne 0` -> `-eq 1` in the classify gate, the ANSI strip
+  narrowed to SGR, refusal-before-wall precedence -- are pinned (rows RC2W, CSI, RW of `regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt`), with
+  every other decision of the file: its controls' CONTRACT is derived from the file (v5) and rows each decision's
+  generating set (v6) -- every override's VALUE at its own call, a re-run into a used out dir, a missing parent, a
+  non-empty refused stdout, both ends of each rule pattern, a parameterless CSI, the caller-read phrases re-derived by
+  grep (status.sh counts `SEAT WALLED`) and the `codex rc=` line's numbers -- each pinned or disclosed with its reason
+  (`regress/artifacts/cxlaunchland_20261016/KILLTABLE_v6.txt`; `regress/artifacts/cxlaunchland_20261016/CENSUS_v5.txt` names the on-record count behind each synthetic row).
```

### 5b. the ledger rows

```
# ledger changes the tools/cxlaunch.sh landing makes, against HEAD (a preview; applied at commit)

== cxlaunchdaybreak 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the same landing: a content-filter refusal on Astra is re-run ONCE on gpt-daybreak-blue-latest, the refused run kept as .refused.*, the answer credited to Daybreak; it does not fire on an answer or a wall, nor on a refusal asked of Daybreak itself, nor with the fallback set empty (D1-D5, D1R, FB1, FB2, FD, E1, E2, OVA, FR, RNF in RECEIPT_v6.txt; the real-run receipt is codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchdaybreak closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr), the v4 edge rows (W12/W13, K30/K31, R2X/D3, W1L, FB1/FB2, X14/X15) and the v5 rows (RC1A/RC3A codex's own rc, D5, FD, CH, SI, N1F, D1R, DP/EO/E0b, the alternatives RF1-RF3/WL1-WL3/RFC/WLC, the cascade pairs RW/RI/WI/EM/IR, the awk guards HB/BA/R7A/R7B/NM/TM/MA/WS, PK and LOG) and the v6 rows (OV/OVA each override's value at its own call, FR the fallback's own rc, RS/RSF a used out dir, MP/MPF a missing parent, RN/RNF a non-empty refused stdout, SP1/SP2 and R9A/R9B the rule patterns' two ends, BN, CZ, WZ, R7X/R7XL codex's own rc 7, PK's SEAT WALLED, LOG's numbers) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v6.txt still kill every one of its mutants as named?  Is the record (the launcher's header, the controls' CONTRACT, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt -- D1: the tracked launcher exits 7 on a refusal (no fallback), the landed one re-runs it once on gpt-daybreak-blue-latest and credits Daybreak (exit 0); D3 (a real doubled refusal), D4 (exactly two calls on a second refusal), FB1/FB2 (no re-run on an answer or a wall) and E1/E2 (both calls' exact arguments) pin it; the real-run receipt is regress/artifacts/codexpack_20260928/dossier_gdromdma/dossier_gdromdma.launch.log"

== cxlaunchempty 
  state_note: "[2026-09-19 06:2x] Joined #544 (e8a2bc): the 64-byte floor and the verdict-line gate close the empty brief; `grep -a' closes the NUL-byte wall miss (control C18 replays the real stderr).  \n\n[2026-10-17] the tools/cxlaunch.sh landing CLOSES this row's NUL half (grep -a; controls X8, a real NUL-bearing wall, 6 -> 8) and leaves its empty-brief half OPEN, with a second road measured on the landing's v5 pass (Fable 5.1, with the fake codex): a MISSING or RELATIVE brief reaches codex as an EMPTY prompt -- the launcher reads it after cd \"$PROJ\" and checks neither existence nor size -- and an answer to it is reported 'seat answered', exit 0; the 2026-10-17 relative launch (the main loop's own) exited 1 only because codex refused.  A relative OUT dir breaks too.  The v5 pass ruled it disclose-and-FILE; it is filed HERE, the defect's own row.  The fix stays #544's (the peer's round, e8a2bc: a 64-byte floor and a verdict-line gate, staged in _scratchpad/w544/), which now rebases on the landed launcher; offered to it (Fable 5.1): read the brief before the cd into a variable and refuse an empty one (BODY=$(cat \"$BRIEF\") && [ -n \"$BODY\" ] || exit 9), closing the missing and relative roads with the empty one."

== cxlaunchquotation 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the tools/cxlaunch.sh landing: the production rule (codex's ^ERROR: lines, ANSI-stripped and read with grep -a, classified ONLY when rc != 0 or stdout is empty; stdout never grepped for wall words) replaces the classifier that scored a complete answer WALLED for the word 'quota' or a quoted wall line.  Witness: the tracked file exits 8 on N1/N2, the landed one 0 (RECEIPT_v6.txt).  The controls' CONTRACT (run_controls_v6.sh) is derived from the file -- every predicate, pattern alternative, redirection, constant, exit-cascade order and caller-read log phrase -- and rows each decision's generating set (every override's value, a used out dir, both ends of each pattern), each pinned or disclosed with its reason; KILLTABLE_v6.txt kills each of its mutants as named.  Six passes on the landed file -- pass 2, the adjudication pass and the v3, v4, v5 and v6 passes, the owner's four-seat roster each time (Fable 5.1 stalled on the adjudication and v3 passes; Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] cxlaunchquotation closed by the tools/cxlaunch.sh landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (the landed launcher, v1): SHIP WITH CHANGES (2) -- GPT-6 Astra (ultra, `ran: model: gpt-6-astra'): read the model only from codex's header block and stop crediting 'answered by' when it is absent; make the controls exit non-zero on a bad tally and pin the `^ERROR:' anchor and the effort argument.  Both applied in v2.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/codex_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2: SHIP WITH CHANGES (2) -- GLM 5.3 (glm-5.3:cloud): reword the UNVERIFIED note to what was searched and put a count behind the header window; record that the ANSI strip widens both residuals.  Applied (v2 dropped the window for the header block; the residual is in the launcher's header).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/glm_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2: SHIP WITH CHANGES (1) -- Grok 4.7 (xhigh): grep without -a reads a NUL-bearing stderr as binary and drops the wall lines -- the real 2026-09-19 battery-preflight wall was recorded exit 6.  Measured on that file and fixed (grep -a, control X8).", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/grok_cxland.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2: SHIP WITH CHANGES (2) -- Fable 5.1, in two parts: its first run FELL BACK to claude-opus-4-8 after two refusals (FALLBACK_opus48_cxland.md, credited as Opus 4.8, and that run executed the TRACKED launcher unmodified and fired nine real Astra calls -- disclosed, no tree writes); resumed, Fable 5.1 wrote v2 itself: C1 add the tracked file as the pre-fix column, C2 correct two bug-file statements by content, pin four escapes and leave two unpinned.  All applied.", "ev": "regress/artifacts/cxlaunchland_20261016/pass2/fable5_cxland_v2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the header-block awk matched the banner ANYWHERE (N1's own stderr quotes four complete headers from line 5528), so v3 reads only the OPENING block; E1/E2 matched a substring, so `ultrax' passed -- v3 compares the exact argument sequence; and the record edits the packet called done were not yet in the tree.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/codex_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: launcher, controls and kill table hold; the three changes are the records the packet described as written (F10, F19, the cxlaunchunpinned filing), which were prepared but not yet applied.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/grok_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3, answering under the Fable seat's token (the packet listed all four; the transport is glm-5.3:cloud): cite RECEIPT_v2 not RECEIPT in the header, correct m_eq1's reason (N4 is rc 1; the observable shape is an rc outside {0,1} with an answer), pin --sandbox read-only and the brief.  All applied in v3.", "ev": "regress/artifacts/cxlaunchland_20261016/f2/glm_cxlandf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SEAT FAILURE -- the Fable 5.1 agent STALLED (stream watchdog, no progress for 600 s) after its opening line; no answer file.  Re-fired on the v3 pass, not counted as agreement."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: FLOOR BREACHES in v3's controls -- `NR > 12' -> `NR > 3' (the one real warning-prefixed header on record would go UNVERIFIED), the refusal guards `-gt 0' -> `-eq 1' at both sites and the wall guard `-gt 0' -> `-gt 1' (every fixture carried count 1 or 2+), refusal-then-refusal unrowed; the header comment's 'never names the model' survived; and 'no stderr on record carries both' is false for rc-0 answers.  All addressed in v4 (the class closure).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/codex_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Grok 4.7: FLOOR BREACH -- the fallback test `-gt 0' -> `-ge 0' (or widened with the wall count) passes all 70 because every row but D1/D2 disables the fallback, while production would re-run Daybreak on every answer; the window pinned only up to 20; the G9 bracket named the stale lines wrong.  All addressed in v4 (FB1/FB2 run with the fallback on).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/grok_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V3 PASS: SHIP WITH CHANGES (2) -- GLM 5.3: FLOOR BREACHES -- a window widened up to `NR > 20' passes (X9's quoted block sits at line 21), and the 30-line cap is pinned by nothing (`print' unconditional passes all 70).  Both addressed in v4 (W12/W13 and K30/K31 at the edges).", "ev": "regress/artifacts/cxlaunchland_20261016/v3pass/glm_cxlandv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V3 PASS: SEAT FAILURE -- the Fable 5.1 agent STALLED again (stream watchdog, 600 s), after reading the launcher and before writing an answer; most likely the whole 18-mutant kill table run as ONE foreground command (about 13 minutes).  Re-fired on the v4 pass with that hazard named."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v6 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v6 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v6 pass, NOT FIRED: the kimi seat sat outside the roster; nothing was sent."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v6 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v6 pass, NOT FIRED: minimax-m3 was not given any packet; the roster, not a wall."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V4 PASS: SHIP WITH CHANGES (7) -- Fable 5.1 (claude-fable-5-1 throughout, no fallback): the v4 CONTRACT's 'every decision' sentence is FALSE -- twelve MEASURED one-edit escapes of the 116 controls, seven at decisions it never named: codex's own rc passed through, the fallback's same-model and empty-disable conjuncts, the header's ANSI strip (149 of 975 opening blocks on record carry ANSI, 105 answered), `< /dev/null', the output names, six pattern alternatives with 0 instances; the v4 enumeration came from the passes' findings, not the file.  Addressed in v5, whose CONTRACT is derived from the file; its DISCLOSE for the alternatives was overridden (pinned) and put back to it.", "ev": "regress/artifacts/cxlaunchland_20261016/v4pass/fable5_cxlandv4.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V4 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: the CONTRACT is incomplete -- the .refused.txt move, codex's rc pass-through, the wall alternatives and the same-model conjunct each pass all 116; the kill-table driver accepted a run without its sentinel; census_v4 omitted the 30-line cap and V10's 410 counts empty-or-absent siblings, not exit status; 'never scored WALLED' and the unconditional exit-5 sentence over-claim.  All addressed in v5.", "ev": "regress/artifacts/cxlaunchland_20261016/v4pass/codex_cxlandv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V4 PASS: SHIP WITH CHANGES (5) -- Grok 4.7: five one-edit survivors traced against every row -- both `body -eq 0' sites (the smallest answer fixture was 40 bytes), the final rc test, the header strip, the .refused.txt move, the default codex path; V10 does not hold as written; the census figures named three populations; the panel.sh note is stale.  All addressed in v5.", "ev": "regress/artifacts/cxlaunchland_20261016/v4pass/grok_cxlandv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V4 PASS: SHIP WITH CHANGES (5) -- GLM 5.3 (glm-5.3:cloud, packet-fed): the classification tail -- an rc outside {0,1} with an answer -- undisclosed (pinned in v5: RC3A, RC2W); the cap rows are synthetic, unterminated blocks (disclosed); the FB comment false (fixed); the m_sgr figure cited at three populations (census_v5 measures its own); its F1 (W12/K30 set CX_MODEL) refuted by grep.", "ev": "regress/artifacts/cxlaunchland_20261016/v4pass/glm_cxlandv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V5 PASS: SHIP WITH CHANGES (5) -- Fable 5.1 (claude-fable-5-1 throughout, agent_models.py), measuring in a mirror: 224/224 reproduced; 53 decision constructs read off the file, 21 one-edit mutants of its own through the 224 -- 19 valid escapes in four groups: the override VALUES, the redirections' truncation, synthetic constant edges (a bare ESC[m, mkdir -p, the fallback line's asked:), and U21's disclosure a WRONG RECORD (a missing or relative brief reaches codex as an EMPTY prompt and an answer to it is reported seat answered, exit 0); eleven killed by five rows it built and measured, eight equivalents to disclose; the synthetic-pin BOUNDARY; zero floor breaches.  All addressed in v6 (U21 filed on cxlaunchempty).", "ev": "regress/artifacts/cxlaunchland_20261016/v5pass/fable5_cxlandv5.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V5 PASS: SHIP WITH CHANGES (5) -- GPT-6 Astra: fifteen one-edit survivors reasoned against the 224 (the main loop then MEASURED them: each override's value, the model at both calls, the fallback's own rc, mkdir -p, `>>' and `2>>', the refused stdout, both rule anchors, a parameterless CSI, `model:' with no space, the wall message, the logged stdout count); the CONTRACT's 'no caller reads the wall wording' false (status.sh counts SEAT WALLED), 'LOST iff exit 7' false (codex's own rc 7), the NM wording and the 44-file `;'-SGR provenance (42 are the #544 stub's output -- measured true).  All addressed in v6.", "ev": "regress/artifacts/cxlaunchland_20261016/v5pass/codex_cxlandv5.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V5 PASS: SHIP WITH CHANGES (2) -- Grok 4.7: the truncation edge (`>>' passes all 224, and the pack runner reuses the out dir on a retry, so an exit-5 answer could be doubled and marked done); 'nine find no block anywhere' false (the pattern has no end anchor) and 'every caller on record passes absolute paths' false; four equivalent forms to disclose.  U7 pin, U21 disclose and file.  All addressed in v6.", "ev": "regress/artifacts/cxlaunchland_20261016/v5pass/grok_cxlandv5.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V5 PASS: SHIP WITH CHANGES (3) -- GLM 5.3 (glm-5.3:cloud, packet-fed): the redirections' truncation edge and the effort overrides' honoured edge unpinned (both MEASURED escapes); ESC, the strip's 2>/dev/null, `mkdir -p', `mv -f' and the banner text unnamed; the synthetic-pinning criterion to record (disclose only when no caller reads the difference).  U7 pin, U21 disclose and file.  All addressed in v6.", "ev": "regress/artifacts/cxlaunchland_20261016/v5pass/glm_cxlandv5.txt", "d": "✓"}
  hold_question: "REGRESS (held 2026-10-17 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr), the v4 edge rows (W12/W13, K30/K31, R2X/D3, W1L, FB1/FB2, X14/X15) and the v5 rows (RC1A/RC3A codex's own rc, D5, FD, CH, SI, N1F, D1R, DP/EO/E0b, the alternatives RF1-RF3/WL1-WL3/RFC/WLC, the cascade pairs RW/RI/WI/EM/IR, the awk guards HB/BA/R7A/R7B/NM/TM/MA/WS, PK and LOG) and the v6 rows (OV/OVA each override's value at its own call, FR the fallback's own rc, RS/RSF a used out dir, MP/MPF a missing parent, RN/RNF a non-empty refused stdout, SP1/SP2 and R9A/R9B the rule patterns' two ends, BN, CZ, WZ, R7X/R7XL codex's own rc 7, PK's SEAT WALLED, LOG's numbers) -- and does regress/artifacts/cxlaunchland_20261016/KILLTABLE_v6.txt still kill every one of its mutants as named?  Is the record (the launcher's header, the controls' CONTRACT, the CHANGELOG block, the OB corrections) true of what shipped?"
  state: "closed"
  state_note: "filed 2026-10-09: measured on GPT-6 Astra's check of the asiceventaddr convergence -- a complete 10,466-byte answer with its verdict line, no `ERROR:` line on stderr, and the launcher printed 'SEAT WALLED' (LAUNCH_RC=8) because the answer's own sentence '... its quotation must retain ...' matched `grep -ic 'quota'` (the answer: regress/artifacts/fablequeue8n_20261009/astra_confirm/codex_astra_asicconverge.txt; the launcher's own output: cxlaunch_asicconverge_stdout.txt beside it).  tools/cxlaunch.sh:44 builds `wall` from the `ERROR:` lines PLUS the whole stdout, so any answer that uses the words quota / quotation / rate limit / usage limit reads as a wall -- the carrier's quoting-re-arms-the-reader class, one level down (the script's own comment at :33-41 diagnoses the stderr half and kept the stdout half).  Fix: word-anchor the pattern and test stdout only when no verdict line is present; owes controls both ways (a real 403/quota notice still reds; an answer containing 'quotation' does not).  LOW: a human reads the answer; an unattended runner would discard it.\n\n[2026-10-17] CLOSED by the tools/cxlaunch.sh landing -- and the fix this note prescribes (\"word-anchor the pattern and test stdout only when no verdict line is present\") was REPLACED by the three-seat ruling's production rule, not applied: stdout is never grepped for wall words; codex's ^ERROR: lines are classified only when rc != 0 or stdout is empty (regress/artifacts/adj_20261016/RULINGS_C_records.md F1).  Merges the 2026-09-26 filing cxlaunchwallfp (no ledger row)."
  witness: "harness:regress/artifacts/cxlaunchland_20261016/RECEIPT_v6.txt -- the TRACKED launcher (cb180d9d) exits 8 on N1, a captured real Astra answer whose stderr quotes a codex wall line, and on N2, a synthetic answer carrying the four wall words ('quota' among them); the landed file exits 0 on both; regress/artifacts/cxlaunchland_20261016/KILLTABLE_v6.txt kills every pinned one-edit mutant of the landed file"
```

### 5c. the CHANGELOG block (a DRAFT: its v6-pass sentence is written from this pass's answers)

# `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- an rc-0 run with a non-empty stdout is never scored WALLED or REFUSED for what its stderr quotes, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5 (after the refusal, wall and empty-stdout checks); the controls row each decision's VALUES and used states, not only its defaults (v6: 269 checks, 133 mutants)

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F1): codex's `^ERROR:` lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall
words -- the discriminator is the exit status and the answer, which quoted text cannot forge.  Every real wall and refusal
on record is rc 1 with an empty stdout, and every rc-0 run carries an answer: 474 launch-log rows, 440 rc 0 with stdout and
34 rc 1 empty, nothing else (`CENSUS_v5.txt`).

* `tools/cxlaunch.sh`: until this landing the tracked file ran Astra at `max` with the 2026-09-07 classifier while most farm
  jobs ran an untracked scratchpad copy -- and the carrier described the copy's behaviour as the tracked file's.  The landed
  file: ANSI colour stripped and `grep -a` before the `^ERROR:` anchor (a real coloured refusal read exit 6 unstripped; a
  real NUL-bearing wall read exit 6 without `-a`); the Daybreak fallback (`gpt-daybreak-blue-latest`, the refused run kept
  as `.refused.*`, the answer credited to Daybreak; not fired on an answer, a wall, a refusal asked of Daybreak itself, or
  with the fallback set empty); the model read ONLY from codex's OPENING header block -- banner and first rule by line 12,
  the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch, "model UNVERIFIED", exit
  0, with no model line in an opening block); the effort `ultra`.  Its header records the residuals (N4 and its refusal
  twin), exit 5's novelty to the pack runner and the log phrases its callers read (`run_pack_body.sh` and `status.sh`),
  codex's own rc 7 (not a refusal), the usage requirement of ABSOLUTE paths with what a missing or relative brief really
  does (codex gets an EMPTY prompt -- Fable 5.1, measured), and the controls.  Its executable lines are v3's but ONE: v6
  rewords the UNVERIFIED message to "no model line in an opening codex header block", which fixture NM showed is the truth.
* Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v6.sh`: every row drives three launchers -- the TRACKED
  file the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a
  fixture.  269/269 (`RECEIPT_v6.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8
  (a NUL in stderr), IR 1 -> 5 (a different model), CH 0 -> 5 (a coloured header), CSI and CZ 6 -> 7 (a non-SGR escape, a
  parameterless one).  Its header is the CONTRACT, derived from the FILE (v5) and, in v6, rowing each decision's VALUES and
  used states: every override set to a non-default value at its own call (OV), a re-run into a used out dir (RS), a missing
  parent (MP), the fallback's own rc (FR), a non-empty refused stdout (RN), both ends of both rule patterns (SP1, SP2, R9A,
  R9B), a near-miss banner (BN), `model:` with no space (WZ), codex's own rc 7 (R7X), `SEAT WALLED` iff exit 8 (PK, which
  `status.sh` reads), and the `codex rc=` line's numbers, not only its format (LOG).  Its BOUNDARY for synthetic rows (Fable
  5.1): an edge is pinned when its constant selects an exit status, a call argument or a caller-read phrase on an input
  codex can produce; disclosed when it needs the harness environment, an unclaimed encoding, an unreachable flag value or a
  display line.  CSI is synthetic in BOTH halves -- 42 of the 44 codex `.err` files carrying a `;`-joined SGR are the #544
  control stub's own output, the other 2 a coloured GXemul prompt quoted mid-line (`v5pass/SEMISGR_WHERE.txt`; the v5 text
  called that half load-bearing).  Kill table `run_mutants_v6.sh`: 133/133 as recorded (`KILLTABLE_v6.txt`) -- the 105
  v5 mutants and 28 new, each killed by the controls its line names; the driver re-runs once any mutant run carrying the
  load flake's signature (an empty `stdout= b`, Fable 5.1).
* Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
  `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
  freely", "has no Daybreak fallback" and "panel.sh's comment is still owed" statements bracketed by content; RULINGS_C's
  drifted line citations re-cited by id.  No row filed: the relative-path defect the v5 pass ruled disclose-and-FILE is
  filed ON `cxlaunchempty`, whose defect it is (an empty prompt reaching codex) by a second road; that row's NUL half is
  recorded closed by this landing (X8), and its fix stays `#544`'s, the peer session's round, which rebases on the landed
  file.

**Pass 2** (`pass2/`, on v1): Astra SWC 2, GLM SWC 2, Grok SWC 1 (the NUL-bearing wall, measured), Fable SWC 2 (its first run
fell back to claude-opus-4-8 after two refusals -- disclosed, credited as Opus 4.8; resumed, Fable 5.1 wrote v2).
**Adjudication pass** (`f2/`, on v2): Astra SWC 3 (the header awk matched the banner ANYWHERE; E1/E2 matched a substring),
Grok SWC 3 and GLM SWC 3 (records; the receipt citation; `m_eq1`'s reason); Fable SEAT FAILURE (a stall).  **V3 pass**
(`v3pass/`): Astra SWC 3, Grok SWC 3, GLM SWC 2 -- one-edit mutants passing all 70 v3 controls at the window and cap
constants, the multiplicity guards and the fallback predicate, so v4 closed that class; Fable SEAT FAILURE (a second
stall).  **V4 pass** (`v4pass/`): Fable SWC 7, Astra SWC 3, Grok SWC 5, GLM SWC 5 -- the v4 CONTRACT was derived from the
passes' FINDINGS, not the file, and decisions no pass had named had one-edit mutants passing all 116 v4 controls (codex's
own rc, the fallback's second and third conjuncts, the header strip, the stdin redirect, the output names, the pattern
alternatives, the body tests, the default codex path), so v5 derived the CONTRACT from the file.  **V5 pass** (`v5pass/`):
Fable SWC 5, Astra SWC 5, GLM SWC 3, Grok SWC 2 -- all four zero floor breaches, and one shape: a row pinned a value's
DEFAULT, not the value, and a FRESH state, not a used one.  The main loop measured every claimed escape before acting
(`v5pass/main_meas.txt`: 18 of 18 pass all 94 after-column checks of the v5 controls), Fable 5.1 measured 19 more forms and
built the five rows that kill them (v6's OV, RS, MP, CZ, LOG); five records sentences were false (no caller reads the wall
wording; LOST iff exit 7; the NM message; the 44-file provenance; a relative brief makes the launcher exit 1); U7 PINNED, all
four agreeing, with Fable's boundary.  **V6 pass** (`v6pass/`): [to be written from its answers].  Opus, agy, kimi,
deepseek and minimax not fired, by the owner's roster of 2026-10-16.


## 6. Questions

1. **Your own v5 findings** (the Y-rows naming you): is my disposition right, AND is the fix right -- does the named row go
   red under the named mutant FOR THE REASON NAMED?  Be harder on the ones you raised than on anyone else's.
2. **The enumeration.**  List every decision of `tools/cxlaunch.sh` you checked against the CONTRACT, by construct.  For a
   decision that is missing, or a listed row that does not straddle its edge, give the exact one-edit mutant, which of the
   269 controls it passes, and the property it breaks.  A zero is evidence only with its denominator.
3. **The kill table** (section 4b).  Is any mutant killed for a reason other than the one its line names?  Is there a one-edit
   mutant OUTSIDE the table that passes all 269 controls and breaks a line of the CONTRACT?  **Grade each you find: a floor
   breach (clauses a-d) or clause-(e) contract debt, and say why.**  Name the shapes you swept.
4. **The records** (section 5).  Which sentences are false of what ships?
5. **Which of my 26 dispositions is WRONG?**  Name the count you checked.
6. **Does the chain close here?**  If your answer to 3 is zero floor breaches, say so in one line with its denominator.

Open with your verdict line: `VERDICT: CLOSE` / `VERDICT: SHIP WITH CHANGES (n)` / `VERDICT: DO NOT SHIP`.  Label each claim
MEASURED (you ran it), READ (you opened the file) or REASONED.  Write nothing to any project tree.
