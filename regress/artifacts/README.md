# Cited measurement logs

**Every score a round block cites must resolve to a path that EXISTS.** Precommit section X
(`tools/pipeline/check_cited_artifacts.py`) enforces that mechanically.

These logs live **in the repo, by owner decision (2026-08-24)**, and the reason is the one
thing the untracked alternative could not give: *a citation is only re-derivable if the
artifact travels with the record.* Before this, the archive sat in `_scratchpad/` — outside
the git root, untracked — so section X's green certified existence **on one machine**, and a
fresh clone would have failed every post-462 citation.

## Layout, and why it is table-stamped

    kill462/
        table1_52rows/    the first table's per-mutant logs
        table2_57rows/    the second's
        table3_58rows/    the third's
        table462.results  the driver's own running record

**One round can run several tables**, and each writes a `probe_<mutant>.raw` per mutant. Flat
storage therefore collides: `#462` ran three tables, so three different `probe_M11.raw` files
exist and only the directory stamp distinguishes them. That is not hypothetical — `#462`'s
round block cited `probe_base.raw` for a 52/52 score, a later table overwrote that filename,
and the claim became **contradicted by its own evidence** rather than merely unverifiable.

Section X matches a cited directory **component-wise**, so `table2_57rows/probe_M11.raw` can
only be satisfied by a file at that path — a basename fallback would rebuild the very reuse
defect this layout exists to prevent.

## What is NOT here

`#462`'s 57-row **base** log, and `#461`'s `m_dmarevert` per-row results. Both were lost to
filename reuse before archiving existed, and both are recorded as lost rather than cited:
`#461`'s detector is consequently **not auditable** for the lethal-only class, which is a
measured coverage cap and not a guess — see `killartifacts` in the queue file.
