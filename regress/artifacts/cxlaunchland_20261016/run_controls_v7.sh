#!/bin/bash
#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
#  F1), v7 after the four-seat pass 2, the adjudication pass and the v3, v4, v5 and v6 passes.  Every row runs a launcher against a FAKE
#  codex that replays a fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the
#  expected one:
#
#    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
#             landing REPLACES -- it names its codex binary under $HOME and has no override
#    before   cxlaunch_before.sh   = the untracked production copy the farm ran (md5 3c51a757...)
#    after    tools/cxlaunch.sh    = the landed file (or $CXL_AFTER, which the mutant table uses)
#
#  The tracked column is the PRE-FIX state (Fable 5.1's pass-2 C1, via its Opus 4.8 fallback): N1 and N2 are the
#  `cxlaunchquotation' false wall (exit 8 there, 0 after), D1 the missing Daybreak fallback (7 there, 0 after).  The tracked and
#  before expectations RECORD what the two old files do; only the after column is a claim.  Those of the rows v5 added were
#  recorded from a calibration run of this file (RECEIPT_v5_calibration.txt); every after expectation was written before it.
#
#  v5 -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3) measured one-edit mutants passing all 116 v4 controls at
#  decisions the v4 CONTRACT did not list -- codex's own rc passed through, the fallback's second and third conjuncts, the
#  header's ANSI strip, the stdin redirect, the output names, the pattern alternatives, the two `-eq 0` body tests, the default
#  codex path.  The v4 CONTRACT was derived from the three passes' FINDINGS, not from the file (Fable 5.1).  v5's is derived from
#  the file: every predicate, conjunct, pattern alternative, redirection, constant, exit-cascade order and caller-read log
#  phrase, each asked "which row goes red if this changes".  Every launcher run is under `timeout 120' (a looping mutant exits
#  124 and reds; an honest run takes about 0.6 s -- Fable 5.1, v4 pass) and is fed a MARKER file on stdin; HOME is a scratch
#  dir holding a second fake at the launcher's default codex path, which marks the runs that reach it.
#
#  v6 -- the v5 pass measured one-edit mutants passing all 224 v5 controls at decisions the v5 CONTRACT listed as pinned, one
#  shape again: a row pinned the DEFAULT of a value and not the value itself, or a fresh state and not a used one.  Each
#  override honoured only as empty or default (CX_EFFORT=ultra, the fallback's effort and model, the main call's model --
#  GLM 5.3, GPT-6 Astra, Fable 5.1); `>' and `2>' never met a used out dir (`>>' passes -- all four seats); `mkdir -p' never
#  met a missing parent; the refused run's stdout was always empty; the fallback's own rc never nonzero with an answer; the
#  rule patterns' anchors, a parameterless CSI, `model:' with no space, the banner text's `Codex', a nine-dash rule; and the
#  `codex rc=' line's numbers, never compared.  The CONTRACT also said no caller reads the wall wording (status.sh does),
#  `The answer is LOST' iff exit 7 (codex's own rc 7 exits 7 without it), and that nine dashes are not a rule (they are --
#  the pattern has no end anchor; Grok 4.7), and that a relative brief makes the LAUNCHER exit 1 (it does not: an empty
#  prompt reaches codex, and codex decided -- Fable 5.1, measured).  Each is now a row, a check or a corrected sentence.
#
#  v7 -- the v6 pass found no floor breach and one shape in v6's OWN new checks: a check that reads the launcher's text to
#  decide what it expects.  PK decided "is this codex's own rc 7?" from the log's `codex exited 7' -- so a refusal echo
#  rewritten to that text passed (GPT-6 Astra); v7 keys PK on the ROW (R7X, and its rc-8 twin R8X).  LOG compared numbers on
#  default runs only, so a hardcoded logged effort passed; RXM had no row for the raw-status message's number.  And four
#  values no row varied: a two-line brief, a refused destination already occupied (`mv -n'), a lowercase tag, the strip
#  class's other members.  Each is now a row or a check; the false sentences are corrected (GPT-6 Astra, GLM 5.3).
#
#  THE CONTRACT -- the decisions read off the landed launcher (by construct), the rows that pin the edges each names, and
#  what is not pinned.  Rows SAMPLE the values a decision admits -- briefs, tags, out-dir states, header shapes -- except
#  where a set is finite and named: the ANSI strip's class is EXHAUSTED (CSX with CZ's empty parameter), as are the refusal and wall patterns'
#  alternatives (a row each).  A claim here is of the edges named, not of every value (GPT-6 Astra, v6 pass: the v6
#  records called every decision pinned or disclosed while nine one-edit escapes stood):
#  configuration
#    CX_CODEX_BIN honoured, its `:-'      E0b (no after run but DP's and EO's reaches the default-path fake); EO (set EMPTY)
#    the default codex path               DP (CX_CODEX_BIN unset: the run reaches $HOME/AppData/Local/Programs/.../codex)
#    CX_MODEL, CX_EFFORT, CX_AUP_EFFORT, their `:-' and defaults
#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default); OVA (each
#                                         set to a NON-default value: each reaches its own call, both compared whole)
#    CX_AUP_MODEL, its default and `-' (EMPTY disables the fallback)
#                                         E2; FD (every row that sets it empty makes exactly one call); OVA (a non-default
#                                         fallback model is the second call's)
#    the output names and the stdout/stderr redirections
#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written); RSF
#                                         (a re-run into a dir holding a stale answer and a stale header: both TRUNCATED);
#                                         TGF (a lowercase tag names its files as given)
#    `mkdir -p "$OUT"'                    MPF (an out dir two levels below a missing parent is created)
#    `< /dev/null' on codex's stdin       SI (no after run's codex reads the marker the launcher is fed)
#    `cd "$PROJ"'                         CWD (every after run's codex starts in the project root)
#    the argv cap `sz -gt 30000', exit 9  X14 (30,000 accepted) / X15 (30,001: exit 9, codex never called)
#  the call
#    the argument sequence                E1 (one call), E2 and EO (Astra, then Daybreak), DP -- each compared whole; MBA
#                                         (a TWO-line brief reaches codex whole)
#  the opening header
#    ANSI strip on the header             CH (the real coloured header of fx/R2.stderr, asked as gpt-6-other -> 5)
#    the window `NR > 12 && h < 2'        W12 / W13 (first rule at line 12 read, at 13 not); X13 (the real banner-at-4 header);
#                                         X9, X10 (no opening block, a quoted one at line 21)
#    the banner: `h == 0 &&', `/^OpenAI Codex/'
#                                         HB (a banner-shaped line inside the block does not restart it); BA (a banner with a
#                                         prefix, above the real one, is not a banner); BN (`OpenAI notice:', a near-miss
#                                         above the real banner, is not one: the text's `Codex'); every header row
#    the first rule: `h == 1 &&', 8 dashes, `next'
#                                         BA (a rule before any banner is not the first rule); R7A (seven dashes are not a
#                                         rule); R9A (nine dashes ARE one -- the pattern has no end anchor; the v5 gloss
#                                         "nine find no block anywhere" was false, Grok 4.7); SP1 (a separator not at column
#                                         0, before the first rule, is not one: the `^'); every header row (`next')
#    the closing rule: `h == 2 &&', 8 dashes, `exit'
#                                         BA (a rule before any banner closes nothing); R7B (seven dashes do not close the
#                                         block); R9B (nine dashes DO close it: a model after them is not read); SP2 (a
#                                         separator not at column 0, inside the body, does not close it: the `^'); NM (no
#                                         model line in the block: a model line after the close is not read)
#    the body: `h == 2', the cap `++n > 30'
#                                         R7A (the lines between banner and first rule are not body); K30 / K31 (a model at
#                                         body line 30 read, at 31 not)
#    the first `model:' line, anchored    TM (two model lines: the first is read); MA (`fallback model:' is not a model line);
#                                         M1, X5
#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies); WZ (`model:gpt-6-astra',
#                                         NO whitespace, verifies: the trims' `*', zero or more)
#  classification
#    the gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4; RC2W (rc 2 with an answer IS classified); B1G (a 1-byte rc-0
#                                         answer is NOT)
#    `^ERROR:', `grep -a'                 X1; X8
#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR);
#                                         CZ (`ESC[m', a CSI with NO parameter: the class's `*'); CSX (EVERY member of the
#                                         class -- the digits 0-9 and `;' as parameters, each final letter A-Z and a-z -- as
#                                         escapes in one line before `ERROR:'; with CZ's empty parameter, the class EXHAUSTED -- GLM 5.3, v7 pass)
#    the ESC byte, `printf '\033''        A1, CH, CSI, CZ, Q3, R2X -- each needs the strip, and a wrong ESC strips nothing
#    the refusal alternatives, `-i'       P2, Q1, A1 (`flagged for possible cybersecurity'); RF1 (`cannot help with');
#                                         RF2 (`can't help with'); RF3 (`I won't help'); RFC (the first, upper case)
#    the wall alternatives, `-i'          P1, Q2, Q3, X8 (`usage limit'); WL1 (`quota'); WL2 (`rate limit');
#                                         WL3 (`not authenticated'); WLC (the first, upper case)
#    refusal count `refus -gt 0', at BOTH guards
#                                         P2, Q1, A1, D1 (count 1); R2X (2, the final guard); D3 (2, the fallback)
#    wall count `wall -gt 0'              W1L (count 1); P1, Q2, Q3, X8 (2); N4 (6)
#  the fallback
#    trigger `refus -gt 0 && -n AUP_MODEL && AUP_MODEL != MODEL'
#                                         D1, D2, D3 fire; FB1, FB2 do not (an answer, a wall; the fallback on); FD (empty:
#                                         never); D5 (asked ON Daybreak and refused: no second run)
#    once                                 D4 (refused, then refused on Daybreak: exactly two calls)
#    the fallback run re-classified       D1, D2 and every row whose fallback answers (D3, OV, RN, RN2, FR): a stale refusal
#                                         count from the first run would exit 7; FR also re-reads the rc (Grok 4.7, v6 pass:
#                                         D4 cannot pin it -- its second run refuses too)
#    the refused run's files kept         D1R (codex_D1.refused.txt and .refused.err byte-for-byte the first run's; codex_D1.txt
#                                         and .err the Daybreak run's); RNF (a NON-EMPTY refused stdout, byte-for-byte); RN2F
#                                         (the refused files REPLACE stale ones already there: `-f')
#    the answer credited to the fallback  D1, D3 (Daybreak credited); D2 (Daybreak compared -> 5)
#  the exit cascade: refused 7, walled 8, empty 6, a different model 5, codex's own rc
#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1); FR (3:
#                                         the FALLBACK run's raw rc, with an answer); R7X (codex's own rc 7 with an answer);
#                                         R8X (codex's own rc 8 with an answer: not a wall)
#    the order, each adjacent pair        RW (refusal + wall -> 7); P2 (refusal + empty + rc 1 -> 7); RI (refusal + another
#                                         model's header -> 7); P1 (wall + empty -> 8); WI (wall + another header -> 8);
#                                         EM (empty + another header -> 6); X1 (empty + rc 1 -> 6); IR (rc 1, an answer,
#                                         another header -> 5)
#    the empty test `body -eq 0'          N3, X1 (0 bytes -> 6); B1E (1 byte -> 0)
#    identity `-n RAN && RAN != ANSWERED_BY'
#                                         M1, D2, X5, W12, K30, X13, CH, IR, BA -> 5; M2, X6, X9, W13, K31, NM, HB -> UNVERIFIED, 0
#  the log phrases a caller reads -- _scratchpad/codexpack_20260928/run_pack_body.sh (done_job and reap) AND status.sh beside
#  it, which counts `SEAT WALLED' (GPT-6 Astra, v5 pass: the v5 CONTRACT said no caller read the wall wording); derived by
#  `grep -rlE "SEAT WALLED|The answer is LOST|seat answered|answered by: "' over _scratchpad and GXEMUL-SEC/tools, the
#  launcher copies and the agy pack excluded -- the PHRASE readers are those two pack scripts; census_v5.py, in
#  regress/artifacts and outside that grep's scope, reads the `codex rc=' line (LOG), not the phrases (GPT-6 Astra, v6 pass)
#    `seat answered' iff exit 0; `The answer is LOST' iff the REFUSAL exit; `SEAT WALLED' iff the classified WALL exit --
#    codex's own rc 7 and rc 8, with an answer, exit 7 and 8 and print `codex exited N' instead (with an empty stdout the
#    run exits 6), so the runner retries them (R7X, R8X); PK
#    decides which rows those are by the ROW, never by the launcher's text (v6 read the text, and a refusal echo rewritten
#    to `codex exited 7' passed -- GPT-6 Astra, v6 pass); `answered by: <model>' iff an exit 0 whose model verified
#                                         PK (every after run); R7XL, R8XL; RXM (each raw-status message names its own rc);
#                                         N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB, R9B (none)
#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, WHOLE, as an explicit fidelity guarantee: census_v5.py
#    parses its rc and stdout count and the asked/ran census its model names; the stderr count and the asked effort are
#    pinned for fidelity, not for a reader (D1 -- GPT-6 Astra and Grok 4.7, v7 pass; v5 read the format only, Astra)
#                                         LOG (N1, both of D1's calls, RC3A, both of OV's -- its NON-default models and
#                                         efforts: each line compared whole)
#  NOT PINNED, each with its reason:
#    `|| exit 9' after `cd'               needs a missing project dir -- untestable without editing the file
#    `set -u'                             reached only by a missing positional argument (a usage error, exit 1); every caller
#                                         passes three, and a row without them would write outside the scratch dir under a
#                                         mutant that drops it.  Load-bearing for one kill: under it `m_noinit''s unbound
#                                         `$refus' errors every rc-0 row (Fable 5.1, v5 pass)
#    the banner rule's `next'             equivalent: the banner line matches no later rule
#    the body cap's and the window guard's `exit' (not `next')
#                                         equivalent: past the cap every later line also fails `++n > 30' and is not
#                                         printed, and past line 12 with no block every later line is skipped either way
#    `mv -f' (both moves)                 equivalent off a terminal: mv prompts only with a terminal on stdin AND an
#                                         unwritable destination; no caller runs the launcher on a terminal
#    `2>/dev/null' on strip_ansi and on the verdict grep
#                                         display only: each reads a file that exists whenever it runs ($ERR after codex
#                                         wrote it; $TXT), and the suppressed text changes no decision
#    RELATIVE or MISSING paths            the brief's size and `mkdir' resolve in the caller's directory, codex's files after
#                                         `cd "$PROJ"', and the brief is checked only against the argv cap: a missing brief, or
#                                         a relative one that does not resolve from the project root, reaches codex as an EMPTY
#                                         prompt (one that resolves there is read from there -- GPT-6 Astra, v6 pass: v6 said
#                                         the brief is not checked, and that a relative one always arrives empty), and what
#                                         codex does is what is reported -- on 2026-10-17 codex
#                                         refused it and exited 1, while a fake that answers it is reported `seat answered',
#                                         exit 0 (Fable 5.1, v5 pass, measured; the v5 text called the exit 1 the launcher's).
#                                         It is `cxlaunchempty''s defect -- an empty prompt reaches codex -- by a second road,
#                                         and is FILED on that row with the relative OUT dir.  Every caller in the tree passes
#                                         absolute paths (the pack runner's ARTS defaults to one, and it skips a missing
#                                         brief); so does every row here
#    the `model:' label's case, and the identity compare's case
#                                         equivalent on record: codex's header is lower-case by its format (all 975 opening
#                                         blocks match `^model:'), and a case-folded compare is a policy change, not a drift
#    `wc -c' (bytes) for the argv cap     equivalent here: under the C locale the harness and the farm run in `wc -m' counts
#                                         bytes too, and every brief on record is ASCII
#    the banner past `OpenAI Codex' (narrowed to `OpenAI Codex v')
#                                         equivalent on record: every banner is `OpenAI Codex v...' (BN pins the widening)
#    the closing rule's `exit' against another way to end the block (`h = 3; next')
#                                         equivalent by construction: nothing matches past the close either way; the edge
#                                         that matters, `exit' against `next', is NM's
#    the `.' of `can.t' and `won.t'       the quoting form of an apostrophe inside a single-quoted pattern, not a decision:
#                                         an ASCII `'' cannot be written there, and 0 column-0 ERROR lines on record carry a
#                                         curly apostrophe or any non-ASCII byte (Fable 5.1, v5 pass)
#    the stream a caller-read phrase is printed on
#                                         equivalent for both phrase readers: the pack runner launches with `> launch.log
#                                         2>&1' (run_pack_body.sh:66) and status.sh reads that log, so stdout and stderr
#                                         reach both alike (GLM 5.3 asked; settled by reading)
#    the RAN grep's missing `-a'          EQUIVALENT: `HDR=$(...)' drops every NUL before the grep reads HDR (bash warns
#                                         `ignored null byte in input'), so the grep never sees one.  Measured: a NUL in the
#                                         block's workdir line verifies, one INSIDE the model name is deleted -- `gpt-6-a<NUL>
#                                         stra' verifies as gpt-6-astra -- and one after `gpt-6-other' still exits 5
#                                         (v6pass/main_meas/NUL_HDR.txt); 0 of the 979 opening blocks on record carry a NUL,
#                                         while 87 of 2,429 codex .err files carry one elsewhere (NUL_BLOCKS.txt).  GLM 5.3
#                                         asked, v6 pass; the first reading here -- grep prints `Binary file' and the run exits
#                                         5 -- was refuted by that measurement
#    a CSI with a private-mode `?' parameter, and an ESC that is neither CSI nor OSC
#                                         not stripped (the class is `[0-9;]*[A-Za-z]'), so a refusal behind `ESC[?25l' is not
#                                         read as one: on the shapes the launcher classifies -- rc != 0, or an empty stdout --
#                                         the run exits 6, 5 or the raw rc -- never 0, and never a CLASSIFIED refusal (a raw rc 7 with
#                                         an answer still exits 7, without LOST -- GPT-6 Astra, v7 pass); 0 of 8,601 .err files on
#                                         record carry a `?'-CSI, and the 2 carrying another ESC have none before an `ERROR:'
#                                         (v6pass/main_meas/ESC_WHERE.txt; GLM 5.3, v6 pass)
#    display only -- printed, read by no decision and no production caller: `brief bytes'; the `ran:' line (the header's
#                                         effort is printed, never compared; a records census once counted its model names beside
#                                         `asked:' -- GLM 5.3, GPT-6 Astra, v7 pass); `verdict-in-stdout' (verd exists for that line alone); the
#                                         IGNORED note; the refusal excerpts (`-m1'/`-m2', `cut -c1-160'); the REPHRASE line;
#                                         the `*** SEAT REFUSED on <model> (content filter):' excerpt header and the `*** AUP
#                                         FALLBACK:' echo; the wording of the 5, 6, 7, 8 and rc messages beyond the phrases above (the 8's `SEAT
#                                         WALLED' and the rc message's `codex exited N', its number included, ARE pinned, by
#                                         PK, R7XL, R8XL and RXM); the exit-0 lines' text after `model UNVERIFIED' (N1V and
#                                         WMT pin `seat answered. (answered by: <model>)' whole; the UNVERIFIED loop pins
#                                         `model UNVERIFIED' and no `answered by:' -- Grok 4.7, v6 pass; GLM 5.3, v7 pass, named the
#                                         header, the echo and the 7's wording missing from this list)
#    the empty test's MEASURE             `wc -c' against `wc -w' (any count blind to whitespace): no fixture's stdout is
#                                         whitespace-only, so a word count passes all 123 after-column checks -- MEASURED
#                                         (v7pass/main_meas/m_bodywords.out) -- while on rc 0, a lone space on stdout and a quoted
#                                         column-0 wall line the launcher exits 0 and the mutant 8 (SPACE_STDOUT_DEMO.txt; GPT-6
#                                         Astra, v7 pass).  Clause (e): FILED as cxlaunchcov
#  (The v6 sentence below said "every rc row and every Daybreak answer sits off CENSUS_v5's diagonal"; the Daybreak answers
#  are ON it -- rc 0 with stdout -- and the fallback's sequence has one real instance, dossier_gdromdma.launch.log: GPT-6
#  Astra, GLM 5.3, v6 pass.  Corrected in the list.)
#  SYNTHETIC SHAPES, and THE BOUNDARY of what is pinned without an instance on record (Fable 5.1, v5 pass, with GLM 5.3's and
#  Grok 4.7's criterion; pass 2's "0 on record, so disclose" is superseded): a synthetic edge is PINNED when its constant
#  selects an exit status, a call argument or a log phrase a caller reads, on an input codex can produce through its
#  documented interface -- a diagnostic line, a header line, an escape sequence, a status, an answer; it is DISCLOSED as
#  equivalent when the edge is reachable only through the harness environment (a locale), an input encoding the file does
#  not claim, a flag whose other value is unreachable here, or a display line (the NOT PINNED list).  Pinned under it, each
#  with 0 instances on record -- CENSUS_v5.txt names the count for each shape it classifies (diagnostic lines, escapes,
#  opening blocks, the rc-by-stdout table); B1E/B1G's one-byte answers and D5's asked-on-Daybreak refusal are shapes it
#  does not census, since it collapses stdout to empty or not and parses no asked model (GPT-6 Astra, v7 pass): RF1-RF3, RFC, WL1-WL3, WLC, RW, RI, WI, EM, IR, BA, BN, HB,
#  R7A, R7B, R9A, R9B, SP1, SP2, NM, TM, MA, WS, WZ, K30, K31, W12/W13, CZ, CSX, R7X, R8X, RC1A, RC3A, RC2W, B1G, B1E, D5, FR
#  and RN -- the rc rows among them (RC1A, RC3A, RC2W, IR, FR, RN, R7X, R8X) sit OFF CENSUS_v5's diagonal (0 launch lines off
#  rc 0 with stdout / rc 1 empty); the fallback rows' Daybreak answers sit ON it, synthetic in no shape, their
#  refusal-then-answer sequence with one real instance (dossier_gdromdma.launch.log) -- and CSI, in BOTH halves.  RS, MP, RN2,
#  OV, MB and TG are CALLER inputs, not codex output, so no census counts them (v6 listed RS, MP and OV under "CENSUS_v5.txt
#  names each count", which it does not): an out dir's prior state (RS, RN2) or missing parent (MP), the overrides (OV), and
#  a two-line brief and a lower-case tag (MB, TG) -- the shapes real callers pass (2,352 of the 2,383 codex_*.err tags on
#  record are lower-case, v6pass/main_meas/TAGCASE.txt), which v6's one-line brief and upper-case row names never varied.  The v5 CONTRACT called its `;'-joined half load-bearing because 44 of the codex .err files carry
#  one; 42 of the 44 are the #544 control stub's own output and the other 2 quote a coloured GXemul prompt mid-line, never a
#  codex diagnostic (v5pass/SEMISGR_WHERE.txt; GPT-6 Astra, v5 pass).  Every line opening with eight dashes in the first 42
#  lines of the 2,427 codex .err files is exactly eight dashes (1,954 lines, v5pass/RULELEN_CENSUS.txt), so R9A/R9B pin the
#  pattern's own edge, not a shape seen.
#
#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
#  Usage: bash run_controls_v7.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
#  the mutant table uses; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
TRACKED="$HERE/cxlaunch_tracked.sh"
BEFORE="$HERE/cxlaunch_before.sh"
AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
ONLY="${CXL_AFTER_ONLY:-}"
N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
NROWS=83
NFD=70
for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout" "$HERE/fx/R2.stderr"; do
    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
