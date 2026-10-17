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

<TOKEN_LINE>

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
