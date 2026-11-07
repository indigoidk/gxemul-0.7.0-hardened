# Reading task: hrec_cxlaunchquotation (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECCXLAUNCHQUOTATION-3d77` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `cxlaunchquotation` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `cxlaunchquotation` (state `held`)

**title:** tools/cxlaunch.sh's wall check greps the seat's ANSWER for 'quota', which matches 'quotation': a complete answer is reported SEAT WALLED and the launcher exits 8

**state_note (head):** [2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-17 (7aa2c41f, and its hash-follow 2951694f) while its review stage (the V6 and V7 passes of the tools/cxlaunch.sh landing) held a Fable wall written as untokened prose; that entry now carries the HELD token and the row is held until Fable answers -- the question is in hold_question.  Rulings and commits proceed meanwhile (the owner's 2026-10-17 directive); the close does not.  ||  filed 2026-10-09: measured on GPT-6 Astra's check of the asiceventaddr convergence -- a complete 10,466-byte answer with its verdict line, no `ERROR:` line on stderr, and the launcher printed 'SEAT WALLED' (LAUNCH_RC=8) because the answer's own sentence '... its quotation must retain ...' matched `grep -ic 'quota'` (the answer: regress/artifacts/fablequeue8n_20261009/astra_confirm/codex_astra_asicconverge.txt; the launcher's own output: cxlaunch_asicconverge_stdout.txt beside it).  tools/cxlaunch.sh:44 builds `wall` from the `ERROR:` lines PLUS the whole stdout, so any answer that uses the words quota / quotation / rate limit / usage limit reads as a wall -- the carrier's quoting-re-arms-the-reader class, one level down (the script's own comment at :33-41 diagnoses the stderr half and kept the stdout half).  Fix: word-anchor the pattern and test stdout only when no verdict line is present; owes controls both ways (a real 403/quota notice still reds; an answer containing 'quotation' does not).  LOW: a human reads the answer; an unattended runner would discard it.

[2026-10-17] CLOSED by the tools/cxlaunch.sh landing -- and the fix this note prescribes ("word-anchor the pattern and test stdout only when no verdict line is present") was REPLACED by the three-seat ruling's production rule, not applied: stdout is never grep

