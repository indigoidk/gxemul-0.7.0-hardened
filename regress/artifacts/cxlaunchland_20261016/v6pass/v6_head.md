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

<TOKEN_LINE>

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
