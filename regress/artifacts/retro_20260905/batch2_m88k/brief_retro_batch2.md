# RETROSPECTIVE FIX REVIEW, BATCH 2 OF THE ASTRA + FABLE RE-CHECK -- the m88k CPU fixes shipped 2026-08-01..2026-08-12 (two commits), reviewed against the tree at HEAD by GPT-6 Astra at max effort; a Fable 5.1 pass adjudicates the findings.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `2bb9cb4`).  There are THREE
pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).
They are NOT this fork.  If your line numbers disagree with the CHANGELOG's by hundreds you are reading one of them -- say so
rather than reconciling.

**If you cannot read files that is expected** -- name any premise you cannot settle rather than guessing at it.  (This
batch is addressed to a FILE-READING seat; everything below is a pointer into the tree plus the questions.)

**Where this brief or a record states an ARITHMETIC claim -- a field range, an encoding count, a rounding case -- ENUMERATE
it rather than reasoning about it.**  Walk the values.  A derivation that skips one masking line reads exactly like a
correct one.  **And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER of these values can
actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation: one line per commit (`HOLDS` / `DEFECT` / `RECORD`) and one
batch line.

## CITE BY GREP ANCHOR, NOT BY LINE NUMBER

Same-file references positional or by construct name; cross-file references as a VERIFIED-UNIQUE grep anchor
(`grep -n '<anchor>' <file>`).  A grep anchor that matches nothing is loud; a wrong number is silent.

## WHAT THIS BATCH IS

The owner asked (2026-09-04) that previously shipped fixes be re-reviewed by GPT-6 Astra at max effort and adjudicated
by Fable 5.1.  The chosen scope is every product fix in `src/devices` and `src/cpus` since 2026-08-01, batched by file,
oldest first.  Each round below shipped a CHANGELOG block (`grep -n '^# Round NN\|^# #NNN' GXEMUL-SEC/CHANGELOG.md` finds it;
the newest blocks are at the TOP of the file), a product diff, and a detector (a gate row under `GXEMUL-SEC/regress/`;
`grep -rn '#NNN' GXEMUL-SEC/regress/*.sh GXEMUL-SEC/regress/*.py GXEMUL-SEC/regress/*.c` finds the rows that cite the round).  This is batch 2: the m88k CPU fixes.  The primary source is on disk: `_scratchpad/mc88100.txt` (the MC88100 user's manual, pdftotext; tables can stagger names against values -- calibrate on a row the tree already pins before citing a table value, and prefer the prose).

## THE COMMITS (oldest first; `git -C GXEMUL-SEC show --format= <sha> -- <file>` gives the diff WITHOUT the message)

| sha | date | round | subject |
|---|---|---|---|
| d12114d | 2026-08-01 | #323 | bcnd rejected two thirds of its own condition masks |
| ed242c0 | 2026-08-12 | #380 | the m88k idle fold ran the bcnd.n delay slot zero times |

Files: `src/cpus/cpu_m88k.c`, `src/cpus/cpu_m88k_instr.c`, `src/cpus/generate_m88k_bcnd.c`, `src/cpus/tmp_m88k_bcnd.c` (GENERATED from the generator -- check the two agree).  Later commits may have touched the same lines; review each fix AS IT STANDS AT HEAD, and say when a later round changed it.

## SETTLED PREMISES, RE-INLINED (each is a QUESTION if you can check it)

1. **bcnd's M5 condition field** is a five-bit mask over {reserved, gt0, eq0, lt0, ...} in the MC88100 manual's `bcnd` page; the pre-fix decoder accepted only a subset of the legal masks and treated the rest as illegal.  Enumerate all 32 values of the field against the manual and against `tmp_m88k_bcnd.c` at HEAD.
2. **The idle fold** (#380) short-circuits a tight `bcnd.n` self-loop; the delay slot of a `.n` branch must execute exactly once per taken branch.  Check the fold's condition at HEAD and its gate row.
3. **The generator and its output are BOTH in the tree** -- a fix landing in one and not the other is the class to look for.

## QUESTIONS (answer per commit, then for the batch)

1. **IS THE FIX RIGHT AT HEAD?**  Read the shipped hunks as they stand now.  For arithmetic and encodings, ENUMERATE
   (the twenty-four encodings; the FPSCR bit positions; the straddle split).  Cite the manual by extracted-text line
   (`grep -n` in the `_scratchpad/mc88100.txt` file) for every architectural claim you rely on.
2. **DOES ITS DETECTOR STILL PIN IT?**  Name the gate and the row (grep anchor).  Name the smallest edit to the fixed
   code that reverts the fix's EFFECT and would pass the detector at HEAD -- and if none exists, say what row makes it
   impossible.  A detector whose rows only round-trip a value against itself is the anchor-rule failure; say so if you
   see it.
3. **IS THE RECORD HONEST?**  The CHANGELOG block's claims (measured kills, counts, manual citations) against the tree
   and the manuals.  A count without a deriver, a citation to a page that says something else, a "measured" number with
   no artifact -- name them.  Corrections that landed only in a later paragraph while the original sentence stands are
   the class this project keeps finding.
4. **THE SMALLEST LIVE DEFECT**, if any: something a GUEST can reach at HEAD in these files that the rounds did not fix
   or introduced.  State it with a measurable consequence (a value, a row that would red, a halt) or do not state it.
5. **VERDICT PER COMMIT** -- `HOLDS` (fix right, detector pins it, record honest), `DEFECT` (a live defect with a
   measurable consequence: this becomes a queue item), `RECORD` (a wrong record to correct in place) -- and a one-line
   BATCH VERDICT with what you could not check (read-only workspace: say what a measuring seat should build).

If, while verifying a claim, you found something ELSE -- say so.  agy is deliberately not fired on this batch; a Fable 5.1
pass adjudicates your findings and decides which become rounds.
