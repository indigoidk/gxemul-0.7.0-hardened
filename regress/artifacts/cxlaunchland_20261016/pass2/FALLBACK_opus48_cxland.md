FABLE_CXLAND_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES (2) -- the landed launcher is correct and reproduces 30/30; the two changes are to the WITNESS and the RECORDS around it, not to the code.

I read the landed `tools/cxlaunch.sh` (md5 47d47097), the `before` fixture (3c51a757), the OLD tracked HEAD
(`git show HEAD:tools/cxlaunch.sh`, md5 cb180d9d), the controls driver, both censuses, the F1 ruling, the ledger
rows, and the OB/ledger records targets. I re-ran `run_controls.sh` (reproduced the RECEIPT exactly bar the date
line), traced every exit path by hand, built ten mutant launchers OUTSIDE the project and scored each against the
30 controls, and measured the real `codex_*.err` / `*.launch.log` populations with `-I` python. I did NOT run the
real codex CLI.

---

## The two changes

**C1 (records / witness) -- the RECEIPT's baseline is the ALREADY-FIXED farm copy, so the controls that would
witness `cxlaunchquotation`'s own defect are green-on-both and witness PRESERVATION, not the kill.**

The tree actually replaces tracked HEAD `cb180d9d`. I read its classifier directly: `refus`/`wall` are computed
UNCONDITIONALLY at top level (HEAD lines 42-48), and `wall` is built from `ERROR: + stdout` -- there is no
`if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]` gate. That is the defective classifier `cxlaunchquotation` and the
wall-FP were filed against. The real pre-fix symptom is on disk, not a fixture:
`regress/artifacts/fablequeue8n_20261009/astra_confirm/cxlaunch_asicconverge_stdout.txt` shows the old classifier
report a real `rc 0, 10,466-byte` answer as `*** SEAT WALLED. / LAUNCH_RC=8` (`wall(ERROR: + stdout): 1`).

The `before` fixture (3c51a757, the farm copy) ALREADY carries both the classify gate (its line 66) and the
`^ERROR:` anchor (its line 62). So against `before`, N2 (an rc-0 answer whose stdout is literally
`"... a usage limit, a quota, a rate limit ... not authenticated"` -- plainly crafted to trip the quotation bug)
and N1 (an rc-0 answer with column-0 `ERROR:` lines in stderr) are BOTH exit 0 on before and after
(RECEIPT: N1/N2 before=0 after=0). They witness that the landed file does not regress the farm copy -- they do
NOT witness `cxlaunchquotation` being killed, because the defect is not in the chosen baseline.

Closing `cxlaunchquotation` with `witness: harness:.../RECEIPT.txt` therefore closes it against a baseline that
already contains its fix. The witness ladder's clause (i) wants the symptom shown on the PRE-FIX committed state
and gone post-fix; the pre-fix state here is `cb180d9d`, not the farm copy. The fix: either (a) add a third
launcher column `before2 = git show HEAD:tools/cxlaunch.sh` (cb180d9d) to the RECEIPT and show N1/N2 red (exit 8)
-> green (exit 0) there, or (b) keep the farm-copy baseline but state in the closure that the pre-fix symptom is
the `cxlaunch_asicconverge_stdout.txt` artifact (LAUNCH_RC=8) and that the RECEIPT witnesses the TRACKING of an
already-fixed copy (the diff/md5), not a red-on-baseline control. Count I checked: 0 of the 30 controls red on
the baseline for the quotation / wall-word-in-stdout defect; 1 of 1 real pre-fix symptom exists (the asicconverge
artifact).

**C2 (records) -- correct by CONTENT, and the ruling named only two of (at least) four stale/false targets.**

The ruling's cited correction targets are stale line numbers: OB:24714-24716 is actually `stagetokenscontrols`,
and ledger:62489 is a `"date"` line in the `armvecrecurse`/kimi region. The live cxlaunch records are
OB:24668 (`cxlaunchdaybreak` heading), OB:24722 (`cxlaunchquotation`), OB:16562 (a rule statement), and the
ledger rows at 62601 (`cxlaunchdaybreak`) / 62674 (`cxlaunchquotation`) / 53074 (`cxlaunchempty`). Two of these
are now FALSE under the landing and must be corrected, not merely re-pointed:
* OB:24668 -- "`tools/cxlaunch.sh` has no Daybreak fallback" -- the landed file HAS the fallback (D1 proves it
  fires and credits Daybreak; the real receipt is `codexpack_20260928/dossier_gdromdma/...launch.log`).
