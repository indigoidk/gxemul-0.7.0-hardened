# V3 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v3 after the adjudication pass

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v3 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v3/` (mirroring `tools/`); the controls are `run_controls_v3.py` and
`run_mutants_v3.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming the staged files; the
adjudication-pass answers are in `f2/`.  Everything a packet-fed seat needs is inlined below.

**This is the repair chain's pass on v3.**  It closes on the first pass whose zero floor breaches survive adjudication --
so if you find none, say which cells and mutant shapes you swept.  Review EFFORT is scoped to the v2 -> v3 diff; the FLOOR
question -- a one-edit mutant of the staged checker, renderer or Q2 block that passes all 46 controls and breaks a ruled
property -- is asked of the whole v3 material.  Check the premises in section 2b; do not ratify them.

<TOKEN_LINE>

## 1. The adjudication-pass verdicts (on v2), every finding shared with every seat

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`f2/codex_dashokf2.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`f2/glm_dashokf2.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (3)** (`f2/fable5_dashokf2.md`; agent_models.py: clean claude-fable-5-1).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`f2/grok_dashokf2.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| H1 | Astra | the "identity" key is a COUNT CEILING over selected content: normalise an entry then restore it byte for byte, or replace it with one equal in all six fields and different in `ev`, and the check passes; 1,342 keys cover 1,356 frozen answers | **ACCEPTED as the narrower guarantee**, in Astra's words: *current selected-content multiplicities cannot exceed their landing baseline*.  The docstring and the Q2 comment now say "a ceiling ... not an entry identity", name the three cases that pass, and drop "can only shrink" (the count can climb back to 1,356, and a reviewed re-freeze can raise it).  Persistent entry identity with provenance is NOT built -- see 2b |
| H2 | Astra, GLM, Fable, Grok | one-edit survivors of v2's 35 controls: the tooltip's denial restored after the checked prefix (Astra, GLM, Grok); its tail deleted (Fable); `-u GXLEDGER` deleted from Q2 (Astra); the loader's `+=` made `=` (Astra, GLM, Grok); v1's lexical date compare restored, and the "not ISO" reason deleted (Fable); which Q2 branch fired (`-eq 1` -> `-eq 7`, the message rewritten; Fable); ⏸ and … only incidentally positive; a whitespace-only `d` rendered invisible (Fable) | **ALL PINNED**: R1 compares the legacy tooltip WHOLE and R1c refuses the denial anywhere on the page; R4 the whole legend line; W5 (a bad default ledger, a clean exported GXLEDGER: BAD); C17b (one key split across two baseline rows must sum); C19 asserts the reason; W1-W5 assert their branch's own first-line words; C2c/C2d; R1d.  Each has its mutant in the kill table |
| H3 | GLM, Astra, Fable | `d_nonote` is killed by C1's baseline mismatch, not by the note property | **CORRECTED**: its line says so; the COHERENT note-out (v1's key on both sides, a deliberate two-edit DESIGN mutant) `d_nonote2` is killed by exactly C15 and C16 |
| H4 | Fable, Astra | `run_mutants.py` (v2's table) runs `run_controls.py`, which is the v1 suite and crashes on the 7-field baseline: the 14/14 reproduced only in a staging copy | **FIXED**: `run_mutants.py` names `run_controls_v2.py` and takes CTL_*; v3's runner names `run_controls_v3.py`; the v3 receipts are of the staged files by md5 |
| H5 | Astra | the docstring promised rc 2 for a misshapen ledger, but `{"rows": null}` raised an uncaught exception | **FIXED**: the ledger walk is wrapped -- rc 2 "ledger misshapen", no traceback; C21a-c (`{"rows": null}`, a row that is not an object, a list) |
| H6 | Grok, Fable (exposure), main loop (measured) | the md5 pin hashes raw bytes; this machine's system git sets `core.autocrlf=true` (the repo's own config says false) | **FIXED on a measurement**: a fresh clone of an LF baseline here checked it out with md5 89d1d370 for 06a3ffc6, so the raw pin would red Q2 on every commit from a fresh clone.  The pin now folds CRLF to LF before hashing (the constant is unchanged); C18b |
| H7 | Grok | "editing such an entry means giving it a glyph, the ruling's way out" credits a NOTE-only toll to the ruling, which says nothing of note edits | **CORRECTED**: the toll is named as this check's |
| H8 | Fable | the docstring named one exit ("give it a glyph") where the hint names three | **CORRECTED**: "classify it -- a glyph, no `d`, or a non-answer record token" |
| H9 | Astra | the renderer comment's heading "NEITHER APPROVAL NOR A SEAT FAILURE" survives | **CORRECTED** (and it says what it used to say) |
| H10 | Fable | the renderer comment's "the reason first in its tooltip" is false on a refused-exemption cell | **CORRECTED** ("after a refused exemption's line, if any") |
| H11 | GLM | the summary's "%d frozen" counts passes, not the baseline; "(none exists)" is unchecked | **CORRECTED**: "%d within the frozen ceiling (baseline %d)"; the date paragraph gives the count -- 0 of 1,342 keys carry an empty or non-ISO date -- and says the ISO test is a SHAPE test, not a calendar one |
| H12 | Astra | RULINGS_C_records.md:44 calls the label "Astra's wording"; Astra's phrase was "legacy OK — verdict unclassified" | **CORRECTED AT COMMIT** (section 5c) |
| H13 | Astra, Fable | W1-W5 count failures with stand-in reporters, not the production good/bad and final exit | **DISCLOSED** in the controls' docstring; the production wiring is correct by inspection |
| H14 | main loop | a MISSING `d` on an ANSWER renders as the seat-failure glyph, and Q2 admits new ones (condition 1) | **FILED as `dashmissingd`** (LOW, a rule question for its own round) with its census (section 2b) |

## 2b. Premises to CHECK (stated as questions)

* **H1's narrower guarantee.**  Is a ceiling over (row, phase, seat, date, `d`, note sha1) the right thing to ship under
  RULINGS_C F2 ("an OK becomes ✓ only when a reader rewrites that one entry"), given that a revert and an `ev`-only
  replacement pass?  The alternative is entry identity with provenance (a comparison against HEAD's ledger, or persistent
  ids), which this round does not build.  Say which, and why.
* **H6's measurement.**  A temp repo with an LF copy of the baseline, cloned on this machine, gave md5 89d1d370 for the
  committed 06a3ffc6 (`core.autocrlf=true` in the system gitconfig, false in this repo's own config).  Is folding CRLF in
  the checker the right repair, as against a `.gitattributes` line?
* **H14's census** (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`, deriver `dashmissingd_census.py`): at HEAD 8bf8b5a1, 1,561 of
  5,177 entries are answers with no `d`, and 814 of 2,953 displayed answer cells show `…` because of it -- 682 of those,
  by a keyword screen of the note, record a real answer.  Is filing it (a rule question) right, rather than folding it
  into this round?  Is LOW right, beside `dashokclass`'s LOW and 670 cells?
* The seat entries this landing writes carry `d` ✓ for an answered seat whose changes were applied, and no `d` for a seat
  failure or a seat not fired (it renders `…`, which is what it was).  Is that the right practice while `dashmissingd`
  is open?
