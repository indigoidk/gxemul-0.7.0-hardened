# RETROSPECTIVE FIX REVIEW, BATCH 3a OF THE ASTRA + FABLE RE-CHECK -- the dev_wdc.c (IDE/ATAPI) fixes shipped 2026-08-02..2026-08-26 (seven commits, eight round numbers), reviewed against the tree at HEAD by GPT-6 Astra at max effort; a Fable 5.1 pass adjudicates the findings.

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
`grep -rn '#NNN' GXEMUL-SEC/regress/*.sh GXEMUL-SEC/regress/*.py GXEMUL-SEC/regress/*.c` finds the rows that cite the round).  This is batch 3a: the older half of the dev_wdc.c fixes (the 2026-08-27..30 ATAPI chain #473-#495 is batch 3b).  **NO ATA/ATAPI standard is on disk** -- cite the source and the shipped differentials, and where the standard is load-bearing, say WHICH document (ATA/ATAPI-6, SFF-8020i) and section would settle it rather than asserting it.

## THE COMMITS (oldest first; `git -C GXEMUL-SEC show --format= <sha> -- <file>` gives the diff WITHOUT the message)

| sha | date | round | subject |
|---|---|---|---|
| 052982a | 2026-08-02 | #337 | four guest-reachable exit(1) calls in the IDE controller |
| c941fe3 | 2026-08-03 | #341 | dev_wdc's ATAPI read accounted for bytes it never delivered |
| 2e709cd | 2026-08-14 | #405 | ATA IDENTIFY packed its capacity bytes with `% 255`, not `& 255` |
| 085766a | 2026-08-14 | #407 | #405's detector had four holes and a note that was wrong the flattering way |
| e86e293 | 2026-08-14 | #408 | the round that fixed stale citations made the identical error, and the detector was relying on -O2 to hide UB |
| 154d21c | 2026-08-14 | #414 | every -d g disk and every floppy reported zero capacity, from one multiplication with two factors nobody computed |
| baacf9b | 2026-08-26 | #464 | six unlatched fatal() bounded, and the detector's first gate |

Files: `src/devices/dev_wdc.c`; detectors `regress/diff_wdc_identify.c`, `regress/wdc_flood_probe.py`, `regress/wdc_latch_census.py`, and the gate rows citing each round.  Later commits may have touched the same lines; review each fix AS IT STANDS AT HEAD, and say when a later round changed it.

## SETTLED PREMISES, RE-INLINED (each is a QUESTION if you can check it)

1. **#337's four exit(1) sites** became latched `fatal()` declines (`warned_badlen` is the tree's REFERENCE latch, cited by other devices); a later round (#464) bounded six more unlatched fatal()s.  Enumerate the remaining `exit(` and unlatched `fatal(` sites in the file at HEAD.
2. **#405/#407/#408** are one chain: IDENTIFY's capacity words, the differential that pins them, and two corrections of the record about it.  The `% 255` -> `& 255` fix and the `-O2`-hidden UB in the detector are checkable by reading.
3. **#414's zero capacity** was a multiplication whose two factors were never computed for `-d g` disks and floppies; the fix computes them.  Check the geometry arithmetic by enumeration for one small disk.
4. **The 2026-08-27..30 chain (#473..#495) touched the SAME functions** -- a batch-3a fix may stand modified; say so per commit rather than grading the old hunk.

## QUESTIONS (answer per commit, then for the batch)

1. **IS THE FIX RIGHT AT HEAD?**  Read the shipped hunks as they stand now.  For arithmetic and encodings, ENUMERATE
   (the twenty-four encodings; the FPSCR bit positions; the straddle split).  Cite the manual by extracted-text line
   (`grep -n` in the source and the shipped differentials) for every architectural claim you rely on.
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