done
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
ESC=$(printf '\033')

mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr from stdin)
    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
}
printf 'A complete review answer.\nVERDICT: SHIP\n' > "$T/ans_verdict.txt"
#  NOT the word "verdict" in any case: the launcher counts it case-insensitively, and a first draft of this fixture said
#  "no verdict line" -- so it HAD one, and the kill table measured X2 blind to the mutant it exists for.
printf 'A complete review answer that ends without its summary line.\n' > "$T/ans_noverdict.txt"
printf 'x' > "$T/ans_1byte.txt"
hdr() {    # $1 the model -- a minimal closed opening header block
    printf 'OpenAI Codex v0.153.4\n--------\nmodel: %s\nreasoning effort: ultra\n--------\n' "$1"
}
hdr gpt-6-astra > "$T/hdr_astra.txt"
hdr gpt-6-other > "$T/hdr_other.txt"
grep -m1 '^ERROR:' "$HERE/fx/P2.stderr" > "$T/refusal_line.txt"
grep -m1 '^ERROR:' "$HERE/fx/P1.stderr" > "$T/wall_line.txt"
[ -s "$T/refusal_line.txt" ] && [ -s "$T/wall_line.txt" ] || { echo "APPARATUS FAIL: no column-0 ERROR line in P1 or P2"; exit 9; }
mkfx P1 1 "" "$HERE/fx/P1.stderr"
mkfx P2 1 "" "$HERE/fx/P2.stderr"
mkfx N1 0 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx N2 0 "$HERE/fx/N2.stdout" ""
mkfx N3 0 "" ""
mkfx N4 1 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx Q1 1 "" "$QD/Q1.stderr"
mkfx Q2 0 "" "$QD/Q2.stderr"
mkfx Q3 1 "" "$QD/Q3.stderr"
sed "s/^ERROR:/${ESC}[1m${ESC}[31mERROR:${ESC}[0m${ESC}[0m/" "$HERE/fx/P2.stderr" | mkfx A1 1 "" -
hdr gpt-daybreak-blue-latest | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" "$T/hdr_astra.txt"
sed 's/^/regress\/artifacts\/old_panel\/codex.txt:17:/' "$HERE/fx/P2.stderr" | mkfx X1 1 "" -
mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
{ printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -
#  X9/X10: twenty lines of streamed text, then a complete codex header block QUOTED from a file the review read (the shape
#  N1's stderr carries from line 5528) -- and no opening header at all
latehdr() {    # $1 the quoted block's model
    i=1; while [ $i -le 20 ]; do printf 'streamed line %d of a file the review read\n' $i; i=$((i + 1)); done
    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$1"
    printf 'reasoning effort: ultra\n--------\nuser\nthe quoted session brief\n'
}
latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -
#  v4 (the v3 pass): the window's and the cap's EDGES, the real warning-prefixed header, a real doubled refusal, one wall line
hdrat() {    # $1 lines before the banner, $2 the block's model -- a CLOSED opening block whose banner is line $1+1
    i=1; while [ $i -le "$1" ]; do printf 'startup line %d\n' $i; i=$((i + 1)); done
    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$2"
    printf 'reasoning effort: ultra\n--------\nuser\nthe session brief\n'
}
hdrat 10 gpt-6-other | mkfx W12 0 "$T/ans_verdict.txt" -      # banner line 11, first rule line 12: inside the window
hdrat 11 gpt-6-other | mkfx W13 0 "$T/ans_verdict.txt" -      # banner line 12, first rule line 13: outside it
head -14 "$REPO/regress/artifacts/ppcrldimimask/codex_book1check_20260910.err" | mkfx X13 0 "$T/ans_verdict.txt" -
capat() {    # $1 body lines before the block's `model:' line -- an UNTERMINATED opening block
    printf 'OpenAI Codex v0.153.4\n--------\n'
    i=1; while [ $i -le "$1" ]; do printf 'body line %d\n' $i; i=$((i + 1)); done
    printf 'model: gpt-6-other\nreasoning effort: ultra\n'
    i=1; while [ $i -le 20 ]; do printf 'streamed line %d\n' $i; i=$((i + 1)); done
}
capat 29 | mkfx K30 0 "$T/ans_verdict.txt" -                  # the model is body line 30: read
capat 30 | mkfx K31 0 "$T/ans_verdict.txt" -                  # the model is body line 31: not read
mkfx R2 1 "" "$HERE/fx/R2.stderr"
mkfx W1L 1 "" "$T/wall_line.txt"
mkfx ANS 0 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
#  v5 (the v4 pass): the rc pass-through, the gate's and the empty test's 1-byte edge, the real coloured header, each pattern
#  alternative and the case fold, a non-SGR strip, each adjacent pair of the exit cascade, and every awk guard and constant
mkfx RC1A 1 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
mkfx RC3A 3 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
mkfx RC2W 2 "$T/ans_verdict.txt" "$HERE/fx/P1.stderr"
mkfx B1G 0 "$T/ans_1byte.txt" "$HERE/fx/P1.stderr"
mkfx B1E 0 "$T/ans_1byte.txt" "$T/hdr_astra.txt"
head -12 "$HERE/fx/R2.stderr" | mkfx CH 0 "$T/ans_verdict.txt" -      # its opening block only: `ESC[1mmodel:ESC[0m gpt-6-astra'
printf 'ERROR: I cannot help with that request.\n' | mkfx RF1 1 "" -
printf "ERROR: I can't help with that request.\n" | mkfx RF2 1 "" -
printf "ERROR: I won't help with that request.\n" | mkfx RF3 1 "" -
printf 'ERROR: THIS CONTENT WAS FLAGGED FOR POSSIBLE CYBERSECURITY RISK.\n' | mkfx RFC 1 "" -
printf 'ERROR: quota exceeded for this workspace.\n' | mkfx WL1 1 "" -
printf 'ERROR: rate limit reached; retry in 60s.\n' | mkfx WL2 1 "" -
printf 'ERROR: not authenticated -- run codex login.\n' | mkfx WL3 1 "" -
printf "ERROR: You've hit your USAGE LIMIT.\n" | mkfx WLC 1 "" -
printf '%s\n' "${ESC}[2K${ESC}[1;31mERROR:${ESC}[0m This content was flagged for possible cybersecurity risk." | mkfx CSI 1 "" -
cat "$T/refusal_line.txt" "$T/wall_line.txt" | mkfx RW 1 "" -
cat "$T/hdr_other.txt" "$T/refusal_line.txt" | mkfx RI 1 "" -
cat "$T/hdr_other.txt" "$T/wall_line.txt" | mkfx WI 1 "" -
mkfx EM 0 "" "$T/hdr_other.txt"
mkfx IR 1 "$T/ans_verdict.txt" "$T/hdr_other.txt"
printf 'OpenAI Codex v0.153.4\n--------\nmodel:\t  gpt-6-astra \r\nreasoning effort: ultra\n--------\n' | mkfx WS 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nfallback model: gpt-6-other\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx MA 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
    | mkfx TM 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nreasoning effort: ultra\n--------\nuser\nmodel: gpt-6-other\n' \
    | mkfx NM 0 "$T/ans_verdict.txt" -
printf '> OpenAI Codex v0.1 (a quoted transcript)\n--------\nmodel: gpt-6-other\n--------\n' > "$T/ba_pre.txt"
cat "$T/ba_pre.txt" "$T/hdr_astra.txt" | mkfx BA 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nOpenAI Codex v0.1 (quoted)\n--------\nmodel: gpt-6-other\n--------\n' \
    | mkfx HB 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n-------\nmodel: gpt-6-other\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx R7A 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\n-------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx R7B 0 "$T/ans_verdict.txt" -
#  v6 (the v5 pass): each override's VALUE honoured at its own call, the fallback's own rc, a re-run into a used dir, a missing
#  parent, a non-empty refused stdout, separators off column 0, a parameterless CSI, `model:' with no space, codex's own rc 7, a
#  near-miss banner, nine-dash rules
hdr m-fallback | mkfx OV2 0 "$T/ans_verdict.txt" -
hdr gpt-daybreak-blue-latest | mkfx FR3 3 "$T/ans_verdict.txt" -
printf 'STALE ANSWER from an earlier run of this tag\n' > "$T/seed_stdout"
hdr gpt-6-stale > "$T/seed_stderr"
printf 'A partial answer the content filter cut off.\n' > "$T/ans_partial.txt"
mkfx RN1 1 "$T/ans_partial.txt" "$HERE/fx/P2.stderr"
printf 'OpenAI Codex v0.153.4\nx --------\n--------\nworkdir: x\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
    | mkfx SP1 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nnote: a -------- b\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
    | mkfx SP2 0 "$T/ans_verdict.txt" -
printf '%s\n' "${ESC}[mERROR: This content was flagged for possible cybersecurity risk." | mkfx CZ 1 "" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel:gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx WZ 0 "$T/ans_verdict.txt" -
mkfx R7X 7 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
{ printf 'OpenAI notice: a deprecation warning\n--------\nmodel: gpt-6-other\n--------\n'; cat "$T/hdr_astra.txt"; } \
    | mkfx BN 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n---------\nmodel: gpt-6-other\nreasoning effort: ultra\n---------\n' | mkfx R9A 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\n---------\nmodel: gpt-6-other\n' | mkfx R9B 0 "$T/ans_verdict.txt" -
#  v7 (the v6 pass): codex's own rc 8; a two-line brief; stale refused files; every strip-class member in one line
mkfx R8X 8 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
printf 'control brief\nsecond line of the brief\n' > "$T/brief_multi.md"
printf 'STALE refused stdout from an earlier run\n' > "$T/seed_refused_txt"
printf 'STALE refused stderr from an earlier run\n' > "$T/seed_refused_err"
csx=""; for L in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z; do
    csx="$csx${ESC}[1$L"; done
printf '%s%sERROR: This content was flagged for possible cybersecurity risk.\n' "${ESC}[0;1;2;3;4;5;6;7;8;9m" "$csx" \
    | mkfx CSX 1 "" -

#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL); logs its arguments to $FX_ARGS, its working
#  directory to $FX_ARGS.cwd and the first 60 bytes of its stdin to $FX_ARGS.stdin
cat > "$T/fakecodex.sh" <<'EOF'
#!/bin/bash
D="$FX"; prev=""
for a in "$@"; do
    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
    prev="$a"
done
if [ -n "${FX_ARGS:-}" ]; then
    { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
    pwd >> "$FX_ARGS.cwd"
    head -c 60 >> "$FX_ARGS.stdin"
fi
cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
EOF
chmod +x "$T/fakecodex.sh"
#  the default-path fake under the scratch HOME: it marks the run, then is the same fake (the tracked launcher names only this
#  path; the after launcher reaches it only when CX_CODEX_BIN is unset or empty)
DEFBIN="$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
mkdir -p "$DEFBIN"
printf '#!/bin/bash\n[ -n "${FX_ARGS:-}" ] && echo DEFAULT >> "$FX_ARGS.default"\nexec bash "%s" "$@"\n' "$T/fakecodex.sh" > "$DEFBIN/codex"
chmod +x "$DEFBIN/codex"
printf 'control brief\n' > "$T/brief.md"
printf '%30000s' '' | tr ' ' b > "$T/brief30000.md"
printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"
printf 'STDIN MARKER -- codex must never read this\n' > "$T/stdin_marker"

pass=0; total=0
run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit (? = record only, counted as a failure), then env
    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
    local out="$T/out_${row}_${lab}"
    case " $* " in *" CX_AUP_MODEL= "*) : > "$T/disabled_${row}_${lab}" ;; esac
    #  v6: SEED=1 pre-seeds the out dir with a stale answer and a stale header (RS); NEST=1 puts it two levels below a
    #  missing parent (MP).  Both reach the launcher's environment too, where nothing reads them.
    case " $* " in *" SEED=1 "*) mkdir -p "$out"; cp "$T/seed_stdout" "$out/codex_${row}.txt"; cp "$T/seed_stderr" "$out/codex_${row}.err" ;; esac
    case " $* " in *" NEST=1 "*) out="$out/nest/ed" ;; esac
    #  v7: SEEDREF=1 pre-seeds the REFUSED destinations with stale files (RN2); TAG_OVERRIDE gives the run a tag other than
    #  its row name (TG); BRIEF_OVERRIDE (v5) a brief other than the default
    case " $* " in *" SEEDREF=1 "*) mkdir -p "$out"; cp "$T/seed_refused_txt" "$out/codex_${row}.refused.txt"
        cp "$T/seed_refused_err" "$out/codex_${row}.refused.err" ;; esac
    local tag="$row"
    case " $* " in *" TAG_OVERRIDE="*) for kv in "$@"; do case "$kv" in TAG_OVERRIDE=*) tag="${kv#TAG_OVERRIDE=}" ;; esac; done ;; esac
    ( export HOME="$T/home" CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
      for kv in "$@"; do export "$kv"; done
      [ "${UNSET_CODEX_BIN:-}" = 1 ] && unset CX_CODEX_BIN
      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$tag" < "$T/stdin_marker" ) > "$T/log_${row}_${lab}.txt" 2>&1
    local got=$?
    echo "$got" > "$T/exit_${row}_${lab}"
    total=$((total + 1))
    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
    printf '%-4s %-7s exit=%-3s want=%-3s %s\n' "$row" "$lab" "$got" "$want" "$ok"
    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
}
three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
    if [ "$ONLY" != 1 ]; then
        run "$row" tracked "$TRACKED" "$wt" "$@"
        run "$row" before "$BEFORE" "$wb" "$@"
    fi
    run "$row" after "$AFTER" "$wa" "$@"
}
check() {    # $1 label, $2 0/1 result
    total=$((total + 1))
    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
}

