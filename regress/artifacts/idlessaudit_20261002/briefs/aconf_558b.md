#558 -- the twelve repairs of your aconf_558: right?

Open with the token `ASTRA558B_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `e1871fa5`; files
under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idlessaudit_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf558.diff` (8 hunks: the four drafts and `AGY_FLAGS_DISPOSITION.md`,
which is now v3).  Generator: `draft\prep558.py.txt`.  Each of your twelve items was checked against its file before
the edit (`#555`'s CHANGELOG lines 85/94: 130 rows, 37 ledger rows; `armcp15cp14exits` filed by `#554` at `1202d342`
from queue lines 18721-18722; nine `cpu->running = 0` in `dev_mb89352.c`; `icite2_2`'s twenty ids sit at
`IDLESS_TABLE2.tsv` rows 111-130).

For each of your items 1-12: `<n> | RIGHT / WRONG: <why, path:line>` -- is the repair exactly what the item asked, and
is any copy of the corrected wording left (a quotation of the corrected-away text, marked as such, does not count)?
Then: anything else in the 8 hunks.  End with `DENOMINATOR: <h> of 8 hunks read`.
