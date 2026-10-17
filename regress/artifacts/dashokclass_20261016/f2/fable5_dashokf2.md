FABLE_DASHOKF2_20261016
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES (3) -- v2 implements every ruled property and I reproduce both receipts byte-for-byte (35/35, 14/14 killed as named, same red sets) from the staged files plus HEAD's ledger; the note-in-key repair is the right fix and my own pass-2 "note out of the key: right" was wrong; but (1) the kill table as STAGED cannot be reproduced by the driver it names -- `run_mutants.py` calls `run_controls.py`, which in the artifact dir is the 19-control v1, and that pair crashes on the 7-field baseline (measured: `ValueError: too many values to unpack (expected 6)`, then `APPARATUS FAIL: the base run is not clean`); (2) three accepted dispositions are pinned only in half -- six one-edit mutants pass all 35 and four of them break a claim the packet makes about v2 (the tooltip's tail, the malformed-date reason, which Q2 branch fired); (3) three sentences still overclaim (the renderer comment's "reason first", the docstring's "can only shrink", the docstring's single exit).

Seat: Fable 5.1 (file-reading, measuring).  Everything marked MEASURED ran in a temp mirror OUTSIDE the project
(`scratchpad/dashokf2/mirror`: the repo's `stage_tokens.py`, the four staged_v2 files, `git show HEAD:tools/pipeline/ledger.json`
with HEAD = 8bf8b5a1, `run_controls_v2.py` copied in AS `run_controls.py` beside `run_mutants.py`, `gen_dashboard_before.py` and
`write_baseline.py`).  Nothing under the project was written except this file.  The receipt header's three md5 prefixes
(`111bcac0 | 2565a4a0 | a96dad35`) are the staged_v2 checker, renderer and precommit exactly, so section 5 is of the files in
section 4.  Roster note: when I wrote this, `f2/codex_dashokf2.txt` and `f2/grok_dashokf2.txt` were 0 bytes (codex's `.err` is
35 KB, grok's is empty) -- I did not wait and did not read them.

## 1. My own findings -- disposition and FIX, each

| # | disposition right? | fix right? | measured |
|---|---|---|---|
| D1 tooltip/legend | yes | **yes, and better than my wording**: Astra's "outside ... read the note for the outcome" asserts nothing about what the class "counts as", which mine still did.  Every legacy cell HAS a note to read (0 of the 1,356 off-domain answers carry an empty/missing note).  Half-pinned: R1 asserts the prefix up to `is outside`; `x_tip_tail` (the tail deleted) passes 35/35 | yes |
| D2 refill (count key) | yes | **yes -- and my pass-2 "Note out of the key: right" was WRONG on the fix.**  124 of the 1,136 (row, phase, seat, date, d) tuples hold entries distinguishable ONLY by their note; a count key conflated all of them and freed a refillable slot on every conversion.  C15 reds the refill; C16 reds the note edit.  See section 4 | yes |
| D3 legitimate correction fails | yes, accepted as designed | yes; v2 widens it to note edits and says so (docstring + Q2 message) | -- |
| D5 baseline guard | yes | **the md5 pin is the right fix and my `cmp`-against-HEAD was inferior**: it would refuse every reviewed re-freeze for ever, and carries the same exposure.  See section 5 | C18 reproduces |
| D8 inclusive boundary unpinned | yes | yes: C12 before/on/after with the fixture identity FROZEN isolates the date test; `d_cutoff18` and my `x_cut_gt` (`>=` -> `>`) are each killed by C12 ALONE -- the named reason | yes |
| D9 lexical dates / TypeError | yes | yes for rc: C19a/C19b rc 1, no traceback.  **The "named in the reason" half is unpinned**: `x_lexdate` (v1's `if t[3] >= CUTOFF:`) passes 35/35 while reporting a numeric date and `2026-9-9` as "dated on or after the cutoff"; v2 names "its date is not ISO" for all three malformed forms I tried | yes |
| D10 explicit blank | yes | yes; C14 is the named kill of `d_blank` (C1 and C11 also red because 23 blank-d answers leave the population and the frozen count no longer matches) | yes |
| D11 control gaps | yes | yes, verified in the v2 source: C1 `"%d frozen" % N_OFF` with N_OFF re-derived, C2b, C11 `nb == N_OFF`, R1 kimi -> `tok`/`∅` plus the tip, R2 `sum == total == n_entries` and `legacy == n_legacy` (1,397 incl. non-answers), R3 `h is not None`, W1-W4 a counted `fails`.  **"ALL FIXED" overstates one thing I myself called not worth a control in pass 2**: which Q2 branch fired is unpinned -- `x_pre_rc7` (`-eq 1` -> `-eq 7`) and `x_w2msg` (`bad "x"`) pass 35/35, W2/W3 only test the `BAD ` prefix and the counter | yes |
| D12 cp1252 | yes | yes; `reconfigure(errors="backslashreplace")`, C20 pins it, `d_noreconf` reds nine rows | yes |
| D14, D15 | corrected | the 5,177 / `2042…` / hold 53 / none 29472 census is what my mirror renders from HEAD's ledger | yes |
| D16 regenerate matrix.html | in plan | not mine to run.  What I did check: the WORKING-TREE ledger (29 lines changed since HEAD: state notes, a HELD entry re-dated, two rows reordered) passes the v2 checker with the pinned baseline, rc 0, 1356/1356 -- so Q2 is green at landing whichever ledger the commit carries | yes |
| D17 "only shrink" | corrected | one residual: the docstring still says "The grandfathered population can only shrink".  It can never EXCEED the frozen set, but a deleted frozen entry can be restored, and the six byte-identical identities can be re-added up to their frozen count -- "never exceeds the frozen set" is the exact sentence | reasoned |
| D19 five `✗` | noted | right; no sweep | -- |
| D20 refusal line first | kept, agreed | **the renderer comment at the `D_CLASS` block still says "with the reason first in its tooltip"**: on a refused-exemption cell the refusal is inserted at 0 AFTER the legacy line, so the comment is false exactly where D20 applies.  One clause: "first (after a refused exemption's line, if any)" | read |

## 2. The repair as material -- a path where v2 does wrong what v1 did right

**None that breaks a ruled property; one class v2 refuses that v1 passed, and it is the one section 3 names.**  Walked field by
field: row / phase / seat / date / `d` edits fail under both; `ev`, `b`, `grade` and any unkeyed field pass under both; a note
edit (including moving note text into `ev`) fails under v2 only.  The exits the checker's own hint line names -- give it a
glyph, omit `d`, or mark it a non-answer record (NOTSEAT / NOPANEL / ANNOTATION take it out of the population under both) -- are
all available; **the docstring names only the first** ("editing such an entry means giving it a glyph"), which is narrower than
the hint two lines below it.

Two things worth saying plainly about that class:
* **A whole-ledger rewrite that normalises note whitespace would red 1,356 entries at once.**  That is a mechanical sweep, and
  refusing it is what the ruling asked for.  JSON re-serialisation (indent, key order, CRLF/LF of the file) does not touch note
  VALUES, so the ledger's own CRLF-on-disk practice is unaffected -- MEASURED by the working-tree run above.
* **The defang case is Q2 catching the carrier's own named failure, not new friction.**  A hold entry whose marker is defanged
  stops being `is_held`, becomes an answer with a blank or `HELD` `d`, and is refused -- which is precisely "defanging
  MANUFACTURES a seat answer that never happened" from the carrier's 08-30 correction.  NOTSEAT or a glyph is the right
  edit; both pass.

**Entries the identity key cannot tell apart**: exactly the byte-identical ones.  MEASURED on HEAD: 1,356 answers in 1,342
identities; six identities with multiplicity > 1 -- `pcc2widthkills`/review/agy/2026-09-03/`N/A` x5,
`crimewidthkill`/review/agy/2026-09-13/`NOT-FIRED` x5, `mapledmaaddr`/review/agy/2026-09-12/`NOT-FIRED` x4,
`sgideprimop`/review/agy/2026-09-03/`N/A` x2, `pcc2defaultkill`/review/agy/2026-09-05/`N/A` x2,
`alphaswpctxreg`/review/grok/2026-09-08/`y` x2.  A "refill" of one of those yields a copy a reader cannot tell apart either, so
nothing new enters.  The other blind spot is by construction: a refill that reuses all six keyed fields with a different `ev`
passes -- same verdict text, same note, a different evidence pointer.  Disclose it; no row.

Dates: `date_str` + the ISO-prefix rule behave as the docstring says for every form I tried (`10/18/2026`, numeric, `2026-9-9`
-> "not ISO"; `2026-10-17T09:00` -> "on or after the cutoff"); a syntactically-ISO nonsense date (`2026-13-45`) is refused with the
cutoff reason, which is a wrong reason on an entry that fails anyway -- nit.

## 3. The kill table

**Reproduced exactly** (MEASURED, my mirror): BASE 35/35; the same fourteen scores and the same red sets line for line; 14/14
killed as named.  Every named kill is for the named reason -- `d_cutoff18` and `d_nodate` red only C12's on/after rows;
`d_nomd5` only C18; `r_nolegend` only R4; `r_strip` only R2; `w_envkeep` only W4; `w_collapse` only W3.  Two honest notes:
* `d_nonote` is killed by C1 because a checker without the note cannot MATCH a baseline that carries note shas -- it pins the
  format coupling, not the comparison.  The comparison is pinned by C15/C16, which is the pair that would kill the two-edit
  form (note dropped on both sides); the one-edit form cannot exist.  Fine, say so in the table's comment.
* `r_ok`/`r_pend`/`r_noescape` additionally red R3 only because R3's own find-text is gone from the mutant -- a presence pin,
  not a second behavioural kill.

**One-edit mutants NOT in the table, run through the 35 (MEASURED):**

```
x_domain_nohold    25/35   red: C1 C10 C11 C12 C18 C2 C2b C7 C8 W1   (DOMAIN minus ⏸)
x_domain_nopend    25/35   red: same                                (DOMAIN minus …)
x_dup_plus1        24/35   red: C11 C14 C15 C16 C19a C19b C5 C6 C9 W2 W4
x_cut_gt           34/35   red: C12                                  (>= -> >)
x_pin_notdefault   30/35   red: C11 C12 C18                          (pin only on the override path)
x_ws_blank         34/35   red: R3 ONLY -- a presence pin             ({e(d) if d else "?"})
x_pre_rc7          35/35   PASSES ALL   (elif -eq 1 -> -eq 7)
x_w2msg            35/35   PASSES ALL   (W2's bad message -> "x")
x_lexdate          35/35   PASSES ALL   (v1's `if t[3] >= CUTOFF:`)
x_noreason         35/35   PASSES ALL   ("its date is not ISO" suffix deleted)
x_tip_tail         35/35   PASSES ALL   ("; read the note for the outcome" deleted)
x_note_none        35/35   PASSES ALL   (equivalent: 0 off-domain answers have an empty note)
```

**No escape breaks a RULED property** (one residue class, text kept, hold/record precedence, five-number strip, the four
completeness conditions, identity grandfathering, hard Q2).  Four break a claim the PACKET makes about v2, and each is one
assertion away: R1 asserts the whole tooltip line (D1); C19a/C19b assert `not ISO` in the output (D9); W2 asserts `not a
frozen legacy entry` and W3 `could not run` in their first line (D11).  Two are disclosed only: ⏸ and … are positive-pinned
only INCIDENTALLY -- the shipped ledger carries 21 ⏸ and 35 … explicit-d answers, so dropping either from DOMAIN reds C1;
a positive row per glyph (two rows) would make that direct.  A whitespace-only `d` renders invisible under `x_ws_blank`
(0 such values in the ledger; R1's fixture row has all nine seats, so a second row like `ctlesc` would carry it).

## 4. The note in the key -- KEEP IT

Ruling on my own pass-2 position, harder than on anyone else's: **I was wrong.**  The argument I gave ("a correction or a
defanged marker must not re-arm an entry") proves too little, because the alternative is measured to admit new content.  Three
measured facts settle it: (i) under a count key the refill is rc 0 (Astra and I both ran it); (ii) 124 of 1,136 tuples hold
entries that differ only in their note, so the count key could not tell 11 % of the population apart; (iii) **a comparison
against HEAD's ledger has the same hole** -- "convert X, add Y with X's tuple" leaves the per-tuple count unchanged, so only
identity closes it, and identity without the note is the count key again.  The price is the right price under the ruling:
"an OK becomes ✓ or anything else only when a reader rewrites that one entry" -- a reader editing a note has read the entry,
and that is the moment the ruling says classification happens.  If the owner wants note-only corrections free, the only
honest form is a second, reviewed re-freeze (the md5 pin makes it a two-file diff), not a weaker key.

## 5. The baseline guard -- the md5 pin

Of the three: the pinned total is weakest (a one-for-one identity swap keeps 1,356 and launders the new one); my `cmp` against
`HEAD:` detects every change but refuses every reviewed re-freeze for ever and shares the pin's one exposure; the md5 pin
detects every change AND lets a re-freeze land as a visible two-file diff, with the writer refusing to overwrite without
`--force`.  Say the true thing about it: the pin makes a re-freeze VISIBLE, "reviewed" is a practice.  The one exposure, for
the record: the pin is a hash of bytes, so a checkout that converts the file's line endings would red Q2 with rc 2 on every
commit -- `core.autocrlf` is `false` here and there is no `.gitattributes`, so it is not live; a `text eol=lf` attribute on the
baseline would make it moot.

## 6. Which accepted dispositions are wrong -- 20 of 20 checked (D1-D20), plus one defect outside the twenty

Wrong outright: **none**.  Half-right / overstated, 4: **D9** (the reason half unpinned), **D11** ("ALL FIXED" -- the branch
attribution is unpinned, consistent with my own pass-2 call that it was not worth a control, so overstated rather than
wrong), **D17** (the residual "can only shrink"), **D20** (kept, but the renderer comment still says "reason first").  Holds,
16: D1-D8, D10, D12-D16, D18 (settled by reading `cell()`: the live-hold return, the unparseable-hold return and the `tok`
return all precede `tip`), D19.

**Outside the twenty, and it is the change I would hold the landing for: the kill table is not reproducible from the staged
artifact set as named.**  `run_mutants.py` runs `os.path.join(HERE, "run_controls.py")`; in `regress/artifacts/dashokclass_20261016/`
that file is the v1 suite (12,529 bytes, "Controls for `dashokclass` (2026-10-16): ..."), and MEASURED against the staged_v2
checker and baseline it dies on the 7-field rows (`ValueError: too many values to unpack (expected 6)`), after which
`run_mutants.py` prints `BASE NO TALLY` / `APPARATUS FAIL: the base run is not clean` and exits 9.  The 14/14 was produced in a
staging copy where v2 sat under v1's name.  That is the score-claim-names-its-artifact class: the named artifact does not
produce the number.  Land `run_controls_v2.py` AS `run_controls.py` and keep v1 as `run_controls_v1.py` (the writer's own
`write_baseline_v1.py` precedent), or point `run_mutants.py` at the v2 name -- then re-run both receipts from the landed names.

## The three changes

1. **Reproducibility (records, must):** `run_controls.py` = v2 in the committed artifact dir (v1 kept under `_v1`), receipts re-run
   from the landed names.
2. **Pin the unpinned halves (L1, three one-line assertions):** R1 the whole legacy tooltip line; C19a/C19b `not ISO` in the
   output; W2/W3 their first-line message text.  Optional, disclosed otherwise: a `d: " "` fixture; positive rows for ⏸ and ….
3. **Three sentences (L4):** the renderer comment's "reason first" -> "first, after a refused exemption's line if any"; the
   docstring's "can only shrink" -> "never exceeds the frozen set"; the docstring's single exit -> the three the hint names.

## What I could not check

* The other seats' F2 answers (0 bytes when I looked).
* The landing's section Q (matrix.html regeneration) -- not simulated; only Q2 on the working-tree ledger was run.
* `write_baseline.py --force` was not re-run; the staged baseline's md5 equals the pinned constant and `baseline_write.out`
  (1,356 entries in 1,342 identities) matches my own identity count, which is what I relied on instead.

Durable artifacts: none written (the task allowed one file).  Every number above re-derives in under five minutes from the
staged_v2 files, `tools/pipeline/stage_tokens.py`, `git show 8bf8b5a1:tools/pipeline/ledger.json`, and `run_controls_v2.py`
copied in as `run_controls.py` beside `run_mutants.py`; the extra mutants are twelve `str.replace` edits of the find-texts
quoted in section 3, each run through that suite with the matching `CTL_*` override.
