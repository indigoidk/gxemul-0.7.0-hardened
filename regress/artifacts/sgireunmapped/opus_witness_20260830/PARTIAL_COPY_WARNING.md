# `table_final.txt` HERE IS A SUPERSEDED INTERMEDIATE. THE COMPLETED RESCORE IS `table2_repaired.txt`.

## The record this file used to carry was WRONG, and it is corrected in place

An earlier version of this file said the rescore *"died and will never finish"*.  **It
finished — 9 of 9, sentinel `RESCORE2_DONE`.**  That claim was mine, it was wrong, and it was
committed before it was checked.

## What is actually here

    table_final.txt        3,519 b   00:12:04   2 of 9 scored, NO sentinel   <- superseded
    table2_repaired.txt   13,458 b   00:25:29   9 of 9, RESCORE2_DONE        <- THE RESULT
    table1_scores.txt      1,802 b   00:09:12   9 of 9, TABLE_DONE           <- first table

**Two independent tables, nine variants each, and they agree:**

    base 10/14   fix 14/14   mret0 12/14   mlatch 13/14   mwonly 11/14
    mshrink 13/14   mshrinkb 13/14   mtexshrink 13/14   mnolatch 13/14

`base` is RED (test-first).  `fix` is the only clean sweep.  `mnolatch` reads **13/14** rather
than the 14/14 of the first run, and that single difference is the whole point: it is the row
that COULD NOT FAIL until the `pc`-cache defect in the shared harness was repaired.  The two
runs disagreeing on exactly one variant, for exactly the predicted reason, is stronger evidence
than two identical runs would have been.

## Why I got it wrong — and it was NOT the reason first proposed

The measuring seat attributed my error to *"a process check run from the Windows side cannot
see WSL processes"*.  **That is not what happened**, and the distinction matters because the
wrong lesson would be learned from it.  Checked deliberately, from BOTH sides:

    WSL side:  size=3519  mtime=2026-08-31 00:12:04
    WIN side:  size=3519  mtime=00:12:04

Both agreed.  There was no stale metadata and no invisible process.

**THE ACTUAL CAUSE: TWO FILES SHARING ONE NAME IN TWO DIRECTORIES.**  The rescore wrote to
`opussgire/table_final.txt` — the scratch **root** — which reached 13,458 bytes at 00:24:03.
The copy I was watching was `opussgire/artifacts/table_final.txt`, a stale intermediate that
was last written at 00:12:04 and never touched again.  I stat'd the wrong one, saw no growth
and no processes, and concluded death.

The seat made the mirror error in its addendum: it reported *"table_final.txt: mtime 00:24:03,
13,458 bytes"* — the **root** file — while correcting a warning about the **artifacts** file.
Both of us named a path we had not disambiguated.

> **A FILENAME IS NOT AN IDENTIFIER WHEN IT EXISTS TWICE.  Cite the path, and stat the path
> you cite.**  This is the citation-form rule one level down: a bare basename is the
> filesystem's version of a bare line number.

## The methodological point that survives unchanged

Count `^SCORE` lines, not `VARIANT` headers.  A started variant and a finished one look
identical from the header — which is how an earlier draft of this file said "three variants"
where the honest count was two.  By that same metric, `table2_repaired.txt` reads a genuine
9 of 9.