* OB:16562 -- "anchors stderr tests on codex's own `^ERROR:` lines and greps stdout freely" -- the landed rule
  classifies stdout ONLY on failure (`rc != 0` or empty); "greps stdout freely" is no longer true.
Locate every edit by `grep`-ing the id/text, never by the ruling's numbers (the carrier's own
line-numbers-drift lesson).

## Filed, NOT blocking -- control coverage debt (above the vacuity floor for THIS landing)

Ten mutant launchers, scored against all 30 controls in a scratch dir outside the project. Five single edits pass
**30/30 while degrading a real property** (`v_*` scripts kept in my scratch):
* drop the `^` from `grep '^ERROR:'` -> reinstates the 2026-09-07 "codex streams source, bare grep matches any
  file containing the words" defect. 30/30.
* `[ "$body" -eq 0 ]` -> `[ "$verd" -eq 0 ]` in the classify gate -> breaks the EXACT F1 condition
  ("classified only when rc != 0 OR stdout is EMPTY"). 30/30.
* `-ne 0` -> `-eq 1` in the gate; `[0-9;]*[A-Za-z]` -> `[0-9;]*m` in the strip; suffix-only identity compare
  (`${RAN##*-}`). Each 30/30.
These break PRE-EXISTING launcher properties (the `^ERROR:` anchor and the `rc!=0||body==0` gate both live in
the `before` baseline, verified -- they are not landing deltas), so by the floor rules they are above-floor
coverage debt of the broader launcher, not a clause-(d) breach of this landing. The landing's OWN deltas ARE
floor-pinned: Q3/A1 red-on-before for the ANSI strip, M1/D2 for the identity check. FILE a row to add two pins
(a fixture whose stderr has a mid-line "ERROR:" from streamed source on a failed run, to pin the `^`; and an
rc-0/non-empty/no-VERDICT/wall-word-in-stderr fixture, to pin `body` not `verd`). For a LOW harness landing,
filing is the right disposition.

---

## Answers by number

**1. The rule.** Yes -- implemented exactly. `refus`/`wall` are initialised 0 and set ONLY inside
`if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]`; the `else` arm just prints the "IGNORED" note. Exits 7/8 are gated on
`refus`/`wall`, so on an rc-0 non-empty answer they are structurally 0 and the run can never exit 7 or 8
(N1 proves it: 6 ERROR-shaped stderr lines IGNORED -> "seat answered"). No real wall/refusal ends as exit 0: an
rc-1/empty run whose `ERROR:` text matches no refusal/wall pattern (e.g. `Reconnecting...`, `cannot find the
path`, `access token could not be refreshed` -- all of which are on record, 150/87/2 occurrences) falls through
to `body -eq 0` -> exit 6, a failure code, not 0. The fallback block is straight-line (not a loop), so a
double-refusal (Astra then Daybreak) runs it once and then hits exit 7 -- no laundering, no loop. Launch-log
census confirms the premise: 519 `*.launch.log`, 0 lines off the {rc 0 with stdout, rc != 0 with empty stdout}
diagonal.

**2. The ANSI strip.** `sed "s/${ESC}\[[0-9;]*[A-Za-z]//g"` is right for the measured shape: I ran it on a REAL
coloured refusal (`_scratchpad/panel_20260919_013302/codex_adv540p2.REFUSED1.err`, `ESC[1mESC[31mERROR:ESC[0mESC[0m`)
-> `grep '^ERROR:'` returns 2, the unstripped anchor returns 0. The `[A-Za-z]` final-byte class covers ALL CSI
sequences (SGR and non-SGR). Forms it misses: OSC (`ESC]...BEL/ST`) and a lone `ESC` not followed by `[` are not
stripped; a bare `CR` is not relevant to a `^` anchor on `\n`-split lines. Census of 2372 `codex_*.err`: OSC = 0,
non-SGR CSI = 0, and the only two ESC-survivors are literal `\x1b`-in-prose inside a quoted-source audit
(`lcabadval`), which carry no `^ERROR:`. So those misses are hypothetical (0 on record). Yes, the strip CAN create
a column-0 `ERROR:` that was not one before -- that is its intended job for codex's own coloured diagnostics -- and
it can likewise promote a QUOTED coloured line (an old panel file codex streams back contains ESC codes). But the
classify-only-on-failure condition bounds it completely: on an rc-0 answer `CXERR` is never consulted, so a
promoted quoted line can only affect an already-failed/empty run (no answer to lose) -- i.e. the N4 residual
(rc != 0 WITH an answer), which is explicitly recorded and is 0 of 387 on record. Not a regression against the
production copy within that bound.

