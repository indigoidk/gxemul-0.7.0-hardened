# The `/bin/false` null medium -- prediction, written before the run (its mtime precedes `false.out`'s)

From the #580 regress review (`../adj_20261104/FABLE_REGRESS.md`, floor (c)): a binary that exits 1 with no output greens the
sixteen stop rows (absence rows, as on `/bin/true` and the absent binary) AND the `neg` row (it wants exit 1), so the shipped
122-row probe scores **17/122**, with `MIPS_PRIMUNDEC_CONTROL=FAIL` (every other control still red) and the `r59 mdmx notRI` row
red (noread).  The review filed it with no row owed; this leg measures it instead.