echo "# cxlaunch landing controls (v7), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
three P1 8 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
three P2 7 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
three N1 8 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
three N2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three N3 6 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
three N4 8 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
three Q1 7 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
three Q2 8 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
three Q3 6 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
three A1 6 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
three M1 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three M2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three D1 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three D2 7 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
three X1 6 6 6 FX="$T/fx/X1" CX_AUP_MODEL=
three X2 8 0 0 FX="$T/fx/X2" CX_AUP_MODEL=
three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
three W12 0 0 5 FX="$T/fx/W12" CX_AUP_MODEL=
three W13 0 0 0 FX="$T/fx/W13" CX_AUP_MODEL=
three X13 0 0 5 FX="$T/fx/X13" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three K30 0 0 5 FX="$T/fx/K30" CX_AUP_MODEL=
three K31 0 0 0 FX="$T/fx/K31" CX_AUP_MODEL=
three R2X 6 6 7 FX="$T/fx/R2" CX_AUP_MODEL=
three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5, EO, FR and
#  RN and RN2 (refusals), set to a NON-default model by OV, and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
#  GLM 5.3, v4 pass.)
three FB1 8 0 0 FX="$T/fx/N1"
three FB2 8 8 8 FX="$T/fx/P1"
three X14 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30000.md"
three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"
#  v5 rows
three RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=
three RC3A 3 3 3 FX="$T/fx/RC3A" CX_AUP_MODEL=
three RC2W 8 8 8 FX="$T/fx/RC2W" CX_AUP_MODEL=
three B1G 8 0 0 FX="$T/fx/B1G" CX_AUP_MODEL=
three B1E 0 0 0 FX="$T/fx/B1E" CX_AUP_MODEL=
three D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest
three CH 0 0 5 FX="$T/fx/CH" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three DP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= UNSET_CODEX_BIN=1
three EO 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest CX_CODEX_BIN= CX_MODEL= CX_EFFORT= CX_AUP_EFFORT=
three RF1 7 7 7 FX="$T/fx/RF1" CX_AUP_MODEL=
three RF2 7 7 7 FX="$T/fx/RF2" CX_AUP_MODEL=
three RF3 7 7 7 FX="$T/fx/RF3" CX_AUP_MODEL=
three RFC 7 7 7 FX="$T/fx/RFC" CX_AUP_MODEL=
three WL1 8 8 8 FX="$T/fx/WL1" CX_AUP_MODEL=
three WL2 8 8 8 FX="$T/fx/WL2" CX_AUP_MODEL=
three WL3 8 8 8 FX="$T/fx/WL3" CX_AUP_MODEL=
three WLC 8 8 8 FX="$T/fx/WLC" CX_AUP_MODEL=
three CSI 6 6 7 FX="$T/fx/CSI" CX_AUP_MODEL=
three RW 7 7 7 FX="$T/fx/RW" CX_AUP_MODEL=
three RI 7 7 7 FX="$T/fx/RI" CX_AUP_MODEL=
three WI 8 8 8 FX="$T/fx/WI" CX_AUP_MODEL=
three EM 6 6 6 FX="$T/fx/EM" CX_AUP_MODEL=
three IR 1 1 5 FX="$T/fx/IR" CX_AUP_MODEL=
three WS 0 0 0 FX="$T/fx/WS" CX_AUP_MODEL=
three MA 0 0 0 FX="$T/fx/MA" CX_AUP_MODEL=
three TM 0 0 0 FX="$T/fx/TM" CX_AUP_MODEL=
three NM 0 0 0 FX="$T/fx/NM" CX_AUP_MODEL=
three BA 0 0 5 FX="$T/fx/BA" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three HB 0 0 0 FX="$T/fx/HB" CX_AUP_MODEL=
three R7A 0 0 0 FX="$T/fx/R7A" CX_AUP_MODEL=
three R7B 0 0 5 FX="$T/fx/R7B" CX_AUP_MODEL= CX_MODEL=gpt-6-other
#  v6 rows (the tracked and before expectations recorded from RECEIPT_v6_calibration.txt; the after ones written first)
three OV 7 0 0 FX="$T/fx/P2" FX2="$T/fx/OV2" FX2_MODEL=m-fallback CX_MODEL=m-primary CX_EFFORT=low CX_AUP_MODEL=m-fallback CX_AUP_EFFORT=high
three FR 7 3 3 FX="$T/fx/P2" FX2="$T/fx/FR3" FX2_MODEL=gpt-daybreak-blue-latest
three RS 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= SEED=1
three MP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= NEST=1
three RN 7 0 0 FX="$T/fx/RN1" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three SP1 0 0 5 FX="$T/fx/SP1" CX_AUP_MODEL=
three SP2 0 0 5 FX="$T/fx/SP2" CX_AUP_MODEL=
three CZ 6 6 7 FX="$T/fx/CZ" CX_AUP_MODEL=
three WZ 0 0 0 FX="$T/fx/WZ" CX_AUP_MODEL=
three R7X 7 7 7 FX="$T/fx/R7X" CX_AUP_MODEL=
three BN 0 0 0 FX="$T/fx/BN" CX_AUP_MODEL=
three R9A 0 0 5 FX="$T/fx/R9A" CX_AUP_MODEL=
three R9B 0 0 0 FX="$T/fx/R9B" CX_AUP_MODEL=
#  v7 rows (the tracked and before expectations recorded from RECEIPT_v7_calibration.txt; the after ones written first)
three R8X 8 8 8 FX="$T/fx/R8X" CX_AUP_MODEL=
three MB 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief_multi.md"
three RN2 7 0 0 FX="$T/fx/RN1" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest SEEDREF=1
three TG 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= TAG_OVERRIDE=tg_lower
three CSX 6 6 7 FX="$T/fx/CSX" CX_AUP_MODEL=

