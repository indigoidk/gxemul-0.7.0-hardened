FABLE_SEAT_ALIVE_20261009_RGH
`# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)`

# Regress review -- stagetokens / heldmasked / fbsmlane, and the n6 rule question
Fable 5.1 (claude-fable-5-1), flagship REGRESS seat, 2026-10-09.  Read-only on every project tree; every run
below was made in this seat's own scratch (`...\scratchpad\fable_rgh\`, the WSL clone `/tmp/gxrgh`).
Tree under review: `GXEMUL-SEC` at HEAD `a05660af` (the checkpoint's HEAD line says `3a8c3b1a`; one records
commit landed after it).  Measured against COMMITTED shas via `git archive`, never the dirty working tree.

## VERDICT LINES

stagetokens: REGRESS WITH FINDINGS (5) -- the controls still discriminate at HEAD (base 49/49, all 33 mutants killed, output byte-identical to the committed v3); no reader has changed since 09ded75; two stale/imprecise records, 13 expectations no shipped mutant reds (12 measured failable with extra mutants, 1 mislabelled), one dashboard conflation, one narrower-than-documented section-I guarantee.
heldmasked: REGRESS WITH FINDINGS (1) -- the fix is at HEAD and discriminates (the pre-fix reinstatement M_count_beats_hold reds 7 expectations; the real ledger now prints `HOLD pcc2c040assertrow review 9/9 awaiting: glm, deepseek, minimax, kimi`); its `t_discharged` row has no killing mutant in the shipped table (measured failable, 43/49, by an extra mutant).
fbsmlane: REGRESS WITH FINDINGS (1) -- the lane re-runs at HEAD exactly as the #537 F2 table recorded (P0 OK via R3, P3 FAIL, P1 FAIL-not-via-named-row, P2 OK under the old R4 pin, P4 OK); the R3 pin is the right pin and the closure is complete; one wording L4 in the row's `hold` field.
n6: RULED (a) -- the 2026-08-30 fable5 entry is a seat answer that re-opened the stage: it discharged a held question (the project's own discharge rule makes the discharging entry an answer by construction), produced new design findings rather than disposing of a panel's, and carries answer-only fields; the owner's 2026-09-18 decision and the shipped guard (t_selflate) already say the same, and the stage is 9/9 at HEAD.

---

## 0. Premise audit, before anything else

* **"later commits touched stage_tokens.py's readers and check_stage_panels.py" -- MEASURED FALSE for the
  committed history.**  `git log 09ded75..HEAD -- tools/pipeline/{stage_tokens,check_stage_panels,
  check_fable_queue,gen_codex_wall,gen_dashboard}.py` is EMPTY; all five are byte-identical between HEAD and
  the working tree (md5).  The only #534-touched files with later commits are `tools/pipeline/check_probe_wiring.py`
  (a manifest, not a token reader; dirty in the working tree) and `tools/precommit_check.sh`, whose diff since
  09ded75 contains no line near sections H / H2 / I (the only keyword hit is the #560 "UNSTAGED src/" warn text).
  So nothing weakened what was reviewed; H2 (`stage_tokens.py --selfcheck`) is still wired at precommit lines
  859-868 and passes at HEAD: `STAGE_TOKENS_PASS 24 file(s) scanned, 0 literal(s) outside stage_tokens.py`.
* The readers importing `stage_tokens` at HEAD are exactly the four #534 named plus the untracked
  `check_fix_seats.py` (still untracked, still on the checkpoint's NEVER COMMIT list), so the controls' contract
  line "check_fix_seats.py ... is NOT covered ... its control is owed when it ships" still holds.
* The three commits landed what their records say: 09ded75's stat is harness-only (no `src/`), with
  `stage_tokens.py` +243, the four readers, H2 in precommit, the manifest, the controls and panel artifacts;
  cdbe7d7's tracked non-artifact files are exactly the CHANGELOG's "four files, no emulator code"
  (`diff_fbpending_bound.c`, `gate_offline.sh`, `selfmutant.py`, `fbpending_bound.why`) plus records.

## 1. `stagetokens` (closed; 686d179 09ded75)

**READ.**  Ledger row (26 entries), the queue's 8n entry, CHANGELOG `#534` and `#537` blocks, OUTSTANDING_BUGS
21828-21887 and the `dashmalformedheld` block, `stage_tokens.py`, `check_stage_panels.py`, `check_fable_queue.py`,
`gen_codex_wall.py`, `gen_dashboard.py:120-180`, `run_controls.py` and `controls_20260918_v3.out`, precommit's
H / H2 / I / I2 blocks, and the 09ded75 hunks in `check_probe_wiring.py` and `precommit_check.sh`.

**RAN** (scratch `fable_rgh\`):
* `git archive HEAD tools/pipeline regress/artifacts/stagetokens/controls_534` -> `headtools/`; then
  `python run_controls.py` from that copy (its `PIPE` resolves to HEAD's tools, its `REAL` to HEAD's ledger):
  **`controls_HEAD.out`: base 49/49 green, all 33 mutants killed, `STAGE_TOKEN_CONTROLS_PASS`, and
  `diff` against the committed `controls_20260918_v3.out` is IDENTICAL** (stderr 0 bytes).
* HEAD's real checkers on HEAD's ledger and queue (`GXLEDGER`/`GXQUEUE` pointed at the archive):
  `csp_HEAD.out` -- `STAGE_PANELS_PASS`, 273 complete / 21 grandfathered / 255 filed / 11 HELD / 0 incomplete,
  `ok stagetokens review 9/9`, `ok n6 assess 9/9`, `ok fbsmlane review 9/9`; `fq_HEAD.out` -- `FABLE_QUEUE_PASS`,
  `ok stagetokens regress owed and queued`, `ok heldmasked regress owed and queued`;
  `stage_tokens.py --census`: HELD 51/44, ANNOTATION 13/13, RE_READ 1/1, NOPANEL 28/22, NOTSEAT 408/374.
* `rgh_extra_mutants.py` -> `extra_mutants.out`: the 49 expectations matched by substring against the 33 shipped
  mutants' red lists, then seven extra mutants run through `run_controls.run()` from the HEAD copy.
* `fx_regresshold/`: a three-row fixture ledger against HEAD's `check_fable_queue.py`, `check_stage_panels.py`
  and `gen_codex_wall.py`.

**FINDINGS.**

1. **Stale field (L4, minor).**  `ledger.json` row `stagetokens`, `hold_question`: *"PASS 2 IS OWED ON THIS DIFF
   and these are its questions. (1) Is `[NOT A PANEL STAGE: NO PANEL CONVENED]` the right SHAPE ..."*.  The row is
   closed; pass 2, the F2 pass and the last seat all ran on 2026-09-18 and answered Q1-Q3 (R2 entry-scoped token;
   the sorting rule; the distinct `∅` glyph).  "IS OWED" is false at HEAD.  No tool reads `hold_question` on a
   closed row, so the cost is a reader's.
2. **A version label reused after the file changed (records, minor).**  Entry [18] (codex, F2 pass) ends
   *"ALL REPAIRED (v3: 48/48, 32 mutants killed)"*; the committed `controls_20260918_v3.out` reads 49/49 and 33
   mutants, because the last seat's `t_selflate` was appended to "v3" without a bump.  Entry [25] (fable5) records
   the delta, so the facts are recoverable, but a reader following "v3" to the artifact meets different numbers.
   `run_controls.py`'s docstring ("every one is killed in controls_20260918_v3.out ... measured passing 48/48 by
   the fable5 last seat") is consistent with the file.
3. **13 of 49 expectations are reddened by NO shipped mutant -- coverage debt, FILE (not a floor breach: the
   contract is mutant-centred and all 33 die).**  Measured list (`never_reddened.txt`): `CSP t_held HOLD`,
   `CSP t_annot grandfathered`, `CSP t_reread one-seat filing`, `CSP t_nopanel exempt`, `CSP t_notseat incomplete`,
   `FQ t_notseat short`, `FQ t_nopanel exempt`, `FQ t_held queued`, `DASH annotation renders tok`,
   `DASH nopanel renders tok`, `DASH notseat renders tok`, `CSP t_heldnop HOLD`, `CSP t_discharged complete`.
   Six one-line extra mutants (`extra_mutants.out`) show twelve of them failable:
   `X_is_held_exact` (`HELD in _note(e)` -> `HELD == _note(e)`) 32/49; `X_never_discharge` (`done = False and ...`)
   43/49; `X_notseat_is_answer` 45/49; `X_annotation_is_answer` 45/49; `X_nopanel_not_exempt` 41/49;
   `X_dash_tok_blank` (`class="c tok"` -> `"c none"`) 44/49.  **The thirteenth is mislabelled**: the expectation
   `CSP t_reread one-seat filing` is `not has(csp, r"^\s+t_reread\s")`, and every listing line except a VIOLATION
   prefixes the id with `ok`/`--`/`..`, so the regex can only ever assert "t_reread is not a violation" -- it
   cannot see filing-vs-grandfathered.  Measured: the filing-shortcut mutant `X_filing_is_zero`
   (`check_stage_panels.py` `if len(got) == 1:` -> `== 0`) ESCAPES 49/49 (t_reread then grandfathers through its
   RE_READ exemption and prints `--`, which the regex does not match).  A rename, or pinning the
   `..    t_reread  review  1/9  filed` line, closes it.  Shape to adopt: the seven mutants above, one commit.
4. **Dashboard: an answer whose `d` is `"OK"` renders in the seat-failure class (LOW, display only).**
   `gen_dashboard.py:74` `D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}` and `:161`
   `cls = D_CLASS.get(d, "pend")`.  HEAD's ledger carries **439 entries with `d: "OK"`** (a 2026-08-27..31
   convention -- `wdcnoirq`, `gdromcondlies`, `gdromexitsix`, `shortread`, `sgireunmapped`, ... and `n6`'s
   2026-08-30 fable5 assess entry); in HEAD's `matrix.html` **365 cells render the glyph `OK` and all 365 carry
   class `pend`**, zero class `ok`.  `#534`'s F3 counted "1,415 `ok` cells before and after" -- the `✓`
   population; the `OK` population was outside that count.  H and I never read `d`, so no gate is affected; the
   published matrix is.  One line in `D_CLASS` (`"OK": "ok"`) or a ledger sweep `OK` -> `✓`; either owes the
   controls a `DASH` row with `d="OK"`.
5. **Section I's regress guarantee is narrower than its docstring, and the hold reaches the queue by another
   road (LOW, measured).**  Fixture `fx_regheld`: a CLOSED row with commits whose only regress entry is a LIVE
   `[HELD AWAITING SEAT: fable5]`, NOT named in the queue -> `check_fable_queue.py` reports `0 closed rows owing a
   regress review` (its rule 3 reads the marker as "a regress entry"; rules 1-2 `continue` before the regress
   phase), `check_stage_panels.py` ignores regress by design -- but `gen_codex_wall.py` lists it
   (`fx_regheld (regress:fable5)`), and precommit **I2 hard-fails a stale wall**.  So a closed row's held regress
   review IS forced into `fable_queue.md`, by I2 rather than by I, and `check_fable_queue`'s "held-and-queued"
   count (2 at HEAD) excludes the 20 `regress:fable5` holds the wall carries.  The docstring's rule 2 ("Every HELD
   marker's row must be NAMED IN THE QUEUE FILE") should say I2 is the enforcer for regress holds, or the loop
   should test regress holds before `continue`.  The sibling fixture `fx_noregress` (no regress entry) is caught
   as intended.

Nothing here reopens the row: the detector material at HEAD is the material that was reviewed, and it
discriminates.

## 2. `heldmasked` (closed; 09ded75)

**READ.**  The row's two entries, `check_stage_panels.py:205-233` (the `and not live` test precedes the count),
`stage_tokens.live_holds()`, the CHANGELOG `#534` paragraph "heldmasked WAS AN L3, NOT A FILING", OUTSTANDING_BUGS
21870-21876.

**RAN.**  The controls above (the fix's four rows are in the table: `CSP t_fullhold HOLD 9/9`,
`CSP t_fullclosed CLOSED-WHILE-HELD`, `CSP t_discharged complete`, `CSP t_samedayhold HOLD`); the exact pre-fix
reinstatement `M_count_beats_hold` (`if len(got) >= n_seats and not live:` -> `if len(got) >= n_seats:`) scores
42/49 at HEAD, reddening t_fullhold, t_fullclosed, t_samedayhold, t_partial, t_otherseat, t_notseatdis and
t_malformed; `M_discharge_ge` reds t_samedayhold.  On the REAL ledger at HEAD, `csp_HEAD.out` line 306:
`HOLD  pcc2c040assertrow review    9/9  awaiting: glm, deepseek, minimax, kimi` -- the owner's hold wins over the
full count, which is the whole fix; no CLOSED-WHILE-HELD anywhere, consistent with the re-disposition that the
other two of the "three stages" were discharged holds.

**FINDING (1).**  `t_discharged` -- one of the four rows the closure names -- is reddened by no shipped mutant
(see stagetokens finding 3).  It is NOT vacuous: `X_never_discharge` reds it (43/49, also taking t_partial,
t_shortdis, t_fqdis and the wall's discharged-hold row).  Under the accept-row rule a row is discharged by a
MEASURED kill, so the shipped table owes that mutant; FILE, one line.  The records are otherwise true: the witness
string, the "one live + two discharged" re-disposition, and the bug-file's italic correction all match what the
tools print today.

## 3. `fbsmlane` (closed; cdbe7d7)

**READ.**  The row (closure, `hold`, `witness`, `state_note`, the regress HELD marker and its question),
CHANGELOG `#537` (THE DEFECT / THE FIX / THE PIN / MEASURED / GATE 2), OUTSTANDING_BUGS 21949-21988,
`gate_offline.sh:936-954` (`selfmutant_one`), `:1094-1116` (the lane call and its comment), `:1130` / `:1153`
(SM_COVERED / SM_EXEMPT), `:1333-1343` (the #442 main lane), `selfmutant.py` whole, `fbpending_bound.why`,
`.old` / `.new`, `f2_pin/run537b.sh` and `f2_pin/out/P0-P4`, `gate/gate_offline_20260918_1959.log:480-555`,
`gate/g2_0830_names.txt` vs `g2_today_names.txt`, and `git diff cdbe7d7 HEAD` on the harness, the helper and the
device.

**RAN** (WSL Gentoo, `build_and_lane.log`, `lane_out/`):
* `git archive HEAD` -> `/tmp/gxrgh/GXEMUL-SEC`; `./configure` rc 0; `make -j12` rc 0 (19:30:19-19:31:49);
  **224 objects, `gxemul` 6,164,048 bytes, binary newer than every source** -- a clean baseline, not an inherited
  one.  The lane links 222 objects (224 minus `main.o` and `dev_footbridge.o`, the gate's own exclusion).
* `lane_rgh.sh` -- the helper invoked exactly as `selfmutant_one` does (same `selfmutant.py`, same fragments, the
  pin string and the relative `-I` flags both grep-confirmed present on the gate's own `selfmutant_one` line):

      P0  HEAD harness, the gate's R3 pin            SELFMUTANT_OK    killed by the named row: FAIL R3 ... cats, slowest legal
      P5  HEAD harness, the OLD R4 pin               SELFMUTANT_OK    killed by: FAIL R4 every case bounded  (R4 still kills; its defect is attribution)
      P6  the R3 pin with ONE space fewer            SELFMUTANT_SETUP "names 0 rows in the pristine run" (drift is loud, as the gate comment claims)
      P1  R3 blinded + R1 tightened, R3 pin          SELFMUTANT_FAIL  "detector failed, but NOT via the named row" (R1 x4 killed it)
      P2  the same composite, OLD R4 pin             SELFMUTANT_OK    the escape the pin move closes -- still reproducible at HEAD
      P3  R3 blinded alone, R3 pin                   SELFMUTANT_FAIL  "mutant applied but the detector did NOT report a failure"
      P4  R1 tightened alone, R3 pin                 SELFMUTANT_OK    via R3 -- the composite's second edit is inert alone (the licence for a composite)

  Every leg matches `f2_pin/out/` and the CHANGELOG MEASURED table; P5/P6 are this seat's additions and confirm the
  two sentences the gate comment makes about the pin.
* Records checks: the gate log's lane row (`:487-489`) is as the witness field says; `g2_0830_names.txt` (345) vs
  `g2_today_names.txt` (346) differ by exactly the added lane row plus the SC-manifest row's `got=` text -- the
  CHANGELOG's "exactly this lane's row plus that one row turning red" is precise; `rc_offline.txt` `rc=1`,
  "FAIL (1 of 346 checks)" = the closure's 345/346.
* Drift since cdbe7d7: `#548` added R5's lowest-peak clause and rows R6/R6b and changed two comments; `#556`
  added a records note to `selfmutant.py`; `dev_footbridge.c` moved under #539/#545/#548.  **The R3 row text, the
  `cats, slowest legal` case, the 8-space padding, the `.old` anchor's uniqueness and the pin are untouched** --
  P0's pristine arm proves all of it at once ("row id unique and green").

**THE QUEUE QUESTION -- is R3 the right pin, or is further lane coverage owed?  R3, and no.**
* P3 shows R3 is the ONLY row that sees this self-mutant: blind it and the detector reports nothing at all.  So
  R3 is not merely a good pin, it is the only pin the lane's own rule (5) -- name exactly one row that the mutant
  kills -- admits for `1 -> 0`.
* A second pinned row for R1 pins nothing about this mutant: R1 stays GREEN under it (the `.why`'s point, and P4
  shows R1's channel is the tightened composite, not the reset).  The helper takes one (mutant, row) per stem;
  "more lane coverage" would mean more MUTANTS, and the three other #442 hand-built mutants (pre-fix,
  one-callback, no-ceiling) are kill-table coverage of the HARNESS, recorded in `gate_offline.sh:1327-1332` with
  `#548`'s correction -- not this row's subject, which was a lane that could not run.  The lane is, in the gate's
  own words, a LIVENESS CONTROL "not a census".
* A drift-tolerant pin would trade P6's loud SETUP for the family-match the helper's rule (5) exists to forbid;
  an R3-only aggregate over the seven cases is the R4 shape one level down (P2 is what that buys).
So the closure is complete as it stands.  The `.why` and the gate comment already carry the pin's reasoning with
their provenance; nothing is owed.

**FINDING (1), wording L4.**  `ledger.json` row `fbsmlane`, `hold`: *"DISCHARGED by #537 (2026-09-18): the
SM_EXEMPT line is gone and the lane runs, pinned on R3."*  The SM_EXEMPT line is not gone: `gate_offline.sh:1153`
is `SM_EXEMPT="ieee_store:2099-01-01"   # #537: fbpending_bound moved to SM_COVERED`.  fbpending_bound's ENTRY in
it is gone.  Low: the same row's closure and state_note say it correctly ("moved SM_EXEMPT -> SM_COVERED").

## 4. `n6` -- the rule question: RULED (a)

**READ.**  The row's assess entries at HEAD; commit `017d0882` ("n6: the hold is discharged, and the answer
moved the round's shape in four places", 2026-08-30 20:39) and its ledger hunk -- the entry as first written;
the row at its parent `68af1a7e` (`state: held`, `hold: correct it inside the n5 fix round (R9)`, and a two-part
`hold_question`: K1 repoint -- oracle-correction or laundering, and what must be red first; the probe's liveness
and signature controls once the last kill goes); the 2026-09-18 entries [5]-[6] and the queue's 8n `n6` entry;
`stage_tokens.py`'s classification and the `t_selflate` row of the controls.

**Ruling: (a), a seat answer that re-opened the stage.**  Four reasons, in order of weight:
1. By the project's own structure.  The row was HELD with a question for the flagship seat; `live_holds()`
   defines a hold as discharged by an `is_answer` entry of the named seat dated strictly later.  The entry that
   discharged n6's hold therefore IS an answer by construction -- the tools' definition, not a hat label.  At HEAD
   `is_answer()` returns True for it (no token in its note) and the 09-18 record says so in words: "The 08-30
   entry stays untagged (an answer)".
2. By what it did.  It adjudicated no panel's findings (none existed; it "honoured the embargo while #497's table
   runs").  It produced NEW findings on the row's substance -- blast radius 1 arm -> 3 probes planting
   `0xE5907188`, repoint to +0x100 not +0x18c, the OR-accumulation signature replacing a RAM-indistinguishable
   readback, the title de-count -- and it refuted the row's own prescription.  That is a reading seat's answer to
   the assess question, self-graded with disclosure.  A main-loop adjudication record (NOTSEAT's class) disposes of
   OTHER entries' findings; this one made its own.
3. By its fields.  `d: "OK"`, `grade: CONFIRMED`, `outcome: UPHELD` -- answer fields; the NOTSEAT records on the
   same row carry `grade: ""`, `grader: ""`.
4. By consequence.  A post-cutoff answer by the annotating seat refuses the pre-policy grandfathering -- guard (i),
   rowed as `t_selflate` "the n6 shape, the one real disputed stage" -- so the stage owed the full panel.  That is
   exactly what the owner ruled on 2026-09-18 and what happened: `panel_20260918_133231`, all seven seats, and
   `csp_HEAD.out` prints `ok n6 assess 9/9`.
Why not (c): the prior flagship read the entry's self-description ("a READING seat's adjudication") rather than
its function; the words "adjudication" and "adjudicated" are the author's hat, and the commit that recorded the
entry calls it "the answer" in its title.  Why not (b): RE_READ asserts a SINGLE-SEAT re-read of a filing; the
stage already held two real answers plus the grandfather annotation, and the entry was new work, not a re-read --
agy's objection was right and the self-tag was rightly reverted.

Two consequences for the record, neither of which reopens anything:
* `n6`'s 2026-08-30 cell renders in class `pend` on the published matrix (stagetokens finding 4): the ruling says
  "answer", the dashboard colours it "seat failure".  `d: "✓"` on that entry, or the `D_CLASS` line.
* `fq_HEAD.out` line 1: `ok n6 regress owed and queued` -- #539's regress review of `n6` (commit 7836071) is
  counted as queued ONLY because `### `n6`` heads the 8n rule-question entry.  When this ruling discharges that
  entry, keep a heading for the regress review (or add the review), else rule 3 reds the next commit.

## Seat ledger
This phase is FLAGSHIP-ONLY by standing directive; no panel was convened and none was owed.  Seat: Fable 5.1
(`claude-fable-5-1`), identity by the liveness token and the verbatim CHECKPOINT line above.  No other seat was
fired or deliberately withheld.  Measuring basis: one clean HEAD build in a scratch clone (part 1 and part 2 both
satisfied there), the shipped controls run from a HEAD archive, HEAD's checkers on HEAD's ledger, two fixtures and
seven extra mutants of this seat's own.

## Where everything is (durable in the session scratchpad; `/tmp/gxrgh` is volatile and may be deleted)
`...\scratchpad\fable_rgh\`: `HEAD.sha`, `head.tar`, `headtools/` (archive of HEAD tools + controls),
`controls_HEAD.out` (+ `.err`, 0 bytes), `csp_HEAD.out`, `fq_HEAD.out`, `fx_regresshold/`, `rgh_extra_mutants.py`,
`extra_mutants.out`, `never_reddened.txt`, `build_head.sh`, `lane_rgh.sh`, `configure.log`, `make.log`,
`build_and_lane.log`, `lane_out/{SUMMARY.txt,P0_newpin,P1_composite_newpin,P2_composite_oldpin,P3_blindR3_newpin,
P4_tightenR1_newpin,P5_head_oldpin,P6_shortpin}.txt`, `led_68af1a7e.json`, `led_017d0882.json`.
