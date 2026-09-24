# Round 2 -- reverse reconciliation: do the recorded, applied-but-uncommitted changes actually exist in the tree?

**Open with ONE line:** `VERDICT: <n> ABSENT of 81` (n = claims whose described change is not in the tree).
Then the per-claim table, then the per-class counts (they must sum to 81), then a seat record (model, what you read,
what you ran).  **READ-ONLY**: read files and run read-only git only; edit, stage, commit, delete, build and run nothing.

## Why

Round 1 (your earlier answer, `seats/codex_verify.txt` / `seats/grok_verify.txt` in the same directory) established
that no FILE was lost after the 2026-09-22 reboot, and proposed the check that would falsify the stronger claim: take
every RECORDED change that is said to have been applied and look for it in the tree.  One instance is already known:
`gdromdmadefault` entry [11] (2026-09-17) says four comment corrections were APPLIED, and one of them -- the comment
listing `dma alias` as an ARMING-arm byte store when it is a `default:`-arm store at +0x05 -- is not in the file:
`GXEMUL-SEC/regress/gdrom_default_probe.py:1187` still says "BOTH are on the ARMING arm".  It is present in both the
2026-09-21 and 2026-09-23 snapshots, so it was never applied rather than lost.

## Input

`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\verify_20260923\APPLIED_CLAIMS.txt` -- **81 numbered claims**, extracted
mechanically: every ledger entry dated 2026-09-15..2026-09-21 whose note uses an applied / corrected-in-place /
in-the-working-tree / re-pinned / past-tensed verb.  Each shows the row, entry index, date, seat, row state, the files
it names, and up to four excerpts around the verb.  The full entry text is in
`GXEMUL-SEC/tools/pipeline/ledger.json` (`rows[id=<row>].entries[<n>].note`).  The extractor is deliberately broad:
some matches will not describe a file change at all.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (HEAD
`f685d75`); ignore every other `src/` under the project root.

## For each claim, one class

* `PRESENT-WT` -- the described change is in the working tree and not in HEAD (cite `file:line`)
* `PRESENT-HEAD` -- the change is committed (cite the commit or `HEAD:file:line`)
* `ABSENT` -- the entry says it was applied, and the file does not carry it (cite the `file:line` that contradicts it)
* `SUPERSEDED` -- it was applied and a LATER recorded edit replaced it (cite both)
* `NOT-A-CHANGE` -- the verb matched but the sentence claims no edit to a file (for example "the finding now reads")
* `UNCHECKABLE` -- say exactly what is missing

**Calibration, and it is the test of your method:** the claim for `gdromdmadefault` entry [11] must come out `ABSENT`
for its `dma alias` correction.  If your method does not find that one, say so before reporting anything else.

Where one entry claims several changes, classify the entry by its worst part and list the parts.  Work through all 81;
if you must stop early, say at which claim number and give the counts for the ones you finished.
