FABLE_DASHOKV4_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP WITH CHANGES (18) -- the shipped CODE (checker, renderer, Q2) is correct on every input I could build and every
recorded kill reproduces (72/72 and 66/66 byte-identical in a mirror); the ENUMERATION is not complete: 21 one-edit mutants not
in the table pass all 72 controls, of which 15 break a decision the CONTRACT lists as pinned, and six records sentences are
false or unreproducible.  All 15 have one shape -- a pin that tests ONE edge of its decision (the trailing end, the first
literal line, the number but not the label, a substring but not the whole, one branch of three) -- so the chain does not close
on this pass; it closes on the next, narrow one, if the rows below land and nothing survives adjudication.

Fable 5.1 review seat (this agent; `agent_models.py` is the main loop's to run).  Everything measured ran in a MIRROR under my
session scratchpad -- a copy of `tools/pipeline/{stage_tokens.py,ledger.json,gen_dashboard.py}`, `tools/precommit_check.sh` and
the whole `regress/artifacts/dashokclass_20261016/` tree at the same relative layout, so both runners' `REPO` derivation resolves
inside the mirror.  Nothing was written into any project tree except this file.  Labels: MEASURED = run; READ = the file opened;
REASONED = derived from a reading without a run.  Every number names its deriver.

## 0. What I measured (the facts the answers rest on)

* **The 72 controls reproduce.** `run_controls_v4.py` on the staged v4 files in the mirror: 72/72 in 18 s, BYTE-IDENTICAL to
  `RECEIPT_v4_on_staged_v4.txt` (diff after trailing-space strip: none).  The receipt's header md5s 79e2497e / 516df040 /
  ee874ba0 / 06a3ffc6 are the staged files' md5s today (`md5sum`).
* **The 66-mutant table reproduces.** `run_mutants_v4.py` in the mirror: `KILL TABLE: 66/66 as recorded`, `DASHOKCLASS_MUTANTS_DONE`,
  the body BYTE-IDENTICAL to `KILLTABLE_v4_staged.txt` (`#` path lines excluded) -- every tally, kill list and named killer,
  `d_notenone`'s escape included.
* **The census reproduces on the working tree AND on HEAD's own ledger.** The working-tree `ledger.json` is dirty against
  8bf8b5a1 (29+/29-: two rows re-ordered, one non-off-domain date 2026-10-02 -> 10-06); my census (`scratchpad/census.py`, the
  repo's `stage_tokens`) on both files is identical on every number: 5,177 entries; 1,397 off-domain entries, 1,356 answers, 41
  non-answers (36 HELD, 5 NOTSEAT); all 1,397 `d` values strings, 0 null; OK 439, N/A 248, y 89, blank 23 (29 entries), NOT-FIRED
  22, NOT FIRED 14, HELD 10, WALL 7; latest off-domain answer 2026-09-19; 0 off-domain answers with an empty note; 21 ⏸ and 35 …
  answers; 1,342 keys over 1,356; the baseline 1,342 rows summing to 1,356, 0 non-ISO dates, max multiplicity 5; every ledger key
  in the baseline and every baseline key in the ledger.
* **`dashmissingd_census.py` on HEAD's ledger**: 5177 / 1561 (2026-08 174, 2026-09 1244, 2026-10 143; latest 2026-10-16) / 300 /
  2953 / 814 / 682 -- identical to `DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`.
* **The staged renderer on HEAD's ledger**: 670 legacy / 833 pend / 1413 ok / 53 hold / 17 bad / 374 tok cells; the strip
  `1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all`; the class line present and first in all 670 legacy tooltips; 365 legacy glyphs
  `OK`, 305 not.  Rendering `r_norecord` on the same ledger changes EXACTLY 32 cells' tooltips (ok 3, legacy 9, pend 17, hold 2 =
  ⏸-answer cells, bad 1): Astra's J1 "32" is exact.
* **`gen_dashboard_before.py` is HEAD's renderer byte for byte**; the working-tree `precommit_check.sh` equals HEAD's in content
  (git shows it modified, line endings only); staged v4 differs from both by exactly the 32-line Q2 block.  "Installed byte for
  byte" clobbers nothing.
* **Section H** (`check_stage_panels.py` :184-212, READ): `if not st.is_answer(ent): continue`, then `len(got) >= n_seats`,
  n_seats = len(ledger["seats"]) = 9, `STAGES = ("assess", "research", "review")`, no roster vocabulary.  The staged precommit
  runs `set -u` (:22) and no `set -e`; `bad () { fail=$((fail+1)); printf '  FAIL  %s\n' "$*"; }` at :37, `good ()` at :39, the
  tail `if [ $fail -gt 0 ]; then ... exit 1 fi ... exit 0` -- the W rows' counting stand-ins model them faithfully (the
  CONTRACT's "correct by inspection" is now my inspection).
* **My own sweep**: 29 one-edit mutants of the staged v4 files, each through the 72 controls in the mirror
  (`scratchpad/extra_mutants.py`; `extra_mutants.out`, `extra_mutants2.out`, `extra_mutants3.out`), with a POSITIVE CONTROL
  (`r_ok`'s edit) that reddened R1 R1b R1d R1e R1f R1g R1h R2 R3 as the table says, and `r_sumor` (an explicit blank counted
  as …) killed by R2 as predicted -- the driver detects kills.  Results in sections 2 and 3.  Twelve of the 29 were hypotheses
  from the landed codex and grok answers, measured here rather than taken.

## 1. My own findings (J8, J9, J10, J16) -- disposition AND fix

* **J8** (R1 pinned ONE cell's tooltip) -- PINNED is right and the fix is right: `r1g()` (READ :479-492) requires the WHOLE escaped
  tooltip for seven `d` values among all legacy cells; both my mutants die on R1g (table).  The two non-simple legacy cells are
  R1e/R1f's -- and R1e is a SUBSTRING check (the record line, the class), which is why `r_tipnorecord` below escapes it.
* **J9** (null d; padded glyph; NOTSEAT half; the hint) -- right for the hint and the null (C26, C11); HALF right for the other two.
  R1h pins the padded glyph on the RENDERER only: `d_dompad` (`str(x["d"]).strip() in DOMAIN`) passes all 72 (MEASURED), so Q2
  would wave through an answer the dashboard shows as legacy ` ✓` -- the two-files-disagree class this round exists to close.
  And C24 is CONFOUNDED (Astra's point, verified by census): `d_isheld` newly selects HEAD's 5 off-domain NOTSEAT records, so C24
  reds for the ledger's reason, not its own entry's.  Fixes owed: a checker-side padded-glyph row; C24 isolated like C2c/C2d.
* **J10** (three records sentences) -- CORRECTED, and the corrections are right (the docstring's "upheld there without
  restatement" :10-12; grok's entry; the H collision in the filing).  One correction against my own v3 numbers: the row's
  "158 entries ... 127 untokened ... 71 with no d" is a keyword-screen count whose regex my v3 answer did not record, and I cannot
  reproduce it: seven plausible screens on HEAD's ledger give 110-222 / 101-200 / 47-87 (`NOT FIRED|not fired|roster`,
  case-insensitive: 205 / 183 / 87).  The deriver rule: add the screen to `dashmissingd_census.py` beside its NOANS regex and
  cite that output, or mark the three numbers "by a keyword screen, unreproduced".  Astra and Grok could not reproduce them
  either, for the same reason.
* **J16** -- right: answered seats carry `d` ✓ with their own verdicts; the five not-fired entries carry no `d` (5b); section 5.

## 2. The enumeration -- is the CONTRACT complete?  No: fifteen decisions it lists as pinned have an open edge

Every decision checked, by the CONTRACT's own lines, READ against the staged files, the pin tested by the table's mutant or mine:

**checker**
* ledger shape -- C21a-f/C23 pin `ledger_shape` (READ :95-112) and the four shape mutants die there.  MEASURED beyond the rows:
  a rows-ABSENT ledger (`{}`, `{"seats": []}`) is rc 2; a note that is a list / None / dict is REFUSED rc 1, a bool note rc 2
  (no mis-typed note is skipped as a non-answer -- GLM's hypothesis refuted); an entry with no `seat` key is refused rc 1.
  `{"rows": []}` and a row without `entries` walk as empty and pass, and both are well-formed.  **HOLDS.**
* baseline shape -- "a list of [6 strings, positive int]" pinned by C13, C17, C21g: list-ness and a string count only.
  **OPEN (MEASURED, each passes all 72): `len(k) == 7` -> `>= 7`; `type(k[6]) is int` -> `isinstance` (a `true` count);
  `k[6] > 0` -> `!= 0` (a negative count); the six-strings test narrowed to five.**  Harm bounded by the md5 pin on the default
  path (a misshapen DEFAULT baseline cannot land without a reviewed re-freeze) -- an overclaim of the CONTRACT line: four
  override rows (rc 2 each), or DISCLOSE them beside `k[6] > 0` with that reason.  Astra's qualification of the existing
  disclosure is right: `> 0` -> `>= 0` is equivalent for the ceiling arithmetic, not for the promised malformed-baseline exit.
* md5 pin, CRLF fold, override skip -- C18/C18b, C11/C12/C17.  **HOLDS.**
* the selection -- C7, C14, C2/C2b/C2c/C2d (their own witnesses: the shipped 21 ⏸ / 35 … answers are why the v3 rows reddened
  for the ledger's reason), C8, C24 (confounded, above), C26.  **OPEN: the checker-side padded glyph (`d_dompad`).**
* the key, byte for byte -- the CONTRACT says "C25a-k: a suffix, a trailing space, a case change, a row move" and discloses
  "whitespace-stripping INSIDE a field rather than at its ends (C25 edits the ends)".  **C25 edits the TRAILING end only, and the
  row id by a move only.  OPEN (MEASURED): `d_rowstrip` (`str(r.get("id")).strip()`), `d_datelstrip` (`v.lstrip()`), `d_dlstrip`
  (`str(x["d"]).lstrip()`) each pass all 72; seat/phase/note `.lstrip()` are the same edit (REASONED).**  `d_rowfold` dies on C1
  because frozen answers sit in some of the 7 of 912 rows whose id carries upper case (one-sided, like `d_dfold`).  The
  disclosure sentence is false as written.
* the ceiling -- `seen[t] > base[t]`, C9/C10/C15, `d_dupplus1`, `d_nonote2`.  **HOLDS.**
* the cutoff -- inclusive, ISO-shaped, isolated, far: C3/C4/C12x4/C19a/b and five table mutants.  **HOLDS at the dates
  tested; one edge open: `^...$` on the ISO regex (`d_isodollar`) passes all 72** -- a MATCHED identity dated
  `2026-10-17T12:00:00` is no longer refused by date (the docstring's "OPENS with the ISO shape" :50).  Equivalent on the shipped
  baseline (all 1,342 frozen dates are before the cutoff, latest 2026-09-19, and a suffixed on-or-after answer cannot be frozen
  without a re-freeze), so one C12 row with a suffixed matched identity pins it.  `ISO.match` -> `ISO.search` passes all 72 and is
  equivalent on every refusal outcome (the reason's wording differs) -- disclose.
* output -- cp1252-safe (C20), every refusal named (C11, W2), "the reason named" (C19 for the ISO sub-reason, C11 for the hint).
  **OPEN (MEASURED): the cutoff refusal's reason replaced (`d_cutreason`), the ceiling refusal's reason emptied (`d_ceilreason`),
  and the refusal line's row/phase SWAPPED (`d_rowphaseswap`) each pass all 72** -- C11 counts lines, W2 checks the prefix, nothing
  reads the identifiers or the two main reasons.  A committer meeting `OFF-DOMAIN ANSWER ... -- x` has lost the instruction.
* the summary line -- `d_summary`/C11 pins the within-count; `d_baselen`/C1 pins `sum` against `len(base)`.  **OPEN: in C1 and
  C11 -- the only rows that read the baseline number -- it EQUALS the within-count (1356/1356, 0/0), so `sum(base.values())` ->
  `len(cur) - len(bad)` (`d_basewithin`) passes all 72 (MEASURED).**  Cosmetic, pass all 72, NOT owed: "inclusive"
  (`d_cutoffmsg`), "(none)" (`d_datenone`), the undated refusal also saying "not ISO" (`d_hintundated`).
* `str(x["d"])` in the key -- `d_nostr` passes all 72: equivalent for every type the baseline can hold; a list/dict `d` would
  raise an uncaught TypeError, rc 1 WITH a traceback (REASONED).  Disclose.
* the glyph set -- C27.  **OPEN: pinned by TEXT, not by VALUE -- `literal()` returns the FIRST line starting `DOMAIN = ` /
  `D_CLASS = `, and a SECOND assignment later in the file is the effective one and passes all 72 with a fifth member "ZXQ"
  (`d_domredef`, `r_dclassredef`, MEASURED).**  J11's class, reopened at the pin.

**renderer** (the 32 changed lines against HEAD, READ): class on the answer a cell shows (R1 per seat, the HELD with `d "HELD"`
and the NOTSEAT record with `d "OK"` both in the fixture -- GLM's fourth hypothesis is answered by the fixture itself); whole
tooltips R1/R1g; escape R1b; `?` R1d; padded glyph R1h; strip R2; legend R4; R3.  MEASURED beyond the rows: an explicit
`"d": null` renders `legacy` with glyph `None`.  **OPEN (MEASURED, each passes all 72):**
* `if cls == LEGACY and all(st.is_answer(x) for x in mine)` (`r_tipnorecord`) -- drops the class line from the 32 cells with an
  adjoining record; R1e checks the record substring, not the whole tooltip;
* `if cls == LEGACY and d is not None` (`r_tipnotnull`) and `d = ent.get("d") if ent.get("d") is not None else "…"`
  (`r_nullpend`) -- an explicit null loses its class line / renders pend; no renderer null fixture (HEAD has none, C26 refuses new
  ones, but the ruled class is "every explicit `d` outside the four");
* `{n[LEGACY]} legacy` -> `{n[LEGACY]} approved` (`r_striplabel`) -- the strip prints "1397 approved"; R2 reads numbers, not
  labels;
* `n[str(d).strip() if str(d).strip() in D_CLASS else LEGACY]` (`r_sumstrip`) -- a padded glyph counted as its glyph; R2 recomputes
  on the shipped ledger, which has none.
* `str(d).strip()` -> `.strip(" \t")` (`r_wsset`) is REPORTED killed by R3 -- but only because R3's find-text for its `noescape`
  mutant is no longer present (a presence pin, the carrier's MUTANT-TEXT-NOT-FOUND property); behaviourally R1d (space, tab) is
  green and a newline- or NBSP-only `d` stays invisible.  Minor; one fixture entry.
* `r_recheld` (the record loop without `and not st.is_held(x)`) passes all 72 -- HEAD code outside the diff; a HELD marker in no
  parseable shape beside an answer would gain a record line.  Note, no row.  The added CSS (`font-size:11px` -> `0` makes the
  legacy text invisible) is read by no control -- REASONED, Astra's point; disclose or presence-pin the two added rules.

**Q2** -- the three branches (W1/W2/W3 first-line words), the checker absent (W6), both env strips (W4/W5), the named lines (W2).
**OPEN, and the most consequential survivor of the pass: `else` -> `elif [ $_cedrc -eq 2 ]; then` (`w_elif2`) passes all 72
(MEASURED; Astra's find).**  The shipped `else` is right; nothing pins it, so a narrowing leaves rc 127 (python absent), 126, or
a crash status silently GREEN -- the check-that-cannot-fail shape in the guard's own wiring.  Dropping `2>&1` passes all 72 and is
equivalent for the checker's own messages (all on stdout).

Zero floor breaches in the PRODUCT code: every passing mutant is a mutant of correct code.  The breaches are of the CONTRACT's
claims, and they share one shape -- each pin tests one edge of its decision and the dual edit walks through the other.  That is
the class v5 should close in one diff rather than cell by cell: **for every pin, build the edit it would NOT see (the other end,
the second assignment, the label, the whole string, the third branch) and row it.**

## 3. The kill table and the floor

* **Is any mutant killed for a reason other than the one its line names?**  Every named killer is among the reds, and the runner
  only requires that (READ; MEASURED 66/66).  Three attributions deserve a sentence: `d_nodate` is "no date TEST" (`if False:`),
  so C12 on/after/far reddening is its named reason; `d_isheld`'s C24 red is the ledger's (5 NOTSEAT records), so isolate C24;
  and the three one-sided folds are killed by C1 as named BUT the runner's comment and J15 say "these normalised keys miss the
  baseline everywhere" -- MEASURED on HEAD's 1,356 frozen answers: the d fold changes **1,100** keys, the note strip changes **2**,
  the note fold **1,352**.  The kills stand (C1 asserts the exact within-count); the sentence does not.  C25e/f are absent from
  those kill lists not because they cannot see a note normalisation but because the bulk mismatch makes every rc-1 row pass
  trivially; if the two edge-whitespace notes were ever tidied, `d_notestrip` would stop dying on C1 and start dying on C25e.
* **One-edit mutants NOT in the table that pass all 72 and break a ruled or CONTRACT-pinned property** (MEASURED, section 2):
  `d_dompad`, `d_domredef`, `r_dclassredef`, `d_rowstrip`, `d_datelstrip`, `d_dlstrip`, `d_cutreason`, `d_ceilreason`,
  `d_rowphaseswap`, `d_basewithin`, `d_isodollar`, `r_tipnorecord`, `r_tipnotnull`, `r_nullpend`, `r_striplabel`, `r_sumstrip`,
  `w_elif2` (17); the baseline-shape four (`d_len7ge`, `d_boolcount`, `d_negcount`, `d_str5`) break the shape claim on the override
  path.  Equivalent on every ruled outcome, disclose: `d_isosearch`, `d_nostr`, `d_hintundated`, `d_datenone`, `d_cutoffmsg`;
  outside the diff: `r_recheld`; presence-pinned only: `r_wsset`.
* **Shapes swept** (the denominator): the cutoff literal / compare / prefix length / ISO anchor at both ends; `date_str`'s repr;
  the summary's three numbers against len(seen), len(cur) +/- len(bad), len(base), sum; both refusal reasons, the identifiers,
  the hint; DOMAIN membership (strip, fold, a second assignment); the selection predicate (missing, blank, null, held, record);
  each of the six key fields stripped at either end, folded, truncated, one-sided and coherent where a coherent form exists; the
  ceiling compare; the loader; the baseline validation (list, length, strings, int vs bool, sign); the md5 pin's path condition
  and fold; `reconfigure`; `ledger_shape` at every level and its or-default forms; the except-arm's rc; the renderer's class map
  and values, the fallback, null handling, the tooltip insert's position, text and condition, the record and held loops, the
  refusal insert, the glyph's escape and whitespace set, `summary()`'s default, membership and dict, the strip's order, labels
  and total, the legend, D_CLASS redefinition, the CSS; Q2's branches, the catch-all, env strips, path, `head`/`sed`, `2>&1`, the
  missing-file branch.  Not swept: two-condition edits; the controls' own code as a target; `stage_tokens.py`.

## 4. The records (section 5) -- six to fix

1. **Two stale TITLE lines** (READ): `staged_v4/tools/precommit_check.sh:496` "... OR IS A FROZEN LEGACY ENTRY" and
   `check_entry_domain.py:2` "... OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED" -- the entry-identity wording the landing
   retires three paragraphs later; J7 fixed only the `say` line (carrier rule 2: grep the siblings).  Astra found the same two.
2. **5d: "killed by exactly C15/C16 and C25d"** -- false of v4: the table kills `d_nonote2` by C15 C16 C25e C25f.  (GLM found it;
   the mirror table confirms.)
3. **"miss the baseline everywhere"** (runner comment, J15, 5d) -- 1,100 / 2 / 1,352 of 1,356.
4. **5c: "5,150 at the ruling's HEAD"** -- MEASURED over the last twelve ledger commits: 5,150 is the count at **e483d931
   (2026-10-09 20:53)**; at c64445fa, which committed RULINGS_C, and at its parent, 5,167.  Name the commit.
5. **`dashmissingd`'s "158 ... 127 ... 71"** -- section 1, J10.
6. **The CHANGELOG's and the closure's "the controls' CONTRACT names each decision's pinned edges and what is disclosed"** and the
   CONTRACT's "C25 edits the ends" -- false until the rows below land.  (Grok and Astra flag the first.)
Timing, not a change: the closure's "four passes ... four-seat roster each time" is true-able only after all four v4 answers are
read -- at 02:29:45 grok sat at 275 bytes unchanged for 13 minutes and I nearly wrote it up as stalled; at 02:38:09 codex (9,230
bytes, 02:32) and grok (9,732 bytes, 02:35, exit file) had landed.  Slow, not dead.  Everything else in section 5 is TRUE of what
ships (section 0), including every number, "68/72 on v3 = the four C21 rows", and `run_mutants.py` naming `run_controls_v2.py`.

## 5. The NOTSEAT disagreement -- ruling

**Upheld for this landing: the five not-fired entries stay untokened; the disagreement travels into `dashmissingd` as a RULE
question with a named mechanism.**  All four seats land here, each from the H reading (Astra withdrew the unilateral NOTSEAT) --
count the arguments: `is_answer` (READ `stage_tokens.py` :65-69) returns True for every untokened note, so a "NOT FIRED" entry is a
seat-answer only because no token exists for what it is -- a defect of the token VOCABULARY, not of these entries; H (READ) counts
recorded seats by that predicate and requires nine with no roster notion, so NOTSEAT-tokening them turns the review stage red at
4/9 and blocks the commit -- H doing its job under "if a seat cannot be run, STOP AND ASK THE OWNER", except that the owner HAS
ruled a four-seat roster and nothing in the ledger can say so; NOPANEL would be false and stage-scoped.  Today's practice is honest
in the NOTE and wrong in the GLYPH (an untokened no-`d` entry renders `…`, the seat-FAILURE glyph, which the carrier's own ledger
section says a deliberately-not-fired seat is not); Astra's would be honest in the glyph (∅) and red in H.  The right thing is a new
entry-scoped token in `stage_tokens.py` -- "not fired by owner roster <date>" -- that `is_answer` treats as a non-answer, the
renderer as a record, and H as roster-excused: an owner decision, since it changes what every future stage may claim.  Name it as
the mechanism inside `dashmissingd`'s rule question; do not build it here.  Preserve Astra's distinction in the prose: nine
recorded seats, four actual reviews.

## 6. Which accepted dispositions are wrong?  16 of 16 checked

Nine hold as written (J2, J3, J4, J5, J6, J8, J10, J12, J16).  Six are INCOMPLETE -- the verb is right, the pin has an open edge:
**J1** (R1e asserts the record substring, not the whole tooltip: `r_tipnorecord`), **J7** (two sibling title lines), **J9** (the
padded glyph pinned on the renderer only; C24 confounded), **J11** (the glyph set pinned by the first literal line), **J13** (the
baseline number pinned only where it coincides with the within-count), **J14** (the whitespace set pinned only by R3's presence
pin).  One carries a WRONG SENTENCE with a right disposition: **J15**.  J1's "32" and J2's shape fix I re-measured and they hold.

## The 18 changes, so the next pass can be narrow

Controls / CONTRACT (each new row measured green on v4 and red on its mutant; each mutant added to `run_mutants_v4.py`):
1. C27 requires exactly ONE module-level assignment of `DOMAIN` and of `D_CLASS` (an `ast` walk; the checker is import-safe, the
   renderer is not) beside the literal check -- `d_domredef`, `r_dclassredef`.
2. a checker-side padded-glyph row: a new answer dated before the cutoff with d ` ✓` -> rc 1 -- `d_dompad`.
3. the FIXTURE page's strip asserted against the fixture's own counts (its ` ✓` entry counted legacy) -- `r_sumstrip`.
4. C25 at the LEADING end of each of the six fields, and the row id with a trailing space (C25l) -- `d_rowstrip`, `d_datelstrip`,
   `d_dlstrip` and the seat/phase/note siblings; the disclosure sentence corrected until then.
5. the refusal line's content: C3 asserts "dated on or after the cutoff"; C9 asserts "beyond the frozen ceiling" and the entry's
   row, phase, seat, date and d in its OFF-DOMAIN line -- `d_cutreason`, `d_ceilreason`, `d_rowphaseswap`.
6. C12-on asserts "(baseline 1357)" beside "1356 within" -- `d_basewithin`.
7. a C12 row with a MATCHED identity dated `2026-10-17T12:00:00` -> rc 1 -- `d_isodollar`.
8. four override-baseline rows (8 fields; a boolean count; a negative count; a non-string sha -> rc 2), or DISCLOSE them beside
   `k[6] > 0` with the md5-pin reason -- `d_len7ge`, `d_boolcount`, `d_negcount`, `d_str5`.
9. R1e asserts the WHOLE tooltip exactly, as R1f does -- `r_tipnorecord`.
10. a fixture entry with `"d": null` in R1g's want list (class legacy, glyph `None`, the class line) -- `r_tipnotnull`, `r_nullpend`.
11. R2 asserts the strip's labels (the whole strip string's shape) -- `r_striplabel`.
12. W7: a stub checker exiting with an unexpected status (7) -> BAD "could not run (rc 7)" -- `w_elif2`.
13. C24 isolated in a ledger holding only its entry; `d_isosearch`, `d_nostr`, `d_hintundated`, `d_datenone`, `d_cutoffmsg`
    recorded as equivalent escapes, `r_recheld` as outside the diff, `r_wsset` as presence-pinned (one NBSP-only fixture `d` for
    R1d is cheap); the CSS disclosed or presence-pinned.
Records:
14. the two title lines (precommit :496, checker :2).
15. 5d's "exactly C15/C16".
16. "miss the baseline everywhere" -> the three measured fractions (runner comment, J15, 5d).
17. 5c: "5,150 at e483d931" (5,167 at c64445fa).
18. the 158/127/71 count: its deriver named, or marked unreproduced; and the "names each decision's pinned edges" sentences
    written only after the rows above land.

What I could not check: `agent_models.py` for this seat (the main loop's); whether the owner's four-seat roster of 2026-10-16 is
recorded anywhere a tool reads (I found no such record in `stage_tokens.py` or `check_stage_panels.py`); the controls' own code and
`stage_tokens.py` as mutation targets.  Mirror artifacts (session scratchpad, volatile): `ctl_v4_mirror.txt`,
`killtable_v4_mirror.txt`, `extra_mutants.py`, `extra_mutants{,2,3}.out`, `census.py`, `render/out.html`, `render_norec/out.html`
-- copy what a durable record cites into `regress/artifacts/dashokclass_20261016/v4pass/` before the record is written.
