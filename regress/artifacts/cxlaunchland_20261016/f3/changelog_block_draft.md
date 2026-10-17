# `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- an rc-0 run with a non-empty stdout is never scored WALLED or REFUSED for what its stderr quotes, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5 (after the refusal, wall and empty-stdout checks); the controls row each listed decision's VALUES and used states, not only its defaults (v7: 289 checks, 144 mutants)

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
  the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch; "model UNVERIFIED", exit
  0, when a run that ANSWERED -- rc 0, a non-empty stdout, no earlier exit -- has no model line in an opening block); the
  effort `ultra`.  Its header records the residuals (N4 and its refusal
  twin), exit 5's novelty to the pack runner and the log phrases its callers read (`run_pack_body.sh` and `status.sh`),
  codex's own rc 7 and 8 (neither a refusal nor a wall, though the pack runner, keying on the status, reports the 7 as
  refused and stops on the 8), the usage requirement of ABSOLUTE paths with what a missing brief, or a relative one that
  does not resolve from the project root, really does (codex gets an EMPTY prompt -- Fable 5.1, measured; the brief's size
  is checked against the argv cap, before the `cd` -- GPT-6 Astra), and the controls.  Its executable lines are v3's but
  ONE: v6 rewords the UNVERIFIED message to "no model line in an opening codex header block", which fixture NM showed is
  the truth; v7 corrects comments only.
* Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v7.sh`: every row drives three launchers -- the TRACKED
  file the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a
  fixture.  289/289 (`RECEIPT_v7.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8
  (a NUL in stderr), IR 1 -> 5 (a different model), CH 0 -> 5 (a coloured header), CSI and CZ 6 -> 7 (a non-SGR escape, a
  parameterless one).  Its header is the CONTRACT, derived from the FILE (v5) and, in v6 and v7, rowing each listed decision's
  VALUES and used states: every override set to a non-default value at its own call (OV), a re-run into a used out dir (RS), a missing
  parent (MP), the fallback's own rc (FR), a non-empty refused stdout (RN), both ends of both rule patterns (SP1, SP2, R9A,
  R9B), a near-miss banner (BN), `model:` with no space (WZ), codex's own rc 7 and 8 (R7X, R8X), `SEAT WALLED` iff the CLASSIFIED wall exit
  (PK, which `status.sh` reads -- decided by the ROW, not by the launcher's own text, from v7), the `codex rc=` line's
  numbers, not only its format, at default and non-default efforts (LOG), each raw-status message's own number (RXM), a
  two-line brief (MB), occupied refused destinations (RN2), a lower-case tag (TG), and every member of the ANSI strip's
  class in one line (CSX).  Rows SAMPLE briefs, tags and out-dir states; the strip's class (CSX with CZ's empty parameter) and the
  patterns' alternatives are EXHAUSTED.  Its BOUNDARY for synthetic rows (Fable
  5.1): an edge is pinned when its constant selects an exit status, a call argument or a caller-read phrase on an input
  codex can produce; disclosed when it needs the harness environment, an unclaimed encoding, an unreachable flag value or a
  display line.  CSI is synthetic in BOTH halves -- 42 of the 44 codex `.err` files carrying a `;`-joined SGR are the #544
  control stub's own output, the other 2 a coloured GXemul prompt quoted mid-line (`v5pass/SEMISGR_WHERE.txt`; the v5 text
  called that half load-bearing).  Kill table `run_mutants_v7.sh`: 144/144 as recorded (`KILLTABLE_v7.txt`) -- the 133
  v6 mutants and 11 new, each killed by the controls its line names; the driver re-runs once any mutant run carrying the
  load flake's signature (an empty `stdout= b`, Fable 5.1).
* Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
  `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
  freely", "has no Daybreak fallback" and "panel.sh's comment is still owed" statements bracketed by content; RULINGS_C's
  drifted line citations re-cited by id.  One row filed, `cxlaunchcov` (the coverage debt the v7 pass measured); the relative-path defect the v5 pass ruled
  disclose-and-FILE is
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
Fable SWC 5, Astra SWC 5, GLM SWC 3, Grok SWC 2 -- Fable, Astra and Grok zero floor breaches, GLM two (the
truncation and effort edges, both rowed in v6 whatever their grade; the v6 records said "all four zero", corrected on the
v6 pass by GPT-6 Astra), and one shape: a row pinned a value's
DEFAULT, not the value, and a FRESH state, not a used one.  The main loop measured every claimed escape before acting
(`v5pass/main_meas.txt`: 18 of 18 pass all 94 after-column checks of the v5 controls), Fable 5.1 measured 19 more forms and
built the five rows that kill them (v6's OV, RS, MP, CZ, LOG); five records sentences were false (no caller reads the wall
wording; LOST iff exit 7; the NM message; the 44-file provenance; a relative brief makes the launcher exit 1); U7 PINNED, all
four agreeing, with Fable's boundary.  **V6 pass** (`v6pass/`): Astra SWC 6, GLM SWC 3, Grok CLOSE -- all three zero floor
breaches; Fable SEAT FAILURE (walled on a usage limit after writing a stub, re-fired once and walled again).  One shape: a
v6 check read the LAUNCHER'S OWN TEXT to decide what it expected (PK keyed codex's own rc 7 on `codex exited 7`, so a
refusal echo rewritten to it passed -- Astra), and four values no row varied (a two-line brief, a lower-case tag, an
occupied refused destination, the strip class's other members): Astra's nine one-edit escapes, each a v7 row or check.
GLM's three kill-table record defects were refuted by reading the table, and its NUL reading by measurement (bash drops the
NUL before the grep -- `v6pass/main_meas/NUL_HDR.txt`); Grok's Y25 correction (D4 cannot pin the fallback's
re-classification -- its second run refuses too) is a mutant, `m_noreclassify`, killed by D1 and D2.  Astra's eight records
sentences corrected, Grok's UNVERIFIED tail named in the CONTRACT, and one more the main loop found (v6 listed caller
inputs -- RS, MP, OV -- under "CENSUS_v5.txt names each count").  **V7 pass** (`v7pass/`): Astra SWC 5, Grok CLOSE, GLM CLOSE (its first firing
an HTTP 502 from the Ollama cloud, re-fired once) -- zero floor breaches on each denominator; Fable SEAT FAILURE (walled on
a usage limit, its fourth wall that day; its stage HELD by owner ruling 2026-10-17).  D1 settled for the pin by both
parties: no census reads the logged effort, so LOG's whole-line comparison is a fidelity guarantee (Grok withdrew "no
reader greps asked:" -- the pass-2 census counted the asked/ran model pairs).  D2: GLM withdrew all four readings.  One
escape measured past the 289 -- `wc -w` for the empty test's `wc -c`, 123/123 after-column (Astra found it, the main loop
measured it, `v7pass/main_meas/`) -- FILED as `cxlaunchcov` with GLM's PK row-name residual; the records corrected in
place (the relative-brief bullet, Z20's "never 7", the census's per-row provenance, the display list's three missing
lines, the rc-7/8 comment's "with an answer", the CSX/CZ attribution).  Opus, agy, kimi,
deepseek and minimax not fired, by the owner's roster of 2026-10-16.