**hold_question:** REVIEW (held 2026-10-18 by fableheldform; Fable walled on V6 and V7, 2026-10-17): regress/artifacts/cxlaunchland_20261016/v6pass/packet_cxland_v6_FABLE.md and v7pass/packet_cxland_v7_FABLE.md -- does the landed launcher (7aa2c41f) stand?  ||  REGRESS (held 2026-10-17 at the tools/cxlaunch.sh landing): does regress/artifacts/cxlaunchland_20261016/RECEIPT_v7.txt still run the TRACKED file the landing replaced, the farm copy and the landed launcher against the same fixtures and get the recorded exits -- in particular N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the Daybreak fallback), X8 6 -> 8 (a NUL in stderr), the v4 edge rows (W12/W13, K30/K31, R2X/D3, W1L, FB1/FB2, X14/X15) and the v5 rows (RC1A/RC3A codex's own rc, D5, FD, CH, SI, N1F, D1R, DP/EO/E0b, the alternatives RF1-R

## The record -- commit message(s)

### commit `7aa2c41f 2026-10-17`

```text
cxlaunchquotation + cxlaunchdaybreak: the codex launcher lands in tools/cxlaunch.sh -- an rc-0 answer is never scored WALLED or REFUSED for what its stderr quotes, an Astra content-filter refusal re-runs once on Daybreak, a different model in codex's opening header exits 5; controls 289/289, kill table 144/144; one coverage row filed

Ruled before any code by Fable 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md F1):
codex's ^ERROR: lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall words.
Every real wall and refusal on record is rc 1 with an empty stdout and every rc-0 run carries an answer (474 launch-log
rows: 440 rc 0 with stdout, 34 rc 1 empty -- CENSUS_v5.txt).

tools/cxlaunch.sh (+159 -25): until now the tracked file ran Astra at max with the 2026-09-07 classifier while most farm
jobs ran an untracked scratchpad copy.  The landed file strips ANSI colour and reads stderr with grep -a before the
^ERROR: anchor; re-runs a content-filter refusal on Astra ONCE on gpt-daybreak-blue-latest (the refused run kept as
.refused.*, the answer credited to Daybreak; not on an answer, a wall, a refusal asked of Daybreak, or with the fallback
set empty); reads the model ONLY from codex's opening header block and exits 5 on a mismatch ("model UNVERIFIED", exit 0,
when an answered run has no model line there); runs at effort ultra.  Its header records the residuals, the exit codes
its callers read (run_pack_body.sh, status.sh), codex's own rc 7 and 8, and what a missing or relative brief really does.

tools/pipeline/check_probe_wiring.py: its MANIFEST classifies the landing's 15 preserved .py artifacts (the mutant
writers and the Fable seat's control-variant builders TOOL; the censuses and seat measurements RESEARCH); none is a
gated detector.  Pretested before this hook: R PASS on a throwaway index, its selftest 22/22, L ATTRIBUTION_PASS.

Controls regress/artifacts/cxlaunchland_20261016/run_controls_v7.sh -- every row drives the TRACKED file (the pre-fix
column), the farm copy and the landed file against a fake codex replaying a fixture: 289/289 (RECEIPT_v7.txt), e.g.
N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8 (a NUL in stderr), IR 1 -> 5 (a
different model).  Its CONTRACT is derived from the file and rows each listed decision's values and used states.  Kill
table run_mutants_v7.sh: 144/144 as recorded (KILLTABLE_v7.txt; per-mutant tallies identical to the table the v7 pass
reviewed, kept as *_md5_80b48191.txt).

Seven passes on the landed file on the owner's four-seat roster.  V7 (the closing pass, findings shared): GPT-6 Astra
SHIP WITH CHANGES (5), Grok 4.7 CLOSE, GLM 5.3 CLOSE (after one HTTP 502 re-fire) -- zero floor breaches on each
denominator.  Fable 5.1 walled on a usage limit: a SEAT FAILURE, its stage HELD by owner ruling 2026-10-17 ("hold any
fable adjucation"), the question in the rows' hold_question.  The one escape measured past the 289 (wc -w for the empty
test's wc -c, 123/123 after-column) is FILED as coverage debt (LOW, clause (e)) with GLM's PK row-name residual.

Records: both rows CLOSED (witness harness:...RECEIPT_v7.txt), their REGRESS reviews HELD for the flagship; the
2026-09-26 cxlaunchwallfp filing merged with its tail-key fix withdrawn; OUTSTANDING_BUGS.md's stale launcher statements
bracketed by content; RULINGS_C_records.md's drifted citations re-cited by id; the relative-brief road filed on the
existing empty-prompt row, whose NUL half this landing closes and whose fix stays #544's (the peer's round, which now
rebases on this file).  matrix.html re-rendered; fable_queue.md's held block regenerated.  This commit's own hash
follows in the next records commit.  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster.  No src/
touched.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## The record -- CHANGELOG block(s)

### CHANGELOG.md lines 3546-3551 (HEAD 8d9df658)

```text
 3546| # Records, 2026-10-17: `cxlaunchquotation` and `cxlaunchdaybreak` name their closing commit 7aa2c41f
 3547| 
 3548| The landing commit 7aa2c41f closed the row(s) and cannot name itself; this adds it to each `commits` field: `cxlaunchquotation` (now `7aa2c41f`); `cxlaunchdaybreak` (now `7aa2c41f`).
 3549| check_commit_attribution grades a closed row whose subject-naming commit is unlisted HARD on the next commit, the
 3550| peer session's included, so this lands at once and alone.  Ledger, matrix and this block only.
 3551| 
```

### CHANGELOG.md lines 3552-3645 (HEAD 8d9df658)

```text
 3552| # `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- an rc-0 run with a non-empty stdout is never scored WALLED or REFUSED for what its stderr quotes, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5 (after the refusal, wall and empty-stdout checks); the controls row each listed decision's VALUES and used states, not only its defaults (v7: 289 checks, 144 mutants)
 3553| 
 3554| **Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
 3555| F1): codex's `^ERROR:` lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall
 3556| words -- the discriminator is the exit status and the answer, which quoted text cannot forge.  Every real wall and refusal
 3557| on record is rc 1 with an empty stdout, and every rc-0 run carries an answer: 474 launch-log rows, 440 rc 0 with stdout and
 3558| 34 rc 1 empty, nothing else (`CENSUS_v5.txt`).
 3559| 
 3560| * `tools/cxlaunch.sh`: until this landing the tracked file ran Astra at `max` with the 2026-09-07 classifier while most farm
 3561|   jobs ran an untracked scratchpad copy -- and the carrier described the copy's behaviour as the tracked file's.  The landed
 3562|   file: ANSI colour stripped and `grep -a` before the `^ERROR:` anchor (a real coloured refusal read exit 6 unstripped; a
 3563|   real NUL-bearing wall read exit 6 without `-a`); the Daybreak fallback (`gpt-daybreak-blue-latest`, the refused run kept
 3564|   as `.refused.*`, the answer credited to Daybreak; not fired on an answer, a wall, a refusal asked of Daybreak itself, or
 3565|   with the fallback set empty); the model read ONLY from codex's OPENING header block -- banner and first rule by line 12,
 3566|   the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch; "model UNVERIFIED", exit
 3567|   0, when a run that ANSWERED -- rc 0, a non-empty stdout, no earlier exit -- has no model line in an opening block); the
 3568|   effort `ultra`.  Its header records the residuals (N4 and its refusal
 3569|   twin), exit 5's novelty to the pack runner and the log phrases its callers read (`run_pack_body.sh` and `status.sh`),
 3570|   codex's own rc 7 and 8 (neither a refusal nor a wall, though the pack runner, keying on the status, reports the 7 as
 3571|   refused and stops on the 8), the usage requirement of ABSOLUTE paths with what a missing brief, or a relative one that
 3572|   does not resolve from the project root, really does (codex gets an EMPTY prompt -- Fable 5.1, measured; the brief's size
 3573|   is checked against the argv cap, before the `cd` -- GPT-6 Astra), and the controls.  Its executable lines are v3's but
 3574|   ONE: v6 rewords the UNVERIFIED message to "no model line in an opening codex header block", which fixture NM showed is
 3575|   the truth; v7 corrects comments only.
 3576| * Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v7.sh`: every row drives three launchers -- the TRACKED
 3577|   file the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a
 3578|   fixture.  289/289 (`RECEIPT_v7.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8
 3579|   (a NUL in stderr), IR 1 -> 5 (a different model), CH 0 -> 5 (a coloured header), CSI and CZ 6 -> 7 (a non-SGR escape, a
 3580|   parameterless one).  Its header is the CONTRACT, derived from the FILE (v5) and, in v6 and v7, rowing each listed decision's
 3581|   VALUES and used states: every override set to a non-default value at its own call (OV), a re-run into a used out dir (RS), a missing
 3582|   parent (MP), the fallback's own rc (FR), a non-empty refused stdout (RN), both ends of both rule patterns (SP1, SP2, R9A,
 3583|   R9B), a near-miss banner (BN), `model:` with no space (WZ), codex's own rc 7 and 8 (R7X, R8X), `SEAT WALLED` iff the CLASSIFIED wall exit
 3584|   (PK, which `status.sh` reads -- decided by the ROW, not by the launcher's own text, from v7), the `codex rc=` line's
 3585|   numbers, not only its format, at default and non-default efforts (LOG), each raw-status message's own number (RXM), a
 3586|   two-line brief (MB), occupied refused destinations (RN2), a lower-case tag (TG), and every member of the ANSI strip's
 3587|   class in one line (CSX).  Rows SAMPLE briefs, tags and out-dir states; the strip's class (CSX with CZ's empty parameter) and the
 3588|   patterns' alternatives are EXHAUSTED.  Its BOUNDARY for synthetic rows (Fable
 3589|   5.1): an edge is pinned when its constant selects an exit status, a call argument or a caller-read phrase on an input
 3590|   codex can produce; disclosed when it needs the harness environment, an unclaimed encoding, an unreachable flag value or a
 3591|   display line.  CSI is synthetic in BOTH halves -- 42 of the 44 codex `.err` files carrying a `;`-joined SGR are the #544
 3592|   control stub's own output, the other 2 a coloured GXemul prompt quoted mid-line (`v5pass/SEMISGR_WHERE.txt`; the v5 text
 3593|   called that half load-bearing).  Kill table `run_mutants_v7.sh`: 144/144 as recorded (`KILLTABLE_v7.txt`) -- the 133
 3594|   v6 mutants and 11 new, each killed by the controls its line names; the driver re-runs once any mutant run carrying the
 3595|   load flake's signature (an empty `stdout= b`, Fable 5.1).
 3596| * Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
 3597|   `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
 3598|   freely", "has no Daybreak fallback" and "panel.sh's comment is still owed" statements bracketed by content; RULINGS_C's
 3599|   drifted line citations re-cited by id.  One row filed, `cxlaunchcov` (the coverage debt the v7 pass measured); the relative-path defect the v5 pass ruled
 3600|   disclose-and-FILE is
 3601|   filed ON `cxlaunchempty`, whose defect it is (an empty prompt reaching codex) by a second road; that row's NUL half is
 3602|   recorded closed by this landing (X8), and its fix stays `#544`'s, the peer session's round, which rebases on the landed
 3603|   file.
 3604| 
 3605| **Pass 2** (`pass2/`, on v1): Astra SWC 2, GLM SWC 2, Grok SWC 1 (the NUL-bearing wall, measured), Fable SWC 2 (its first run
 3606| fell back to claude-opus-4-8 after two refusals -- disclosed, credited as Opus 4.8; resumed, Fable 5.1 wrote v2).
 3607| **Adjudication pass** (`f2/`, on v2): Astra SWC 3 (the header awk matched the banner ANYWHERE; E1/E2 matched a substring),
 3608| Grok SWC 3 and GLM SWC 3 (records; the receipt citation; `m_eq1`'s reason); Fable SEAT FAILURE (a stall).  **V3 pass**
 3609| (`v3pass/`): Astra SWC 3, Grok SWC 3, GLM SWC 2 -- one-edit mutants passing all 70 v3 controls at the window and cap
 3610| constants, the multiplicity guards and the fallback predicate, so v4 closed that class; Fable SEAT FAILURE (a second
 3611| stall).  **V4 pass** (`v4pass/`): Fable SWC 7, Astra SWC 3, Grok SWC 5, GLM SWC 5 -- the v4 CONTRACT was derived from the
 3612| passes' FINDINGS, not the file, and decisions no pass had named had one-edit mutants passing all 116 v4 controls (codex's
 3613| own rc, the fallback's second and third conjuncts, the header strip, the stdin redirect, the output names, the pattern
 3614| alternatives, the body tests, the default codex path), so v5 derived the CONTRACT from the file.  **V5 pass** (`v5pass/`):
 3615| Fable SWC 5, Astra SWC 5, GLM SWC 3, Grok SWC 2 -- Fable, Astra and Grok zero floor breaches, GLM two (the
 3616| truncation and effort edges, both rowed in v6 whatever their grade; the v6 records said "all four zero", corrected on the
 3617| v6 pass by GPT-6 Astra), and one shape: a row pinned a value's
 3618| DEFAULT, not the value, and a FRESH state, not a used one.  The main loop measured every claimed escape before acting
 3619| (`v5pass/main_meas.txt`: 18 of 18 pass all 94 after-column checks of the v5 controls), Fable 5.1 measured 19 more forms and
 3620| built the five rows that kill them (v6's OV, RS, MP, CZ, LOG); five records sentences were false (no caller reads the wall
 3621| wording; LOST iff exit 7; the NM message; the 44-file provenance; a relative brief makes the launcher exit 1); U7 PINNED, all
 3622| four agreeing, with Fable's boundary.  **V6 pass** (`v6pass/`): Astra SWC 6, GLM SWC 3, Grok CLOSE -- all three zero floor
 3623| breaches; Fable SEAT FAILURE (walled on a usage limit after writing a stub, re-fired once and walled again).  One shape: a
 3624| v6 check read the LAUNCHER'S OWN TEXT to decide what it expected (PK keyed codex's own rc 7 on `codex exited 7`, so a
 3625| refusal echo rewritten to it passed -- Astra), and four values no row varied (a two-line brief, a lower-case tag, an
 3626| occupied refused destination, the strip class's other members): Astra's nine one-edit escapes, each a v7 row or check.
 3627| GLM's three kill-table record defects were refuted by reading the table, and its NUL reading by measurement (bash drops the
 3628| NUL before the grep -- `v6pass/main_meas/NUL_HDR.txt`); Grok's Y25 correction (D4 cannot pin the fallback's
 3629| re-classification -- its second run refuses too) is a mutant, `m_noreclassify`, killed by D1 and D2.  Astra's eight records
 3630| sentences corrected, Grok's UNVERIFIED tail named in the CONTRACT, and one more the main loop found (v6 listed caller
 3631| inputs -- RS, MP, OV -- under "CENSUS_v5.txt names each count").  **V7 pass** (`v7pass/`): Astra SWC 5, Grok CLOSE, GLM CLOSE (its first firing
 3632| an HTTP 502 from the Ollama cloud, re-fired once) -- zero floor breaches on each denominator; Fable SEAT FAILURE (walled on
 3633| a usage limit, its fourth wall that day; its stage HELD by owner ruling 2026-10-17).  D1 settled for the pin by both
 3634| parties: no census reads the logged effort, so LOG's whole-line comparison is a fidelity guarantee (Grok withdrew "no
 3635| reader greps asked:" -- the pass-2 census counted the asked/ran model pairs).  D2: GLM withdrew all four readings.  One
 3636| escape measured past the 289 -- `wc -w` for the empty test's `wc -c`, 123/123 after-column (Astra found it, the main loop
 3637| measured it, `v7pass/main_meas/`) -- FILED as `cxlaunchcov` with GLM's PK row-name residual; the records corrected in
 3638| place (the relative-brief bullet, Z20's "never 7", the census's per-row provenance, the display list's three missing
 3639| lines, the rc-7/8 comment's "with an answer", the CSX/CZ attribution).  Opus, agy, kimi,
 3640| deepseek and minimax not fired, by the owner's roster of 2026-10-16.
 3641| Section R: `tools/pipeline/check_probe_wiring.py`'s MANIFEST classifies the landing's 15 preserved `.py` artifacts --
 3642| the six mutant writers and the Fable seat's two control-variant builders TOOL; the two censuses, the Fable seat's
 3643| three measurement scripts and the v6 pass's two escape and NUL counts RESEARCH.  The controls and the kill-table
 3644| drivers are shell scripts, outside that MANIFEST's `.py` domain; none of these is a gated detector.
 3645| 
```

## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_CXLAUNCHQUOTATION: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECCXLAUNCHQUOTATION: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
