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
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v5.py`, 96 rows, its docstring the CONTRACT: each decision
  of the checker, the renderer change and Q2, with the rows standing on BOTH edges of it -- v5 rows the dual edge of every
  pin, the edit an earlier pin would not see -- and what is disclosed with its reason.  96/96 on the staged files, installed
  byte for byte (`RECEIPT_v5_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v5.py`: 105/105 as
  recorded (`KILLTABLE_v5_staged.txt`) -- 103 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356
  off-domain answers has an empty note) and `d_isosearch` (the pattern is `^`-anchored) equivalent escapes; `d_nonote2` and
  `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms), killed by C15/C16 and by C25d.  A fold of `d`, or a
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
4/9 tokened), the rule question carried by `dashmissingd`.  **V5 pass** (`v5pass/`): [to be written from its answers].
Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.
