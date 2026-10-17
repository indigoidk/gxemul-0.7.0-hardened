# `dashokclass` (2026-10-17): the dashboard's LEGACY class and the entry-domain check -- every explicit `d` outside ✓ ✕ ⏸ … on the answer a cell shows renders as one class, "legacy -- verdict unclassified", instead of a seat failure (670 displayed cells at HEAD 8bf8b5a1), and precommit section Q2 holds the off-domain answers to a ceiling frozen at landing

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F2, upholding `packet_C_records.md` F2): no `OK` -> approval mapping, every mechanical sweep withdrawn, the class keyed on
the DOMAIN of `d` rather than on one spelling, and Astra's four completeness conditions for the forward check.

* `tools/pipeline/gen_dashboard.py`: an explicit `d` the four-glyph map does not know, on the ANSWER a cell shows, renders as
  class `legacy` (a live hold and a non-answer record keep their own rendering) -- its text kept, `?` for an explicit blank
  or a whitespace-only `d`, and a tooltip that opens (after a refused exemption's line, if any) with "legacy -- verdict
  unclassified: d = ... is outside ✓ ✕ ⏸ …; read the note for the outcome", because some legacy notes record real seat
  failures; the strip counts the class as a fifth number, so it sums to the entry total; the legend says what the class is.
  A MISSING `d` is unchanged -- it still renders `…` (filed as `dashmissingd`).
* `tools/pipeline/check_entry_domain.py` and `entry_domain_baseline.json`, precommit section **Q2** (HARD): an ANSWER whose
  explicit `d` is outside the four passes only while, for its (row, phase, seat, date, `d`, sha1 of its note), the ledger
  holds no more such answers than the baseline froze at landing (1,342 keys, 1,356 answers), and only if it is dated
  before 2026-10-17.  **The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities
  cannot exceed their landing baseline** -- unmatched content or an excess occurrence fails; a byte-identical revert, a
  replacement differing only outside the six fields, and an edit outside them (`ev`, `grade`, `b`) pass.  Editing a frozen
  entry's note means classifying it; that toll is this check's, not the ruling's.  Every container level of the ledger and
  the baseline is type-checked before it is walked; the baseline is md5-pinned with CRLF folded (this machine's system git
  sets `core.autocrlf=true`; a fresh clone measured 89d1d370 for the committed 06a3ffc6); Q2 strips exported
  `GXDOMAIN_BASELINE` and `GXLEDGER`, and reds on ANY status but 0 and 1; a misshapen or unreadable ledger or baseline is rc
  2, never green.
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v7.py`, 123 rows, its docstring the CONTRACT: each decision
  of the checker, the renderer change and Q2 with its GENERATING SET -- every operand position, both ends of each field,
  both directions of the year's and the month's widths (the day's wider one is equivalent) and both separators of the ISO
  shape, each optional tooltip field alone and all three together on a legacy cell and every field clear or all set on
  ok, bad and hold cells, every `str.isspace()` code point, a list row and a list entry, a row with no id -- and its
  COMPLEMENT (only legacy cells carry the class line; the set where it is used), each member rowed or disclosed with its
  reason.  C27 reads the glyph sets by their EFFECT: both files run as `__main__` on a fixture and their sets are read from
  the globals after the run, which sees every rebinding whose effect survives the run (one made and undone inside it is
  not seen -- GPT-6 Astra, v7 pass, measured); the ast walk refuses each named binding form (a banned builtin called by
  name or attribute, or referenced uncalled by name; a mapping-pattern rest; a store into a frame's globals), a
  non-literal binding rather than crashing on it, and counts each use.  123/123 on the staged files, installed byte for byte
  (`RECEIPT_v7_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v7.py`: 181/181 as recorded
  (`KILLTABLE_v7_staged.txt`) -- 179 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356 off-domain
  answers has an empty note, and no note anywhere is the string "None") and `d_isosearch` (the pattern is `^`-anchored)
  equivalent escapes; `d_nonote2` and `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms) -- `d_nonote2`
  killed by C15 and C16 among others, `d_dfold2` by C25d (Grok 4.7, v6 pass: the v6 text read as if both died on all three).  The note-type scope is disclosed: a list or dict note holding a non-answer token as an element or a
  key is a non-answer and is skipped, as the renderer shows it (GPT-6 Astra, v5 pass, measured).  A fold of `d`, or a
  fold or strip of the note, is one-sided on this ledger and dies on C1: some frozen keys stop matching (the d fold changes
  1,100 of the 1,356 frozen answers' keys, the note strip 2, the note fold 1,352 -- Fable 5.1, v4 pass).  The v1-v4 runners
  and receipts are kept; `run_mutants.py` names `run_controls_v2.py` (it named the v1 suite, which crashes on the 7-field
  baseline, so its 14/14 had reproduced only in a staging copy -- Fable 5.1, GPT-6 Astra).
* Records: `dashokclass` closed (witness `harness:`, its REGRESS review HELD for the flagship); `dashmissingd` (LOW) filed --
  814 of 2,953 displayed answer cells show `…` because their latest answer has no `d` (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`),
  its rule question entangled with section H's seat count: the census's NOT-FIRED screen (`/not[ -]fired|roster/i`) finds
  222 entries, 200 untokened, 87 with no `d` (the v3 pass's "158 / 127 / 71" came from an unrecorded screen and could not be
  reproduced); RULINGS_C's "Astra's wording" corrected to "adapted from", and its "5,150 at HEAD" dated to e483d931.

**Pass 2** (`pass2/`, on v1): Astra SWC 3, GLM SWC 4, Fable SWC 7, Grok SWC 3 -- the count key's refill, the tooltip's
denial, the baseline guard, the unpinned cutoff, the cp1252 traceback, the honoured override.  **Adjudication pass** (`f2/`,
on v2, every finding shared with every seat): all four SWC 3 -- the "identity" is a ceiling (Astra), one-edit survivors
(Astra, GLM, Fable, Grok), v2's runner naming the wrong controls (Fable, Astra), the CRLF pin (Grok; measured), the
note-only toll credited to the ruling (Grok); Fable 5.1 withdrew its own pass-2 "note out of the key".  **V3 pass**
(`v3pass/`): all four SWC 3 -- every seat found one-edit survivors of the 46, so v4 was the class closure.  **V4 pass**
(`v4pass/`): Fable SWC 18, Astra SWC 4, Grok SWC 6, GLM SWC 4 -- 21 one-edit mutants passed all 72 v4 controls, 15 at
decisions v4 listed as pinned, one shape: each pin tested ONE edge of its decision (Fable 5.1); the not-fired entries stay
untokened on this landing, all four agreeing (Astra withdrew its NOTSEAT advice after measuring section H: 9/9 untokened,
4/9 tokened), the rule question carried by `dashmissingd`.  **V5 pass** (`v5pass/`): Fable SWC 10, Astra SWC 10, GLM SWC 3,
Grok SWC 12 -- no floor breach and no misattributed kill (Fable 5.1, measuring in a mirror, both v5 receipts reproduced
byte for byte), and the next layer on two axes: a pin covered PART of its decision's generating set (Astra: ten survivors
measured, among them `globals()` and a dict mutation changing the glyph sets past C27; Grok: eleven traced, three of them
past every v6 row then drafted -- the newline and NBSP cells' tooltips, Q2's `else` at 251 of its 254 statuses, the named
entry by a prefix) and a pin on the SELECTED set said nothing about its complement (Fable: sixteen escapes, among them the
class line on 833 pend cells); GLM named the `entries` default, the note's UTF-8 and the None phase/seat; Astra and Grok
both found K19's "nothing is skipped" false; a renderer crashing on the shipped ledger was scored INCOMPLETE, not killed,
until R2's census was guarded.  All rowed or disclosed in v6 -- W9 EXHAUSTS Q2's else partition (254 statuses), R1w the
whitespace set (29 code points).  **V6 pass** (`v6pass/`): Fable SWC 8 (its seat refused twice and claude-opus-4-8
ran 12 turns of its sweep; resumed, Fable 5.1 wrote the answer), Astra SWC 6, Grok SWC 7, GLM SWC 4 -- C27's universal
false at the renderer and in the main block (all four), a non-literal binding crashing the walk (three), and members
still open: list rows and entries, the widths' other directions, single optional fields, the non-legacy optional-field
cell (graded clause (d) by Fable 5.1, (e) by GPT-6 Astra; rowed either way), every style block, the counter keys, a
numeric d, a row with no id; eight records sentences.  All rowed in v7, which reads the glyph sets by their effect.
**V7 pass** (`v7pass/`): Astra SWC 4, Grok CLOSE, GLM CLOSE -- zero floor breaches on each
denominator; Fable SEAT FAILURE (walled on a usage limit at 09:13, its third wall that morning; its stage HELD by owner
ruling 2026-10-17).  D1 ruled apparatus by all three (Grok withdrew its v6 clause-(c) grade); D2 clause (e) by Astra and
Grok -- the body tests `cls == LEGACY`, not pend against ok, and R1p2 rows the cell either way -- with GLM for Fable's
(d) retrospectively, Fable's own side held.  Four records sentences corrected in place (C27's closure: the effective
read sees what SURVIVES the run; R5's scope; the list-`d` barrier is section Q, not Q2; the widths and the optional
fields), W20's labels bumped, and the escapes measured past the 123 FILED as `dashokcov`: a transient glyph-set rebind
(Astra, measured; Grok, traced), R5's upper-case tag and non-hex escape, three optional-field guards, the refusal-line
order, an empty optional field, three fail-safe apparatus gaps, and an inherited list-`d` renderer crash that
precommit Q guards.  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.
