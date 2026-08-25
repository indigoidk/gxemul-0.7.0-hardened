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

## What is preserved, and the rule — ADJUDICATED 2026-08-24 after two seats disagreed

> **Preserve the COMPLETE FINAL table (every mutant log, cited or not), plus any log a
> durable record cites, plus the driver and a manifest. Do NOT auto-preserve a transient run
> that a later same-config run supersedes and that no record cites.**

Two seats split on this and the rule is the synthesis, not a compromise.

**codex** wanted a prospective cap — keep the final table, any superseded log used to support
a correction, the driver summary and a manifest; do not preserve every transient forever. It
also said *"only files individually cited is too narrow."*

**opus5** refused a cite-based cap **and supplied the proof**: the cite list is written
*before* anyone knows which log an audit will want. `#461` is the measured case — **its
lethal-mutant per-row log was never cited, and it is exactly what the 2026-08-24 audit
needed and could not find.**

The rule keys on **ROLE, not citation**, which satisfies both: "the complete final table"
keeps `#461`'s uncited log, because that log was part of its final table — so the cite-based
cap is refuted by measurement, not by argument. And "not every transient" keeps it bounded to
one final table per round plus memorial logs, rather than every throwaway ask-again run.

**The existing `#462` archive is not reverted** and already conforms: `table1_52rows/` and
`table2_57rows/` are memorial logs cited by corrections, `table3_58rows/` is the final table,
and `table462.results` is the driver record.

*Cost, measured rather than argued: 356 KB on disk, 8,379 bytes gzipped — a 42:1 ratio,
because kill tables are near-identical fixed-column row lists. Git stores blobs compressed and
deltas near-identical files within a pack, so a round costs single-digit KB against a 177 MB
`.git`. The "grows 200 KB per round forever" objection was the DISK figure, and it is the
wrong number to decide on.*
