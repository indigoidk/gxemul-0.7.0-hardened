FABLE_DASHOK_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES (7) -- the renderer and the checker implement the ruled class and the ruled guard, every number in the ledger premises re-derives, and the 19 controls reproduce on HEAD in 4.5 s; but four one-token edits pass all 19 while breaking a ruled property (the inclusive cutoff is unpinned, a new explicit-blank `d` is unguarded, the tooltip and the legend are unread by any control), the tooltip asserts "not a seat failure" over 73 answers whose text says WALL / NOT-FIRED / SEAT REFUSED, the checker's failure path dies in a UnicodeEncodeError under the precommit's real cp1252 stdout, and the packet's entry total and R2 census are one commit stale.

Seat: Fable 5.1 (file-reading, measuring).  Everything below marked MEASURED was run in a temp mirror of the tree
(`scratchpad/dashok/stage`: `tools/pipeline/*.py` + the four staged files + `git show HEAD:tools/pipeline/ledger.json`,
HEAD = 8bf8b5a1), never in the project.  Nothing under the project was written except this file.

## Premises (section 2) -- re-derived, not ratified

| premise | MEASURED on HEAD 8bf8b5a1 | on the working-tree ledger |
|---|---|---|
| 5,167 entries | **5,177** (16512e9c and c64445fa have 5,167; 01aef04f at 21:40 added ten) | 5,177 |
| 1,397 explicit off-domain; 1,356 answers; 1,136 tuples; multiplicity <= 6 | 1,397 / 1,356 / 1,136 / 6 -- holds | identical |
| top `d` among answers | OK 439, N/A 248, y 89, 2026-09-09 63, 2026-09-10 56, blank 23, NOT-FIRED 22, NOT FIRED 14, HELD 10 -- holds | identical |
| latest 2026-09-19; none undated; none >= 2026-10-17 | holds; all 5,177 dates are ISO strings; all 3,170 explicit `d` are strings | identical |
| working tree holds no off-domain answer HEAD lacks | the two off-domain multisets are IDENTICAL and both EQUAL the staged baseline (1,136 tuples, sum 1,356; 0 extra either way) | -- |
| R2: ok 1413 hold 52 bad 17 tok 374 none 29401; pend 1503 -> 833; legacy 670 | **hold 53, none 29472**; ok 1413, bad 17, tok 374, pend 1503 -> 833, legacy 670 -- the receipt's census is of a 5,167-entry ledger, i.e. the staging copy predates 01aef04f | -- |
| strip `1687✓ 17✕ 34⏸ 2032… 1397 legacy · 5167 in all` | `1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all` | same |
| 439 stored OK / 365 displayed OK cells (Astra) | 365 legacy cells show `OK`; 670 legacy cells in all (OK 365, N/A 81, 2026-09-09 39, y 36, 2026-09-10 32, `?` 19, NOT-FIRED 6, ...) | -- |
| answer cell reached only after the hold and record branches | holds by reading `cell()`: `live_holds` -> held-unparseable -> records (`tok`) -> `_latest(answers)` | -- |

So the ledger premises hold and the tool premises hold; the ENTRY TOTAL and the R2 cell census are stale by one commit
(frozen-number class: "measured on HEAD" named a HEAD the staging copy did not have).  The off-domain population did not
move, so the baseline is correct for HEAD; only the record is wrong.

## 1. The ruling

**Implemented as ruled.**  `cls = D_CLASS.get(d, LEGACY)` puts every explicit `d` outside the four glyphs in one class
(R1: OK, blank, N/A all `legacy`; a near-glyph `✗` U+2717 lands there too); a missing `d` is `…` (R1 codex -> pend);
holds and records are untouched (hold 53 and tok 374 identical before/after on HEAD; the hold and record branches precede
the answer cell); the text is kept, escaped; the strip's five numbers sum to the entry total (5,177 on HEAD).

**"legacy -- verdict unclassified" is Astra's phrase minus one word.**  Astra wrote *"legacy OK — verdict unclassified"*
(`codex_adjC.txt:55`); the ruling re-keyed the class on the domain, so dropping "OK" is required, not a liberty.  Faithful
in substance, not verbatim -- say so rather than "Astra's wording".

**Two claims the data does not support, one of them in product text:**