#  E0: the fake ran for every row of every column but X15's, and never for X15's (it must exit 9 BEFORE codex); the run count is
#  pinned, so a deleted row is visible.  The other aggregate checks read the AFTER runs; each pins its own denominator.
cols=3; [ "$ONLY" = 1 ] && cols=1
nruns=$(ls "$T"/log_* 2>/dev/null | wc -l)
miss=""; extra=""
for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}
    case "$b" in X15_*) [ -e "$T/args_$b" ] && extra="$extra $b" ;; *) [ -s "$T/args_$b" ] || miss="$miss $b" ;; esac
done
[ "$nruns" = $((NROWS * cols)) ] && [ -z "$miss" ] && [ -z "$extra" ]; check "E0  all  the fake codex was reached by every run but X15's, and by none of X15's ($NROWS rows x $cols = $nruns of $((NROWS * cols)), pinned)${miss:+ -- NOT reached:$miss}${extra:+ -- X15 REACHED it:$extra}" $?
nafter=0; dbad=""; sbad=""; ns=0; cbad=""; nc=0; pbad=""; fbad=""; nfd=0
for f in "$T"/exit_*_after; do r=${f##*/exit_}; r=${r%_after}; nafter=$((nafter + 1))
    case "$r" in
        DP|EO) [ -e "$T/args_${r}_after.default" ] || dbad="$dbad $r(not reached)" ;;
        *) [ -e "$T/args_${r}_after.default" ] && dbad="$dbad $r" ;;
    esac
    if [ -e "$T/args_${r}_after.stdin" ]; then ns=$((ns + 1)); [ -s "$T/args_${r}_after.stdin" ] && sbad="$sbad $r"; fi
    if [ -e "$T/args_${r}_after.cwd" ]; then nc=$((nc + 1))
        while IFS= read -r d; do [ "$(printf '%s' "$d" | tr 'A-Z' 'a-z')" = /c/documentnosnc/cc/gxemul ] || cbad="$cbad $r"; done < "$T/args_${r}_after.cwd"
    fi
    e=$(cat "$f"); L="$T/log_${r}_after.txt"
    a=$(grep -c 'seat answered' "$L"); l=$(grep -c 'The answer is LOST' "$L"); b=$(grep -c 'answered by: ' "$L"); u=$(grep -c 'model UNVERIFIED' "$L")
    w=$(grep -c 'SEAT WALLED' "$L")    # v6: status.sh counts it (GPT-6 Astra, v5 pass)
    case "$e" in
        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ "$w" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
        #  v6: LOST is the REFUSAL exit's; codex's own rc 7 prints `codex exited 7' and no LOST (GPT-6 Astra, v5 pass)
        #  v7: codex's OWN rc 7 and rc 8 are decided by the ROW (R7X, R8X), never by the launcher's text -- v6 read
        #  `codex exited 7' from the log, and a refusal echo rewritten to it passed (GPT-6 Astra, v6 pass)
        7) if [ "$r" = R7X ]; then { [ "$l" = 0 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"
           else { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r"; fi ;;
        8) if [ "$r" = R8X ]; then { [ "$w" = 0 ] && [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r"
           else { [ "$w" -ge 1 ] && [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r"; fi ;;
        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ] && [ "$w" = 0 ]; } || pbad="$pbad $r" ;;
    esac
    if [ -e "$T/disabled_${r}_after" ] && [ "$r" != X15 ]; then nfd=$((nfd + 1))
        [ "$(grep -c '^CALL$' "$T/args_${r}_after" 2>/dev/null)" = 1 ] || fbad="$fbad $r"
    fi
done
[ "$nafter" = "$NROWS" ] && [ -z "$dbad" ]; check "E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of $nafter)${dbad:+ -- wrong:$dbad}" $?
[ "$ns" = $((NROWS - 1)) ] && [ -z "$sbad" ]; check "SI  after  no after run's codex read the stdin the launcher was fed ($ns runs that reached codex, of $((NROWS - 1)))${sbad:+ -- READ IT:$sbad}" $?
[ "$nc" = $((NROWS - 1)) ] && [ -z "$cbad" ]; check "CWD after  every after run's codex started in the project root ($nc of $((NROWS - 1)))${cbad:+ -- elsewhere:$cbad}" $?
[ "$nfd" = "$NFD" ] && [ -z "$fbad" ]; check "FD  after  every row that sets CX_AUP_MODEL empty made exactly one call ($nfd rows, $NFD pinned)${fbad:+ -- more:$fbad}" $?
[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff the refusal exit 7, 'SEAT WALLED' iff the wall exit 8 -- codex's own 7 and 8 (R7X, R8X) by ROW -- 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
#  v6: the NUMBERS too -- v5 read only the format, and `stdout=$(wc -c < "$ERR")' passed (GPT-6 Astra, v5 pass)
logline() {    # $1 fixture dir, $2 model, $3 effort (default ultra) -- the exact line the launcher must log for one call
    printf 'codex rc=%s   stdout=%s b   stderr=%s b   asked: %s / %s\n' "$(cat "$1/rc")" "$(wc -c < "$1/stdout")" "$(wc -c < "$1/stderr")" "$2" "${3:-ultra}"
}
logline "$T/fx/N1" gpt-6-astra > "$T/want_LOG_N1"; { logline "$T/fx/P2" gpt-6-astra; logline "$T/fx/DB_OK" gpt-daybreak-blue-latest; } > "$T/want_LOG_D1"
logline "$T/fx/RC3A" gpt-6-astra > "$T/want_LOG_RC3A"
#  v7: OV's two lines -- its NON-default models and efforts; `asked: $1 / ultra' passed v6's LOG, whose runs all asked ultra
#  (GPT-6 Astra, v6 pass)
{ logline "$T/fx/P2" m-primary low; logline "$T/fx/OV2" m-fallback high; } > "$T/want_LOG_OV"
lbad=""; for r in N1 D1 RC3A OV; do grep '^codex rc=' "$T/log_${r}_after.txt" | cmp -s - "$T/want_LOG_$r" || lbad="$lbad $r"; done
[ -z "$lbad" ]; check "LOG after  the 'codex rc=N   stdout=N b   stderr=N b   asked: M / E' lines of N1, D1 (both calls), RC3A and OV (both calls, non-default models and efforts), WHOLE: the format the censuses parse and each number the fixture's own${lbad:+ -- wrong:$lbad}" $?
#  v7 RXM: each raw-status message names ITS OWN rc -- `codex exited 7 --' hardcoded kept RC1A, RC3A and FR at their exits and
#  passed v6, whose only check of the number was R7XL against 7 (GPT-6 Astra, v6 pass)
xbad=""; for rn in RC1A:1 RC3A:3 FR:3 R7X:7 R8X:8; do r=${rn%:*}; n=${rn#*:}
    grep -qxF "  *** codex exited $n -- NOT a clean run." "$T/log_${r}_after.txt" || xbad="$xbad $r"; done
[ -z "$xbad" ]; check "RXM after  RC1A, RC3A, FR, R7X and R8X each say 'codex exited N -- NOT a clean run.' with N their own rc${xbad:+ -- wrong:$xbad}" $?
[ "$(ls "$T/out_N1_after" | wc -l)" = 2 ] && cmp -s "$T/out_N1_after/codex_N1.txt" "$T/fx/N1/stdout" && cmp -s "$T/out_N1_after/codex_N1.err" "$T/fx/N1/stderr"; check "N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr" $?
grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_N1_after.txt"; check "N1V after  N1 is credited to gpt-6-astra" $?
wbad=""; for r in WS MA TM WZ BN; do grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_${r}_after.txt" || wbad="$wbad $r"; done
[ -z "$wbad" ]; check "WMT after  WS, MA, TM, WZ and BN verify gpt-6-astra (not UNVERIFIED)${wbad:+ -- wrong:$wbad}" $?
#  content, not exit status -- on the AFTER logs
for r in M2 X6 X9 W13 K31 NM HB R9B; do
    grep -q 'model UNVERIFIED' "$T/log_${r}_after.txt" && ! grep -q 'answered by:' "$T/log_${r}_after.txt"; check "$r  after  says model UNVERIFIED and names no model" $?
done
cmp -s "$T/out_D1_after/codex_D1.refused.txt" "$T/fx/P2/stdout" && cmp -s "$T/out_D1_after/codex_D1.refused.err" "$T/fx/P2/stderr" \
    && cmp -s "$T/out_D1_after/codex_D1.txt" "$T/fx/DB_OK/stdout" && cmp -s "$T/out_D1_after/codex_D1.err" "$T/fx/DB_OK/stderr" \
    && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1R after  refused run kept byte-for-byte as .refused.txt/.err, Daybreak's run as .txt/.err, Daybreak credited" $?
[ "$(grep -c '^CALL$' "$T/args_FB1_after" 2>/dev/null)" = 1 ] && ! ls "$T/out_FB1_after"/*.refused.* >/dev/null 2>&1; check "FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused" $?
[ "$(grep -c '^CALL$' "$T/args_FB2_after" 2>/dev/null)" = 1 ]; check "FB2 after  the fallback on, a wall: ONE call" $?
[ "$(grep -c '^CALL$' "$T/args_D4_after" 2>/dev/null)" = 2 ]; check "D4  after  refused, then refused on Daybreak: EXACTLY two calls" $?
[ "$(grep -c '^CALL$' "$T/args_D3_after" 2>/dev/null)" = 2 ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D3_after.txt"; check "D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited" $?
[ "$(grep -c '^CALL$' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked ON Daybreak and refused: ONE call, no re-run on the same model" $?
[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?
grep -qF "codex's header says gpt-6-astra" "$T/log_CH_after.txt"; check "CH  after  the coloured header is read: the log names gpt-6-astra as the model that ran" $?
#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
callseq() {    # $1 model -- the sequence one call must receive
    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
}
callseq gpt-6-astra > "$T/want_E1"
{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
cmp -s "$T/want_E2" "$T/args_EO_after"; check "EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2" $?
cmp -s "$T/want_E1" "$T/args_DP_after"; check "DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1" $?
#  v6 content checks
callseq2() {    # $1 model, $2 effort
    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
    printf 'ARG model_reasoning_effort=%s\nARG control brief\n' "$2"
}
{ callseq2 m-primary low; callseq2 m-fallback high; } > "$T/want_OV"
cmp -s "$T/want_OV" "$T/args_OV_after" && grep -qF 'seat answered. (answered by: m-fallback)' "$T/log_OV_after.txt"; check "OVA after  CX_MODEL, CX_EFFORT, CX_AUP_MODEL, CX_AUP_EFFORT set to NON-default values: each reaches its own call, both compared whole; the fallback credited" $?
[ "$(ls "$T/out_RS_after" | wc -l)" = 2 ] && cmp -s "$T/out_RS_after/codex_RS.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_RS_after/codex_RS.err" "$T/fx/ANS/stderr"; check "RSF after  a re-run into a dir holding a stale answer and a stale header: both files TRUNCATED, byte-for-byte the new run's" $?
cmp -s "$T/out_MP_after/nest/ed/codex_MP.txt" "$T/fx/ANS/stdout" && cmp -s "$T/out_MP_after/nest/ed/codex_MP.err" "$T/fx/ANS/stderr"; check "MPF after  an out dir two levels below a missing parent is created, and the run lands in it" $?
cmp -s "$T/out_RN_after/codex_RN.refused.txt" "$T/fx/RN1/stdout" && cmp -s "$T/out_RN_after/codex_RN.refused.err" "$T/fx/RN1/stderr" \
    && cmp -s "$T/out_RN_after/codex_RN.txt" "$T/fx/DB_OK/stdout"; check "RNF after  a NON-EMPTY refused stdout is kept byte-for-byte as .refused.txt; Daybreak's answer is .txt" $?
grep -qF '*** codex exited 7 ' "$T/log_R7X_after.txt" && ! grep -q 'The answer is LOST' "$T/log_R7X_after.txt" && ! grep -q 'seat answered' "$T/log_R7X_after.txt"; check "R7XL after  codex's own rc 7 with an answer: 'codex exited 7', and neither LOST nor answered" $?
#  v7 content checks
grep -qF '*** codex exited 8 ' "$T/log_R8X_after.txt" && ! grep -q 'SEAT WALLED' "$T/log_R8X_after.txt" && ! grep -q 'seat answered' "$T/log_R8X_after.txt"; check "R8XL after  codex's own rc 8 with an answer: 'codex exited 8', and neither SEAT WALLED nor answered" $?
{ printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG gpt-6-astra\nARG -c\n'
  printf 'ARG model_reasoning_effort=ultra\nARG control brief\nsecond line of the brief\n'; } > "$T/want_MB"
cmp -s "$T/want_MB" "$T/args_MB_after"; check "MBA after  a TWO-line brief reaches codex whole, as one argument" $?
cmp -s "$T/out_RN2_after/codex_RN2.refused.txt" "$T/fx/RN1/stdout" && cmp -s "$T/out_RN2_after/codex_RN2.refused.err" "$T/fx/RN1/stderr"; check "RN2F after  the refused files REPLACE stale ones already in the out dir, byte-for-byte this run's" $?
[ "$(ls "$T/out_TG_after" | tr '\n' ' ')" = "codex_tg_lower.err codex_tg_lower.txt " ] && cmp -s "$T/out_TG_after/codex_tg_lower.txt" "$T/fx/ANS/stdout"; check "TGF after  a lowercase tag names its files exactly as given" $?
echo "CONTROLS: $pass/$total as expected"
echo "CXLAND_CONTROLS_DONE"
[ "$pass" = "$total" ]
