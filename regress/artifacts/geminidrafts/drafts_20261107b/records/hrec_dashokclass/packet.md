# Reading task: hrec_dashokclass (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBHRECDASHOKCLASS-a479` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one held harness row, `dashokclass` (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator; this fork keeps a
ledger of every filed issue, and a HARNESS row is about the project's own test tooling.  The row below is HELD with its
fix committed; its record is the commit message(s) and any CHANGELOG block shown.  A flagship review is still owed.  You
cannot read files, so judge the record AS WRITTEN.  Do not simply ratify it.  A bracketed dated note is this project's
in-place correction form (it quotes what it corrects); it is not by itself a contradiction.

## The ledger row `dashokclass` (state `held`)

**title:** tools/pipeline/gen_dashboard.py renders every ledger entry whose `d` is "OK" in the seat-failure class: D_CLASS maps only the four glyphs, so all 365 OK cells in matrix.html carry class pend

**state_note (head):** [2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-17 (dd2d4e01, and its hash-follow 98a95899) while its review stage (the V7 pass of the landing) held a Fable wall written as untokened prose; that entry now carries the HELD token and the row is held until Fable answers -- the question is in hold_question.  Rulings and commits proceed meanwhile (the owner's 2026-10-17 directive); the close does not.  ||  filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, "pend")`; HEAD's ledger carries 439 entries with d "OK" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS ("OK": "ok") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d "OK".  LOW, display only.

[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line "OK": "ok", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class (a live hold and a non-answer record keep their own rendering), its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at 

**hold_question:** REVIEW (held 2026-10-18 by fableheldform; Fable walled on V7, 2026-10-17): regress/artifacts/dashokclass_20261016/v7pass/packet_dashok_v7_FABLE.md -- does the landing (dd2d4e01) stand?  ||  REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v7_on_staged_v5.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 123/123 -- in particular R2 (only pend -> legacy, 670 cells, the strip string exact), R2b (the fixture strip by exact membership), C15/C16 (the note in the key), C25a-r (each key field byte for byte, at both ends), C17b-n (the baseline row's every clause and every string position), C18/C18b (the md5 pin, CRLF folded), C21a-m (a misshapen ledger or basel

## The record -- commit message(s)

### commit `dd2d4e01 2026-10-17`

```text
dashokclass: the dashboard's LEGACY class and precommit Q2's entry-domain ceiling land -- 670 displayed cells leave the seat-failure glyph, off-domain answers are held to their landing baseline; controls 123/123, kill table 181/181; dashmissingd and dashokcov filed

Ruled before any code by Fable 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md F2):
no OK -> approval mapping, no sweep, the class keyed on the DOMAIN of d.

tools/pipeline/gen_dashboard.py: an explicit d outside the four glyphs, on the ANSWER a cell shows, renders as class
`legacy' -- its text kept, `?' for a blank or whitespace-only d, a tooltip opening "legacy -- verdict unclassified" --
and the strip counts it as a fifth number; a live hold and a non-answer record keep their own rendering, and a MISSING
d is unchanged.  tools/pipeline/check_entry_domain.py + entry_domain_baseline.json (md5-pinned, CRLF folded), wired as
precommit section Q2 (HARD) in tools/precommit_check.sh: per (row, phase, seat, date, d, note sha1), no more off-domain
answers than the baseline froze (1,342 keys, 1,356 answers); every status but 0 and 1 is BAD.  matrix.html re-rendered by
the new renderer; fable_queue.md's generated block names the row's held REGRESS review.

Controls regress/artifacts/dashokclass_20261016/run_controls_v7.py: 123/123 on the staged files (RECEIPT_v7_on_staged_v5.txt);
kill table run_mutants_v7.py 181/181 as recorded, two escapes recorded as equivalent (KILLTABLE_v7_staged.txt).  The receipt
and table the v7 pass reviewed (controls md5 836927f0) are kept beside them; the committed controls differ from it by
comments and one printed label only (AST-identical otherwise).

Seven passes on the staged files -- pass 2, the adjudication pass, v3 to v7 -- on the owner's four-seat roster.  V7 (the
closing pass, findings shared): GPT-6 Astra SHIP WITH CHANGES (4), Grok 4.7 CLOSE, GLM 5.3 CLOSE -- zero floor breaches on
each denominator.  Fable 5.1 walled on a usage limit (its third wall that morning): a SEAT FAILURE, and its stage -- with
its side of D2 -- HELD by owner ruling 2026-10-17 ("hold any fable adjucation"), the question in the row's hold_question.
The pass's four wrong records are corrected in place (C27 sees a rebinding that SURVIVES the run, not "whatever its
syntax"; R5 reads lower-case style tags and hex escapes; a list d's barrier is section Q, not Q2; the widths and the
optional fields), and what it measured past the 123 controls is FILED as dashokcov (LOW, clause (e)): a transient
glyph-set rebind, R5's tag case and non-hex escapes, three optional-field guards, the refusal-line order, an empty field,
three fail-safe apparatus gaps, and an inherited list-d renderer crash that section Q guards.  dashmissingd (LOW) filed:
814 displayed cells show the `…' glyph because their latest answer has no d -- a rule question entangled with section H.

tools/pipeline/check_probe_wiring.py: its MANIFEST classifies the round's 29 preserved .py artifacts (precommit R
refused the first attempt without them) -- controls, staged copies, the before-renderer and two censuses RESEARCH;
the kill-table drivers, baseline writers and the Fable seat's extra mutants TOOL; none is a gated detector.  R passes
on the unit (74/84 gated, 10 dated-exempt) and its selftest 22/22.

Records: dashokclass CLOSED (witness harness:RECEIPT_v7_on_staged_v5.txt), its REGRESS review HELD for the flagship;
OUTSTANDING_BUGS.md's entry and its 2026-10-09 state note corrected by content; RULINGS_C_records.md's attribution and
strip count corrected in place.  This commit's own hash follows in the next records commit.  Opus, agy, kimi, deepseek
and minimax not fired, by the owner's roster.  No src/ touched.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## The record -- CHANGELOG block(s)

### CHANGELOG.md lines 3646-3653 (HEAD 8d9df658)

```text
 3646| # Records, 2026-10-17: `dashokclass` names its closing commit dd2d4e01
 3647| 
 3648| The landing commit dd2d4e01 closed the row(s) and cannot name itself; this adds it to each `commits` field: `dashokclass` (now `dd2d4e01`); `dashmissingd` (open, filed by it; now `dd2d4e01`); `dashokcov` (open, filed by it; now `dd2d4e01`).
 3649| check_commit_attribution grades a closed row whose subject-naming commit is unlisted HARD on the next commit, the
 3650| peer session's included, so this lands at once and alone.  It also FILED `dashmissingd` and `dashokcov`, which its subject names; check_commit_attribution grades a code commit naming an open row
 3651| whose `commits` is EMPTY as HARD (the field is not closure-only), so each lists the commit that filed it.
 3652| Ledger, matrix and this block only.
 3653| 
```

### CHANGELOG.md lines 3654-3742 (HEAD 8d9df658)

```text
 3654| # `dashokclass` (2026-10-17): the dashboard's LEGACY class and the entry-domain check -- every explicit `d` outside ✓ ✕ ⏸ … on the answer a cell shows renders as one class, "legacy -- verdict unclassified", instead of a seat failure (670 displayed cells at HEAD 8bf8b5a1), and precommit section Q2 holds the off-domain answers to a ceiling frozen at landing
 3655| 
 3656| **Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
 3657| F2, upholding `packet_C_records.md` F2): no `OK` -> approval mapping, every mechanical sweep withdrawn, the class keyed on
 3658| the DOMAIN of `d` rather than on one spelling, and Astra's four completeness conditions for the forward check.
 3659| 
 3660| * `tools/pipeline/gen_dashboard.py`: an explicit `d` the four-glyph map does not know, on the ANSWER a cell shows, renders as
 3661|   class `legacy` (a live hold and a non-answer record keep their own rendering) -- its text kept, `?` for an explicit blank
 3662|   or a whitespace-only `d`, and a tooltip that opens (after a refused exemption's line, if any) with "legacy -- verdict
 3663|   unclassified: d = ... is outside ✓ ✕ ⏸ …; read the note for the outcome", because some legacy notes record real seat
 3664|   failures; the strip counts the class as a fifth number, so it sums to the entry total; the legend says what the class is.
 3665|   A MISSING `d` is unchanged -- it still renders `…` (filed as `dashmissingd`).
 3666| * `tools/pipeline/check_entry_domain.py` and `entry_domain_baseline.json`, precommit section **Q2** (HARD): an ANSWER whose
 3667|   explicit `d` is outside the four passes only while, for its (row, phase, seat, date, `d`, sha1 of its note), the ledger
 3668|   holds no more such answers than the baseline froze at landing (1,342 keys, 1,356 answers), and only if it is dated
 3669|   before 2026-10-17.  **The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities
 3670|   cannot exceed their landing baseline** -- unmatched content or an excess occurrence fails; a byte-identical revert, a
 3671|   replacement differing only outside the six fields, and an edit outside them (`ev`, `grade`, `b`) pass.  Editing a frozen
 3672|   entry's note means classifying it; that toll is this check's, not the ruling's.  Every container level of the ledger and
 3673|   the baseline is type-checked before it is walked; the baseline is md5-pinned with CRLF folded (this machine's system git
 3674|   sets `core.autocrlf=true`; a fresh clone measured 89d1d370 for the committed 06a3ffc6); Q2 strips exported
 3675|   `GXDOMAIN_BASELINE` and `GXLEDGER`, and reds on ANY status but 0 and 1; a misshapen or unreadable ledger or baseline is rc
 3676|   2, never green.
 3677| * Controls `regress/artifacts/dashokclass_20261016/run_controls_v7.py`, 123 rows, its docstring the CONTRACT: each decision
 3678|   of the checker, the renderer change and Q2 with its GENERATING SET -- every operand position, both ends of each field,
 3679|   both directions of the year's and the month's widths (the day's wider one is equivalent) and both separators of the ISO
 3680|   shape, each optional tooltip field alone and all three together on a legacy cell and every field clear or all set on
 3681|   ok, bad and hold cells, every `str.isspace()` code point, a list row and a list entry, a row with no id -- and its
 3682|   COMPLEMENT (only legacy cells carry the class line; the set where it is used), each member rowed or disclosed with its
 3683|   reason.  C27 reads the glyph sets by their EFFECT: both files run as `__main__` on a fixture and their sets are read from
 3684|   the globals after the run, which sees every rebinding whose effect survives the run (one made and undone inside it is
 3685|   not seen -- GPT-6 Astra, v7 pass, measured); the ast walk refuses each named binding form (a banned builtin called by
 3686|   name or attribute, or referenced uncalled by name; a mapping-pattern rest; a store into a frame's globals), a
 3687|   non-literal binding rather than crashing on it, and counts each use.  123/123 on the staged files, installed byte for byte
 3688|   (`RECEIPT_v7_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v7.py`: 181/181 as recorded
 3689|   (`KILLTABLE_v7_staged.txt`) -- 179 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356 off-domain
 3690|   answers has an empty note, and no note anywhere is the string "None") and `d_isosearch` (the pattern is `^`-anchored)
 3691|   equivalent escapes; `d_nonote2` and `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms) -- `d_nonote2`
 3692|   killed by C15 and C16 among others, `d_dfold2` by C25d (Grok 4.7, v6 pass: the v6 text read as if both died on all three).  The note-type scope is disclosed: a list or dict note holding a non-answer token as an element or a
 3693|   key is a non-answer and is skipped, as the renderer shows it (GPT-6 Astra, v5 pass, measured).  A fold of `d`, or a
 3694|   fold or strip of the note, is one-sided on this ledger and dies on C1: some frozen keys stop matching (the d fold changes
 3695|   1,100 of the 1,356 frozen answers' keys, the note strip 2, the note fold 1,352 -- Fable 5.1, v4 pass).  The v1-v4 runners
 3696|   and receipts are kept; `run_mutants.py` names `run_controls_v2.py` (it named the v1 suite, which crashes on the 7-field
 3697|   baseline, so its 14/14 had reproduced only in a staging copy -- Fable 5.1, GPT-6 Astra).
 3698| * Records: `dashokclass` closed (witness `harness:`, its REGRESS review HELD for the flagship); `dashmissingd` (LOW) filed --
 3699|   814 of 2,953 displayed answer cells show `…` because their latest answer has no `d` (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`),
 3700|   its rule question entangled with section H's seat count: the census's NOT-FIRED screen (`/not[ -]fired|roster/i`) finds
 3701|   222 entries, 200 untokened, 87 with no `d` (the v3 pass's "158 / 127 / 71" came from an unrecorded screen and could not be
 3702|   reproduced); RULINGS_C's "Astra's wording" corrected to "adapted from", and its "5,150 at HEAD" dated to e483d931.
 3703| 
 3704| **Pass 2** (`pass2/`, on v1): Astra SWC 3, GLM SWC 4, Fable SWC 7, Grok SWC 3 -- the count key's refill, the tooltip's
 3705| denial, the baseline guard, the unpinned cutoff, the cp1252 traceback, the honoured override.  **Adjudication pass** (`f2/`,
 3706| on v2, every finding shared with every seat): all four SWC 3 -- the "identity" is a ceiling (Astra), one-edit survivors
 3707| (Astra, GLM, Fable, Grok), v2's runner naming the wrong controls (Fable, Astra), the CRLF pin (Grok; measured), the
 3708| note-only toll credited to the ruling (Grok); Fable 5.1 withdrew its own pass-2 "note out of the key".  **V3 pass**
 3709| (`v3pass/`): all four SWC 3 -- every seat found one-edit survivors of the 46, so v4 was the class closure.  **V4 pass**
 3710| (`v4pass/`): Fable SWC 18, Astra SWC 4, Grok SWC 6, GLM SWC 4 -- 21 one-edit mutants passed all 72 v4 controls, 15 at
 3711| decisions v4 listed as pinned, one shape: each pin tested ONE edge of its decision (Fable 5.1); the not-fired entries stay
 3712| untokened on this landing, all four agreeing (Astra withdrew its NOTSEAT advice after measuring section H: 9/9 untokened,
 3713| 4/9 tokened), the rule question carried by `dashmissingd`.  **V5 pass** (`v5pass/`): Fable SWC 10, Astra SWC 10, GLM SWC 3,
 3714| Grok SWC 12 -- no floor breach and no misattributed kill (Fable 5.1, measuring in a mirror, both v5 receipts reproduced
 3715| byte for byte), and the next layer on two axes: a pin covered PART of its decision's generating set (Astra: ten survivors
 3716| measured, among them `globals()` and a dict mutation changing the glyph sets past C27; Grok: eleven traced, three of them
 3717| past every v6 row then drafted -- the newline and NBSP cells' tooltips, Q2's `else` at 251 of its 254 statuses, the named
 3718| entry by a prefix) and a pin on the SELECTED set said nothing about its complement (Fable: sixteen escapes, among them the
 3719| class line on 833 pend cells); GLM named the `entries` default, the note's UTF-8 and the None phase/seat; Astra and Grok
 3720| both found K19's "nothing is skipped" false; a renderer crashing on the shipped ledger was scored INCOMPLETE, not killed,
 3721| until R2's census was guarded.  All rowed or disclosed in v6 -- W9 EXHAUSTS Q2's else partition (254 statuses), R1w the
 3722| whitespace set (29 code points).  **V6 pass** (`v6pass/`): Fable SWC 8 (its seat refused twice and claude-opus-4-8
 3723| ran 12 turns of its sweep; resumed, Fable 5.1 wrote the answer), Astra SWC 6, Grok SWC 7, GLM SWC 4 -- C27's universal
 3724| false at the renderer and in the main block (all four), a non-literal binding crashing the walk (three), and members
 3725| still open: list rows and entries, the widths' other directions, single optional fields, the non-legacy optional-field
 3726| cell (graded clause (d) by Fable 5.1, (e) by GPT-6 Astra; rowed either way), every style block, the counter keys, a
 3727| numeric d, a row with no id; eight records sentences.  All rowed in v7, which reads the glyph sets by their effect.
 3728| **V7 pass** (`v7pass/`): Astra SWC 4, Grok CLOSE, GLM CLOSE -- zero floor breaches on each
 3729| denominator; Fable SEAT FAILURE (walled on a usage limit at 09:13, its third wall that morning; its stage HELD by owner
 3730| ruling 2026-10-17).  D1 ruled apparatus by all three (Grok withdrew its v6 clause-(c) grade); D2 clause (e) by Astra and
 3731| Grok -- the body tests `cls == LEGACY`, not pend against ok, and R1p2 rows the cell either way -- with GLM for Fable's
 3732| (d) retrospectively, Fable's own side held.  Four records sentences corrected in place (C27's closure: the effective
 3733| read sees what SURVIVES the run; R5's scope; the list-`d` barrier is section Q, not Q2; the widths and the optional
 3734| fields), W20's labels bumped, and the escapes measured past the 123 FILED as `dashokcov`: a transient glyph-set rebind
 3735| (Astra, measured; Grok, traced), R5's upper-case tag and non-hex escape, three optional-field guards, the refusal-line
 3736| order, an empty optional field, three fail-safe apparatus gaps, and an inherited list-`d` renderer crash that
 3737| precommit Q guards.  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.
 3738| Section R: `tools/pipeline/check_probe_wiring.py`'s MANIFEST classifies the round's 29 preserved `.py` artifacts --
 3739| the controls, the staged copies, the before-renderer and the two censuses RESEARCH; the kill-table drivers, the
 3740| baseline writers and the Fable seat's extra mutants TOOL.  None is a gated detector: the gated check is
 3741| `tools/pipeline/check_entry_domain.py`, precommit Q2, and `tools/` is outside that MANIFEST's domain.
 3742| 
```

## Questions -- verdict line first

1. Does the record contradict itself -- two numbers for one quantity, a total its parts do not sum to, a claim one
   paragraph makes and another undoes, or the ledger row saying something the commit message does not?  Quote both.
2. Which claims are stated as MEASURED but cite no artifact (a log, a file under regress/artifacts/)?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the record's own evidence covers less?
4. What would a reviewer checking this record against its artifacts most likely find wrong?
When you count items the record enumerates, list them by name before giving the count.

End with one line: `HARNESSREC_DASHOKCLASS: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBHRECDASHOKCLASS: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