* The tooltip ends *"(not approval, not a seat failure)"* and the legend says the same.  MEASURED: **73 of the 1,356
  off-domain ANSWERS carry a `d` that names a seat non-answer** -- NOT-FIRED 22, NOT FIRED 14, HELD 10, WALL 7,
  WALLED-COVERED-BY-SUBSTITUTE 2, SURVIVOR-SKIP-FULL-ROT 2, SEAT REFUSED 1, P2-SEAT-DOWN 1, F2-NOT-FIRED 1, FAIL 1 ...
  -- and **20 displayed legacy cells** show such text.  A hover on one reads *"d = 'WALL' is none of ✓ ✕ ⏸ … (not
  approval, not a seat failure) — 2026-08-27 — UNKNOWN"*: the dashboard telling a reader that a recorded wall was not a
  seat failure.  The ruling's words are "neither approval nor a seat failure" as a statement about the RENDERING; the
  tooltip states it about the ENTRY.  Reword to the rendering: *"legacy -- verdict unclassified: d = 'WALL' is none of
  ✓ ✕ ⏸ …; counted as neither approval nor seat failure -- read the text"*.  Same in the legend.  (Change 3.)
* The legend's *"an older entry's verdict text"* is loose for the 128 date-valued and the 8 `NO-SURVIVING-D-MUTANT`
  `d`s, and "older" is true only while Q2 holds.  Tolerable; the first point is the one that matters.