**3. The identity check.** `head -n 40` is safe with a large margin: of 773 `codex_*.err` with a header, 772 have
`^model:` at line 5 and exactly one at line 7 (two pre-header `401 Unauthorized` lines) -- a 33-line margin. It is
not PROVABLY bounded (a pathological reconnect/401 prologue could in principle exceed 40), but the failure mode is
benign: RAN empties -> UNVERIFIED note, never a wrong exit. A quoted `model:` line cannot be read as the header:
the header is emitted at session start, BEFORE codex reads the brief or streams any source, so the first
`^model:` in the window is always the real one (confirmed: first `^model:` is the header in 773/773). Section 3's
UNVERIFIED-not-failed is RIGHT: of the population the check actually runs against -- cxlaunch-captured answered
runs -- 0 of 330 lack the header (and 0 of the 322 asked/ran launch-log pairs); failing it would convert a future
CLI format change into a lost answer on every run. (The 1200 header-less answered `codex_*.err` elsewhere are
non-cxlaunch captures -- synthetic `w544` fixtures, panel.sh refires -- not this launcher's stderr.)

**4. The controls.** Q3 (6->8) and A1 (6->7) are non-vacuous: both red on before (unstripped anchor misses the
coloured `ERROR:`) and green on after. M1 (0->5) and D2 (0->5) are non-vacuous: the fake codex replays the
`model: gpt-6-astra` header regardless of `-m`, so asked!=ran is a real mismatch; before has no identity check.
None of the four delta-controls is green-on-both. The vacuity that EXISTS is at the baseline level (C1): N1/N2 are
green-on-both because `before` already fixed the quotation/wall-FP defect -- they witness preservation, and the
real repro lives in the asicconverge artifact against `cb180d9d`. **Smallest edits that pass all 30 and break a
ruled property** (measured, not sketched): `[ "$body" -eq 0 ]` -> `[ "$verd" -eq 0 ]` (breaks the exact F1
condition) and dropping the `^` from `grep '^ERROR:'` (reinstates the 2026-09-07 defect); both score 30/30
because no control pins a failed run carrying a non-wall `ERROR:` or an answer with no VERDICT token. These break
PRE-EXISTING properties, so they are the filed coverage debt above, not a landing floor breach.

**5. Records.** `cxlaunchdaybreak` closes cleanly: the landed fallback is real (D1) and has a real-run witness
(the 09-28 dossier log: refused on Astra, Daybreak answered rc 0 24,066 b, refused files kept). `cxlaunchquotation`
should close only after C1 -- its witness as written does not contain a row that reds on its own defect.
`cxlaunchwallfp` (OB:22502, no ledger row) merges correctly; the withdrawn "read only the final `ERROR:` line"
refinement is right to withdraw (N4's final `ERROR:` line is itself a quotation -- I confirmed the dossier
refused.err ends on quoted `ERROR:` lines). C2 applies to the OB/ledger edits.

**6. Which of my dispositions is wrong? -- count named.** None of section 3's THREE dispositions is wrong on the
counts I re-derived: header UNVERIFIED (0 of 330 cxlaunch-captured answered runs, 0 of 322 pairs), N4/twin
residual (0 of 387 off-diagonal; 0 of 519 launch logs), PROJ hardcoded (pre-existing in before, out of ruling
scope). The disposition that does not hold is in section 1 -- that this RECEIPT witnesses `cxlaunchquotation`:
0 of 30 controls red on the baseline for that defect, while 1 real pre-fix symptom (asicconverge, LAUNCH_RC=8)
sits uncited. That is C1.

## What I could not check
* The real codex CLI (not run, per the brief); all codex behaviour is from captured `.err`/`.launch.log` on disk.
* An absolute upper bound on the pre-header prologue (empirically <= 7 lines; head -40 is a margin, not a proof).
* Whether codex ever emits OSC/non-SGR-CSI colour in some unseen config (0 on record; bounded by classify-only-on-
  failure regardless).
* A corroborating run of HEAD(cb180d9d) through the validated driver did not finish in the window; I relied
  instead on reading HEAD's source (ungated classify, `wall(ERROR: + stdout)`) and the real asicconverge artifact,
  which is a stronger witness than a fixture.