Nits: when a stage exemption is refused, that line is inserted at 0 AFTER the legacy line, so the legacy reason is
second, not first (arguably the right precedence; the packet's "opens with" is then not always true).  The five `✗`
(U+2717) answers -- `b47`/research/codex 08-15, `b27`/research/codex 08-15, `fbdiv`/review/minimax 08-15,
`wdcflood`/review/kimi 08-25 x2 -- are objections in a lookalike glyph and are the obvious first candidates for a READER's
one-at-a-time rewrite; no sweep, as ruled.

## 2. The grandfathering key

**Right key, right exclusion, one inherent hole, one real friction, no mechanical guard on the baseline.**

* Note out of the key: right.  A correction or a defanged marker must not re-arm an entry; C10 and the note-free tuple
  make that hold.
* An edit that adds a NEW off-domain answer and passes Q2 -- MEASURED rc 0: rewrite `alphactxfail`/assess/codex/
  2026-09-08/`y` to `✓` (allowed) and append a brand-new entry with that same (row, phase, seat, date, d) and a new note.
  The freed slot is reused; the multiset is unchanged.  Inherent to a note-less count key; it requires back-dating onto
  an existing (row, phase, seat, date), which the diff shows.  Disclose it in the docstring as the key's known shape.
  (The other "pass" is the token-quoting hazard the carrier already names: a note that quotes `[NOT A SEAT ANSWER]` is
  exempt by `is_answer`; not new here.)
* An edit that blocks a legitimate change -- MEASURED rc 1: correct that same entry's date by one day (a typo fix) ->
  `NEW OFF-DOMAIN ANSWER ... date 2026-09-09 d 'y' -- not among the 0 grandfathered entries of this tuple`.  The same
  happens to a row rename, a seat-id or phase correction.  The editor's only honest exits are to read the entry and glyph
  it, or leave the typo.  Acceptable, but the packet's "Q2 is HARD (it can only fail on an entry added after it lands)" is
  false: it fails on any edit that changes a grandfathered tuple.  Write that into the Q2 comment and the docstring.
  (Change 6.)  Dropping `date` from the key would tolerate date fixes at the cost of widening slot reuse to any date;
  I do not recommend it, I name it.
* The writer's placement is **not a guard**.  Anyone can run it, or hand-edit the tracked baseline, and commit; nothing
  in Q2 looks at the baseline's history.  The date test is the only thing that survives a re-baseline (see 3).  Cheap
  structural guard, three lines in the Q2 block: when HEAD has `tools/pipeline/entry_domain_baseline.json`, `cmp` the
  working copy against `git show HEAD:...` and `bad` on any difference ("the frozen baseline changed -- the population
  can only shrink, and shrinking needs no re-freeze because the checker tolerates spare count").  One control: a
  modified baseline -> BAD.  (Change 7.)

## 3. The cutoff

* What the date test adds, given the baseline: exactly one real property -- a re-baseline, honest or not, cannot admit
  an entry dated on/after the cutoff, so a launderer must also back-date, which the diff shows.  Otherwise it is
  redundant: every C-row that reds for the date also reds for the baseline (C3, C4), and C12 is the only row where the
  date test is load-bearing, at 2026-10-20.
* **The inclusive boundary is unpinned.**  MEASURED: `CUTOFF = "2026-10-18"` passes 19/19; `"2026-10-20"` passes 19/19;
  only `"2026-10-21"` trips C12.  C3 ("on the cutoff, d OK (inclusive)") reds for the baseline reason, not the one it
  names -- carrier rule 4, "did it fail for the reason under test?".  Repair: give C3 the C12 shape at the boundary --
  the on-cutoff tuple IN a fixture baseline -- MEASURED: real checker rc 1 ("dated on or after the cutoff"), the 10-18
  mutant rc 0.  (Change 1.)
* Malformed dates: none exist (all 5,177 dates are ISO strings).  A NEW entry with a malformed date is refused whatever
  the string, because its tuple is new -- but the printed REASON can be wrong: `"9/9/2026"`, `"2026-9-9"` and
  `"Oct 18 2026"` all sort above `"2026-10-17"` and are reported as "dated on or after the cutoff".  A non-string date
  (JSON integer) -- MEASURED: `TypeError` -> rc 1 with a traceback; RED, misattributed.  Astra asked for the
  malformed-date treatment to be specified: one `re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)` reported as its own reason
  does it.  Fold into change 4 or file; I count it under 4.

## 4. The controls

Failability, row by row: C1 reds when the baseline does not cover the ledger (C11 proves it); C2 is the positive and
reds if a glyph were refused; C3 reds (wrong reason, above); C4 reds for both reasons; C5, C6, C9 red for the baseline
reason they name; C7 reds if a missing `d` were treated as off-domain; C8 reds if `is_answer` were dropped (that mutant
also turns C1 red); C10 reds if shrink were refused; C11 and C12 are real mutants; C13 pins rc 2 for an unreadable
baseline only.  R1 pins class AND glyph per seat (the two R3 mutants prove the fallback is load-bearing); R2 pins the
cell census and the strip's arithmetic -- not the total against the entry count, not the legend, not the tooltip.
W1/W2 pin only the first line's `GOOD`/`BAD` prefix.

**Smallest edits that pass all 19 and break a ruled property -- all MEASURED at 19/19:**

| edit | breaks |
|---|---|
| `CUTOFF = "2026-10-17"` -> `"2026-10-18"` (one token) | "inclusive 2026-10-17 -- fails even if its tuple were in the baseline" |
| checker `if "d" not in x or ...` -> `if not x.get("d") or ...` | "every explicit `d` outside the four": a NEW entry with `d: ""` passes Q2 (C1 drops to 1333/1333 and still passes) |
| delete the two-line `tip.insert(0, "legacy -- verdict unclassified: ...")` | "the reason first in its tooltip" |
| delete the legend `<span>` line | "labelled 'legacy -- verdict unclassified'" |
| precommit `elif [ $_cedrc -eq 1 ]` -> `-eq 7` | message attribution only: W2 still starts `BAD ` ("could not run (rc 1)") |

Repairs, all L1: C3 re-cut as above (change 1); a C6b -- a new entry dated after the cutoff with `d: ""` -> rc 1
(change 2); R1 or a new R4 asserting the tooltip prefix and the legend line are present in the rendered fixture
(part of change 3, so the reworded text is pinned the day it lands).  The precommit branch nit is not worth a control.

**The controls also run the Q2 block in an environment the precommit does not have.**  `run_checker` and W1/W2 inject
`PYTHONIOENCODING=utf-8`; `precommit_check.sh` sets neither that nor `PYTHONUTF8`, and git-bash's Windows python 3.12
has cp1252 stdout on a pipe.  MEASURED, with the precommit's own shape `_ced=$(python "$CED" 2>&1)` and no env var:
a new OK after the cutoff -> rc 1, 12 lines, the last one `UnicodeEncodeError: 'charmap' codec can't encode character
'✓'` (the `-> give each a d from ✓ ✕ ⏸ …` hint dies); a new `✗` -> rc 1, 11 lines, the ENTRY line itself dies on
`%r`.  Still RED (rc 1 either way), but the operator gets a traceback where the instruction should be.  The other 25
precommit-wired checkers print no non-ASCII in any `print()` (measured, 0 hits), so the house idiom is ASCII output or
none.  Fix: `sys.stdout.reconfigure(errors="backslashreplace")` at the top of `main()`, and run W1/W2 WITHOUT the env
var so the control exercises the precommit's environment.  (Change 4.)  `run_controls.py` itself needs `-X utf8` or the
env var to print R2's strip -- the same mechanism my first census crashed on; the receipt does not say how it was run.

## 5. Display

* `?` for an explicit blank: right, and whitespace-only renders `?` too (measured).  A JSON `null` renders the text
  `None` in the legacy class (measured) -- no instance exists, Q2 refuses new ones (`d 'None'`, rc 1); nit only.
* HTML-escaping every `d`: right, and it changes NO existing cell -- 0 of 3,170 explicit `d` carry `& < > " '`
  (measured on HEAD); a `<b>&` fixture renders `&lt;b&gt;&amp;`.  The nine non-ASCII `d`s (`✗` x5, `—` x4) are
  untouched by escaping.  The tooltip's `%r` is escaped with the rest of the tip, so a `d` with a quote is safe.

## 6. Which dispositions are wrong -- count checked: 10 (the five section-2 premises and the five section-3 dispositions)

Wrong or overstated, 4:
1. "5,167 ledger entries", the strip `2032… · 5167 in all`, and R2's `hold 52 / none 29401` -- one commit stale; HEAD is
   5,177 / `2042…` / hold 53 / none 29472.  Re-run the controls on HEAD (4.5 s) and re-stage the receipt before the
   landing cites any of them.  (Change 5.)
2. "Q2 is HARD (it can only fail on an entry added after it lands)" -- a grandfathered entry's date/row/seat/phase
   correction fails it (measured).  (Change 6.)
3. "C12 shows the date test is load-bearing" -- at 2026-10-20 only; "inclusive 2026-10-17" is pinned by nothing
   (measured, three cutoff values).  (Change 1.)
4. The tooltip/legend parenthetical "(not approval, not a seat failure)" -- contradicted by 73 answers and 20 displayed
   cells.  (Change 3.)
Half-wrong, 1: "Astra's wording" -- Astra's minus "OK".
Hold, 5: the key as the (row, phase, seat, date, d) multiset with the note out; the baseline equals HEAD's population
exactly; the working tree adds nothing; `?` for blank and the escape; the strip's five-number sum.

## The seven changes, in landing order

1. C3 re-cut so inclusivity is load-bearing (the C12 shape at 2026-10-17; measured real rc 1 / 10-18 mutant rc 0).
2. A control for a NEW explicit-blank `d` after the cutoff (rc 1); the `not x.get("d")` mutant must red it.
3. Tooltip and legend reworded to a claim about the rendering, pinned by a control that reads them.
4. The checker's failure path encoding-safe (`reconfigure(errors="backslashreplace")`), a "malformed date" reason, and
   W1/W2 run without `PYTHONIOENCODING`.
5. HEAD's numbers in the record: re-run `run_controls.py` on HEAD and re-stage `RECEIPT_staged.txt`.
6. The Q2 comment and the docstring say what Q2 also fails on (any change to a grandfathered tuple) and disclose the
   freed-slot shape.
7. A frozen-baseline check in the Q2 block (cmp against `HEAD:` when HEAD has the file), with its one control.

None of these touches the ruled class or the ruled grandfathering; 1-2 and the control half of 3-4 are L1
(pre-ship construction), the text halves of 3, 5 and 6 are L4 (wrong record), 7 is the structure-first rule applied to
"the checker only reads it".

## What I could not check

* The other seats' answers: `codex_dashok.txt` and `grok_dashok.txt` were 0 bytes when I looked; I did not wait.
* The landing's effect on precommit section Q: the working tree's `matrix.html` is already modified (the peer's), and
  the landing must regenerate it with the NEW renderer or Q reds; I did not simulate the commit.
* `write_baseline.py` was not run (the baseline's equality with HEAD's population was verified directly instead).
* Whether the staging copy that produced the receipt was `cp -a`'d before 21:40 or built from an older HEAD: inferred
  from the entry counts (5,167 = c64445fa/16512e9c) and the receipt's 22:23 mtime, not observed.

Durable artifacts of this review: the mirror and its mutants live only in the session scratchpad
(`scratchpad/dashok/stage`, `stage_cut_2026-10-{18,20,21}`, `stage_m2_blankd`, `stage_m3_tip`, `stage_m4_legend`,
`stage_m5_pre`, `fx/`); every number above is reproducible from the staged files plus `git show HEAD:tools/pipeline/
ledger.json` in under a minute, which is why I did not copy them into `regress/artifacts/`.
